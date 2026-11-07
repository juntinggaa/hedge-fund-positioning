# Amendment 7 Nov 2026: Gemini effort level and dataset assembly (DRAFT)

**Status: draft for team approval. It must be signed before any main reply is coded.**
It changes which collected Gemini replies are analysed. It changes no prompt, arm,
week, order, codebook rule or outcome. No reply has been coded, and no code or
outcome was looked at in reaching this decision.

## 1. What happened

| Product | Model shown | Effort | Collected | By |
|---|---|---|---|---|
| ChatGPT Plus | GPT-6 Sol (see §4) | High | 60/60 | Jun Ting |
| Claude Pro | Opus 5.5 | High | 60/60 | Jun Ting |
| Gemini (Google AI Pro) | Gemini 4 Argon | **Low** | 60/60 | teammates |
| Gemini (Google AI Pro) | Gemini 4 Argon | High | 16/60 (GEM-001, 045–052, 054–060) | Jun Ting |

The high-effort Gemini run stopped at a usage cap. A separate, complete run of all 60
Gemini prompts had already been made by teammates at low effort.

## 2. Decision

1. **The main Gemini data are the 60 low-effort replies**, all from the teammates' run.
2. **Low-effort and high-effort replies are not mixed** within Gemini. The 60 prompts are in one shuffled order, so each week's three arms are spread across the IDs. Patching only GEM-002 to 044 with low-effort replies would leave 14 of the 20 weeks with arms at different effort levels. The within-week A / C-bare / C-ann contrast would then be confounded with effort. Mixing would also breach the collection rule "never switch model or effort to keep going".
3. **The 16 high-effort Gemini replies become a descriptive effort check.** They are not part of the main analysis.
   - The 16 pairs (same prompt, high vs low) are coded masked, mixed in with the main replies.
   - Report how often the composite code agrees between the two efforts, plus discordant counts. No test is run on this check.
   - GEM-045 is flagged: the cap was reached around the time of that reply, so its actual effort is unknown. GEM-053 is excluded, because its effort is unknown and it was never saved as canonical.
   - Files: `effort_check_GEM_high/`, pairing in `effort_check_GEM_high/PAIRS_PRIVATE.csv`.
4. ChatGPT and Claude are unchanged: one effort level (High) throughout.

## 3. Consequences for the analysis

- **The primary within-product contrasts are unaffected.** C-bare vs C-ann and the contrasts against A each compare arms collected at a single effort level within a product.
- **Cross-product comparisons gain a caveat.** Gemini differs from the other two products in effort level as well as vendor, so any statement that one product overreaches more than another must say so. The effort check in §2.3 gives some indication of how much effort changes the codes. It is too small to remove the caveat.
- The protocol's "standard effort level" is recorded as achieved for ChatGPT and Claude (High). For Gemini it was not achieved: Low was used, which is a deviation.

## 4. Other provenance gaps to disclose (found while assembling)

- **ChatGPT model label.** In 42 of 60 ChatGPT replies, the log says the model picker was not shown in temporary chat. The model is therefore taken from the settings chosen before the temporary chat opened, not from a label in the UI. Eight replies log "GPT-6". GPT-001 to 010 have no log.
- **Missing metadata.**
  - GPT-001 to 010 and CLA-011, 037, 038 and 043 have no collection log.
  - All 60 low-effort Gemini rows have no log in the repo.
  - Their runsheet fields are blank and must be filled by the collector from memory, chat history or screenshots. Any field that cannot be recovered is left blank, with a note.
- **Missing screenshots.** 11 ChatGPT, 20 Claude and all 60 low-effort Gemini replies have no screenshot (list from `python scripts/ingest_main_v1_3.py docs/main_v1_3/responses`). These are reported as missing; they are not reconstructed.

## 5. Files

- `scripts/assemble_responses_v1_3.py` copies replies, screenshots and logged fields into `docs/main_v1_3/responses/<CODE>/`, the layout the checker expects. It never moves or edits a source file. Source paths and sha256 hashes are in `responses/PROVENANCE.csv`.
- Original files stay in `main prompt outputs/`.

## Sign-off

| Name | Approve (Y/N) | Date |
|---|---|---|
| Lip Jun Ting | | |
| Tia Elizabeth Ansari | | |
| Upadhye Neeti Rahul | | |
| Chua Jun Yu Xavier | | |
