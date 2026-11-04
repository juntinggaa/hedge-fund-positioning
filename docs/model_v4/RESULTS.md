# Adaptation to changing market relationships — experiment results

Run date: 5 November 2026 (Singapore). Exploratory; the design was written before these fits.

**Recommendation: weighted_104.** candidate passes the exploratory replacement rule; not deployed. No selected model, LLM stimulus, or earlier result was replaced.

## What was compared

The same 40 inputs and weekly net-position/OI-change target were held fixed. Six training histories were tested, each with and without strictly earlier-OOS affine calibration: expanding, rolling 3/5/10 years (156/260/520 eligible observations), and exponential recency weights with 2/5-calendar-year half-lives (104/260 weeks). All use the same alpha grid and chronological inner CV.

The primary table uses **668 identical weeks, 26 November 2013–8 September 2026**. Calibration needs 52 previous outer-OOS pairs, so the initial 52 weeks are removed from **every** candidate's primary comparison. The familiar 7.40% baseline uses 720 weeks and is shown separately in raw_720_week_context.csv; do not compare it directly to the primary table's R².

## Matched-week results

| Candidate | R² vs mean | RMSE (pp) | MSE gain | 90% CI for gain | Holm p |
|---|---|---|---|---|---|
| weighted_104 | 10.81% | 2.060 | +3.33% | [+0.96%, +5.72%] | 0.070 |
| weighted_260 | 9.70% | 2.073 | +2.13% | [+0.83%, +3.46%] | 0.027 |
| weighted_104_calibrated | 9.49% | 2.075 | +1.90% | [-1.36%, +5.33%] | 1.000 |
| weighted_260_calibrated | 8.58% | 2.086 | +0.91% | [-1.37%, +3.43%] | 1.000 |
| rolling_156 | 8.13% | 2.091 | +0.43% | [-2.67%, +3.67%] | 1.000 |
| expanding | 7.74% | 2.095 | reference | — | — |
| rolling_520 | 7.72% | 2.095 | -0.02% | [-1.31%, +1.26%] | 1.000 |
| rolling_520_calibrated | 7.22% | 2.101 | -0.56% | [-2.25%, +1.23%] | 1.000 |
| rolling_260 | 7.22% | 2.101 | -0.56% | [-2.74%, +1.59%] | 1.000 |
| expanding_calibrated | 6.46% | 2.110 | -1.38% | [-2.64%, -0.07%] | 1.000 |
| rolling_260_calibrated | 6.35% | 2.111 | -1.51% | [-4.65%, +1.53%] | 1.000 |
| rolling_156_calibrated | 5.19% | 2.124 | -2.76% | [-6.79%, +1.32%] | 1.000 |

Reference R² on this matched sample: 7.74%; RMSE 2.095 percentage points of open interest. Best point estimate: **weighted_104**, R² 10.81%, MSE gain +3.33% versus reference. Positive gain means less error; uncertainty and the multiple-comparison rule determine whether to recommend a replacement.

## What the results mean

The successful adaptation keeps older history but gives it less influence. Under a two-year half-life, an observation two years old gets half the weight of the newest one; four years old gets one quarter. Rolling windows instead discard older observations completely. In this experiment, gradual forgetting performed better.

On the original **720-week** raw-prediction sample, expanding M3 has R² 7.40%, two-year weighting 10.47%, and five-year weighting 9.10%. These are matched comparisons too; the 668-week primary table is needed for fair comparison with calibrated variants.

For the best candidate, the RMSE reduction is 1.68% versus the expanding reference. An increase of a few percentage points in R² is not the same as a similarly sized reduction in RMSE. The error in each week remains large relative to the typical fitted adjustment.

The two-year weighted candidate passes the predeclared 10% family-adjusted threshold, but its adjusted p-value is above 5%. The five-year candidate has a smaller gain and stronger statistical evidence. Both remain exploratory findings, not confirmation on untouched data. Era results below show that gains are concentrated in 2017-19 and 2023-26; two-year weighting is essentially flat in 2020-22.

## Calibration versus each model's own raw predictions

These are secondary comparisons on the same 668 weeks, with a separate six-test Holm adjustment.

| Scheme | MSE reduction from calibration | 90% interval | Secondary Holm p |
|---|---:|---:|---:|
| expanding_calibrated | -1.38% | [-2.64%, -0.07%] | 1.000 |
| rolling_156_calibrated | -3.20% | [-5.12%, -1.23%] | 1.000 |
| rolling_260_calibrated | -0.94% | [-2.82%, +1.15%] | 1.000 |
| rolling_520_calibrated | -0.54% | [-1.98%, +0.96%] | 1.000 |
| weighted_104_calibrated | -1.48% | [-3.02%, +0.17%] | 1.000 |
| weighted_260_calibrated | -1.24% | [-2.62%, +0.25%] | 1.000 |

## Era stability

MSE reduction versus the same-week expanding reference. The last row is overlapping descriptive context and is not used for selection.

| Candidate | 2013-16 | 2017-19 | 2020-22 | 2023-26 | 2021+ (descriptive) |
|---|---:|---:|---:|---:|---:|
| weighted_104 | +0.22% | +5.01% | -0.07% | +9.61% | +5.30% |
| weighted_260 | -0.31% | +2.90% | +0.80% | +6.16% | +3.80% |
| weighted_104_calibrated | -1.18% | +2.84% | -3.70% | +11.14% | +4.54% |
| weighted_260_calibrated | -1.89% | +1.96% | -3.16% | +8.05% | +3.11% |
| rolling_156 | -4.35% | +2.86% | -3.62% | +8.99% | +2.82% |
| expanding | +0.00% | +0.00% | +0.00% | +0.00% | +0.00% |
| rolling_520 | +0.00% | -1.09% | +1.12% | -0.23% | +0.66% |
| rolling_520_calibrated | -1.31% | -0.77% | -1.37% | +1.51% | +0.74% |
| rolling_260 | -3.00% | +2.47% | -0.39% | -0.21% | +0.56% |
| expanding_calibrated | -1.31% | -0.00% | -4.23% | +0.19% | -1.81% |
| rolling_260_calibrated | -5.67% | +0.53% | -3.79% | +4.73% | +1.62% |
| rolling_156_calibrated | -9.89% | +3.40% | -6.79% | +5.55% | -1.00% |

## Temporal checks and calibration behaviour

- Equal-weight expanding and five-year rolling reproduce the existing v2 predictions within numerical tolerance.
- Scaling and alpha tuning occur inside each inner training fold. Weighted scaling and ridge use the same fold-local weights.
- Each calibrator uses at most 104 earlier outer-OOS pairs, with at least 52; it is held fixed over the next 13-week test block.
- No current-block labels or in-sample fitted values enter calibration. No slope was estimated on the evaluation sample and then applied backwards.

| Scheme | Median effective training n | Median alpha | Median prior-OOS calibration slope | Calibration slope range |
|---|---:|---:|---:|---:|
| expanding | 617.5 | 1000.00 | 1.12 | [0.55, 1.49] |
| rolling_156 | 156.0 | 1000.00 | 1.47 | [-0.06, 2.88] |
| rolling_260 | 260.0 | 1000.00 | 1.04 | [0.34, 2.75] |
| rolling_520 | 520.0 | 658.11 | 1.01 | [0.51, 2.23] |
| weighted_104 | 290.2 | 316.23 | 1.04 | [0.45, 1.79] |
| weighted_260 | 507.1 | 316.23 | 1.14 | [0.56, 1.77] |

Degenerate calibration fallbacks: 0. Large or unstable calibration slopes are diagnostics, not a reason to rescale all predictions after seeing the results.

## Interpretation and limits

This tests adaptation with the existing feature representation. It does not add genuine basis valuations, financing capacity, or confidential fund information. The result concerns a retrospective same-week conditional estimate, not a next-week forecast. Changes to estimation history do not undo long-memory feature construction (for example, expanding empirical-duration or funding transforms). A gain would show reduced historical prediction error under these rules; it would not identify strategies or private information. A null would not establish an inherent predictability ceiling.

Recommendation for a follow-on version: consider the uncalibrated two-year weighted model under the declared rule, with the five-year weighted model as a sensitivity check. Do not append the noisy affine calibration. Before collecting new LLM responses, any adoption needs its own model card, recomputed residual percentiles and uncertainty bands, a coverage check for that model, and newly versioned prompts. Existing M3 uncertainty claims must not be transferred unchanged.

The historical dataset and prior model results have already influenced development. The 11 replacement comparisons use Holm-adjusted one-sided HAC p-values and 90% stationary-bootstrap intervals (block mean 13, 2,000 replicates). These safeguards do not make the exercise fresh confirmation. Nested time-series CV tunes ridge penalties; training-history and calibration alternatives are evaluated as a declared exploratory family.

All 200 protected pre-existing files matched their pre-run SHA-256 hashes. No raw-data refresh, full LLM run, commit, push, or production-model replacement was performed.

## Reproduce

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/model_v4.py
.venv/bin/python -m pytest -q
```

Artifacts: comparison.csv, raw_720_week_context.csv, eras.csv, calibration_vs_own_raw.csv, fit_log.csv, calibration_log.csv, cumulative_improvement.csv, prediction parquet files, and selection.json.

Validation: 90 offline tests passed (including 11 new adaptation checks); 5 network tests were deselected. The new checks cover equal-weight reference equivalence, weighted scaling and regression, fold-local weights, outer-target causality, calibration warm-up, fixed-block calibration causality, degenerate calibration, and preserved files.

Implementation references: [weighted StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [weighted Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html).
