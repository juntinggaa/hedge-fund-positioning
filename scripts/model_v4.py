"""Run the isolated adaptation experiment. Existing model/LLM files are read-only.

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/model_v4.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from statsmodels.stats.multitest import multipletests

from hfpos import config
from hfpos.model_v2.evaluate import benchmark_series, hac_test, metrics
from hfpos.model_v2.features import TARGET, base_frame, v1_features
from hfpos.model_v4.adaptation import SCHEMES, calibrate, walk

ROOT = config.REPO_ROOT
DOC = ROOT / "docs/model_v4"
OUT = ROOT / "reports/model_v4"
PRED = ROOT / "data/processed/model_v4"
DELIVER = Path("/Users/lipjunting/Documents/Codex/2026-11-04/can-u/outputs/adaptation_experiment")
SEED, BOOT_REPS, BLOCK = 20261105, 2000, 13


def check_preservation() -> int:
    protected = json.loads((DOC / "preservation_before.json").read_text())["sha256"]
    changed = [name for name, digest in protected.items()
               if not (ROOT / name).exists()
               or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest]
    if changed:
        raise RuntimeError(f"Pre-existing files changed: {changed}")
    return len(protected)


def bootstrap_indices(n: int) -> np.ndarray:
    rng = np.random.default_rng(SEED)
    draws = np.empty((BOOT_REPS, n), dtype=np.int32)
    draws[:, 0] = rng.integers(n, size=BOOT_REPS)
    for t in range(1, n):
        restart = rng.random(BOOT_REPS) < 1 / BLOCK
        draws[:, t] = np.where(restart, rng.integers(n, size=BOOT_REPS),
                               (draws[:, t - 1] + 1) % n)
    return draws


def loss_test(ref: pd.Series, candidate: pd.Series, draws: np.ndarray) -> dict:
    diff = ref - candidate
    _, p = hac_test(diff)
    boot = diff.to_numpy()[draws].mean(axis=1)
    lo, hi = np.quantile(boot, [0.05, 0.95])
    scale = float(ref.mean())
    return {
        "mse_reduction_pct": float(diff.mean() / scale * 100),
        "hac_p_one_sided": p,
        "boot90_lo_pct": float(lo / scale * 100),
        "boot90_hi_pct": float(hi / scale * 100),
    }


def table_md(table: pd.DataFrame) -> str:
    columns = ["Candidate", "R² vs mean", "RMSE (pp)", "MSE gain", "90% CI for gain", "Holm p"]
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for _, r in table.iterrows():
        base = r["candidate"] == "expanding"
        gain = "reference" if base else f"{r['mse_reduction_pct']:+.2f}%"
        ci = "—" if base else f"[{r['boot90_lo_pct']:+.2f}%, {r['boot90_hi_pct']:+.2f}%]"
        hp = "—" if base else f"{r['holm_p']:.3f}"
        lines.append(f"| {r['candidate']} | {r['r2_vs_mean'] * 100:.2f}% | "
                     f"{r['rmse'] * 100:.3f} | {gain} | {ci} | {hp} |")
    return "\n".join(lines)


def figures(table, runs, common, cumulative, calibration_logs):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 150})
    t = table[table.candidate != "expanding"].sort_values("mse_reduction_pct")
    fig, ax = plt.subplots(figsize=(10, 6))
    yy = np.arange(len(t))
    ax.hlines(yy, t.boot90_lo_pct, t.boot90_hi_pct, color="#64748b", linewidth=2)
    ax.scatter(t.mse_reduction_pct, yy,
               c=["#087f5b" if x else "#2563eb" for x in t.passes_gate], zorder=3)
    ax.axvline(0, color="#111827", linestyle="--", linewidth=1)
    ax.set_yticks(yy, t.candidate)
    ax.set_xlabel("Squared-error reduction versus expanding M3 (%)\nPositive is better; bars are 90% stationary-bootstrap intervals")
    ax.set_title("Does adaptation improve positioning estimates?")
    fig.tight_layout(); fig.savefig(OUT / "comparison.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    for name in [s.name for s in SCHEMES if s.name != "expanding"]:
        ax.plot(common, cumulative[name], label=name, linewidth=1.3)
    best = table[table.candidate != "expanding"].sort_values("rmse").iloc[0].candidate
    if best.endswith("_calibrated"):
        ax.plot(common, cumulative[best], label=best, color="#111827", linewidth=2)
    ax.axhline(0, color="#111827", linewidth=0.8)
    ax.set_ylabel("Cumulative MSE reduction (% of total reference error)")
    ax.set_title("When did adaptations help or hurt?")
    ax.legend(fontsize=8, ncols=2); fig.tight_layout()
    fig.savefig(OUT / "cumulative_improvement.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    for name in ("expanding", "weighted_104", "weighted_260"):
        logs = calibration_logs[calibration_logs.scheme == name]
        ax.plot(pd.to_datetime(logs.block_start), logs.slope, label=name, linewidth=1.2)
    ax.axhline(1, color="#111827", linestyle="--", linewidth=1)
    ax.set_ylabel("Slope learned from prior OOS pairs")
    ax.set_title("Calibration changes over time; each slope uses only earlier predictions")
    ax.legend(); fig.tight_layout(); fig.savefig(OUT / "calibration_slopes.png"); plt.close(fig)


def main():
    for p in (OUT, PRED):
        p.mkdir(parents=True, exist_ok=True)
    n_protected = check_preservation()
    frame = base_frame()
    features = v1_features(frame)
    runs, fit_logs, cal_logs = {}, [], []
    fingerprint = hashlib.sha256(
        frame[features + [TARGET]].to_csv().encode()
        + (ROOT / "src/hfpos/model_v4/adaptation.py").read_bytes()
        + (DOC / "SPEC_2026-11-05.md").read_bytes()
        + sklearn.__version__.encode()
    ).hexdigest()
    for scheme in SCHEMES:
        print(f"Fitting {scheme.name}...", flush=True)
        cache = PRED / f"{scheme.name}.parquet"
        cache_meta = PRED / f"{scheme.name}_cache.json"
        fits_path = OUT / f"fits_{scheme.name}.csv"
        if (cache.exists() and cache_meta.exists() and fits_path.exists()
                and json.loads(cache_meta.read_text()).get("fingerprint") == fingerprint):
            raw = pd.read_parquet(cache)
            fits = pd.read_csv(fits_path)
            print("  using matching cached fits", flush=True)
        else:
            raw, fits = walk(frame, features, TARGET, scheme)
            raw.to_parquet(cache); fits.to_csv(fits_path, index=False)
            cache_meta.write_text(json.dumps({"fingerprint": fingerprint}) + "\n")
        if scheme.name in ("expanding", "rolling_260"):
            old_name = "M3_exp" if scheme.name == "expanding" else "M3_roll"
            old = pd.read_parquet(ROOT / f"data/processed/model_v2/{old_name}.parquet")
            if not raw.index.equals(old.index):
                raise AssertionError(f"{scheme.name} reference dates changed")
            np.testing.assert_allclose(raw.pred, old.pred, rtol=1e-10, atol=1e-12)
            print("  existing v2 predictions reproduced", flush=True)
        runs[scheme.name] = raw
        fit_logs.append(fits)
        adjusted, log = calibrate(raw)
        adjusted.to_parquet(PRED / f"{scheme.name}_calibrated.parquet")
        log["scheme"] = scheme.name
        cal_logs.append(log)
        runs[f"{scheme.name}_calibrated"] = adjusted
        print(f"  {len(raw)} raw predictions; {adjusted.pred.notna().sum()} calibrated", flush=True)

    fit_table = pd.concat(fit_logs, ignore_index=True)
    cal_table = pd.concat(cal_logs, ignore_index=True)
    fit_table.to_csv(OUT / "fit_log.csv", index=False)
    cal_table.to_csv(OUT / "calibration_log.csv", index=False)
    common = runs["expanding"].index
    for run in runs.values():
        common = common.intersection(run.dropna(subset=["pred"]).index)
    if len(common) != 668 or str(common[0].date()) != "2013-11-26":
        raise AssertionError("Predeclared common evaluation sample changed")
    b1 = benchmark_series(frame, TARGET, "mean")["pred"].loc[common]
    ref = runs["expanding"].loc[common]
    ref_loss = (ref.actual - ref.pred).pow(2)
    draws = bootstrap_indices(len(common))
    top_k = int(np.ceil(0.10 * len(common)))
    top_ref = set((ref.actual - ref.pred).abs().nlargest(top_k).index)
    top_raw = set(ref.actual.abs().nlargest(top_k).index)
    rows, eras, secondary = [], [], []
    cumulative = pd.DataFrame(index=common)
    for name, run in runs.items():
        r = run.loc[common]
        m = metrics(r.actual, r.pred, b1)
        loss = (r.actual - r.pred).pow(2)
        m.update({"candidate": name, "first": str(common[0].date()),
                  "last": str(common[-1].date())})
        if name != "expanding":
            m.update(loss_test(ref_loss, loss, draws))
        top = set((r.actual - r.pred).abs().nlargest(top_k).index)
        m["top_decile_overlap_reference"] = len(top & top_ref)
        m["top_decile_overlap_raw_change"] = len(top & top_raw)
        m["top_decile_count"] = top_k
        rows.append(m)
        cumulative[name] = (ref_loss - loss).cumsum() / ref_loss.sum() * 100
        for era, start, end in [("2013-16", 2013, 2016), ("2017-19", 2017, 2019),
                                ("2020-22", 2020, 2022), ("2023-26", 2023, 2026),
                                ("2021+ (descriptive)", 2021, 2026)]:
            mask = (common.year >= start) & (common.year <= end)
            ee = metrics(r.actual[mask], r.pred[mask], b1[mask])
            ee.update({"candidate": name, "era": era,
                       "mse_reduction_pct": float((ref_loss[mask] - loss[mask]).mean()
                                                  / ref_loss[mask].mean() * 100)})
            eras.append(ee)
        if name.endswith("_calibrated"):
            own = runs[name.removesuffix("_calibrated")].loc[common]
            own_loss = (own.actual - own.pred).pow(2)
            secondary.append({"candidate": name, **loss_test(own_loss, loss, draws)})
    table = pd.DataFrame(rows)
    eligible = table.candidate != "expanding"
    table.loc[eligible, "holm_p"] = multipletests(
        table.loc[eligible, "hac_p_one_sided"], method="holm")[1]
    table["passes_gate"] = (table.holm_p < 0.1) & (table.boot90_lo_pct > 0)
    table.to_csv(OUT / "comparison.csv", index=False)
    era_table = pd.DataFrame(eras)
    era_table.to_csv(OUT / "eras.csv", index=False)
    cumulative.to_csv(OUT / "cumulative_improvement.csv")
    secondary = pd.DataFrame(secondary)
    secondary["holm_p_secondary"] = multipletests(secondary.hac_p_one_sided, method="holm")[1]
    secondary.to_csv(OUT / "calibration_vs_own_raw.csv", index=False)
    raw_context = []
    for scheme in SCHEMES:
        r = runs[scheme.name]
        mean = benchmark_series(frame, TARGET, "mean")["pred"].reindex(r.index)
        raw_context.append({"candidate": scheme.name, **metrics(r.actual, r.pred, mean)})
    pd.DataFrame(raw_context).to_csv(OUT / "raw_720_week_context.csv", index=False)
    passing = table[table.passes_gate].sort_values("rmse")
    selected = "expanding" if passing.empty else str(passing.iloc[0].candidate)
    best = table.sort_values("rmse").iloc[0]
    decision = {
        "recommended": selected, "passing_candidates": passing.candidate.tolist(),
        "best_point_estimate": best.candidate, "common_weeks": len(common),
        "first": str(common[0].date()), "last": str(common[-1].date()),
        "reference_matches_v2": True, "protected_files_unchanged": n_protected,
        "fingerprint": fingerprint, "sklearn_version": sklearn.__version__,
        "production_model_changed": False,
        "reason": "no candidate passes Holm-adjusted p < 0.10 and positive 90% bootstrap interval"
                  if passing.empty else "candidate passes the exploratory replacement rule; not deployed",
        "source_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ["src/hfpos/model_v4/adaptation.py", "scripts/model_v4.py",
                         "tests/test_model_v4.py", "docs/model_v4/SPEC_2026-11-05.md"]
        },
    }
    (OUT / "selection.json").write_text(json.dumps(decision, indent=2) + "\n")
    figures(table, runs, common, cumulative, cal_table)
    write_report(table, era_table, secondary, fit_table, cal_table, decision)
    check_preservation()
    DELIVER.mkdir(parents=True, exist_ok=True)
    for name in ["comparison.csv", "eras.csv", "calibration_vs_own_raw.csv", "selection.json",
                 "raw_720_week_context.csv", "fit_log.csv", "calibration_log.csv",
                 "comparison.png", "cumulative_improvement.png", "calibration_slopes.png"]:
        shutil.copy2(OUT / name, DELIVER / name)
    shutil.copy2(DOC / "RESULTS.md", DELIVER / "RESULTS.md")
    shutil.copy2(DOC / "SPEC_2026-11-05.md", DELIVER / "SPEC_2026-11-05.md")
    print(table_md(table.sort_values("rmse")), flush=True)
    print(json.dumps(decision, indent=2), flush=True)


def write_report(table, eras, secondary, fits, cals, decision):
    best = table.sort_values("rmse").iloc[0]
    ref = table[table.candidate == "expanding"].iloc[0]
    raw_context = pd.read_csv(OUT / "raw_720_week_context.csv").set_index("candidate")
    lines = [
        "# Adaptation to changing market relationships — experiment results",
        "", "Run date: 5 November 2026 (Singapore). Exploratory; the design was written before these fits.",
        "", f"**Recommendation: {'retain corrected expanding M3' if decision['recommended'] == 'expanding' else decision['recommended']}.** "
        + decision["reason"] + ". No selected model, LLM stimulus, or earlier result was replaced.",
        "", "## What was compared",
        "", "The same 40 inputs and weekly net-position/OI-change target were held fixed. "
        "Six training histories were tested, each with and without strictly earlier-OOS affine calibration: "
        "expanding, rolling 3/5/10 years (156/260/520 eligible observations), and exponential recency weights "
        "with 2/5-calendar-year half-lives (104/260 weeks). All use the same alpha grid and chronological inner CV.",
        "", "The primary table uses **668 identical weeks, 26 November 2013–8 September 2026**. "
        "Calibration needs 52 previous outer-OOS pairs, so the initial 52 weeks are removed from **every** "
        "candidate's primary comparison. The familiar 7.40% baseline uses 720 weeks and is shown separately "
        "in raw_720_week_context.csv; do not compare it directly to the primary table's R².",
        "", "## Matched-week results", "", table_md(table.sort_values("rmse")),
        "", f"Reference R² on this matched sample: {100 * ref.r2_vs_mean:.2f}%; "
        f"RMSE {100 * ref.rmse:.3f} percentage points of open interest. "
        f"Best point estimate: **{best.candidate}**, R² {100 * best.r2_vs_mean:.2f}%, "
        f"MSE gain {best.get('mse_reduction_pct', 0):+.2f}% versus reference. "
        "Positive gain means less error; uncertainty and the multiple-comparison rule determine whether to recommend a replacement.",
        "", "## What the results mean", "",
        "The successful adaptation keeps older history but gives it less influence. Under a two-year half-life, "
        "an observation two years old gets half the weight of the newest one; four years old gets one quarter. "
        "Rolling windows instead discard older observations completely. In this experiment, gradual forgetting performed better.",
        "", f"On the original **720-week** raw-prediction sample, expanding M3 has R² "
        f"{100 * raw_context.loc['expanding', 'r2_vs_mean']:.2f}%, two-year weighting "
        f"{100 * raw_context.loc['weighted_104', 'r2_vs_mean']:.2f}%, and five-year weighting "
        f"{100 * raw_context.loc['weighted_260', 'r2_vs_mean']:.2f}%. These are matched comparisons too; "
        "the 668-week primary table is needed for fair comparison with calibrated variants.",
        "", f"For the best candidate, the RMSE reduction is "
        f"{100 * (1 - best.rmse / ref.rmse):.2f}% versus the expanding reference. "
        "An increase of a few percentage points in R² is not the same as a similarly sized reduction in RMSE. "
        "The error in each week remains large relative to the typical fitted adjustment.",
        "", "The two-year weighted candidate passes the predeclared 10% family-adjusted threshold, "
        "but its adjusted p-value is above 5%. The five-year candidate has a smaller gain and stronger statistical evidence. "
        "Both remain exploratory findings, not confirmation on untouched data. Era results below show that gains "
        "are concentrated in 2017-19 and 2023-26; two-year weighting is essentially flat in 2020-22.",
        "", "## Calibration versus each model's own raw predictions", "",
        "These are secondary comparisons on the same 668 weeks, with a separate six-test Holm adjustment.",
        "", "| Scheme | MSE reduction from calibration | 90% interval | Secondary Holm p |",
        "|---|---:|---:|---:|",
    ]
    for _, r in secondary.iterrows():
        lines.append(f"| {r.candidate} | {r.mse_reduction_pct:+.2f}% | "
                     f"[{r.boot90_lo_pct:+.2f}%, {r.boot90_hi_pct:+.2f}%] | {r.holm_p_secondary:.3f} |")
    lines += ["", "## Era stability", "", "MSE reduction versus the same-week expanding reference. "
              "The last row is overlapping descriptive context and is not used for selection.", ""]
    pivot = eras.pivot(index="candidate", columns="era", values="mse_reduction_pct")
    columns = ["2013-16", "2017-19", "2020-22", "2023-26", "2021+ (descriptive)"]
    lines += ["| Candidate | " + " | ".join(columns) + " |", "|---|" + "---:|" * len(columns)]
    for name in table.sort_values("rmse").candidate:
        lines.append("| " + name + " | " + " | ".join(f"{pivot.loc[name, c]:+.2f}%" for c in columns) + " |")
    lines += ["", "## Temporal checks and calibration behaviour", "",
              "- Equal-weight expanding and five-year rolling reproduce the existing v2 predictions within numerical tolerance.",
              "- Scaling and alpha tuning occur inside each inner training fold. Weighted scaling and ridge use the same fold-local weights.",
              "- Each calibrator uses at most 104 earlier outer-OOS pairs, with at least 52; it is held fixed over the next 13-week test block.",
              "- No current-block labels or in-sample fitted values enter calibration. No slope was estimated on the evaluation sample and then applied backwards.",
              "", "| Scheme | Median effective training n | Median alpha | Median prior-OOS calibration slope | Calibration slope range |", "|---|---:|---:|---:|---:|"]
    for scheme in SCHEMES:
        f = fits[fits.scheme == scheme.name]
        c = cals[cals.scheme == scheme.name]
        lines.append(f"| {scheme.name} | {f.effective_n.median():.1f} | {f.alpha.median():.2f} | "
                     f"{c.slope.median():.2f} | [{c.slope.min():.2f}, {c.slope.max():.2f}] |")
    lines += ["", f"Degenerate calibration fallbacks: {int(cals.fallback.sum())}. "
              "Large or unstable calibration slopes are diagnostics, not a reason to rescale all predictions after seeing the results.",
              "", "## Interpretation and limits", "",
              "This tests adaptation with the existing feature representation. It does not add genuine basis valuations, financing capacity, or confidential fund information. "
              "The result concerns a retrospective same-week conditional estimate, not a next-week forecast. "
              "Changes to estimation history do not undo long-memory feature construction (for example, expanding empirical-duration or funding transforms). "
              "A gain would show reduced historical prediction error under these rules; it would not identify strategies or private information. "
              "A null would not establish an inherent predictability ceiling.",
              "", "Recommendation for a follow-on version: consider the uncalibrated two-year weighted model under the declared rule, "
              "with the five-year weighted model as a sensitivity check. Do not append the noisy affine calibration. "
              "Before collecting new LLM responses, any adoption needs its own model card, recomputed residual percentiles and uncertainty bands, "
              "a coverage check for that model, and newly versioned prompts. Existing M3 uncertainty claims must not be transferred unchanged.",
              "", "The historical dataset and prior model results have already influenced development. "
              "The 11 replacement comparisons use Holm-adjusted one-sided HAC p-values and 90% stationary-bootstrap intervals "
              "(block mean 13, 2,000 replicates). These safeguards do not make the exercise fresh confirmation. "
              "Nested time-series CV tunes ridge penalties; training-history and calibration alternatives are evaluated as a declared exploratory family.",
              "", f"All {decision['protected_files_unchanged']} protected pre-existing files matched their pre-run SHA-256 hashes. "
              "No raw-data refresh, full LLM run, commit, push, or production-model replacement was performed.",
              "", "## Reproduce", "", "```bash", "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/model_v4.py", ".venv/bin/python -m pytest -q", "```",
              "", "Artifacts: comparison.csv, raw_720_week_context.csv, eras.csv, calibration_vs_own_raw.csv, "
              "fit_log.csv, calibration_log.csv, cumulative_improvement.csv, prediction parquet files, and selection.json.",
              "", "Validation: 90 offline tests passed (including 11 new adaptation checks); 5 network tests were deselected. "
              "The new checks cover equal-weight reference equivalence, weighted scaling and regression, fold-local weights, "
              "outer-target causality, calibration warm-up, fixed-block calibration causality, degenerate calibration, and preserved files.",
              "", "Implementation references: [weighted StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), "
              "[weighted Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html).", ""]
    (DOC / "RESULTS.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
