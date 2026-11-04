"""Model v2 comparison, exactly as frozen in docs/model_v2/SPEC_2026-11-05.md.

    python scripts/model_v2.py

Writes predictions to data/processed/model_v2/, tables and figures to
reports/model_v2/, and the selection decision to reports/model_v2/selection.json.
"""

from __future__ import annotations

import json
import warnings

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

warnings.filterwarnings("ignore")

from hfpos import config  # noqa: E402
from hfpos.model_v2 import VERSION  # noqa: E402
from hfpos.model_v2.estimators import make  # noqa: E402
from hfpos.model_v2.evaluate import (benchmark_series, hac_test, metrics, r2,  # noqa: E402
                                     stationary_bootstrap_ci, walk)
from hfpos.model_v2.features import ALT_TARGET, TARGET, assemble, trailing_percentile  # noqa: E402
from hfpos.stage1.models import make_estimator as make_v1  # noqa: E402

OUT = config.REPO_ROOT / "reports" / "model_v2"
PRED = config.REPO_ROOT / "data" / "processed" / "model_v2"
ERAS = {"2013-2016": ("2013", "2016"), "2017-2019": ("2017", "2019"),
        "2020-2022": ("2020", "2022"), "2023-2026": ("2023", "2026")}
REF = "M3_exp"
MAIN = ["B2_exp", "M3_exp", "M3_roll", "M4_exp", "M4_roll", "M5_exp", "M5_roll",
        "M6_exp", "M6_roll"]
SIMPLICITY = {"M3_exp": 0, "M3_roll": 0, "M6_exp": 1, "M6_roll": 1, "M4_exp": 2,
              "M4_roll": 2, "M5_exp": 3, "M5_roll": 3, "B2_exp": -1}


def run_candidates(frame, sets) -> dict[str, pd.DataFrame]:
    runs = {"B2_exp": walk(frame, sets["B2"], TARGET, lambda: make("ar1"))}
    for m in ("M3", "M4", "M5"):
        for w in ("exp", "roll"):
            runs[f"{m}_{w}"] = walk(frame, sets[m], TARGET, lambda: make("ridge"),
                                    "expanding" if w == "exp" else "rolling")
            print(f"  {m}_{w} done", flush=True)
    for w in ("exp", "roll"):
        runs[f"M6_{w}"] = walk(frame, sets["M6"], TARGET, lambda: make("fused"),
                               "expanding" if w == "exp" else "rolling")
        print(f"  M6_{w} done", flush=True)
    return runs


def run_audits(frame, sets) -> dict[str, pd.DataFrame]:
    m3 = sets["M3"]
    no_oi = [c for c in m3 if c != "d_log_oi"]
    return {
        "audit_v1_ridge": walk(frame, m3, TARGET, lambda: make_v1("ridge", 20260918)),
        "audit_v1_gbm": walk(frame, m3, TARGET, lambda: make_v1("gbm", 20260918)),
        "audit_gbm_fixed": walk(frame, m3, TARGET, lambda: make("gbm_fixed")),
        "ablate_M3_no_d_log_oi": walk(frame, no_oi, TARGET, lambda: make("ridge")),
        "alt_M3": walk(frame, m3, ALT_TARGET, lambda: make("ridge")),
        "alt_M3_no_d_log_oi": walk(frame, no_oi, ALT_TARGET, lambda: make("ridge")),
    }


def scored(runs, names, common, b1) -> pd.DataFrame:
    rows = []
    for n in names:
        r = runs[n].loc[common]
        rows.append({"candidate": n, "coverage_n": len(runs[n]),
                     "coverage_first": str(runs[n].index[0].date()),
                     **metrics(r["actual"], r["pred"], b1.loc[common])})
    return pd.DataFrame(rows)


def comparisons(runs, common) -> pd.DataFrame:
    ref = runs[REF].loc[common]
    ref_loss = (ref["actual"] - ref["pred"]) ** 2
    rows = []
    for n in MAIN + ["B0", "B1"]:
        if n == REF:
            continue
        r = runs[n].loc[common]
        d = ref_loss - (r["actual"] - r["pred"]) ** 2          # >0: candidate better
        t, p = hac_test(d)
        lo, hi = stationary_bootstrap_ci(d.to_numpy())
        rows.append({"candidate": n, "mse_reduction_vs_M3": float(d.mean()),
                     "pct_mse_reduction": float(d.mean() / ref_loss.mean() * 100),
                     "hac_t": t, "p_one_sided": p, "boot90_lo": lo, "boot90_hi": hi})
    return pd.DataFrame(rows)


def splits(runs, frame, common, b1) -> pd.DataFrame:
    vix = frame["vix"]
    vix_pct = pd.Series([(vix.iloc[:i].dropna() < vix.iloc[i]).mean() if i > 52 else np.nan
                         for i in range(len(vix))], index=vix.index)
    extreme_pct = trailing_percentile(frame["s_level"]).shift(1)
    masks = {f"era {k}": (common >= f"{a}-01-01") & (common <= f"{b}-12-31")
             for k, (a, b) in ERAS.items()}
    masks["stressed (VIX > prior 67th pct)"] = (vix_pct.loc[common] > 0.67).to_numpy()
    masks["calm (VIX < prior 33rd pct)"] = (vix_pct.loc[common] < 0.33).to_numpy()
    ext = extreme_pct.loc[common]
    masks["extreme s_{t-1} (prior-260w pct <=10 or >=90)"] = ((ext <= 0.10) | (ext >= 0.90)).to_numpy()
    masks["non-extreme s_{t-1}"] = ((ext > 0.10) & (ext < 0.90)).to_numpy()
    rows = []
    for label, m in masks.items():
        idx = common[np.asarray(m, bool)]
        row = {"split": label, "n": len(idx)}
        for n in ("M3_exp", "M4_exp", "M5_exp", "M6_exp", "M6_roll"):
            r = runs[n].loc[idx]
            row[f"{n}_r2_vs_mean"] = r2(r["actual"], r["pred"], b1.loc[idx]) if len(idx) > 20 else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def select(comp: pd.DataFrame, table: pd.DataFrame) -> dict:
    cands = comp[comp["candidate"].isin(MAIN)].copy()
    cands = cands.merge(table[["candidate", "rmse"]], on="candidate")
    passing = cands[(cands["p_one_sided"] < 0.10) & (cands["boot90_lo"] > 0)]
    if passing.empty:
        chosen, reason = REF, "no candidate beat M3 under the predeclared rule; retain M3"
    else:
        best_rmse = passing["rmse"].min()
        tied = passing[passing["rmse"] <= best_rmse * 1.001]
        chosen = min(tied["candidate"], key=lambda c: SIMPLICITY[c])
        reason = "lowest common-week MSE among candidates passing HAC p<0.10 and bootstrap CI>0"
    return {"version": VERSION, "selected": chosen, "reason": reason,
            "passing": passing["candidate"].tolist()}


def figures(runs, common, comp, frame, sets):
    ref = runs[REF].loc[common]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for n, c in (("M4_exp", "#1D9E75"), ("M5_exp", "#534AB7"), ("M6_exp", "#D85A30"),
                 ("M3_roll", "#888780")):
        r = runs[n].loc[common]
        d = (ref["actual"] - ref["pred"]) ** 2 - (r["actual"] - r["pred"]) ** 2
        ax.plot(d.cumsum() * 1e4, label=n, color=c, lw=1.2)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylabel("cumulative squared-error saving vs M3 (x1e4)")
    ax.set_title("Above zero = candidate beating corrected ridge (M3)")
    ax.legend(frameon=False, fontsize=8); fig.tight_layout()
    fig.savefig(OUT / "cum_loss_vs_M3.png", dpi=180); plt.close(fig)

    from hfpos.model_v2.estimators import make as mk
    data = frame[sets["M6"] + [TARGET]].dropna()
    est = mk("fused").fit(data[sets["M6"]].to_numpy(float), data[TARGET].to_numpy(float))
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(est.best_estimator_.coef_ * 100, color="#D85A30")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xlabel("lag (trading days)")
    ax.set_ylabel("weight on daily return (pp of OI per 1% return)")
    ax.set_title(f"M6 return signature, full-sample fit, gamma={est.best_params_['gamma']:.2g} (descriptive only)")
    fig.tight_layout(); fig.savefig(OUT / "m6_return_signature.png", dpi=180); plt.close(fig)

    t = comp.set_index("candidate")
    order = [n for n in MAIN if n != REF]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    y = np.arange(len(order))
    ax.errorbar(t.loc[order, "mse_reduction_vs_M3"] * 1e5, y,
                xerr=[(t.loc[order, "mse_reduction_vs_M3"] - t.loc[order, "boot90_lo"]) * 1e5,
                      (t.loc[order, "boot90_hi"] - t.loc[order, "mse_reduction_vs_M3"]) * 1e5],
                fmt="o", color="#185FA5", capsize=3)
    ax.axvline(0, color="black", lw=0.6); ax.set_yticks(y, order)
    ax.set_xlabel("mean squared-error reduction vs M3 (x1e5), 90% stationary-bootstrap CI")
    fig.tight_layout(); fig.savefig(OUT / "mse_reduction_ci.png", dpi=180); plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True); PRED.mkdir(parents=True, exist_ok=True)
    frame, sets = assemble()
    print("candidates", flush=True)
    runs = run_candidates(frame, sets)
    print("audits", flush=True)
    audits = run_audits(frame, sets)
    b1 = benchmark_series(frame, TARGET, "mean")["pred"]
    runs["B0"] = benchmark_series(frame, TARGET, "zero").rename(columns={})
    runs["B1"] = benchmark_series(frame, TARGET, "mean")
    for n, r in {**runs, **audits}.items():
        r.to_parquet(PRED / f"{n}.parquet")

    common = runs["M3_exp"].index
    for n in MAIN + ["B0", "B1"]:
        common = common.intersection(runs[n].index)
    print(f"common weeks: {len(common)} ({common[0].date()} .. {common[-1].date()})")

    table = scored(runs, MAIN + ["B0", "B1"], common, b1)
    comp = comparisons(runs, common)
    table.to_csv(OUT / "comparison.csv", index=False)
    comp.to_csv(OUT / "loss_differentials_vs_M3.csv", index=False)
    split_table = splits(runs, frame, common, b1)
    split_table.to_csv(OUT / "splits.csv", index=False)

    a_common = common
    for n in audits:
        if not n.startswith("alt_"):
            a_common = a_common.intersection(audits[n].index)
    audit_rows = scored({**runs, **audits},
                        ["M3_exp", "audit_v1_ridge", "audit_v1_gbm", "audit_gbm_fixed",
                         "ablate_M3_no_d_log_oi"], a_common, b1)
    audit_rows.to_csv(OUT / "audits.csv", index=False)

    alt_b1 = benchmark_series(frame, ALT_TARGET, "mean")["pred"]
    alt_rows = []
    for n in ("alt_M3", "alt_M3_no_d_log_oi"):
        r = audits[n].loc[common.intersection(audits[n].index)]
        alt_rows.append({"run": n, **metrics(r["actual"], r["pred"], alt_b1.loc[r.index])})
    prim = runs["M3_exp"].loc[audits["alt_M3"].index.intersection(common)]
    alt_rows.append({"run": "corr(pred primary, pred alt)",
                     "n": len(prim),
                     "r2_vs_mean": float(prim["pred"].corr(audits["alt_M3"].loc[prim.index, "pred"]))})
    pd.DataFrame(alt_rows).to_csv(OUT / "alt_target.csv", index=False)

    decision = select(comp, table)
    decision["common_weeks"] = [str(common[0].date()), str(common[-1].date()), len(common)]
    (OUT / "selection.json").write_text(json.dumps(decision, indent=2) + "\n")
    figures(runs, common, comp, frame, sets)

    fmt = lambda v: f"{v:.4f}"  # noqa: E731
    cols = ["candidate", "n", "r2_vs_mean", "r2_vs_zero", "rmse", "mae", "bias", "pred_sd",
            "mz_slope", "resid_ac1", "corr_resid_actual", "sqrt_1_minus_r2"]
    print(table[cols].to_string(index=False, float_format=fmt))
    print(comp.to_string(index=False, float_format=fmt))
    print(split_table.to_string(index=False, float_format=fmt))
    print(audit_rows[["candidate", "n", "r2_vs_mean", "rmse", "corr_resid_actual"]].to_string(index=False, float_format=fmt))
    print(pd.DataFrame(alt_rows).iloc[:, :6].to_string(index=False, float_format=fmt))
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
