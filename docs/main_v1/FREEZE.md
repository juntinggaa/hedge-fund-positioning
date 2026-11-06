# Main experiment v1: frozen sample and materials

> **Current version: main-v1.1 (2026-11-06)**, see §7. Use
> `prompts_main_v1.1.jsonl` for collection. The main-v1 files below are kept
> unchanged as the base that v1.1 is derived from.

**Materials frozen 2026-11-05, before any main-experiment response exists.** This
fixes *which weeks* and *which prompts*. The dated analysis amendment in §8
specifies the primary comparison, composite and analysis; independent human
pilot validation of the operational codebook remains required before the main run.

```
python scripts/freeze_main_v1.py       # rebuilds docs/main_v1/ byte-for-byte from pinned inputs
pytest tests/test_main_v1.py           # checks hashes, strata, spacing, placebo, prompts
```

## 1. Amendment to the Milestone 1 sampling plan

**What changed.** The registered sample (`docs/milestone1/sample.csv`: 40
stratified weeks, 10 per stratum, 8-week within-stratum spacing, plus purposive
2025-09-02) is replaced for the main experiment by **Option B, 8-week spacing**:
32 stratified weeks (S1 10, S2 2, S3 10, S4 10) plus the same purposive week.

**Why.** Arms C-bare, C-ann and D need a genuine out-of-sample model estimate
and at least 52 earlier out-of-sample errors to build the range. With model v4
that first happens on **2013-11-26**. Only 27 of the original 41 weeks qualify,
and they are unevenly spread across strata: S1 4/10, S2 2/10. The amendment
gives every inferential week all five arms. The decision rests on model
coverage, a design property. **It was not made on the basis of any LLM
response, coding outcome or residual size**, and none existed for these weeks.

**How the weeks were drawn** (`scripts/review_sample_feasibility.py`, candidate
file `reports/sampling_review_2026-11-05/B_8w_dates.csv`):
- Same strata definitions as Milestone 1. The extreme-short cut-off is frozen at
  −0.37567236606810045 and was not recomputed.
- Pool: weeks with valid model output, excluding the six pilot-development
  weeks (2023-07-11, 2025-02-18, 2025-06-17, 2026-06-30, 2026-08-25, 2026-09-01)
  and the purposive week.
- Spacing: the original 8 weeks (56 days), applied within each stratum, exactly
  as the original sampler does. Across strata the closest pair is 4 weeks apart
  (2014-09-02 S1, 2014-09-30 S2).
- Seed 20261105 + stratum index; uniform over feasible quota-sized subsets.
- S2 can supply at most 2 weeks at this spacing (all 15 eligible S2 weeks fall
  in Sep–Dec 2014). S2 is therefore a **late-2014 check**, not coverage of the
  pre-2015 era.

**What is lost.** No week before 2014. That removes the financial crisis and the
2006–2012 cases. S4 is entirely August 2024 onward. Conclusions about the model
arms apply to 2014–2026. The optional A/B supplement (§4) partly restores
historical coverage for the arms that need no model.

## 2. Data and model pins

| item | file | check |
|---|---|---|
| CFTC 10Y panel, append-only to 2026-10-27 (released 2026-10-30) | `data/raw/sampling_review_2026-11-05/cftc_tff_ust_10y.parquet` | first 1,057 rows equal the pinned panel exactly; hash in `manifest.json` |
| model v4.0 predictions, frozen estimator extended 7 weeks without refitting | `data/raw/sampling_review_2026-11-05/weighted_104_extended.parquet` | equals frozen `data/processed/model_v4/weighted_104.parquet` on all 720 shared weeks |
| v4 model card (annotation text) | `docs/model_v4/materials/model_card_v4.json` | unchanged; performance text still describes the 720-week evaluation |
| all other extended inputs | `reports/sampling_review_2026-11-05/data_manifest.json` | every listed hash re-verified by the freeze script |

The sample includes 2026-09-08 (S3), already the original pinned endpoint, and
2026-10-27 (S4), an added report requiring the extension. Treat the seven
extension weeks as a small check made after model selection, not as confirmation.

## 3. Materials

- `sample.csv`: 33 weeks (32 inferential and 1 purposive, qualitative only).
- `stimuli.csv`: model numbers per week. The range uses only strictly earlier
  errors; percentiles are stated in both directions.
- `prompts_main.jsonl`: 33 × 5 arms = **165 prompts**, so **330 responses**
  with two LLMs. A and B are byte-identical to the legacy generator. C-bare,
  C-ann and D use the v4 block. C-ann uses the v4 annotation.
- **Placebo amendment.** Applied to this sample, the v4 permutation (seed
  20261104) left **2 weeks showing their own genuine residual** in arm D. It is
  replaced by a **seeded derangement**: the same generator, re-drawn until no
  week keeps its own residual (4 draws). The decision is outcome-blind. The
  source week of every placebo is in `stimuli.csv`.

## 4. Optional historical A/B supplement (not yet adopted)

- `supplement_AB_optional.csv`: the 14 original Milestone 1 weeks without model
  coverage (2006–2013, S1 and S2).
- `prompts_supplement_AB_optional.jsonl`: 14 × {A, B} = 28 prompts, or **56
  responses** with two LLMs.
- If run, it is descriptive only. It is never pooled with the main inferential
  sample, and it is never used to compare against model-arm rates.
- **Decided 2026-11-06:** deferred; not included in the 660-response main scope.
  Adding it later requires a dated scope decision, not selection by main results.

## 5. Decisions and outstanding validation (updated 2026-11-06)

| item | options / notes | decision |
|---|---|---|
| Research question and **primary comparison** | C-bare vs C-ann: does the annotation change unsupported attribution? Separately within each product | **decided 2026-11-06**, §8 |
| Primary outcome | B2 ≥ 2 OR B3 ≥ 2 OR R ≥ 2 for model-block comparisons; B3 ≥ 2 retained as key secondary. Any A/B contrast uses B2/B3 on both sides | **content specified 2026-11-06; human reliability pending**, §8 |
| Products | four product configurations (§7) | **decided 2026-11-06** |
| Retrieval | No-search instruction, not a technical block. Keep account settings unchanged; record actual controls/visible retrieval. Retain searched completed replies in primary analysis | **decided 2026-11-06**, §8; ChatGPT has an automatic-search switch; no Gemini equivalent found in inspected settings |
| Elicitation | neutral only; pressured condition deferred | **decided 2026-11-06** within the 660-response scope |
| Replicates | one first completed response per prompt/product; retain refusals; log technical retries | **decided 2026-11-06** |
| Coding | two independent humans, masked labels and shared numeric references; composite/component binary κ target ≥0.7 plus raw agreement/prevalence; undefined κ is indeterminate | **validation pending**; `CODEBOOK_v2_1_PILOT.md` |
| Analysis | unit = week; exact two-sided McNemar per product, Holm across four primary tests; paired differences/intervals and calendar-quarter sensitivity | **specified 2026-11-06**, `ANALYSIS_v1_1.md` |
| A/B supplement | §4 | **deferred 2026-11-06** |

## 6. Before the main run

1. Follow the dated §8 analysis specification and the 60-run fresh pilot plan
   in `docs/pilot_main_v1_1/`. No main responses before human validation.
2. Use weeks **outside** the main/original samples and known development cases.
   Use v1.1 wording with recorded retrieval, not a claimed consumer-app lockdown.
   Two human coders independently code masked response packets.
3. Review composite/component binary agreement and pooled C-bare/C-ann
   prevalence without pilot arm effects. If reliability is inadequate, clarify,
   date/version the rules and validate on fresh responses. Undefined κ from
   constant ratings is indeterminate, not an automatic pass. Record the final
   validation decision before main collection; do not change the composite to
   increase significance.
4. Run the main responses: 660 with four products, plus 112 if the supplement
   is adopted. Record search use for every response.

No main-experiment response has been generated (`manifest.json`:
`responses_generated: 0`).

## 7. Amendment main-v1.1 (2026-11-06): four products and a no-search line

**Products.** Each prompt goes to four product configurations. Each is reported
separately as a product, not as a pure model.

| vendor | free | paid |
|---|---|---|
| OpenAI | ChatGPT Free (record the mode actually available) | ChatGPT Plus (record the model label) |
| Google | Gemini Free (record the model label; Auto if that is all that is offered) | Gemini on a Google AI Pro plan (record the model label) |

- Pin a named model wherever the app allows it, and record the label shown on
  **every** response.
- **What the four products can and cannot show:**
  - Agreement across them shows an arm effect is not one product's quirk.
  - Free vs paid differences are **not** a causal effect of paying, because
    model, routing, features and limits all differ.
  - The unit of analysis stays the **week** (32 inferential weeks). More
    products do not add independent cases.

**No-search line.** Every prompt in every arm now ends with one extra
paragraph: *"Please answer without using web search."*
- Why: searching changes the evidence the model sees. Correction recorded
  2026-11-06: ChatGPT has an automatic Web search switch; no equivalent was found
  in the inspected Gemini settings. The instruction is used consistently while
  keeping account settings unchanged; it is not described as an enforced lock.
- The line deliberately says nothing like "use only the information provided".
  That would cue caution and forbid background knowledge, which is the channel
  through which overreach happens.
- It is held constant across all arms. It may interact with arm content, so
  effects apply to the v1.1 instruction condition, not necessarily earlier
  pilots. Search use is recorded per response because apps may ignore the request.
- Consequence: v1.1 prompts are no longer byte-identical to the legacy A/B
  prompts or the earlier pilots. Each v1.1 row keeps its `v1_prompt_sha256`, so
  the only difference is checkable.

**Files.** `prompts_main_v1.1.jsonl` (165 prompts, 660 responses) and
`prompts_supplement_AB_optional_v1.1.jsonl` (28 prompts, 112 responses if
adopted), with hashes in `manifest_v1.1.json`. Rebuild with
`python scripts/freeze_main_v1_1.py`.

**Updated by §8:** comparison/outcome content, retrieval handling, neutral-only
elicitation, one completed response and deferred supplement are now specified.
Human coding reliability and the final operational validation decision remain open.

## 8. Analysis amendment and fresh pilot (2026-11-06)

`AMENDMENT_2026-11-06.md` preserves the original documented B3-only primary
outcome and discloses that pilot arm differences had been seen before the new
composite was proposed. B3 ≥ 2 remains a key secondary outcome. Primary C-bare
vs C-ann uses the model-block composite; any A/B contrast uses the common B2/B3
composite identically on both sides. R applies to D as well as the C arms.

The composite content is specified before new pilot replies, with human
validation pending under `CODEBOOK_v2_1_PILOT.md`. `ANALYSIS_v1_1.md` specifies
four-product Holm correction, exact McNemar, paired effects/intervals, missing
and refusal handling, and temporal dependence sensitivity. The power examples
are hypothetical fixed-cutoff calculations, not an estimate of actual joint
Holm power or a promise of sensitivity to moderate effects.

`scripts/build_pilot_main_v1_1.py` prepares three fresh cases × five arms × four
products = **60 pilot replies planned**, with source hashes, a 60-run schedule,
seeded placebo derangement, numeric coder references and two separate blank
coding templates. It calls no LLM and does not change the main sample/prompts.
`scripts/validate_pilot_main_v1_1.py` prepares blinded packets after collection
and reports pooled reliability without pilot arm/product outcome contrasts.
