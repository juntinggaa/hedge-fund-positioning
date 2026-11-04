# Model v2: audit, comparison and recommendation

Run on 2026-11-05 against the frozen spec `SPEC_2026-11-05.md`. **All comparisons
are exploratory**, because v1 out-of-sample results had already been seen.
**Outcome: a null improvement.** Under the predeclared rule no candidate beats the
corrected v1 ridge, so **model v2.0 = M3, the v1 specification with audit fixes.**

## Reproduce

```
python -m hfpos.ingest.cftc_traders     # trader counts + revision check (network)
python scripts/model_v2.py              # all candidates, audits, tables, figures, selection
python scripts/build_stimuli_v2.py      # model card + versioned stimuli
python scripts/build_prompts.py --week 2025-09-02 --arm C-ann --model-version v2
pytest tests/test_model_v2.py
```

Outputs:
- `reports/model_v2/{comparison, loss_differentials_vs_M3, splits, audits, alt_target}.csv`
- `selection.json` and three figures
- predictions in `data/processed/model_v2/`

v1 regenerates byte-identically (checked with `git diff` after rerunning
`scripts/stage1_report.py`).

## 1. Audit findings

| item | finding | effect | action |
|---|---|---|---|
| A. Scaler before RidgeCV/LassoCV inner splits | **Confirmed.** Inner validation folds shared the scaler fitted on the full outer training fold. No leak into the outer test week. | R² 7.53% (v1-style) vs 7.40% (fixed). The fix picks more shrinkage: prediction SD 0.0063 → 0.0053, MZ slope 0.95 → 1.13. | v2 uses `GridSearchCV` over the whole pipeline. A test records the fit sizes (20/40/60/80/100). |
| B. GBM random early-stopping holdout | **Confirmed.** `validation_fraction=0.2` is a random split. It does not touch the outer test block. | Without early stopping, GBM gets *worse* (3.46% → 0.34%). Random early stopping was acting as regularisation, not inflating results. | GBM stays out of contention under either setting. |
| C. Information timing | Features: market data through *t*, CFTC cross-group/contract data through *t−1*. **But `d_log_oi` uses this week's CFTC open interest**, which arrives in the same Friday report as the target. | **Not a nowcast.** It is a **retrospective same-week conditional estimate**. (An earlier draft claimed pre-Friday availability; withdrawn, spec Amendment 1.) | Wording corrected in the spec, here, and in the v2 annotation. |
| C. Revisions | Live CFTC vs pinned panels, all four contracts: **0 revised cells**. FRED yields are not vintage-tracked. | none | `cftc_traders.revision_check` |
| D. Tables vs stimuli | v1 tables and stimuli come from the same ridge run. `config.yaml stage1.feature_set` was **not read anywhere** (the default was hardcoded). | Same numbers, by coincidence. | `build()` now reads the config. v2 stimuli carry `model_id`/`model_version` and a predictions hash, checked by a test. |
| E. Frozen annotation | The v1 text says "about 5%" and "0.98" (actual: 7.5%, 0.957) and names a "futures-cash spread". | Factually stale in the C-ann arm. | v1 text left byte-identical (hash test). A versioned v2 template is filled from `model_card_v2.json`. |
| Basis feature | `futures_cash_spread` is a futures-*return* residual after the CMT-yield move, not a valuation basis. Its docstring had the direction **backwards**: the long-cash/short-futures trade pays when futures are *rich* (Glicoes et al. 2024). | none on the numbers | Renamed `futures_yield_residual` in v2. Docstring corrected. |
| Arm design | **C and D do not include B's mechanism paragraph.** Every arm starts from A. | B vs C is not a nested comparison. My earlier walkthrough described it wrongly. | Documented in `build_prompts.py`. The design is unchanged and is the team's call. |

## 2. Main comparison (720 common weeks, 2012-11-27 .. 2026-09-08)

| candidate | R² vs mean | R² vs zero (= level vs random walk) | RMSE (pp OI) | MZ slope | resid AC1 | corr(resid, actual) | ΔMSE vs M3 | HAC p (1-sided) | boot 90% CI excludes 0 |
|---|---|---|---|---|---|---|---|---|---|
| B0 zero change | 0.15% | 0 | 2.19 | – | −0.15 | 1.000 | −7.8% | – | – |
| B1 hist. mean | 0 | −0.15% | 2.19 | – | −0.15 | 1.000 | −8.0% | – | – |
| B2 AR(1) | 1.96% | 1.81% | 2.17 | 0.81 | 0.02 | 0.985 | −5.9% | 1.00 | no |
| **M3 corrected ridge, exp** | **7.40%** | **7.26%** | **2.10** | 1.13 | −0.02 | 0.970 | ref | – | – |
| M3 rolling 5y | 6.79% | 6.65% | 2.11 | 1.11 | −0.08 | 0.973 | −0.7% | 0.70 | no |
| M4 + trend, exp | 8.35% | 8.21% | 2.09 | 1.21 | −0.03 | 0.970 | **+1.0%** | **0.095** | **no** (−0.07e-5 .. +1.0e-5) |
| M4 rolling | 7.68% | 7.54% | 2.10 | 1.16 | −0.08 | 0.971 | +0.3% | 0.41 | no |
| M5 + econ, exp | 7.11% | 6.97% | 2.11 | 1.39 | −0.06 | 0.980 | −0.3% | 0.63 | no |
| M5 rolling | 7.24% | 7.09% | 2.11 | 1.34 | −0.09 | 0.979 | −0.2% | 0.55 | no |
| M6 fused-lag, exp | 0.24% | 0.09% | 2.18 | 0.97 | −0.15 | 1.000 | −7.7% | 1.00 | no |
| M6 rolling | 1.66% | 1.51% | 2.17 | 0.75 | −0.16 | 0.986 | −6.2% | 1.00 | no |

**Selection:** M4-exp is the only candidate with HAC p < 0.10, but its bootstrap CI
includes zero, so it fails the predeclared rule. With six comparisons, p = 0.095
would be weak evidence anyway. **Retain M3.**

Figures:
- `cum_loss_vs_M3.png`: M4's lead builds slowly from 2018 and gives some back in
  2022 and 2026.
- `mse_reduction_ci.png`
- `m6_return_signature.png`

### Splits (R² vs mean, predeclared, thresholds use prior data only)

| split | n | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|
| 2013–16 | 208 | 8.4% | 8.4% | 4.6% | 0.3% |
| 2017–19 | 157 | 5.0% | 7.8% | 6.5% | 0.1% |
| 2020–22 | 156 | 5.2% | 5.9% | 7.0% | 0.3% |
| 2023–26 | 193 | 9.2% | 10.6% | 12.2% | 0.3% |
| stressed (VIX > prior 67th pct) | 165 | 5.0% | 7.1% | 6.8% | 0.5% |
| calm (VIX < prior 33rd pct) | 306 | 5.5% | 6.0% | 3.6% | 0.3% |
| extreme `s_{t-1}` (prior-260w pct ≤10/≥90) | 328 | 7.2% | 9.6% | 8.1% | 0.1% |
| non-extreme | 392 | 7.6% | 7.4% | 6.4% | 0.4% |

v1 reported 7.9% vs 2.9% for stressed vs calm, using **full-sample** VIX terciles.
With prior-only thresholds the gap is 5.0% vs 5.5% for M3, so **the v1 claim that
the model works better under stress does not survive and should be dropped from
the report.**

v1's "most extreme 10% of short positioning: 13.8%" used a full-sample decile. The
v2 split is not comparable. Because the level trends, 328 of 720 weeks (46%) sit
in the top or bottom decile of their own trailing 5 years. On that definition M3
is no better on extreme weeks (7.2%) than elsewhere (7.6%). **Soften the v1
extreme-positioning claim as well.**

## 3. Target checks

- **Alternative target** `(N_t − N_{t−1})/OI_{t−1}`: M3 R² 5.89% vs its own mean.
  Its predictions correlate 0.935 with the primary model's. This is not a reason
  to switch targets; the scales differ.
- **`d_log_oi` ablation:** removing it costs the primary target ~1 pp
  (7.40% → 6.41%) and the alternative target nothing (5.89% → 5.88%). **About a
  seventh of the primary model's R² is denominator mechanics** (OI growth
  mechanically shrinks net/OI), not information about positioning decisions. Say
  so in the report.
- **Level:** R² vs zero change equals R² of the reconstructed level against a
  random walk, 7.26% for M3. The 98.6% level-vs-mean figure from v1 is not
  evidence of skill.
- **Historical context** (`level_pct_prior_260w` in the v2 stimuli): where `s_t`
  sits among the previous 260 weeks. It is a different notion from the residual.
  An extreme *level* is not an unexpected *adjustment*.

## 4. corr(residual, actual) ≈ √(1−R²) is not an identity here

The identity holds for **in-sample OLS with an intercept**, with R² measured
against the same sample's mean. There the residual is orthogonal to the fitted
values. Out of sample, `Cov(e, ŷ) = Var(ŷ)(b − 1)`, where *b* is the
Mincer–Zarnowitz slope, and R² is measured against an expanding mean rather than
the evaluation-sample mean. So:

- **Under-dispersed predictions (b > 1).** The residual co-moves with the
  prediction and corr(e, y) > √(1−R²). M3: b = 1.13, corr 0.970 vs √ 0.962.
- **Over-dispersed predictions (b < 1).** corr(e, y) < √(1−R²). v1 ridge: b = 0.95,
  corr 0.957 vs √ 0.962.

The approximation was close for v1 by luck of calibration. It is still a useful
rule of thumb: a 0.9 correlation needs R² of roughly 19%. But the report should
call it an approximation, not an identity.

**The original gate (corr ≤ 0.9) is retained and failed:** 0.957 for v1 and 0.970
for v2.0. It is not replaced.

## 5. Research → implementation

| paper | methodological lesson | our adaptation | limitation |
|---|---|---|---|
| Boos & Grob (2023) | Position = smooth weighted sum of past daily returns. Difference both sides to avoid a spurious regression. A fused ridge penalises adjacent-lag differences (eq. 7). 5-year rolling window; nowcast before the Friday release. | M6: 250 lags, regressor differenced against the *actual* previous snapshot, uniform smoothing, γ by inner time-series CV; expanding and 5-year rolling windows. | Commodities, contracts target, LOOCV, weekly refit. **Their ~40% R² is not our benchmark.** Out of sample here, γ hits the grid's upper bound and R² ≈ 0. This specification did not explain the series; that is not evidence about whether the funds trend-follow. The full-sample signature is a negative ramp, descriptive only. |
| Park (2019) | Speculators' **trader counts**, net and in excess of the cross-maturity average, as curve-positioning indicators. Legacy COT; not duration-adjusted. | Lagged leveraged-fund long/short trader counts; a DV01-*approximate* curve tilt from **positions** (fixed per-contract DV01). | Park's excess-net-count indicator was not replicated. Our DV01s are fixed approximations. Park's object is information about the economy; ours is same-week adjustment. |
| Barth et al. (2024) | Asset managers' reaching for duration drives >60% of the rise in futures OI. Hedge funds take the other side. | Already present: lagged asset-manager net and change; `d_log_soma` for Fed duration absorption. | No mutual-fund (N-PORT) flows or Treasury supply series added (see §7). |
| Glicoes et al. (2024) | A basis is a valuation (CTD invoice vs cash, net of carry and term repo). Futures shorts alone overstate basis activity. | Renamed the return-residual feature and corrected its interpretation. No basis built from CMT yields. | No CTD/conversion-factor/term-repo data, so no genuine basis. |
| Kruttli et al. (LTCM Redux) | Internal VaR constraints and precautionary liquidity, not repo terms, drove 2020 de-risking. | Proxies: `pos_x_rvol` (position × Treasury vol), `funding_x_vix`, `d_rvol_4w` (in M5). | Form PF VaR is confidential. The proxies did not help out of sample (M5 ≈ M3). |

## 6. Assessment and recommendation

**In plain English.** The corrected model is a **modest** improvement on simple
predictions. Its RMSE is about **3.8% lower** than the historical-mean benchmark;
the richer-trend M4 would cut a further ~0.5%. It is not a strong decomposition of
positioning. Of the 72 largest absolute weekly changes, **64 are also among the
72 largest absolute residuals (89%)**, so most extreme cases are already visible
in the raw change (see `CASES.md` for the weeks it does re-rank). None of the
research-motivated changes reliably improves the estimate. Richer trend signals (M4) help a little: about 1%
lower squared error, concentrated after 2017. But the gain is within the noise of
the bootstrap. The economic block (M5) adds noise on average, though it does best
in 2023–26. Our adaptation of the Boos–Grob distributed-lag model, which explains ~40% of
commodity speculators' position changes in their paper, explains essentially
nothing here. The defensible conclusion is narrow: **this trend specification
did not explain aggregate 10Y leveraged-fund positioning.** It does not show
these funds are not trend-followers. Aggregation across strategies, the net/OI
target, the 13-week refit, the γ grid (γ hit its upper bound) and the
one-contract scope could each produce the null. The synthetic-recovery test
verifies the estimator, not the economic reading. A null result from five specifications is
**not** a ceiling on what is attainable.

**Recommendation:** use **model v2.0 = M3, the corrected ridge** (expanding
window). It has the same specification as v1, with the audit fixes, versioned
metadata and an accurate annotation.

**Proposed ML-output block** (`--model-version v2`, real output for 2 Sep 2025):

```
Output of a supervised model of leveraged-fund positioning (model v2.0):

- Expected net position this week: -45.39% of open interest (90% range from the model's past errors: -48.89% to -41.89%)
- Actual net position this week: -48.53% of open interest
- Residual (actual minus expected): -3.13% of open interest, larger in size than 85% of the model's past out-of-sample residuals
```

The v2 C-ann annotation is filled from `model_card_v2.json`: 7% of variance, error
2.1 pp, correlation 0.97, the real feature list, and "residual = unexpected
change given last week's position".

**Interval coverage (checked on saved predictions, prior-only RMSE, ≥52 prior
errors):** the ±1.645·RMSE band contained the actual change in **91.3% of 668
eligible weeks**: 88.9% in 2013–16, 91.7% in 2017–19, 91.7% in 2020–22 and 92.7%
in 2023–26. It is described as an *approximate* 90% range supported by
historical coverage, not a guarantee.

**What M5 did not test.** Trader counts and volatility interactions are not the
mechanisms the literature names. Untested: genuine cash-futures basis
profitability, Treasury supply, dealer balance-sheet/financing capacity, and
direct asset-manager demand. The highest-value next question is whether a
defensible historical basis-profitability measure can be built, and whether it
explains *gross short* adjustments. That is a separate research phase, not part
of Milestone 2.

**Team decisions before regenerating experimental materials:**
1. The v2 block adds an uncertainty range and a residual percentile. That is more
   information than the v1 pilot saw, so C-bare/D responses under v1 and v2 are
   not comparable. Pick one version for the whole main run.
2. The band needs 52 prior errors, so **2 sampled weeks (2013-01-08, 2013-09-03)
   lose model output** (coverage 29 → 27 of 41). The alternative is dropping the
   band for all weeks to keep 29.
3. `level_pct_prior_260w` is computed but **not shown**. Showing it only in the C
   arms would confound C against A.
4. Arms are not cumulative (C ⊅ B). Either keep that and say so, or add a B+C arm.

**Options for the main comparison** (not decided):
- Use model v2.0 **with** the approximate range, accepting 27 covered cases.
- Run A/B/C/D on **the same 27 cases**, and report extra A/B cases separately.
- *Withdrawn 2026-11-05:* "report C vs D as the primary model-arm contrast". What
  each contrast identifies is in `docs/milestone2/COMPARISONS.md`; the research
  question and primary comparison are a team decision.
- The v2 pilot (`docs/milestone2/pilot_v2/PILOT_V2.md`) changed the block's
  percentile wording and raised one open design choice: whether to show the
  residual as a *change*.

## 7. Worthwhile extensions needing data we lack or deferred

- A genuine net basis / implied repo: CTD prices, conversion factors, term repo
  (Glicoes et al.).
- NY Fed primary-dealer positions and financing (weekly API exists; series breaks
  in 2013/2015/2022/2024 need careful splicing).
- Treasury auction settlements by tenor (FiscalData), and an FOMC/payroll/CPI
  calendar with scheduled dates.
- Rate-implied volatility (MOVE is proprietary) and DV01 from actual CTD
  durations, instead of fixed approximations.
- Form PF / OFR Hedge Fund Monitor aggregates with publication-date vintages
  (quarterly).
- Forecast calibration (MZ slope ≈ 1.1–1.4 says ridge predictions are shrunk).
  Any rescaling must be fitted on training folds only. Not done here, to avoid a
  post-hoc tweak.

## 8. What this does not show

- A higher R² does not identify more basis trading.
- Residuals do not identify private information.
- The v1 Granger result (p = 0.86) does not prove positioning has no information.
- Five failed specifications do not establish a performance ceiling.
