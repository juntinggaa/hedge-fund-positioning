# Amendment main-v1.3 — 20 weeks, three products, arms A / C-bare / C-ann (DRAFT, 6 Nov 2026)

**Status: draft for team approval. It replaces the unsigned main-v1.2 draft
(`docs/main_v1_2/`, kept unchanged as history) and must be signed before any main
reply is collected.** v1.3 is identical to v1.2 except for the three changes below,
so read `docs/main_v1_2/AMENDMENT_main_v1_2.md` §2, §4 and §5 for:
- the product rule;
- why B and D were dropped;
- the collection rules;
- coding.

Build: `python scripts/freeze_main_v1_3.py` → `docs/main_v1_3/` (hash-pinned in
`manifest_v1.3.json`; test `tests/test_main_v1_3.py`). Check collected files with
`python scripts/ingest_main_v1_3.py docs/main_v1_3/responses`.

## 1. Changes from v1.2

| Item | v1.2 draft | **v1.3** |
|---|---|---|
| Weeks | 32 inferential + 1 purposive | **20 inferential**: a seeded uniform draw within each frozen stratum, S1 6 / S2 2 / S3 6 / S4 6 (seed 20261108). Purposive week 2025-09-02 dropped |
| Replies | 99 × 3 = 297 | **60 × 3 = 180** |
| Collection order | a separate random order per product | **one seeded order shared by all products** (seed 20261107), so `GPT-k`, `GEM-k` and `CLA-k` are the same prompt |

**Unchanged:**
- the prompt text (byte-identical to v1.1);
- the three products and the model rule;
- arms A, C-bare and C-ann;
- the standard effort level;
- codebook v2.3;
- the coding and collection rules.

## 2. Why

**Time and focus.**
- The milestone is due 8 Nov.
- Following course guidance, the emphasis shifts from collecting many outputs to interpreting the replies:
  - what kinds of overreach occur;
  - where each product draws or blurs the line between observed, inferred and merely plausible;
  - how the annotation changes the wording.

**How the weeks were chosen.**
- The weeks are a seeded random subset of the already-frozen stratified sample.
- They were chosen without looking at any main-week LLM output (none exists) and without using pilot results.
- All of S2 is kept (it has only 2 weeks).
- Subsetting preserves the within-stratum spacing of at least 56 days.

## 3. Consequences for the analysis

- **Primary contrast unchanged:** C-bare vs C-ann per product, exact two-sided McNemar, Holm across three products.
- **Power with 20 paired weeks:**
  - The smallest Holm threshold (0.0167) still needs at least **7 discordant weeks all one way**.
  - That is now 35% of weeks.
  - Only a large effect can reach significance.
- **The tests are therefore reported as supporting evidence.** The main results are:
  - descriptive rates per product × arm;
  - discordant-pair counts and paired differences with intervals;
  - a qualitative analysis of the replies, with verbatim examples for each code and each product.

  A non-significant test is not evidence of no difference.
- **Secondary and descriptive contrasts** as in v1.2 §3. The purposive week is no longer part of the run.

## Sign-off

| Name | Agree (Y/N) | Date |
|---|---|---|
| Lip Jun Ting | | |
| Tia Elizabeth Ansari | | |
| Upadhye Neeti Rahul | | |
| Chua Jun Yu Xavier | | |
