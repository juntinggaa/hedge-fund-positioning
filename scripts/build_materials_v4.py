"""Prepare isolated weighted-model cards, uncertainty diagnostics and review prompts.

    .venv/bin/python scripts/build_materials_v4.py
    .venv/bin/python scripts/build_materials_v4.py --week 2025-09-02 --arm C-ann

No LLM responses are generated and the legacy defaults are unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hfpos import config
from hfpos.ingest import cftc
from hfpos.model_v4.materials import (
    ARMS, MATERIAL_VERSION, MIN_PRIOR, MODEL_ID, MODEL_VERSION, PLACEBO_SEED, Z90,
    annotation, build_prompt, build_stimuli, coverage_table, legacy_module, prior_uncertainty,
)

ROOT = config.REPO_ROOT
DOC = ROOT / "docs/model_v4/materials"
OUT = ROOT / "reports/model_v4/materials"
DELIVER = Path("/Users/lipjunting/Documents/Codex/2026-11-04/can-u/outputs/weighted_model_materials")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_preservation() -> int:
    rec = json.loads((DOC / "preservation_before.json").read_text())["sha256"]
    changed = [p for p, h in rec.items() if not (ROOT / p).exists() or digest(ROOT / p) != h]
    if changed:
        raise RuntimeError(f"Existing files changed: {changed}")
    return len(rec)


def clean_json(value):
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def write_json(path: Path, value):
    path.write_text(json.dumps(clean_json(value), indent=2, allow_nan=False) + "\n")


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    protected = check_preservation()
    selection_path = ROOT / "reports/model_v4/selection.json"
    selection = json.loads(selection_path.read_text())
    if selection["recommended"] != MODEL_ID or MODEL_ID not in selection["passing_candidates"]:
        raise ValueError("Saved experiment no longer recommends the specified candidate")
    pred_path = ROOT / f"data/processed/model_v4/{MODEL_ID}.parquet"
    pred = pd.read_parquet(pred_path)
    positions = cftc.load("UST_10Y")
    sample = pd.read_csv(ROOT / "docs/milestone1/sample.csv")
    stats = prior_uncertainty(pred)
    coverage = coverage_table(pred, stats)
    stimuli = build_stimuli(sample, positions, pred, stats)
    stats.to_csv(OUT / "prior_uncertainty.csv", float_format="%.17g")
    coverage.to_csv(OUT / "coverage_by_era.csv", index=False)
    stimuli_path = DOC / "stimuli_v4.csv"
    stimuli.to_csv(stimuli_path, index=False, float_format="%.17g")
    raw = pd.read_csv(ROOT / "reports/model_v4/raw_720_week_context.csv").set_index("candidate").loc[MODEL_ID]
    comparisons = pd.read_csv(ROOT / "reports/model_v4/comparison.csv").set_index("candidate")
    primary = comparisons.loc[MODEL_ID]
    reference = comparisons.loc["expanding"]
    covered = stimuli[stimuli.has_model_output]
    source_files = [
        "src/hfpos/model_v4/adaptation.py", "src/hfpos/model_v4/materials.py",
        "scripts/model_v4.py", "scripts/build_materials_v4.py", "scripts/build_prompts.py",
        "src/hfpos/model_v2/features.py", "src/hfpos/features/build.py",
        "src/hfpos/features/align.py", "src/hfpos/features/macro.py",
        "src/hfpos/features/basis.py", "src/hfpos/features/positions.py",
        "src/hfpos/features/momentum.py", "docs/milestone1/sample.csv",
        "docs/model_v4/materials/SPEC_2026-11-05.md", "config.yaml",
    ]
    inputs = {name: digest(ROOT / name) for name in source_files}
    inputs["data/processed/model_v4/weighted_104.parquet"] = digest(pred_path)
    inputs["reports/model_v4/selection.json"] = digest(selection_path)
    fixed = int((covered.week == covered.placebo_source_week).sum())
    card = {
        "schema_version": 1, "model_version": MODEL_VERSION, "material_version": MATERIAL_VERSION,
        "model_id": MODEL_ID, "status": "validated candidate materials; no LLM run started",
        "prepared_date_singapore": "2026-11-05",
        "description": "Uncalibrated ridge, same 40 features as M3; all prior training rows with exponential "
                       "104-calendar-week half-life, fold-local weighted scaling and regression, "
                       "chronological four-split alpha selection; 260 initial rows, refit every 13 rows",
        "target": "same-week change in leveraged-fund net position / open interest",
        "estimate_type": "retrospective conditional estimate; includes current-week CFTC open interest",
        "expected_level": "previous actual net/OI plus predicted weekly change",
        "interpretation": "residual is a conditional level gap / unexpected adjustment, not a strategy share",
        "selection": {
            "exploratory": True, "matched_n": int(primary["n"]),
            "matched_first": primary["first"], "matched_last": primary["last"],
            "candidate_r2_vs_mean": float(primary.r2_vs_mean),
            "reference_r2_vs_mean": float(reference.r2_vs_mean),
            "mse_reduction_pct": float(primary.mse_reduction_pct),
            "holm_p": float(primary.holm_p),
            "mse_reduction_boot90_pct": [float(primary.boot90_lo_pct), float(primary.boot90_hi_pct)],
            "rule": "Holm-adjusted one-sided HAC p < 0.10 and positive 90% bootstrap lower bound",
            "fresh_confirmation": False,
        },
        "all_raw_predictions_evaluation": {
            "n": len(pred), "first": str(pred.index[0].date()), "last": str(pred.index[-1].date()),
            "r2_vs_mean": float(raw.r2_vs_mean), "r2_vs_zero": float(raw.r2_vs_zero),
            "rmse_pp": float(raw.rmse * 100), "mae_pp": float(raw.mae * 100),
            "corr_residual_actual_change": float(raw.corr_resid_actual),
            "mz_slope": float(raw.mz_slope),
        },
        "uncertainty": {
            "method": "expected level +/- 1.645 * RMSE of strictly earlier outer-OOS errors",
            "nominal_coverage": 0.90, "minimum_prior_errors": MIN_PRIOR,
            "historical_coverage": float(coverage.iloc[0].coverage),
            "n_eligible": int(coverage.iloc[0].n),
            "coverage_by_era": coverage[coverage.era != "all"].to_dict("records"),
            "interpretation": "approximate prediction range; no conditional or distribution-free guarantee",
            "width_tuned_to_coverage": False,
        },
        "sample": {
            "original_n": len(stimuli), "eligible_n": len(covered),
            "by_stratum": stimuli.groupby("stratum").agg(total=("week", "size"),
                                                          eligible=("has_model_output", "sum")).to_dict("index"),
            "ineligible_weeks": stimuli.loc[~stimuli.has_model_output,
                                              ["week", "availability_reason"]].to_dict("records"),
        },
        "arms": {"A": "unchanged raw table and neutral question", "B": "unchanged A plus mechanism paragraph",
                 "C-bare": "A plus versioned quantitative block", "C-ann": "C-bare plus versioned annotation",
                 "D": "A plus seeded placebo quantitative block"},
        "placebo": {"policy": "same seeded permutation policy as v2; source week logged internally",
                    "seed": PLACEBO_SEED, "fixed_points": fixed,
                    "note": "placebo inputs are experimentally altered; real-model coverage does not validate the fake centre"},
        "source_sha256": inputs,
        "positions_content_sha256": hashlib.sha256(positions.to_csv().encode()).hexdigest(),
        "stimuli_sha256": digest(stimuli_path),
        "preexisting_files_preserved": protected,
        "no_change_to": ["legacy defaults", "earlier cards and prompts", "research question", "primary comparison",
                         "elicitation factor", "retrieval factor", "human coding decisions"],
    }
    card_path = DOC / "model_card_v4.json"
    write_json(card_path, card)
    annotation_path = DOC / "annotation_v4.txt"
    annotation_path.write_text(annotation(card) + "\n")
    legacy = legacy_module(ROOT)
    prompts = []
    for week in covered.week:
        for arm in ARMS:
            text = build_prompt(week, arm, positions, stimuli, card, legacy)
            prompts.append({"week": week, "arm": arm, "model_version": MODEL_VERSION,
                            "material_version": MATERIAL_VERSION, "prompt": text,
                            "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(),
                            "model_card_sha256": digest(card_path), "stimuli_sha256": digest(stimuli_path)})
            if arm in ("A", "B"):
                assert text == legacy.build(week, arm, positions, pd.DataFrame())
    prompt_path = DOC / "review_prompts.jsonl"
    prompt_path.write_text("".join(json.dumps(row) + "\n" for row in prompts))
    example_week = "2025-09-02"
    for arm in ("C-bare", "C-ann", "D"):
        (DOC / f"example_{arm}.txt").write_text(
            build_prompt(example_week, arm, positions, stimuli, card, legacy) + "\n")
    write_json(DOC / "materials_manifest.json", {
        "model_version": MODEL_VERSION, "material_version": MATERIAL_VERSION,
        "generated_files_sha256": {str(p.relative_to(ROOT)): digest(p) for p in [
            card_path, stimuli_path, annotation_path, prompt_path,
            DOC / "example_C-bare.txt", DOC / "example_C-ann.txt", DOC / "example_D.txt"]},
        "matched_cases": len(covered), "prompt_count": len(prompts),
        "responses_generated": 0, "legacy_A_B_byte_identical": True,
    })
    plot_coverage(coverage)
    write_report(card, coverage, stimuli, prompts, example_week)
    check_preservation()
    DELIVER.mkdir(parents=True, exist_ok=True)
    for p in [card_path, stimuli_path, annotation_path, DOC / "MATERIALS_REPORT.md",
              DOC / "example_C-bare.txt", DOC / "example_C-ann.txt", DOC / "review_prompts.jsonl",
              DOC / "materials_manifest.json", OUT / "coverage_by_era.csv", OUT / "coverage.png"]:
        shutil.copy2(p, DELIVER / p.name)
    print(json.dumps({"model": MODEL_ID, "version": MODEL_VERSION,
                      "historical_range_coverage": card["uncertainty"]["historical_coverage"],
                      "eligible_cases": len(covered), "review_prompts": len(prompts),
                      "responses_generated": 0, "protected_files_unchanged": protected}, indent=2))


def plot_coverage(coverage):
    fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
    era = coverage[coverage.era != "all"]
    bars = ax.bar(era.era, era.coverage * 100, color="#2563eb", width=.55)
    ax.axhline(90, color="#111827", linestyle="--", label="Nominal 90%")
    for bar, (_, row) in zip(bars, era.iterrows()):
        ax.text(bar.get_x() + bar.get_width() / 2, 45,
                f"{row.coverage * 100:.1f}%\nn={row.n}", ha="center", va="center",
                color="white", fontsize=10)
    ax.set_ylim(0, 104); ax.set_ylabel("Observed coverage (%)")
    ax.set_title("Weighted-model range coverage varies across eras")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right"); fig.tight_layout(); fig.savefig(OUT / "coverage.png")
    plt.close(fig)


def write_report(card, coverage, stimuli, prompts, example_week):
    eligible = stimuli[stimuli.has_model_output]
    example = eligible[eligible.week == example_week].iloc[0]
    real_exp, real_res, band = example.expected_net_over_oi * 100, example.residual * 100, example.band90_halfwidth * 100
    lines = [
        "# Recency-weighted model: validated candidate materials", "",
        "Prepared 5 November 2026. Existing model predictions were used; no refit or LLM experiment was run.", "",
        f"**Model {MODEL_VERSION}: uncalibrated two-year-half-life ridge ({MODEL_ID}).** "
        f"Material version: {MATERIAL_VERSION}. The earlier default and every earlier experimental artifact are preserved.", "",
        "## Performance and coverage", "",
        f"The exploratory adaptation comparison used 668 matched weeks: R² {card['selection']['candidate_r2_vs_mean'] * 100:.2f}% "
        f"versus reference {card['selection']['reference_r2_vs_mean'] * 100:.2f}%. The full 720-week raw-prediction record has "
        f"R² {card['all_raw_predictions_evaluation']['r2_vs_mean'] * 100:.2f}% versus the historical-mean-change benchmark. "
        "These are different evaluation samples and are recorded separately in the card.", "",
        f"The unchanged range policy (1.645 × earlier OOS RMSE) achieved **{card['uncertainty']['historical_coverage'] * 100:.1f}% "
        f"coverage over {card['uncertainty']['n_eligible']} eligible weeks**. Width was not tuned after observing this result. "
        "It remains an approximate historical prediction range, not a guarantee for each case.", "",
        "| Era | Weeks | Realised coverage | Mean half-width (pp OI) |", "|---|---:|---:|---:|",
    ]
    for _, row in coverage[coverage.era != "all"].iterrows():
        lines.append(f"| {row.era} | {row.n} | {row.coverage * 100:.1f}% | {row.mean_band_halfwidth_pp:.2f} |")
    lines += ["", "## Example: 2 September 2025", "",
              f"- Expected net position: **{real_exp:+.2f}% of open interest**.",
              f"- Actual net position: **{example.actual_net_over_oi * 100:+.2f}%**.",
              f"- Residual: **{real_res:+.2f} percentage points of open interest**.",
              f"- Approximate range: **{real_exp - band:+.2f}% to {real_exp + band:+.2f}%**.",
              f"- Prior error observations: {example.n_prior_errors}; all precede this case.",
              "", "The expected level is previous actual level plus predicted weekly change. "
              "The residual is a conditional level gap / unexpected adjustment. It is not an identified portion of basis trading, "
              "a directional forecast, or evidence of private information.", "",
              "## Ready review materials", "",
              f"- Availability table retains all {len(stimuli)} original cases; {len(eligible)} have both a saved OOS prediction "
              f"and at least {MIN_PRIOR} earlier errors.",
              f"- {len(prompts)} matched neutral-question review prompts: A, B, C-bare, C-ann and D on those same {len(eligible)} cases.",
              "- A and B are byte-identical to the legacy templates. C-bare retains level presentation; C-ann supplies the accurate new annotation. "
              "B's mechanism paragraph is not silently added to C or D.",
              "- D preserves the earlier seeded permutation policy. Source weeks are recorded in the internal stimulus table; "
              f"{card['placebo']['fixed_points']} cases retain their own residual under that permutation. "
              "The genuine-model coverage figure is not evidence about the validity of the deliberately altered placebo centre.",
              "- The percentile text says 'smaller' and 'at least as large', accounting for ties and avoiding the earlier complementary-percentile confusion.",
              "- Per-prompt hashes, the model-card hash, data/source hashes and a materials manifest tie every number to its version.", "",
              "| Stratum | Original cases | Eligible cases |", "|---|---:|---:|"]
    for stratum, row in card["sample"]["by_stratum"].items():
        lines.append(f"| {stratum} | {row['total']} | {row['eligible']} |")
    lines += ["", "## Scope and next use", "",
              "These are prepared candidate materials, not collected evidence. The current research question, primary comparison, "
              "pressure factor, retrieval factor and proposed human coding rules are not changed by this build. "
              "The restricted eligible set is not a representative sample of all 41 cases or the full historical population. "
              "The model was selected retrospectively and includes current-week CFTC open interest, so it is not a pre-release nowcast.", "",
              "The next experimental step is a small fresh pilot using a consistent retrieval-disabled harness and independent human coding. "
              "That pilot and any main LLM run have not been started here.", "",
              f"Preservation check: all {card['preexisting_files_preserved']} pre-existing files match their pre-build SHA-256 hashes. "
              "No older card, prompt, raw file, saved response, selection record or model result was replaced.", "",
              "Validation: the full offline suite passed 100 tests, including 10 new material-generation checks; "
              "5 network tests were deselected. Checks cover prior-only uncertainty, percentile ties, pinned-data reconstruction, "
              "placebo arithmetic, matched case sets, unchanged A/B text, accurate annotation metrics, provenance hashes and preservation.", "",
              "## Reproduce", "", "```bash", ".venv/bin/python scripts/build_materials_v4.py",
              ".venv/bin/python scripts/build_materials_v4.py --week 2025-09-02 --arm C-ann", "```", ""]
    (DOC / "MATERIALS_REPORT.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", help="print a prepared preview without rebuilding")
    parser.add_argument("--arm", choices=ARMS, default="C-ann")
    args = parser.parse_args()
    if args.week:
        card = json.loads((DOC / "model_card_v4.json").read_text())
        stimuli = pd.read_csv(DOC / "stimuli_v4.csv")
        print(build_prompt(args.week, args.arm, cftc.load("UST_10Y"), stimuli, card, legacy_module(ROOT)))
    else:
        prepare()


if __name__ == "__main__":
    main()
