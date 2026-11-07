# Technical attempt log: pilot-main-v1.1 collection (6 Nov 2026)

Recorded separately from responses.jsonl. Only completed, retained replies appear there. No attempt below was regenerated for content reasons.

| Time (UTC, approx.) | Run | Surface | Event | Action |
|---|---|---|---|---|
| 2026-11-05 ~17:38 | PV11-016 (Gemini Free, D) | gemini.google.com | Reply captured; prompt matched numerically | Kept |
| 2026-11-05 ~17:40 | PV11-017 (Gemini Free, B), attempt 1 | gemini.google.com (new chat) | Submitted text was the 2-word string "D (placebo)" instead of the frozen B prompt. The clipboard had been staged with the correct prompt hash (verified) beforehand. Cause not determined. A stray Gemini chat ("Placebo Question Context Request") now exists in the Junting account history | Discarded; no reply used. Not deleted (would need approval) |
| 2026-11-05 ~17:41 | PV11-017, attempt 2 | gemini.google.com (new chat) | Composer checked by screenshot before sending: full frozen prompt present | Sent; reply kept |
| 2026-11-05 ~17:12 | PV11-013 | chatgpt.com Temporary Chat | Copy-response button wrote the user prompt to the clipboard (4 attempts) | Response recovered by select-all and copy; span extracted |
| 2026-11-05 ~17:16 | PV11-014 | chatgpt.com | Copy-response button again returned the prompt | Same recovery |
| 2026-11-05 ~17:17 | PV11-015 | chatgpt.com | First capture taken mid-stream | Discarded; recaptured after completion |
| 2026-11-05 17:12 onward | PV11-016 to 045 (Gemini) and PV11-021 to 050 (ChatGPT Plus) | both | Capture by select-all and copy, not the markdown copy button. Replacement characters appear in 10 replies | Flagged in technical_notes |
| Earlier session (time not recorded) | PV11-002 | chatgpt.com (earlier session, Jingyen) | Earlier element-ID errors; reply recovered from composer read-back | Still UNVERIFIED (partial sentence match against AX file) |
| Earlier session (time not recorded) | Session | Chrome | Only one Chrome instance is connected (Jun Ting, ChatGPT Plus). The Jingyen profile (ChatGPT Free, Gemini Pro) is not reachable from this session | ChatGPT Free PV11-036 to 040, 056 to 060 and Gemini Pro PV11-006 to 010 and others remain pending |

## Protocol gaps to disclose

- **Timestamps.** The collection log says actual start and end timestamps are retained for every response. For runs 011 to 050 they were not captured precisely, so `started_at_utc` and `completed_at_utc` are null. Runs 001 to 005 have their original timestamps.
- **Capture method.** Runs 011 and 012 used the markdown copy button. Later runs used select-all rendered text, which loses markdown markers and can alter some characters.
- **Browser profile.** Runs 011 to 050 were collected in the Junting profile (ChatGPT Plus, Gemini Free), not the Jingyen profile specified in the collection plan.
