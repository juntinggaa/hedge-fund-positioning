# v2 pilot: does the LLM keep position, adjustment and motive apart?

Run 2026-11-05. 6 cases × {C-bare, C-ann} (model v2.0 block), neutral question.

**Harness:** Codex CLI 0.165.0-alpha.1.2, `gpt-6-luna`, reasoning effort high,
read-only sandbox, fresh ephemeral session in an empty directory, run order
shuffled. Web search was used in 5 of 12 runs (see `key.csv`).

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

## Provisional results (coder 0)

| | C-bare (6) | C-ann (6) |
|---|---|---|
| B3 ≥ 2 (primary) | 0 | 0 |
| B2 ≥ 2 | 1 (P03 "points to a bearish positioning bias") | 0 |
| R ≥ 2 | 1 (P02 "the short is more bearish than the model expected") | 0 |
| U = 0 (range used correctly) | 3 | 5 |
| L = 0 (residual read as an *adjustment*) | 0 | 2 |
| F ≥ 2 (numerical misreading) | 1 | 1 |

## What the pilot shows

1. **Motive: the floor again.** B3 = 0 in all 12 neutral-question runs. Every run
   separated position from motive, mostly with named limits (M ≥ 2 in all 12). The
   neutral question alone cannot measure B3; this confirms the pressured
   elicitation factor.
2. **Large position vs model surprise: mostly kept apart.** Responses described
   the large *level* ("heavily net short") separately from the residual, and read
   in-range residuals as ordinary model error. With the annotation this happened
   in 5 of 6 runs; without it, 3 of 6. The two directional readings of the
   residual (R = 2, B2 = 2) were both in **C-bare**.
3. **Adjustment vs level: almost never articulated.** Only 2 of 12 described the
   residual as an unexpected *change*. Most said "less short than expected", a
   level framing (L = 1). **This is probably induced by our block**, which shows
   expected and actual *levels*. If the study wants to test the
   level/adjustment distinction, the block must show the change, for example
   "last week −39.83% → expected change … → actual change …". That would add last
   week's level, which arm A does not show. **Team decision.**
4. **Stimulus defect found and fixed.** "Larger in size than 4% of past
   residuals" was read as "96%" by 2 of 12 responses (P06, P12). P12 then reported
   an "apparent inconsistency" in the model summary. The wording now states both
   directions ("4% were smaller … 96% were larger"), with a test guarding it. This
   is an F code caused by our wording, not by the LLM's epistemics.
5. **Codable scales.**
   - **U** varies and looks usable.
   - **L** is almost always 1, so as written it has little variance. Revisit it
     after decision 3.
   - **R** and **B2** discriminated the two problematic runs.

## Before the main run

- Two human coders code `coding_sheet.csv` blind, then compute κ per code. Clear
  at ≥ 0.7 or amend to v2.1 and re-pilot on fresh responses (codebook §4).
- Decide the change-framing of the block (point 3) **before** freezing materials.
- Freeze model v2.0 materials with the revised percentile wording.
