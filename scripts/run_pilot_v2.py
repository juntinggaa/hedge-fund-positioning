"""Run the v2 pilot prompts through Codex CLI with a fixed, recorded harness.

    python scripts/run_pilot_v2.py

Same harness as docs/milestone2/pilot_codex.md: codex exec, gpt-6-luna,
model_reasoning_effort=high, read-only sandbox, fresh ephemeral session started in an
EMPTY directory (no project context). Web search is whatever the CLI default allows
and is recorded from the event log. Output: docs/milestone2/pilot_v2/responses.jsonl.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "docs/milestone2/pilot_v2"
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
MODEL, EFFORT = "gpt-6-luna", "high"


def run(job: dict) -> dict:
    with tempfile.TemporaryDirectory() as empty:
        last = Path(empty) / "last.txt"
        started = datetime.now(timezone.utc).isoformat(timespec="seconds")
        proc = subprocess.run(
            [CODEX, "exec", "-m", MODEL, "-c", f"model_reasoning_effort={EFFORT}",
             "--sandbox", "read-only", "--skip-git-repo-check", "--ephemeral", "--json",
             "-C", empty, "-o", str(last), job["prompt"]],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=900)
        events = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
        text = last.read_text() if last.exists() else ""
    usage = next((e.get("usage") for e in reversed(events) if e.get("usage")), None)
    searches = sum(1 for e in events if "web_search" in json.dumps(e.get("item", {})))
    return {**{k: job[k] for k in ("run_id", "week", "arm", "case_type")},
            "model": MODEL, "effort": EFFORT, "started_utc": started,
            "returncode": proc.returncode, "web_search_events": searches,
            "usage": usage, "response": text, "stderr_tail": proc.stderr[-400:]}


def main():
    jobs = [json.loads(l) for l in (DIR / "prompts.jsonl").read_text().splitlines()]
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(run, jobs))
    with open(DIR / "responses.jsonl", "w") as fh:
        for r in results:
            fh.write(json.dumps(r) + "\n")
    for r in results:
        print(r["run_id"], r["arm"], r["week"], r["returncode"], len(r["response"]), r["web_search_events"])


if __name__ == "__main__":
    main()
