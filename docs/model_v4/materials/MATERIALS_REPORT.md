# Recency-weighted model: validated candidate materials

Prepared 5 November 2026. Existing model predictions were used; no refit or LLM experiment was run.

**Model v4.0: uncalibrated two-year-half-life ridge (weighted_104).** Material version: v4.0-review-1. The earlier default and every earlier experimental artifact are preserved.

## Performance and coverage

The exploratory adaptation comparison used 668 matched weeks: R² 10.81% versus reference 7.74%. The full 720-week raw-prediction record has R² 10.47% versus the historical-mean-change benchmark. These are different evaluation samples and are recorded separately in the card.

The unchanged range policy (1.645 × earlier OOS RMSE) achieved **91.9% coverage over 668 eligible weeks**. Width was not tuned after observing this result. It remains an approximate historical prediction range, not a guarantee for each case.

| Era | Weeks | Realised coverage | Mean half-width (pp OI) |
|---|---:|---:|---:|
| 2013-16 | 162 | 87.7% | 3.80 |
| 2017-19 | 157 | 92.4% | 3.65 |
| 2020-22 | 156 | 92.3% | 3.57 |
| 2023-26 | 193 | 94.8% | 3.47 |

## Example: 2 September 2025

- Expected net position: **-46.18% of open interest**.
- Actual net position: **-48.53%**.
- Residual: **-2.34 percentage points of open interest**.
- Approximate range: **-49.65% to -42.72%**.
- Prior error observations: 666; all precede this case.

The expected level is previous actual level plus predicted weekly change. The residual is a conditional level gap / unexpected adjustment. It is not an identified portion of basis trading, a directional forecast, or evidence of private information.

## Ready review materials

- Availability table retains all 41 original cases; 27 have both a saved OOS prediction and at least 52 earlier errors.
- 135 matched neutral-question review prompts: A, B, C-bare, C-ann and D on those same 27 cases.
- A and B are byte-identical to the legacy templates. C-bare retains level presentation; C-ann supplies the accurate new annotation. B's mechanism paragraph is not silently added to C or D.
- D preserves the earlier seeded permutation policy. Source weeks are recorded in the internal stimulus table; 0 cases retain their own residual under that permutation. The genuine-model coverage figure is not evidence about the validity of the deliberately altered placebo centre.
- The percentile text says 'smaller' and 'at least as large', accounting for ties and avoiding the earlier complementary-percentile confusion.
- Per-prompt hashes, the model-card hash, data/source hashes and a materials manifest tie every number to its version.

| Stratum | Original cases | Eligible cases |
|---|---:|---:|
| P | 1 | 1 |
| S1 | 10 | 4 |
| S2 | 10 | 2 |
| S3 | 10 | 10 |
| S4 | 10 | 10 |

## Scope and next use

These are prepared candidate materials, not collected evidence. The current research question, primary comparison, pressure factor, retrieval factor and proposed human coding rules are not changed by this build. The restricted eligible set is not a representative sample of all 41 cases or the full historical population. The model was selected retrospectively and includes current-week CFTC open interest, so it is not a pre-release nowcast.

The next experimental step is a small fresh pilot using a consistent retrieval-disabled harness and independent human coding. That pilot and any main LLM run have not been started here.

Preservation check: all 242 pre-existing files match their pre-build SHA-256 hashes. No older card, prompt, raw file, saved response, selection record or model result was replaced.

Validation: the full offline suite passed 100 tests, including 10 new material-generation checks; 5 network tests were deselected. Checks cover prior-only uncertainty, percentile ties, pinned-data reconstruction, placebo arithmetic, matched case sets, unchanged A/B text, accurate annotation metrics, provenance hashes and preservation.

## Reproduce

```bash
.venv/bin/python scripts/build_materials_v4.py
.venv/bin/python scripts/build_materials_v4.py --week 2025-09-02 --arm C-ann
```
