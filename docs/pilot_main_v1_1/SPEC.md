# Fresh pilot build specification — 6 November 2026

Version: pilot-main-v1.1-2026-11-06. This specification is written before the
first case draw and before new pilot responses. It prepares materials only;
neither the builder nor the validator sends prompts to an LLM.

## Selection fixed before drawing

- Use the append-only CFTC 043602 panel and frozen extended weighted_104
  predictions, with existing v4 construction and at least 52 earlier OOS errors.
- Retain the original extreme-short cutoff, derived from the original pinned
  negative-net/OI tenth percentile; do not recompute on the extension.
- Select three cases: one net long, one moderate short (S2 or S3), one extreme
  short from 2015 onward. A three-case pilot does not cover all four main strata.
- Exclude all 33 main weeks, all original Milestone 1 sample weeks, the six
  known v2 pilot-development dates, and the technical-test date 2014-03-04.
- Sort each eligible category's dates, then choose uniformly with Python
  Random seeds 20261106, 20261107, and 20261108. Do not inspect residual sizes,
  old/new LLM replies, scores, product differences or expected p-values to pick dates.
- This is a small validation sample, not a prevalence estimate. It does not
  impose an eight-week separation from every main case; the main sample itself
  stays unchanged. No pilot cases/responses enter main estimates.

## Materials and order

Build 15 unique prompts using existing v4 A/B/C-bare/C-ann/D rendering plus the
exact main-v1.1 suffix “Please answer without using web search.” Use the same
frozen model card and annotation. No stronger “use only supplied information”
line, pressured question or extra context is added.

D uses a seeded derangement of the three pilot residuals only (same rejection
sampling policy/seed 20261104 as main). No pilot week keeps its own residual;
the main 33-case derangement remains unchanged. Placebo is not a genuine estimate
for the target week and is used only as the designated experimental control.

Each prompt goes once to four configurations, 60 replies planned:

| Product | Chrome profile | Requested mode |
|---|---|---|
| ChatGPT Free | Jingyen | default genuinely free mode; record visible label |
| ChatGPT Plus | Junting | High thinking effort; record visible label |
| Gemini Free | Junting | Auto/Low as available; verify before collection |
| Gemini on Google AI Pro | Jingyen | Argon High; verify before collection |

Requested modes are not invented exact backend IDs. Verify availability before
the first run; pause/log a fallback rather than silently mixing configurations.
Randomize case and product order and rotate a seeded arm permutation across
cases/products. Fix the schedule before replies. Keep a fresh Temporary Chat
for each prompt. Do not change account-wide settings.

## Coding and validation

Follow CODEBOOK_v2_1_PILOT.md and the dated outcome amendment. Components and
threshold are specified now, pending human reliability validation. Collect and
archive full replies before navigation; save visual output as well as text.
Two independent human coders receive masked product/arm IDs and numeric reference
packets; annotation/explainer text and the private collector key are withheld.
The method masks labels, not all clues in response content; disclose partial blinding.

Prepare separate coder packets after validating that all 60 first completed
responses are saved. No LLM coder substitutes for either human. Preserve
pre-adjudication scores. Report pooled reliability/prevalence without arm/product
effects. Undefined κ is indeterminate. There is no pilot significance gate and
no rule that changes the primary outcome to manufacture more events.

Only after human review and a dated codebook validation decision should the
660-response main run begin. Rebuild the same material files byte-for-byte;
never overwrite collected responses or completed coding sheets.
