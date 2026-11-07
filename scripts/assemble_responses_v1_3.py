"""Assemble the main-v1.3 analysis dataset in the layout ingest_main_v1_3.py checks.

    python scripts/assemble_responses_v1_3.py

COPIES only (never moves or edits a source file). Sources:
    GPT, CLA  docs/main_v1_3/main prompt outputs/<ID>.txt          (high effort)
    GEM       docs/main_v1_3/main prompt outputs/responses/<ID>.md  (teammates, Argon low)
Runsheet fields are taken from the collection logs (collection_*/**/attempts.jsonl)
where a completed record exists; anything not logged is left BLANK for the collector
to fill. Nothing is guessed. The 16 high-effort Gemini replies go to
docs/main_v1_3/effort_check_GEM_high/ (outside responses/, so not in the main data).

Output: docs/main_v1_3/responses/<CODE>/{<ID>.md, <ID>.png, runsheet_<CODE>.csv},
        docs/main_v1_3/responses/PROVENANCE.csv, docs/main_v1_3/effort_check_GEM_high/.
"""

from __future__ import annotations

import csv
import glob
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "docs/main_v1_3"
SRC = KIT / "main prompt outputs"
OUT = KIT / "responses"
EFF = KIT / "effort_check_GEM_high"
DONE = {"completed", "terminal_response_saved"}
COLS = ["assignment_id", "collection_order", "prompt_file", "collector_name", "account_label",
        "started_at_sgt", "finished_at_sgt", "model_label_shown", "thinking_setting_shown",
        "temporary_chat", "search_observed", "status", "attempt_number", "reply_file",
        "screenshot_file", "notes"]
LOGGED = COLS[3:13]
# Effort provenance for the high-effort Gemini replies, from collection_batches/gemini_descending.
EFFORT_FLAG = {"GEM-045": "cap hit at about the same time; High was selected before sending but actual effort is unknown"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_logs() -> list[dict]:
    dec, recs = json.JSONDecoder(), []
    for f in sorted(glob.glob(str(KIT / "collection_*/**/attempts.jsonl"), recursive=True)):
        for line in open(f):
            s, i = line.strip(), 0
            while i < len(s):  # one line holds two records joined by a literal "\n"
                while i < len(s) and (s[i].isspace() or s.startswith("\\n", i)):
                    i += 2 if s.startswith("\\n", i) else 1
                if i >= len(s):
                    break
                r, i = dec.raw_decode(s, i)
                if r.get("assignment_id"):
                    recs.append(r)
    return recs


def logged_fields(recs: list[dict], aid: str) -> tuple[dict, str | None]:
    """Merge every record of the last completed attempt; later non-empty values win."""
    mine = [r for r in recs if r["assignment_id"] == aid]
    done = [r for r in mine if r.get("status") in DONE]
    if not done:
        return {}, None
    att = done[-1].get("attempt_number")
    merged = {}
    for r in mine:
        if r.get("attempt_number") in (att, None):
            merged.update({k: v for k, v in r.items() if v not in (None, "")})
    merged["status"] = "completed"
    if att is not None:
        merged["attempt_number"] = att
    return {k: str(merged.get(k, "")) for k in LOGGED}, merged.get("screenshot_file")


def find_shot(aid: str, logged: str | None) -> Path | None:
    cands = [SRC / "screenshots" / f"{aid}.png"]
    if logged:
        p = Path(logged)
        cands += [p] if p.is_absolute() else [SRC / "screenshots" / p.name]
    cands += sorted((SRC / "screenshots").glob(f"{aid}_a*.png"))
    return next((c for c in cands if c.exists()), None)


def main() -> None:
    key = list(csv.DictReader(open(KIT / "assignment_key_PRIVATE.csv")))
    recs = load_logs()
    prov = []
    for code in ("GPT", "CLA", "GEM"):
        d = OUT / code
        d.mkdir(parents=True, exist_ok=True)
        rows = []
        for k in (r for r in key if r["product_code"] == code):
            aid = k["assignment_id"]
            src = SRC / "responses" / f"{aid}.md" if code == "GEM" else SRC / f"{aid}.txt"
            row = dict.fromkeys(COLS, "")
            row.update(assignment_id=aid, collection_order=k["collection_order"], prompt_file=k["prompt_file"])
            if code == "GEM":
                fields, shot_log = {}, None  # teammates' run: no log in this repo
                row["notes"] = "teammate collection, Argon (low effort per coordinator): collector to confirm all fields"
            else:
                fields, shot_log = logged_fields(recs, aid)
                if not fields:
                    row["notes"] = "no collection log: collector to fill"
            row.update({c: v for c, v in fields.items() if v})
            if src.exists():
                shutil.copyfile(src, d / f"{aid}.md")
                row["reply_file"] = f"{aid}.md"
                prov.append([code, aid, "reply", str(src.relative_to(ROOT)), sha(src)])
            shot = None if code == "GEM" else find_shot(aid, shot_log)
            if shot:
                shutil.copyfile(shot, d / f"{aid}.png")
                row["screenshot_file"] = f"{aid}.png"
                prov.append([code, aid, "screenshot", str(shot), sha(shot)])
            rows.append(row)
        with open(d / f"runsheet_{code}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(rows)

    EFF.mkdir(exist_ok=True)
    eff_rows = []
    for src in sorted(SRC.glob("GEM-*.txt")):
        aid = src.stem
        shutil.copyfile(src, EFF / f"{aid}.md")
        prov.append(["GEM-high", aid, "reply", str(src.relative_to(ROOT)), sha(src)])
        k = next(r for r in key if r["assignment_id"] == aid)
        eff_rows.append({"assignment_id": aid, "week": k["week"], "arm": k["arm"],
                         "high_effort_file": f"{aid}.md", "paired_low_effort_file": f"../responses/GEM/{aid}.md",
                         "effort_provenance": EFFORT_FLAG.get(aid, "High logged before send")})
    with open(EFF / "PAIRS_PRIVATE.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(eff_rows[0]))
        w.writeheader()
        w.writerows(eff_rows)
    with open(OUT / "PROVENANCE.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["set", "assignment_id", "kind", "source", "sha256"])
        w.writerows(prov)
    print(f"copied {sum(p[2] == 'reply' for p in prov)} replies, {sum(p[2] == 'screenshot' for p in prov)} screenshots; "
          f"{len(eff_rows)} high-effort Gemini pairs")


if __name__ == "__main__":
    main()
