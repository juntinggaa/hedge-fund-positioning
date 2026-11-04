"""Model v3 factor comparison, as frozen in docs/model_v3/SPEC_2026-11-05.md.

    python scripts/fetch_v3_sources.py   # once, network
    python scripts/model_v3.py           # offline

Writes reports/model_v3/*.csv, selection.json and data/processed/model_v3/*.parquet.
Nothing under model_v2 or v1 is written.
"""

from __future__ import annotations

import json
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from hfpos import config  # noqa: E402
from hfpos.model_v2.estimators import make  # noqa: E402
from hfpos.model_v2.evaluate import (benchmark_series, hac_test, metrics,  # noqa: E402
                                     stationary_bootstrap_ci, walk)
from hfpos.model_v2.features import ALT_TARGET, TARGET, assemble  # noqa: E402
from hfpos.model_v3 import VERSION, sources  # noqa: E402
from hfpos.model_v3.features import break_audit, dealer_block, supply_block  # noqa: E402

OUT = config.REPO_ROOT / "reports" / "model_v3"
PRED = config.REPO_ROOT / "data" / "processed" / "model_v3"
V2PRED = config.REPO_ROOT / "data" / "processed" / "model_v2"
D_PRIMARY = ["d_coup711_z", "d_coup711_ch4_z", "d_ust_tot_z", "d_ust_tot_ch4_z"]
D_FAILS = ["d_fails_z"]
PP = 100.0


def build():
    frame, sets = assemble()
    S = supply_block(frame.index)
    D = dealer_block(frame.index)
    frame = pd.concat([frame, S, D], axis=1)
    m3, s = sets["M3"], list(S.columns)
    return frame, {"M3": m3, "M3+S": m3 + s, "M3+D": m3 + D_PRIMARY,
                   "M3+S+D": m3 + s + D_PRIMARY, "M3+D+fails": m3 + D_PRIMARY + D_FAILS,
                   "B2": ["d_net_over_oi_lag1"]}


def run_set(frame, sets, names, target):
    est = {"B2": "ar1"}
    return {n: walk(frame, sets[n], target, lambda n=n: make(est.get(n, "ridge"))) for n in names}


def compare(runs, ref, names, common, b1, sample):
    rows = []
    r0 = runs[ref].loc[common]
    ref_loss = (r0["actual"] - r0["pred"]) ** 2
    k = max(1, int(round(0.10 * len(common))))
    top_ref = set((r0["actual"] - r0["pred"]).abs().nlargest(k).index)
    for n in names:
        r = runs[n].loc[common]
        m = metrics(r["actual"], r["pred"], b1.loc[common])
        row = {"sample": sample, "candidate": n, "n": m["n"],
               "first_oos": str(common[0].date()), "last_oos": str(common[-1].date()),
               "r2_vs_B1_pct": m["r2_vs_mean"] * 100, "r2_vs_B0_pct": m["r2_vs_zero"] * 100,
               "rmse_pp": m["rmse"] * PP, "mae_pp": m["mae"] * PP, "mz_slope": m["mz_slope"],
               "pred_sd_pp": m["pred_sd"] * PP}
        if n != ref and not n.startswith("B"):
            d = ref_loss - (r["actual"] - r["pred"]) ** 2
            t, p = hac_test(d)
            lo, hi = stationary_bootstrap_ci(d.to_numpy())
            top_c = set((r["actual"] - r["pred"]).abs().nlargest(k).index)
            row.update({"pct_mse_reduction_vs_ref": d.mean() / ref_loss.mean() * 100,
                        "hac_t": t, "hac_p_one_sided": p,
                        "boot90_lo_pct": lo / ref_loss.mean() * 100,
                        "boot90_hi_pct": hi / ref_loss.mean() * 100,
                        "passes_gate": bool(p < 0.10 and lo > 0),
                        f"top{k}_resid_overlap_with_ref": len(top_c & top_ref)})
        rows.append(row)
    return pd.DataFrame(rows)


def eras(runs, ref, names, common, sample):
    rows = []
    r0 = runs[ref].loc[common]
    for n in names:
        r = runs[n].loc[common]
        d = (r0["actual"] - r0["pred"]) ** 2 - (r["actual"] - r["pred"]) ** 2
        for era, g in d.groupby(pd.cut(d.index.year, [2010, 2012, 2016, 2019, 2022, 2026],
                                       labels=["2011-12", "2013-16", "2017-19", "2020-22",
                                               "2023-26"])):
            if len(g):
                base = ((r0["actual"] - r0["pred"]) ** 2).loc[g.index].mean()
                rows.append({"sample": sample, "candidate": n, "era": era, "n": len(g),
                             "pct_mse_reduction_vs_ref": g.mean() / base * 100})
    return pd.DataFrame(rows)


def alt(frame, sets, names, rows_index, sample):
    alt_b1 = benchmark_series(frame, ALT_TARGET, "mean")["pred"]
    sub = frame.loc[rows_index]
    runs = run_set(sub, sets, names, ALT_TARGET)
    common = runs[names[0]].index
    for n in names[1:]:
        common = common.intersection(runs[n].index)
    out = []
    for n in names:
        r = runs[n].loc[common]
        out.append({"sample": sample, "candidate": n, "n": len(r),
                    "alt_r2_vs_B1_pct": metrics(r["actual"], r["pred"], alt_b1.loc[common])["r2_vs_mean"] * 100})
    return pd.DataFrame(out)


def coefs(frame, sets, names, rows_index):
    rows = []
    for n in names:
        feats = sets[n]
        data = frame.loc[rows_index, feats + [TARGET]].dropna()
        g = make("ridge").fit(data[feats].to_numpy(float), data[TARGET].to_numpy(float))
        coef = g.best_estimator_.named_steps["est"].coef_
        for f, c in zip(feats, coef):
            if f.startswith(("s_", "d_coup", "d_ust", "d_fails")):
                rows.append({"candidate": n, "feature": f, "std_coef_pp": c * PP,
                             "alpha": g.best_params_["est__alpha"]})
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True); PRED.mkdir(parents=True, exist_ok=True)
    frame, sets = build()
    b1 = benchmark_series(frame, TARGET, "mean")["pred"]

    pdw = sources.load_pd()
    break_audit(pdw, sources.pd_breaks(), sources.PD_PRIMARY + sources.PD_SECONDARY) \
        .to_csv(OUT / "pd_break_audit.csv", index=False)

    # --- full sample: M3 vs M3+S --------------------------------------------------
    full_rows = frame[sets["M3+S"] + [TARGET]].dropna().index
    full = frame.loc[full_rows]
    runs_f = run_set(full, sets, ["M3", "M3+S", "B2"], TARGET)
    common_f = runs_f["M3"].index.intersection(runs_f["M3+S"].index).intersection(runs_f["B2"].index)
    v2 = pd.read_parquet(V2PRED / "M3_exp.parquet")
    same = v2.index.intersection(common_f)
    m3_identical = bool(np.allclose(v2.loc[same, "pred"], runs_f["M3"].loc[same, "pred"]))

    # --- D sample: identical rows for every model ---------------------------------
    d_cols = sets["M3+S+D"] + D_FAILS + [TARGET]
    d_rows = frame[d_cols].dropna().index
    dsub = frame.loc[d_rows]
    names_d = ["M3", "M3+D", "M3+S+D", "M3+D+fails", "B2"]
    runs_d = run_set(dsub, sets, names_d, TARGET)
    common_d = runs_d["M3"].index
    for n in names_d[1:]:
        common_d = common_d.intersection(runs_d[n].index)
    runs_d["M3_v2.0_as_fitted"] = v2
    for n, r in runs_f.items():
        r.to_parquet(PRED / f"full_{n.replace('+', '_')}.parquet")
    for n, r in runs_d.items():
        if n != "M3_v2.0_as_fitted":
            r.to_parquet(PRED / f"dsample_{n.replace('+', '_')}.parquet")

    comp = pd.concat([
        compare(runs_f, "M3", ["M3", "M3+S", "B2"], common_f, b1, "full"),
        compare(runs_d, "M3", names_d + ["M3_v2.0_as_fitted"], common_d, b1, "D"),
    ], ignore_index=True)
    comp.to_csv(OUT / "comparison.csv", index=False)
    era = pd.concat([eras(runs_f, "M3", ["M3+S"], common_f, "full"),
                     eras(runs_d, "M3", ["M3+D", "M3+S+D", "M3+D+fails"], common_d, "D")])
    era.to_csv(OUT / "eras.csv", index=False)
    alts = pd.concat([alt(frame, sets, ["M3", "M3+S"], full_rows, "full"),
                      alt(frame, sets, ["M3", "M3+D", "M3+S+D"], d_rows, "D")])
    alts.to_csv(OUT / "alt_target.csv", index=False)
    co = pd.concat([coefs(frame, sets, ["M3+S"], full_rows),
                    coefs(frame, sets, ["M3+D", "M3+D+fails"], d_rows)])
    co.to_csv(OUT / "coefficients_descriptive.csv", index=False)

    eligible = comp[comp["candidate"].isin(["M3+S", "M3+D", "M3+S+D"])]
    passing = eligible[eligible["passes_gate"] == True]  # noqa: E712
    sel = {"version": VERSION, "spec": "docs/model_v3/SPEC_2026-11-05.md",
           "full_sample_M3_identical_to_v2": m3_identical,
           "full_common_weeks": [str(common_f[0].date()), str(common_f[-1].date()), len(common_f)],
           "d_common_weeks": [str(common_d[0].date()), str(common_d[-1].date()), len(common_d)],
           "passing": passing["candidate"].tolist(),
           "decision": ("retain M3" if passing.empty else
                        "candidate(s) pass; adoption needs a team decision (spec section 6)"),
           "v2_gate_outcome_unchanged": "M4: HAC p=0.095, bootstrap CI includes 0, not adopted"}
    (OUT / "selection.json").write_text(json.dumps(sel, indent=1))
    pd.set_option("display.width", 220)
    print(comp.round(3).to_string()); print(era.round(2).to_string()); print(alts.round(2).to_string())
    print(co.round(3).to_string()); print(json.dumps(sel, indent=1))


if __name__ == "__main__":
    main()
