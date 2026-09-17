# Can a machine be taught to read the market correctly?

### Grounding, tooling, and directional misattribution in LLM interpretation of institutional futures positioning

**NST2046 Group Project — Milestone 1: Investigation Proposal**
Group: *[names]* · *[date]*

---

## 1. Question and claim

Non-expert investors increasingly ask general-purpose LLMs to interpret financial data.
We study a setting where the intuitive reading is documented to be wrong, the ground
truth is public and verifiable, and a repair is available — which lets us ask not only
whether the system fails, but whether failure is a property of the model or of how it
is deployed.

**Research question.** When a large language model is given retrieval grounding and a
positioning-decomposition tool, how does its rate of directional misattribution change
when interpreting CFTC Treasury futures data for a non-expert user — and what follows
for responsibility if a documented failure turns out to be cheaply repairable?

The domain is chosen because the naive reading is specifically and demonstrably wrong.
Leveraged funds hold very large *short* positions in Treasury futures. The intuitive
inference — "hedge funds expect bond prices to fall" — is substantially incorrect: much
of that position is the cash–futures **basis trade**, in which the fund simultaneously
holds the underlying security. The position expresses an arbitrage, not a view. Federal
Reserve research attributes a substantial share of hedge-fund Treasury exposure to such
strategies. In our verified data, leveraged funds are net short in 66% of 1,057 weeks,
reaching −48.5% of open interest in September 2025.

**Hypotheses.**

- **H1.** A bare model misattributes directional intent to non-directional positioning
  at a high rate.
- **H2.** Retrieval grounding repairs *factual* errors — fabricated figures — but not
  *interpretive* ones. Supplying correct numbers does not change the framing applied
  to them.
- **H3.** Tool augmentation, giving the model an explicit decomposition of positioning
  into explained and unexplained components, substantially reduces interpretive
  misattribution.
- **H4 (competing).** The failure persists across all three conditions: the training
  association is strong enough to override supplied evidence.

**Provisional claim.** The failure is an *application* deficit rather than a knowledge
deficit — the model can state what a basis trade is, but does not invoke it when
reading positioning — and it is therefore repairable by deployment design rather than
retraining. If that holds, the normative weight shifts from the technology to the
choices of those who deploy it.

## 2. System and mechanism

**Technical object.** A three-arm workflow built around two instruction-tuned LLMs at
pinned versions, with temperature and sampling parameters fixed and logged. We treat
the deployed model-plus-scaffolding as the system under test.

| Arm | Configuration | Isolates |
|---|---|---|
| **A — Baseline** | Bare model; positioning table in the prompt | The unaided failure rate (H1) |
| **B — Grounded** | Retrieval over our verified CFTC corpus and basis-trade reference material | Whether correct facts fix framing (H2) |
| **C — Tool-augmented** | Agent calls a positioning-decomposition model, then answers from its output | Whether structured evidence fixes framing (H3) |

**Input → representation → output.** The input is one week of TFF data — dealer, asset
manager and leveraged-fund long/short/spreading positions plus open interest — and a
question about what it implies. The model tokenises this and generates autoregressively,
conditioned on a training distribution in which *large short position* co-occurs
overwhelmingly with bearish interpretation, because that inference holds in most
markets. Treasury futures are a structural exception, under-represented relative to the
general pattern.

**Failure mechanism (arms A, B).** The model regresses to the modal association in its
training data rather than applying the market-specific exception, and output fluency
carries no signal that the substitution occurred. Arm B tests whether the substitution
is caused by missing information or survives its provision.

**Intervention mechanism (arm C).** A supervised model predicts expected leveraged-fund
positioning from market conditions — basis-trade conditions, momentum, rate level and
curve, volatility, funding spreads — using expanding-window walk-forward estimation so
no fitted value depends on data unavailable at the time. The residual is the
*unexplained* component. The agent receives a decomposition rather than a raw position,
changing what it has to reason over: not "a 3.26M contract short" but "a short of which
most is consistent with known strategy conditions and a stated remainder is not."

## 3. Prior work

**Positioning is not belief.** Federal Reserve and Office of Financial Research analyses
of the Treasury cash–futures basis trade document leveraged funds holding large short
futures against long cash positions. Fishe & Smith (2012, *Journal of Financial
Markets*) find a trader's business category is a weaker guide to their information than
their observed behaviour, reinforcing that category-level positions do not license
simple intent claims.

**Models generate fluent unfaithful text.** Ji et al. (2023, *ACM Computing Surveys*)
establish that generated content can be confidently stated and unsupported, and that
fluency does not track accuracy.

**Retrieval and tools are the standard repair.** Lewis et al. (2020, *NeurIPS*)
introduced retrieval-augmented generation for knowledge-intensive tasks; Schick et al.
(2023) showed models can learn to call external tools. Both are proposed as remedies for
unsupported generation. Whether they repair *interpretation* as opposed to *recall* is
much less settled — that is the gap we test.

**Users over-trust automated output.** Parasuraman & Riley (1997) show operators accept
automated recommendations against contrary evidence, with effects strongest for
non-experts.

**Repairability bears on responsibility.** Matthias (2004) frames the responsibility gap
for adaptive systems where no party both foresaw and controlled the harm. A failure that
is cheap to repair narrows that gap: it makes the deployment choice, not the model's
opacity, the locus of answerability.

> **Verification note.** Every source is to be retrieved and checked against the original
> before submission. No claim here rests on an LLM's report of what a paper says.

## 4. Technical investigation plan

**Data.** CFTC *Traders in Financial Futures* futures-only reports for 10-Year Treasury
Note futures (contract code `043602`): 1,057 weekly observations, 2006-06-13 to
2026-09-08. Ingested from the CFTC public reporting API and reconciled against CFTC's
official zip archives across 2,310 data cells with zero mismatches; the vintage is
pinned by content hash. Ground truth is fixed and independently checkable.

**Baseline and controlled variation.** Arm A is the baseline. Arms B and C each change
one thing against it. Model, temperature, test cases and scoring rubric are held
constant across arms; a second model is run on all arms to separate model-specific from
general behaviour.

**Test cases.** Purposively sampled to span the interpretive space, not randomly drawn:

1. **2025-09-02** — record leveraged-fund short, −48.5% of open interest. Maximum
   temptation to read as extreme bearishness.
2. A week where leveraged funds are net **long** (34.2% of weeks) — distinguishes
   reading the data from reciting a narrative.
3. A **pre-2015** week, when the basis trade was small and a directional reading is more
   defensible — tests whether the model is sensitive to era.
4. A **fabrication probe** — a plausibly-phrased question about a week beyond the model's
   data cut-off.

**Outcome measures.** Each response is scored on a fixed rubric by two members
independently; disagreements are recorded and adjudicated, and inter-rater agreement is
reported rather than assumed.

| Measure | Type | Scale |
|---|---|---|
| Numerical fidelity | factual | correct / approximate / fabricated |
| Directional attribution | interpretive | none / hedged / asserted |
| Alternative explanation raised unprompted | interpretive | binary |
| Calibration | interpretive | confidence vs evidential support |
| Decomposition fidelity (arm C only) | factual | faithful / distorted / ignored |

The factual/interpretive split is what makes H2 testable: grounding is predicted to move
the first and not the second.

**Expected failure modes.** High directional attribution in arm A; basis trade rarely
raised unprompted; fabricated open-interest figures on the probe. In arm C we
specifically expect and will analyse **tool-output distortion** — the agent receiving a
correct decomposition and still narrating it directionally, which would be the most
interesting failure available to us.

## 5. Societal and philosophical stakes

**Stakeholders.** Non-expert investors using LLMs for market interpretation; advisers
whose clients arrive with model-generated views; regulators whose disclosure regimes
assume a human intermediary; model providers who choose deployment scaffolding.

**Benefits.** Real and worth stating: these systems make institutional data legible to
people who would never open a CFTC report. The failure is the cost of that access, not
an argument against it.

**Harms, and their distribution.** The harm is asymmetric. A professional reading the
same data has Bloomberg, Fed research, and colleagues who will say *that's the basis
trade*. The non-expert has the chatbot and nothing to check it against, so the error
lands precisely on those least able to detect it. Where positioning data is published to
create market transparency, a systematic misreading layer degrades the transparency the
disclosure was meant to produce.

**Normative question.** *When a failure is known and cheaply repairable, who is
answerable for leaving it unrepaired?* Human testimony carries accountability, and a
speaker's confidence usually tracks their competence. An LLM's confident register is a
property of its training objective, not its evidential position, so the cue we ordinarily
use to calibrate trust is severed from what it normally indicates. Matthias's
responsibility gap is usually argued from opacity and unforeseeability. Our design
attacks that premise directly: if arm C repairs what arm A breaks, the harm was neither
unforeseeable nor uncontrollable, and the gap narrows to a choice. If arm C *fails*, the
gap widens and the case for restricting such use strengthens. Either result carries
normative weight, which is why we pre-commit to reporting both.

## 6. Feasibility and roles

| Week | Work | Owner |
|---|---|---|
| 1 | Test cases, prompt design, scoring rubric; arm A harness | *[name]* |
| 1–2 | Feature pipeline and basis proxy | *[name]* |
| 2–3 | Decomposition model, walk-forward estimation | *[name]* |
| 3 | Arm B retrieval corpus | *[name]* |
| 4 | Arm C agent and tool interface | *[name]* |
| 5 | Run all arms; independent double-scoring | all |
| 6 | Analysis; societal and philosophical drafting | *[name]* |
| 7 | Report and presentation | all |

**Dependencies.** API access to two models — the binding constraint, to be secured in
week 1. The CFTC dataset is already ingested, verified and version-pinned.

**Deliberately out of scope.** We do not test whether the decomposition predicts future
returns. The model's job is to produce an honest description, not a forecast, so no
predictive-inference apparatus is required. This keeps the finance component
proportionate to its role as one instrument in the experiment.

**Fallback.** If arm C cannot be built in time, we ship arms A and B — which alone
constitute a baseline, a controlled variation and a testable hypothesis (H2) — and name
arm C as the most informative next experiment. If H1 fails and the baseline is already
correct, the project becomes locating the boundary: sparser context, less common
contracts, and multi-turn conversations where an early framing persists.

## 7. AI-use plan

| Tool | Purpose | How outputs are checked |
|---|---|---|
| LLMs under test | Object of study, not authority | Outputs are data, scored against CFTC ground truth |
| Claude Code | Data pipeline, harness, decomposition model | Code reviewed and tested; 58 automated tests; data reconciled against official CFTC archives |
| LLM assistants | Drafting, structuring, literature leads | Every factual claim and citation retrieved and verified at source |

No claim in the report rests on an LLM's assertion that something is true. Prompts and
outputs that materially change our method or conclusions are retained in the evidence
log. The dataset is entirely public; no personal or confidential data is used.

---

## References

*To be verified at source before submission; see §3 verification note.*

1. Commodity Futures Trading Commission. *Traders in Financial Futures* reports. Public
   reporting dataset `gpe5-46if`. [verified — primary data source]
2. Fishe, R. & Smith, A. (2012). Identifying informed traders in futures markets.
   *Journal of Financial Markets*. [academic]
3. Ji, Z. et al. (2023). Survey of hallucination in natural language generation.
   *ACM Computing Surveys*. [academic]
4. Lewis, P. et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP
   tasks. *NeurIPS*. [academic]
5. Schick, T. et al. (2023). Toolformer: language models can teach themselves to use
   tools. [academic]
6. Parasuraman, R. & Riley, V. (1997). Humans and automation: use, misuse, disuse,
   abuse. *Human Factors*. [academic]
7. Matthias, A. (2004). The responsibility gap: ascribing responsibility for the actions
   of learning automata. *Ethics and Information Technology*. [academic]
8. Federal Reserve / Office of Financial Research analyses of the Treasury cash–futures
   basis trade. [institutional — select and cite specific publications]
