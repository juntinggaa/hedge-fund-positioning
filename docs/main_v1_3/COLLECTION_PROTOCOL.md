# Main-v1.3 collection protocol — 4 people, 180 replies

## Roles

| Person | Role | Assignments |
|---|---|---|
| P1 | Collector, **ChatGPT Plus** account holder | `runsheet_GPT.csv` (GPT-001 … GPT-060) |
| P2 | Collector, **Google AI Pro** account holder | `runsheet_GEM.csv` (GEM-001 … GEM-060) |
| P3 | Collector, **Claude Pro** account holder | `runsheet_CLA.csv` (CLA-001 … CLA-060) |
| P4 | **Coordinator**: checks every saved reply against the rules, keeps the tracker, takes over a product if its collector is stuck, and later builds the masked coding packets | — |

- Each product stays on **one account**. If a second account is unavoidable, it must be on the same plan and its label goes in `account_label`.
- Only P4 opens `assignment_key_PRIVATE.csv` (week and arm per ID). Collectors don't need it.
- At about 3–4 minutes per reply, each collector needs roughly 3–4 hours, plus waits for cap resets. Spread the work over sessions.

## Shared folder (Google Drive)

```
main_v1_3/
  GPT/   runsheet_GPT (Google Sheet)   GPT-001.md  GPT-001.png  ...
  GEM/   runsheet_GEM (Google Sheet)   GEM-001.md  GEM-001.png  ...
  CLA/   runsheet_CLA (Google Sheet)   CLA-001.md  CLA-001.png  ...
```

- Upload each `runsheet_<CODE>.csv` as a Google Sheet. Copy the `prompts/` folder from the repo to the drive, or open the files locally.
- **Do not paste replies into the spreadsheet.** Cells mangle long markdown. Each reply goes in its own `.md` file.

## Steps for every assignment (in runsheet order)

1. Open a **new temporary/incognito chat** and confirm memory is off.
2. Select the model and the standard thinking level, and leave them fixed for the whole run:
   - ChatGPT Plus: GPT-6 Sol;
   - Gemini: Gemini 4 Argon;
   - Claude: Opus 5.5.
3. Open `prompts/<ID>.txt`, select all, copy, paste and send. **Don't add or change anything.**
4. Wait for the reply to finish. Use the reply's **Copy** button. Save it as `<ID>.md` in your product folder.
5. Take one screenshot showing the model label, the temporary-chat indicator, and the top of the reply. Save it as `<ID>.png`.
6. Fill the runsheet row:

| Column | What to write |
|---|---|
| collector_name, account_label | who, and which account |
| started_at_sgt / finished_at_sgt | e.g. `2026-11-07 14:05` |
| model_label_shown | exactly as the app shows it |
| thinking_setting_shown | exactly as shown |
| temporary_chat | `Y` / `N` |
| search_observed | `none` / `searched` / `citations` |
| status | `completed`, `refusal`, `error`, `fallback_model`, `cap_hit` or `incomplete` |
| attempt_number | `1`, or `2`, `3` for resends after an error, fallback or cap |
| reply_file / screenshot_file | `<ID>.md` / `<ID>.png` (for a resend: `<ID>_a2.md`) |
| notes | anything odd |

## When something goes wrong

| Situation | Do |
|---|---|
| Reply looks wrong or overreaches | **Nothing.** That is the data. Never resend because of content. |
| App error, or the reply stops mid-way | `error` or `incomplete`. Keep what you got, then resend as attempt 2 in a new chat. |
| Cap reached, or the model label changes to a smaller model | `cap_hit` or `fallback_model`. Keep any reply. Stop that product until the reset, then resend as the next attempt. Never switch model or effort to keep going. |
| Refusal | `refusal`. Save it. It counts as the first completed reply. Don't resend. |
| The app searched the web | Keep it. Set `search_observed`. Don't resend. |
| You pasted the wrong prompt | Note it, then resend the right one as the next attempt in a new chat. |

## Hand-over to analysis

1. P4 downloads each sheet as `runsheet_<CODE>.csv` into `docs/main_v1_3/responses/<CODE>/`, together with the `.md` and `.png` files.
2. Run the checker:
   ```
   python scripts/ingest_main_v1_3.py docs/main_v1_3/responses
   ```
   It lists every missing file, empty field and duplicate, and writes `responses_v1.3.jsonl` with a hash of every reply. Fix problems by adding missing records, never by editing reply text.
3. P4 builds the masked coding packets: random order, IDs replaced, no product, arm or week labels. The two human coders then code independently with codebook v2.3.

**Run a short trial first:** each collector does assignment 001 and P4 checks it before anyone continues.
