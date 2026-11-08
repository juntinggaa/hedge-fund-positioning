# Candidate examples (agreed machine codes; verify against the reply before quoting)

## 1. Baseline overreach (arm A, table only)

Both coders agree: motive or share asserted from the table alone.

**GEM-059** (GEM, A, week 2025-06-24)
- B2=3 (Codex): "While a portion of this reflects directional bets on higher yields (stickier inflation or heavy Treasury supply), the primary driver of a short position of this magnitude is the **cash-futures basis trade**." — Asserts that actual leveraged funds are betting on higher yields without evidence identifying their beliefs.
- B2=2 (Claude): "the data indicates an entrenched basis trade ecosystem" — Unhedged claim that the actual leveraged-fund short is basis trading, inferred from mirror-image net positions without a cash leg.
- B3=2 (Codex): "the primary driver of a short position of this magnitude is the **cash-futures basis trade**." — Assigns basis trading the predominant role in generating the actual short position without strategy-share evidence.
- B3=2 (Claude): "the primary driver of a short position of this magnitude is the **cash-futures basis trade**" — Unhedged vague majority share ('primary driver') of the actual short assigned to basis trading.

**GEM-007** (GEM, A, week 2025-04-15)
- B2=2 (Codex): "They short futures (-540k net) to hedge the interest rate risk of their cash bond holdings and over-the-counter (OTC) interest rate swaps." — Assigns the actual dealer short position to hedging unobserved cash bonds and swaps.
- B2=2 (Claude): "Hedge funds step in as the arbitrage counterparty." — Unhedged assignment of basis-arbitrage purpose to the actual leveraged-fund short.
- B3=2 (Codex): "However, the sheer scale—over 2 million gross short contracts against just 201k long—is overwhelmingly structural arbitrage." — Attributes an overwhelming share of actual leveraged-fund positioning to structural arbitrage without strategy-share evidence.
- B3=2 (Claude): "However, the sheer scale—over 2 million gross short contracts against just 201k long—is overwhelmingly structural arbitrage." — Unhedged vague share ('overwhelmingly') of the actual short assigned to arbitrage.

**CLA-023** (CLA, A, week 2026-09-08)
- B2=2 (Codex): "Leveraged funds sell that rich future and buy the cheapest-to-deliver cash Treasury, financing the bond in repo." — Assigns an actual cash-futures basis strategy and financing arrangement without observing the cash leg.
- B2=2 (Claude): "Leveraged funds sell that rich future and buy the cheapest-to-deliver cash Treasury, financing the bond in repo." — Unhedged assertion that the actual leveraged-fund short is basis trading, with no cash-leg data.
- B3=2 (Codex): "The headline pattern is the cash-futures basis trade, and it’s large. These positions mostly reflect market structure, not a directional view on yields." — Attributes most of the actual positioning to the stated basis-trade structure without identifying strategy shares.
- B3=2 (Claude): "Their futures short is largely offset by long cash positions this report" — Unhedged vague share ('largely') of the actual short assigned to cash-hedged basis trades.

**GEM-039** (GEM, A, week 2016-07-12)
- B2=2 (Codex): "Their slight net-long bias reflects momentum/CTA strategies riding the mid-2016 drop in global yields, largely offset by relative-value shorts." — The reply assigns momentum/CTA and relative-value strategies to the actual leveraged-fund positions without identifying evidence.
- B2=3 (Claude): "Fast-money accounts are fiercely divided on the direction of 10-year yields" — Asserts as fact that actual leveraged-fund traders hold divided views on yield direction (beliefs), not identified by the table.
- B3=2 (Codex): "The CFTC Traders in Financial Futures (TFF) report for July 12, 2016 reveals a **healthy, two-way institutional market dominated by hedging and relative-value trading** rather than one-sided speculative crowding." — The reply asserts that hedging and relative-value strategies dominate this actual market without evidence identifying their share.
- B3=2 (Claude): "a large share of leveraged fund short and long positions consists of **cash-futures basis trading**" — Unhedged vague share of the actual leveraged-fund positions assigned to basis trading.

(27 cases in total)

## 2. Annotation works: same week, C-bare overreaches, C-ann does not

Paired weeks; C-bare reply first, then the C-ann reply for the same week and product.

**CLA-033** (CLA, C-bare, week 2021-11-02)
- B2=2 (Codex): "a net long here reflects ordinary portfolio construction rather than a market call." — Assigns the actual asset-manager net long to portfolio construction without identifying its purpose.
- B2=2 (Claude): "Pension funds, insurers and bond funds use futures to add duration cheaply, so a net long here reflects ordinary portfolio construction rather than a market call." — Unhedged assignment of a purpose (ordinary portfolio construction / adding duration) to this week's actual asset-manager net long.
- B3=1 (Claude): "Positions taken just ahead of a widely anticipated FOMC decision partly reflect event hedging" — Non-numeric, weak share ('partly') of positions assigned to event hedging; not a majority-share claim.
- R=1 (Codex): "At most it is a mild hint that funds were holding back relative to whatever the model’s inputs implied." — Offers a hedged interpretation of restraint relative to the model.
- R=1 (Claude): "At most it is a mild hint that funds were holding back relative to whatever the model" — Model-relative framing, but 'holding back' is directional/intent shorthand without a definite unsupported inference.

**CLA-052** (CLA, C-ann, week 2021-11-02)
- B2=1 (Codex): "Their gross short of about 499k contracts could still contain substantial basis positions offset by longs held for other reasons, and netting hides that." — Qualifies basis positioning as a possibility.
- B2=1 (Claude): "Long 10-year futures positions as part of flattening trades would fit that backdrop, but this data can’t confirm it." — Hedged with explicit non-confirmation.
- B3=1 (Codex): "Their gross short of about 499k contracts could still contain substantial basis positions offset by longs held for other reasons, and netting hides that." — Suggests a substantial but explicitly hedged, non-numeric basis share within gross shorts.
- B3=1 (Claude): "Their gross short of about 499k contracts could still contain substantial basis positions offset by longs held for other reasons, and netting hides that." — Hedged ('could') non-numeric magnitude.

**GEM-041** (GEM, C-bare, week 2019-05-07)
- B2=2 (Codex): "Asset managers systematically use Treasury futures to add duration efficiently without tying up balance sheet cash, providing the structural bid on the other side of the basis trade." — Assigns these asset-manager positions a duration-acquisition purpose and a role in an actual basis trade without identifying evidence.
- B2=2 (Claude): "Asset managers systematically use Treasury futures to add duration efficiently without tying up balance sheet cash, providing the structural bid on the other side of the basis trade." — Unhedged assignment of purpose to actual asset-manager longs and assertion that they are the other side of an actual basis trade.

**GEM-031** (GEM, C-ann, week 2019-05-07)
- B2=1 (Codex): "Asset managers also account for the largest spreading total (**767,698 contracts**), reflecting active calendar-roll or intra-contract relative-value management alongside their directional net long footprint." — The sentence offers alternative purposes without choosing between them.
- B2=1 (Claude): "reflecting active calendar-roll or intra-contract relative-value management alongside their directional net long footprint" — Spreading described with alternatives ('or'); largely definitional.

**GEM-006** (GEM, C-bare, week 2021-08-31)
- B2=3 (Codex): "moderately bullish price positioning (expecting lower or stable yields) among speculative and real-money accounts" — Asserts actual speculative and institutional expectations of lower or stable yields from their futures exposure.
- B2=3 (Claude): "moderately bullish price positioning (expecting lower or stable yields) among speculative and real-money accounts" — Asserts as fact that leveraged funds and asset managers expect lower or stable yields, a belief, without hedging.
- R=1 (Claude): "your model confirms that speculative long positioning is slightly elevated relative to baseline fundamentals (+1.74% residual)" — Model-relative directional shorthand ('elevated relative to baseline fundamentals'); no definite unsupported actual shift or motive.

**GEM-046** (GEM, C-ann, week 2021-08-31)
- B2=1 (Codex): "Because the **cash Treasury leg is unobserved**, leveraged funds could be holding these long futures against short cash Treasury positions (a reverse basis or curve trade), hedging swap books, or adjusting cross-maturity spreads." — Explicitly hedged alternative mechanisms.
- B2=1 (Claude): "This indicates intense intra-market positioning (such as calendar-roll activity ahead of the September delivery cycle or portfolio duration matching) rather than simple one-way directional betting."
- R=1 (Claude): "While the +1.74 pp residual leans bullish/long on the futures leg, it is statistically routine"

(36 cases in total)

## 3. Failure: overreach despite the annotation (C-ann)

The annotation states the model does not identify motives or shares; the reply still asserts one.

**CLA-008** (CLA, C-ann, week 2021-01-26)
- B2=2 (Codex): "Taken alone, this report describes a market with lots of two-way, mostly hedged activity." — The reply identifies the actual market activity as hedged without observing the offsetting economic exposures.
- B2=2 (Claude): "Most of this open interest reflects offsetting exposures, hedges and spreads rather than outright bets on yields." — Unhedged claim that the actual positions are mainly hedges rather than directional bets, which futures-only data cannot identify.
- B3=2 (Codex): "Most of this open interest reflects offsetting exposures, hedges and spreads rather than outright bets on yields." — The reply assigns most actual open interest to a nondirectional mixture including hedges without identifying its motive composition.
- B3=2 (Claude): "Most of this open interest reflects offsetting exposures, hedges and spreads rather than outright bets on yields." — Unhedged vague share ('Most') assigning actual open interest to hedging/non-directional motives.

**GEM-055** (GEM, C-ann, week 2014-09-02)
- B2=2 (Codex): "Diverse strategies within this bucket (macro directional, trend-following, relative-value, and cash-futures basis trading) are largely offsetting each other in the aggregate net count." — The reply assigns named strategies to the actual leveraged-fund books without identifying which strategies generated the positions.
- B2=2 (Claude): "Diverse strategies within this bucket (macro directional, trend-following, relative-value, and cash-futures basis trading) are largely offsetting each other in the aggregate net count." — Asserts without hedging that named strategies generated and offset the actual gross positions.
- R=2 (Codex): "During the week ending September 2, 2014, Leveraged Funds either liquidated long futures or initiated new short futures at a pace far exceeding their normal historical response to observed price action, volatility, and curve moves." — The reply infers actual weekly long liquidation or short initiation from the residual without the preceding actual position.
- R=2 (Claude): "During the week ending September 2, 2014, Leveraged Funds either liquidated long futures or initiated new short futures at a pace far exceeding their normal historical response to observed price action, volatility, and curve moves." — Infers an actual directional weekly position shift (liquidating longs/adding shorts) from the residual without the preceding actual level.

**GEM-026** (GEM, C-ann, week 2025-08-19)
- B2=2 (Codex): "Real-money institutions (pension funds, mutual funds, insurance companies) are heavily utilizing futures to add duration and lock in yields without deploying full cash upfront." — The reply assigns actual asset-manager positions the purposes of adding duration and locking in yields without identifying those purposes.
- B2=2 (Claude): "Real-money institutions (pension funds, mutual funds, insurance companies) are heavily utilizing futures to add duration and lock in yields without deploying full cash upfront." — Unhedged assignment of purpose to the actual asset-manager long.
- R=2 (Codex): "Because 47% of historical out-of-sample errors were at least this large, the extra shorting represents standard week-to-week noise rather than a structural shock or regime break." — The reply treats the negative residual as actual extra shorting without the preceding actual net position.
- R=1 (Claude): "Conversely, if a large portion of the residual (-1.40 percentage points) reflects directional shorting, the market is modestly more vulnerable to a short squeeze should macroeconomic data surprise to the downside." — Conditional ('if') directional/motive reading of the residual.

**GEM-014** (GEM, C-ann, week 2017-07-03)
- B2=2 (Codex): "At the same time, asset managers hold 939,893 short contracts and the largest spreading book (477,453 contracts), reflecting heavy two-way hedging and calendar/curve management alongside their net duration demand." — Infers actual hedging and curve-management purposes from asset managers' gross and spreading positions.
- B2=2 (Claude): "reflecting heavy two-way hedging and calendar/curve management alongside their net duration demand" — Assigns hedging purpose to asset managers' actual gross shorts from gross numbers alone, unhedged.

(10 cases in total)

## 4. Residual misread (R>=2, C arms)

The model residual treated as an actual directional shift or a motive.

**GEM-034** (GEM, C-bare, week 2026-09-08)
- R=2 (Codex): "The +1.94 pp positive residual suggests that, at the margin, hedge funds have either trimmed tactical directional shorts (anticipating softer growth/inflation or lower yields) or slightly scaled back basis-trade arbitrage due to tighter implied repo spreads or dealer balance-sheet constraints heading into the September quarterly futures roll." — Both alternatives infer actual reductions in short strategies from the positive residual without the preceding actual position.
- R=2 (Claude): "The +1.94 pp positive residual suggests that, at the margin, hedge funds have either trimmed tactical directional shorts (anticipating softer growth/inflation or lower yields) or slightly scaled back basis-trade arbitrage" — Infers an actual reduction of positions (and associated beliefs/strategies) from the residual without the preceding actual level.

**GEM-055** (GEM, C-ann, week 2014-09-02)
- R=2 (Codex): "During the week ending September 2, 2014, Leveraged Funds either liquidated long futures or initiated new short futures at a pace far exceeding their normal historical response to observed price action, volatility, and curve moves." — The reply infers actual weekly long liquidation or short initiation from the residual without the preceding actual position.
- R=2 (Claude): "During the week ending September 2, 2014, Leveraged Funds either liquidated long futures or initiated new short futures at a pace far exceeding their normal historical response to observed price action, volatility, and curve moves." — Infers an actual directional weekly position shift (liquidating longs/adding shorts) from the residual without the preceding actual level.

**GEM-017** (GEM, C-bare, week 2014-09-02)
- R=2 (Codex): "Hedge funds have already pared back their longs." — Infers an actual reduction in longs from the model-relative gap without a preceding actual position.
- R=2 (Claude): "Hedge funds have already pared back their longs." — Infers an actual directional position cut from the residual without the preceding actual level.

**GEM-047** (GEM, C-bare, week 2014-09-30)
- R=2 (Codex): "The positioning data and model output reveal a distinct institutional split between real-money duration buyers and speculative short sellers, with leveraged funds leaning noticeably more bearish on prices (expecting higher yields) than baseline model drivers predict—though still within normal historical bounds." — Uses the model-relative gap to assert actual expectations of higher yields.
- R=2 (Claude): "leveraged funds leaning noticeably more bearish on prices (expecting higher yields) than baseline model drivers predict" — Infers trader belief/direction from the residual without identifying evidence.

(6 cases in total)

## 5. Counterexample: ChatGPT stays near zero

ChatGPT replies flagged by both coders (rare).

**GPT-001** (GPT, A, week 2021-01-26)
- B2=2 (Codex): "The 26 January 2021 report portrays a Treasury market characterized by cautious positioning, substantial hedging activity, and no dominant speculative directional bet." — The conclusion asserts substantial actual hedging activity without evidence identifying the purposes of the positions.
- B2=2 (Claude): "characterized by cautious positioning, substantial hedging activity, and no dominant speculative directional bet" — Bottom line asserts without hedging that the actual market positions reflect substantial hedging activity, a strategy the table cannot identify.
- B3=1 (Codex): "The substantial offsetting long and short positions indicate that much of the activity may reflect hedging, spread trading, and relative-value strategies rather than straightforward directional speculation." — The magnitude attributed to strategies is hedged by may.
- B3=1 (Claude): "much of the activity may reflect hedging, spread trading, and relative-value strategies rather than straightforward directional speculation" — Hedged non-numeric share ('much ... may').

**GPT-007** (GPT, A, week 2025-04-15)
- B2=2 (Codex): "The CFTC positioning data for 15 April 2025 suggests a Treasury market characterized by extreme positioning divergence, a substantial leveraged basis trade, and vulnerability to disorderly deleveraging." — The opening assigns a substantial actual leveraged basis trade to the market without observing the cash or repo legs.
- B2=2 (Claude): "suggests a Treasury market characterized by extreme positioning divergence, a substantial leveraged basis trade, and vulnerability to disorderly deleveraging" — Under rule 11, 'suggests' followed by a named strategy (a substantial leveraged basis trade) assigns the actual-case strategy without hedging.
- B3=1 (Codex): "A major reason for this divergence is likely the Treasury cash-futures basis trade." — The major contribution assigned to basis trading is hedged by likely.
- B3=1 (Claude): "plausibly reflecting widespread use of leveraged cash-futures basis trades rather than simply bearish expectations for Treasuries"

(2 cases in total)

## 6. Counterexample: C-bare worse than A in the same week

Adding model numbers without the annotation increased overreach.

**CLA-027** (CLA, C-bare, week 2021-01-26)
- B2=2 (Codex): "The data says more about how the market is structured, with asset managers holding duration through futures and hedge funds running offsetting relative-value books, than about where Treasury yields were likely headed." — The closing sentence asserts that these hedge funds are running relative-value books without identifying their actual strategies.
- B2=2 (Claude): "with asset managers holding duration through futures and hedge funds running offsetting relative-value books" — Bottom line assigns, without hedging, a relative-value strategy to the actual leveraged-fund positions (cash leg unobserved).
- B3=1 (Codex): "Much of that is likely relative-value activity, such as curve, calendar or cash-futures basis trades, rather than a view on yield direction." — The non-numeric motive-share claim is hedged by "likely".
- B3=1 (Claude): "Much of that is likely relative-value activity, such as curve, calendar or cash-futures basis trades, rather than a view on yield direction." — Hedged ('likely') non-numeric share.

**CLA-051** (CLA, C-bare, week 2016-07-12)
- B2=2 (Codex): "Their gross figures (867k long, 1.05m short, 397k spreading) also point to hedging and relative-value activity." — The reply assigns hedging and relative-value purposes to the actual asset-manager positions from gross figures alone.
- B2=2 (Claude): "Their gross figures (867k long, 1.05m short, 397k spreading) also point to hedging and relative-value activity." — Unhedged 'point to' assigning named strategies (hedging and relative value, conjunctively) to the actual asset-manager positions from gross figures alone.

(2 cases in total)
