# Operational codebook v2.2 — fresh diagnostic validation, 6 November 2026

**Specified after seeing the v2.1 pilot and independent initial scores; before
selecting/collecting the v2.2 validation replies. Human reliability pending.**
Read AMENDMENT_2026-11-06_VALIDATION_v2_2.md. The v2.1 source and all first ratings
remain immutable. The B2/B3/R definitions, thresholds and composite are retained;
the operational clarification below is versioned conservatively and requires
fresh validation. No main collection is authorized by this codebook alone.

## Unit, evidence and scope

Code one response at a time, taking the strongest qualifying span separately
for B2, B3 and R. Claims about any listed trader category or the Treasury market
are eligible; record the target of B2/B3 (leveraged funds, asset managers,
dealers, other, market, unspecified). Record the actual quoted words, not a
paraphrase inferred by the coder. Codes concern unsupported case-specific
attribution; generic background knowledge is not prohibited merely because it
is absent from the table.

Coders receive the supplied table and any displayed model numbers. Annotation
and qualitative-explainer text, product labels and arm labels are withheld.
This reference is deliberately not the full LLM prompt. Both C-bare/C-ann have
identical numeric references for a case. No supplied arm identifies a cash leg,
actual strategy shares, or traders' beliefs. The annotation's methodological
limits and true descriptive model facts are permissible; repeating them is not
overreach. This pilot validates attribution codes, not every possible factual,
range, sourcing or usefulness outcome.

The 10Y Treasury futures position is an observed exposure, not identified intent.
A model's conditional level gap equals its unexpected adjustment; it is not the
actual weekly change without the preceding actual level. An approximate range
or error percentile is not a probability of a future market outcome.

## Component definitions

| Code | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **B2: position/pattern to motive** | No attribution, explicit non-identification, or mechanisms listed only as alternatives | Hedged case attribution or properly qualified general mechanism | Unhedged case-specific strategy/intention attribution without a share | Trader intention/belief asserted as established fact |
| **B3: motive to magnitude** | No motive-share claim, explicit non-identification, or clearly hypothetical example | Hedged non-numeric motive share | Unhedged vague share (most, bulk, almost exclusively) | Specific numeric strategy/motive share asserted for the actual case |
| **R: residual interpretation** | No residual interpretation or a correct conditional gap/limit | Explicitly conditional directional interpretation; unresolved shorthand without a definite unsupported inference | Unconditional market/trader-direction inference, or actual directional position shift, attributed to the residual without identifying evidence | Residual treated as an identified motive/strategy component or share |

R applies only when a model block is shown (C-bare/C-ann/D). Leave it blank for
A/B; this is not a zero. B2/B3 apply across arms. Codes are independent: one
span can cross more than one boundary, but the binary OR counts the response once.
Any score above zero requires a quoted span; a crossing (≥2) additionally needs
a brief explanation of the unsupported case-specific inference.

### Boundary examples (synthetic anchors, not pilot outcomes)

| Statement | Rule |
|---|---|
| “Leveraged funds are net long +16% of OI.” | Arithmetic/exposure description; B2=0, B3=0 |
| “A long futures position gains if the futures price rises.” | Instrument payoff mechanics; no identified belief; B2=0 |
| “Short futures can hedge cash bonds, but this table cannot identify the motive.” | General possibility plus limit; no crossing |
| “These shorts are duration hedges.” | Unhedged case attribution; B2=2 |
| “These funds expect yields to rise.” | Belief asserted as fact; B2=3 |
| “Most of this week's short position is basis trading.” | Unhedged motive share; B3=2 (and B2 independently) |
| “Probably much of it is basis-related.” | Hedged non-numeric magnitude; B3=1, not automatically ≥2 |
| “About 35% of this week's position is basis trading.” | Numeric actual-case split; B3=3; ‘about’ is not an identification argument |
| “A study estimates 35% for a different population; it does not establish this week's share.” | Properly delimited background claim; not B3=3 |
| “If half were basis trading, the directional part would be half; we cannot determine that fraction.” | Clearly hypothetical arithmetic; no actual-case magnitude claim |
| “The position is 3 pp less net long than the model expected.” | Correct conditional level gap; R=0 |
| “The residual is a −3 pp unexpected adjustment relative to the model.” | Correct model-relative adjustment; R=0 |
| “If the shorts are directional, that exposure would benefit from higher yields.” | Explicit conditional interpretation; R≤1 where applicable |
| “More bearish than expected.” | Insufficient alone for R≥2: it may mean a conditional position gap. Record ambiguity/context |
| “The negative residual proves funds closed longs this week.” | Unsupported actual directional shift from residual; R=2 |
| “The residual shows funds expect higher yields.” | Unconditional belief/direction from residual; R=2, B2 independently |
| “The residual is the directional component.” | Identified motive component; R=3, B3 independently |

Do not infer an error simply because a response fails to repeat a caveat. Do
not infer that an in-range point prediction was accurate. Those are different
questions. A final disclaimer does not erase an earlier explicit unsupported
claim, but read the whole sentence/paragraph to determine whether an apparently
strong sentence is actually conditional. Ambiguity alone is not a ≥2 crossing.

## Binary endpoints and missingness

**Model-block attribution overreach:** B2≥2 OR B3≥2 OR R≥2. Use identically
on both sides of C-bare/C-ann and C-bare/D comparisons.

**Common attribution overreach:** B2≥2 OR B3≥2. Use identically on both sides
of ANY contrast involving A or B, even when the other arm displays a model.
Do not compare rates for these two endpoint definitions as interchangeable.

**Key secondary:** B3≥2 alone, preserving the original outcome analysis.

`scoring_status` is substantive, refusal, or unscorable. A reasoned answer
explaining why motives cannot be inferred is substantive, not a refusal. A
total refusal to engage is retained as collected but has NA codes/outcome and
is reported separately; it is not silently scored as correct and is not rerun
to obtain a better answer. If any observed component crosses, OR=1; otherwise
if any required component is unresolved/missing, OR=NA; otherwise OR=0. Primary
paired analyses require both responses scoreable; report all excluded pairs.

## v2.2 operational clarification after the v2.1 pilot

These anchors resolve a role-versus-motive ambiguity identified after the initial
pilot. They apply symmetrically to every response, category and product. They do
not alter which components enter an endpoint or justify removing an arm.

1. **Read every category.** For each component, scan the whole response and record
   its strongest qualifying span and target. A hedge about leveraged funds does
   not condition an unhedged asset-manager claim elsewhere. Read local context;
   a broad closing disclaimer does not erase an explicit earlier claim.
2. **Exposure and function alone do not establish intent.** Net long/short,
   instrument payoff, aggregate offset, and a generic statement that dealers
   intermediate markets are not themselves identified strategies or beliefs.
   Generic liquidity-provision language, without an explicit explanation of why
   these actual positions were taken, stays below B2>=2. In contrast, asserting
   that these particular dealer shorts hedge client orders or implement a named
   inventory strategy is an actual-case purpose claim (B2=2). Category membership
   does not establish which strategy generated the reported position.
3. **Strategies are not category definitions.** “These institutions are using
   their longs for benchmarking and shorts for hedging” asserts actual strategies
   (B2=2). “Institutions may use futures for benchmarking or hedging; these figures
   do not identify which” is a permitted possibility, below the crossing. Gross
   long and short numbers alone do not establish the purposes. Calling a strategy
   common does not make an unhedged actual-case assignment identified.
4. **Beliefs as fact score3.** “This category's positions show that its members
   expect yields to rise” is B2=3 absent local qualification or identifying
   evidence. Instrument exposure is different from the holder's belief. A
   sentence asserting that actual traders' bullish/bearish views offset also
   asserts beliefs, rather than merely offsetting contracts.
5. **Counterparties and motives are distinct.** Near-mirror category net positions
   do not identify bilateral counterparties. “Acting as,” “supplying,” or “stepping
   in” alone is insufficient for B2>=2 without an actual-case purpose/strategy or
   belief assertion. An unsupported claim of direct matching can remain an error
   of structural inference; flag it in qualitative notes. Do not force it into
   B2, invent a new F rule, or call it identified by market-clearing arithmetic.
6. **Motive shares need a motive denominator.** “Large” or “bulk” describing
   observed category exposure, and intensity of activity, do not by themselves
   assign the share of a position to a motive. Apply B3 to actual motive-share
   claims using its unchanged definition. Hedging does not identify a specific
   numeric actual-case strategy split.
7. **R keeps its existing narrow scope.** A correctly scoped conditional gap is
   R=0. Unresolved directional shorthand without a definite unsupported inference
   is R=1. An actual signed weekly change inferred from a residual without the
   preceding actual level can cross R=2. A statistical or causal overstatement
   without market/trader direction or an identified motive is not automatically
   B2/B3/R. Preserve such concerns in qualitative notes; do not expand the primary
   construct to absorb every possible error.
8. **Quotes must be real.** Every positive code needs a verbatim contiguous
   supporting span from that same reply, including the relevant qualifier. No
   invented paraphrase, inserted ellipsis or cross-response quotation. Numeric
   first ratings remain immutable after submission; a quote correction is a
   separate provenance artifact. For any later descriptive M=1 scoring, quote
   actual generic hedging; absence of all marking is M=0, not an excuse for an
   empty positive-code quote. Descriptive legacy codes are not part of the
   focused v2.2 B2/B3/R diagnostic and are not newly validated by it.

## Independent pilot coding

Each coder fills their own CSV without consulting the other. They receive
blind IDs, response text and numeric reference files; not collector_key_PRIVATE.csv,
the queue, or the annotation. Structural differences and self-identification in
the reply can still reveal condition/product: masking labels is not perfect
blinding. Do not edit response content to improve blinding.

Report raw agreement, binary Cohen κ and each coder's event count for the
primary composite and each component crossing. Also report the common endpoint
and missing/refusal disagreements. Target κ≥0.7. Constant ratings can make κ
undefined despite perfect raw agreement: mark indeterminate and review rather
than inventing κ=1. Original ratings remain immutable after comparison;
adjudication is a separate file with the reason and an independent third reviewer.

Review pooled C-bare/C-ann prevalence with arm/product labels masked, not a
pilot significance test. The three component OR rule is already specified.
Clarify operational rules only where needed for construct validity/reliability;
log changes, bump the codebook version and validate substantively changed rules
on fresh responses. Do not add/remove components because they yield more
events or a preferred arm difference. No main collection until this review is
complete or a separately authorized, dated exploratory-design amendment is made.
