
## Technical incident — 2026-11-05T19:16:04.625Z UTC

A global address-bar shortcut was sent while TextEdit had focus, so the literal URL `https://chatgpt.com/?temporary-chat=true` was submitted as a follow-up in PV11-002's Temporary Chat. The reply was excluded from the pilot. The original PV11-002 completed response remains preserved; this later turn cannot change it. Submit/completion timestamps were not captured and remain null. The event is recorded in `incidents_luna.jsonl` and `raw/PV11-002-unintended-url-followup.txt`. The collector then used the visible New chat and Temporary chat controls; the new blank chat visibly shows Temporary Chat, Unpersonalized, and Think ON.
