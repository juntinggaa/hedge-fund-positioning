"""main-v1.1: the frozen main-v1 prompts plus one no-search line, identical in every arm.

    python scripts/freeze_main_v1_1.py

Derived only from docs/main_v1/prompts_*.jsonl (hash-checked against manifest.json);
the v1 files are not modified. No LLM is called.
"""

from __future__ import annotations

import hashlib
import json

from hfpos import config

ROOT = config.REPO_ROOT
D = ROOT / "docs/main_v1"
VERSION = "main-v1.1"
NO_SEARCH = "Please answer without using web search."
PRODUCTS = ["ChatGPT Free", "ChatGPT Plus", "Gemini Free", "Gemini paid (Google AI Pro)"]
SOURCES = {"prompts_main.jsonl": "prompts_main_v1.1.jsonl",
           "prompts_supplement_AB_optional.jsonl": "prompts_supplement_AB_optional_v1.1.jsonl"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    v1 = json.loads((D / "manifest.json").read_text())
    out_hashes, counts = {}, {}
    for src, dst in SOURCES.items():
        raw = (D / src).read_bytes()
        if sha(raw) != v1["outputs_sha256"][src]:
            raise ValueError(f"{src} differs from the frozen main-v1 manifest")
        rows = []
        for line in raw.decode().splitlines():
            p = json.loads(line)
            text = p["prompt"] + "\n\n" + NO_SEARCH
            rows.append({**p, "material_version": VERSION, "prompt": text,
                         "prompt_sha256": sha(text.encode()),
                         "v1_prompt_sha256": p["prompt_sha256"]})
        (D / dst).write_text("".join(json.dumps(r) + "\n" for r in rows))
        out_hashes[dst] = sha((D / dst).read_bytes())
        counts[dst] = len(rows)
    manifest = {
        "frozen_date_singapore": "2026-11-06", "material_version": VERSION,
        "derived_from": {"docs/main_v1/manifest.json": sha((D / "manifest.json").read_bytes()),
                         **{f"docs/main_v1/{s}": v1["outputs_sha256"][s] for s in SOURCES}},
        "change": f"appended '\\n\\n{NO_SEARCH}' to every prompt, all arms identically",
        "products": PRODUCTS,
        "counts": {**counts, "main_responses_four_products": 4 * counts["prompts_main_v1.1.jsonl"],
                   "supplement_responses_four_products":
                       4 * counts["prompts_supplement_AB_optional_v1.1.jsonl"]},
        "outputs_sha256": out_hashes,
        "script_sha256": sha((ROOT / "scripts/freeze_main_v1_1.py").read_bytes()),
        "responses_generated": 0,
    }
    (D / "manifest_v1.1.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(json.dumps(manifest["counts"], indent=1))


if __name__ == "__main__":
    main()
