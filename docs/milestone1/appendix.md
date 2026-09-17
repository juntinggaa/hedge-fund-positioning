# Milestone 1 — Evidence Appendix

*(One page, not counted in the 3-page limit)*

## A. Planned investigation

```
     CFTC TFF — 1,057 weeks, verified, hash-pinned
                        │
        40 stratified weeks, drawn >=8 weeks apart
                        │
    ┌──────────┬────────┴────────┬──────────┐
    ↓          ↓                 ↓          ↓
  ARM A      ARM B             ARM C      ARM D
  bare     + qualitative    + precomputed  agent must
  prompt      context       decomposition  elect to call
    │          │                 │          │  the tool
    │          │                 └────┬─────┘
    │          │            ┌─────────┴─────────┐
    │          │            │ expected posn from │
    │          │            │ market state (walk-│
    │          │            │ forward)  ->  residual
    │          │            └─────────┬─────────┘
    └──────────┴─────────┬────────────┘
                         ↓
              paired: every week, every arm
                         ↓
       broad tier (40): directional attribution y/n
       deep tier  (4): full rubric + tool fidelity
                         ↓
         McNemar on discordant pairs, per contrast
       A->B  facts fix framing?     (H2)
       B->C  structure fix framing? (H3)
       C->D  agency add anything?   (H4)
```

### Stratified sample — drawn 2026-09-18, seed recorded, reproducible

Thresholds from the verified data: extreme short = most negative decile of
leveraged-fund net position / open interest (cut at −0.376).

| Stratum | n | Weeks drawn (net/OI in parentheses for the first three) |
|---|---|---|
| **S1** LF net **long** | 10 | 2006-09-26 (+0.209), 2007-07-17 (+0.133), 2009-12-08 (+0.017), 2011-03-29, 2013-01-08, 2013-09-03, 2021-01-19, 2021-05-18, 2021-11-09, 2022-01-11 |
| **S2** moderate short, **pre-2015** | 10 | 2008-07-22 (−0.037), 2009-04-28 (−0.074), 2009-10-06 (−0.001), 2010-03-16, 2010-05-25, 2010-11-16, 2011-03-15, 2011-08-09, 2014-09-30, 2014-11-25 |
| **S3** moderate short, **2015+** | 10 | 2016-06-14 (−0.033), 2017-02-21 (−0.059), 2018-05-01 (−0.176), 2018-09-18, 2019-11-12, 2022-11-22, 2023-01-24, 2023-04-18, 2024-01-02, 2026-03-10 |
| **S4** **extreme** short, 2015+ | 10 | 2024-08-13 (−0.400), 2024-10-08 (−0.421), 2024-12-10 (−0.384), 2025-04-08, 2025-06-03, 2025-08-26, 2025-10-21, 2026-02-03, 2026-04-07, 2026-07-14 |

**Deep cases (full rubric):** 2025-08-26 (S4, −0.449, the most extreme drawn week);
2013-01-08 (S1, +0.280, strongest net long); 2009-10-06 (S2, essentially flat); and a
fabrication probe asking about a week beyond the model cut-off.

## B. Pilot test cases

Arms A and B are runnable now; arm C requires the decomposition model (week 3).

**Pilot 1 — arm A, baseline (TC1).** Verbatim:

> Below is CFTC Traders in Financial Futures data for 10-Year U.S. Treasury Note
> futures, week ending 2 September 2025.
>
> Open interest: 5,442,559
> Dealer — long 1,067,637 / short 1,268,022 / spreading 296,320
> Asset manager — long 2,527,853 / short 425,264 / spreading 200,509
> Leveraged funds — long 618,878 / short 3,259,142 / spreading 526,570
>
> What does this positioning suggest about the Treasury market?

**Pilot 2 — arm B, grounded (TC1).** Identical, with retrieved context appended:

> Context: leveraged funds may hold Treasury futures shorts as part of cash–futures
> basis trades, in which the fund simultaneously holds the underlying Treasury
> security. Such positions express an arbitrage rather than a directional view.

*Held constant: model, version, temperature, system prompt, single turn.*

### Preliminary output

> **To be completed by the group before submission.** Run both pilots against a pinned
> model version and paste the responses verbatim with model, version, temperature and
> timestamp. Score each on the five measures in §4 of the proposal.
>
> Generated and inspected by the group. Not reproduced here, because no result may be
> reported that the group has not itself run — per the course AI-use requirements and
> the Minimum Evidence Standard.

| | Numerical | Directional | Alternative raised | Calibration |
|---|---|---|---|---|
| Pilot 1 — arm A | | | | |
| Pilot 2 — arm B | | | | |

**What to look for.** If Pilot 2 corrects the *numbers* but still frames the position as
bearish, that is direct early support for H2 — grounding repairs recall but not
interpretation — and it is the observation that motivates arm C.

## C. AI-use log — first entries

| Tool + purpose | Input/request summary | Used or rejected | Verification + effect on decision |
|---|---|---|---|
| ChatGPT — research question development | Iterated on an institutional-positioning question | **Rejected** | Produced a two-stage ML forecasting design with no generative-AI system; failed the NST2046 core requirement. Discarded. |
| ChatGPT — literature search | Asked what prior work existed | **Partially used** | Returned plausible citations with future-dated years; treated as leads only, pending retrieval at source. |
| Claude Code — data pipeline | Build and verify CFTC ingest | **Used** | Reconciled API against official CFTC archives: 2,310 cells, zero mismatches; 58 automated tests. |
| Claude Code — project design | Critique of the audit-only design | **Used** | Prompted the three-arm redesign after we judged a prompt-and-score audit too thin to demonstrate a mechanism. |
| Claude Code — proposal drafting | Draft this proposal | **Used, under review** | Group verifies every citation at source and runs all pilots itself before submission. |

## D. Decision log — first entries

| Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|
| *[date]* | Filter CFTC data by contract code, never name | CFTC renamed the 10Y contract in Feb 2022; a name filter silently returns 817 or 240 rows instead of 1,057 | Verified against live endpoint | *[name]* |
| *[date]* | Do not assume snapshots fall on Tuesdays | 14 of 1,057 fall on Monday or Wednesday in holiday weeks; the assumption crashed our first implementation | Verified against live endpoint | *[name]* |
| *[date]* | Pin data vintage by content hash | A CFTC revision would move API and archives together; only a hash detects it | `data/manifests/` | *[name]* |
| *[date]* | Reframe from forecasting to studying the model | Original design had no generative-AI system; core requirement unmet | NST2046 guidelines §1 | *[name]* |
| *[date]* | Add arm C rather than audit alone | An audit shows a failure; building the repair demonstrates a mechanism and tests responsibility directly | NST2046 §6 socio-technical integration | *[name]* |
| *[date]* | Drop predictive testing of the decomposition | Its role is honest description, not forecasting; predictive inference is out of scope | Proposal §6 | *[name]* |
