# Pilot results — arms A and B

**Run:** 18 September 2026 · ChatGPT web interface · reasoning effort **High**
**Configuration:** Temporary Chat + **Unpersonalized** ("this chat will ignore memory, plugins,
and custom instructions") — a separate fresh chat per arm.
**Ground truth:** CFTC TFF, 10-Year T-Note (`043602`), week ending 2 September 2025.
Leveraged funds net −2,640,264 = **−48.5% of open interest** (verified, hash-pinned).

> **Limitations of this run.** The web interface does not expose an exact model version
> string, request id, or token counts, and sampling parameters are not configurable. These are
> *preliminary* results in the sense the guidelines intend; the graded experiment should run
> through an API with a pinned model. Both arms are n=1.

---

## Arm A — baseline (no context supplied)

**Prompt.** CFTC TFF positioning table for the week ending 2 September 2025, followed by
"What does this positioning suggest about the Treasury market?" No mention of basis trades.

**Response (verbatim, abridged where marked):**

> For 10-year Treasury futures, long futures generally benefit from falling yields/rising
> Treasury prices, while shorts benefit from rising yields/falling prices. On that basis, the
> positioning is unusually polarized.
>
> [table: Dealers −200,385 / −3.7%; Asset managers +2,102,589 / +38.6%; Leveraged funds
> −2,640,264 / **−48.5%**]
>
> The leveraged-fund number needs much more caution. A 2.64 million contract net short looks
> spectacularly bearish if interpreted literally, but **hedge funds frequently short Treasury
> futures as one leg of the cash-futures basis trade**: buy the underlying Treasury bond,
> finance it in repo, and short the corresponding futures contract. Such a position is
> primarily a relative-value/convergence trade, **not necessarily a bet that 10-year yields
> will rise.**
>
> Dealer positions often reflect their role intermediating client flows and hedging inventory,
> so I would put less weight on that number as a directional forecast.
>
> The important market implication is therefore **crowding and asymmetry rather than an
> unambiguous bearish signal**. […]
>
> **So I would not conclude from the CFTC numbers alone that "hedge funds expect Treasury
> yields to soar."** The more informative signal is the extraordinary divergence between
> real-money and leveraged positioning.

## Arm B — grounded (basis-trade context supplied)

**Prompt.** Identical data, plus: "Note: leveraged funds may hold Treasury futures shorts as
part of cash-futures basis trades […] such positions express an arbitrage rather than a
directional view."

**Response (verbatim, abridged where marked):**

> The positioning looks less like a straightforward "Treasuries are bearish" signal and more
> like a large structural split between real-money longs and leveraged relative-value shorts.
>
> [table: identical figures, −48.5%]
>
> First, the leveraged-fund short should not automatically be read as a large bearish rates
> bet. […] the −2.64 million net leveraged-fund position considerably overstates how bearish
> hedge funds may actually be on duration.
>
> even here, "bullish" needs qualification: asset managers can use futures for duration
> management, benchmark replication and liability hedging, so not every long represents a
> discretionary forecast that yields will fall.
>
> Consequently, the data are **not a clean bearish signal** for 10-year Treasuries. […] it
> creates an important short-covering/basis-unwind tail risk if volatility or funding stress
> rises.

---

## Scoring

| Measure | Arm A | Arm B |
|---|---|---|
| Numerical fidelity | **Correct** — all three nets and OI shares exact | **Correct** |
| Unsupported directional attribution | **None** — explicitly refused | **None** |
| Non-directional explanation raised | **Yes, unprompted** | Yes (prompted) |
| Calibration | Appropriate — hedged, named the confound | Appropriate |

## What this means

**H1 is falsified on this test case.** The bare model did not misattribute directional intent.
It raised the basis trade unprompted, computed −48.5% of open interest exactly, distinguished
asset-manager duration demand from a bullish view, and stated that dealer positions are
intermediation rather than forecast. Arm B's added context changed the framing of the opening
sentence but not the substance — so **H2 cannot be tested as written either**, because there
was no factual or interpretive error for grounding to repair.

This is the scenario the proposal's §6 fallback anticipated: *"If H1 fails and the baseline is
already correct, the project becomes locating the boundary."* The pilot has done its job — it
falsified the central hypothesis before seven weeks were spent on it.

**Caveats before generalising.** n=1, one model, one week, the flagship case, a highly
structured prompt, and — importantly — **Unpersonalized mode**, which a real retail user is
not in. Weaker models, casual phrasing, multi-turn framing, and user push-back remain untested.
