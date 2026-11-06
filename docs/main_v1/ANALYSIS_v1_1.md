# Main-v1.1 analysis specification — 6 November 2026

Status: content specified before fresh pilot/main responses; operational
human coding still pending validation. Sample and materials are unchanged.

## Primary question, estimand and four-test family

Within each product: does adding the annotation change model-block attribution
overreach? Compare C-bare vs C-ann using `B2>=2 OR B3>=2 OR R>=2`.

The analysis unit is the historical week. Use up to 32 substantive matched
week pairs per product; exclude the purposive 2025-09-02 case from rates,
intervals and tests. Do not treat the four products as 128 independent weeks,
or the 660 collected replies as independent observations. Named product/mode
comparisons do not identify the causal effect of paying for a subscription.

For each product, report the full 2×2 paired table:

- n00: both below the crossing threshold;
- b=n10: overreach in C-bare only (annotation improvement);
- c=n01: overreach in C-ann only (annotation worsening);
- n11: both overreach.

Report both arm rates and **delta = annotated rate − bare rate = (c−b)/n**;
negative values favour annotation. Test with exact two-sided McNemar (binomial
test among discordant pairs). No discordances: p=1, no evidence of a difference,
not proof of equivalence or evidence that the annotation was ignored.

Apply Holm to the four primary product p-values at familywise α=0.05. Sorted
cutoffs are .0125, .05/3, .025 and .05, proceeding only while earlier tests
reject. If a product has no scoreable pairs, report it unestimable and use p=1
for family bookkeeping; do not shrink the planned family to make rejection easier.

## Intervals and temporal dependence

Report a conservative 95% paired risk-difference interval: form 97.5%
Clopper-Pearson bounds [Lb,Ub] and [Lc,Uc] for each discordant-cell probability
using n matched weeks, then project to [Lc−Ub, Uc−Lb]. Bonferroni coverage for
the two probabilities gives at least 95% coverage for the difference under
independent week pairs. These intervals are conservative, per-product intervals;
they are not four-product simultaneous intervals. They are not obtained by
incorrectly treating the two arms as independent samples. All-zero observations
must not produce a spurious [0,0] uncertainty interval.

Exact McNemar and those intervals assume independent week pairs. Eight-week
within-stratum spacing is a design precaution, not proof. As a prespecified
descriptive sensitivity, resample **calendar-quarter clusters** within product
(5,000 draws, seed 20261106), preserving the two arm responses for each week.
Report cluster count and percentile interval, with sparse-cluster limitations.
If resampling is degenerate/no variation, mark the interval unestimable rather
than presenting zero width as certainty. This sensitivity is not a replacement
confirmatory p-value and does not establish independent market episodes.

S2 has two late-2014 cases. Report stratum counts/differences descriptively;
do not test a broad pre/post-2015 interaction or claim historical representativeness.

## Secondary analyses

1. **B3>=2 alone**, C-bare/C-ann within each product: report paired tables,
   differences/intervals and a separate, explicitly secondary four-product Holm
   family. This preserves the original documented outcome; it cannot rescue an
   unsuccessful primary composite after the fact.
2. C-bare/D using the model-block composite, and A/C-bare and A/B using the
   common B2/B3 composite on BOTH sides: descriptive/exploratory paired effects,
   not additional confirmatory successes. An absence of C/D difference is
   ambiguous about how the model output was used.
3. Component B2, B3 and R rates/quoted examples, plus response lengths and
   missing/refusal/retrieval counts. Do not merge distinct codes into an ordinal
   maximum and claim automatically greater power. New numerical/range codes
   are not promoted into the primary composite after observing results.

## Retrieval, missing responses and deviations

The identical instruction is “Please answer without using web search.” Keep
account-wide settings unchanged as requested, and record actual visible state
and model/mode per run. Gemini retrieval has not been technically disabled;
a ChatGPT automatic-search switch exists, but its state is not silently changed
for this protocol. Absence of visible search is not proof of no retrieval.

Retain searched completed responses in the primary product-level analysis;
record visible retrieval separately from citations. A search-excluded analysis
is descriptive and may condition on behaviour caused by the arm.

Retain the first completed response, including a refusal. Technical failures
may be retried with an attempt log, never because an answer is inconvenient.
Keep original attempts. Record unscoreable/refusal counts and only analyse
complete scoreable pairs for an endpoint. A substantive statement of limits is
not a refusal. Give the planned denominator (32), completed pairs and exclusion
reasons. Do not impute missing/refusal responses as safe or overreaching.

## Precision before collection

Significance boundaries: 7:0 discordances p=.015625; 8:0 p=.0078125;
10:1 p=.01171875. Eight same-direction discordances suffice for the first Holm
cutoff; this is not a power calculation. Power depends on joint discordance
probabilities and the dependence structure across weeks/products.

The pilot builder writes exact enumerated scenarios for n=32 at fixed α=.0125:
(.15,.05), (.25,.05), (.30,.10), (.35,.05) for probabilities (bare-only, ann-only).
They are hypothetical, not estimated from pilot arm differences, and not full
joint Holm power. Moderate effects may be missed. A nonsignificant result is
not evidence of no effect; zero observed crossings are limited to these cases,
products and instructions.

Implementation: `src/hfpos/llm/experiment.py`. References:
[exact McNemar](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html),
[Holm procedure](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html),
[Clopper-Pearson intervals](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html).
