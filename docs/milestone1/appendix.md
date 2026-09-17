# Milestone 1 — Evidence Appendix

## A. Planned investigation

```
 CFTC TFF, 1,057 weeks (verified, hash-pinned) -> 40 stratified weeks, >=8 weeks apart
      |
   ARM A  bare prompt          ARM C  + precomputed decomposition
   ARM B  + qualitative context ARM D  agent must elect to call the tool
      |                               ( expected positioning from market
      |                                 state, walk-forward -> residual )
      v
 paired: every week seen by every arm
      v
 broad tier (40 wks): unsupported directional attribution y/n
 deep  tier ( 4 wks): full rubric + tool fidelity
      v
 McNemar on discordant pairs:  A->B facts fix framing? (H2)
                               B->C structure fix it?  (H3)
                               C->D agency add value?  (H4)
```

**Stratified sample, drawn 2026-09-18** (seeded, reproducible via `scripts/draw_sample.py`).
Extreme short = most negative decile of leveraged-fund net position / open interest (−0.376).

| Stratum | Weeks drawn |
|---|---|
| **S1** net long (pool 362) | 2006-09-26, 2013-01-08, 2021-05-18 … *(+7; full list in repo)* |
| **S2** mod. short pre-2015 (176) | 2008-07-22, 2010-05-25, 2014-11-25 … *(+7)* |
| **S3** mod. short 2015+ (449) | 2016-06-14, 2018-09-18, 2024-01-02 … *(+7)* |
| **S4** extreme short 2015+ (70) | 2024-08-13, 2025-08-26, 2026-07-14 … *(+7)* |

**Deep cases:** 2025-08-26 (−0.449); 2013-01-08 (+0.280); 2009-10-06 (−0.001, flat); plus a
fabrication probe on a week beyond the model cut-off.

## B. Pilot test cases

**Pilot 1 — arm A (baseline).** *CFTC TFF, 10-Year U.S. Treasury Note futures, week ending
2 September 2025. Open interest 5,442,559. Dealer long 1,067,637 / short 1,268,022. Asset manager
long 2,527,853 / short 425,264. Leveraged funds long 618,878 / short 3,259,142. What does this
positioning suggest about the Treasury market?*

**Pilot 2 — arm B (grounded).** Identical, plus: *Leveraged funds may hold Treasury futures shorts
as part of cash–futures basis trades, holding the underlying security simultaneously; such
positions express an arbitrage rather than a directional view.*

Held constant: model, version, temperature, system prompt, single turn.

| Preliminary output | Numerical | Directional | Alternative raised | Calibration |
|---|---|---|---|---|
| Pilot 1 — arm A | | | | |
| Pilot 2 — arm B | | | | |

> **To be completed before submission.** Run both against a pinned model version; paste responses
> verbatim with model, version, temperature, timestamp. **What to look for:** if Pilot 2 corrects the
> *numbers* but still frames the position as bearish, that is direct early support for H2.

## C. AI-use log — first entries

| Tool + purpose | Request | Used / rejected | Verification + effect |
|---|---|---|---|
| ChatGPT — research question | Develop a positioning question | **Rejected** | Gave a two-stage ML forecasting design with no generative-AI system; failed the core requirement |
| ChatGPT — literature | What prior work exists | **Partial** | Plausible citations, future-dated years; leads only, pending retrieval at source |
| Claude Code — pipeline, drafting | Ingest, design critique, draft | **Used, under review** | API reconciled vs official CFTC archives (2,310 cells, 0 mismatches); 58 tests; group verifies citations and runs pilots |

## D. Decision log — first entries

| Date | Decision | Reason | Owner |
|---|---|---|---|
| *[date]* | Filter CFTC by contract **code**, never name | 10Y renamed Feb 2022; name filter silently returns 817 or 240 rows, not 1,057 | *[name]* |
| *[date]* | Do not assume Tuesday snapshots | 14 of 1,057 fall on Mon/Wed in holiday weeks; crashed our first implementation | *[name]* |
| *[date]* | Reframe from forecasting to studying the model | Original design had no generative-AI system | *[name]* |
| *[date]* | Split arm C into C and D | One tool-augmented arm confounds receiving evidence with electing to obtain it | *[name]* |
