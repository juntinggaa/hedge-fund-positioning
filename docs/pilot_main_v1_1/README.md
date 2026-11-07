# Fresh pilot materials ready

Version: pilot-main-v1.1-2026-11-06. Built without LLM calls.

Three fresh cases, 15 unique prompts, 60 planned responses across four products. All cases are outside the main/original samples and known development cases. Dates were chosen without residual magnitudes or LLM results. This is a validation sample, not a historical prevalence sample.

| Category | Week | Stratum | Earlier OOS errors |
|---|---|---|---:|
| net_long | 2021-09-21 | S1 | 460 |
| moderate_short | 2020-11-03 | S3 | 414 |
| extreme_short | 2025-08-05 | S4 | 662 |

Use prompts.jsonl or the collector packet; follow collection_queue.jsonl. Profile mapping: Jingyen = ChatGPT Free / Gemini Pro; Junting = ChatGPT Plus / Gemini Free. Verify the requested modes before collecting; do not change account-wide settings. Use a fresh Temporary Chat for each prompt and save the first completed reply immediately. Retain refusals and searched responses; log visible retrieval separately from citations.

Copy responses_template.jsonl to responses.jsonl and fill it; never fill the template itself. The build does not overwrite responses.jsonl or completed coding files. Do not regenerate satisfactory or inconvenient answers. Record technical retries in a separate attempt log.

After collection run `python scripts/validate_pilot_main_v1_1.py prepare --responses PATH --out PATH`. Give each coder their separate packet, the numeric references, and CODEBOOK_v2_1_PILOT.md. Do not give coders the collector key, queue, model labels or the annotation text. Blinding is partial: response content can itself reveal the condition. Coders work independently; keep original scores before adjudication.

Run the validator's `agreement` command on completed coder CSVs. It reports pooled reliability without product/arm outcome contrasts. Constant scores produce undefined kappa, not invented perfect reliability. Main collection remains on hold until the pilot is reviewed and the operational codebook is validated. No significant pilot arm difference is required.
