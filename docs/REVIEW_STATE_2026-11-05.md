# Review state, 2026-11-05

Snapshot for reviewers: what is fixed, what is proposed, and what is open.
Nothing is committed. HEAD is `508ceb5`, and everything below is in the working
tree.

## Frozen (do not change without a dated amendment)

| item | file | status |
|---|---|---|
| v1 model, tables, stimuli, v1 annotation text | `reports/tables/stage1_*`, `docs/milestone2/arm_c_stimuli.csv`, `scripts/build_prompts.py` (ANNOTATION, hash-tested) | unchanged |
| v2 spec and Amendment 1 (pre-Friday nowcast claim withdrawn) | `docs/model_v2/SPEC_2026-11-05.md` | frozen |
| v2 predictions, tables, selection (M3 retained; M4 failed the gate) | `data/processed/model_v2/`, `reports/model_v2/` | unchanged (hash-checked) |
| v2.0 model card ("retrospective same-week conditional estimate") | `docs/model_v2/model_card_v2.json` | frozen |
| v3 spec, with Amendment 1 made before fitting | `docs/model_v3/SPEC_2026-11-05.md` | frozen |
| pilot v2 responses as recorded (original stimulus wording) | `docs/milestone2/pilot_v2/responses.jsonl` | unchanged |
| pinned raw data | `data/raw/*.parquet`, `data/raw/v3/*.parquet` + manifests | unchanged / new |
| retrieval lockdown for the controlled condition | `src/hfpos/llm/codex_harness.py`, `docs/milestone2/RETRIEVAL.md` | verified 3/3 probes |

## Proposed (not adopted)

| item | file | adopted when |
|---|---|---|
| codes L and U, draft b | `docs/milestone2/pilot_v2/CANDIDATE_CODES.md` | two human coders apply them and reach κ ≥ 0.7. No human agreement exists yet |
| coder-0 (Claude) codes, drafts a and b | `coder0_claude_PROVISIONAL*.csv` | never used for κ |
| v2 stimulus block (range; two-direction percentile wording) | `scripts/build_prompts.py --model-version v2` | team picks model and design |
| v2 annotation text | `annotation_v2()` | same |

## Superseded or withdrawn (kept for the record)

- `PILOT_V2_draft_a_SUPERSEDED.md`: the L code treated correct level-gap
  language as a misunderstanding, it attributed the percentile misreading to
  wording alone, and it said the neutral question "cannot measure" anything.
- "Report C vs D as the primary model-arm contrast" (RESULTS.md, CASES.md) is
  withdrawn. See `docs/milestone2/COMPARISONS.md`.

## Open team decisions

1. Research question and primary comparison (`docs/milestone2/COMPARISONS.md`).
2. Whether to add an information-matched A arm.
3. Whether to show the change explicitly in the C block. This is now a clarity
   choice, not a fix.
4. Whether pressured elicitation and retrieval-on are main-design factors.
5. Model for stimuli: v2.0 M3 (v3 recommends retaining it); v1 vs v2 block.
6. Human coding of `coding_sheet.csv`, then re-pilot under the retrieval lockdown.

The main LLM dataset is **not** regenerated until 1–5 are decided.
