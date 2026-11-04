# Retrieval control for the LLM experiment

**Status:** a retrieval-disabled configuration is prepared and verified. It is
**not yet used**: no experiment has been re-run with it.

## Probes (2026-11-05, codex-cli 0.165.0-alpha.1.2, gpt-6-luna)

The probe prompt explicitly asked for a web search, a browser lookup, or a shell
fetch. Summaries are in `retrieval_probes/probes_2026-11-05.json`.

| configuration | what happened |
|---|---|
| default | `web_search` items, live search |
| `-c web_search="disabled"` | **still searched**, through the `codex_apps` MCP server (`search_service.web_run`). The log items do not contain "web_search" |
| `--disable web_search_request` | still searched |
| `--disable apps` | still searched (`web_search`) |
| web search disabled, apps/browser/computer-use features off | the bundled computer-use plugin's `cua_repl` MCP server was called |
| per-plugin `-c plugins."…".enabled=false` | not effective: `cua_repl` still called, and in one probe it **attempted to open Chrome on this Mac** (access was denied) |
| `-c mcp_servers.cua_repl.enabled=false` | config error ("invalid transport"); the run produced nothing |
| **final lockdown** (below) | **0 tool items in 3 of 3 adversarial probes.** Each run had one `error` item ("code-mode host is disabled"), i.e. a refused attempt. All three answers said lookup was unavailable. |

**Final lockdown** (`hfpos.llm.codex_harness.LOCKDOWN`, passed as an argv list):

```
-c web_search="disabled"
--disable apps --disable browser_use --disable browser_use_external
--disable in_app_browser --disable computer_use --disable code_mode_host
--disable plugins
```

Also: `--sandbox read-only` (the model reported network access was restricted),
`--ephemeral`, and a fresh empty working directory per run. The global
`~/.codex/AGENTS.md` is empty, so it injects no instructions.

**Per-run audit, mandatory:**
- Each run's JSON event log is scanned for *any* completed item that is not a
  message, reasoning or refused-attempt error.
- `retrieval_clean = False` if any such item exists, if the exit code is non-zero,
  or if the response is empty.
- Unclean runs are excluded or re-run, and the count is reported.
- This cannot prove the absence of retrieval inside the provider's own model
  serving. It shows that no client-side tool ran.

## Pilot limitation (v2 pilot, already collected, not re-run)

The v2 pilot ran **with retrieval available**. Its counter (`"web_search"` in the
item text) found search in **5 of 12** runs. That counter **would miss
MCP-routed searches** like the one above. Input-token counts are consistent with
exactly those 5 runs: 37–97k tokens for those, 15.8–16.8k for the rest. That is
corroborating, not proof. Pilot results therefore mix runs with and without
outside material. Responses with search cited CFTC and Fed sources, which bears
on codes S and K.

## Design implication

- **Retrieval-off is the controlled condition.** It measures what the model asserts
  from the supplied evidence.
- **Retrieval-on is a different condition** (agent product, outside material). If
  the team wants it, run it as a separate, pre-declared factor, not mixed in.
