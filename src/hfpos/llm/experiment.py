"""Scoring boundaries and small-sample summaries for the positioning audit.

No LLM calls. These functions do not decide whether text crosses a boundary;
that is the independent human coders' job.
"""
from __future__ import annotations

from math import comb

import numpy as np
import pandas as pd
from scipy.stats import binomtest

MODEL_ARMS = frozenset({"C-bare", "C-ann", "D"})
ARMS = frozenset({"A", "B", *MODEL_ARMS})


def composite(b2: int | None, b3: int | None, residual: int | None = None,
              *, include_residual: bool = False) -> int | None:
    """Three-valued OR. Missing/NA never silently becomes safe (zero)."""
    values = [b2, b3] + ([residual] if include_residual else [])
    if any(x is not None and x not in (0, 1, 2, 3) for x in values):
        raise ValueError("codes must be 0..3 or None")
    if any(x is not None and x >= 2 for x in values):
        return 1
    return None if any(x is None for x in values) else 0


def contrast_components(arm_a: str, arm_b: str) -> tuple[str, ...]:
    """Both sides receive the SAME endpoint; A/B comparisons never include R."""
    if arm_a not in ARMS or arm_b not in ARMS or arm_a == arm_b:
        raise ValueError("need two distinct known arms")
    return ("B2", "B3", "R") if {arm_a, arm_b} <= MODEL_ARMS else ("B2", "B3")


def binary_agreement(a, b) -> dict:
    """Unweighted Cohen kappa, agreement and prevalence; constants are indeterminate."""
    if len(a) != len(b):
        raise ValueError("coder vectors differ in length")
    valid = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if any(x not in (0, 1) or y not in (0, 1) for x, y in valid):
        raise ValueError("binary values required")
    if not valid:
        return {"n_joint": 0, "n_not_jointly_scored": len(a), "raw_agreement": None,
                "kappa": None, "reason": "no jointly scored responses"}
    x, y = np.asarray(valid, dtype=float).T
    observed = float((x == y).mean())
    expected = float(x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean()))
    kappa = (observed - expected) / (1 - expected) if expected < 1 else None
    return {"n_joint": len(valid), "n_not_jointly_scored": len(a) - len(valid),
            "raw_agreement": observed, "kappa": kappa,
            "coder1_events": int(x.sum()), "coder2_events": int(y.sum()),
            "reason": "constant ratings; kappa undefined" if kappa is None else None}


def paired_summary(bare, annotated, confidence: float = .95) -> dict:
    """Exact McNemar and conservative matched risk-difference interval.

    Interval projects simultaneous Bonferroni Clopper-Pearson bounds for the two
    discordant-cell probabilities. Coverage is at least the stated level under
    independent week pairs. It is conservative and is NOT Holm-simultaneous
    across products. Unlike a naive bootstrap, all-zero data do not imply [0,0].
    """
    if len(bare) != len(annotated) or not 0 < confidence < 1:
        raise ValueError("invalid paired data or confidence")
    pairs = [(x, y) for x, y in zip(bare, annotated) if x is not None and y is not None]
    if any(x not in (0, 1) or y not in (0, 1) for x, y in pairs):
        raise ValueError("binary values required")
    n = len(pairs)
    if not n:
        return {"n_paired": 0, "n_missing_pairs": len(bare), "p_exact": None}
    x, y = np.asarray(pairs, dtype=int).T
    b, c = int(((x == 1) & (y == 0)).sum()), int(((x == 0) & (y == 1)).sum())
    marginal_confidence = 1 - (1 - confidence) / 2
    ci_b = binomtest(b, n).proportion_ci(marginal_confidence, method="exact")
    ci_c = binomtest(c, n).proportion_ci(marginal_confidence, method="exact")
    return {"n_paired": n, "n_missing_pairs": len(bare) - n,
            "both_zero": int(((x == 0) & (y == 0)).sum()),
            "bare_only": b, "annotated_only": c, "both_one": int(((x == 1) & (y == 1)).sum()),
            "bare_rate": float(x.mean()), "annotated_rate": float(y.mean()),
            "delta_annotated_minus_bare": (c - b) / n,
            "delta_ci_low": float(ci_c.low - ci_b.high),
            "delta_ci_high": float(ci_c.high - ci_b.low),
            "p_exact": float(binomtest(b, b + c).pvalue) if b + c else 1.0,
            "ci_method": "conservative paired CP projection; independent week pairs"}


def exact_power(n: int, p_bare_only: float, p_ann_only: float, alpha: float = .0125) -> float:
    """Enumerate discordance counts. Fixed cutoff, NOT full Holm family power."""
    if n < 1 or min(p_bare_only, p_ann_only) < 0 or p_bare_only + p_ann_only > 1:
        raise ValueError("invalid sample size or probabilities")
    power = 0.0
    for b in range(n + 1):
        for c in range(n - b + 1):
            pv = binomtest(b, b + c).pvalue if b + c else 1.0
            if pv <= alpha:
                power += (comb(n, b) * comb(n - b, c) * p_bare_only ** b * p_ann_only ** c
                          * (1 - p_bare_only - p_ann_only) ** (n - b - c))
    return float(power)


def calendar_quarter_sensitivity(dates, bare, annotated, n_boot: int = 5000,
                                 seed: int = 20261106) -> dict:
    """Resample calendar-quarter clusters; descriptive sensitivity, not primary p-value."""
    if not (len(dates) == len(bare) == len(annotated)):
        raise ValueError("vectors differ in length")
    if any(x not in (0, 1) or y not in (0, 1) for x, y in zip(bare, annotated)
           if x is not None and y is not None):
        raise ValueError("binary paired outcomes required")
    rows = [(date, y - x) for date, x, y in zip(dates, bare, annotated)
            if x is not None and y is not None]
    if not rows:
        return {"estimable": False, "reason": "no paired observations"}
    f = pd.DataFrame(rows, columns=["date", "delta"])
    if not f.delta.isin([-1, 0, 1]).all():
        raise ValueError("binary paired outcomes required")
    f["quarter"] = pd.to_datetime(f.date).dt.to_period("Q")
    clusters = [g.delta.to_numpy(float) for _, g in f.groupby("quarter")]
    if len(clusters) < 2 or f.delta.nunique() < 2:
        return {"estimable": False, "n_quarters": len(clusters),
                "reason": "too few quarters or no variation; do not report a zero-width interval"}
    rng = np.random.default_rng(seed)
    means = [np.concatenate([clusters[j] for j in rng.integers(len(clusters), size=len(clusters))]).mean()
             for _ in range(n_boot)]
    if np.ptp(means) == 0:
        return {"estimable": False, "n_quarters": len(clusters), "reason": "degenerate resampling"}
    lo, hi = np.quantile(means, [.025, .975])
    return {"estimable": True, "n_quarters": len(clusters), "n_boot": n_boot,
            "ci_low": float(lo), "ci_high": float(hi), "seed": seed,
            "method": "calendar-quarter cluster percentile bootstrap; sensitivity only"}
