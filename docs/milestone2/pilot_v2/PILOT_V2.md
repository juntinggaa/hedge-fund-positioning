# v2 pilot: does the LLM keep position, adjustment and motive apart?

Run 2026-11-05. 6 cases × {C-bare, C-ann} (model v2.0 block), neutral question.

**Harness:** Codex CLI 0.165.0-alpha.1.2, `gpt-6-luna`, reasoning effort high,
read-only sandbox, fresh ephemeral session in an empty directory, run order
shuffled. Web search was **available**, and recorded as used in 5 of 12 runs
(`key.csv`; a lower bound, see below).

```
python scripts/pilot_v2_select.py
python scripts/run_pilot_v2.py
```

**Status of the codes:** every code below is from **coder 0 (Claude), provisional,
excluded from κ**. The blind sheet for two human coders is `coding_sheet.csv`
(run_id and text only; arm and week are in `key.csv`). Candidate codes L and U
are defined in `CANDIDATE_CODES.md`.

## Case selection (fixed rule, main-sample weeks excluded)

| type | rule | qualified | picked |
|---|---|---|---|
| a. large move, model not surprised | \|raw\| ≥ p90, same-sign prediction, residual inside range | 12 | 2026-09-01, 2023-07-11 |
| b. modest move, model surprised | \|raw\| ≤ median and residual percentile ≥ 85 | **0** | none |
| c. ordinary | residual percentile ≤ 25, \|raw\| in p25–p75 | 46 | 2026-06-30, 2025-06-17 |
| d. large residual | outside range, percentile ≥ 97 | 18 | 2026-08-25, 2025-02-18 |

- **Type b is empty.** Prediction SD is about 0.5 pp, so the model never makes a
  modest raw move look surprising. This matches `docs/model_v2/CASES.md`: the
  residual mostly re-labels the raw change.
- **Type a's rule is weaker than its label.** "Inside the range" does not mean
  "largely anticipated". 2023-07-11 had a prediction of +0.16 pp against a
  +3.64 pp move, so these weeks are really *large moves the model doesn't flag*.

## Provisional results (coder 0, draft-b definitions)

Revised 2026-11-05. The first write-up (kept unchanged as
`PILOT_V2_draft_a_SUPERSEDED.md`, codes in `coder0_claude_PROVISIONAL.csv`) used L
and U definitions that were too strict. The current codes are in
`coder0_claude_PROVISIONAL_draftb.csv`. **Nothing here is human-validated; there is
no κ.**

| | C-bare (6) | C-ann (6) |
|---|---|---|
| B3 ≥ 2 (primary) | 0 | 0 |
| B2 ≥ 2 | 1 (P03 "points to a bearish positioning bias") | 0 |
| R ≥ 2 | 1 (P02 "the short is more bearish than the model expected") | 0 |
| L = 2 (residual as unexplained fraction of the position, or as motive) | 0 | 0 |
| L = 1 (ambiguous) | 1 (P02) | 0 |
| U ≥ 2 (range contradicted or misused) | 0 | 0 |
| U = 1 (imprecise) | 0 | 1 (P09) |
| Range or percentile used at all | 5 | 6 |
| F = 2 (supplied number misread) | 1 (P06) | 1 (P12) |
| **Runs with web search** | **4** | **1** |

**Retrieval confound.** Web search was available and used in 5 of 12 runs, 4 of
them C-bare. Any C-bare vs C-ann difference here is confounded with retrieval. The
search counter in this harness also missed MCP-routed searches, so 5 is a lower
bound (`docs/milestone2/RETRIEVAL.md`). The main run uses the verified lockdown
in `src/hfpos/llm/codex_harness.py` and treats retrieval-on as a separate,
pre-declared condition.

## Point accuracy and interval coverage (reported separately)

The approximate 90% range is based on the model's past errors. Whether the actual
value falls inside it says nothing about whether the point estimate was close.
(`cases_point_vs_interval.csv`)

| type | week | actual change (pp OI) | predicted change | abs point error | inside range |
|---|---|---|---|---|---|
| a | 2026-09-01 | −4.71 | −2.02 | 2.69 | yes |
| a | 2023-07-11 | +3.64 | +0.16 | 3.47 | yes |
| c | 2026-06-30 | −0.76 | −0.66 | 0.10 | yes |
| c | 2025-06-17 | −0.73 | −0.14 | 0.58 | yes |
| d | 2026-08-25 | +5.45 | +0.31 | 5.14 | no |
| d | 2025-02-18 | +4.91 | +0.08 | 4.83 | no |

2023-07-11 is the clearest case: the actual change fell inside the range while
the point prediction captured about 5% of the move. "Inside the range" means the
miss is ordinary for this model; it does not mean the model anticipated the move.
Type a is therefore better named *large moves the model does not flag*.

## What the pilot shows (provisional)

1. **Motive.** B3 = 0 in all 12 neutral-question runs, and every run named limits
   (M ≥ 2). The neutral question still produced measurable errors (two numerical
   misreadings, one directional reading of the residual, one imprecise use of the
   percentile), so the floor is on **motive claims**, not on error in general. The
   pressured question is a separate elicitation condition with its own
   comparison. It is not a fix for the neutral one.
2. **Level gap vs adjustment.** Under the corrected definition (L), describing
   the residual as a level gap ("3.47 pp less short than expected") is correct,
   because expected level = last week + predicted change. Eleven of 12 responses
   were correct, one was ambiguous, and none treated the residual as a fraction of
   the position. Draft a's claim that the block "induces" a level misunderstanding
   is withdrawn. Whether to *also* show the change explicitly is now a clarity
   choice, not a correction (team decision).
3. **Large position vs model surprise.** Responses kept the large *level* ("heavily
   net short") apart from the residual. The two directional readings of the
   residual (R = 2, B2 = 2) were both C-bare. With n = 6 per arm and the
   retrieval confound, this is a lead for the coders to check, not an effect.
4. **Percentile misreading.** The original stimulus said the residual was "larger
   in size than 4% of past residuals". P06 and P12 restated this as larger than
   96%. Those responses are kept as recorded and coded F = 2. The wording was
   ambiguous, but this does not establish that the wording alone caused the
   misreading: the sentence can be parsed correctly, and other runs did. The new
   wording states both directions ("4% were smaller … 96% were larger") and may
   reduce this error. It has not been tested on fresh responses.
5. **Scales.** U has limited variance once non-use is not an error. L under draft
   b has almost none at the error end. Both stay **proposed** until two human
   coders apply them.

## Before the main run

- Two human coders code `coding_sheet.csv` blind, then compute κ per code. Clear
  at ≥ 0.7, or amend and re-pilot on fresh responses (codebook §4). L and U stay
  proposed until then.
- Re-run the pilot cases under the retrieval lockdown before drawing any arm
  contrast.
- Team decisions: research question and primary comparison
  (`docs/milestone2/COMPARISONS.md`); whether to show the change explicitly.
- Freeze model materials only after the model and design are selected.
