"""Stage-1 diagnostics for the Milestone 2 report.

Produces every Stage-1 number and figure the report cites, so each one is
traceable to a command rather than to a notebook cell someone ran once.

    python scripts/stage1_report.py
"""

from __future__ import annotations

import warnings

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from hfpos import config  # noqa: E402
from hfpos.features.build import TARGET, build, feature_columns  # noqa: E402
from hfpos.ingest import cftc  # noqa: E402
from hfpos.stage0 import leadlag  # noqa: E402
from hfpos.stage1.models import MODELS, make_estimator  # noqa: E402
from hfpos.stage1.run import diagnostics, run  # noqa: E402

warnings.filterwarnings("ignore")

ZSCORE_WINDOW = 52
ERAS = {"2013-2016": ("2013-01-01", "2016-12-31"),
        "2017-2019": ("2017-01-01", "2019-12-31"),
        "2020-2022": ("2020-01-01", "2022-12-31"),
        "2023-2026": ("2023-01-01", "2026-12-31")}


def model_comparison(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    rows, results = [], {}
    for model in MODELS:
        result = run(frame, model)
        results[model] = result
        diag = diagnostics(result, model)
        diag["implied_corr_sqrt_1_minus_r2"] = float(np.sqrt(max(1 - diag["oos_r2"], 0)))
        rows.append(diag)
    return pd.DataFrame(rows), results


def era_breakdown(result: pd.DataFrame) -> pd.DataFrame:
    from hfpos.stage1.run import oos_r2

    rows = []
    for label, (start, end) in ERAS.items():
        chunk = result.loc[start:end]
        if chunk.empty:
            continue
        rows.append({
            "era": label, "n": len(chunk),
            "oos_r2": oos_r2(chunk["actual"].to_numpy(), chunk["expected"].to_numpy(),
                             chunk["benchmark"].to_numpy()),
            "corr_residual_raw": float(chunk["residual"].corr(chunk["actual"])),
        })
    return pd.DataFrame(rows)


def coefficients(frame: pd.DataFrame) -> pd.DataFrame:
    """Ridge coefficients from a single fit on the full usable sample.

    For description only. Every number used as a RESULT comes from the
    walk-forward fits; this is here to say which features carry weight.
    """
    usable = frame.dropna()
    features = feature_columns(usable)
    estimator = make_estimator("ridge", config.load()["inference"]["bootstrap"]["seed"])
    estimator.fit(usable[features].to_numpy(float), usable[TARGET].to_numpy(float))
    coefs = pd.Series(estimator.named_steps["est"].coef_, index=features)
    return (coefs.reindex(coefs.abs().sort_values(ascending=False).index)
            .rename("standardised_coefficient").to_frame())


def zscore_benchmark(frame: pd.DataFrame, result: pd.DataFrame) -> pd.DataFrame:
    """Is the ML residual a different notion of 'unusual' than a 52-week z-score?"""
    positions = cftc.load("UST_10Y")
    net_oi = positions["leveraged_funds_net"] / positions["open_interest"]
    z = ((net_oi - net_oi.rolling(ZSCORE_WINDOW).mean())
         / net_oi.rolling(ZSCORE_WINDOW).std()).reindex(result.index)
    joined = pd.DataFrame({"residual": result["residual"], "raw_change": result["actual"],
                           "zscore_level": z}).dropna()
    return pd.DataFrame([{
        "corr_residual_raw_change": float(joined["residual"].corr(joined["raw_change"])),
        "corr_residual_zscore": float(joined["residual"].corr(joined["zscore_level"])),
        "corr_raw_change_zscore": float(joined["raw_change"].corr(joined["zscore_level"])),
        "n": len(joined),
    }])


def arm_c_stimuli(result: pd.DataFrame) -> pd.DataFrame:
    """The numbers Arm C actually shows the LLM, for the drawn sample weeks.

    Expected LEVEL is the previous week's net/OI plus the model's predicted change,
    so the residual in levels equals the residual in changes. Weeks with no
    out-of-sample prediction are kept, marked, and excluded from the C arms.
    """
    positions = cftc.load("UST_10Y")
    net_oi = positions["leveraged_funds_net"] / positions["open_interest"]
    sample = pd.read_csv(config.REPO_ROOT / "docs/milestone1/sample.csv", parse_dates=["week"])

    rows = []
    for _, row in sample.iterrows():
        week = row["week"]
        has = week in result.index
        expected_level = (net_oi.shift(1).get(week, np.nan) + result["expected"].get(week, np.nan)
                          if has else np.nan)
        rows.append({
            "week": week.date(), "frame": row["frame"], "stratum": row["stratum"],
            "actual_net_over_oi": float(net_oi.get(week, np.nan)),
            "expected_net_over_oi": float(expected_level) if has else np.nan,
            "residual": float(result["residual"].get(week, np.nan)) if has else np.nan,
            "has_model_output": has,
        })
    return pd.DataFrame(rows)


def figures(result: pd.DataFrame, cross: pd.DataFrame) -> None:
    out = config.path("figures")

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.scatter(result["actual"] * 100, result["residual"] * 100, s=8, alpha=0.45,
               color="#1f3a5f", edgecolors="none")
    lo, hi = result["actual"].min() * 100, result["actual"].max() * 100
    ax.plot([lo, hi], [lo, hi], color="#c0392b", lw=1.1, ls="--", label="residual = raw change")
    ax.set_xlabel("raw weekly change in net/OI (% of open interest)")
    ax.set_ylabel("Stage-1 residual (% of open interest)")
    ax.set_title(f"The residual is the raw series: r = {result['residual'].corr(result['actual']):.3f}")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(out / "stage1_residual_vs_raw.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    colors = ["#c0392b" if k < 0 else "#1f3a5f" if k > 0 else "#7f8c8d" for k in cross["lag_k"]]
    ax.bar(cross["lag_k"], cross["corr"], color=colors)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xlabel("k   (negative: returns lead positioning   positive: positioning leads returns)")
    ax.set_ylabel("corr(d net/OI at t, return at t+k)")
    ax.set_title("Positioning follows returns; it does not lead them")
    fig.tight_layout(); fig.savefig(out / "stage0_lead_lag.png", dpi=200); plt.close(fig)


def main() -> None:
    tables = config.path("tables")
    frame = build()

    comparison, results = model_comparison(frame)
    comparison.to_csv(tables / "stage1_model_comparison.csv", index=False)
    print(comparison.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    best = results["ridge"]
    era_breakdown(best).to_csv(tables / "stage1_era_breakdown.csv", index=False)
    coefficients(frame).to_csv(tables / "stage1_ridge_coefficients.csv")
    zscore_benchmark(frame, best).to_csv(tables / "stage1_zscore_benchmark.csv", index=False)

    stimuli = arm_c_stimuli(best)
    stimuli.to_csv(config.REPO_ROOT / "docs/milestone2/arm_c_stimuli.csv", index=False)

    stage0 = leadlag.run(frame.dropna())
    figures(best, stage0["cross_correlations"])

    print("\nera breakdown\n", era_breakdown(best).to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print("\ntop ridge coefficients\n", coefficients(frame).head(10).to_string(float_format=lambda v: f"{v:+.5f}"))
    print("\nz-score benchmark\n", zscore_benchmark(frame, best).to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\narm C coverage: {int(stimuli['has_model_output'].sum())} of {len(stimuli)} drawn weeks")


if __name__ == "__main__":
    main()
