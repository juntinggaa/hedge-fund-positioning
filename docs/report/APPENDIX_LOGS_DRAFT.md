# Appendix drafts: AI-use log, decision log, contribution statement (DRAFT, 8 Nov 2026)

Continues the Milestone 1 logs (`docs/milestone1/appendix.md` §C–D). Fill the *[owner]* cells and
check every row; delete any row the group did not actually do.

## A. AI-use log (Milestone 2)

| Tool | Purpose | Used / rejected | How the output was checked, and what changed |
|---|---|---|---|
| Professor feedback (not AI) | Critique of Milestone 1 | Used | Drove the rebuilt codebook (separate motive and magnitude codes), Arm C model fit report, binary cut-off, frozen annotation |
| Claude Code (Opus) | Data pipeline, Arm C model (v2 to v4), prompt kits, sampling, collection checker, dataset assembly, analysis scripts, drafting | Used, under review | Unit tests; sha256 manifests pin every frozen prompt; checker scripts flag missing or changed files; group read every amendment before use |
| Codex / ChatGPT (GPT-6.x) | External review of model, design and wording | Used selectively | Each pasted review was checked against the code; some points accepted (nowcast claim corrected to "retrospective same-week estimate"; composite critique), others corrected |
| Codex browser agents | Pasting frozen prompts into ChatGPT, Claude and Gemini (high effort) and saving replies | Used | Prompt read-back and hash checks logged in `collection_*/attempts.jsonl`; error pages and truncated replies archived, not used (`main prompt outputs/_archive/`) |
| ChatGPT Plus (GPT-6 Sol, High), Claude Pro (Opus 5.5, High), Gemini (4 Argon, Low) | **Objects of study** | Used as data | 180 replies, frozen prompts, temporary chats, no web search |
| OpenAI API `gpt-5.5-2026-04-23` | Second machine coder for codebook validation (v2.2, v2.3) | Used | Agreement with Claude on pilot replies: composite κ 0.66 (v2.2) and 0.83 (v2.3), in-sample only |
| DeepSeek API | Planned third coder | Rejected | Account had no balance |
| Codex `gpt-6.1-sol` (high) | Machine coder 1, main run | Used | Read-only, empty folder, no commands run; every quote checked verbatim against the reply by script |
| Claude Opus 5.5 subagents | Machine coder 2, main run | Used | Each saw only its own masked packet; same verbatim-quote checks |
| Humans (4) | Reliability sample and dispute resolution, 30 replies double-coded | Used | Human–human and human–machine κ reported |

**Known risk to state in the report:** two coders are made by vendors whose products are under study
(an OpenAI model codes ChatGPT replies, a Claude model codes Claude replies). Replies were masked, but
writing style can identify a product, so self-preference cannot be ruled out. The human sample is the check.

## B. Decision log (Milestone 2)

| Date | Decision | Reason | Owner |
|---|---|---|---|
| 4 Nov | Rebuild codebook: B2 pattern→motive, B3 motive→magnitude, R residual interpretation, scored separately | Professor: one 0–3 scale mixed the boundaries H1 compares | *[owner]* |
| 4 Nov | Build and report the Arm C model; add placebo arm D | Professor: a poor model makes the residual uninformative | *[owner]* |
| 5 Nov | Describe the model as a retrospective same-week estimate, not a nowcast | It uses the same week's open interest | *[owner]* |
| 5 Nov | Keep model v4 (weighted ridge); reject Treasury-supply and dealer-inventory factors | Both failed the pre-set gate | *[owner]* |
| 5 Nov | Do not add cash-Treasury holdings as a factor | No timely, matched series; would not identify the cash leg | *[owner]* |
| 6 Nov | Use the chat products, not the API | We study what users actually get; API settings differ from the apps. Record shown labels and settings instead | *[owner]* |
| 6 Nov | Codebook v2.2 → v2.3 (B2 rules 9–12; anchors 13–14) | Coder disagreements on pilot replies; written after seeing them, so κ on those replies is in-sample | *[owner]* |
| 6 Nov | Drop arm B and arm D from the main run | Decided after the pilot (B looked redundant with A; D for budget) and disclosed as such | *[owner]* |
| 6 Nov | main-v1.3: 20 weeks (seeded within strata), 3 products, arms A / C-bare / C-ann, one shared order | Deadline; emphasis on interpreting replies over volume | *[owner]* |
| 7 Nov | Advice-framing add-on built as exploratory, outside the main analysis | Tests "should I buy?" pressure; not part of the primary family | *[owner]* |
| 7 Nov | Gemini analysed at low effort (all 60); 16 high-effort replies kept as a descriptive effort check | High-effort run hit a cap; mixing efforts would confound arm with effort in 14 of 20 weeks | *[owner]* |
| 7 Nov | Two machine coders on 196 masked replies; 17 composite disputes plus 13 agreed replies double-coded by humans | κ alone is machine–machine; humans settle disputes and give reliability | *[owner]* |
| 8 Nov | Factual accuracy not coded | Out of scope for this run; stated as a limitation | *[owner]* |

## C. Contribution statement (fill in)

| Member | Contributions |
|---|---|
| Lip Jun Ting | *[e.g. data pipeline, Arm C model, collection (ChatGPT, Claude, Gemini high), coordination, human coding]* |
| Tia Elizabeth Ansari | *[ ]* |
| Upadhye Neeti Rahul | *[ ]* |
| Chua Jun Yu Xavier | *[ ]* |
