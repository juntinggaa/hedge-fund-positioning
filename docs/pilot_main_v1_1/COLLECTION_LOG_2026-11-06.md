# Pilot collection log — 6 November 2026 (Asia/Singapore)

## Operational scheduling deviation, recorded before parallel collection

The first five ChatGPT Free runs were started in the frozen global order (PV11-001 through PV11-005). To reduce collection time, the remaining collection is split across independent Chrome profiles: Jingyen/Tong (ChatGPT Free, Gemini Pro) and Junting/Person 1 (ChatGPT Plus, Gemini Free). Each profile stream preserves its relative order from collection_queue.jsonl, including the assigned within-product case/arm order. The original global cross-profile order will consequently differ. The original queue, IDs and hashes remain unchanged; actual start/end timestamps are retained for every response.

This change concerns scheduling only. It was chosen for collection speed after inspecting capture integrity, without scoring pilot outcomes or using responses to select prompts, cases, endpoints or models. One first completed response is retained per run. No main-study responses are being generated.

Browser control is divided by surface: the main collector uses the native Tong window; the second collector uses DOM controls in Person 1 only, without native keyboard or window switching. Each collector saves separate response records before merging and validating all 60 IDs.

## Continuation, 6 November 2026 (Asia/Singapore), Claude session

- Only one Chrome instance was connected (Jun Ting, ChatGPT Plus). Runs 011 to 050 were collected in that profile: 15 ChatGPT Plus and 15 Gemini Free, in the queue's per-stream order.
- The Jingyen profile (ChatGPT Free PV11-036 to 040 and 056 to 060, Gemini Pro PV11-006 to 010 and the rest) was not reachable. Those 25 runs remain pending.
- Now collected: 35 of 60 retained replies. Each has a verified prompt hash (SHA-256 before send). The submitted text was checked by screenshot or readback. Numeric tokens matched the frozen prompt for all Gemini runs. ChatGPT readback was not byte-compared.
- Deviations: (a) start and completion timestamps were not captured for 011 to 050; (b) the capture method changed after run 012 (see ATTEMPT_LOG_2026-11-06.md); (c) 10 replies contain replacement characters from clipboard decoding; (d) one Gemini submission (PV11-017, attempt 1) sent the wrong text and was discarded, with a logged retry; (e) PV11-002 remains unverified.
- Gemini Free settings observed: model "Auto", thinking level "Low" (picker). Web-search control: none on this surface; no-search instruction only, as frozen.
