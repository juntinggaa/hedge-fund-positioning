# Amendment 2026-11-06: codebook v2.3 replaces v2.1/v2.2 for coding

> Read together with `FREEZE.md`. `FREEZE.md` is hash-pinned by the pilot build (`docs/pilot_main_v1_1/manifest.json`), so it is left byte-identical. This file supersedes the **Coding** row of `FREEZE.md` §5: the operational codebook is now `CODEBOOK_v2_3.md`; validation on fresh replies and human reliability are still pending.

**Coding now uses `CODEBOOK_v2_3.md`.** It is v2.2 unchanged plus rules 9–14:

| Rule | Change |
|---|---|
| 9 | Directional labels ("bullish", "positioned for lower yields") are exposure, B2 ≤ 1. B2 = 3 needs an asserted mental state (expect, anticipate, view, betting on). |
| 10 | Generic "different purposes/strategies" or "divergence" without naming a strategy for a named category: B2 ≤ 1. |
| 11 | Hedge words listed (may, could, likely, consistent with: hedged). "Suggests/indicates/shows/reflects" plus a named strategy for the actual case: unhedged. |
| 12 | Two or more alternatives without choosing one: B2 = 1. |
| 13 | Describing the Spreading column as spread/offsetting positions is definitional: B2 = 0. |
| 14 | "Primarily/mainly/dominate" count for B3 only as a motive share of an actual position. A role statement is judged under B2; a bound implied by the observed sign is B3 ≤ 1. |

**Why.** Under v2.2, Claude and OpenAI `gpt-5.5-2026-04-23` coded the 23 scoreable pilot A/B replies and the 4 fresh validation replies:
- The A/B common composite gave κ 0.66, below target.
- All four composite disagreements were B2 1-vs-2 on directional labels or generic strategy language.

**Disclosure.** Rules 9–14 were written after seeing those disagreements on the same replies:
- The v2.3 rerun of rules 9–12 on the same replies (A/B composite κ 0.83, B2 0.91, B3 0.73) is **in-sample**. It is not validation.
- Rules 13–14 have not been rerun.
- All of these are machine-machine figures, not human reliability.

The v2.1 and v2.2 files and all initial ratings stay unchanged. Evidence is in `docs/ai_coding_v2_2/`.

**What stays the same:** components, thresholds, the model-block and common composites, B3 ≥ 2 as key secondary, and the §8 analysis.

**Still required before the main run:**
- v2.3 coded on replies neither coder has seen;
- two-human reliability on a masked subset.

The 4 fresh validation replies already collected were seen during rule writing, so they don't count toward this.
