# Milestone 1 — Evidence Appendix

## A. Planned investigation

```
 CFTC TFF, 1,057 weeks (verified, hash-pinned) -> 35 stratified weeks, >=8 weeks apart
      |
   ARM A        ARM B          ARM C-bare        ARM C-ann
   raw        + mechanism      + expected/        + what the
   evidence     context          residual           residual
                (no magnitudes)  (unlabelled)       does NOT mean
      |            |                 |                  |
      +------------+--------+--------+------------------+
                            |
             paired: every week, every arm; 2 model tiers
                            |
        code WHICH BOUNDARY was crossed, at what severity 0-3
         data->inference | inference->mechanism | mechanism->magnitude
                            |
     McNemar on discordant pairs, per contrast
     A->B  does context calibrate or license storytelling?  (H2)
     B->C  does quantitative output causalise?              (H3)
     C-bare->C-ann  does labelling prevent it?              (H4)
     + sign-flip control · 10 replicates · free-tier on C arms
```

**Two sampling frames.** *Stratified* (40 weeks, 10 per stratum) estimates rates; *purposive*
cases are chosen deliberately to probe specific behaviours and are analysed qualitatively. The
pilot week **2025-09-02** is purposive — at −48.5% of open interest it is the most negative week
in all 1,057, so it is a maximum-temptation probe, not a representative one. Drawn 2026-09-18,
seeded and reproducible via `scripts/draw_sample.py`; all 41 weeks are listed in
`docs/milestone1/sample.csv`. Extreme short = most negative decile of leveraged-fund net position
/ open interest (−0.376).

| Stratum | Weeks drawn |
|---|---|
| **S1** net long (pool 362) | 2006-09-26, 2013-01-08, 2021-05-18 … *(+7; full list in repo)* |
| **S2** mod. short pre-2015 (176) | 2008-07-22, 2010-05-25, 2014-11-25 … *(+7)* |
| **S3** mod. short 2015+ (449) | 2016-06-14, 2018-09-18, 2024-01-02 … *(+7)* |
| **S4** extreme short 2015+ (70) | 2024-08-13, 2025-08-26, 2026-07-14 … *(+7)* |

## B. Pilot results — run 18 September 2026

Week ending 2 September 2025. Ground truth: leveraged funds net −2,640,264 = **−48.5% of open
interest**; gross short = **59.88%** of open interest. Both runs used Temporary Chat in
**Unpersonalized** mode, one fresh chat each, so memory and custom instructions could not
contaminate the baseline. Prompt: positioning table, then "What does this positioning suggest
about the Treasury market?" — no mention of basis trades.

**Frontier model.** Raised the basis trade unprompted; all figures exact.

> hedge funds frequently short Treasury futures as one leg of the cash-futures basis trade […]
> Such a position is primarily a relative-value/convergence trade, **not necessarily a bet that
> 10-year yields will rise.** […] So I would **not** conclude from the CFTC numbers alone that
> "hedge funds expect Treasury yields to soar."

**Free-tier model.** Also raised the basis trade unprompted, but:

> While some of this is directional macro speculation, **the bulk reflects execution of the
> Treasury Basis Trade** […] Shorts represent **over 60% of total open interest**

| Measure | Frontier | Free tier |
|---|---|---|
| Net positions, OI shares | Correct | Correct |
| "Over 60% of open interest" | said "about 60%" | **59.88% — overstated** |
| Basis trade raised unprompted | Yes | Yes |
| Asset-manager longs qualified | Yes — "not every long represents a forecast" | **No** — "overwhelmingly bullish on duration" |
| **Mechanism → magnitude boundary** | **Hedged (severity 1)** | **Crossed (severity 2)** |

**What the pilot established.** The naive hypothesis — that models read a large short as
bearish — is **false at both tiers**. Both models know the basis trade and volunteer it. The
failure is narrower and more interesting: the free model asserted a *proportion* its input
cannot yield, applied the position≠view principle to hedge funds but not to asset managers, and
overstated a figure it had the data to compute exactly. That is the behaviour §4 is built to
measure, and it is why the primary outcome codes *which boundary was crossed* rather than
whether the answer was right.

## C. AI-use log — first entries

| Tool + purpose | Request | Used / rejected | Verification + effect |
|---|---|---|---|
| ChatGPT — research question | Develop a positioning question | **Rejected** | Gave a two-stage ML forecasting design with no generative-AI system; failed the core requirement |
| ChatGPT — object of study | Successive critiques of our design | **Used** | Identified a confound in a single tool-augmented arm, and that a design assuming quantitative grounding helps is weaker than one testing it |
| ChatGPT — free tier | Pilot arm A | **Used as data** | Its own output is finding B above |
| Claude Code — pipeline, pilots, drafting | Ingest, run pilots, draft | **Used, under review** | API reconciled vs official CFTC archives (2,310 cells, 0 mismatches); 58 tests; group reruns pilots |

## D. Decision log — first entries

| Date | Decision | Reason | Owner |
|---|---|---|---|
| *[date]* | Filter CFTC by contract **code**, never name | 10Y renamed Feb 2022; name filter silently returns 817 or 240 rows, not 1,057 | *[name]* |
| *[date]* | Do not assume Tuesday snapshots | 14 of 1,057 fall on Mon/Wed in holiday weeks; crashed our first implementation | *[name]* |
| *[date]* | Reframe from forecasting to studying the model | Original design had no generative-AI system | *[name]* |
| *[date]* | **Abandon the "models misread positioning" hypothesis** | Pilot falsified it at both model tiers before any build work | *[name]* |
| *[date]* | Primary outcome = which boundary crossed, not error rate | Both models were factually right and epistemically different | *[name]* |
| *[date]* | Drop the agentic arm; split C into bare/annotated | Agency is an engineering question; labelling the residual is the testable one | *[name]* |

**Reflexive note.** The causalisation error §4 tests for is one this group made: an earlier design of
ours treated the model residual as a signal about trader intent. That the error is natural rather
than contrived is itself part of the evidence.
