"""Freeze the main-experiment sample (Option B, 8-week spacing) and build its prompts.

    python scripts/freeze_main_v1.py

Inputs (all hash-checked, none modified):
  reports/sampling_review_2026-11-05/B_8w_dates.csv     candidate dates (seeded, outcome-blind)
  data/raw/sampling_review_2026-11-05/*                 append-only extended panel + frozen v4 extension
  docs/model_v4/materials/model_card_v4.json            frozen v4 card (annotation text source)
Outputs: docs/main_v1/ only. No LLM is called.
"""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.model_v4 import materials as m

ROOT = config.REPO_ROOT
OUT = ROOT / "docs/main_v1"
EXT = ROOT / "data/raw/sampling_review_2026-11-05"
CANDIDATES = ROOT / "reports/sampling_review_2026-11-05/B_8w_dates.csv"
EXT_MANIFEST = ROOT / "reports/sampling_review_2026-11-05/data_manifest.json"
CARD = ROOT / "docs/model_v4/materials/model_card_v4.json"
ORIGINAL_SAMPLE = ROOT / "docs/milestone1/sample.csv"
PURPOSIVE = "2025-09-02"
MATERIAL_VERSION = "main-v1"
GAP_DAYS = 56
DEV_WEEKS = {"2023-07-11", "2025-02-18", "2025-06-17", "2026-06-30", "2026-08-25", "2026-09-01"}
LABELS = {"S1": "S1 LF net long", "S2": "S2 moderate short, pre-2015",
          "S3": "S3 moderate short, 2015+", "S4": "S4 extreme short, 2015+", "P": "purposive"}


def sha(path) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_extension() -> dict:
    pins = json.loads(EXT_MANIFEST.read_text())["files"]
    bad = [f for f, h in pins.items() if sha(ROOT / f) != h]
    if bad:
        raise ValueError(f"extended data changed since the sampling review: {bad}")
    return pins


def load_inputs():
    positions = pd.read_parquet(EXT / "cftc_tff_ust_10y.parquet")
    pinned = pd.read_parquet(ROOT / "data/raw/cftc_tff_ust_10y.parquet")
    if not positions.iloc[:len(pinned)].equals(pinned):
        raise ValueError("extended panel does not reproduce the pinned history")
    preds = pd.read_parquet(EXT / "weighted_104_extended.parquet")
    frozen = pd.read_parquet(ROOT / f"data/processed/model_v4/{m.MODEL_ID}.parquet")
    common = frozen.index
    if not preds.loc[common, ["actual", "pred"]].equals(frozen[["actual", "pred"]]):
        raise ValueError("extended predictions do not reproduce frozen v4")
    return positions, preds


def main_sample() -> pd.DataFrame:
    c = pd.read_csv(CANDIDATES)
    c = c[c.option == "B_8w"].copy()
    rows = [{"week": w, "frame": "stratified", "stratum": s, "role": "inferential"}
            for w, s in zip(c.week, c.stratum)]
    rows.append({"week": PURPOSIVE, "frame": "purposive", "stratum": "P", "role": "qualitative only"})
    out = pd.DataFrame(rows)
    out["stratum_label"] = out.stratum.map(LABELS)
    return out.sort_values(["frame", "stratum", "week"], ascending=[False, True, True]).reset_index(drop=True)


def supplement_sample() -> pd.DataFrame:
    """Optional historical A/B supplement: original weeks the model cannot cover."""
    v4 = pd.read_csv(ROOT / "docs/model_v4/materials/stimuli_v4.csv")
    s = v4.loc[~v4.has_model_output, ["week", "frame", "stratum"]].copy()
    s["role"] = "optional descriptive A/B supplement"
    s["stratum_label"] = s.stratum.map(LABELS)
    return s.reset_index(drop=True)


def derange_placebo(stimuli: pd.DataFrame, preds: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Replace the v4 permutation by a seeded derangement: no week shows its own residual.

    Rejection sampling from the same seeded generator (uniform over derangements).
    Outcome-blind: depends only on the number of weeks and the seed."""
    out = stimuli.copy()
    n = len(out)
    rng = np.random.default_rng(m.PLACEBO_SEED)
    attempts = 0
    while True:
        attempts += 1
        perm = rng.permutation(n)
        if not (perm == np.arange(n)).any():
            break
    errors = preds.actual - preds.pred
    for dest, src in enumerate(perm):
        value = float(out.loc[src, "residual"])
        out.loc[dest, "placebo_source_week"] = out.loc[src, "week"]
        out.loc[dest, "placebo_residual"] = value
        out.loc[dest, "placebo_expected_net_over_oi"] = out.loc[dest, "actual_net_over_oi"] - value
        out.loc[dest, "placebo_residual_abs_pct_vs_prior"] = m.percentile_for_value(
            errors, pd.Timestamp(out.loc[dest, "week"]), value)
    return out, attempts


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pins = check_extension()
    positions, preds = load_inputs()
    card = json.loads(CARD.read_text())
    legacy = m.legacy_module(ROOT)

    sample = main_sample()
    stats = m.prior_uncertainty(preds)
    stimuli = m.build_stimuli(sample, positions, preds, stats)
    stimuli["material_version"] = MATERIAL_VERSION
    if not stimuli.has_model_output.all():
        raise ValueError("every main-sample week must have eligible model output")
    v4_fixed = int((stimuli.week == stimuli.placebo_source_week).sum())
    stimuli, attempts = derange_placebo(stimuli.reset_index(drop=True), preds)
    sample = sample.merge(stimuli[["week", "actual_net_over_oi"]], on="week")
    sample.to_csv(OUT / "sample.csv", index=False, float_format="%.17g")
    stimuli.to_csv(OUT / "stimuli.csv", index=False, float_format="%.17g")

    prompts = []
    for week in sample.week:
        for arm in m.ARMS:
            text = m.build_prompt(week, arm, positions, stimuli, card, legacy)
            if arm in ("A", "B"):
                assert text == legacy.build(week, arm, positions, pd.DataFrame())
            prompts.append({"set": "main", "week": week, "arm": arm,
                            "role": sample.set_index("week").loc[week, "role"],
                            "material_version": MATERIAL_VERSION, "model_version": m.MODEL_VERSION,
                            "prompt": text, "prompt_sha256": hashlib.sha256(text.encode()).hexdigest()})
    (OUT / "prompts_main.jsonl").write_text("".join(json.dumps(p) + "\n" for p in prompts))

    supp = supplement_sample()
    supp.to_csv(OUT / "supplement_AB_optional.csv", index=False)
    pinned_positions = pd.read_parquet(ROOT / "data/raw/cftc_tff_ust_10y.parquet")
    sprompts = []
    for week in supp.week:
        for arm in ("A", "B"):
            text = legacy.build(week, arm, pinned_positions, pd.DataFrame())
            sprompts.append({"set": "supplement_optional", "week": week, "arm": arm,
                             "role": "optional descriptive A/B supplement",
                             "material_version": MATERIAL_VERSION, "prompt": text,
                             "prompt_sha256": hashlib.sha256(text.encode()).hexdigest()})
    (OUT / "prompts_supplement_AB_optional.jsonl").write_text(
        "".join(json.dumps(p) + "\n" for p in sprompts))

    covered = stimuli[stimuli.has_model_output]
    manifest = {
        "frozen_date_singapore": "2026-11-05",
        "material_version": MATERIAL_VERSION, "model_version": m.MODEL_VERSION, "model_id": m.MODEL_ID,
        "design": "Option B, 8-week within-stratum spacing, 10/2/10/10 + purposive",
        "counts": {"inferential_weeks": int((sample.role == "inferential").sum()),
                   "purposive_weeks": int((sample.role != "inferential").sum()),
                   "main_prompts": len(prompts), "main_responses_two_llms": 2 * len(prompts),
                   "supplement_weeks": len(supp), "supplement_prompts": len(sprompts),
                   "supplement_responses_two_llms": 2 * len(sprompts)},
        "placebo": {"seed": m.PLACEBO_SEED,
                    "policy": "seeded derangement over all main weeks (rejection sampling, same generator)",
                    "attempts": attempts, "v4_policy_fixed_points_on_this_sample": v4_fixed,
                    "fixed_points": int((covered.week == covered.placebo_source_week).sum())},
        "inputs_sha256": {
            str(CANDIDATES.relative_to(ROOT)): sha(CANDIDATES),
            str(EXT_MANIFEST.relative_to(ROOT)): sha(EXT_MANIFEST),
            str(CARD.relative_to(ROOT)): sha(CARD),
            str(ORIGINAL_SAMPLE.relative_to(ROOT)): sha(ORIGINAL_SAMPLE),
            "data/raw/cftc_tff_ust_10y.parquet": sha(ROOT / "data/raw/cftc_tff_ust_10y.parquet"),
            f"data/processed/model_v4/{m.MODEL_ID}.parquet":
                sha(ROOT / f"data/processed/model_v4/{m.MODEL_ID}.parquet"),
            "scripts/build_prompts.py": sha(ROOT / "scripts/build_prompts.py"),
            "src/hfpos/model_v4/materials.py": sha(ROOT / "src/hfpos/model_v4/materials.py"),
            "scripts/freeze_main_v1.py": sha(ROOT / "scripts/freeze_main_v1.py"),
            **pins},
        "outputs_sha256": {f: sha(OUT / f) for f in ("sample.csv", "stimuli.csv", "prompts_main.jsonl",
                                                     "supplement_AB_optional.csv",
                                                     "prompts_supplement_AB_optional.jsonl")},
        "responses_generated": 0,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(json.dumps(manifest["counts"] | {"placebo_fixed_points": manifest["placebo"]["fixed_points"]},
                     indent=1))


if __name__ == "__main__":
    main()
