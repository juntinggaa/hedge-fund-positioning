"""Versioned Arm C / D stimuli from the model v2 selection.

    python scripts/model_v2.py          # first: produces predictions + selection.json
    python scripts/build_stimuli_v2.py

Writes docs/model_v2/model_card_v2.json (the single source for every number in the
v2 annotation) and docs/milestone2/arm_c_stimuli_v2.csv. The v1 stimuli file is
never touched.

Uncertainty, defensibly: for week t the 90% band is expected_t +/- 1.645 x RMSE of
the model's out-of-sample errors in weeks BEFORE t, and the residual's percentile
is its |size| rank among those prior errors. Weeks with fewer than 52 prior
errors get no band.
"""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.ingest import cftc
from hfpos.model_v2 import VERSION
from hfpos.model_v2.features import trailing_percentile

ROOT = config.REPO_ROOT
PLACEBO_SEED = 20261104          # same seed as v1 arm D
MIN_PRIOR = 52
Z90 = 1.645


def prior_stats(pred: pd.DataFrame) -> pd.DataFrame:
    err = (pred["actual"] - pred["pred"]).to_numpy()
    rmse, past = np.full(len(err), np.nan), []
    for i in range(len(err)):
        if len(past) >= MIN_PRIOR:
            rmse[i] = float(np.sqrt(np.mean(np.square(past))))
        past.append(err[i])
    return pd.DataFrame({"prior_rmse": rmse, "prior_n": np.arange(len(err))}, index=pred.index)


def band_coverage(pred: pd.DataFrame) -> float:
    """Share of eligible weeks whose actual change fell inside +/- Z90 x prior RMSE."""
    err = (pred["actual"] - pred["pred"]).to_numpy()
    hits = [abs(err[i]) <= Z90 * np.sqrt(np.mean(err[:i] ** 2))
            for i in range(MIN_PRIOR, len(err))]
    return float(np.mean(hits))


def pct_of_prior(err_series: pd.Series, week, value: float) -> float:
    prior = err_series.loc[:week].iloc[:-1].abs()
    return float((prior < abs(value)).mean()) if len(prior) >= MIN_PRIOR else np.nan


def main() -> None:
    sel = json.loads((ROOT / "reports/model_v2/selection.json").read_text())
    name = sel["selected"]
    pred = pd.read_parquet(ROOT / f"data/processed/model_v2/{name}.parquet")
    table = pd.read_csv(ROOT / "reports/model_v2/comparison.csv").set_index("candidate")
    row = table.loc[name]
    err = pred["actual"] - pred["pred"]

    pos = cftc.load("UST_10Y")
    s = pos["leveraged_funds_net"] / pos["open_interest"]
    level_pct = trailing_percentile(s)
    stats = prior_stats(pred)

    sample = pd.read_csv(ROOT / "docs/milestone1/sample.csv", parse_dates=["week"])
    rows = []
    for _, r in sample.iterrows():
        w = r["week"]
        has = w in pred.index and not np.isnan(stats["prior_rmse"].get(w, np.nan))
        prev = float(s.shift(1).get(w, np.nan))
        exp_level = prev + float(pred["pred"].get(w, np.nan)) if has else np.nan
        resid = float(err.get(w, np.nan)) if has else np.nan
        band = Z90 * float(stats["prior_rmse"].get(w, np.nan)) if has else np.nan
        rows.append({
            "week": w.date(), "frame": r["frame"], "stratum": r["stratum"],
            "model_version": VERSION, "model_id": name, "has_model_output": has,
            "prev_net_over_oi": prev, "actual_net_over_oi": float(s.get(w, np.nan)),
            "expected_net_over_oi": exp_level, "residual": resid,
            "band90_halfwidth": band,
            "residual_abs_pct_vs_prior": pct_of_prior(err, w, resid) if has else np.nan,
            "level_pct_prior_260w": float(level_pct.get(w, np.nan)),
        })
    out = pd.DataFrame(rows)

    covered = out["has_model_output"].to_numpy(bool)
    shuffled = np.random.default_rng(PLACEBO_SEED).permutation(out.loc[covered, "residual"].to_numpy())
    out["placebo_residual"] = np.nan
    out.loc[covered, "placebo_residual"] = shuffled
    out["placebo_expected_net_over_oi"] = out["actual_net_over_oi"] - out["placebo_residual"]
    out["placebo_residual_abs_pct_vs_prior"] = [
        pct_of_prior(err, pd.Timestamp(w), v) if c else np.nan
        for w, v, c in zip(out["week"], out["placebo_residual"], covered)]
    out.to_csv(ROOT / "docs/milestone2/arm_c_stimuli_v2.csv", index=False)

    sources = sorted((ROOT / "src/hfpos/model_v2").glob("*.py")) + [
        ROOT / "scripts/model_v2.py", ROOT / "scripts/build_stimuli_v2.py"]
    code_hash = hashlib.sha256(b"".join(f.read_bytes() for f in sources)).hexdigest()
    card = {
        "model_version": VERSION, "model_id": name,
        "description": "ridge on 40 v1 'extended' features, scaler and alpha (logspace(-2,4,13)) "
                       "fitted inside every inner TimeSeriesSplit(4) fold; expanding window, "
                       "min 260 weeks, refit every 13 weeks",
        "target": "weekly change in leveraged-fund net / open interest, UST 10Y futures-only TFF",
        "expected_level": "previous week's actual net/OI + predicted change",
        "spec": "docs/model_v2/SPEC_2026-11-05.md",
        "selection_reason": sel["reason"],
        "eval_weeks": sel["common_weeks"],
        "oos_r2_vs_historical_mean": round(float(row["r2_vs_mean"]), 4),
        "oos_r2_vs_zero_change": round(float(row["r2_vs_zero"]), 4),
        "oos_rmse_pp_of_oi": round(float(row["rmse"]) * 100, 2),
        "corr_residual_actual_change": round(float(row["corr_resid_actual"]), 3),
        "mincer_zarnowitz_slope": round(float(row["mz_slope"]), 2),
        "predictions_sha256": hashlib.sha256(pred.to_csv().encode()).hexdigest(),
        "code_sha256": code_hash,
        "band90_historical_coverage": round(band_coverage(pred), 3),
        "description_of_estimate": "retrospective same-week conditional estimate (not a pre-release nowcast: d_log_oi uses this week's CFTC open interest)",
        "arm_c_coverage": f"{int(covered.sum())} of {len(out)} sampled weeks",
        "weeks_without_band": [str(w) for w, has, inpred in zip(
            out["week"], covered, [pd.Timestamp(w) in pred.index for w in out["week"]])
            if inpred and not has],
    }
    (ROOT / "docs/model_v2/model_card_v2.json").write_text(json.dumps(card, indent=2) + "\n")
    print(json.dumps(card, indent=2))
    print(out.loc[covered].head(3).T)


if __name__ == "__main__":
    main()
