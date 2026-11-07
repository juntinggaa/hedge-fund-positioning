# Luna collection pilot repair handoff — 6 Nov 2026

## Status

The authorized capture and repair queue is complete: 49 of 49 planned attempts are accounted for, with zero pending. The ledger contains 44 rows in `responses_collection_luna.jsonl` and five rows in `superseding_attempts_luna.jsonl`; the ID sets are disjoint. There is one separately documented technical mis-send incident for PV11-002, excluded from the pilot. No main study calls were started.

Technical capture repairs completed:

- Gemini Free, Temporary Chat: PV11-016–020, PV11-031–035, and PV11-041–045 (15 captures).
- ChatGPT Plus, Temporary chat and Unpersonalized, High effort: PV11-013, PV11-023, PV11-047, and PV11-048 (4 captures).

Each repair preserves its original response and stores evidence in the collection’s `raw/`, `ax/`, and `screenshots/` folders. Copy captures were hash checked and compared with response accessibility text. No response was regenerated during these repairs.

## Reconciliation and visual evidence

- PV11-023’s first clipboard read contained PV11-013’s prior response; it is preserved in `raw/PV11-023-luna-plus-temp-repair-1-initial-copy-mismatch-from-prior-chat.txt`. Two later reads stabilized on the correct 4,494-character response (SHA-256 `5d07fdd587cc1dd0e8a709589dacb6772b46f3e2b3f2aa4693c0dbe61ed954ae`). The final text matched 35 response-text AX nodes; six chart-artifact AX nodes and the interactive chart screenshots are recorded separately.
- PV11-043’s initial clipboard read contained PV11-042’s prior response (3,202 characters); it is preserved in `raw/PV11-043-luna-temp-repair-1-initial-copy-mismatch-from-prior-chat.txt`. The stabilized 4,372-character response (SHA-256 `5afa9bc1fd6c25c888055029cedea2d1cdc5d2d5c9e7d296d82eae5a0200a5c0`) matched 29 AX text nodes after documented rendering normalization. The frozen prompt and pre-send composer matched; no rerun was made.
- PV11-047 and PV11-048 show horizontal position bar graphics in their first terminal responses. Screenshots and AX labels are saved; no interactive chart options or controls were exposed. Their initial generic “no interactive visual” classifications were corrected by append-only metadata amendments.

## Exceptions to preserve

- PV11-044 returned a 91-character refusal. It is the captured response; no retry was made.
- PV11-055’s first terminal visual said “Couldn’t load interactive visual.” A later same-response retry remained pending alongside a limit-reached notice. Keep the text and first failure evidence; do not claim a successful visual. Citation-source controls exposed CME Group and Federal Reserve Bank of Chicago nodes, but the retrieval observation remains “no visible search.”
- PV11-030’s final visual state is unknown; only generation progress was captured. Do not regenerate or mark it as fully visually captured.
- PV11-059’s completed AX text ended mid-sentence at “Without it, we cannot reliably distinguish a crowded bear”; preserve that observed capture boundary.
- PV11-002’s unintended URL follow-up is in `incidents_luna.jsonl` and `ATTEMPT_LOG_2026-11-06.md`, excluded from the pilot; its original completed response remains intact.

## Next step

Wait for the user’s explicit scientific GO before starting the main 660-call study. The repair queue is complete, but that GO has not been given.
