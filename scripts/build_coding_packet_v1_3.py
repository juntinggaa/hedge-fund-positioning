"""Masked coding packet for main-v1.3 (codebook v2.3).

    python scripts/build_coding_packet_v1_3.py

Items: the 180 main replies (docs/main_v1_3/responses/<CODE>/<ID>.md) plus the 16
high-effort Gemini replies (docs/main_v1_3/effort_check_GEM_high/). Each gets a
random blind_id; all 196 are shuffled together (seed) and split into batches, so
coders cannot tell product, arm, week, effort or set. Coders see only the numeric
reference (table, plus model numbers for C arms; the C-ann annotation is withheld,
so C-bare and C-ann look identical) and the reply.

Output: docs/coding_main_v1_3/
    packets/PACKET_<nn>.md   self-contained coder prompt (codebook + replies)
    KEY_PRIVATE.csv          blind_id -> set, assignment, product, arm, week (coordinator only)
    manifest.json            hashes of every input and output
No LLM is called.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "docs/main_v1_3"
OUT = ROOT / "docs/coding_main_v1_3"
CODEBOOK = ROOT / "docs/main_v1/CODEBOOK_v2_3.md"
PILOT_PROMPT = ROOT / "docs/ai_coding_v2_2/PROMPT_v2_3_2_pilot_AB_24.md"  # source of intro + output format
SEED = 20261112
BATCH = 20
NO_SEARCH = "Please answer without using web search."
REF_NOTE = ("Coder reference: this supplies the table and any displayed model numbers. Explanatory text is "
            "withheld to mask annotation assignment. It is not the full LLM prompt. None of these arms "
            "identifies actual strategy shares or trader motives.")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def codebook_body() -> str:
    lines = CODEBOOK.read_text().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## Unit, evidence and scope"))
    skip0 = next(i for i, l in enumerate(lines) if l.startswith("## Independent pilot coding"))
    skip1 = next(i for i, l in enumerate(lines) if l.startswith("## v2.3 additions"))
    # Section headings name the coders that motivated them; strip the parenthetical so no product name appears.
    keep = [l.split(" (")[0] if l.startswith("### v2.3") else l for l in lines[start:skip0] + lines[skip1:]]
    return "\n".join(keep).strip()


def header_and_format() -> tuple[str, str]:
    p = PILOT_PROMPT.read_text()
    intro = p.split("# CODEBOOK v2.3")[0].strip()
    fmt = "# OUTPUT FORMAT" + p.split("# OUTPUT FORMAT", 1)[1].split("# REPLIES TO CODE")[0].rstrip()
    return intro, fmt


def reference(prompt: str) -> str:
    lines = [l for l in prompt.strip().splitlines() if l.strip() != NO_SEARCH]
    return "\n".join(lines).strip() + "\n\n" + REF_NOTE


def main() -> None:
    prompts = {(r["week"], r["arm"]): r["prompt"]
               for r in map(json.loads, open(KIT / "prompts_main_v1.3.jsonl"))}
    key = {r["assignment_id"]: r for r in csv.DictReader(open(KIT / "assignment_key_PRIVATE.csv"))}
    items = []
    for aid, k in key.items():
        items.append(("main", aid, KIT / "responses" / k["product_code"] / f"{aid}.md"))
    for p in sorted((KIT / "effort_check_GEM_high").glob("GEM-*.md")):
        items.append(("effort_high", p.stem, p))
    rng = random.Random(SEED)
    rng.shuffle(items)
    ids = set()
    rows = []
    for n, (set_, aid, path) in enumerate(items):
        while (bid := f"X-{rng.getrandbits(48):012x}") in ids:
            pass
        ids.add(bid)
        k = key[aid]
        ref_arm = "A" if k["arm"] == "A" else "C-bare"  # C-ann shown the C-bare reference
        rows.append({"blind_id": bid, "batch": n // BATCH + 1, "position": n % BATCH + 1, "set": set_,
                     "assignment_id": aid, "product_code": k["product_code"], "arm": k["arm"], "week": k["week"],
                     "effort": "low" if (k["product_code"] == "GEM" and set_ == "main") else "high",
                     "r_applicable": "NO" if k["arm"] == "A" else "YES",
                     "reply_path": str(path.relative_to(ROOT)), "reply_sha256": sha(path.read_bytes()),
                     "reference": reference(prompts[(k["week"], ref_arm)]), "reply": path.read_text().strip()})

    intro, fmt = header_and_format()
    body = codebook_body()
    (OUT / "packets").mkdir(parents=True, exist_ok=True)
    nb = rows[-1]["batch"]
    for b in range(1, nb + 1):
        mine = [r for r in rows if r["batch"] == b]
        parts = [intro, "# CODEBOOK v2.3 (apply exactly)\n\n" + body, fmt,
                 f"# REPLIES TO CODE (batch {b} of {nb}; {len(mine)} replies)"]
        for r in mine:
            parts.append(f"==================== REPLY {r['position']} of {len(mine)} | blind_id: {r['blind_id']} | "
                         f"R applicable: {r['r_applicable']} ====================\n\n"
                         f"----- NUMERIC REFERENCE -----\n{r['reference']}\n\n----- REPLY -----\n{r['reply']}")
        parts.append(f"# END OF BATCH {b}. Return ONLY the JSON array of {len(mine)} objects, in the order given.")
        (OUT / f"packets/PACKET_{b:02d}.md").write_text("\n\n\n".join(parts) + "\n")

    cols = ["blind_id", "batch", "position", "set", "assignment_id", "product_code", "arm", "week",
            "effort", "r_applicable", "reply_path", "reply_sha256"]
    with open(OUT / "KEY_PRIVATE.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    outs = sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file() and p.name != "manifest.json"
                  and not p.parts[len(OUT.parts)].startswith("coder_"))
    m = {"built": "2026-11-07", "codebook": str(CODEBOOK.relative_to(ROOT)), "codebook_sha256": sha(CODEBOOK.read_bytes()),
         "seed": SEED, "batch_size": BATCH, "n_items": len(rows),
         "n_by_set": {s: sum(r["set"] == s for r in rows) for s in ("main", "effort_high")},
         "script_sha256": sha(Path(__file__).read_bytes()),
         "outputs_sha256": {o: sha((OUT / o).read_bytes()) for o in outs}}
    (OUT / "manifest.json").write_text(json.dumps(m, indent=1) + "\n")
    print(json.dumps({k: m[k] for k in ("n_items", "n_by_set")}), f"{nb} batches")


if __name__ == "__main__":
    main()
