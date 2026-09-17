# Unusual Institutional Positioning and U.S. Treasury Futures

**Status:** scoping draft · **Owner:** TBD · **Timeline:** 10 working weeks (shift to fit your deadline)

---

## 1. Summary

Leveraged funds hold very large short positions in U.S. Treasury futures, but a short
position is not the same thing as a bearish view — much of it is the cash–futures basis
trade, plus momentum and ordinary macro response. We use machine learning to model the
*normal* component of leveraged-fund positioning, treat the unexplained remainder as a
positioning **surprise**, and test whether that surprise carries incremental out-of-sample
information about subsequent Treasury futures returns and volatility.

The ML question is separate from the finance question and is stated explicitly:
**does a machine-learned definition of "unusual" beat a trailing z-score?** If it does not,
we report that.

---

## 2. Research question

> After removing the component of leveraged-fund Treasury futures positioning explained by
> basis-trade conditions, momentum, and macro-financial state, does the residual contain
> incremental out-of-sample information about Treasury futures returns and volatility — and
> does a machine-learned definition of "unusual" outperform a simple positioning z-score?

### Hypotheses

| # | Hypothesis | Direction |
|---|---|---|
| H1 | The leveraged-fund positioning surprise has incremental predictive content for 1-week 10Y Treasury futures returns, beyond a macro/market baseline | **Two-sided** |
| H2 | The ML-derived surprise outperforms a 52-week z-score of net positioning on the same test | One-sided |
| H3 | Predictive content is stronger for volatility than for direction | One-sided |
| H4 | Predictive content concentrates in the tails of the surprise distribution | One-sided |

**H1 is deliberately two-sided.** Unusual shorting preceding *falling* prices reads as
informed trading; unusual shorting preceding *rising* prices reads as crowded positioning and
forced unwinds. Both are real findings. Do not write the project so only one sign counts.

---

## 3. Pre-registered test plan

Fix this before looking at any Stage-2 output. Write it into the README and do not change it.

**Primary test (one, and only one):**

> Leveraged-fund ML surprise → 1-week-ahead 10Y Treasury futures return.
> Augmented model vs. baseline model. Clark–West test for nested OOS forecast comparison.
> Significance threshold 5%.

**Secondary (exploratory, multiplicity-adjusted, reported as such):**

- Horizons: 2-week, 4-week
- Groups: dealers, asset managers
- Maturities: 2Y, 5Y, 30Y; level vs. slope
- Outcomes: realized volatility, yield change
- Regime: interaction with a high-volatility dummy
- Tails: top/bottom decile of surprise

Secondary p-values get a Romano–Wolf or Benjamini–Hochberg adjustment. State the family size
in the paper. Roughly 3 groups x 4 horizons x 4 maturities is ~48 tests — at 5% you expect
two or three false positives by construction.

---

## 4. Success criteria

The project succeeds if it **answers** the question, not if the answer is yes. Three
deliverables, none of which depends on a significant coefficient:

1. **Decomposition.** How the drivers of leveraged-fund Treasury positioning shift across
   2006–2026 — GFC, ZIRP, March 2020, the 2022 hiking cycle, the 2023–25 basis-trade build-up.
   Descriptive, publishable, and interesting regardless of Stage 2.
2. **Honest effect sizes.** Out-of-sample R², Clark–West statistic, and bootstrap confidence
   intervals for the primary test, reported whatever they are.
3. **Method comparison.** ML surprise vs. z-score vs. raw position change, on identical
   test windows.

A null on H1 with all three delivered is a complete project. Say so to your supervisor now,
in writing, so nobody is disappointed in week 9.

---

## 5. Data checklist

| # | Dataset | Source | Identifier | Notes |
|---|---|---|---|---|
| 1 | CFTC Traders in Financial Futures | cftc.gov historical compressed archive | Futures-only, annual files | Dealer / Asset Manager / Leveraged Funds / Other, long + short + spreading, plus open interest. **Verify contract market codes against the report header — do not trust a code you found in a blog post.** |
| 2 | Treasury futures prices | CME settlement (preferred) or Yahoo `ZN=F` | 10Y note | See roll note below |
| 3 | Treasury yields | FRED | `DGS2` `DGS5` `DGS10` `DGS30` | Daily constant-maturity |
| 4 | Policy rate | FRED | `DFF`, `IORB` | |
| 5 | Repo / funding | FRED | `SOFR`, `BGCR`, `TGCR` | SOFR starts 2018; pre-2018 needs a fallback — see risk R4 |
| 6 | Equity vol | FRED | `VIXCLS` | |
| 7 | Rate vol | **Not on FRED** | — | MOVE is proprietary (ICE). Use realized vol from futures returns, or swaption-implied if your institution has access. Budget for realized vol. |
| 8 | Macro (optional) | FRED | `CPIAUCSL`, `UNRATE`, `T10Y2Y` | Watch release-date vs. reference-date alignment |

### Two data traps

**Roll.** `ZN=F` is a stitched front-month series with discontinuities at each quarterly roll.
Computing weekly returns naively across a roll boundary injects a spurious jump. Either
back-adjust, or compute returns within a single contract and chain them. Decide in week 2 and
document it.

**Release timing.** TFF positions are as of Tuesday close; the report publishes Friday
afternoon. This gives two distinct questions, and we report both:

- **Information content:** return window starts Tuesday close. Answers "did the positioning
  contain information?" Not tradable.
- **Tradable:** return window starts after the Friday release. Answers "could anyone have used
  it?" This is the economically meaningful one.

Never mix them. Never let a Tuesday-dated feature into a Tuesday-start tradable test.

---

## 6. Method

### Stage 0 — baseline reality checks

Before any ML. Do positions lead or lag returns? Run the lead-lag correlations and a small
VAR. If positions purely *follow* returns (Sanders–Irwin–Merrin), your Stage-1 feature set
must include lagged returns or the "surprise" will just be momentum wearing a hat.

### Stage 1 — model normal positioning

- **Target:** change in net position scaled by open interest, `Δ(Net/OI)`. Not raw net
  contracts — open interest grows by an order of magnitude over the sample.
- **Features:** lagged returns (1/4/12w), realized vol, yield levels and changes, 10Y–2Y
  slope, curvature, SOFR–IORB spread, basis proxy, ΔOI, lagged own position level and change,
  VIX, roll-week dummy, FOMC-week dummy.
- **Models:** Ridge and Lasso first, then XGBoost. **Report OOS R² for each.** With ~1,000
  observations and 20–40 features, the linear model may well win; if it does, say so — that is
  a finding about the data, not a failure.
- **Validation:** expanding window, minimum 260-week training block, refit every 13 weeks.
  Hyperparameters tuned on an inner time-series split *inside* the training window only.
  Feature scaling fitted inside the loop. No exceptions.

### Stage 2 — test the surprise

```
r[t+h] = a + b·surprise[t] + c'·X[t] + e[t+h]
```

Baseline `X` only, versus augmented `X + surprise`. Compare by out-of-sample R²
(Campbell–Thompson) and Clark–West, not in-sample t-stats.

### The four competing definitions of "unusual"

Run all four through the identical Stage-2 pipeline. This is the ML claim:

1. Raw `Δ(Net/OI)` — no model at all
2. 52-week z-score of `Net/OI` — the classic COT index
3. Ridge residual
4. XGBoost residual

If (3) and (4) do not beat (2), the machine learning contributed nothing and the paper says so.

### Two diagnostics that must appear in the paper

- **Stage-1 OOS R².** If it is near zero, the residual is the raw series and there is no
  decomposition.
- **corr(residual, raw Δ(Net/OI)).** If this is above ~0.9, the "strategy removal" is
  cosmetic. Report it in the main text, not an appendix. Somebody will compute it otherwise.

---

## 7. Inference protocol

Three corrections, all mandatory:

1. **Overlapping returns.** 2- and 4-week horizons overlap. Newey–West with lag ≥ h−1, or
   Hodrick standard errors.
2. **Generated regressor.** The Stage-2 regressor is estimated, so ordinary standard errors
   are wrong (Pagan 1984). With an ML first stage there is no analytic fix: **block-bootstrap
   the entire two-stage pipeline**, stationary bootstrap with mean block ~13 weeks, 1,000
   replications. Budget real time for this; it is the most likely point of attack in a viva.
3. **Multiplicity.** Primary test unadjusted. Everything else adjusted, family size stated.

### Power, stated honestly up front

TFF begins mid-2006. ~1,000 weekly observations, minus a 260-week burn-in, leaves roughly
700 test weeks — and at a 4-week horizon, ~175 non-overlapping ones. A realistic incremental
R² is 1–2%. Write this into the proposal so that a small effect is interpreted correctly
rather than as failure.

---

## 8. Economic significance

Cheap to add, and it makes the project feel finished. Map the surprise to a long/short
position in the 10Y contract, using the **tradable** (post-Friday) timing. Report Sharpe,
turnover, and max drawdown, gross and net of costs. ZN bid–ask is typically one tick
(1/64 of a point, ~$15.63 per contract) — small, but state the assumption explicitly.

---

## 9. Scope

### In

10Y flagship · leveraged funds as main subject · dealers and asset managers as benchmarks ·
Ridge/Lasso + XGBoost · z-score benchmark · block bootstrap · decomposition figure ·
tradable trading test

### Out (record the reasoning; reviewers will ask why not)

| Cut | Why |
|---|---|
| Mixture-of-experts | Needs far more than 1,000 observations |
| Inverse RL | TFF is an aggregated stock, not one agent's action sequence |
| Agent-based simulation | Separate project |
| Full HMM regimes | ~150 observations per regime. Use a volatility interaction dummy |
| Cross-asset extension | Only if weeks 9–10 come in early |

---

## 10. Milestones

| Week | Milestone | Done when |
|---|---|---|
| 1 | Scoping locked | Pre-registered test plan in README, supervisor sign-off on null-safe framing |
| 2 | Data ingest | TFF + prices + FRED pulled and cached; roll handling decided and documented |
| 3 | Feature pipeline | Basis proxy built; all features reproducible from raw with one command |
| 3 | Stage 0 | Lead-lag and VAR results written up |
| 4–5 | Stage 1 | Expanding-window harness; Ridge/Lasso/XGBoost OOS R² compared; leakage audit passed |
| 5 | **Gate** | Stage-1 OOS R² and corr(residual, raw) reported. If corr > 0.9, stop and rethink before Stage 2 |
| 6 | Stage 2 primary | Baseline vs. augmented, Clark–West, one number |
| 7 | Inference | Block bootstrap over full pipeline; Newey–West |
| 8 | Secondary + decomposition | Maturities, horizons, groups, tails, vol outcome; decomposition figure |
| 9 | Trading test + robustness | Tradable timing, subsample stability |
| 10 | Write-up | Paper, README, reproducible repo |

The week-5 gate is the important one. It is much cheaper to discover the decomposition is
cosmetic in week 5 than in week 9.

---

## 11. Risk register

| ID | Risk | Likelihood | Mitigation |
|---|---|---|---|
| R1 | Residual ≈ raw position change; novelty collapses | **High** | Week-5 gate. Report the correlation. Fall back to the decomposition as primary contribution |
| R2 | Null result on H1 | **High** | Null-safe deliverables (§4). Volatility outcome as second shot (H3) |
| R3 | ML loses to the z-score | Medium | That *is* a result. H2 is stated so this is reportable, not embarrassing |
| R4 | Basis proxy is weak; pre-2018 has no SOFR | **High** | Fallback ladder below. Downgrade the claim to "conditions favouring basis trading" if needed |
| R5 | Look-ahead leakage | Medium | Scaling and tuning inside the CV loop; separate information vs. tradable tests; explicit leakage audit in week 5 |
| R6 | Generated-regressor inference challenged | Medium | Block bootstrap, budgeted in week 7 |
| R7 | Relationship unstable across regimes | High | Subsample splits reported as a finding, not hidden |
| R8 | CFTC category reclassification breaks the series | Low–Medium | Check CFTC release notes for classification changes; inspect the series for step changes |

### R4 fallback ladder for the basis proxy

The claim "we removed basis trading" rests entirely on this, and it is the hardest item on the
data list — harder than everything else combined. In descending order of quality:

1. CTD implied repo vs. GC repo — needs the deliverable basket and conversion factors. Real work.
2. Futures-implied yield vs. cash 10Y yield
3. Swap spreads
4. SOFR–IORB spread

Also note: **the basis trade was small before roughly 2015**, so "removing basis" means
different things in different parts of the sample. Say this rather than letting a reader find it.

---

## 12. Repo layout

```
.
├── README.md                 # includes the pre-registered test plan, frozen
├── Makefile                  # make data / features / stage1 / stage2 / paper
├── environment.yml
├── data/{raw,interim,processed}/    # gitignored; ingest is reproducible
├── src/
│   ├── ingest/               # cftc.py  prices.py  fred.py
│   ├── features/             # basis.py  momentum.py  macro.py
│   ├── stage1/               # models.py  walkforward.py
│   ├── stage2/               # predict.py  inference.py
│   └── eval/                 # metrics.py  bootstrap.py  plots.py
├── tests/                    # at minimum: a leakage test on the walk-forward split
├── notebooks/                # exploration only; nothing load-bearing
└── reports/{figures,tables}/
```

One rule worth enforcing from day one: **notebooks are for looking, `src/` is for results.**
Every number in the paper comes from a `make` target.

---

## 13. Open questions for your supervisor

1. Deadline and expected output — course report or submittable paper? Changes how much §4
   matters.
2. Is there institutional access to swaption vol or CTD/deliverable-basket data? Determines R4.
3. Is a null result acceptable for the grade? Get this answered in week 1, in writing.
4. Team size and split. The natural three-way division is ingest/features, Stage 1, Stage 2 +
   inference.
