"""Three diagnostics on the Stage-1 model, run as one script.

Answers, with evidence rather than assertion:

  1. Which variables contribute, and do the added economic variables help?
     Feature-set comparison plus leave-one-group-out ablation, all out of sample.
  2. Which prediction problem are we solving? Contemporaneous change, next-week
     change, and the level -- and what the level's flattering R-squared really is.
  3. Does it work in calm periods and fail in stressed ones, and does it work on
     the extreme-positioning weeks the LLM experiment actually samples?

    python scripts/model_experiments.py
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from hfpos import config  # noqa: E402
from hfpos.features.build import TARGET, build, feature_columns  # noqa: E402
from hfpos.ingest import cftc  # noqa: E402
from hfpos.stage1.models import fit_predict  # noqa: E402
from hfpos.stage1.run import oos_r2  # noqa: E402
from hfpos.stage1.walkforward import ExpandingWindowSplitter  # noqa: E402

SEED = 20260918
MIN_TRAIN = 260
STEP = 13

GROUPS = {
    "own position": ("net_over_oi_lag1", "d_net_over_oi_lag1", "d_log_oi"),
    "momentum / vol": ("ret_", "rvol_", "roll_week"),
    "rates and curve": ("y_", "dy_", "slope", "curvature"),
    "equity vol": ("vix", "d_vix"),
    "basis conditions": ("futures_cash_spread", "funding_spread"),
    "Fed / calendar": ("d_log_soma", "quarter_end_week"),
    "other groups": ("dealer_", "asset_manager_", "other_reportable_"),
    "other contracts": ("2y_", "5y_", "30y_"),
}


def walk(frame: pd.DataFrame, features: list[str], target: pd.Series, model: str,
         embargo: int = 0) -> pd.DataFrame:
    """Walk-forward predictions for an arbitrary target and feature list."""
    data = frame[features].join(target.rename("__y__")).dropna()
    X, y = data[features].to_numpy(float), data["__y__"].to_numpy(float)
    pred = np.full(len(data), np.nan)
    bench = np.full(len(data), np.nan)
    for split in ExpandingWindowSplitter(MIN_TRAIN, STEP, embargo).split(len(data)):
        pred[split.test] = fit_predict(X[split.train], y[split.train], X[split.test], model, SEED)
        bench[split.test] = y[split.train].mean()
    out = pd.DataFrame({"actual": y, "expected": pred, "benchmark": bench}, index=data.index)
    out["residual"] = out["actual"] - out["expected"]
    return out.dropna()


def score(result: pd.DataFrame) -> dict:
    return {
        "n": len(result),
        "oos_r2": oos_r2(result["actual"].to_numpy(), result["expected"].to_numpy(),
                         result["benchmark"].to_numpy()),
        "corr_resid_raw": float(result["residual"].corr(result["actual"])),
    }


def check_1_features() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []
    frames = {}
    for feature_set in ("baseline", "extended"):
        frame = build(feature_set=feature_set)
        frames[feature_set] = frame
        features = feature_columns(frame)
        for model in ("ridge", "lasso", "gbm"):
            result = walk(frame, features, frame[TARGET], model)
            rows.append({"feature_set": feature_set, "n_features": len(features),
                         "model": model, **score(result)})
    comparison = pd.DataFrame(rows)

    frame = frames["extended"]
    features = feature_columns(frame)
    full = score(walk(frame, features, frame[TARGET], "ridge"))["oos_r2"]
    ablation = []
    for label, prefixes in GROUPS.items():
        kept = [c for c in features if not any(c.startswith(p) for p in prefixes)]
        dropped = len(features) - len(kept)
        if dropped == 0:
            continue
        got = score(walk(frame, kept, frame[TARGET], "ridge"))["oos_r2"]
        ablation.append({"group_removed": label, "features_removed": dropped,
                         "oos_r2_without": got, "loss_vs_full": full - got})
    ablation = pd.DataFrame(ablation).sort_values("loss_vs_full", ascending=False)
    return comparison, ablation, frames["extended"]


def check_2_targets(frame: pd.DataFrame) -> pd.DataFrame:
    features = feature_columns(frame)
    positions = cftc.load("UST_10Y")
    level = (positions["leveraged_funds_net"] / positions["open_interest"]).reindex(frame.index)

    rows = []
    contemporaneous = walk(frame, features, frame[TARGET], "ridge")
    rows.append({"target": "this week's change (current spec)",
                 "benchmark": "training mean of changes", **score(contemporaneous)})

    forecast = walk(frame, features, frame[TARGET].shift(-1), "ridge", embargo=0)
    rows.append({"target": "NEXT week's change (true forecast)",
                 "benchmark": "training mean of changes", **score(forecast)})

    level_result = walk(frame, features, level, "ridge")
    rows.append({"target": "this week's LEVEL", "benchmark": "training mean of levels",
                 **score(level_result)})

    # Same level predictions, scored against the honest benchmark: last week's level.
    lagged = level.shift(1).reindex(level_result.index)
    rows.append({
        "target": "this week's LEVEL", "benchmark": "random walk (last week's level)",
        "n": len(level_result),
        "oos_r2": oos_r2(level_result["actual"].to_numpy(), level_result["expected"].to_numpy(),
                         lagged.to_numpy()),
        "corr_resid_raw": float(level_result["residual"].corr(level_result["actual"].diff())),
    })
    return pd.DataFrame(rows)


def check_3_regimes(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = feature_columns(frame)
    result = walk(frame, features, frame[TARGET], "ridge")

    positions = cftc.load("UST_10Y")
    net_oi = (positions["leveraged_funds_net"] / positions["open_interest"]).reindex(result.index)
    vix = frame["vix"].reindex(result.index)

    def subset(label: str, mask: pd.Series) -> dict:
        chunk = result[mask.reindex(result.index).fillna(False)]
        if len(chunk) < 20:
            return {"regime": label, "n": len(chunk), "oos_r2": np.nan, "corr_resid_raw": np.nan}
        return {"regime": label, **score(chunk)}

    extreme = net_oi <= net_oi.quantile(0.10)
    calm = vix <= vix.quantile(0.33)
    stressed = vix >= vix.quantile(0.67)
    regimes = pd.DataFrame([
        subset("all predicted weeks", pd.Series(True, index=result.index)),
        subset("most extreme 10% of short positioning", extreme),
        subset("all other weeks", ~extreme),
        subset("calm (lowest VIX tercile)", calm),
        subset("stressed (highest VIX tercile)", stressed),
        subset("Mar-Jun 2020 (COVID dislocation)",
               pd.Series(result.index.to_series().between("2020-03-01", "2020-06-30").to_numpy(),
                         index=result.index)),
        subset("2022-2023 hiking cycle",
               pd.Series(result.index.to_series().between("2022-01-01", "2023-12-31").to_numpy(),
                         index=result.index)),
    ])

    eras = []
    for start, end in (("2013", "2016"), ("2017", "2019"), ("2020", "2022"), ("2023", "2026")):
        chunk = result.loc[start:end]
        eras.append({"era": f"{start}-{end}", **score(chunk)})
    return regimes, pd.DataFrame(eras)


def main() -> None:
    tables = config.path("tables")

    comparison, ablation, frame = check_1_features()
    print("=" * 78)
    print("CHECK 1a - does the extended feature set help?")
    print(comparison.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print("\nCHECK 1b - leave-one-group-out, extended set, ridge")
    print(ablation.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    targets = check_2_targets(frame)
    print("\n" + "=" * 78)
    print("CHECK 2 - which prediction problem?")
    print(targets.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    regimes, eras = check_3_regimes(frame)
    print("\n" + "=" * 78)
    print("CHECK 3 - performance across regimes")
    print(regimes.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print()
    print(eras.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    comparison.to_csv(tables / "exp_feature_sets.csv", index=False)
    ablation.to_csv(tables / "exp_ablation.csv", index=False)
    targets.to_csv(tables / "exp_targets.csv", index=False)
    regimes.to_csv(tables / "exp_regimes.csv", index=False)
    eras.to_csv(tables / "exp_eras.csv", index=False)


if __name__ == "__main__":
    main()
