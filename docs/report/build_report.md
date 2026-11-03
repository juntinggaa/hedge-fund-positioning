# Project Build Report

## What has been built, what has been verified, and the exact state of the machine-learning component

META Repository: juntinggaa/hedge-fund-positioning (private) | Branch: main | Head commit: ad60892
META Report date: 3 November 2026 | Course: NST2046 Generative AI and Society
META Author of this report: Claude Code (Opus 5). Every number below was recomputed or re-run on the report date unless marked otherwise.

---

## 1. Executive summary

Read this section first; it contains the one thing that matters most.

**The machine-learning model is specified, scaffolded, tested for leakage safety, and not
fitted.** No estimator has been trained on this data. There is no out-of-sample R-squared, no
residual series, no positioning "surprise" and no predictive result, because the fourteen
functions that would produce them raise `NotImplementedError` by design. What exists is the
statistical architecture around the model: the walk-forward splitter that decides which
observations a model may ever see, the as-of-date and release-date logic that defines a
legitimate prediction window, and the content-hash machinery that pins the data vintage a fit
would be reproducible against. That architecture is complete and covered by 58 passing tests.

This is a deliberate ordering, not an abandoned effort. The leakage guards were built first
because a fitted model with a leak is worse than no model: it produces a number that looks
like a finding.

**The role of the model also changed mid-project, and this is the most important design fact
in the repository.** The original project made the ML model the result: decompose
leveraged-fund Treasury positioning into an explained component and a residual, then test
whether the residual predicts returns. Under the course requirements the project was
re-scoped to an audit of how large language models interpret institutional positioning data.
The ML model survived the re-scope but changed job entirely. It is no longer asked to be
*right*. It is now a **stimulus generator**: its expected-position and residual output is the
experimental material handed to an LLM in two of four conditions, precisely to find out
whether a plausible-looking quantitative output causes the model to manufacture a causal
story the number cannot support.

That inverts the usual quality requirement. A forecasting project needs the model to be
accurate. This project needs it to be *honest about what it is*, because the thing under test
is whether an LLM respects the limits of a statistic that asserts nothing about causation.

**What is verified and finished:** the data layer. 1,057 weekly CFTC observations for 10-Year
Treasury Note futures, 2006-06-13 to 2026-09-08, reconciled against CFTC's own official
archives with zero mismatches, pinned by SHA-256 content hash which still matched on the
report date.

**What is evidence, not plan:** three pilot LLM runs were executed and the project's original
central hypothesis was falsified by them. That falsification is reported in the proposal
rather than hidden, and the research design was rebuilt around what the pilots actually showed.

---

## 2. Module-by-module state

CODE
File                              Lines  State         Tests
--------------------------------------------------------------------
src/hfpos/ingest/cftc.py            254  implemented   yes
src/hfpos/ingest/cftc_archive.py    126  implemented   yes
src/hfpos/manifest.py                90   implemented   yes
src/hfpos/timing.py                  85   implemented   yes
src/hfpos/stage1/walkforward.py      80   implemented   yes
src/hfpos/config.py                  28   implemented   indirect
scripts/draw_sample.py               89   implemented   no
scripts/run_pilots.py               125  implemented   no
--------------------------------------------------------------------
src/hfpos/features/build.py          15   scaffold      no
src/hfpos/features/basis.py          18   scaffold      no
src/hfpos/features/momentum.py       15   scaffold      no
src/hfpos/features/macro.py          15   scaffold      no
src/hfpos/stage0/leadlag.py          15   scaffold      no
src/hfpos/stage1/models.py           17   scaffold      no
src/hfpos/stage1/run.py              19   scaffold      no
src/hfpos/stage2/predict.py          24   scaffold      no
src/hfpos/stage2/inference.py        19   scaffold      no
src/hfpos/eval/metrics.py            15   scaffold      no
src/hfpos/eval/bootstrap.py          16   scaffold      no
src/hfpos/eval/plots.py              17   scaffold      no
src/hfpos/ingest/prices.py           16   scaffold      no
src/hfpos/ingest/fred.py             16   scaffold      no
CODE

"Scaffold" means: module docstring stating the method, the known traps and the decision
rationale, plus a typed function signature that raises `NotImplementedError` with its issue
number. Fourteen such call sites exist. They are deliberately loud: nothing silently returns
a placeholder number that could leak into a write-up.

**Test status, re-run on the report date:** 53 offline tests pass, 5 network tests pass, 58
total, no failures, no skips. The network tests are the ones that hit the live CFTC endpoint
and re-check the reconciliation, so passing them means the cross-source agreement still holds
today and is not a stale claim from September.

---

## 3. The machine-learning model

### 3.1 What it is asked to do

One supervised model, one target, one job: predict what leveraged-fund positioning in 10-Year
Treasury futures *would ordinarily be*, given observable market conditions in that week. The
part it cannot predict is the residual.

The model is explicitly **not** a strategy decomposition. It does not and cannot separate
basis trades from directional bets, because the cash leg of the basis trade is not in the
CFTC futures dataset at all. This distinction is the entire reason the project exists in its
current form, and it is stated three ways in the proposal: explained is not caused; total
model fit is not the contribution of any single regressor; and the residual is not
directional, since it also contains misspecification, omitted variables and data error.

### 3.2 Specification

CODE
Target        d(Net / Open Interest), leveraged funds, weekly first difference
Horizon       contemporaneous (the model explains this week's change)
Estimators    Ridge, Lasso, XGBoost -- all three reported, not just the winner
Features      lagged returns 1/4/12w; realized volatility; yield levels and
              changes (2/5/10/30Y); 10Y-2Y slope; curvature; SOFR-IORB spread;
              cash-futures basis proxy; change in open interest; lagged own
              position level and change; VIX; roll-week dummy; FOMC-week dummy
Validation    expanding window, min 260 weeks of training, refit every 13 weeks
Config        all of the above lives in config.yaml, not in code
CODE

**Why the target is scaled by open interest rather than raw contracts.** Open interest in this
contract is not stationary across the sample: it ranges from 888,595 contracts (week ending
2009-02-24) to 6,254,472 (2026-05-26), a factor of **7.04**. A model trained on raw net
contracts would spend its capacity learning that the market got bigger. Note one correction
to the earlier project plan, which described this growth as "an order of magnitude": the
verified figure is 7.0x, not 10x. The design decision is unaffected; the wording was loose.

**Why the first difference rather than the level.** The level of net/OI has a lag-1
autocorrelation of **0.991**. Predicting it is almost free and almost meaningless: last
week's value is a near-perfect forecast. The first difference has a lag-1 autocorrelation of
**-0.154**, which is a genuine prediction problem. This is also why the LLM sample of 40
weeks is spaced at least eight weeks apart -- at 0.991, adjacent weeks are near-duplicate
stimuli.

**Three estimators, all reported.** With roughly 1,000 observations and 20-40 features, the
linear models may well beat XGBoost. The plan commits in advance to reporting that if it
happens, as a finding about the data rather than a failure of the project. Nothing in the
write-up depends on the gradient-boosted model winning.

### 3.3 The walk-forward estimator: the one ML component that is finished

`src/hfpos/stage1/walkforward.py` is implemented and is the single point through which every
guard against look-ahead bias routes. Two properties are enforced by tests.

**Property 1 -- training data lies strictly before the test block.** No fold ever trains on an
observation at or after the first predicted week.

**Property 2 -- an embargo gap separates them.** This is the subtle one. A forward-looking
target labelled at week *t* is not fully observed until week *t+h*. Training on weeks within
*h* of the test block therefore leaks the answer, even though those weeks are nominally in
the past. Stage 1 targets are contemporaneous and take embargo 0; any Stage 2 test at horizon
*h* must pass embargo *h-1*.

CODE
def split(self, n):
    idx = np.arange(n)
    for start in range(self._first_test_start(), n, self.step):
        train_end = start - self.embargo
        yield Split(train=idx[:train_end], test=idx[start : start + self.step])
CODE

Verified behaviour on the real sample length of 1,057 weeks: **62 folds**, **797 predicted
weeks** at embargo 0, and **794** at embargo 3 (the 4-week-horizon setting). Test blocks tile
the tail of the sample contiguously -- no gaps, no overlap, every eligible observation
predicted exactly once -- which is what makes the out-of-sample R-squared a single honest
number rather than an average over arbitrary splits.

The accompanying rule, stated in the module and in the plan: anything fitted on training data
-- feature scalers, hyperparameters, feature selection -- is fitted **inside** the loop, per
fold. There are no exceptions, and this is the most common way published forecasting results
turn out to be wrong.

### 3.4 The two gates the model must pass before it is allowed into the experiment

These are pre-committed, and either one can kill the ML component.

**Gate 1 -- Stage-1 out-of-sample R-squared.** If it is near zero, the model explains nothing,
the residual is just the raw series with extra steps, and there is no decomposition to hand
the LLM.

**Gate 2 -- correlation between the residual and the raw change in net/OI.** If this exceeds
roughly 0.9, the "removal of normal positioning" is cosmetic. The plan requires this number
in the main text, not an appendix, on the reasoning that any competent reader will compute it
themselves.

Both gates are scheduled before the arms that depend on them, and the proposal already names
the fallback if they fail: ship the two arms that need no model (raw data, and qualitative
market-structure context), which still constitute a baseline, a controlled variation and two
testable hypotheses.

### 3.5 Statistical hazards the design handles

**Generated-regressor problem.** In the original Stage 2, the regressor *is itself an
estimate*, so ordinary standard errors are wrong (Pagan 1984). With an ML first stage there is
no analytic correction. The design's answer is to block-bootstrap the **whole pipeline**,
refitting Stage 1 inside every replication: stationary bootstrap, mean block 13 weeks, 1,000
replications, seed 20260918. Bootstrapping only the second stage does not fix this and is the
most likely point of attack in an oral examination.

**Overlapping returns.** The 2- and 4-week horizons overlap, so residuals are serially
correlated by construction. Newey-West with lag >= h-1, or Hodrick standard errors.

**Multiplicity.** One pre-registered primary test, unadjusted. Everything else --
3 groups x 4 horizons x 4 maturities is roughly 48 tests -- is adjusted (Romano-Wolf or
Benjamini-Hochberg) with the family size stated. At 5% you expect two or three false
positives in that family by construction.

**Power, stated in advance.** Roughly 797 test weeks, but only about 199 non-overlapping ones
at a 4-week horizon. A realistic incremental R-squared in this literature is 1-2%. The plan
writes that down beforehand so that a small effect is read as a small effect rather than as
failure.

### 3.6 The failure mode the model is now designed to provoke

In the re-scoped project the model's output becomes an experimental stimulus, and the specific
error being hunted is **causalisation of a residual**. Given an actual position of -3.2m, an
expected -2.6m and a residual of -0.6m, an LLM may report something like *"81% is attributable
to basis trading, 19% to directional bearishness."*

Every element of that sentence is unwarranted, and the model asserted none of it. The chain
the project traces is:

QUOTE quantitative tool -> apparently precise output -> LLM causalises the statistic -> confident explanation -> user sees unjustified certainty

Two of the four experimental conditions exist to measure this: one hands over the
expected-position and residual numbers unlabelled, the other hands over the identical numbers
plus one sentence stating what a residual does and does not mean. If the single sentence
repairs the failure, the problem is a design choice rather than an inherent property of fluent
generation -- which is a sharper and more useful result than a general complaint about
hallucination.

### 3.7 What finishing the model actually requires

In dependency order, with the hard part named honestly.

CODE
1  Price ingest and roll handling          prices.py        ZN=F is a stitched
                                                            front-month series;
                                                            naive weekly returns
                                                            inject a false jump at
                                                            every quarterly roll
2  FRED ingest                             fred.py          routine
3  Basis proxy                             basis.py         THE HARD ONE -- see below
4  Momentum and macro features             momentum/macro   routine
5  Feature assembly onto the Tuesday grid  build.py         alignment care needed
6  Lead-lag check (do positions follow     leadlag.py       must run BEFORE any
   returns?)                                                model is fitted
7  Estimators and walk-forward driver      models/run.py    harness already exists
8  Gate diagnostics                        run.py           decides the rest
CODE

**Item 3 is harder than everything else combined.** The claim "we modelled conditions
favouring basis trading" rests entirely on a proxy for the cash-futures basis, and the
preferred construction (cheapest-to-deliver implied repo against general-collateral repo)
needs the deliverable basket and conversion factors. The fallback ladder, best first, is: CTD
implied repo vs GC repo; futures-implied yield vs cash yield; swap spreads; SOFR-IORB spread.
SOFR data begins only in 2018, so the early sample needs a lower rung regardless. And the
basis trade was small before roughly 2015, which means "conditions favouring basis trading"
is not the same quantity in 2008 as in 2024. The repository records which rung was used and
requires the claim to be downgraded to match.

**Item 6 is a trap worth naming.** If leveraged-fund positioning merely *follows* returns, then
a feature set without lagged returns produces a "surprise" that is really just momentum in
disguise. That is why the lead-lag check is sequenced before any fitting rather than reported
as a robustness check afterwards.

---

## 4. The data layer

This part is finished, and it is the part the rest of the project stands on.

CODE
Source        CFTC Traders in Financial Futures, futures-only (dataset gpe5-46if)
Contract      10-Year Treasury Note futures, market code 043602  [flagship]
Also pinned   2Y 042601 | 5Y 044601 | 30Y 020601
Coverage      1,057 weekly observations, 2006-06-13 to 2026-09-08
Integrity     SHA-256 content hash, re-verified against the manifest on 2026-11-03: MATCH
Cross-check   reconciled against CFTC's official annual archives across 2,310 cells
              in 2012, 2019, 2024 and 2025 -- zero mismatches
CODE

**The contract-code trap, found the hard way.** CFTC renamed the 10-Year contract in February
2022, from "10-YEAR U.S. TREASURY NOTES" to "UST 10Y NOTE". Filtering the dataset by contract
*name* returns 817 rows or 240 rows instead of 1,057 -- silently, with no error. The ingest
therefore filters by numeric market code only, and a test asserts that a placeholder code
fails loudly rather than returning an empty frame.

**Two data irregularities, recorded rather than smoothed over.** 14 of the 1,057 snapshots are
not dated on a Tuesday (holiday weeks shift the as-of date), and 22 week-to-week gaps are
irregular. An earlier version of the timing module raised an exception on any non-Tuesday
as-of date, which means it would have crashed on live data; it now resolves the release date
as the next Friday from any business day. Both counts are stored in the data manifest.

### Verified descriptive facts

These are the numbers the LLM experiment's stimuli are drawn from, recomputed on the report
date.

CODE
Leveraged funds net SHORT                   695 of 1,057 weeks   (65.8%)
  mean net position when short                        -17.0% of open interest
Leveraged funds net LONG                    362 of 1,057 weeks
Asset managers net LONG                                  75.1% of weeks
  mean net position when long                          +18.2% of open interest
Most negative week in the sample            2025-09-02, -48.53% of open interest
Lag-1 autocorrelation of net/OI                                     0.991
Lag-1 autocorrelation of d(net/OI)                                 -0.154
Open interest range                   888,595 to 6,254,472 contracts (7.04x)
CODE

The 362 net-long weeks matter for the experiment design: they supply the **sign-flip control**.
If an LLM produces the basis-trade narrative on a week when leveraged funds were net long, the
narrative is template-driven rather than evidence-driven.

---

## 5. The Milestone 1 research design, in brief

**Research question.** When LLMs interpret institutional Treasury futures positioning, how
reliably do they distinguish observed evidence, statistical inference, and claims about trader
motive -- and does quantitative model output improve that distinction or create new forms of
false causal confidence?

**Four conditions**, run at a frontier tier and a free tier:

CODE
A        CFTC positioning and observable market data only
B        A + market-structure mechanism, stated WITHOUT any magnitudes
C-bare   A + ML expected position and residual, unlabelled
C-ann    C-bare + one sentence on what a residual does and does not mean
CODE

Condition B must state the mechanism without asserting a proportion. If it hands over a
magnitude, it has given away the very claim the experiment measures and the comparison with
the C conditions is confounded.

**Primary outcome is which boundary was crossed, not a single error rate.** Three boundaries
are coded separately -- data to statistical inference, inference to mechanism, mechanism to
magnitude -- each at severity 0 to 3, with the scale anchored on verbatim pilot responses so
coders calibrate against evidence rather than intuition. A model can clear the first two
boundaries and fail the third, which is exactly what the pilots showed; one combined rate
would have hidden the finding.

**Sampling and scale.** 40 weeks, ten per stratum, stratified across position state and
basis-trade era, spaced at least eight weeks apart, drawn by a seeded script that writes the
full list to `docs/milestone1/sample.csv`. 40 weeks x 4 arms x 2 tiers = **320 responses**.
The pilot week is held in a separate purposive frame rather than quietly counted in the
stratified draw, because it sits 7 days from a drawn week and would violate the spacing rule.

**Analysis.** Paired design, so the primary test is McNemar on discordant pairs per contrast.
Power depends on how many cases change between arms rather than on n. Absolute rates carry
roughly a +/-16 percentage-point margin at n=40: adequate for large effects, not for subtle
ones. The proposal says so explicitly and calls this an exploratory audit rather than a
population estimate.

---

## 6. Pilot evidence, and the hypothesis it killed

Three pilot runs were executed, all on the week ending 2 September 2025, the most extreme
week in the entire sample.

CODE
#  Arm         Tier       Run by          Result
-------------------------------------------------------------------------
1  A bare      frontier   me, via browser hedged, severity 1
2  B grounded  frontier   me, via browser hedged
3  A bare      free       the user        OVERCLAIMED, severity 2
CODE

**The frontier model, with no prompting about basis trades, said:** that hedge funds often
short Treasury futures as one leg of the cash-futures basis trade, that such a position is not
necessarily a bet that yields will rise, and that it would therefore not conclude from the
CFTC numbers alone that hedge funds expect yields to soar. It also computed -48.5% of open
interest exactly.

**The free model, on identical data, asserted** that the bulk of the position reflects
execution of the Treasury basis trade -- a proportional claim its input cannot support, since
the cash leg is absent from the data -- and described open interest as "over 60%" where the
verified figure is 59.88%.

**Consequence: the original hypothesis was falsified before any of the seven project weeks
were spent on it.** The naive prediction was that models would misread a large short as a
directional bearish view. They did not. The real failure is narrower and more interesting:
**boundary-crossing** -- stating inference in the register of observation. The research design
was rebuilt around that, and the falsification is reported in the proposal rather than
quietly dropped.

The pilot's own limits are recorded with it: n=1 per cell, a web interface that exposes no
model version string or token counts, no configurable sampling parameters, and
"Unpersonalized" mode, which is not the mode a real retail user is in.

---

## 7. Verification log

What was actually checked, and by what means.

CODE
Claim                                  How verified                     Status
---------------------------------------------------------------------------------
58 automated tests pass                re-run on report date            CONFIRMED
Data vintage unchanged                 SHA-256 vs pinned manifest       CONFIRMED
API matches CFTC official archives     2,310 cells, 4 years             CONFIRMED
Contract codes correct                 live endpoint + failing-code test CONFIRMED
Descriptive statistics in this report  recomputed from cached parquet   CONFIRMED
Citations (9 sources)                  publisher records, 18 Sep 2026    bibliographic
                                                                        details only
Pilot responses                        run live, logged verbatim        CONFIRMED
ML out-of-sample performance           NOT RUN -- no model fitted       OPEN
CODE

**Things this report deliberately does not claim.** No ML performance number exists, so none is
quoted. The nine citations have had their bibliographic details verified at source and one
retrieved in full, but their *substantive* claims still need checking against full text before
submission. The free-tier run of condition B -- the missing fourth cell of the 2x2 -- has not
been executed, and it speaks directly to one of the hypotheses.

Two corrections I made during the work are worth recording, since both were my errors:
I overstated the roll-date risk in the price series (tested afterwards: roll months account
for 20% of the largest weekly moves, below the 33% baseline you would expect by chance), and
I claimed sampling temperature would be "fixed and logged" when current frontier models no
longer accept a temperature parameter at all. The proposal now runs replicates and reports
variation instead.

---

## 8. Open items

CODE
1  Fill bracketed placeholders in the proposal: teammate names, date, owners
2  Run condition B at the free tier -- the missing cell of the 2x2
3  Trim the appendix from 2 pages to the 1-page limit
4  Upload the .docx to Google Drive for teammate editing (needs a human; no
   connector is attached to this session)
5  Verify substantive claims of all 9 citations against full text
6  Retire or rewrite the 18 GitHub issues that still describe the abandoned
   forecasting project
7  Confirm the re-scope with the teaching team if they are reachable
CODE

Items 1 and 2 are the only ones that block submission quality. Item 2 is the one that would
most improve the evidence base, and it costs a single prompt.

---

## Appendix: reproducing everything in this report

CODE
# install dependencies into the project venv
uv pip install -r requirements.txt pytest

# offline tests (53)
.venv/bin/python -m pytest -q

# live-endpoint reconciliation tests (5)
.venv/bin/python -m pytest -m network -q

# redraw the stratified 40-week sample (deterministic, seed 20260918)
.venv/bin/python scripts/draw_sample.py

# the LLM pilot harness (needs ANTHROPIC_API_KEY, not set in this environment)
.venv/bin/python scripts/run_pilots.py --replicates 3
CODE

Every number the analysis depends on lives in `config.yaml` rather than in code, and the data
vintage is pinned by content hash in `data/manifests/`. A fit that cannot be reproduced against
that hash is not a result.
