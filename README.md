# Unusual Institutional Positioning and U.S. Treasury Futures

Full scope, methods, risks and milestones: [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md)

## Research question

> After removing the component of leveraged-fund Treasury futures positioning explained by
> basis-trade conditions, momentum, and macro-financial state, does the residual contain
> incremental out-of-sample information about Treasury futures returns and volatility — and
> does a machine-learned definition of "unusual" outperform a simple positioning z-score?

## Pre-registration — FROZEN

Committed before any Stage-2 code existed. Do not edit.

**Primary test.** Leveraged-fund ML surprise → 1-week-ahead 10Y Treasury futures return.
Augmented model vs. baseline. Clark–West test for nested out-of-sample forecast comparison.
Threshold 5%. **Two-sided.**

**Secondary, exploratory, multiplicity-adjusted.** Horizons 2w/4w · dealers and asset managers ·
2Y/5Y/30Y, level vs. slope · realized volatility · high-volatility interaction · surprise tails.

## Hypotheses

| # | Hypothesis |
|---|---|
| H1 | The leveraged-fund positioning surprise has incremental predictive content for 1-week 10Y returns beyond a macro/market baseline (two-sided) |
| H2 | The ML surprise outperforms a 52-week z-score of net positioning |
| H3 | Predictive content is stronger for volatility than for direction |
| H4 | Predictive content concentrates in the tails of the surprise distribution |

## The two diagnostics that decide whether this project has a thesis

Reported in the main text, week 5, before Stage 2:

1. Stage-1 out-of-sample R²
2. `corr(residual, raw Δ(Net/OI))` — above ~0.9 and the decomposition is cosmetic

## Deliverables that do not depend on a significant result

1. Decomposition of leveraged-fund positioning drivers, 2006–2026
2. Honest effect sizes with bootstrap intervals
3. ML surprise vs. z-score vs. raw, identical test windows

## Setup

```bash
bash scripts/bootstrap_github.sh    # creates repo, labels, milestones, issues, fills the board
```
