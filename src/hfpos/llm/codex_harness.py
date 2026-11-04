"""Reproducible Codex CLI harness for the LLM experiment, with retrieval DISABLED.

Verified empirically on 2026-11-05 against codex-cli 0.165.0-alpha.1.2 (see
docs/milestone2/RETRIEVAL.md for the probe logs). Findings that shaped this:

- `-c web_search="disabled"` alone does NOT stop retrieval: the model then searched
  via the `codex_apps` MCP server (`search_service.web_run`), whose log items do not
  contain the string "web_search".
- `--disable apps` removes that route; the bundled computer-use plugin still exposes a
  `cua_repl` MCP server that attempted to open the user's Chrome, so all plugins are
  disabled with `--disable plugins` (per-plugin overrides were not effective).
- Every run is audited from its JSON event log: ANY completed item that is not an
  agent message or reasoning counts as a tool call. A run with tool calls is flagged
  `retrieval_clean = False` and must be excluded or re-run, not silently kept.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"

#: Overrides passed as separate argv items (no shell quoting involved).
LOCKDOWN = [
    "-c", 'web_search="disabled"',
    "--disable", "apps", "--disable", "browser_use", "--disable", "browser_use_external",
    "--disable", "in_app_browser", "--disable", "computer_use", "--disable", "code_mode_host",
    # All plugins off. Per-plugin `-c plugins."...".enabled=false` overrides did NOT
    # remove the bundled computer-use server (`cua_repl`), and overriding
    # mcp_servers.cua_repl directly fails ("invalid transport"); the feature flag works.
    "--disable", "plugins",
]

MESSAGE_TYPES = {"agent_message", "reasoning"}


def tool_items(events: list[dict]) -> list[str]:
    """Completed tool items (search, MCP call, command, ...). Empty means no tool ran."""
    out = []
    for e in events:
        it = e.get("item") or {}
        if (e.get("type") == "item.completed"
                and it.get("type") not in MESSAGE_TYPES | {"error"}):
            out.append(f"{it.get('type')}:{it.get('server') or ''}:{it.get('tool') or ''}")
    return out


def blocked_attempts(events: list[dict]) -> list[str]:
    """`error` items, e.g. "code-mode host is disabled": the model tried a disabled
    tool and was refused (fail-closed). Recorded, not counted as retrieval."""
    return [str((e.get("item") or {}).get("message", ""))[:120] for e in events
            if e.get("type") == "item.completed" and (e.get("item") or {}).get("type") == "error"]


def run(prompt: str, model: str = "gpt-6-luna", effort: str = "high",
        retrieval: bool = False, timeout: int = 900) -> dict:
    """One fresh, ephemeral session in an empty directory. Returns text + audit."""
    with tempfile.TemporaryDirectory() as empty:
        last = Path(empty) / "last.txt"
        argv = [CODEX, "exec", "-m", model, "-c", f"model_reasoning_effort={effort}",
                "--sandbox", "read-only", "--skip-git-repo-check", "--ephemeral", "--json",
                "-C", empty, "-o", str(last)]
        if not retrieval:
            argv += LOCKDOWN
        started = datetime.now(timezone.utc).isoformat(timespec="seconds")
        proc = subprocess.run(argv + [prompt], capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=timeout)
        events = [json.loads(l) for l in proc.stdout.splitlines() if l.startswith("{")]
        text = last.read_text() if last.exists() else ""
    tools = tool_items(events)
    usage = next((e.get("usage") for e in reversed(events) if e.get("usage")), None)
    return {"model": model, "effort": effort, "retrieval_allowed": retrieval,
            "argv_overrides": [] if retrieval else LOCKDOWN, "started_utc": started,
            "returncode": proc.returncode, "tool_items": tools,
            "blocked_attempts": blocked_attempts(events),
            "retrieval_clean": (not tools and proc.returncode == 0 and bool(text))
                               if not retrieval else None,
            "stderr_tail": proc.stderr[-600:],
            "usage": usage, "response": text, "events": events}
