"""Check and merge one coder's raw JSON batches into CODES.csv.

    python scripts/merge_coder_v1_3.py docs/coding_main_v1_3/coder_codex_sol

Checks each batch against the packet: every blind_id present once, in order; codes in
0-3 or null; R null exactly where R is not applicable; any score > 0 has a quote found
verbatim in that reply (whitespace/markdown-insensitive); any score >= 2 has a reason.
Raw files are never edited. Problems are listed, not fixed.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PK = ROOT / "docs/coding_main_v1_3"
FIELDS = ["blind_id", "scoring_status", "B2", "B2_quote", "B2_target", "B2_reason", "B3", "B3_quote",
          "B3_target", "B3_reason", "R", "R_quote", "R_reason", "notes"]


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("\\", "")
    s = re.sub(r"[*_`#>]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def parse(text: str) -> list:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text[text.index("["): text.rindex("]") + 1])


def main(coder_dir: str) -> int:
    cdir = Path(coder_dir)
    key = list(csv.DictReader(open(PK / "KEY_PRIVATE.csv")))
    by_batch = {}
    for k in key:
        by_batch.setdefault(int(k["batch"]), []).append(k)
    problems, out = [], []
    for b, ks in sorted(by_batch.items()):
        raw = cdir / f"RAW_{b:02d}.json"
        if not raw.exists():
            problems.append(f"batch {b}: missing {raw.name}")
            continue
        try:
            arr = parse(raw.read_text())
        except Exception as e:
            problems.append(f"batch {b}: not parseable JSON ({e})")
            continue
        got = [o.get("blind_id") for o in arr]
        want = [k["blind_id"] for k in ks]
        if got != want:
            problems.append(f"batch {b}: blind_ids differ from packet order ({len(got)} vs {len(want)})")
        objs = {o.get("blind_id"): o for o in arr}
        for k in ks:
            o = objs.get(k["blind_id"])
            if o is None:
                problems.append(f"{k['blind_id']}: not coded")
                continue
            reply = norm((ROOT / k["reply_path"]).read_text())
            for c in ("B2", "B3", "R"):
                v = o.get(c)
                if v is not None and v not in (0, 1, 2, 3):
                    problems.append(f"{k['blind_id']} {c}: bad value {v!r}")
                    continue
                if c == "R" and k["r_applicable"] == "NO" and v is not None:
                    problems.append(f"{k['blind_id']} R: should be null (arm A)")
                if c == "R" and k["r_applicable"] == "YES" and v is None and o.get("scoring_status") == "substantive":
                    problems.append(f"{k['blind_id']} R: null but applicable")
                if isinstance(v, int) and v > 0:
                    q = o.get(f"{c}_quote") or ""
                    if not q.strip():
                        problems.append(f"{k['blind_id']} {c}={v}: no quote")
                    elif norm(q) not in reply:
                        problems.append(f"{k['blind_id']} {c}={v}: quote not verbatim: {q[:70]!r}")
                    if v >= 2 and not (o.get(f"{c}_reason") or "").strip():
                        problems.append(f"{k['blind_id']} {c}={v}: no reason")
            out.append({f: ("" if o.get(f) is None else o.get(f)) for f in FIELDS})
    with open(cdir / "CODES.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} of {len(key)} coded; {len(problems)} problems")
    for p in problems:
        print(" -", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
