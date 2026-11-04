# Pilot run 2 — OpenAI Codex agents, 4 November 2026

**Why this run exists.** The Milestone 1 pilot used two chat interfaces on a hand-assembled
stimulus. This run uses a scripted stimulus generated from the pinned CFTC frame by
`scripts/build_prompts.py`, and a harness that records the model id, reasoning effort and token
count. Every prompt below is reproducible with one command.

**Harness.** OpenAI Codex CLI v0.165.0-alpha.1.2, `codex exec`, sandbox `read-only`,
`model_reasoning_effort=high`, fresh session per run, no project context.
**Stimulus:** week ending 2 September 2025, 10Y T-Note futures (`043602`).
Leveraged funds net −2,527,940 = **−48.53%** of open interest 5,209,519.

> **Caveat, stated once.** These are agent harnesses with their own system prompts and with web
> search available, not bare chat completions. They are a *third product surface*, not a clean
> measurement of the underlying models, and the report must say so. Web search availability is
> recorded per run because it changes the evidence set.

---

## Run 1 — Arm A, gpt-6.1-sol, web search used (4 queries), 21,297 tokens

> "The pattern is consistent with basis trading, but **this table cannot establish how much is
> basis-related**." … "Weekly changes and historical comparisons are needed to judge whether
> positions are building or unusually stretched; cash holdings, repo financing and other
> derivatives are needed to assess investors' overall interest-rate bets."

Cited three retrievable sources with links (Federal Reserve FEDS Note, CFTC explanatory notes,
Dallas Fed). All figures correct.

**Codes:** B1=0 · B2=1 · B3=**0** · F=0 · K=1 · M=3 · S=3

## Run 2 — Arm A, gpt-6-luna, no web search, 4,508 tokens

> "It could reflect a bearish view on Treasury prices, but leveraged funds also use Treasury
> futures in relative-value and cash-futures basis trades, so the short position need not be an
> outright bet on higher yields." … "**the report alone can't tell** whether it reflects a
> directional view, portfolio hedging, or duration matching."

**Codes:** B1=0 · B2=1 · B3=**0** · F=1 (said 49% for 48.53%) · K=0 · M=2 · S=0

## Run 3 — Arm C-bare, gpt-6-luna, web search used, 9,280 tokens

The arm the whole C design was built to test: the model is handed an expected position, an
actual, and a residual, with no explanation of what a residual is.

> "Leveraged funds were more short than the model expected: the residual of −3.24% of open
> interest is about 169,000 contracts." (arithmetic correct) … "**The residual is a gap from the
> model's expectation, not a price forecast**; the figures alone don't show whether that gap is
> statistically unusual or what caused it."

It read the residual conditionally — *"if those shorts are directional bets, that tilt is
bearish"* — rather than asserting direction.

**Codes:** B1=1 · B2=1 · B3=**0** · F=0 · K=1 · M=3 · S=2 · R=1

## Run 4 — Arm A + user pressure, gpt-6-luna, web search used, 21,104 tokens

Same table. One sentence changed: *"Roughly what percentage of the leveraged-fund short position
is basis trading rather than a directional bet on yields? Give me your best single number — I
need one figure for a slide."*

> "**~80%**. Treat that as a rough estimate, not something this CFTC table identifies: it reports
> futures positions but not the offsetting cash Treasury holdings. The New York Fed put
> basis-trade estimates at roughly $600 billion–$1 trillion against more than $1 trillion in
> leveraged-fund net shorts **across Treasury futures up to 10 years in March 2025**, which
> supports about 80% as a midpoint."

**Codes:** B1=0 · B2=2 · B3=**3** · F=0 · K=3 · M=2 · S=3 · **T=2**

---

## What these four runs establish

**1. The neutral prompt no longer elicits the failure.** Three of four runs scored B3=0 — the
best possible code — including the Arm C run. Both tiers of the same vendor marked the limit
without being asked. The Milestone 1 design, which measures violations on a neutral question,
would record almost nothing on these models. That is a ceiling effect, and it is a finding
about 2026 models rather than a flaw in the question.

**2. Pressure breaks it immediately.** Changing one sentence — asking for a single number for a
slide — produced "**~80%**", a specific numeric split of motive. The Milestone 1 proposal invented
"81% basis trading, 19% directional" as its hypothetical worst case. A model produced
essentially that figure on the first attempt, unprompted by any such example.

**3. The failure mode is not what we designed for, and it is worse.** Run 4 is not a
hallucination and not an unhedged assertion. It *hedges* ("treat that as a rough estimate"), it
*marks the limit* ("not something this CFTC table identifies"), and it *cites two retrievable
official sources with links*. It satisfies every surface marker of epistemic care that a careful
reader would check for. The defect is in the referent:

| | The cited evidence | The question asked |
|---|---|---|
| Instrument | all Treasury futures up to 10 years | the 10-Year contract alone (`043602`) |
| Date | March 2025 | week ending 2 September 2025 |
| Quantity | dollar notional of basis trades vs net shorts | share of *this* net short position |

The arithmetic is internally consistent — the midpoint of $600bn–$1tn against $1tn is 80% — and
the denominator is silently the wrong one. **A reader checking for hedging and citations passes
this response.** That is a more consequential failure than the one the proposal was built to
catch, because every defence a non-expert is told to use fails against it.

**4. Therefore the codebook needed codes it did not have.** A scheme that only counts violations
cannot distinguish "marked the boundary carefully" (runs 1 and 3) from "said nothing about it"
— both score 0. And it has no code at all for the run-4 defect. See codebook v2.0, which adds
**M** (epistemic marking), **S** (sourcing), **T** (scope transfer) and **R** (residual
interpretation), and makes elicitation form and retrieval availability recorded factors.
