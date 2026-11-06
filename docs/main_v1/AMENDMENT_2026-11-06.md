# Analysis amendment — 6 November 2026

**Adopted before main collection.** Primary comparison and outcome content are
specified below. Operational coding is pending independent human pilot validation.
The 32-week main sample, purposive extra, v4 estimator, and all main-v1/v1.1
prompts and data pins are unchanged. No main responses have been generated.

## Original specification retained

`docs/milestone2/codebook.md` v2.0 §3 calls **B3 ≥ 2** the “pre-registered primary
outcome”. That original document is preserved unchanged, with its hash in the
pilot preservation record. This amendment supersedes its primary-outcome and
elicitation decisions for main-v1.1; it does not retroactively rewrite them.
The term describes the project's documented specification; no external registry
registration has been verified here.

## Reason and disclosure

The twelve neutral v2 pilot replies received B3=0 under provisional Claude
coding. Their arm assignments and differences had already been seen when the
new composite was proposed. These were not independent human-validated scores:
the pilot used an older v2 model block, one model, and web search was observed
in five replies. They motivate concern about a narrow motive-share outcome;
they do not establish an annotation effect or predict the rates for four
consumer products using v4/main-v1.1.

The broader outcome is chosen to measure unsupported attribution, not to obtain
a smaller p-value. It may still have a floor effect. Fresh pilot/main outcomes
were not used to select this composite. The annotation itself explains several
boundaries, so an outcome limited to motive proportions would omit relevant
unsupported mechanistic/directional interpretations.

## Decisions now specified

1. **Primary contrast:** C-bare vs C-ann, separately for each of four product
   configurations. The table and model numbers are identical; the annotation
   differs. The effect is evaluated under the common v1.1 no-search instruction.
2. **Primary outcome (model-block attribution overreach):**
   `B2 >= 2 OR B3 >= 2 OR R >= 2`, one binary value per substantive response.
   Component definitions and threshold rules are specified in
   `CODEBOOK_v2_1_PILOT.md`. They are fixed in content now; human reliability
   validation remains outstanding.
3. **Common attribution overreach**, for ANY contrast involving A or B:
   `B2 >= 2 OR B3 >= 2`, identically on both sides. R is not applicable to A/B,
   not an observed zero. Never give the C side an extra way to cross the endpoint.
4. R applies to C-bare, C-ann **and D**, all of which display a model block. D
   is scored against its displayed placebo numbers without telling the coder it
   is placebo. The model-block composite can be used for C-bare vs D.
5. B3 ≥ 2 remains a **key secondary outcome** for C-bare vs C-ann, with its
   own four-product Holm family. Report all original component rates regardless
   of whether the new composite yields significance.
6. Main elicitation is **neutral only**, one first completed response per
   prompt/product: 640 inferential responses plus 20 qualitative responses = 660.
   Pressure and the optional historical supplement are deferred, not silently added.
7. Retain completed responses that visibly search in the primary product-level
   analysis; flag retrieval separately from citations. A search-excluded analysis,
   if shown, is descriptive and can suffer selection bias. No account-wide
   settings are changed. A no-search instruction is not a technical tool lock.

## Pilot rule and timing

Build a fresh three-case, five-arm, four-product pilot (60 responses), outside
the main/original samples and known development dates. Case selection uses
eligibility, position state and a fixed seed, never LLM replies or residual
magnitude. No pilot reply is pooled into the main sample.

Two human coders work independently with product/arm labels masked and a shared
numeric reference that withholds the annotation. Blinding is partial because
response content and the presence of numbers may reveal the condition. Every
non-zero code requires a quoted span; primary crossings must meet the explicit
unsupported-claim rules. Quoted annotation limitations are not errors.

Compute agreement on the binary composite directly and on each component's
binary crossing, alongside raw agreement and each coder's event counts. Target
κ ≥ 0.7; undefined κ from constant ratings is **indeterminate**, not an automatic
pass or an automatic scoring failure. Resolve that explicitly before main collection.

Inspect reliability and pooled prevalence with arm/product labels concealed.
The primary prevalence check pools C-bare/C-ann only, not all five arms where R
has different applicability. Pilot scripts do not report between-arm effects.
Do not change components or thresholds to produce more discordance/significance.
Operational clarifications must be dated; a substantive change requires a new
codebook version and fresh validation before main collection.

## Analysis and power

`ANALYSIS_v1_1.md` specifies the four-product testing families, paired effect
estimates, confidence intervals, missing/refusal handling and dependence
sensitivity. Exact McNemar assumes independent week pairs; eight-week
within-stratum spacing does not prove this assumption. Keep the purposive case
out of inferential rates/tests. The same weeks across products do not become
128 independent historical cases.

At the first Holm cutoff (0.0125), exact two-sided McNemar p-values are 0.015625
for 7:0 discordances, 0.0078125 for 8:0, and 0.01171875 for 10:1. These are
significance boundaries, not statistical power. Subsequent Holm cutoffs are
0.05/3, 0.05/2, and 0.05 after earlier rejections.

Power scenarios are generated before collection from assumed discordance
probabilities (`docs/pilot_main_v1_1/power_scenarios.csv`). They assume independent
weeks and use a fixed 0.0125 cutoff, not the full joint Holm procedure. Moderate
effects may be missed. A nonsignificant result does not establish equivalence;
report counts, paired differences and intervals. No significant pilot contrast
is a prerequisite to the main study.
