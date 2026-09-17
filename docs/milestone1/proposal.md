# Where does the evidence end?

### Observed data, statistical inference, and unsupported claims about motive in LLM interpretation of institutional positioning

**NST2046 Group Project — Milestone 1: Investigation Proposal**
Group: *[names]* · *[date]*

---

## 1. Question and claim

**Research question.** When LLMs interpret institutional Treasury futures positioning, how
reliably do they distinguish observed evidence, statistical inference, and claims about trader
motive — and does quantitative model output improve that distinction or create new forms of
false causal confidence?

The domain is chosen because the boundary is unusually sharp. CFTC data records *positions*,
never *purposes*. A large leveraged-fund short may be a directional bet, or one leg of the
cash–futures basis trade — $830bn, 35% of hedge funds' $2.4tn long Treasury exposure as of
September 2025 (Monin 2026). Crucially, **no amount of CFTC futures data can resolve the
split**: the cash leg is not in the dataset. Any claim about the proportion is inference.

**We have already tested the naive version of this and falsified it.** In pilot runs
(Appendix B), both a frontier model and a free-tier model raised the basis trade *unprompted*
and computed the positions exactly. Neither said "hedge funds are bearish." But the free model
asserted that **"the bulk reflects execution of the Treasury Basis Trade"** — a proportional
claim its input cannot support — while the frontier model hedged to *"probably substantially
for basis purposes."* The failure is therefore not ignorance but **boundary-crossing**: stating
inference in the register of observation.

| | Hypothesis |
|---|---|
| **H1** | Models breach the *mechanism → magnitude* boundary far more often than the *data → inference* boundary: they compute correctly, then quantify motive without warrant. |
| **H2** | Qualitative grounding suppresses simplistic errors but may *increase* sophisticated unsupported claims, by supplying a mechanism to over-apply. |
| **H3** | Quantitative grounding either improves calibration **or** induces causalisation of the residual. **We do not predict the direction.** |
| **H4** | Annotating what the residual means materially changes the rate of causalisation. |

**Provisional claim.** Fluency erases epistemic boundaries. A user receives CFTC fact,
statistical relationship, plausible mechanism and model-generated speculation in one seamless
paragraph, delivered in a single confident register, with nothing marking where each ends.

## 2. System and mechanism

**Technical object.** A four-condition workflow around instruction-tuned LLMs, run at a
frontier tier and a free tier. Current frontier models no longer accept `temperature` or other
sampling parameters, so runs cannot be pinned deterministic; we run replicates and report
variation instead.

| Arm | Receives | Isolates |
|---|---|---|
| **A** | CFTC positioning and observable market data | What is inferred from evidence alone |
| **B** | A + market-structure explanation, **mechanism only, no magnitudes** | Does domain knowledge calibrate, or license storytelling? (H2) |
| **C-bare** | A + ML expected-position and residual, unlabelled | Does quantitative output induce causalisation? (H3) |
| **C-ann** | C-bare + a statement of what the residual does and does not mean | Does labelling prevent it? (H4) |

B must state the mechanism without asserting any proportion; otherwise it hands the model the
magnitude claim and the C comparison is confounded.

**Intervention mechanism.** A supervised model predicts expected leveraged-fund positioning
from market state — basis conditions, momentum, rate level and curve, volatility, funding
spreads — by expanding-window walk-forward estimation, so no fitted value uses data unavailable
at the time. The residual is the portion the model does not explain.

**The causalisation error we are looking for.** Given actual −3.2m, expected −2.6m, residual
−0.6m, a model might report *"81% is attributable to basis trading, 19% to directional
bearishness."* That is unjustified three times over: **explained is not caused** (the model
predicts position from conditions, it does not decompose by strategy); **total fit is not any
single regressor**; and **the residual is not directional** — it is misspecification, omitted
variables and data error, of which information is at most one part. The ML model asserts none of
it. The socio-technical chain is precise:

> quantitative tool → apparently precise output → LLM causalises the statistic → confident
> explanation → user sees unjustified certainty

## 3. Prior work

**Positions are not purposes.** Monin (2026) and OFR Working Paper 21-01 document leveraged
funds holding large short futures against long cash positions, arbitrage rather than direction
dominating. Fishe & Smith (2012, *Journal of Financial Markets*), using confidential data on
8,921 traders, find business category a weaker guide to information than observed behaviour.

**Fluent text can be unfaithful, and retrieval is the standard repair.** Ji et al. (2023, *ACM
Computing Surveys*) establish that fluency does not track accuracy; Lewis et al. (2020, *NeurIPS*)
introduced retrieval-augmented generation and Schick et al. (2023) tool use, both offered as
remedies. Whether either repairs *epistemic calibration* rather than factual recall is not
established — and our pilot suggests recall was never the problem.

**Over-trust and responsibility.** Parasuraman & Riley (1997) show operators accept automated
recommendations against contrary evidence, most strongly among non-experts. Matthias (2004) frames
the responsibility gap for systems whose behaviour no party both foresaw and controlled.

> **Verification note.** Bibliographic details for all nine sources were checked against
> publisher records on 18 September 2026; the Monin FEDS Note was retrieved in full. Substantive
> claims are to be confirmed against full text before final submission. No claim rests on an
> LLM's report of what a paper says.

## 4. Technical investigation plan

**Data.** CFTC *Traders in Financial Futures*, 10-Year Treasury Note futures (`043602`): 1,057
weekly observations, 2006-06-13 to 2026-09-08, ingested from the CFTC public reporting API,
reconciled against CFTC's official archives across 2,310 cells with zero mismatches, pinned by
content hash.

**Sampling.** 35 weeks, stratified across position state and basis-trade era rather than drawn
at random, and spaced at least eight weeks apart because positioning is strongly autocorrelated.
Strata and drawn weeks are listed in Appendix A; the draw is scripted and reproducible.

**Primary outcome — which boundary was crossed.** Not a single "error rate". Each response is
coded for crossings of three distinct boundaries:

| Boundary | A crossing looks like |
|---|---|
| Data → statistical inference | "this is unusually large" (no baseline supplied) |
| Inference → mechanism | "this is basis trading" |
| Mechanism → magnitude | "the bulk of it is" · "81% is" |

A model can clear the first two and fail the third — which is precisely what the pilot showed —
so a single rate would hide the finding.

**Severity scale**, anchored on real pilot responses so coders calibrate against evidence
rather than intuition:

| | Behaviour | Pilot anchor |
|---|---|---|
| 0 | Marks the limit explicitly | *"the CFTC data alone cannot establish how much"* |
| 1 | Hedged attribution | *"probably substantially for basis purposes"* (frontier) |
| 2 | Unhedged proportional claim | *"the bulk reflects execution of the Basis Trade"* (free) |
| 3 | Asserted as fact | *"hedge funds are overwhelmingly bearish"* |

**Controls.** A **sign-flip** case — one of the 362 weeks where leveraged funds are net *long* —
tests whether the basis-trade narrative appears regardless of the data, which would show it is
template-driven. **Stability**: ten replicates of one case per arm, with hedge-terms mapped to the
severity scale *before* running; if the claimed proportion drifts while evidence is fixed,
confidence is generated rather than derived. **Tier**: the free model runs the C arms specifically,
since causalisation is likelier there and testing C only at the frontier risks missing it.

**Analysis.** Paired design — every week goes to every arm — so the primary test is **McNemar
on discordant pairs** per contrast. Power depends on how many cases change between arms, not on
n. Absolute rates carry roughly a ±16 percentage-point margin at n=35; enough for large effects,
not subtle ones. This is an exploratory audit, not a population estimate.

**Coding protocol.** Full three-boundary coding on a stratified subset of 60 responses,
double-scored with Cohen's κ reported; binary screening on the rest, licensed only if κ ≥ 0.7.

**No predetermined outcome.** C improving calibration means structured evidence helps; C matching
B means the ML tool was unnecessary and context sufficed; C inducing causalisation means
quantitative grounding manufactured false confidence — the most consequential result available to
us. We pre-commit to reporting whichever occurs.

## 5. Societal and philosophical stakes

**The harm, traced.** A retail investor asks why Treasury yields are moving. The system replies
that 81% of hedge-fund positioning is basis trading and 19% directional bearishness. They
conclude that institutional money is not really short duration, decide against hedging their
bond exposure, and are wrong in the one direction that costs them. No step in that chain
involves a factual error the user could have caught: the positions were right, the mechanism was
real, and only the *proportion* was invented — the one element carrying no epistemic marking.

**Stakeholders.** Non-expert investors; students and journalists using LLMs as explainers; advisers
whose clients arrive with model-generated views. The harm is asymmetric: a professional has
Bloomberg, Fed research and colleagues who will say *the data cannot tell you that*. The non-expert
has one fluent paragraph.

**Normative question.** *What duty does a generative system have to mark the boundary between what
is observed, what is statistically inferred, and what is merely plausible — when the user cannot
detect that boundary themselves?* Human testimony carries accountability, and a speaker's
confidence usually tracks their competence; an LLM's confident register is a property of its
training objective, not its evidential position. Matthias's responsibility gap is normally argued
from opacity. Our design tests a sharper version: if a one-line annotation (arm C-ann) repairs the
failure, it was neither unforeseeable nor uncontrollable and the gap narrows to a design choice;
if annotation fails, the problem is structural to fluent generation.

## 6. Feasibility and roles

**Weeks 1–4** — coding scheme and codebook, A/B harness, feature pipeline and basis proxy
(*[name]*); decomposition model by walk-forward estimation, C-bare and C-ann assembly (*[name]*).
**Weeks 5–7** — run all arms at both tiers, replicates, sign-flip control, κ check, analysis,
societal drafting, report and presentation (all). Every member codes responses.

**Dependencies.** API access at two tiers — the binding constraint, secured in week 1. The CFTC
dataset is already ingested, verified and version-pinned. **Out of scope:** we do not test whether
the decomposition predicts returns; its role is description. A planned agentic arm is dropped —
whether an agent electing to call a tool differs from one handed the same output is an engineering
question that broadens the project past seven weeks.

**Fallback.** If the decomposition model is not ready we ship A and B — a baseline, a controlled
variation, two testable hypotheses. If all arms prove well-calibrated, that is a reportable negative
result.

## 7. AI-use plan

**LLMs under test** are the object of study, not an authority: outputs are data, coded against §4.
**Claude Code** builds the pipeline, harness and decomposition model and assists drafting — checked
by 58 automated tests and by reconciling data against CFTC's archives; the group verifies every
citation and reruns the pilots. **LLM assistants** gave question development and literature leads;
two earlier designs were rejected against course requirements and pilot evidence. No claim rests on
an LLM's assertion that something is true, and prompts that materially changed our method are kept
in the evidence log.

---

## References

*Bibliographic details verified against publisher records, 18 September 2026.*

1. Commodity Futures Trading Commission. *Traders in Financial Futures* (futures-only). Public reporting dataset `gpe5-46if`. Reconciled against CFTC annual archives. [primary data]
2. Monin, P. J. (2026). Decomposing hedge funds' U.S. Treasury exposures. *FEDS Notes*, Board of Governors of the Federal Reserve System, 22 June 2026. [institutional]
3. Office of Financial Research (2021). Hedge funds and the Treasury cash–futures disconnect. *OFR Working Paper 21-01*. [institutional]
4. Fishe, R. P. H. & Smith, A. D. (2012). Identifying informed traders in futures markets. *Journal of Financial Markets*, 15(3), 329–359. doi:10.1016/j.finmar.2011.08.006 [academic]
5. Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A. & Fung, P. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*, 55(12), Article 248. doi:10.1145/3571730 [academic]
6. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S. & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 33*. arXiv:2005.11401 [academic]
7. Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N. & Scialom, T. (2023). Toolformer: language models can teach themselves to use tools. *NeurIPS 36*. [academic]
8. Parasuraman, R. & Riley, V. (1997). Humans and automation: use, misuse, disuse, abuse. *Human Factors*, 39(2), 230–253. doi:10.1518/001872097778543886 [academic]
9. Matthias, A. (2004). The responsibility gap: ascribing responsibility for the actions of learning automata. *Ethics and Information Technology*, 6(3), 175–183. doi:10.1007/s10676-004-3422-1 [academic]
