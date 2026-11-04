"""Which weeks does the model re-rank, and why? (fixed selection rule, no cherry-picking)

    python scripts/model_v2_cases.py

Rule, fixed before looking: K = 72 (the top decile of the 720 evaluation weeks).
  entrants = in the top-K |M3 residual| but not in the top-K |raw change|
  leavers  = in the top-K |raw change| but not in the top-K |M3 residual|
Every entrant and leaver is reported. For each, the M3 prediction is decomposed into
feature-group contributions using the SAME fold model that produced it (refit
identically), as coef x standardised value. Robustness: is the week also top-K by
|residual| under M3-rolling, M4, M5, M3 without d_log_oi, and the alternative target?
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from hfpos import config  # noqa: E402
from hfpos.model_v2.estimators import make  # noqa: E402
from hfpos.model_v2.evaluate import MIN_TRAIN, STEP  # noqa: E402
from hfpos.model_v2.features import TARGET, assemble  # noqa: E402

K = 72
P = config.REPO_ROOT / "data/processed/model_v2"
OUT = config.REPO_ROOT / "reports/model_v2"
GROUPS = {
    "own position": ("net_over_oi_lag1", "d_net_over_oi_lag1"),
    "open-interest change": ("d_log_oi",),
    "price momentum / vol": ("ret_", "rvol_", "roll_week"),
    "rates and curve": ("y_", "dy_", "slope", "d_slope", "curvature"),
    "equity vol": ("vix", "d_vix"),
    "futures-yield resid / funding": ("futures_yield_residual", "funding_spread"),
    "Fed / calendar": ("d_log_soma", "quarter_end_week"),
    "other groups (lagged)": ("dealer_", "asset_manager_", "other_reportable_"),
    "other contracts (lagged)": ("2y_", "5y_", "30y_"),
}


def group_of(col: str) -> str:
    for g, prefixes in GROUPS.items():
        if any(col == p or col.startswith(p) for p in prefixes):
            return g
    raise KeyError(col)


def contributions(frame, feats, weeks) -> pd.DataFrame:
    data = frame[feats + [TARGET]].dropna()
    X, y = data[feats].to_numpy(float), data[TARGET].to_numpy(float)
    pos = {d: i for i, d in enumerate(data.index)}
    rows = []
    for start in range(MIN_TRAIN, len(y), STEP):
        block = data.index[start:start + STEP]
        wanted = [w for w in weeks if w in set(block)]
        if not wanted:
            continue
        est = make("ridge").fit(X[:start], y[:start]).best_estimator_
        sc, coef = est.named_steps["scale"], est.named_steps["est"].coef_
        for w in wanted:
            z = (X[pos[w]] - sc.mean_) / sc.scale_
            c = pd.Series(coef * z, index=feats).groupby(group_of).sum()
            rows.append({"week": w, **c.to_dict()})
    return pd.DataFrame(rows).set_index("week")


def top(series: pd.Series) -> set:
    return set(series.abs().nlargest(K).index)


def main():
    frame, sets = assemble()
    runs = {n: pd.read_parquet(P / f"{n}.parquet") for n in
            ("M3_exp", "M3_roll", "M4_exp", "M5_exp", "ablate_M3_no_d_log_oi", "alt_M3")}
    m3 = runs["M3_exp"]
    common = m3.index
    for r in runs.values():
        common = common.intersection(r.index)
    m3 = m3.loc[common]
    resid = m3["actual"] - m3["pred"]
    raw_top, res_top = top(m3["actual"]), top(resid)
    entrants = sorted(res_top - raw_top)
    leavers = sorted(raw_top - res_top)
    print(f"overlap {len(raw_top & res_top)}/{K}; entrants {len(entrants)}, leavers {len(leavers)}")

    robust = {n: top((r.loc[common, "actual"] - r.loc[common, "pred"]))
              for n, r in runs.items() if n != "M3_exp"}
    contrib = contributions(frame, sets["M3"], entrants + leavers)

    rank_raw = m3["actual"].abs().rank(ascending=False)
    rank_res = resid.abs().rank(ascending=False)
    rows = []
    for kind, weeks in (("entrant", entrants), ("leaver", leavers)):
        for w in weeks:
            c = contrib.loc[w]
            dominant = c.abs().idxmax()
            rows.append({
                "kind": kind, "week": w.date(),
                "raw_change_pp": m3.loc[w, "actual"] * 100,
                "predicted_pp": m3.loc[w, "pred"] * 100,
                "residual_pp": resid.loc[w] * 100,
                "rank_raw": int(rank_raw[w]), "rank_resid": int(rank_res[w]),
                "dominant_group": dominant,
                "dominant_pp": c[dominant] * 100,
                "dominant_share_of_abs": c.abs()[dominant] / c.abs().sum(),
                "same_sign_pred_vs_raw": bool(np.sign(m3.loc[w, "pred"]) == np.sign(m3.loc[w, "actual"])),
                **{f"top_in_{n}": w in s for n, s in robust.items()},
            })
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "cases_rerank.csv", index=False)
    (contrib * 100).round(2).to_csv(OUT / "cases_contributions_pp.csv")
    pd.set_option("display.width", 250)
    print(table.round(2).to_string(index=False))
    print((contrib * 100).round(2).to_string())


if __name__ == "__main__":
    main()
