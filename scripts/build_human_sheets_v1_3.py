"""Human adjudication + reliability sample for main-v1.3 coding.

    python scripts/build_human_sheets_v1_3.py

Picks 30 replies: every reply where the two machine coders disagree on a composite
(DISAGREEMENTS.csv) plus a seeded random sample of agreed main replies. Each reply goes
to one pair of people (6 pairs x 5), so each person codes 15. Disputed and agreed
replies are mixed and look identical; machine codes are not shown.

Output: docs/coding_main_v1_3/human/
    SEND_<Name>/  CODING_GUIDE.md, CODEBOOK_v2_3.md, REPLIES_<Name>.md, SHEET_<Name>.csv
    HUMAN_KEY_PRIVATE.csv   item -> pair, disputed flag (coordinator only)
"""

from __future__ import annotations

import csv
import itertools
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PK = ROOT / "docs/coding_main_v1_3"
OUT = PK / "human"
PEOPLE = ["JunTing", "Tia", "Neeti", "Xavier"]
N_TOTAL = 30
SEED = 20261113
NO_SEARCH = "Please answer without using web search."

GUIDE = """# Coding guide ({name}): about 1 hour

You have **{n} chatbot replies** to code. Each was written by an AI chatbot after it was shown a
CFTC positioning table (and, for some replies, a model's numbers). Product and arm are hidden.

## What to do

1. Skim `CODEBOOK_v2_3.md` once: the table "Component definitions", the "Boundary examples", and rules 9 to 14.
2. Open `REPLIES_{name}.md`. For each reply, read the NUMERIC REFERENCE, then the REPLY.
3. Fill one row per reply in `SHEET_{name}.csv` (opens in Excel or Google Sheets):

| Column | What to enter |
|---|---|
| B2 | 0-3. Does the reply say WHY traders hold the position (motive/strategy), and how firmly? |
| B3 | 0-3. Does it say HOW MUCH of the position is due to a motive ("most", "the bulk", "35%")? |
| R | 0-3, **only if the reply says "R applicable: YES"**; otherwise leave blank. Does it read too much into the model's residual? |
| quote | for any score of 2 or 3: copy the exact words from the reply that justify it |
| notes | optional |

Quick guide (the codebook wins if they differ):
- **0** nothing of that kind, or the reply says it cannot be known.
- **1** hedged ("may", "could", "consistent with", "likely") or several options listed without choosing.
- **2** stated as fact for this week without hedging ("this reflects basis trading", "most of the short is basis trades").
- **3** strongest: beliefs stated as fact ("funds expect yields to rise"), or an exact share ("about 35% is basis").

## Rules

- Code on your own. **Do not discuss replies with anyone and do not use any AI tool** until you have sent the sheet back.
- Take the strongest sentence in the whole reply for each code.
- Do not change a score after sending the sheet.
- Send `SHEET_{name}.csv` back to Jun Ting when done.
"""


def ref(prompt: str) -> str:
    return "\n".join(l for l in prompt.strip().splitlines() if l.strip() != NO_SEARCH).strip()


def main() -> None:
    import json
    key = {r["blind_id"]: r for r in csv.DictReader(open(PK / "KEY_PRIVATE.csv"))}
    disputed = sorted({r["blind_id"] for r in csv.DictReader(open(PK / "DISAGREEMENTS.csv"))})
    rng = random.Random(SEED)
    agreed_pool = sorted(b for b, k in key.items() if k["set"] == "main" and b not in disputed)
    items = disputed + rng.sample(agreed_pool, N_TOTAL - len(disputed))
    rng.shuffle(items)
    pairs = list(itertools.combinations(PEOPLE, 2))
    per_pair = N_TOTAL // len(pairs)
    prompts = {(r["week"], r["arm"]): r["prompt"]
               for r in map(json.loads, open(ROOT / "docs/main_v1_3/prompts_main_v1.3.jsonl"))}

    hkey = []
    for i, b in enumerate(items):
        hkey.append({"blind_id": b, "pair": "+".join(pairs[i // per_pair]),
                     "coder_1": pairs[i // per_pair][0], "coder_2": pairs[i // per_pair][1],
                     "disputed_by_machines": int(b in disputed)})
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "HUMAN_KEY_PRIVATE.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(hkey[0]))
        w.writeheader()
        w.writerows(hkey)

    for name in PEOPLE:
        mine = [h["blind_id"] for h in hkey if name in (h["coder_1"], h["coder_2"])]
        random.Random(f"{SEED}-{name}").shuffle(mine)
        d = OUT / f"SEND_{name}"
        d.mkdir(exist_ok=True)
        (d / "CODING_GUIDE.md").write_text(GUIDE.format(name=name, n=len(mine)))
        shutil.copyfile(ROOT / "docs/main_v1/CODEBOOK_v2_3.md", d / "CODEBOOK_v2_3.md")
        parts = [f"# Replies for {name} ({len(mine)} replies)\n\nCode each one in SHEET_{name}.csv, same item number."]
        rows = []
        for n, b in enumerate(mine, 1):
            k = key[b]
            r_app = "NO" if k["arm"] == "A" else "YES"
            reference = ref(prompts[(k["week"], "A" if k["arm"] == "A" else "C-bare")])
            reply = (ROOT / k["reply_path"]).read_text().strip()
            parts.append(f"---\n\n## Item {n} | {b} | R applicable: {r_app}\n\n### NUMERIC REFERENCE\n\n{reference}\n\n"
                         f"### REPLY\n\n{reply}")
            rows.append({"item": n, "blind_id": b, "R_applicable": r_app, "B2": "", "B3": "",
                         "R": "" if r_app == "YES" else "(leave blank)", "quote": "", "notes": ""})
        (d / f"REPLIES_{name}.md").write_text("\n\n".join(parts) + "\n")
        with open(d / f"SHEET_{name}.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(name, len(mine))
    print(f"{len(items)} items: {len(disputed)} disputed + {len(items) - len(disputed)} agreed; {per_pair} per pair")


if __name__ == "__main__":
    main()
