# Focused validation collection protocol — 6 November 2026

Only collect the24 PVR22 jobs in collection_queue.jsonl. This is a fresh pilot
validation, not the main study. Do not start main660 after completing this queue:
return it for independent coding and an explicit scientific gate.

Preserve all prior pilot attempts, ratings, settings and inputs. Use the same
accounts: Jingyen/Tong=ChatGPTFree ThinkON and GeminiGoogleAIPro ArgonHigh;
Junting/Person1=ChatGPTPlus High and GeminiFree Auto/Low. Fresh Temporary Chat
for every job; ChatGPT Unpersonalized. Verify actual account/tier and visible
mode. No account-wide settings, model substitutions, upgrades or purchases.
Use the exact frozen prompt; no extra explanatory turn or edited instruction.
The no-search wording is a request, not a guaranteed technical search block.

Global queue order interleaves products; within each product the six jobs are
randomized. Product availability/quota may change global product order: preserve
each product's relative order and log the actual timestamp/order and reason for
any deferral. This allowance is specified before collecting fresh replies. Do
not choose order based on reply content. Wait for actual quota resets and do
not change mode/account to evade a limit. Coordinate browser ownership with the
parent; do not control the browser concurrently with another agent.

Before send: check the actual composer from the visible UI, save full pre-send
AX and a screenshot, hash its exact text against prompt_sha256, and verify
Temporary/mode/account. Hashing the source file is insufficient proof of what
was pasted. If UI rendering changes only whitespace, retain the entire raw
composer readback plus its hash, use prompt_verification="whitespace-normalized",
and prove equality with only whitespace normalization. Do not discard numbers,
signs, punctuation or substantive words to force a match. Record the raw and
normalized comparison distinctly; a source-file hash is not the raw UI hash. Start time is the live send time, completion is observed completion;
never reconstruct a fictitious exact timestamp. Keep any bound/unknown honest.

Save the first completed valid-condition answer regardless of content, refusal,
citations or search. Use the reply's Copy control, confirm it copied the reply
rather than the prompt, and compare full visible AX text/math with the saved raw
UTF8 reply. Preserve raw formatting/artifacts and code blocks; no guessed glyphs,
missing words, invented chart values or semantic-number stripping. Observe
actual terminal completion before leaving a Temporary Chat. Save raw AX and
screenshots immediately, including every offscreen segment necessary to verify
full text and any actual visual. A visual terminal failure is part of the reply;
do not click retry on a completed failed widget. If a visual is pending after
a documented timeout (maximum10minutes after verbal completion), capture the
pending state and mark capture incomplete; do not turn it into a safe answer.
Do not open a new chat before saving the first answer and source evidence.

Record each job immediately with the original validator fields: run_id,
prompt_sha256, status,response_text,observed_model_label,observed_thinking_label,
temporary_chat_verified,started_at_utc,completed_at_utc,retrieval_observation,
citations_observed,submitted_prompt_sha256,prompt_verification,response_sha256,
capture_method,screenshot_files,technical_notes. Also retain attempt_id, blind_id, product_id, profile, week, arm,
pre_send_ax_file, ax_snapshot_file, raw_capture_file, copy_button_capture_file,
and any visual_evidence_files, with actual source paths. Retrieval labels are
"no visible search" / "observed" / "unknown". Citations alone do not prove
search. Use status="completed" if captured; a refusal remains a completed raw reply and is
classified later by coders. Capture-quality problems go in separate notes.

Write append-only responses_collection.jsonl under collection_luna/ in this
folder. Save individual raw source proofs under outputs/pilot_validation_v2_2/
luna/ in the parent workspace. Never replace a raw metadata record: append a
revision sidecar with source/old/new/hash if needed. Keep malformed sends,
technical retries, incomplete captures and quota evidence in ATTEMPT_LOG.md and
CHECKPOINT.md. Technical retries only repair demonstrably wrong condition,
mis-send or capture failure under a documented criterion, never answer quality;
if unclear stop that job for the parent rather than regenerate. No silent
content reruns, discarded refusals or second-turn prompts. A source-incomplete
reply is retained and flagged for the existing unscorable policy.

At completion hand off all24 assignments and proofs. Do not judge arm effects,
code the replies, adjust codebook, claim kappa passed or launch the main run.
