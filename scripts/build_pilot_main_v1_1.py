"""Prepare fresh pilot materials and a 60-run queue. Never calls an LLM.

The main sample/prompts, original codebook, and all pinned model inputs are read-only.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.llm.experiment import exact_power
from hfpos.model_v4 import materials as m

ROOT = config.REPO_ROOT
OUT = ROOT / "docs/pilot_main_v1_1"
VERSION = "pilot-main-v1.1-2026-11-06"
DATE = "2026-11-06"
SEED = 20261106
NO_SEARCH = "Please answer without using web search."
DEVELOPMENT = {"2014-03-04", "2023-07-11", "2025-02-18", "2025-06-17",
               "2026-06-30", "2026-08-25", "2026-09-01"}
PRODUCTS = (
    {"product_id": "chatgpt_free", "product": "ChatGPT Free", "profile": "Jingyen",
     "requested_mode": "Default mode of genuinely free account; record visible label"},
    {"product_id": "chatgpt_plus", "product": "ChatGPT Plus", "profile": "Junting",
     "requested_mode": "High thinking effort; record visible model label"},
    {"product_id": "gemini_free", "product": "Gemini Free", "profile": "Junting",
     "requested_mode": "Auto, Low; verify available controls before first run"},
    {"product_id": "gemini_pro", "product": "Gemini on Google AI Pro", "profile": "Jingyen",
     "requested_mode": "Argon High; verify visible label before first run"},
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derangement(n: int, seed: int = m.PLACEBO_SEED) -> tuple[np.ndarray, int]:
    if n < 2:
        raise ValueError("need at least two distinct cases for a placebo derangement")
    rng = np.random.default_rng(seed)
    for attempt in range(1, 100001):
        p = rng.permutation(n)
        if (p != np.arange(n)).all():
            return p, attempt
    raise RuntimeError("derangement draw limit exceeded")


def choose_cases(pos: pd.DataFrame, pred: pd.DataFrame, excluded: set[str]) -> tuple[pd.DataFrame, dict]:
    """Seeded uniform draw by sign/state only; no residual size or LLM scores."""
    stats = m.prior_uncertainty(pred)
    original = pd.read_parquet(ROOT / "data/raw/cftc_tff_ust_10y.parquet")
    old_s = original.leveraged_funds_net / original.open_interest
    cut = float(old_s[old_s < 0].quantile(.1))
    s = pos.leveraged_funds_net / pos.open_interest
    eligible = s.index.isin(stats.index[stats.band90_halfwidth.notna()])
    available = ~s.index.strftime("%Y-%m-%d").isin(excluded)
    definitions = [("net_long", s > 0), ("moderate_short", (s < 0) & (s > cut)),
                   ("extreme_short", (s <= cut) & (s.index >= "2015-01-01"))]
    selected, pools = [], {}
    for i, (kind, mask) in enumerate(definitions):
        pool = s.index[mask & eligible & available].sort_values()
        pools[kind] = len(pool)
        if pool.empty:
            raise ValueError(f"no fresh eligible {kind} case")
        day = pool[random.Random(SEED + i).randrange(len(pool))]
        st = ("S1" if s[day] > 0 else "S4" if s[day] <= cut else
              "S2" if day < pd.Timestamp("2015-01-01") else "S3")
        selected.append({"week": str(day.date()), "frame": "pilot_validation", "stratum": st,
                         "case_type": kind, "role": "pilot only", "net_over_oi": float(s[day]),
                         "n_prior_errors": int(stats.loc[day, "n_prior_errors"])})
    return pd.DataFrame(selected), {"frozen_cut": cut, "eligible_pool_sizes_after_exclusions": pools}


def make_queue(prompts: list[dict]) -> list[dict]:
    by_key = {(p["week"], p["arm"]): p for p in prompts}
    weeks = sorted({p["week"] for p in prompts})
    rng = random.Random(SEED)
    rng.shuffle(weeks)
    arms = list(m.ARMS)
    rng.shuffle(arms)
    jobs = []
    for wi, week in enumerate(weeks):
        products = list(enumerate(PRODUCTS))
        rng.shuffle(products)
        for pi, product in products:
            offset = (wi + pi) % len(arms)
            for arm in arms[offset:] + arms[:offset]:
                p = by_key[week, arm]
                key = f"{VERSION}|{product['product_id']}|{week}|{arm}|rep1"
                blind = "B-" + hashlib.sha256(("blind|" + key).encode()).hexdigest()[:12]
                jobs.append({"run_id": f"PV11-{len(jobs) + 1:03d}", "blind_id": blind,
                             "collection_order": len(jobs) + 1, **product, **p,
                             "replicate": 1, "elicitation": "neutral", "status": "pending"})
    return jobs


def build(out: Path = OUT) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    inputs = {}
    def pin(path):
        path = ROOT / path
        inputs[str(path.relative_to(ROOT))] = sha(path)
        return path
    v1 = json.loads(pin("docs/main_v1/manifest.json").read_text())
    v11 = json.loads(pin("docs/main_v1/manifest_v1.1.json").read_text())
    for path, expected in v1["inputs_sha256"].items():
        if sha(pin(path)) != expected:
            raise ValueError(f"main input pin differs: {path}")
    for name, expected in v1["outputs_sha256"].items():
        if sha(pin("docs/main_v1/" + name)) != expected:
            raise ValueError(f"main material pin differs: {name}")
    for name, expected in v11["outputs_sha256"].items():
        if sha(pin("docs/main_v1/" + name)) != expected:
            raise ValueError(f"v1.1 material pin differs: {name}")
    for name in ["docs/main_v1/FREEZE.md", "docs/main_v1/AMENDMENT_2026-11-06.md",
                 "docs/main_v1/CODEBOOK_v2_1_PILOT.md", "docs/main_v1/ANALYSIS_v1_1.md",
                 "docs/milestone2/codebook.md", "docs/pilot_main_v1_1/SPEC.md",
                 "scripts/build_pilot_main_v1_1.py", "scripts/validate_pilot_main_v1_1.py",
                 "src/hfpos/llm/experiment.py"]:
        pin(name)
    pos = pd.read_parquet(ROOT / "data/raw/sampling_review_2026-11-05/cftc_tff_ust_10y.parquet")
    pred = pd.read_parquet(ROOT / "data/raw/sampling_review_2026-11-05/weighted_104_extended.parquet")
    main = pd.read_csv(ROOT / "docs/main_v1/sample.csv")
    original = pd.read_csv(ROOT / "docs/milestone1/sample.csv")
    excluded = set(main.week) | set(original.week) | DEVELOPMENT
    rules = {"version": VERSION, "date_singapore": DATE, "seed": SEED,
             "categories": ["one net long", "one moderate short (S2 or S3)", "one extreme short, 2015+"],
             "eligibility": "v4 output and at least 52 strictly earlier weekly OOS errors",
             "selection": "sorted eligible dates; independent seeded uniform choice per category",
             "exclusions": sorted(excluded), "LLM_outcomes_used": False,
             "residual_magnitudes_used_for_selection": False,
             "spacing": "main sample's spacing is preserved; no pilot-to-main spacing guarantee"}
    written = []
    def write(name, content):
        path = out / name
        content = content.encode() if isinstance(content, str) else content
        path.parent.mkdir(parents=True, exist_ok=True)
        if (out / "responses.jsonl").exists() and (out / "responses.jsonl").stat().st_size:
            if not path.exists() or path.read_bytes() != content:
                raise ValueError("responses already exist; create a new pilot version before changing materials")
        path.write_bytes(content)
        written.append(name)
    def dump(name, obj):
        write(name, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    dump("selection_rules.json", rules)  # written before the first date selection
    cases, case_info = choose_cases(pos, pred, excluded)
    stimuli = m.build_stimuli(cases, pos, pred, m.prior_uncertainty(pred))
    assert stimuli.has_model_output.all()
    permutation, attempts = derangement(len(stimuli))
    errors = pred.actual - pred.pred
    for dest, source in enumerate(permutation):
        value = float(stimuli.loc[source, "residual"])
        stimuli.loc[dest, "placebo_source_week"] = stimuli.loc[source, "week"]
        stimuli.loc[dest, "placebo_residual"] = value
        stimuli.loc[dest, "placebo_expected_net_over_oi"] = stimuli.loc[dest, "actual_net_over_oi"] - value
        stimuli.loc[dest, "placebo_residual_abs_pct_vs_prior"] = m.percentile_for_value(
            errors, pd.Timestamp(stimuli.loc[dest, "week"]), value)
    stimuli["material_version"] = VERSION
    write("cases.csv", cases.to_csv(index=False, float_format="%.17g"))
    write("stimuli.csv", stimuli.to_csv(index=False, float_format="%.17g"))
    card = json.loads((ROOT / "docs/model_v4/materials/model_card_v4.json").read_text())
    legacy = m.legacy_module(ROOT)
    prompts = []
    for week in cases.week:
        for arm in m.ARMS:
            text = m.build_prompt(week, arm, pos, stimuli, card, legacy) + "\n\n" + NO_SEARCH
            prompts.append({"week": week, "arm": arm, "role": "pilot only",
                            "material_version": VERSION, "model_version": m.MODEL_VERSION,
                            "prompt": text, "prompt_sha256": hashlib.sha256(text.encode()).hexdigest()})
    write("prompts.jsonl", "".join(json.dumps(p) + "\n" for p in prompts))
    queue = make_queue(prompts)
    assert len(queue) == 60 and len({q["blind_id"] for q in queue}) == 60
    write("collection_queue.jsonl", "".join(json.dumps(q) + "\n" for q in queue))
    metadata = pd.DataFrame([{k: v for k, v in q.items() if k != "prompt"} for q in queue])
    write("collector_key_PRIVATE.csv", metadata.to_csv(index=False))
    for product in PRODUCTS:
        pid = product["product_id"]
        write(pid + "_runsheet.csv", metadata.loc[metadata.product_id == pid].to_csv(index=False))
    lookup = {(p["week"], p["arm"]): p for p in prompts}
    by_week = stimuli.set_index("week")
    sheets = []
    for q in queue:
        # Identical numeric reference for C-bare/C-ann. Annotation and B explainer
        # are withheld; primary codes concern claims not identified in ANY arm.
        raw_a = lookup[q["week"], "A"]["prompt"]
        reference = raw_a.removesuffix("\n\n" + NO_SEARCH)
        if q["arm"] in ("C-bare", "C-ann", "D"):
            reference += "\n\n" + m.model_block(by_week.loc[q["week"]], placebo=q["arm"] == "D")
        reference += ("\n\nCoder reference: this supplies the table and any displayed model numbers. "
                      "Explanatory text is withheld to mask annotation assignment. It is not the full LLM prompt. "
                      "None of these arms identifies actual strategy shares or trader motives.\n")
        evidence = f"evidence/{q['blind_id']}.txt"
        write(evidence, reference)
        sheets.append({"blind_id": q["blind_id"], "evidence_file": evidence,
                       "response_text": "", "scoring_status": "", "B2": "", "B2_quote": "",
                       "B2_target": "", "B3": "", "B3_quote": "", "B3_target": "",
                       "R": "", "R_quote": "", "R_applicable": q["arm"] in ("C-bare", "C-ann", "D"),
                       "notes": ""})
    for coder in (1, 2):
        sheet = pd.DataFrame(sheets).sample(frac=1, random_state=SEED + 100 + coder)
        write(f"coder{coder}_template.csv", sheet.to_csv(index=False))
    template = []
    for q in queue:
        template.append({"run_id": q["run_id"], "prompt_sha256": q["prompt_sha256"],
                         "status": "pending", "response_text": "", "observed_model_label": "",
                         "observed_thinking_label": "", "temporary_chat_verified": None,
                         "started_at_utc": "", "completed_at_utc": "",
                         "retrieval_observation": "unknown", "citations_observed": None,
                         "submitted_prompt_sha256": "", "prompt_verification": "unverified",
                         "response_sha256": "", "capture_method": "", "screenshot_files": [],
                         "technical_notes": ""})
    write("responses_template.jsonl", "".join(json.dumps(q) + "\n" for q in template))
    power = [{"n_weeks": 32, "fixed_alpha": .0125, "p_bare_only": b, "p_ann_only": c,
              "true_delta_ann_minus_bare": c - b, "exact_power_at_fixed_cutoff": exact_power(32, b, c)}
             for b, c in [(.15, .05), (.25, .05), (.30, .10), (.35, .05)]]
    write("power_scenarios.csv", pd.DataFrame(power).to_csv(index=False))
    packet = "# Pilot prompts (collector only)\n\n"
    for p in prompts:
        packet += f"## {p['week']} — {p['arm']}\n\n{p['prompt']}\n\n---\n\n"
    write("collector_prompts.md", packet)
    preservation = json.loads((OUT / "preservation_before.json").read_text())
    changed = [path for path, expected in preservation.items() if sha(ROOT / path) != expected]
    if set(changed) - {"docs/main_v1/FREEZE.md"}:
        raise ValueError(f"protected files changed: {changed}")
    dump("preservation_check.json", {"files_checked": len(preservation),
         "authorized_document_amendments": changed, "unauthorized_changes": []})
    case_table = "| Category | Week | Stratum | Earlier OOS errors |\n|---|---|---|---:|\n"
    case_table += "".join(f"| {r.case_type} | {r.week} | {r.stratum} | {r.n_prior_errors} |\n"
                          for r in cases.itertuples())
    report = ("# Fresh pilot materials ready\n\n"
              f"Version: {VERSION}. Built without LLM calls.\n\n"
              "Three fresh cases, 15 unique prompts, 60 planned responses across four products. "
              "All cases are outside the main/original samples and known development cases. "
              "Dates were chosen without residual magnitudes or LLM results. This is a validation sample, "
              "not a historical prevalence sample.\n\n" + case_table + "\n"
              "Use prompts.jsonl or the collector packet; follow collection_queue.jsonl. "
              "Profile mapping: Jingyen = ChatGPT Free / Gemini Pro; Junting = ChatGPT Plus / Gemini Free. "
              "Verify the requested modes before collecting; do not change account-wide settings. "
              "Use a fresh Temporary Chat for each prompt and save the first completed reply immediately. "
              "Retain refusals and searched responses; log visible retrieval separately from citations.\n\n"
              "Copy responses_template.jsonl to responses.jsonl and fill it; never fill the template itself. "
              "The build does not overwrite responses.jsonl or completed coding files. "
              "Do not regenerate satisfactory or inconvenient answers. Record technical retries in a separate attempt log.\n\n"
              "After collection run `python scripts/validate_pilot_main_v1_1.py prepare --responses PATH --out PATH`. "
              "Give each coder their separate packet, the numeric references, and CODEBOOK_v2_1_PILOT.md. "
              "Do not give coders the collector key, queue, model labels or the annotation text. "
              "Blinding is partial: response content can itself reveal the condition. "
              "Coders work independently; keep original scores before adjudication.\n\n"
              "Run the validator's `agreement` command on completed coder CSVs. "
              "It reports pooled reliability without product/arm outcome contrasts. Constant scores produce "
              "undefined kappa, not invented perfect reliability. Main collection remains on hold until the "
              "pilot is reviewed and the operational codebook is validated. No significant pilot arm difference is required.\n")
    write("README.md", report)
    manifest = {"version": VERSION, "date_singapore": DATE,
                "selection": case_info, "cases": list(cases.week),
                "counts": {"unique_prompts": 15, "planned_responses": 60, "products": 4,
                           "responses_generated_by_build": 0},
                "placebo": {"seed": m.PLACEBO_SEED, "attempts": attempts,
                            "fixed_points": int((stimuli.week == stimuli.placebo_source_week).sum()),
                            "scope": "permutation of three pilot residuals only; main placebo unchanged"},
                "inputs_sha256": inputs,
                "outputs_sha256": {name: sha(out / name) for name in sorted(written)}}
    write("manifest.json", json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = build()
    print(json.dumps({"cases": result["cases"], **result["counts"]}, indent=2))
