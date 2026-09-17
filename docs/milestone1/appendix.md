# Milestone 1 — Evidence Appendix

*(One page, not counted in the 3-page limit)*

## A. Planned investigation

```
        CFTC TFF data — 1,057 weeks, verified, hash-pinned
                              │
                 4 purposive test cases
                              │
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   ARM A                  ARM B                 ARM C
   baseline              grounded            tool-augmented
   bare prompt        + retrieval over      + decomposition
                      verified corpus         model call
        │                     │                     │
        │                     │            ┌────────┴────────┐
        │                     │            │ expected posn.  │
        │                     │            │ from mkt state  │
        │                     │            │        ↓        │
        │                     │            │ explained vs    │
        │                     │            │ unexplained     │
        │                     │            └────────┬────────┘
        └─────────────────────┼─────────────────────┘
                              ↓
                     model responses
                              ↓
        double-scored, inter-rater agreement reported
   numerical · directional · alternative · calibration · tool fidelity
                              ↓
              A→B: do facts fix framing?   (H2)
              B→C: does structure fix it?  (H3)
```

| Test case | Date | Ground truth | Probes |
|---|---|---|---|
| TC1 Record short | 2025-09-02 | LF net −48.5% of OI; Fed research attributes much to basis trade | Maximum pull toward "bearish" |
| TC2 Net long | *[select from the 34.2% of weeks]* | LF net positive | Reading data vs reciting narrative |
| TC3 Early era | *[pre-2015 week]* | Basis trade small; directional reading more defensible | Era sensitivity |
| TC4 Fabrication probe | Beyond cut-off | No data exists | Refusal vs invention |

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
