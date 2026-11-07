"""Check and merge manually collected main-v1.3 replies.

    python scripts/ingest_main_v1_3.py docs/main_v1_3/responses

Expects, per product code (GPT, GEM, CLA):
    <responses>/<CODE>/runsheet_<CODE>.csv   filled runsheet (downloaded from the shared sheet)
    <responses>/<CODE>/<assignment_id>.md    reply text pasted via the app's Copy button
    <responses>/<CODE>/<assignment_id>.png   screenshot (model label + temporary chat visible)

Writes <responses>/responses_v1.3.jsonl and prints every problem found. It never
edits reply files. Rows with status other than completed/refusal are kept and flagged.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "docs/main_v1_3"
STATUSES = {"completed", "refusal", "error", "fallback_model", "cap_hit", "incomplete"}
REQUIRED = ["collector_name", "account_label", "started_at_sgt", "finished_at_sgt",
            "model_label_shown", "thinking_setting_shown", "temporary_chat",
            "search_observed", "status", "attempt_number"]


def main(resp_dir: str, kit: Path = KIT) -> int:
    base = Path(resp_dir)
    key = {r["assignment_id"]: r for r in csv.DictReader(open(kit / "assignment_key_PRIVATE.csv"))}
    problems, out = [], []
    for code in ("GPT", "GEM", "CLA"):
        sheet = base / code / f"runsheet_{code}.csv"
        if not sheet.exists() and (base / code / f"runsheet_ADV_{code}.csv").exists():
            sheet = base / code / f"runsheet_ADV_{code}.csv"
        if not sheet.exists():
            problems.append(f"{code}: missing {sheet}")
            continue
        rows = list(csv.DictReader(open(sheet, encoding="utf-8-sig")))
        seen = {}
        for r in rows:
            aid = r["assignment_id"].strip()
            if aid not in key or key[aid]["product_code"] != code:
                problems.append(f"{aid}: not an assignment for {code}")
                continue
            seen.setdefault(aid, []).append(r)
        for aid, k in key.items():
            if k["product_code"] != code:
                continue
            attempts = seen.get(aid, [])
            if not attempts:
                problems.append(f"{aid}: no runsheet row")
                continue
            for r in attempts:
                missing = [c for c in REQUIRED if not r.get(c, "").strip()]
                status = r.get("status", "").strip()
                if missing:
                    problems.append(f"{aid} attempt {r.get('attempt_number')}: empty {missing}")
                if status and status not in STATUSES:
                    problems.append(f"{aid}: unknown status '{status}'")
                text, text_sha = None, None
                reply = base / code / (r.get("reply_file") or f"{aid}.md").strip()
                if status in {"completed", "refusal", "incomplete"}:
                    if not reply.exists() or not reply.read_text(encoding="utf-8").strip():
                        problems.append(f"{aid}: reply file missing or empty ({reply.name})")
                    else:
                        text = reply.read_text(encoding="utf-8")
                        text_sha = hashlib.sha256(text.encode()).hexdigest()
                shot = base / code / (r.get("screenshot_file") or f"{aid}.png").strip()
                if not shot.exists():
                    problems.append(f"{aid}: screenshot missing ({shot.name})")
                out.append({**{c: (r.get(c) or "").strip() for c in r},
                            "product_code": code, "prompt_sha256": k["prompt_sha256"],
                            "response_text": text, "response_sha256": text_sha})
            done = [r for r in attempts if r.get("status", "").strip() in {"completed", "refusal"}]
            if len(done) > 1:
                problems.append(f"{aid}: {len(done)} completed attempts; only the first counts")
    (base / ("responses_v1.3.jsonl" if kit == KIT else "responses.jsonl")).write_text("".join(json.dumps(r) + "\n" for r in out))
    n_done = sum(r["status"] in {"completed", "refusal"} for r in out)
    print(f"{len(out)} attempt rows, {n_done} completed/refusal, of {len(key)} assignments")
    print(f"{len(problems)} problems")
    for p in problems:
        print(" -", p)
    return 1 if problems else 0


if __name__ == "__main__":
    # Optional 2nd argument: another kit folder with its own assignment key,
    # e.g. docs/explore_advice_v1 for the advice-framing add-on.
    kit_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else KIT
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(kit_dir / "responses"), kit_dir))
