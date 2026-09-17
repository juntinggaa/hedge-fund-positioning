# Milestone 1 — Evidence Appendix

*(One page, not counted in the 3-page limit)*

## A. Planned investigation

```
   CFTC TFF data (verified, 1057 weeks)
                 │
      select 4 purposive test cases
                 │
      ┌──────────┴──────────┐
      ↓                     ↓
  BASELINE            VARIATIONS
  bare prompt         + basis context
                      + ask alternatives
                      + second model
                      + prose format
      └──────────┬──────────┘
                 ↓
          model responses
                 ↓
      double-scored on 4 measures
   directional · alternative · numerical · calibration
                 ↓
      compare baseline vs variation
                 ↓
   knowledge deficit or application deficit?
```

| Test case | Date | Ground truth | What it probes |
|---|---|---|---|
| TC1 Record short | 2025-09-02 | LF net −48.5% of OI; Fed research attributes much of this to basis trade | Maximum temptation to read as bearish |
| TC2 Net long | *[select from the 34.2% of weeks]* | LF net positive | Reading the data vs reciting a narrative |
| TC3 Early era | *[pre-2015 week]* | Basis trade small; directional reading more defensible | Era-sensitivity |
| TC4 Fabrication probe | Week beyond cut-off | No data exists | Refusal vs invention |

## B. Pilot test cases

**Pilot 1 — baseline prompt (TC1).** Verbatim:

> Below is CFTC Traders in Financial Futures data for 10-Year U.S. Treasury Note
> futures, week ending 2 September 2025.
>
> Open interest: 5,442,559
> Dealer — long 1,067,637 / short 1,268,022 / spreading 296,320
> Asset manager — long 2,527,853 / short 425,264 / spreading 200,509
> Leveraged funds — long 618,878 / short 3,259,142 / spreading 526,570
>
> What does this positioning suggest about the Treasury market?

**Pilot 2 — context variation (TC1).** Identical, with one sentence appended:

> Note that leveraged funds may hold Treasury futures shorts as part of cash–futures
> basis trades rather than directional positions.

*Held constant across both: model version, temperature, system prompt, single-turn.*

### Preliminary output

> **To be completed by the group before submission.** Run both pilots against a pinned
> model version and paste the responses verbatim, with model, version, temperature and
> timestamp. Score each on the four measures in §4 of the proposal.
>
> These outputs must be generated and inspected by the group. They are not reproduced
> here because no result may be reported that the group has not itself run — per the
> course AI-use requirements and the Minimum Evidence Standard.

| | Directional attribution | Alternative raised | Numerical fidelity | Calibration |
|---|---|---|---|---|
| Pilot 1 (baseline) | | | | |
| Pilot 2 (+ context) | | | | |

## C. AI-use log — first entries

| Tool + purpose | Input/request summary | What was used or rejected | Verification + effect on decision |
|---|---|---|---|
| ChatGPT — research question development | Iterated on an institutional-positioning research question | **Rejected** the resulting design | Proposed a two-stage ML forecasting project with no generative-AI system; failed the NST2046 requirement. Discarded and reframed. |
| ChatGPT — literature search | Asked what prior work existed | **Partially used** | Returned plausible citations with 2026 dates; treated as leads only, pending retrieval at source. |
| Claude Code — data pipeline | Build and verify CFTC ingest | **Used** | Reconciled API against official CFTC archives, 2,310 cells, zero mismatches; 58 automated tests. |
| Claude Code — proposal drafting | Draft this proposal | **Used, under review** | Group verifies every citation at source and runs all pilots itself before submission. |

## D. Decision log — first entries

| Date | Decision | Reason | Evidence | Owner |
|---|---|---|---|---|
| *[date]* | Filter CFTC data by contract code, never name | CFTC renamed the 10Y contract in Feb 2022; a name filter silently returns 817 or 240 rows instead of 1,057 | Verified against live endpoint | *[name]* |
| *[date]* | Do not assume snapshots fall on Tuesdays | 14 of 1,057 fall on a Monday or Wednesday in holiday weeks; the assumption crashed our first implementation | Verified against live endpoint | *[name]* |
| *[date]* | Pin data vintage by content hash | A CFTC revision would move both the API and the archives together; only a hash detects it | `data/manifests/` | *[name]* |
| *[date]* | Reframe project to audit an LLM rather than build a forecaster | Original design had no generative-AI system; ~30% of the rubric had no answer | NST2046 guidelines §1, §6 | *[name]* |
