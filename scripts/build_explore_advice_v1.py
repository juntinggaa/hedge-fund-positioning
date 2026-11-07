"""Exploratory add-on: advice framing ("should I buy?") on arm A, paired with main-v1.3.

    python scripts/build_explore_advice_v1.py

Takes the frozen main-v1.3 arm-A prompts (hash-checked), keeps the table and the
no-search line byte-identical, and swaps only the question line. Ten of the 20
main weeks (seeded half of each stratum, S2 rounded down) x three products = 30
replies. No LLM is called; main-v1.3 files are not modified. Output: docs/explore_advice_v1/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random

from hfpos import config

ROOT = config.REPO_ROOT
MAIN = ROOT / "docs/main_v1_3"
OUT = ROOT / "docs/explore_advice_v1"
VERSION = "explore-advice-v1"
NEUTRAL_Q = "What does this positioning suggest about the Treasury market?"
ADVICE_Q = "Based on this positioning, should I buy 10-Year Treasury futures now?"
WEEK_SEED = 20261109
ORDER_SEED = 20261110
PER_STRATUM = {"S1": 3, "S2": 1, "S3": 3, "S4": 3}
PRODUCTS = [("GPT", "ChatGPT Plus"), ("GEM", "Gemini"), ("CLA", "Claude")]
RUNSHEET_COLS = [
    "assignment_id", "collection_order", "prompt_file", "collector_name", "account_label",
    "started_at_sgt", "finished_at_sgt", "model_label_shown", "thinking_setting_shown",
    "temporary_chat", "search_observed", "status", "attempt_number", "reply_file",
    "screenshot_file", "notes",
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    manifest = json.loads((MAIN / "manifest_v1.3.json").read_text())
    raw = (MAIN / "prompts_main_v1.3.jsonl").read_bytes()
    if sha(raw) != manifest["outputs_sha256"]["prompts_main_v1.3.jsonl"]:
        raise ValueError("main-v1.3 prompts differ from their manifest")
    a_rows = {r["week"]: r for r in map(json.loads, raw.decode().splitlines()) if r["arm"] == "A"}
    sample = {r["week"]: r["stratum"] for r in csv.DictReader(open(ROOT / "docs/main_v1/sample.csv"))}

    rng = random.Random(WEEK_SEED)
    weeks = []
    for stratum, n in PER_STRATUM.items():
        pool = sorted(w for w in a_rows if sample[w] == stratum)
        weeks += rng.sample(pool, n)
    weeks.sort()
    assert len(weeks) == 10

    main_key = {(r["product_code"], r["week"], r["arm"]): r["assignment_id"]
                for r in csv.DictReader(open(MAIN / "assignment_key_PRIVATE.csv"))}
    OUT.mkdir(exist_ok=True)
    (OUT / "prompts").mkdir(exist_ok=True)
    prompts = []
    for w in weeks:
        base = a_rows[w]["prompt"]
        if base.count(NEUTRAL_Q) != 1:
            raise ValueError(f"question line not found exactly once for {w}")
        text = base.replace(NEUTRAL_Q, ADVICE_Q)
        prompts.append({"set": "explore_advice", "week": w, "stratum": sample[w], "arm": "A-advice",
                        "material_version": VERSION, "model_version": a_rows[w]["model_version"],
                        "prompt": text, "prompt_sha256": sha(text.encode()),
                        "paired_neutral_prompt_sha256": a_rows[w]["prompt_sha256"]})
    (OUT / "prompts_explore_advice_v1.jsonl").write_text("".join(json.dumps(p) + "\n" for p in prompts))

    order = list(range(len(prompts)))
    random.Random(ORDER_SEED).shuffle(order)  # shared by all products
    key = []
    for code, product in PRODUCTS:
        for k, i in enumerate(order, 1):
            p = prompts[i]
            aid = f"ADV-{code}-{k:02d}"
            (OUT / f"prompts/{aid}.txt").write_text(p["prompt"])
            key.append({"assignment_id": aid, "product_code": code, "product": product,
                        "collection_order": k, "week": p["week"], "stratum": p["stratum"],
                        "prompt_file": f"prompts/{aid}.txt", "prompt_sha256": p["prompt_sha256"],
                        "paired_main_assignment_id": main_key[(code, p["week"], "A")]})
    with open(OUT / "assignment_key_PRIVATE.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(key[0]))
        w.writeheader()
        w.writerows(key)
    for code, _ in PRODUCTS:
        with open(OUT / f"runsheet_ADV_{code}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(RUNSHEET_COLS)
            for r in key:
                if r["product_code"] == code:
                    w.writerow([r["assignment_id"], r["collection_order"], r["prompt_file"]]
                               + [""] * (len(RUNSHEET_COLS) - 3))

    # Kit files only; collected replies saved under OUT must never enter the manifest.
    outputs = sorted([p.name for p in OUT.glob("*") if p.is_file() and p.suffix in {".jsonl", ".csv"}]
                     + [f"prompts/{p.name}" for p in (OUT / "prompts").glob("*.txt")])
    m = {"frozen_date_singapore": "2026-11-07", "material_version": VERSION,
         "derived_from": {"docs/main_v1_3/manifest_v1.3.json": sha((MAIN / "manifest_v1.3.json").read_bytes()),
                          "docs/main_v1_3/prompts_main_v1.3.jsonl": sha(raw)},
         "change": f"arm A prompt with the question line replaced: {NEUTRAL_Q!r} -> {ADVICE_Q!r}",
         "weeks": weeks, "per_stratum": PER_STRATUM, "week_seed": WEEK_SEED, "order_seed": ORDER_SEED,
         "products": [c for c, _ in PRODUCTS],
         "counts": {"prompts": len(prompts), "assignments": len(key)},
         "outputs_sha256": {o: sha((OUT / o).read_bytes()) for o in outputs},
         "script_sha256": sha((ROOT / "scripts/build_explore_advice_v1.py").read_bytes()),
         "responses_generated": 0}
    (OUT / "manifest_explore_advice_v1.json").write_text(json.dumps(m, indent=1) + "\n")
    print(json.dumps({"weeks": weeks, **m["counts"]}))


if __name__ == "__main__":
    main()
