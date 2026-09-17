# Can a machine be taught to read the market correctly?

### Grounding, tooling, and directional misattribution in LLM interpretation of institutional futures positioning

**NST2046 Group Project — Milestone 1: Investigation Proposal**
Group: *[names]* · *[date]*

---

## 1. Question and claim

Non-expert investors increasingly ask general-purpose LLMs to interpret financial data.
We study a setting where the intuitive reading is documented to be wrong, ground truth
is public and verifiable, and a repair is available — letting us ask not merely whether
the system fails, but whether failure is a property of the model or of how it is
deployed.

**Research question.** When an LLM is given qualitative context, quantitative
decomposition, or agentic tool access, how does its rate of unsupported directional
attribution change when interpreting CFTC Treasury futures data for a non-expert user —
and what follows for responsibility if a documented failure proves cheaply repairable?

The domain is chosen because the naive reading is demonstrably wrong. Leveraged funds
hold very large *short* positions in Treasury futures. The intuitive inference — "hedge
funds expect bond prices to fall" — is substantially incorrect: much of that position is
the cash–futures **basis trade**, where the fund simultaneously holds the underlying
security, expressing an arbitrage rather than a view. Federal Reserve research
attributes a substantial share of hedge-fund Treasury exposure to such strategies. In
our verified data leveraged funds are net short in 66% of 1,057 weeks, reaching −48.5%
of open interest in September 2025.

| | Hypothesis |
|---|---|
| **H1** | A bare model makes unsupported directional attributions at a high rate. |
| **H2** | Qualitative grounding repairs *factual* errors but not *interpretive* ones: correct numbers do not change the framing applied to them. |
| **H3** | Quantitative decomposition substantially reduces interpretive misattribution. |
| **H4** | Agentic tool access adds little beyond receiving the same decomposition directly. |

**Provisional claim.** The failure is an *application* deficit, not a knowledge deficit —
the model can define a basis trade but does not invoke the concept when reading
positioning — and is therefore repairable by deployment design rather than retraining.
If so, normative weight shifts from the technology to those who deploy it.

## 2. System and mechanism

**Technical object.** A four-arm workflow around instruction-tuned LLMs at pinned
versions, with temperature and sampling parameters fixed and logged. The deployed
model-plus-scaffolding is the system under test.

| Arm | Configuration | Isolates |
|---|---|---|
| **A** | Bare model, positioning table in prompt | Unaided failure rate (H1) |
| **B** | + qualitative market-structure context | Effect of domain context (H2) |
| **C** | + precomputed decomposition placed in prompt | Effect of quantitative evidence (H3) |
| **D** | Agent with a decomposition tool it must elect to call | Effect of agentic tool use (H4) |

C and D are the design's centre. They differ only in how the same evidence is obtained —
guaranteed versus elective — so the C–D contrast isolates agency from information, which
a single tool-augmented arm would confound.

**Input → representation → output.** The input is one week of TFF data (dealer, asset
manager and leveraged-fund long/short/spreading positions, plus open interest) and a
question about what it implies. The model tokenises this and generates autoregressively,
conditioned on a training distribution in which *large short position* co-occurs
overwhelmingly with bearish interpretation, because that inference holds in most markets.
Treasury futures are a structural exception, under-represented against the general
pattern.

**Failure mechanism (A, B).** The model regresses to the modal association in training
rather than applying the market-specific exception, and output fluency carries no signal
that the substitution occurred. B tests whether this is caused by missing information or
survives its provision.

**Intervention mechanism (C, D).** A supervised model predicts expected leveraged-fund
positioning from market state — basis conditions, momentum, rate level and curve,
volatility, funding spreads — using expanding-window walk-forward estimation, so no
fitted value depends on data unavailable at the time. The residual is the *unexplained*
component. The system then reasons over a decomposition rather than a raw number: not "a
3.26M contract short" but "a short of which most is consistent with known strategy
conditions and a stated remainder is not."

## 3. Prior work

**Positioning is not belief.** Federal Reserve and Office of Financial Research analyses
of the Treasury basis trade document leveraged funds holding large short futures against
long cash positions. Fishe & Smith (2012, *Journal of Financial Markets*) find a trader's
business category is a weaker guide to their information than their observed behaviour,
reinforcing that category-level positions do not license intent claims.

**Models generate fluent unfaithful text.** Ji et al. (2023, *ACM Computing Surveys*)
establish that generated content can be confidently stated and unsupported, and that
fluency does not track accuracy.

**Retrieval and tools are the standard repair.** Lewis et al. (2020, *NeurIPS*)
introduced retrieval-augmented generation; Schick et al. (2023) showed models can learn
to call external tools. Both are proposed as remedies for unsupported generation. Whether
they repair *interpretation* as opposed to *recall* is far less settled — the gap we test.

**Users over-trust automated output.** Parasuraman & Riley (1997) show operators accept
automated recommendations against contrary evidence, most strongly among non-experts.

**Repairability bears on responsibility.** Matthias (2004) frames the responsibility gap
for adaptive systems where no party both foresaw and controlled the harm. A cheaply
repairable failure narrows that gap, making the deployment choice rather than model
opacity the locus of answerability.

> **Verification note.** Every source is to be retrieved and checked against the original
> before submission. No claim here rests on an LLM's report of what a paper says.

## 4. Technical investigation plan

**Data.** CFTC *Traders in Financial Futures* futures-only reports for 10-Year Treasury
Note futures (code `043602`): 1,057 weekly observations, 2006-06-13 to 2026-09-08,
ingested from the CFTC public reporting API, reconciled against CFTC's official archives
across 2,310 cells with zero mismatches, and pinned by content hash.

**Sampling.** Forty weeks, stratified to span the interpretive space rather than drawn at
random, since a random draw would over-represent ordinary weeks:

| Stratum | n | Why |
|---|---|---|
| S1 Leveraged funds net **long** | 10 | Distinguishes reading the data from reciting a narrative |
| S2 Moderate short, **pre-2015** | 10 | Basis trade small; directional reading more defensible |
| S3 Moderate short, **2015+** | 10 | Basis trade large; directional reading less defensible |
| S4 **Extreme** short, 2015+ | 10 | Maximum pull toward a bearish reading |

Positioning is strongly autocorrelated, so 40 adjacent weeks would be far fewer than 40
independent observations. Weeks are therefore drawn at least eight weeks apart and spread
across the full 2006–2026 period.

Four of these also serve as **deep cases**, including 2025-09-02 (record short, −48.5% of
open interest) and a fabrication probe asking about a week beyond the model's cut-off.

**Paired design.** Every sampled week is presented to every arm. The unit of analysis is
therefore the *within-week change* under a changed system, not a comparison of unrelated
responses.

**Measures, scored in two tiers.**

| Tier | Cases | Measures |
|---|---|---|
| Broad | all 40 | Unsupported directional attribution (y/n); non-directional explanation raised (y/n) |
| Deep | 4 | Numerical fidelity; directional attribution; alternative raised; calibration; tool-output fidelity (C, D); tool-call rate and correctness (D) |

The factual/interpretive split is what makes H2 falsifiable: grounding is predicted to
move numerical fidelity and not directional attribution.

**Analysis.** The primary test is **McNemar's test on discordant pairs** for each arm
contrast (A→B, B→C, C→D). Power depends on how many cases *change* between arms, not on
n: if arm C corrects fifteen of the weeks arm A gets wrong and introduces no new errors,
the exact test is significant well beyond conventional thresholds at n=40. Absolute rates
are reported with confidence intervals, and we state plainly that a single proportion at
n=40 carries roughly a ±15 percentage-point margin — sufficient to detect large effects,
not subtle ones. This is an exploratory audit, not a population-level estimate.

**Scoring protocol.** All deep cases and a randomly selected 25% of the broad sample are
independently double-scored; Cohen's κ is reported. Single-scoring of the remainder is
licensed only if κ ≥ 0.7. Below that the rubric is revised and the sample re-coded.

**Model coverage.** All four arms on the primary model (160 responses); arms A and C only
on a second model as a robustness check (80 responses). We do not run the full grid.

**Expected failure modes.** High directional attribution in A; basis trade rarely raised
unprompted; fabricated figures on the probe. In C and D we specifically expect and will
analyse **tool-output distortion** — the system receiving a correct decomposition and
narrating it directionally anyway, which would be the most interesting result available
to us, since it would implicate the generative objective rather than the information
supply.

## 5. Societal and philosophical stakes

**Stakeholders.** Non-expert investors using LLMs for market interpretation; advisers
whose clients arrive with model-generated views; regulators whose disclosure regimes
assume a human intermediary; providers who choose deployment scaffolding.

**Benefits.** Real and worth stating: these systems make institutional data legible to
people who would never open a CFTC report. The failure is the cost of that access, not an
argument against it.

**Harms, and their distribution.** The harm is asymmetric. A professional reading the same
data has Bloomberg, Fed research, and colleagues who will say *that's the basis trade*.
The non-expert has the chatbot and nothing to check it against, so the error lands
precisely on those least able to detect it. Where positioning data is published to create
market transparency, a systematic misreading layer degrades the transparency the
disclosure was meant to produce.

**Normative question.** *When a failure is known and cheaply repairable, who is answerable
for leaving it unrepaired?* Human testimony carries accountability, and a speaker's
confidence usually tracks their competence. An LLM's confident register is a property of
its training objective, not its evidential position, so the cue we ordinarily use to
calibrate trust is severed from what it normally indicates. Matthias's responsibility gap
is typically argued from opacity and unforeseeability. Our design attacks that premise: if
C repairs what A breaks, the harm was neither unforeseeable nor uncontrollable and the gap
narrows to a choice. If C fails, the gap widens and the case for restricting such use
strengthens. Either result carries normative weight, which is why we pre-commit to
reporting both.

## 6. Feasibility and roles

| Week | Work | Owner |
|---|---|---|
| 1 | Stratified sample; prompts; scoring rubric; arm A harness | *[name]* |
| 1–2 | Feature pipeline and basis proxy | *[name]* |
| 2–3 | Decomposition model, walk-forward estimation | *[name]* |
| 3 | Arm B context corpus; arm C prompt assembly | *[name]* |
| 4 | Arm D agent and tool interface | *[name]* |
| 5 | Run all arms (240 responses); κ check; scoring | all |
| 6 | Analysis; societal and philosophical drafting | *[name]* |
| 7 | Report and presentation | all |

**Dependencies.** API access to two models — the binding constraint, secured in week 1.
The CFTC dataset is already ingested, verified and version-pinned.

**Deliberately out of scope.** We do not test whether the decomposition predicts future
returns. Its role is honest description, not forecasting, so no predictive-inference
apparatus is required.

**Fallback.** If arm D cannot be built in time we ship A, B and C — which alone give a
baseline, two controlled variations and three testable hypotheses — and name D as the most
informative next experiment. Arm B is retained under any cut, because without it a win for
C cannot be distinguished from the effect of information alone. If H1 fails and the
baseline is already correct, the project becomes locating the boundary: sparser context,
less common contracts, and multi-turn conversations where an early framing persists.

## 7. AI-use plan

| Tool | Purpose | How outputs are checked |
|---|---|---|
| LLMs under test | Object of study, not authority | Outputs are data, scored against CFTC ground truth |
| Claude Code | Pipeline, harness, decomposition model | Code reviewed and tested; 58 automated tests; data reconciled against official CFTC archives |
| LLM assistants | Drafting, structuring, literature leads | Every factual claim and citation retrieved and verified at source |

No claim in the report rests on an LLM's assertion that something is true. Prompts and
outputs that materially changed our method or conclusions are retained in the evidence
log. The dataset is public; no personal or confidential data is used.

---

## References

*To be verified at source before submission; see §3 verification note.*

1. Commodity Futures Trading Commission. *Traders in Financial Futures* reports. Public
   reporting dataset `gpe5-46if`. [verified — primary data source]
2. Fishe, R. & Smith, A. (2012). Identifying informed traders in futures markets.
   *Journal of Financial Markets*. [academic]
3. Ji, Z. et al. (2023). Survey of hallucination in natural language generation. *ACM
   Computing Surveys*. [academic]
4. Lewis, P. et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP
   tasks. *NeurIPS*. [academic]
5. Schick, T. et al. (2023). Toolformer: language models can teach themselves to use
   tools. [academic]
6. Parasuraman, R. & Riley, V. (1997). Humans and automation: use, misuse, disuse, abuse.
   *Human Factors*. [academic]
7. Matthias, A. (2004). The responsibility gap: ascribing responsibility for the actions
   of learning automata. *Ethics and Information Technology*. [academic]
8. Federal Reserve / Office of Financial Research analyses of the Treasury cash–futures
   basis trade. [institutional — cite specific publications]
