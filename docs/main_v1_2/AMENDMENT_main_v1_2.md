# Amendment main-v1.2 — three products, arms A / C-bare / C-ann (DRAFT, 6 Nov 2026)

**Status: draft for team approval. It takes effect only once the team signs off below and
before any main reply is collected.** It supersedes the product, arm, effort and coding
sections of `docs/main_v1/FREEZE.md` §5/§7, `ANALYSIS_v1_1.md` and the v2.3 codebook
amendment where they conflict. The sample, data pins and prompt text are unchanged.

Build: `python scripts/freeze_main_v1_2.py` → `docs/main_v1_2/` (hash-pinned in
`manifest_v1.2.json`; test `tests/test_main_v1_2.py`).

## 1. What changes

| Item | main-v1.1 | **main-v1.2** |
|---|---|---|
| Products | ChatGPT Free, ChatGPT Plus, Gemini Free, Gemini on Google AI Pro | **ChatGPT Plus (GPT-6 Sol), Gemini on Google AI Pro (Gemini 4 Argon), Claude Pro (Opus 5.5)** |
| Arms | A, B, C-bare, C-ann, D | **A, C-bare, C-ann** |
| Prompt text | v1.1 (with the no-search line) | **unchanged** (byte-identical to v1.1 for these arms) |
| Weeks | 32 inferential + 1 purposive (2025-09-02) | unchanged |
| Replies | 165 × 4 = 660 | **99 × 3 = 297** |
| Effort | not fixed (pilot used High on Plus and Argon) | **each app's standard thinking level, fixed per product for the whole run** |
| Codebook | v2.1, then v2.2 | **v2.3** (`docs/main_v1/CODEBOOK_v2_3.md`) |

## 2. Why, and what the pilot did and did not decide

**Products.**
- **Rule:** each vendor's best model included in its standard ~US$20/month consumer plan, used in the chat app in the same collection window. The comparison is between products, not between underlying models or tiers.
- **Fable 5.1:** Anthropic's top model needs usage credits on Claude Pro, so it is outside the rule. This is disclosed.
- **Why a single tier:** using one tier across three vendors removes the tier-versus-vendor confound the course feedback raised.
- **Pilot disclosure:** the free tiers and the vendor choice were revisited after the 60-reply pilot.
  - Both ChatGPT products had almost no overreach in any arm.
  - Both Gemini products overreached often.
  - So vendor, not tier, carried most of the variation.
  - A third vendor was added to test how far that generalises. This decision was informed by pilot outcomes and is reported as such.

**Arm B dropped (redesign, informed by the pilot).**
- B supplies basis-trade context. Unprompted arm-A pilot replies already invoked the basis trade in 10 of 12 cases, so the manipulation is largely redundant for these products.
- Descriptively, A and B overreach rates were similar: 6/12 vs 4/11 (Claude) and 7/12 vs 7/11 (Codex).
- Only 1 of 11 paired A–B comparisons was discordant per coder, in opposite directions.
- Eleven pairs cannot establish "no effect". The decision rests on redundancy plus the collection budget.

**Arm D dropped (budget).**
- D is a placebo check on whether replies track the actual residual. It is secondary to the primary contrast.
- With 32 weeks it has little power.
- Dropping it is a scope decision for time and usage caps, not a pilot result.

**Arms kept.**
- C-bare vs C-ann is the primary comparison (unchanged).
- A is the no-model baseline. A vs C-bare is a secondary contrast.

## 3. Analysis (updates `ANALYSIS_v1_1.md`)

- **Primary:**
  - Per product, C-bare vs C-ann on the 32 inferential weeks.
  - Outcome: model-block attribution overreach, B2 ≥ 2 OR B3 ≥ 2 OR R ≥ 2.
  - Test: exact two-sided McNemar, with Holm across the **three** products.
  - With 32 pairs, the smallest Holm threshold (0.05/3 = 0.0167) needs at least **7 discordant weeks all one way** (p = 0.0156). Report discordant counts, paired differences and intervals as well as p-values. A non-significant result is not evidence of no difference.
- **Secondary:**
  - A vs C-bare on the common composite (B2 ≥ 2 OR B3 ≥ 2), used identically on both sides.
  - B3 ≥ 2 alone (the original outcome).
  - Each component separately.
- **Descriptive:** overreach rates per product × arm, including the purposive week, which is reported separately and not in inferential tests.
- Missing data, refusals and temporal-dependence sensitivity: as in `ANALYSIS_v1_1.md`.

## 4. Collection rules (detail in `COLLECTION_PROTOCOL.md`)

1. **One fixed setting per product for the whole run.**
   - Select the named model and the app's standard thinking level.
   - Use a new temporary/incognito chat for every prompt, with memory off.
   - Paste the prompt file exactly. Add nothing.
2. **The first completed reply counts.** Never resend because of what a reply says.
3. **Usage caps:** pause until the reset. Never switch model or effort to continue.
4. **Fallback models:** a reply produced by a different model than the one selected (visible label) is logged `fallback_model`, kept, and resent after the reset as a new attempt. The same applies to app errors.
5. **Record on every attempt:**
   - the visible model label and thinking setting;
   - temporary-chat status;
   - visible search/citations;
   - times;
   - account.

   Replies that searched despite the no-search line are kept and flagged, as in v1.1.
6. **Order:** collect in each runsheet's seeded order (the order is pre-randomised across weeks and arms).

## 5. Coding

- **Primary:** two human coders, codebook v2.3, masked packets (no product, arm or week labels; random order), independent, before any discussion.
- **Reliability:** κ on the composite and each component, plus raw agreement and prevalence. The κ ≥ 0.70 target is as before.
- **Before trusting the main codes:** v2.3 has only in-sample machine agreement so far. The first coded batch of main replies (for example 30 masked replies spanning all products) serves as its fresh test. Report it separately.
- **AI check coders are labelled as machine coding and never replace human codes.** No product's replies are machine-coded by the same vendor's model (Claude replies are not coded by Claude, GPT replies not by an OpenAI model).
- **Blinding limit:** team members who collected replies have seen some of them. Masking reduces but does not remove this. Disclose it.

## 6. Unchanged

- The sample;
- the data pins;
- model v4.0;
- the prompt wording, including the no-search line;
- the neutral elicitation;
- the composite definitions;
- B3 ≥ 2 as key secondary;
- all earlier files and pilot data.

## Sign-off

| Name | Agree (Y/N) | Date |
|---|---|---|
| Lip Jun Ting | | |
| Tia Elizabeth Ansari | | |
| Upadhye Neeti Rahul | | |
| Chua Jun Yu Xavier | | |
