# Where does the model re-rank weeks? (fixed rule, every case reported)

`python scripts/model_v2_cases.py`: tables in `reports/model_v2/cases_rerank.csv` and
`cases_contributions_pp.csv`.

**Rule (fixed before looking):** K = 72, the top decile of 720 evaluation weeks.
- *Entrants* are in the top-K by |M3 residual| but not by |raw change|.
- *Leavers* are the reverse.

Each M3 prediction is decomposed into feature-group contributions (coefficient ×
standardised value) using the same fold model that produced it. Robustness asks
whether the week's status holds under five alternatives: M3-rolling, M4, M5, M3
without `d_log_oi`, and the alternative target.

## What the ML step changes

- **Overlap 64/72 (89%).** Only 8 weeks enter and 8 leave.
- **Re-ranking happens at the margin.**
  - Entrants move from raw ranks 84–189 to residual ranks 33–72.
  - Leavers move from raw ranks 33–72 to 74–137.
  - Mean |prediction| is 0.7–0.8 pp, against raw moves of about 3–4 pp.
- **Sign pattern.**
  - **All 8 entrants** had a prediction of the *opposite* sign to the actual
    move. The model expected funds to go the other way, so the surprise exceeds
    the raw change.
  - **All 8 leavers** had a same-sign prediction. The model anticipated part of
    the move.
- **No single feature group drives it.** The dominant group accounts for 24–46%
  of the absolute contributions. "Own position" (lagged level and change) and
  "rates and curve" dominate most often.
- **Mostly robust.**
  - 11 of 16 weeks keep their status in at least 4 of the 5 alternatives.
  - Fragile: **2021-01-19** (0/5), 2014-10-28 (1/5), 2018-10-09 (2/5).
  - **Three re-ranked weeks are in the main LLM sample:** 2013-09-03 (3/5),
    2014-09-30 (3/5) and 2021-01-19 (0/5). Whether 2021-01-19 looks "surprising"
    depends on the specification.

## Do the adjustments make economic sense?

These readings are partly interpretive; they are offered as plausibility checks
and do not establish anything.

- **2022-06-14** (entrant, residual +4.37 pp). This is the week of the
  10 June CPI surprise and the 15 June 75 bp hike. The model expected funds to
  add shorts (−1.13 pp), driven by rates/curve (−0.78) and the futures-yield
  residual (−0.33). They covered +3.24 pp instead. The model's yields-up →
  shorts-up association failed in a policy shock. That is plausibly a genuine
  surprise, robust in 4 of 5 specifications.
- **2026-09-01** (leaver). Of the −2.02 pp the model anticipated, −0.74 pp came
  from the **open-interest change**, plausibly September-roll contract expiry
  (not verified against the roll calendar), and −0.83 pp from rates. Without
  `d_log_oi` the week returns to the top decile. **Part of the model's
  "anticipation" here is denominator mechanics**, not a positioning decision.
- **2014 cluster.** 5 of 8 leavers fall in 2013–14, early in the evaluation, when
  the model had the least training data. That is weak evidence the early-sample
  re-ranking is noisier.

## Implication for the project

The residual mostly re-labels the raw change. For 89% of the extreme weeks, "the
model was surprised" and "positioning moved a lot" pick out the same weeks. The
model's distinctive information is confined to a handful of marginal weeks, some
of them specification-dependent. **So the main thing Arm C can test is the *form*
of a model output, not new information.** Arm D (the placebo) holds that form
fixed and varies whether the residual is genuine.

*Withdrawn 2026-11-05:* an earlier sentence here recommended reporting C vs D as
the primary model-arm contrast. That was premature. What each contrast identifies
is set out in `docs/milestone2/COMPARISONS.md`; the primary comparison is pending
a team decision.
