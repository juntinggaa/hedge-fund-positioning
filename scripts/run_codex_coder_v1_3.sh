#!/usr/bin/env bash
# Code masked packets with Codex (gpt-6.1-sol, high effort), one fresh ephemeral session per packet.
#   scripts/run_codex_coder_v1_3.sh 01 02 ...      (no args = all packets)
# Runs in an empty scratch directory, read-only, plugins off, so the coder cannot see the repo
# (and therefore not KEY_PRIVATE.csv). Output: docs/coding_main_v1_3/coder_codex_sol/RAW_<nn>.json
# plus the event log; the event log is checked for any command execution.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CODEX=/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex
PK="$ROOT/docs/coding_main_v1_3/packets"
OUT="$ROOT/docs/coding_main_v1_3/coder_codex_sol"
mkdir -p "$OUT"
EMPTY="$(mktemp -d)"
trap 'rm -rf "$EMPTY"' EXIT
batches=("$@"); [[ ${#batches[@]} -eq 0 ]] && batches=($(ls "$PK" | sed -E 's/PACKET_([0-9]+)\.md/\1/'))
PRE="Everything you need is in this message. Do not run any commands, do not read or search any files, do not browse. Apply the codebook and return only the JSON array."
for b in "${batches[@]}"; do
  ( { echo "$PRE"; echo; cat "$PK/PACKET_$b.md"; } | "$CODEX" exec -m gpt-6.1-sol -c model_reasoning_effort='"high"' \
      -s read-only --disable plugins --ephemeral --skip-git-repo-check -C "$EMPTY" --json \
      -o "$OUT/RAW_$b.json" - >"$OUT/events_$b.jsonl" 2>"$OUT/stderr_$b.txt"
    echo "PACKET_$b exit=$? commands=$(grep -c '"command_execution"' "$OUT/events_$b.jsonl")" ) &
done
wait
