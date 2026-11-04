# What each arm comparison identifies (2026-11-05)

**Status: the research question and the primary comparison are pending a
deliberate team decision.** The pilot is not a reason to promote any contrast.
Earlier text in `docs/model_v2/RESULTS.md` and `CASES.md` that recommended C vs D
as primary has been withdrawn (the edits are marked there).

Arms (from `scripts/build_prompts.py`): A = CFTC table; B = A + trader-category
explainer; C = A + model block (C-bare: no annotation; C-ann: with annotation);
D = A + model block with a **placebo** residual (same format and distribution,
shuffled across weeks, seed 20261104). The arms are **not cumulative**: C and D
start from A, not B.

| Contrast | Held fixed | Varies | Identifies | Does not identify |
|---|---|---|---|---|
| C-bare vs C-ann | table, model numbers, week | the annotation text | effect of explaining the model output (annotation effect) | anything about the model's information content |
| C vs D | table, block format, numeric precision, presence of a "surprise" number | whether the residual is the real one for that week | sensitivity of responses to genuine vs placebo model evidence | that numerical presentation *caused* overconfidence: similar C and D responses are also consistent with the model ignoring the block, or with both blocks being read correctly as weak evidence |
| A vs C (and A vs D) | the table, week | presence of a model block, which also adds information (expected level, residual, range, percentile) | the effect of evidence presentation **including** an information-set difference | a pure presentation (format) effect |
| B vs C | week | explainer vs model block (both differ from A) | which addition changes responses more | either effect alone, since B lacks the block and C lacks the explainer |
| A vs B | the table, week | explainer text | effect of a category explainer | – |
| Neutral vs pressured question | stimulus | the question | a separate elicitation condition, analysed as its own factor | the neutral-question floor is not zero measurable error (pilot: F misreads and imprecise range use occurred) |

Notes:
- A difference between C and D tells us responses track the content of the
  evidence. No difference is ambiguous (see the table).
- A vs C confounds format with information. Separating them would need an arm
  that gives the same information without model framing (e.g. last week's level
  in the A table). That is a design choice for the team.
- Retrieval (web search) changes the evidence set; it is a separate pre-declared
  factor, and the controlled condition runs with it disabled
  (`docs/milestone2/RETRIEVAL.md`).

## Team decisions
1. Research question: motive overreach (B3), evidence calibration (C vs D), or
   presentation (A vs C)?
2. Primary comparison and which contrasts are secondary.
3. Whether to add an information-matched A arm.
4. Whether pressured elicitation is in the main design.
