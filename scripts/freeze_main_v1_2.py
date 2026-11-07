"""main-v1.2: three products, arms A / C-bare / C-ann, with a manual collection kit.

    python scripts/freeze_main_v1_2.py

Prompt text is byte-identical to main-v1.1 (hash-checked against manifest_v1.1.json);
v1.2 only selects three arms and builds the collection plan. No LLM is called and
no earlier file is modified. Output: docs/main_v1_2/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random

from hfpos import config

ROOT = config.REPO_ROOT
SRC = ROOT / "docs/main_v1"
OUT = ROOT / "docs/main_v1_2"
VERSION = "main-v1.2"
ARMS = ["A", "C-bare", "C-ann"]
ORDER_SEED = 20261107
PRODUCTS = [  # (code, product, model to select, plan)
    ("GPT", "ChatGPT Plus", "GPT-6 Sol (GPT-6.1 Sol if offered in the chat picker)", "ChatGPT Plus"),
    ("GEM", "Gemini", "Gemini 4 Argon", "Google AI Pro"),
    ("CLA", "Claude", "Opus 5.5", "Claude Pro"),
]
RUNSHEET_COLS = [
    "assignment_id", "collection_order", "prompt_file", "collector_name", "account_label",
    "started_at_sgt", "finished_at_sgt", "model_label_shown", "thinking_setting_shown",
    "temporary_chat", "search_observed", "status", "attempt_number", "reply_file",
    "screenshot_file", "notes",
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    m11 = json.loads((SRC / "manifest_v1.1.json").read_text())
    raw = (SRC / "prompts_main_v1.1.jsonl").read_bytes()
    if sha(raw) != m11["outputs_sha256"]["prompts_main_v1.1.jsonl"]:
        raise ValueError("prompts_main_v1.1.jsonl differs from manifest_v1.1.json")
    rows = [json.loads(l) for l in raw.decode().splitlines()]
    keep = [r for r in rows if r["arm"] in ARMS]
    for r in keep:
        if sha(r["prompt"].encode()) != r["prompt_sha256"]:
            raise ValueError(f"prompt hash mismatch {r['week']} {r['arm']}")
    assert len(keep) == 99, len(keep)

    OUT.mkdir(exist_ok=True)
    (OUT / "prompts").mkdir(exist_ok=True)
    prompts = [{**r, "material_version": VERSION, "v1_1_prompt_sha256": r["prompt_sha256"]}
               for r in keep]
    (OUT / "prompts_main_v1.2.jsonl").write_text("".join(json.dumps(r) + "\n" for r in prompts))

    rng = random.Random(ORDER_SEED)
    assignments = []
    for code, product, model, plan in PRODUCTS:
        order = list(range(len(prompts)))
        rng.shuffle(order)
        for k, i in enumerate(order, 1):
            p = prompts[i]
            aid = f"{code}-{k:03d}"
            fname = f"prompts/{aid}.txt"
            (OUT / fname).write_text(p["prompt"])
            assignments.append({
                "assignment_id": aid, "product_code": code, "product": product,
                "model_to_select": model, "plan": plan, "collection_order": k,
                "week": p["week"], "arm": p["arm"], "role": p["role"],
                "prompt_file": fname, "prompt_sha256": p["prompt_sha256"],
            })

    # Private key (week/arm per assignment): coordinator only, never given to coders.
    with open(OUT / "assignment_key_PRIVATE.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(assignments[0]))
        w.writeheader()
        w.writerows(assignments)
    # Runsheets for collectors: no week/arm columns.
    for code, product, model, plan in PRODUCTS:
        with open(OUT / f"runsheet_{code}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(RUNSHEET_COLS)
            for a in assignments:
                if a["product_code"] == code:
                    w.writerow([a["assignment_id"], a["collection_order"], a["prompt_file"]]
                               + [""] * (len(RUNSHEET_COLS) - 3))

    outputs = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*")
                     if p.is_file() and p.name != "manifest_v1.2.json"
                     and p.suffix in {".jsonl", ".csv", ".txt"})
    manifest = {
        "frozen_date_singapore": "2026-11-06", "material_version": VERSION,
        "derived_from": {"docs/main_v1/manifest_v1.1.json": sha((SRC / "manifest_v1.1.json").read_bytes()),
                         "docs/main_v1/prompts_main_v1.1.jsonl": sha(raw)},
        "change": "selected arms A, C-bare, C-ann (B and D dropped); prompt text unchanged; "
                  "three products; seeded per-product collection order",
        "arms": ARMS, "order_seed": ORDER_SEED,
        "products": [{"code": c, "product": p, "model_to_select": m, "plan": pl} for c, p, m, pl in PRODUCTS],
        "counts": {"prompts": len(prompts), "weeks": len({p["week"] for p in prompts}),
                   "assignments": len(assignments)},
        "outputs_sha256": {o: sha((OUT / o).read_bytes()) for o in outputs},
        "script_sha256": sha((ROOT / "scripts/freeze_main_v1_2.py").read_bytes()),
        "responses_generated": 0,
    }
    (OUT / "manifest_v1.2.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(json.dumps(manifest["counts"]))


if __name__ == "__main__":
    main()
