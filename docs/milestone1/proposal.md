# When the machine reads the market wrong

### Directional attribution errors in LLM interpretation of institutional futures positioning

**NST2046 Group Project — Milestone 1: Investigation Proposal**
Group: *[names]* · *[date]*

---

## 1. Question and claim

Retail investors increasingly ask general-purpose LLMs to interpret financial data. We
investigate one setting where the correct interpretation is counter-intuitive and the
data is public, verifiable, and unambiguous.

**Research question.** When a large language model is asked to interpret CFTC *Traders
in Financial Futures* data on U.S. Treasury futures, does it attribute directional
market views to positioning that is substantially non-directional — and what follows
for non-expert users who treat the answer as financial guidance?

The setting is chosen because the naive reading is wrong in a specific, documented way.
Leveraged funds hold very large *short* positions in Treasury futures. The intuitive
reading — "hedge funds expect bond prices to fall" — is substantially incorrect: a
large share of that position is the cash–futures **basis trade**, in which the fund
simultaneously holds the underlying Treasury security. The position expresses an
arbitrage, not a directional view. Federal Reserve research attributes a substantial
share of hedge-fund Treasury exposure to such strategies.

We therefore test three competing hypotheses:

- **H1.** Given positioning data without additional context, the model characterises
  large leveraged-fund net shorts as bearish directional views at a high rate.
- **H2.** Supplying basis-trade context in the prompt materially reduces that rate.
  This distinguishes a *knowledge* deficit from an *application* deficit: whether the
  model does not know, or knows but does not invoke what it knows.
- **H3.** Asked about specific weeks, the model states positioning figures that are
  fabricated rather than declining to answer.

**Provisional claim.** The model reproduces the dominant association in its training
distribution (*net short → bearish*) rather than the market-specific exception, and
presents the result with unwarranted confidence. The harm is not that the model is
sometimes wrong; it is that the error is *systematic, confident, and invisible to the
user who most needs the correction*.

## 2. System and mechanism

**Technical object.** Two instruction-tuned LLMs accessed via API at pinned model
versions, recorded exactly in the final report, with temperature and all sampling
parameters fixed and logged. We treat the deployed model-plus-prompt as the system
under test, not the base architecture.

**Input → representation → output chain.** The input is a prompt containing a tabular
extract of one week of TFF data (dealer, asset manager, leveraged fund long/short/
spread positions, plus open interest) and a question asking what the positioning
implies. The model tokenises this and, conditioned on that context, generates output
autoregressively. Generation is a next-token prediction shaped by the training
distribution, in which "large short position" co-occurs overwhelmingly with bearish
interpretation, because that inference is correct in most markets. Treasury futures
are an exception created by market structure — the basis trade — that is
under-represented relative to the general pattern.

The mechanism we claim, and will test, is therefore: **the model regresses to the modal
association in its training data rather than applying the market-specific exception,
and the fluency of the output carries no signal that this substitution occurred.**

## 3. Prior work

Four strands establish what is known and what is contested.

**Institutional positioning is not equivalent to directional belief.** Federal Reserve
and Office of Financial Research analyses of the Treasury cash–futures basis trade
document leveraged funds holding large short futures positions against long cash
positions. Academic work on informed trading in futures markets (Fishe & Smith, 2012,
*Journal of Financial Markets*) further finds that a trader's business category is a
weaker guide to their information than their observed behaviour — reinforcing that
category-level positions do not license simple intent claims.

**LLMs generate fluent but unfaithful text.** The hallucination literature (Ji et al.,
2023, *ACM Computing Surveys*) establishes that generated content can be confidently
stated and factually unsupported, and that fluency is uncorrelated with accuracy.

**Users over-trust automated outputs.** Work on automation bias (Parasuraman & Riley,
1997) shows operators accept automated recommendations even against contrary evidence,
with effects strongest for non-experts under time pressure.

**Machine assertion raises unresolved normative questions.** Matthias (2004) on
responsibility gaps in learning systems frames the question of who is answerable when
an adaptive system's output causes harm and no party both foresaw and controlled it.

*What is contested.* Whether current models fail on domain-specific exceptions of this
kind, and whether prompt context repairs the failure, is not established for this
setting. That gap is what we test.

> **Verification note.** Every source above must be independently retrieved and checked
> against the original before submission. No claim in this proposal rests on an LLM's
> report of what a paper says.

## 4. Technical investigation plan

**Data.** CFTC *Traders in Financial Futures* futures-only reports for the 10-Year
Treasury Note contract (market code `043602`), 1,057 weekly observations from
2006-06-13 to 2026-09-08. Ingested from the CFTC public reporting API and reconciled
against CFTC's official zip archives across 2,310 data cells spanning four years, with
zero mismatches. Ground truth is therefore fixed and independently checkable.

**Baseline.** A bare prompt: the week's positioning table plus "What does this
positioning suggest about the Treasury market?" No hint that non-directional
strategies exist.

**Controlled variations.** One factor changed at a time against that baseline:

| Variation | Tests |
|---|---|
| + basis-trade context in the prompt | H2: knowledge vs. application deficit |
| + explicit request for alternative explanations | Whether prompting for alternatives suffices |
| Second model, same prompts | Whether the failure is model-specific or general |
| Data presented as prose rather than a table | Whether format drives the reading |

**Test cases.** Purposively sampled, not random, to span the interpretive space:

1. **2025-09-02** — record leveraged-fund short, −48.5% of open interest. Maximum
   temptation to read as extreme bearishness.
2. A week where leveraged funds are net **long** (34.2% of weeks) — tests whether the
   model is reading the data or reciting a stock narrative.
3. A pre-2015 week, when the basis trade was small — the correct answer differs by era.
4. A **fabrication probe**: a plausibly-phrased question about a week beyond the data
   cut-off, testing H3.

**Outcome measures.** Each response is scored on a fixed rubric by two team members
independently, with disagreements recorded and adjudicated; we report inter-rater
agreement rather than assuming it:

1. **Directional attribution** — does the response assert a bullish/bearish view?
   (none / hedged / asserted)
2. **Alternative explanation** — is the basis trade or any non-directional motive
   raised unprompted? (binary)
3. **Numerical fidelity** — are stated figures correct against ground truth?
   (correct / approximate / fabricated)
4. **Calibration** — does stated confidence match evidential support?

**Expected failure modes.** High directional attribution in the baseline; basis trade
rarely raised unprompted; fabricated open-interest figures on the probe; confident
register throughout. We pre-commit to reporting these rates whatever they are.

## 5. Societal and philosophical stakes

**Stakeholders.** Retail investors using LLMs for market interpretation; financial
advisers whose clients arrive with model-generated views; regulators whose disclosure
regimes assume a human intermediary; model providers.

**Benefits.** Genuine and worth stating: these systems make institutional data legible
to people who would otherwise never open a CFTC report. The failure we study is the
cost of that access, not an argument against it.

**Harms, and their distribution.** The harm is asymmetric in a way that matters. A
professional reading the same data has Bloomberg, Fed research, and colleagues who will
say *that's the basis trade*. The retail user has the chatbot and nothing to check it
against — so the error lands precisely on those least able to detect it. Where
positioning data is published for market transparency, a systematic misreading layer
degrades the transparency the disclosure was meant to create.

**Normative question.** *Under what conditions is it reasonable to accept a machine's
assertion as testimony?* Human testimony carries accountability: a misleading adviser
can be challenged, and their confidence usually tracks their competence. An LLM's
confident register is a property of its training objective, not of its evidential
position, so the ordinary cue we use to calibrate trust is severed from what it
normally indicates. Matthias's responsibility gap sharpens this: if a retail investor
acts on a confident false claim, the provider disclaimed reliance, the user could not
have known, and the model has no beliefs to be culpable for — the harm occurs with no
locus of answerability. Our technical result determines whether this is a live problem
in this domain or a hypothetical one.

## 6. Feasibility and roles

| Week | Work | Owner |
|---|---|---|
| 1 | Test-case selection; prompt design; scoring rubric | *[name]* |
| 1 | API harness, pinned versions, logged outputs | *[name]* |
| 2 | Run baseline + variations; independent double-scoring | all |
| 2 | Societal and philosophical analysis drafting | *[name]* |
| 3 | Analysis, failure case write-up, report | all |

**Dependencies.** API access to two models (the binding constraint — secure in week 1);
the CFTC dataset, already ingested, verified, and version-pinned by content hash.

**Fallback.** If models handle the baseline correctly, H1 fails and the project becomes
*locating the boundary*: we escalate difficulty — sparser context, less common
contracts, multi-turn conversations where an early framing persists — and report the
conditions under which the reading breaks. A robust negative result is a reportable
finding and satisfies the Minimum Evidence Standard.

## 7. AI-use plan

| Tool | Purpose | How outputs are checked |
|---|---|---|
| LLMs under test | Object of study, not authority | Outputs are data; scored against CFTC ground truth |
| Claude Code | Data pipeline, harness, analysis code | Code reviewed and tested; 58 automated tests; data reconciled against official CFTC archives |
| LLM assistants | Drafting, structuring, literature leads | Every factual claim and citation retrieved and verified at the original source |

No claim in the report rests on an LLM's assertion that something is true. Prompts and
outputs that materially change our method or conclusions are retained in the evidence
log. The dataset is entirely public; no personal or confidential data is used.

---

## References

*To be verified at source before submission; see §3 verification note.*

1. Commodity Futures Trading Commission. *Traders in Financial Futures* reports.
   Public reporting dataset `gpe5-46if`. [verified — primary data source]
2. Fishe, R. & Smith, A. (2012). Identifying informed traders in futures markets.
   *Journal of Financial Markets*. [academic]
3. Ji, Z. et al. (2023). Survey of hallucination in natural language generation.
   *ACM Computing Surveys*. [academic]
4. Parasuraman, R. & Riley, V. (1997). Humans and automation: use, misuse, disuse,
   abuse. *Human Factors*. [academic]
5. Matthias, A. (2004). The responsibility gap: ascribing responsibility for the
   actions of learning automata. *Ethics and Information Technology*. [academic]
6. Federal Reserve / Office of Financial Research analyses of the Treasury
   cash–futures basis trade. [institutional — select and cite specific publications]
