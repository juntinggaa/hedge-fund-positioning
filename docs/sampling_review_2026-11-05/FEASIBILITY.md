# NST2046 sample feasibility and spacing review — 5 November 2026

**Status: feasibility proposals only. No sample is frozen by this report. The original sample, pinned inputs, v4 results/card, and existing prompts remain unchanged. No main-experiment LLM responses were generated.**

## Recommendation

The eight-week rule is a heuristic, not a mathematical requirement of weekly data. It governs which weeks are sent to the LLMs: v4 continues to use the full weekly input grid and estimate one-week changes. A four-week case gap does not turn the target into a four-week change, and the 52-error minimum counts preceding weekly OOS errors, not 52 selected LLM cases. A four-week rule is a defensible candidate amendment, provided it is fixed before generating main responses and dependence is acknowledged. It does not make nearby cases independent, and it cannot restore unavailable pre-2013 model outputs.

**For the stated priorities of historical diversity and preserving the original stratification, recommend Option A:** keep the original 40 stratified cases plus the separate purposive case, and define two transparent paired analysis sets: A/B on all 40 stratified weeks, and all model-arm contrasts on the same 26 eligible stratified weeks. Run the A/B contrast again on that 26-week subset when comparing contrast sizes. Never compare an arm's 26-case rate against another arm's 40-case rate as a treatment effect. This design preserves the earlier moderate-short and net-long evidence that no complete-case design can cover with frozen v4.

If the team instead decides that a single complete five-arm comparison is the primary research question, **Option B with four-week spacing is the preferred complete-case alternative: 34 stratified cases (10/4/10/10), not 40.** A stricter across-strata four-week candidate is also feasible and supplied. Treat the four S2 cases as a small 2014 transition-period check, not evidence covering the whole pre-2015 era. Use the eight-week/32-case design as a predeclared design sensitivity. The supplied draws are alternatives, not post-response subsets to choose by significance.

Do not loosen all the way to weekly spacing to manufacture ten S2 cases. Do not adopt Option C simply to reach 40: it replaces historical balance with additional cases from already available regimes. The primary scientific contrast remains a separate team decision; this review does not promote a contrast based on pilot responses.

## Is the work necessary?

The feasibility review is necessary before promising a balanced five-arm sample: that promise is not achievable under frozen v4. The data update is optional for the main design and does not solve S2. It has been completed separately so the choice is concrete and reviewable. More ML tuning or a new literature search is not needed to settle this sampling constraint.

## Verified data update and frozen-model extension

- Series: CFTC TFF **futures only**, contract **043602**; 10-Year Treasury Note, not an Ultra-10Y or a futures-and-options series.
- Last official snapshot as of this review: **27 October 2026**, published **30 October 2026 at 15:30 Eastern**. The 3 November snapshot is not yet officially published on 5 November. The official report header and release schedule were checked, rather than treating the API maximum as a release timestamp.
- Original panel: 1,057 rows, 13 June 2006–8 September 2026. New append-only version: **1,064 rows**, ending 27 October. Added snapshots: 15, 22, 29 September; 6, 13, 20, 27 October.
- All 17 fields of every new row match the official 2026 annual archive. Latest open interest and all four groups' gross positions also match the latest official text report. No changed cells were found in the downloaded 2026 overlap for any of the four Treasury contracts. All original historical values are preserved regardless of any potential future revisions; this is an append-only extension, not a revised-history vintage.
- Supporting 2Y, 5Y, and 30Y panels were versioned too, because frozen v4 requires their lagged positioning. Price and FRED inputs were appended into new files without overwriting any pinned observations. The fetched overlap also matches the pinned price and FRED values exactly; seam-revision audits are supplied as CSVs.
- All **40 original features**, and the target, reproduce the pinned historical frame within numerical tolerance. All new feature cells are finite. Prices and daily rates/VIX use observations on or before each Tuesday. The Treasury-holdings observation is the preceding Wednesday (six calendar days old), never the following Wednesday. Source observation dates are recorded for every new week.
- The final v4 estimator was reconstructed on its original **975 training rows through 4 August 2026**, half-life 104 weeks, frozen ridge alpha **316.22776601683796**. It reproduces the five saved predictions in the existing final block to numerical tolerance. The seven additional weeks remain inside that same originally scheduled 13-week test block (12 total observed weeks). There was **no hyperparameter search, recalibration, re-selection, or fitting on added weeks**.
- All seven new predictions have **720–726 strictly preceding outer-OOS errors**, exceeding the 52-error minimum. The range remains expected position ±1.645 times RMS of all strictly earlier OOS errors. Earlier new errors may enter later new ranges; they never enter the frozen estimator. Current-week error is excluded from its own range/rank.
- The annotation and historical model-performance figures are not updated using these weeks. This review does not claim the new data improve v4 or constitute a new model-selection result.

### Publication timing and limits

A report observation date is different from its release date. The evaluation cutoff for each new case is that case's CFTC release, **Friday 15:30 Eastern**, not Tuesday morning. Same-week open interest is required, so these are retrospective conditional estimates, not Tuesday forecasts or prerelease nowcasts. Tuesday daily yields/VIX and futures closes are earlier than the Friday cutoff; Tuesday overnight reference-rate observations publish subsequently, before Friday. H.4.1 is normally Thursday at 16:30; the holdings observation actually used is from the preceding Wednesday and was published the preceding Thursday. None of the seven added releases is holiday-delayed under the official schedule.

This establishes observation alignment, schedule-consistent availability, and current availability. **It does not reconstruct exact historical first-release FRED/Yahoo vintages or prove every historical vendor delivery timestamp.** That would require a separate point-in-time vintage audit (e.g. ALFRED and archived price releases). This limitation also applies to existing v4; the extension does not upgrade it to a historically deployable backtest. Do not describe the ranges as exact conditional 90% probabilities or the model components as strategy shares.

Sources: [latest official futures-only report](https://www.cftc.gov/dea/futures/financial_lf.htm), [CFTC release schedule](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm), [official 2026 annual archive](https://www.cftc.gov/files/dea/history/fut_fin_txt_2026.zip), [H.15 release timing](https://www.federalreserve.gov/releases/h15/), [H.4.1 release timing](https://www.federalreserve.gov/releases/h41/), [SOFR publication](https://www.newyorkfed.org/markets/reference-rates/sofr), [EFFR publication](https://www.newyorkfed.org/markets/reference-rates/effr), [VIX series](https://fred.stlouisfed.org/series/VIXCLS), [ALFRED vintage coverage](https://alfred.stlouisfed.org/).

Detailed evidence: `extension_validation.json`, `data_manifest.json`, `feature_observation_dates.csv`, `additional_weeks.csv`, and the versioned flagship CSV/parquet and extended prediction parquet supplied with this report. Original raw manifests are unchanged.

## Original strata and exact feasibility

The extreme-short threshold is frozen at the original pinned panel's tenth percentile **among negative net/OI observations: −0.37567236606810045**. It was not recomputed after adding data. S1: net/OI > 0. S2: threshold < net/OI < 0 and before 2015. S3: the same moderate-short bounds from 2015 onward. S4: net/OI ≤ threshold from 2015 onward. Zero net/OI would be outside these definitions.

Valid Arm C requires a frozen v4 estimate and at least 52 strictly earlier OOS errors. That window begins **26 November 2013**, but its first qualifying **S2** case is **16 September 2014**: the earlier eligible observations do not satisfy the moderate-short definition. There are just **15 S2 candidates**, all in September–December 2014. Extending the 2026 endpoint cannot add pre-2015 cases.

All 675 eligible dates and their strata are in `all_eligible_dates.csv`; all historical inclusion/exclusion flags are in `all_historical_eligibility.csv`; complete numerical Arm C quantities are in `arm_c_available_all_dates.csv` (ratios, not percentage points, unless converted for display).

| Stratum | Eligible weeks | Eligible span | Max at 8 weeks | Max at 6 weeks | Max at 4 weeks |
|---|---:|---|---:|---:|---:|
| S1 | 134 | 2013-11-26–2022-07-05 | 23 | 28 | 38 |
| S2 | 15 | 2014-09-16–2014-12-30 | 2 | 3 | 4 |
| S3 | 454 | 2015-01-06–2026-10-20 | 64 | 83 | 123 |
| S4 | 72 | 2024-08-13–2026-10-27 | 13 | 15 | 23 |

These are exact individual-stratum maxima, not the size of a jointly spaced four-stratum sample. With equal spacing, selecting the earliest feasible date and repeating attains maximum cardinality; maximum witnesses are supplied in `maximum_witness_dates.csv`.

S2 maximum witnesses:

| Minimum spacing | Maximum | One feasible maximum set |
|---|---:|---|
| 8 weeks | 2 | 2014-09-16, 2014-11-11 |
| 6 weeks | 3 | 2014-09-16, 2014-10-28, 2014-12-09 |
| 4 weeks | 4 | 2014-09-16, 2014-10-14, 2014-11-11, 2014-12-09 |
| 3 weeks | 6 | 2014-09-16, 2014-10-07, 2014-10-28, 2014-11-18, 2014-12-09, 2014-12-30 |
| 2 weeks | 8 | 2014-09-16, 2014-09-30, 2014-10-14, 2014-10-28, 2014-11-11, 2014-11-25, 2014-12-09, 2014-12-23 |
| 1 week | 15 | All available S2 weeks; still one short historical episode |

All 15 S2 candidates: 2014-09-16, 2014-09-30, 2014-10-07, 2014-10-14, 2014-10-21, 2014-10-28, 2014-11-04, 2014-11-11, 2014-11-18, 2014-11-25, 2014-12-02, 2014-12-09, 2014-12-16, 2014-12-23, 2014-12-30. Absence of 23 September here is a stratum exclusion, not a license to interpolate a case.

### What loosening the spacing does

The original code enforces 56 days **within each stratum**, independently. It does not enforce this across all 40 weeks: the original stratified sample's smallest overall gap is 14 days. The purposive September 2025 case is deliberately separate and only seven days from an original S4 case. This should be disclosed rather than silently rewriting the original design as globally spaced.

Four, six, and eight weeks correspond to actual calendar gaps of 28, 42, and 56 days, including holiday-shifted snapshots. The additional global-spacing sensitivity uses interval constraints across all strata. Exact mixed-integer feasibility checks succeed for every B/C quota at every proposed gap; actual globally spaced dates are supplied in `B_4w_global_dates.csv`, etc. Thus neither interpretation rescues ten S2 cases, and stricter global spacing does not require sacrificing the proposed counts.

The original pinned series' net-position-level autocorrelation is about **0.971 at four weeks and 0.944 at eight weeks**; weekly-change autocorrelations are about 0.016 and −0.018, respectively. These are descriptive diagnostics, not estimates of LLM-error dependence or a power calculation. Since the LLM sees levels and recurring market states, low change autocorrelation does not establish independent responses. Eight-week spacing does not establish independence either. Do not calculate an effective sample size from these level correlations and present it as the LLM experiment's effective N.

## Concrete sampling alternatives and response budgets

Candidate B/C pools exclude the six identified previous pilot-development weeks and the separate purposive case, based only on identifiers, not on response content or scores. Excluded development dates: 2023-07-11, 2025-02-18, 2025-06-17, 2026-06-30, 2026-08-25, 2026-09-01. The unrestricted feasibility counts above still include them. The exclusion-adjusted maxima are supplied separately; S2 capacities remain 2/3/4, and all proposed B/C quotas remain feasible.

Option A must preserve every original week, so it retains a known development overlap (2025-08-26), as well as the separately labelled purposive pilot case. It should not be called an entirely untouched confirmatory sample. B/C avoid these identified cases; that alone does not erase retrospective design development.

B fills at most ten per original stratum. C uses explicitly revised allocations totalling 40; its extra cases go to S1/S3/S4 rather than pretending that S2 has ten eligible independent historical cases. Candidate sampling uses a fixed seed (20261105 plus stratum index) and an exact dynamic program to draw uniformly among feasible quota-sized date subsets. No LLM responses, coding outcomes, or residual magnitudes enter selection. The global sensitivities use a fixed date-only pseudorandom optimization objective, not the same uniform distribution. Neither method optimizes year coverage or claims representative inclusion probabilities across all historical weeks.

Arms are A, B, C-bare, C-ann, D. They start from A rather than being cumulative. Counts below assume **one response per week × arm × each of two LLMs**, one elicitation condition and no replicates. Pressure/retrieval conditions or repeated runs would add a separately specified budget.

| Design | S1/S2/S3/S4 | Stratified cases | Complete five-arm cases | Stratified responses, 2 models | Total with separate 5-arm purposive case |
|---|---|---:|---:|---:|---:|
| A: original | 10/10/10/10 | 40 | 26 | 316 | 326 |
| B: 8 weeks | 10/2/10/10 | 32 | 32 | 320 | 330 |
| B: 6 weeks | 10/3/10/10 | 33 | 33 | 330 | 340 |
| B: 4 weeks | 10/4/10/10 | 34 | 34 | 340 | 350 |
| C: 8 weeks | 13/2/13/12 | 40 | 40 | 400 | 410 |
| C: 6 weeks | 13/3/12/12 | 40 | 40 | 400 | 410 |
| C: 4 weeks | 12/4/12/12 | 40 | 40 | 400 | 410 |

In A, each of the two LLMs gives 40×2 + 26×3 = 158 stratified responses. The separate pilot adds five per model. There are 27 complete cases only if the purposive pilot is included; it is excluded from inferential case counts and rates. B/C totals with the pilot similarly add ten responses without adding an inferential week.

### Historical and net-long/template trade-offs

- **A:** retains 2006–2026, 18 calendar years in this draw and 16 pre-2015 stratified cases. A/B retain all ten original net-long controls; C-related comparisons retain only **four**, all in 2021–2022. Its C-complete strata are **4/2/10/10**. This sharply limits conclusions about quantitative evidence on net-long cases or earlier regimes. The earlier A/B-only cases are analytically valuable, not missing values to impute.
- **B at four weeks:** all 34 cases are paired across all five arms, with ten net-long controls and four S2 cases. The supplied within-stratum draw spans 2014–2026, 11 calendar years, with five pre-2015 cases (four S2 plus one S1); its long controls cover 2014–2017 and 2021–2022. This improves the complete-arm template check but drops 2006–2012 and the financial-crisis cases entirely. The globally spaced alternative has six pre-2015 cases and the same quotas; it is a distinct candidate, not an outcome-selected revision.
- **B at eight/six weeks:** 32/33 complete paired cases; S2 only two/three. They preserve the original categories but cannot preserve ten per category. Fewer cases need not make them less scientifically useful than C.
- **C:** at four weeks S2 is 10% of the sample rather than the original 25%; at eight weeks it is 5%. The extra net-long and recent-short cases change the pooled case mix and the question to performance on model-covered regimes. More cases do not recover broad pre-2015 representativeness. Its 12–13 net-long controls strengthen that particular check relative to A's C subset, but cannot supply early historical C evidence.

S4 eligible cases are all from August 2024 onward under the frozen threshold. Keeping the original S4 definition therefore concentrates that stratum in a recent regime under every option. None of the proposed sample sizes supports a claim to cover independent extreme-short episodes across the whole post-2015 period.

## Statistical comparisons and freezing decisions

The unit for each within-model arm contrast is the **week**, not the response. Five arms and two models do not turn 34 weeks into 340 independent observations. Report the two LLMs separately, with their paired case-level differences; any joint analysis must preserve within-week dependence. Two chosen LLMs are not a random sample of model families.

For A, the whole-sample A/B result and the 26-case model-arm result have different historical scopes. For B/C, every arm contrast can use the same stratified cases. Report strata-specific rates/discordant counts and the exact weighting of any pooled result; do not describe sample-mix averages as historical market-frequency estimates. Four S2 cases cannot support a stable pre/post-2015 interaction or broad claims about that era.

McNemar comparisons require paired cases and independent case pairs; pairing alone does not establish temporal independence. With four-week sampling, present paired descriptive effects and discordant counts first. Any inferential intervals/tests need a predeclared temporal dependence strategy and an eight-week sensitivity, rather than an iid p-value justified only by spacing. Calendar-block or episode-based resampling is a possible sensitivity, but results must acknowledge sparse episodes, especially S2; relabelling four close weeks as four independent regimes is invalid. No analysis of currently ungenerated responses has been conducted here.

Keep the purposive pilot qualitative, with no contribution to rates, significance tests, or sample-size claims. Preserve all model limitations: contemporaneous current CFTC OI; weak explanatory information; no identified strategies or private information; retrospective model selection; approximate uncertainty ranges.

Before main generation, record the chosen option, gap and its scope, endpoint, candidate date file hash, primary contrast/outcome, weights, dependency treatment, replicate/elicitation budget, placebo permutation, coding procedure, and treatment of prior-development overlaps. Human coding and the still-open arm-comparison decisions remain separate prerequisites from this sampling review. No existing design file was rewritten to imply those decisions have been made.

## Actual candidate dates

The complete 675-week eligible universe is supplied as CSV. Below are the actual candidate dates for all seven requested option/gap combinations, with the original sample unchanged. B/C global-gap alternatives have their own dated CSVs. These alternatives are not jointly added together.

### A_original

- **S1 (10):** 2006-09-26, 2007-07-17, 2009-12-08, 2011-03-29, 2013-01-08, 2013-09-03, 2021-01-19, 2021-05-18, 2021-11-09, 2022-01-11.
- **S2 (10):** 2008-07-22, 2009-04-28, 2009-10-06, 2010-03-16, 2010-05-25, 2010-11-16, 2011-03-15, 2011-08-09, 2014-09-30, 2014-11-25.
- **S3 (10):** 2016-06-14, 2017-02-21, 2018-05-01, 2018-09-18, 2019-11-12, 2022-11-22, 2023-01-24, 2023-04-18, 2024-01-02, 2026-03-10.
- **S4 (10):** 2024-08-13, 2024-10-08, 2024-12-10, 2025-04-08, 2025-06-03, 2025-08-26, 2025-10-21, 2026-02-03, 2026-04-07, 2026-07-14.
- **P (1):** 2025-09-02.

### B_4w

- **S1 (10):** 2014-01-21, 2015-02-17, 2016-07-12, 2017-08-22, 2017-09-26, 2021-02-09, 2021-03-09, 2021-04-13, 2021-07-20, 2022-04-19.
- **S2 (4):** 2014-09-30, 2014-10-28, 2014-11-25, 2014-12-23.
- **S3 (10):** 2015-07-14, 2015-10-20, 2016-01-05, 2016-10-25, 2017-04-18, 2017-08-29, 2019-06-11, 2020-10-20, 2020-12-29, 2025-04-22.
- **S4 (10):** 2024-09-24, 2024-10-29, 2024-12-10, 2025-04-08, 2025-07-01, 2025-08-19, 2025-11-10, 2026-01-06, 2026-04-21, 2026-07-28.

### C_4w

- **S1 (12):** 2014-03-04, 2016-07-12, 2016-08-23, 2016-11-15, 2017-08-22, 2021-02-23, 2021-04-20, 2021-05-18, 2021-06-22, 2021-10-19, 2022-04-19, 2022-05-17.
- **S2 (4):** 2014-09-30, 2014-10-28, 2014-11-25, 2014-12-23.
- **S3 (12):** 2015-06-23, 2015-08-04, 2015-09-01, 2015-11-24, 2016-01-26, 2016-11-01, 2017-04-18, 2017-08-29, 2019-06-11, 2020-10-20, 2020-12-29, 2025-04-22.
- **S4 (12):** 2024-09-03, 2024-10-15, 2025-04-08, 2025-05-06, 2025-07-15, 2025-09-16, 2025-11-04, 2025-12-30, 2026-01-27, 2026-04-28, 2026-07-14, 2026-10-13.

### B_6w

- **S1 (10):** 2014-02-25, 2016-07-12, 2016-08-30, 2016-11-22, 2017-07-03, 2021-02-09, 2021-05-04, 2021-06-15, 2021-08-03, 2021-11-16.
- **S2 (3):** 2014-09-30, 2014-11-11, 2014-12-23.
- **S3 (10):** 2015-07-14, 2015-09-01, 2015-10-13, 2016-01-05, 2019-10-22, 2020-03-10, 2020-08-04, 2023-02-21, 2023-06-27, 2026-06-02.
- **S4 (10):** 2024-10-01, 2024-12-03, 2025-04-29, 2025-06-10, 2025-09-09, 2025-11-25, 2026-02-03, 2026-04-21, 2026-06-09, 2026-08-11.

### C_6w

- **S1 (13):** 2014-02-11, 2014-04-22, 2014-09-09, 2016-08-30, 2016-11-15, 2017-07-11, 2017-08-22, 2021-01-26, 2021-03-23, 2021-06-22, 2021-09-14, 2021-10-26, 2021-12-14.
- **S2 (3):** 2014-09-30, 2014-11-11, 2014-12-23.
- **S3 (12):** 2015-06-16, 2015-08-18, 2015-09-29, 2015-12-08, 2016-05-24, 2019-04-30, 2019-07-02, 2020-05-12, 2020-09-15, 2022-09-13, 2023-12-26, 2024-05-14.
- **S4 (12):** 2024-09-03, 2024-10-22, 2024-12-10, 2025-04-29, 2025-06-24, 2025-08-05, 2025-10-28, 2026-01-06, 2026-04-21, 2026-06-16, 2026-08-11, 2026-10-13.

### B_8w

- **S1 (10):** 2014-02-11, 2014-07-01, 2014-09-02, 2016-07-12, 2017-07-03, 2021-01-26, 2021-07-06, 2021-08-31, 2021-11-02, 2022-04-19.
- **S2 (2):** 2014-09-30, 2014-11-25.
- **S3 (10):** 2015-09-01, 2016-02-09, 2016-06-21, 2017-11-21, 2018-11-20, 2019-05-07, 2020-09-22, 2020-12-29, 2022-05-31, 2026-09-08.
- **S4 (10):** 2024-10-01, 2025-04-15, 2025-06-24, 2025-08-19, 2025-11-25, 2026-01-27, 2026-04-14, 2026-06-09, 2026-08-18, 2026-10-27.

### C_8w

- **S1 (13):** 2014-02-04, 2014-04-29, 2014-08-19, 2016-08-23, 2016-11-15, 2017-07-11, 2021-01-19, 2021-06-15, 2021-09-07, 2021-11-02, 2022-01-04, 2022-03-15, 2022-06-21.
- **S2 (2):** 2014-09-30, 2014-11-25.
- **S3 (13):** 2015-06-30, 2015-09-08, 2016-01-26, 2016-03-22, 2019-03-05, 2019-05-14, 2020-01-28, 2022-08-02, 2023-09-05, 2024-01-02, 2024-11-26, 2025-02-04, 2026-05-05.
- **S4 (12):** 2024-08-13, 2024-10-08, 2024-12-03, 2025-05-06, 2025-07-15, 2025-09-23, 2025-11-18, 2026-02-03, 2026-04-07, 2026-06-09, 2026-08-18, 2026-10-27.

## Verification and files

240 pre-existing tracked/data files were hash-checked, with **zero changes**, including the original sample, raw pinned panels/manifests, v4 predictions and existing stimuli. New files are isolated under dated namespaces. The 28 targeted checks for spacing feasibility, v4 fitting, and materials passed. Small spacing examples were checked against exhaustive feasible subsets, including holiday/exact-gap boundaries and a cross-stratum global constraint.

The script is `scripts/review_sample_feasibility.py`; candidate rules and the decision log are in the new dated docs folder. The versioned raw source payloads, supporting panels, market extensions and full feature frame remain in the dated data folder, with hashes in `data_manifest.json`. Deliverables include the main updated flagship panel, extended frozen predictions, all eligible dates, all candidate samples, maximum-spacing witnesses, global-gap alternatives, counts and validation evidence. Nothing was committed or pushed as part of this review.
