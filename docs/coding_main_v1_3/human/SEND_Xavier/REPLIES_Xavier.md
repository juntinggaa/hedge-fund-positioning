# Replies for Xavier (15 replies)

Code each one in SHEET_Xavier.csv, same item number.

---

## Item 1 | X-1a6e030d2097 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 24 June 2025. All figures are numbers of contracts.

Open interest (all contracts): 4,918,411

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 239,668 | 601,200 | 23,979 | -361,532 | -7.35% |
| Asset Manager / Institutional | 2,791,767 | 716,605 | 540,268 | 2,075,162 | +42.19% |
| Leveraged Funds | 351,813 | 2,266,214 | 66,296 | -1,914,401 | -38.92% |
| Other Reportable | 458,728 | 354,804 | 1,692 | 103,924 | +2.11% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -41.90% of open interest (approximate 90% range based on earlier out-of-sample errors: -45.38% to -38.43%).
- Actual net position this week: -38.92% of open interest.
- Residual (actual minus expected): +2.98 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 84% were smaller than this one and 16% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

Short answer: this looks like a market with a large, mostly market-neutral relative-value trade, not a strong bet on rates. The model residual adds little.

### The big picture: a basis-trade structure

Asset managers are heavily net long (+42% of OI) and leveraged funds are almost equally net short (−39%). That mirror image is the classic signature of the cash–futures basis trade:

- Asset managers (pension funds, insurers, bond funds) get duration through futures because it’s cheaper on balance sheet and capital than holding cash bonds. Their demand tends to make futures slightly rich relative to cash Treasuries.
- Leveraged funds take the other side. They sell the rich futures and buy the cheaper deliverable cash bonds, usually financed in repo, and capture the small spread with heavy leverage.

So the −1.9 million contract leveraged short (roughly $190 billion face) should not be read as hedge funds betting on higher yields. Most of it is probably offset by long cash positions this report doesn’t show. Dealers’ modest net short (−7%) fits them hedging cash inventory or intermediating.

### What that implies for the Treasury market

The directional signal is weak, but the structural signal matters:

- Funding and liquidity sensitivity. A trade this size depends on cheap, stable repo and on dealer balance sheet. If repo rates spike, margins rise, or volatility jumps, funds may have to unwind fast. That means selling cash Treasuries into a market with limited intermediation capacity, which is what amplified stress in March 2020.
- Crowding. A position near 40% of open interest is concentrated. That raises the chance that a shock turns into forced, correlated selling rather than an orderly adjustment.
- Support for futures demand. The other side of the trade is real end-investor appetite for duration through futures, which is a mildly constructive signal about institutional demand.

### The model residual

Leveraged funds were about 3 points of OI less short than the model expected. Taken in context, that’s unremarkable:

- The actual value sits inside the 90% range (−45.38% to −38.43%).
- About 16% of past out-of-sample residuals were at least this large, so you’d expect a miss this size roughly one week in six.
- It’s a single observation. One week of slightly smaller shorts doesn’t show that the basis trade is unwinding. It could just as easily be noise, timing, or the model missing something.

At most, it’s something to watch. If the residual stayed positive and grew over several weeks, that could point to deleveraging or a narrowing of the futures–cash basis. One week doesn’t tell you that.

### Caveats

- Futures-only and one contract. Basis and curve trades span 2-, 5-, 10-year, Ultra and bond futures. The 10-year alone gives a partial picture, and the cash leg isn’t visible at all.
- Coarse categories. “Leveraged funds” mixes basis traders with genuine macro shorts, so some of the short may be directional.
- Stale data. This is June 2025 positioning, more than 16 months old as of today. It describes the market structure at that time, not current conditions.

Overall, the report points to a Treasury market supported by institutional duration demand and a large leveraged arbitrage. The main risk is a funding or volatility shock forcing that arbitrage to unwind, rather than any directional view.

---

## Item 2 | X-828822b996ea | R applicable: NO

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 25 November 2014. All figures are numbers of contracts.

Open interest (all contracts): 3,032,735

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 111,503 | 165,837 | 55,177 | -54,334 | -1.79% |
| Asset Manager / Institutional | 974,560 | 777,431 | 363,115 | 197,129 | +6.50% |
| Leveraged Funds | 513,347 | 727,518 | 159,499 | -214,171 | -7.06% |
| Other Reportable | 363,481 | 155,133 | 39,549 | 208,348 | +6.87% |

What does this positioning suggest about the Treasury market?

### REPLY

This CFTC Traders in Financial Futures (TFF) report shows a classic tug-of-war between real-money institutions and fast-money speculators, alongside two important structural warnings: an **implied net-short overhang among non-reportable traders** and potential **cash-futures basis distortions**.

Because 10-Year Treasury Note futures (ZN) are quoted in price, a **long position** is a bet on higher bond prices (lower yields), while a **short position** is a bet on lower bond prices (higher yields).

---

### 1. Cohort Breakdown & Market Sentiment

* **Asset Managers / Institutional (+197,129 net; +6.50% of OI):** Pension funds, endowments, insurance companies, and mutual funds dominate the market's footprint (holding ~32.1% of all long OI and ~25.6% of all short OI, plus 363,115 spreading contracts). Their net long position reflects structural demand for duration—either to match long-term liabilities, track benchmark bond indices, or lock in yields against disinflationary/low-growth headwinds.
* **Leveraged Funds (-214,171 net; -7.06% of OI):** Hedge funds and CTAs are the primary bearish cohort, betting on rising yields (falling prices) as the Federal Reserve wrapped up QE3 in late 2014 and moved toward rate normalization. However, **this is not pure directional shorting**: Leveraged Funds frequently short Treasury futures as the short leg of a **cash-futures basis trade** (buying cash Treasuries and selling futures) or to hedge long corporate credit/swap exposure.
* **Other Reportables (+208,348 net; +6.87% of OI):** Corporate treasuries, central banks, smaller proprietary desks, and uncategorized large traders hold the most asymmetric directional stance, with more than a **2.34-to-1 long-to-short ratio** (363,481 long vs. 155,133 short). Together with Asset Managers, they provide a massive wall of duration buying (+405,477 contracts combined).
* **Dealers / Intermediaries (-54,334 net; -1.79% of OI):** Sell-side banks hold a relatively modest net short position (~1.8% of OI). Rather than taking a massive directional bet, dealers are primarily warehousing client flow, hedging cash Treasury inventories built up around auctions, or offsetting interest rate swap books.

---

### 2. The Hidden Imbalance: Non-Reportable Traders

Because every futures contract has both a buyer and a seller, total open interest must sum to zero across the entire market. Summing the four reportable categories reveals what **Non-Reportable (small/retail) traders** are doing:

| Position Metric | Sum of 4 Reportable Categories | Total Open Interest | Implied Non-Reportable (Small Traders) |
| --- | --- | --- | --- |
| **Total Long (incl. Spreading)** | 2,580,231 | 3,032,735 | **452,504** (14.9% of OI) |
| **Total Short (incl. Spreading)** | 2,443,259 | 3,032,735 | **589,476** (19.4% of OI) |
| **Net Position** | **+136,972** (+4.52% of OI) | **0** | **-136,972** (-4.52% of OI) |

*Note: In CFTC TFF accounting, each "Spreading" contract represents both one long and one short contract held by the same trader across different maturities or contract months (totaling 617,340 spreading contracts across reportables).*

* **Takeaway:** Large reportable traders as a whole are net long **+136,972 contracts**, which mathematically forces Non-Reportable (smaller) traders to be net short **-136,972 contracts (-4.52% of OI)**. Both fast-money hedge funds and small traders are positioned on the short side, while institutional real money and large "Other Reportables" hold the long side.

---

### 3. Market Implications & Risks

1. **Elevated Short-Squeeze Risk (Asymmetric Upside in Prices / Downside in Yields):**
With Leveraged Funds (-214,171) and Non-Reportables (-136,972) holding a combined **-351,143 net short contracts (-11.58% of total OI)**, the bearish "higher yields" trade is crowded among price-sensitive, mark-to-market participants. If macroeconomic data disappoints or a global flight-to-safety occurs, Leveraged Funds and small specs are far more likely to be forced to cover shorts rapidly than Asset Managers are to dump core duration holdings.
2. **Heavy Curve & Roll Activity (Spreading = 20.36% of OI):**
The 617,340 contracts tied up in spreading (especially the 363,115 held by Asset Managers) is abnormally high because **late November is the quarterly roll window** from the December (ZNZ4) contract into the March (ZNH5) contract. First Notice Day for December Treasury futures falls at the end of November, meaning a large portion of open interest and spreading volume reflects calendar roll execution rather than new directional conviction.
3. **Cash-Futures Basis Caveat:**
Because the TFF report only captures futures positions, a portion of the Leveraged Fund short position and Asset Manager long position represents **structural basis trading**. Asset managers often prefer futures over cash bonds to gain duration efficiently without tying up balance sheet, while hedge funds step in as arbitrageurs—buying cheaper cash Treasuries (funded via repo) and selling futures to capture the basis. Thus, raw net futures figures slightly overstate pure directional macro bets on interest rates.

---

## Item 3 | X-2cb15542d0ce | R applicable: NO

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 31 August 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,946,457

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 221,815 | 246,372 | 45,195 | -24,557 | -0.62% |
| Asset Manager / Institutional | 1,478,799 | 1,346,863 | 784,122 | 131,936 | +3.34% |
| Leveraged Funds | 773,159 | 501,404 | 145,440 | 271,755 | +6.89% |
| Other Reportable | 130,111 | 291,443 | 27,350 | -161,332 | -4.09% |

What does this positioning suggest about the Treasury market?

### REPLY

The numbers point to a market that was not very crowded in either direction, with a mild long tilt among speculative money. They say more about who was using the contract and how than about a strong directional view.

Checking the numbers

The arithmetic holds. Every net figure is Long − Short, and the percentages match the stated open interest. One derived number is worth adding: the four categories together are net long 217,802 contracts, so the non-reportable (small trader) group, which isn’t in your table, must be net short about 218,000 (about −5.5% of OI). That makes small traders the largest net short group, bigger than “Other Reportable.”

What the positioning suggests

Nobody held an extreme net position. The largest net position, leveraged funds at +6.9% of OI, is small next to the gross positions, which run to hundreds of thousands or millions of contracts. Most of the open interest reflects hedging, relative-value trades and spreads rather than outright bets on yields. As a sentiment gauge, this looks moderate, not one-sided.

Leveraged funds leaned long duration (betting on lower yields). A net long of about 272k contracts is consistent with funds positioned for lower or range-bound 10-year yields. That fits the backdrop at the time. Yields had fallen from roughly 1.75% in March 2021 to around 1.2–1.3% by August, as markets bought into the Fed’s “transitory inflation” story and growth worries from the Delta variant. Still, a net long in one contract isn’t necessarily a duration bet. It could be one leg of a curve trade, such as long 10s against short 2s or 5s, which you’d only see by looking at the other tenors.

Asset managers were modestly long, as usual. Real-money investors routinely use futures to add duration cheaply, so a net long is their normal stance. A +3.3% net is on the light side, which suggests they were not aggressively extending duration.

Dealers were close to flat. At −0.6%, dealers look like intermediaries absorbing flow, not taking a view.

Other Reportable and small traders were the net shorts. This group includes hedgers such as smaller banks, corporates and some mortgage-related accounts, whose shorts often hedge cash bond or rate exposure rather than express a bearish view.

Caveats before drawing conclusions
Timing. Late August is the roll from September into December contracts. Open interest and spreading positions tend to swell then, which likely explains the very large spreading figures, especially asset managers’ 784k. Readings during a roll are noisy.
Pattern versus usual structure. In much of the post-2018 data I recall, asset managers carried large net longs and leveraged funds carried net shorts in Treasury futures, the short side of the cash-futures basis trade. A leveraged-fund net long larger than the asset-manager net long is unusual, so I’d check this against the original CFTC release. I can’t verify it here.
One week, one contract. The signal comes from changes over time and comparison with history, such as where today’s net sits relative to its multi-year range. It also comes from looking across the curve (2-, 5-, 10-year, Ultra 10, bond and Ultra bond), ideally weighted by duration risk rather than contract count.
Futures-only. Funds hedged in cash bonds or swaps can look directional in futures when they aren’t.
In hindsight

If speculators were leaning long, the positioning was soon tested. Powell’s Jackson Hole speech on 27 August opened the door to tapering, and 10-year yields rose toward about 1.5% in late September. Taper was formally announced in November 2021. The data didn’t show a crowded long, though, which is consistent with the selloff being orderly rather than a violent unwind.

If you have the prior weeks’ reports or the other Treasury contracts, I can compute the weekly changes and a curve-wide, risk-weighted picture, which would tell you much more than this snapshot.

---

## Item 4 | X-9a3a9ca8453c | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 30 September 2014. All figures are numbers of contracts.

Open interest (all contracts): 2,731,029

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 103,901 | 166,359 | 26,821 | -62,458 | -2.29% |
| Asset Manager / Institutional | 1,037,278 | 811,115 | 346,632 | 226,163 | +8.28% |
| Leveraged Funds | 483,601 | 581,677 | 51,789 | -98,076 | -3.59% |
| Other Reportable | 373,464 | 214,179 | 37,328 | 159,285 | +5.83% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -0.36% of open interest (approximate 90% range based on earlier out-of-sample errors: -4.10% to +3.39%).
- Actual net position this week: -3.59% of open interest.
- Residual (actual minus expected): -3.24 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 85% were smaller than this one and 15% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The CFTC positioning and model output for the week ending September 30, 2014 point to a **notably larger-than-expected net short shift by Leveraged Funds**, absorbed primarily by **Asset Managers and Other Reportable traders holding net long positions**. However, because the data only captures futures legs and relies on statistical associations with modest explanatory power, it cannot isolate whether this short buildup reflects directional bets on higher yields, curve trades, or cash-futures basis positioning.

---

### 1. Cross-Category Market Structure

Across the 2,731,029 contracts of total open interest, the four reportable categories show a clear divide between liquidity providers/speculators on the short side and institutional/other end-users on the long side:

* **Real-Money & Other Demand (Net Long):** **Asset Managers / Institutional** traders hold the largest footprint in the market—both directionally and via spreading (346,632 contracts)—with a net long position of **+226,163 contracts (+8.28% of OI)**. **Other Reportables** are also meaningfully net long at **+159,285 contracts (+5.83% of OI)**.
* **Speculative & Dealer Supply (Net Short):** **Leveraged Funds** are net short **-98,076 contracts (-3.59% of OI)**, while **Dealers / Intermediaries** are net short **-62,458 contracts (-2.29% of OI)**.
* **Non-Reportable Imbalance:** Summing the net positions of the four reportable categories yields a combined net long of **+224,914 contracts (+8.24% of OI)**. Because every long futures contract matches a short contract, **non-reportable (smaller) traders** must hold an offsetting net short position of **-224,914 contracts (-8.24% of OI)**—a larger collective net short than Leveraged Funds and Dealers combined.

---

### 2. What the Model Output Reveals About Leveraged Funds

The supervised model (v4.0) estimates where Leveraged Funds' net positioning would sit based on same-week market moves (yields, curve shape, volatility, funding stress), open-interest changes, a quarter-end indicator (September 30 is Q3 quarter-end), and lagged positioning:

* **Conditional vs. Actual Positioning:** Given the week's market environment and prior positioning, the model expected Leveraged Funds to hold a nearly flat net position of **-0.36% of OI**. Instead, actual positioning came in at **-3.59% of OI**.
* **A Sizable Negative Surprise (Residual):** The **-3.24 percentage point residual** (roughly 88,200 contracts more net short than conditionally expected, accounting for rounding) represents a substantial weekly adjustment toward the short side that is not explained by the model's standard macro, volatility, and quarter-end covariates.
* **Statistical Magnitude:** While the actual reading (-3.59%) falls inside the broad 90% historical error band (-4.10% to +3.39%), the residual is still quite large—exceeding the model's overall 2.07 percentage point RMSE and ranking in roughly the **top 15% of earlier out-of-sample absolute errors** (85th percentile). Being inside the 90% interval reflects the wide dispersion of weekly positioning swings rather than a close point prediction.

---

### 3. Key Analytical Caveats & What Cannot Be Inferred

When interpreting what this positioning means for the broader 10-Year Treasury market, the model diagnostics highlight several strict boundaries:

1. **Unobserved Cash Legs (Directional Short vs. Basis Trade):** A -3.59% net short in futures—and the -3.24 percentage point unexpected short shift—could reflect Leveraged Funds betting directionally on rising 10-year yields, hedging corporate/agency rate exposure, or putting on **cash-futures basis trades** (buying cash Treasuries and shorting futures). Because cash bond holdings and genuine repo-implied basis profitability are unobserved, neither the raw CFTC numbers nor the model residual can distinguish between directional macro bearishness and relative-value arbitrage.
2. **Modest Model Explanatory Power:** The model improves squared error by **10.47% ($R^2$)** over a simple historical-mean change benchmark. While statistically informative, nearly 90% of the variance in weekly positioning changes remains unexplained by the included variables. The -3.24 percentage point residual simply measures the unexpected weekly flow relative to this specific regression specification—not an isolated trading strategy or private information.
3. **Retrospective, Same-Week Conditioning:** Because the model incorporates contemporaneous market variables and current-week CFTC open interest, it describes how unusual the positioning shift was *given* what happened during the week ending September 30, 2014. It does not serve as a predictive signal for future Treasury yield movements or next-week positioning.

---

## Item 5 | X-3e5133804161 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 26 January 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,447,076

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 189,014 | 219,406 | 45,956 | -30,392 | -0.88% |
| Asset Manager / Institutional | 1,329,379 | 1,266,708 | 687,802 | 62,671 | +1.82% |
| Leveraged Funds | 500,339 | 495,068 | 63,998 | 5,271 | +0.15% |
| Other Reportable | 280,025 | 189,633 | 2,528 | 90,392 | +2.62% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +1.21% of open interest (approximate 90% range based on earlier out-of-sample errors: -2.34% to +4.76%).
- Actual net position this week: +0.15% of open interest.
- Residual (actual minus expected): -1.06 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 43% were smaller than this one and 57% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The CFTC Traders in Financial Futures (TFF) data for the week ending January 26, 2021, alongside the model output, points to a **broadly balanced, consensus-less 10-Year U.S. Treasury futures market** with no extreme directional crowding across major institutional categories and no statistically abnormal shift in speculative positioning.

---

### 1. Breakdown by Trader Category

* **Leveraged Funds (Hedge Funds & CTAs): Virtually Flat (+0.15% of OI)**
* Holding 500,339 long contracts against 495,068 short contracts (a net long of just 5,271 contracts), speculative accounts are almost evenly split.
* In Treasury futures, leveraged funds often hold substantial net short positions due to cash-futures basis trading (buying cash Treasuries and shorting futures) or macro reflation bets. A near-zero net position indicates a lack of strong directional conviction—or that outright macro longs are roughly balancing out relative-value basis shorts.


* **Asset Managers / Institutional: Modestly Net Long (+1.82% of OI)**
* Real-money accounts (pensions, mutual funds, insurance companies) hold the largest gross positions on both sides of the market (1.33M long, 1.27M short) and the largest spreading book (687,802 contracts), yielding a net long of 62,671 contracts.
* Asset managers structurally use Treasury futures to manage portfolio duration and hedge liabilities. However, a +1.82% net long is modest relative to their total footprint, indicating that while real money is a net buyer of duration, their aggregate positioning is far from one-sided.


* **Dealers / Intermediaries: Nearly Flat (-0.88% of OI)**
* Primary dealers and banks sit at a small net short of -30,392 contracts. Because dealers act primarily as liquidity providers and warehouse risk transferred by clients, their near-neutral book confirms that client demand across the rest of the market is largely self-balancing.


* **Other Reportables: Net Long (+2.62% of OI)**
* Corporate treasuries, central banks, and smaller non-leveraged entities hold the largest net directional position (+90,392 contracts), leaning toward locking in yields or holding safe-haven duration.


* **Non-Reportable (Implied Remainder): Net Short (-3.71% of OI)**
* Because total longs and shorts across the entire market must sum to zero, summing the four reportable categories reveals an aggregate reportable net long of **+127,942 contracts** (+3.71% of OI).
* Consequently, **non-reportable (smaller/retail) traders** must hold an offsetting net short position of **-127,942 contracts** (-3.71% of OI), leaning toward higher yields (lower bond prices) against the aggregate institutional book.



| Category Group | Net Contracts | Net as % of OI | Positioning Bias |
| --- | --- | --- | --- |
| **Reportable Institutional Total** | +127,942 | +3.71% | Modest net long duration |
| **Non-Reportable (Implied)** | -127,942 | -3.71% | Net short duration (betting on higher yields) |
| **Leveraged Funds (Model vs. Actual)** | +5,271 | +0.15% (vs. +1.21% exp.) | Neutral; slightly less bullish than predicted |

---

### 2. Interpretation of the Supervised Model Output

The model v4.0 results confirm that leveraged-fund positioning is behaving well within normal historical noise:

1. **Slight Bearish / Less-Bullish Tilt vs. Model Benchmark:** The model expected leveraged funds to hold a net long of +1.21% of OI, whereas actual positioning came in at +0.15%. The residual of **-1.06 percentage points** (~36,539 fewer net long contracts than predicted) indicates that hedge funds are slightly more cautious on bond prices (or slightly more inclined to position for rising yields) than the model's input features would typically imply.
2. **No Statistical Anomaly:** Despite the negative residual, +0.15% sits comfortably inside the model's 90% prediction interval (-2.34% to +4.76%). Furthermore, because **57% of historical out-of-sample errors were at least as large** as 1.06 percentage points, this deviation is smaller than the median historical error. There is no evidence of a sudden regime shift, structural break, or anomalous positioning shock among speculators.

---

### 3. Implications for Market Dynamics

* **Low Risk of Positioning Squeezes:** A primary use of CFTC TFF data is identifying crowded trades that leave the market vulnerable to violent short squeezes or long liquidations. With net positions across all reportable categories clustering tightly between **-0.88% and +2.62% of OI**, the 10-Year note futures market exhibits very low crowding risk.
* **High Two-Way Disagreement:** Even though *net* positions are small, *gross* positions are substantial—Asset Managers and Leveraged Funds combined hold over 1.82 million gross long and 1.76 million gross short contracts. Rather than sitting on the sidelines, large institutions are actively engaged on both sides of the market, reflecting healthy two-way liquidity and divided views on the trajectory of 10-year yields.
* **Fundamentals Over Technicals:** Because speculative positioning is neither stretched to an extreme nor diverging significantly from model expectations, near-term price action in 10-Year Treasuries is unlikely to be driven by forced positioning unwinds. Instead, yields are poised to respond cleanly to incoming macroeconomic data, fiscal supply, and monetary policy signals.

---

## Item 6 | X-50bc0731c545 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 2 November 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,973,988

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 236,520 | 199,259 | 42,525 | 37,261 | +0.94% |
| Asset Manager / Institutional | 1,545,546 | 1,328,035 | 850,685 | 217,511 | +5.47% |
| Leveraged Funds | 742,069 | 499,445 | 110,896 | 242,624 | +6.11% |
| Other Reportable | 142,516 | 301,970 | 9,139 | -159,454 | -4.01% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +8.63% of open interest (approximate 90% range based on earlier out-of-sample errors: +5.06% to +12.21%).
- Actual net position this week: +6.11% of open interest.
- Residual (actual minus expected): -2.53 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 76% were smaller than this one and 24% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The positioning data for the week ending November 2, 2021, shows a **broadly net-long institutional posture in 10-Year U.S. Treasury Note futures**, though leveraged funds are slightly less bullish than the model's baseline expectation.

### 1. Breakdown by Trader Category

* **Broad Institutional Demand for Duration:** Usually, at least one major reportable segment (frequently Leveraged Funds or Dealers) holds a substantial net short position to counterbalance Asset Managers. Here, the three largest institutional categories—**Asset Managers (+5.47% of OI)**, **Leveraged Funds (+6.11% of OI)**, and **Dealers (+0.94% of OI)**—are all simultaneously net long.
* **Asset Managers (Real Money):** Holding the largest outright footprint (1.55M long contracts and 1.33M short contracts), Asset Managers are net long by 217,511 contracts. This reflects steady structural demand for 10-year duration to match liabilities or benchmark indices. Their massive spreading figure (850,685 contracts, or 21.4% of total OI) also indicates heavy calendar-roll or intra-contract relative-value activity.
* **Leveraged Funds (Hedge Funds & CTAs):** Leveraged funds hold the largest net long position in absolute terms (+242,624 contracts, +6.11% of OI). Because leveraged funds frequently utilize short 10-year futures for basis trades (long cash Treasuries vs. short futures) or directional reflation bets, a net long of +6.11% indicates either a directional bet on falling yields (rising bond prices) or a significant unwinding of short basis/macro positions.
* **Counterbalancing Shorts (Other Reportables & Non-Reportables):**
* Summing the reportable categories shows a combined net position of **+337,942 contracts** ($37,261 + 217,511 + 242,624 - 159,454$).
* Because total futures longs and shorts must sum to zero across the entire market, **Non-Reportable (smaller/retail) traders** must hold an aggregate net **short** position of **-337,942 contracts** (-8.50% of open interest). Alongside **Other Reportables** (-159,454 contracts, -4.01% of OI—typically corporate treasuries or smaller proprietary firms hedging rate locks), these two groups are supplying the short contracts absorbed by major institutions.



---

### 2. Interpretation of the Supervised Model Output

The supervised model provides crucial context on whether the leveraged-fund net long (+6.11%) is abnormally high or low relative to prevailing market drivers:

* **Less Bullish Than Expected (Negative Residual):** Given the model's inputs, leveraged funds were expected to be even more net long (+8.63% of OI) than they actually were (+6.11% of OI), resulting in a residual of **-2.53 percentage points** (roughly 100,500 fewer net long contracts than predicted).
* **Statistical Noise vs. Structural Shift:** The actual figure (+6.11%) sits well inside the model's 90% prediction interval (+5.06% to +12.21%). Furthermore, nearly a quarter (24%) of historical out-of-sample errors were at least this large. Statistically, this shortfall is **moderately notable but not an extreme outlier**—it represents mild positioning reluctance rather than a regime break.
* **Market Implication of the Residual:** While the macro or technical inputs feeding the model justified a heavy long stance (+8.63%), leveraged funds held back (or took profits/added shorts). In rates markets, when speculators are less long than macro fundamentals suggest they should be, it can mean:
1. **Caution ahead of a catalyst:** Funds may be trimming duration exposure ahead of central bank announcements or economic releases.
2. **Dry powder:** Because leveraged funds have not stretched to the upper bound of expected long positioning (+8.63% to +12.21%), the long side is less crowded than the model's inputs would normally imply, leaving room for them to add longs if yields fall further—or signaling early skepticism toward a bond rally.



---

### 3. Overall Market Takeaway

The 10-Year Treasury futures market shows **constructive, pro-duration positioning across primary institutional players** (Asset Managers, Leveraged Funds, and Dealers all net long), balanced against rate-hedging and speculative shorts from Other Reportables and Non-Reportable traders. However, the model residual (-2.53% of OI) cautions against reading the +6.11% leveraged-fund net long as extreme euphoria: relative to what the model expects, hedge funds are actually leaning slightly defensive, staying comfortably within normal historical error bounds.

---

## Item 7 | X-0f126908128f | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 2 November 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,973,988

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 236,520 | 199,259 | 42,525 | 37,261 | +0.94% |
| Asset Manager / Institutional | 1,545,546 | 1,328,035 | 850,685 | 217,511 | +5.47% |
| Leveraged Funds | 742,069 | 499,445 | 110,896 | 242,624 | +6.11% |
| Other Reportable | 142,516 | 301,970 | 9,139 | -159,454 | -4.01% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +8.63% of open interest (approximate 90% range based on earlier out-of-sample errors: +5.06% to +12.21%).
- Actual net position this week: +6.11% of open interest.
- Residual (actual minus expected): -2.53 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 76% were smaller than this one and 24% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

Short answer: this report describes how positions were distributed and how leveraged funds’ positioning compared with a weak statistical benchmark. It says little about where Treasury yields were heading or why traders held these positions. Here is what you can and can’t take from it.

The positioning snapshot

Who was net long and who was net short. Leveraged funds (+6.11% of OI) and asset managers (+5.47%) were both net long 10-year note futures. Dealers were close to flat (+0.94%), and “other reportables” were net short (−4.01%). Your table doesn’t show non-reportable traders, but they are implied by what’s left over. Their long position is about 294k contracts and their short about 632k, a net short of roughly 338k contracts, or about −8.5% of OI. That residual short is large, and I’d check it against the source report before relying on it.

Leveraged funds net long is not the textbook basis-trade pattern. In the usual cash-futures basis trade, hedge funds are short futures against long cash bonds, and asset managers hold the offsetting futures longs. Here, leveraged funds were net long in this contract. That doesn’t rule out basis trading. Their gross short of about 499k contracts could still contain substantial basis positions offset by longs held for other reasons, and netting hides that. It does mean the net figure gives no evidence that the basis trade dominated leveraged-fund positioning in the 10-year contract that week.

A net long in one contract isn’t necessarily a bet on falling yields. Leveraged funds often hold one tenor against another, for example long 10s against short 2s or 5s as a flattener, or 10s against the Ultra 10-year. They also run relative-value and hedging books. You’d need their positions in TU, FV, TN, US and UB to judge their overall duration exposure.

Market context (from memory, not checked). Tuesday 2 November 2021 was the day before the FOMC meeting that announced the start of tapering asset purchases. Late October 2021 had seen sharp curve flattening, as markets brought forward expected rate hikes and several central banks, including the RBA and Bank of Canada, turned more hawkish. Long 10-year futures positions as part of flattening trades would fit that backdrop, but this data can’t confirm it.

What the model output adds

The surprise is moderate, not exceptional. The −2.53 pp residual is about 1.2 times the model’s RMSE. Roughly one week in four has had an absolute residual at least this large. The actual level also sits inside the approximate 90% range, near its lower end.

The model explains little of normal weekly variation. An out-of-sample R² of about 10% means most week-to-week movement is unexplained. A residual of this size is well within the model’s ordinary noise.

What the residual does mean. Leveraged funds’ net position ended the week about 2.5 pp of OI below what the model’s associations with market conditions would have implied. In other words, they added less net length, or cut more, than usual given those conditions. Because last week’s level isn’t provided, you can’t even tell whether their net long actually rose or fell.

What the residual does not mean. It doesn’t identify motives, basis-trade quantities, de-risking, or private information. It also can’t serve as a forecast, because the model uses same-week open interest and its specification was chosen retrospectively.

What would make this more informative
Last week’s level and the actual weekly change, so you know the direction of the move.
A multi-year history of leveraged-fund net positioning, to judge whether +6.1% was high or low by historical standards.
The same breakdown for the other Treasury contracts, to see curve and duration exposure across tenors.
Basis, repo and cash-market data, if the real question is about the basis trade.

On its own, this week’s report shows real money and leveraged funds both net long 10-year futures, with leveraged funds slightly less long than the model expected. That’s a modest, unexplained deviation rather than a clear signal about the Treasury market.

---

## Item 8 | X-169d21b0cb90 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 26 January 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,447,076

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 189,014 | 219,406 | 45,956 | -30,392 | -0.88% |
| Asset Manager / Institutional | 1,329,379 | 1,266,708 | 687,802 | 62,671 | +1.82% |
| Leveraged Funds | 500,339 | 495,068 | 63,998 | 5,271 | +0.15% |
| Other Reportable | 280,025 | 189,633 | 2,528 | 90,392 | +2.62% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +1.21% of open interest (approximate 90% range based on earlier out-of-sample errors: -2.34% to +4.76%).
- Actual net position this week: +0.15% of open interest.
- Residual (actual minus expected): -1.06 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 43% were smaller than this one and 57% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

## Treasury market positioning — 26 January 2021

Bottom line: Positioning in 10-Year U.S. Treasury Note futures was broadly balanced, with a modest net-long bias among reportable traders. Leveraged funds were nearly neutral, and their positioning was somewhat less bullish than the model expected. However, the model residual was not unusual by historical standards, so there is little evidence of an exceptional bearish positioning signal or a crowded speculative trade.

### 1. What the reported positions indicate

| Trader category               | Net (% of OI) | Interpretation                  |
| ----------------------------- | ------------- | ------------------------------- |
| Dealer / Intermediary         | −0.88%        | Modestly net short              |
| Asset Manager / Institutional | +1.82%        | Modestly net long               |
| Leveraged Funds               | +0.15%        | Essentially neutral             |
| Other Reportable              | +2.62%        | Most net-long reported category |

The most important observation is that leveraged funds held 500,339 long contracts against 495,068 short contracts, leaving a net long position of just 5,271 contracts.

That is a very small directional exposure relative to total open interest of 3.45 million contracts. It suggests that leveraged funds, in aggregate, were not expressing strong conviction in either rising or falling Treasury futures prices.

Asset managers and other reportable traders were more positively positioned, but their net exposures were also modest relative to total open interest.

### 2. What the model adds

Leveraged-fund net position, percentage of total open interest

Shaded band: approximate 90% range based on prior out-of-sample model errors (−2.34% to +4.76%).

The model expected leveraged funds to be net long by +1.21% of open interest. Actual positioning was +0.15%, producing a residual of −1.06 percentage points.

This means leveraged funds were less long than their modeled baseline, which is mildly bearish in positioning terms.

But the historical error distribution substantially weakens the signal:

- Approximately 43% of earlier absolute residuals were smaller.
- Approximately 57% were as large or larger.
- The observation falls comfortably inside the model's approximate 90% range.

Consequently, the residual is ordinary rather than statistically striking. It does not establish meaningful bearish sentiment or an unusual departure from typical leveraged-fund positioning.

### 3. Implications for Treasury prices and yields

Treasury futures prices generally move inversely to Treasury yields. A strongly net-short leveraged-fund position might indicate substantial speculative exposure to rising yields, while a strongly net-long position might indicate exposure to falling yields.

Neither condition is present here.

The data suggest:

- Limited directional conviction: Leveraged funds were almost evenly split between long and short exposure in aggregate.
- No obvious leveraged-fund positioning extreme: The net position and model residual offer little evidence of crowded bearish or bullish positioning.
- Some positive positioning elsewhere: Asset managers and other reportable traders were net long, although this does not necessarily imply outright bullish expectations because futures can be used for hedging and relative-value strategies.
- No strong standalone yield forecast: The figures do not establish whether Treasury yields were likely to rise or fall next.

Importantly, net positioning can conceal substantial offsetting gross positions. Leveraged funds held nearly one million combined long and short contracts, excluding spreading. Therefore, a small net exposure does not imply little trading activity or insignificant leverage. It also does not rule out crowded relative-value strategies.

### 4. What cannot be inferred

This is a single weekly snapshot, not a positioning time series. Without previous weeks' observations, it is impossible to determine whether leveraged funds had recently been adding duration, reducing shorts, or liquidating longs.

Moreover, the CFTC report does not directly identify traders' motivations, their cash Treasury exposures, or their positions in other Treasury maturities.

The data also describe positions as of 26 January 2021, rather than current market conditions.

## Overall assessment

Signal: Neutral, with a weak bearish tilt relative to the model baseline.

Leveraged funds were slightly net long Treasury futures but less long than expected. The negative residual could indicate marginally less appetite for duration than the model predicted, yet its historical magnitude was unremarkable.

The strongest defensible conclusion is that the report provides no compelling evidence of an unusually bearish leveraged-fund position, an extreme bullish consensus, or an imminent positioning-driven Treasury market move.

To make a directional call on 10-year Treasury yields, this snapshot would need to be combined with changes in positioning, yield movements, macroeconomic expectations, and broader Treasury market conditions.

---

## Item 9 | X-02ff0cab7e0d | R applicable: NO

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 3 July 2017. All figures are numbers of contracts.

Open interest (all contracts): 3,087,863

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 116,919 | 195,535 | 25,483 | -78,616 | -2.55% |
| Asset Manager / Institutional | 1,079,237 | 939,893 | 477,453 | 139,344 | +4.51% |
| Leveraged Funds | 601,628 | 597,986 | 107,636 | 3,642 | +0.12% |
| Other Reportable | 291,420 | 194,425 | 30,300 | 96,995 | +3.14% |

What does this positioning suggest about the Treasury market?

### REPLY

The CFTC positioning data for 10-Year U.S. Treasury Note futures for the week ending 3 July 2017 suggests a moderately bullish but not strongly directional Treasury market, with institutional investors maintaining a net long position while leveraged funds were essentially neutral.

Importantly, a bullish position in Treasury futures implies an expectation of higher Treasury prices and lower yields, since bond prices and yields move inversely.

## 1. What the positioning reveals

| Trader category               | Net position | % of open interest | Interpretation                                                     |
| ----------------------------- | ------------ | ------------------ | ------------------------------------------------------------------ |
| Dealer / Intermediary         | −78,616      | −2.55%             | Net short; potentially reflecting market-making and hedging        |
| Asset Manager / Institutional | +139,344     | +4.51%             | Largest net long; supportive institutional demand                  |
| Leveraged Funds               | +3,642       | +0.12%             | Almost perfectly balanced; little aggregate directional conviction |
| Other Reportable              | +96,995      | +3.14%             | Additional net-long positioning                                    |

### Asset managers: A bullish institutional bias

Asset managers hold the largest net long position at 139,344 contracts, or 4.51% of total open interest.

This indicates a preference for Treasury duration among institutional participants. Possible explanations include expectations of stable or declining yields, portfolio diversification, or demand for duration exposure.

However, asset managers frequently use futures to adjust portfolio duration or hedge other exposures. Their net long position should not automatically be interpreted as a speculative forecast that yields will fall.

### Leveraged funds: A notably neutral stance

Leveraged funds hold 601,628 long contracts and 597,986 short contracts, producing a net long position of just 3,642 contracts.

This is especially interesting because the category has substantial gross exposure but almost no net directional exposure.

It suggests that hedge funds, in aggregate, were not expressing a strong directional view on 10-year Treasury futures. Their positions could reflect relative-value strategies, hedging, or offsetting directional views across different funds.

The absence of a large leveraged-fund net short is important: the data does not indicate a heavily crowded speculative bearish trade against Treasury prices.

### Dealers: Net short, but not necessarily bearish

Dealers are net short 78,616 contracts.

This could reflect hedging customer flows, balance-sheet exposures, or intermediary activities rather than a genuine expectation of rising Treasury yields.

Consequently, dealer positioning is less useful as a standalone directional sentiment signal.

### Other reportable traders: Additional positive exposure

Other reportable traders are net long 96,995 contracts, equivalent to 3.14% of open interest.

This reinforces the positive net positioning among the reported non-dealer categories, although the heterogeneous composition of this group makes its economic motivation less clear.

## 2. Overall positioning balance

Net positioning as a percentage of total open interest

-4%-1.5%1%3.5%6%DealersAsset managersLeveraged fundsOther reportable

Positive = net long Treasury futures; negative = net short. Source: figures supplied in the question.

Adding the reported categories produces a combined net long position of 161,365 contracts, approximately 5.23% of total open interest.

This is not an overall market net long, however. Futures positions must balance between longs and shorts. The residual positions belong to nonreportable traders, whose net short exposure offsets the reportable categories' aggregate net long.

The key pattern is that asset managers and other reportable traders are net long, dealers are net short, and leveraged funds are nearly flat.

## 3. What this suggests for Treasury yields

There are three plausible interpretations:

- Bullish or yield-supportive scenario: Institutional net longs could support Treasury prices and limit upward pressure on yields, especially if institutions continue adding duration.
- Bearish or rising-yield scenario: If yields rise, long-positioned institutional accounts could reduce exposure, potentially contributing to further price declines.
- Range-bound scenario: The near-neutral leveraged-fund positioning is consistent with a market lacking a strong aggregate speculative directional conviction.

The data alone cannot tell us which scenario is most likely. In particular, we would need previous weeks' positioning to determine whether institutional investors were accumulating longs or reducing them.

## 4. Important limitations

Two distinctions matter when interpreting this report.

First, the size of a net position is not the same as the strength of a market forecast. Treasury futures are extensively used for hedging, duration management, and relative-value trading.

Second, a position of +4.51% of open interest cannot be described as historically extreme without examining its distribution over preceding months or years. We also cannot infer fresh buying or selling pressure from a single weekly snapshot.

## Bottom line

The July 2017 positioning suggests a mild institutional bullish bias toward 10-year Treasuries, accompanied by relatively neutral leveraged-fund positioning.

There is no clear evidence in these figures of an aggressively crowded speculative bet on rising Treasury yields. Equally, institutional net longs are not sufficient to establish a powerful bullish consensus.

The strongest conclusion is that institutional participants were net long duration, while leveraged funds exhibited little aggregate directional conviction. That creates a modestly constructive positioning backdrop for Treasury prices, but not a reliable standalone prediction of the next move in yields.

---

## Item 10 | X-b83fc93101b8 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 2 November 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,973,988

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 236,520 | 199,259 | 42,525 | 37,261 | +0.94% |
| Asset Manager / Institutional | 1,545,546 | 1,328,035 | 850,685 | 217,511 | +5.47% |
| Leveraged Funds | 742,069 | 499,445 | 110,896 | 242,624 | +6.11% |
| Other Reportable | 142,516 | 301,970 | 9,139 | -159,454 | -4.01% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +8.63% of open interest (approximate 90% range based on earlier out-of-sample errors: +5.06% to +12.21%).
- Actual net position this week: +6.11% of open interest.
- Residual (actual minus expected): -2.53 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 76% were smaller than this one and 24% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

Short answer

On its own, this snapshot says little about where Treasuries were headed. It shows who held what in one contract in one week. The model output suggests leveraged funds were somewhat less long than usual, but not unusually so.

What the positioning shows
Asset managers net long (+5.5% of OI). This is the normal pattern. Pension funds, insurers and bond funds use futures to add duration cheaply, so a net long here reflects ordinary portfolio construction rather than a market call.
Leveraged funds net long (+6.1% of OI). This is the most interesting line, but it can’t be read as “hedge funds were bullish on bonds.” Leveraged fund futures positions are often one leg of a larger trade:
Cash-futures basis trades usually make funds short futures, so a net long can reflect basis positions being reduced.
Curve trades pair contracts. For example, a flattener could be long 10-year futures against short 2- or 5-year futures.
Relative-value trades against swaps or cash bonds.
Without the positions in other tenors, you can’t tell whether this is a directional duration bet.
Dealers roughly flat (+0.9%) and Other Reportables net short (−4.0%). Neither is large enough to signal much.
What the model output adds

Funds were 2.5 points of OI less long than the model expected. The actual figure sits inside the model’s 90% range, and about a quarter of past residuals were at least this large, so this is roughly a one-in-four event. At most it is a mild hint that funds were holding back relative to whatever the model’s inputs implied. Also, the model forecasts positioning, not prices, so even a large residual wouldn’t by itself predict yields.

Context and caveats
Timing. The report is dated Tuesday 2 November 2021, the day before the Fed announced it would begin tapering asset purchases. Positions taken just ahead of a widely anticipated FOMC decision partly reflect event hedging, which makes a single week especially noisy.
One week, levels only. Positioning is far more informative as week-on-week changes and against its own history, such as percentile ranks or z-scores. Large one-sided positions mainly matter as a crowding risk if the market moves against them.
Worth checking the data. The four categories sum to a net long of about 338,000 contracts. Since all positions net to zero, that implies non-reportable traders were net short about 8.5% of OI. That is large for a group that is usually a small part of this market. The asset manager spreading figure (about 851,000) also looks high. I couldn’t verify this against the CFTC source here, so it’s worth confirming that the columns, especially spreading, weren’t shifted between categories.
It’s historical. This is from five years ago and says nothing about the Treasury market today.

If you have several weeks of this report, or the 2-year and 5-year contracts for the same date, I can help separate directional positioning from curve and basis trades.

---

## Item 11 | X-02609bbb3182 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 22 September 2020. All figures are numbers of contracts.

Open interest (all contracts): 3,262,396

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 183,734 | 255,016 | 49,148 | -71,282 | -2.18% |
| Asset Manager / Institutional | 1,367,316 | 1,162,519 | 602,202 | 204,797 | +6.28% |
| Leveraged Funds | 375,291 | 690,837 | 69,176 | -315,546 | -9.67% |
| Other Reportable | 218,722 | 95,105 | 487 | 123,617 | +3.79% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -11.17% of open interest (approximate 90% range based on earlier out-of-sample errors: -14.70% to -7.63%).
- Actual net position this week: -9.67% of open interest.
- Residual (actual minus expected): +1.49 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 56% were smaller than this one and 44% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The 22 September 2020 CFTC report suggests a Treasury futures market with substantial leveraged-fund net short exposure, offset by net long positioning among asset managers and other reportable traders. The positioning is consistent with significant disagreement across investor groups, but it does not establish that leveraged funds were making an outright bearish bet on Treasury prices.

The model adds an important qualification: leveraged funds were somewhat less short than their observed market conditions would have predicted, but the difference was not historically unusual.

## 1. What the positioning shows

| Trader category  | Net contracts | % of open interest | Interpretation               |
| ---------------- | ------------- | ------------------ | ---------------------------- |
| Leveraged funds  | −315,546      | −9.67%             | Largest reported net short   |
| Asset managers   | +204,797      | +6.28%             | Significant net long         |
| Other reportable | +123,617      | +3.79%             | Additional net long exposure |
| Dealers          | −71,282       | −2.18%             | Moderate net short           |

The most striking feature is the contrast between leveraged funds and asset managers.

Leveraged funds held substantially more short than long futures contracts. On a standalone futures basis, this exposure benefits from falling Treasury futures prices (generally associated with rising yields).

Asset managers held a substantial positive net position, consistent with demand for Treasury duration or duration hedging, although the precise motivations cannot be inferred.

Dealers' net short position may reflect intermediation, hedging, or inventory management rather than an independent directional market view.

This division is consistent with a market in which institutional investors and leveraged intermediaries are taking opposite sides of Treasury futures exposure. It is not, by itself, evidence of which side has superior information.

## 2. What the model adds

Leveraged-fund net position (% of open interest)

Approx. 90% range

Expected

Actual

The model expected a net short position of −11.17% of open interest, compared with the actual −9.67%.

This is a positive residual of approximately 1.49 percentage points, equivalent to roughly 49,000 contracts at that week's open interest.

The interpretation is that leveraged funds were less net short than the model's same-week conditional estimate implied.

However, three qualifications matter:

- The residual was unexceptional: approximately 44% of earlier absolute out-of-sample residuals were at least as large.
- The actual position was inside the model's broad historical-error range of −14.70% to −7.63%.
- A positive residual does not establish that funds actually bought futures or reduced shorts during the week. Establishing the direction of the actual weekly change requires the prior week's position.

The model therefore provides modest evidence of a less-negative-than-expected positioning adjustment, not compelling evidence of an unusual bullish shift.

## 3. Implications for Treasury market dynamics

Yield sensitivity: The large leveraged-fund net short represents exposure that, considered alone, would generally gain from rising Treasury yields and lose from falling yields. But some of that exposure could be hedged against cash Treasuries or other instruments.

Cash-futures basis activity: The combination of leveraged-fund futures shorts and institutional futures longs is compatible with an environment containing leveraged relative-value or basis trading. It does not quantify those trades. In particular, futures shorts hedging long cash Treasuries need not represent bearish duration views.

Position-unwind risk: If leveraged-fund shorts were forced to close rapidly during a Treasury rally, their futures purchases could reinforce a rise in futures prices and a decline in yields. That is a plausible market vulnerability, not a prediction established by these figures. Assessing its magnitude would require information on leverage, funding, liquidity, concentration, and historical positioning extremes.

Market sentiment: The data do not support calling the entire Treasury market bearish. Futures positions necessarily have offsetting counterparties, and the opposing net positions of asset managers and leveraged funds should not be treated as independent measures of aggregate market conviction.

## 4. What should not be concluded

The model's positive residual is not an estimate of the share of leveraged-fund exposure unrelated to basis trading. Nor does its out-of-sample predictive improvement mean it explains a corresponding fraction of outstanding positions.

Likewise, the model's current-week inputs and retrospective selection mean its result should be understood as a conditional historical comparison, not a contemporaneous tradable signal.

The report also does not establish whether −9.67% was historically extreme. That would require comparing positioning with its own historical distribution.

## Bottom line

The September 2020 snapshot points to substantial leveraged-fund Treasury futures short exposure facing significant institutional net long exposure, creating potential sensitivity to changes in yields, funding conditions, and position unwinds.

The model suggests leveraged funds were somewhat less short than the week's observable conditions would normally imply, but the deviation was ordinary relative to historical forecast errors.

The strongest defensible conclusion is therefore one about the structure and potential fragility of Treasury futures positioning, rather than a directional forecast for Treasury yields or evidence of a particular trading strategy.

In short: substantial leveraged short exposure, a modest positive conditional positioning surprise, and no statistically compelling evidence of an exceptional change in leveraged-fund behavior.

---

## Item 12 | X-e71e9fec1715 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 8 September 2026. All figures are numbers of contracts.

Open interest (all contracts): 5,225,295

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 123,341 | 757,787 | 12,409 | -634,446 | -12.14% |
| Asset Manager / Institutional | 3,258,404 | 696,723 | 657,352 | 2,561,681 | +49.02% |
| Leveraged Funds | 391,836 | 2,330,590 | 155,946 | -1,938,754 | -37.10% |
| Other Reportable | 236,286 | 221,378 | 263 | 14,908 | +0.29% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -39.04% of open interest (approximate 90% range based on earlier out-of-sample errors: -42.45% to -35.64%).
- Actual net position this week: -37.10% of open interest.
- Residual (actual minus expected): +1.94 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 68% were smaller than this one and 32% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

## Overall assessment

Treasury futures positioning is heavily polarized, but the leveraged-fund short is broadly consistent with what the model predicts. The report points to substantial institutional demand for Treasury duration, significant leveraged relative-value activity, and potentially crowded positioning. It does not, by itself, provide a strong directional signal for Treasury yields.

### 1. The market has a pronounced positioning imbalance

The dominant positions are:

- Asset managers: Net long 2.56 million contracts (+49.02% of open interest), consistent with substantial institutional demand for Treasury duration.
- Leveraged funds: Net short 1.94 million contracts (−37.10% of open interest), representing considerable short futures exposure.
- Dealers: Net short 634,446 contracts (−12.14%), potentially reflecting intermediation and hedging of client activity.

The combination of large asset-manager longs and leveraged-fund shorts is consistent with the structural division between long-duration institutional investors and leveraged investors pursuing hedging, carry, and relative-value strategies.

Importantly, leveraged-fund futures shorts are not necessarily outright bearish Treasury bets. Some may hedge long positions in cash Treasuries through cash–futures basis trades. The reported futures positions alone cannot establish how much of the short exposure represents these trades.

### 2. The model suggests no unusual leveraged-fund positioning

Leveraged-fund net position, % of open interest

Approx. 90% historical-error range

Actual

The actual position is 1.94 percentage points less short than the model's expected −39.04%.

That is mildly positive relative to the model's baseline, but the evidence is weak:

- The actual observation lies comfortably inside the model's approximate 90% historical-error range.
- Approximately 32% of earlier out-of-sample residuals were at least this large in absolute value.
- The residual therefore is not particularly unusual and does not support a strong conclusion that leveraged funds are unexpectedly reducing bearish exposure or unwinding basis trades.

The distinction between large absolute positioning and unusual positioning conditional on the model is crucial. The leveraged-fund short is large, but the model indicates that such a short is largely expected under prevailing conditions.

### 3. Implications for Treasury prices and yields

Directional outlook: The raw positioning might appear bearish for Treasury prices and bullish for yields because leveraged funds are heavily short. However, the possibility of substantial cash–futures hedging makes that interpretation unreliable. The model-adjusted residual provides, at most, a modest less-bearish indication.

Market vulnerability: Large leveraged-fund shorts create potential short-covering pressure if Treasury futures rise sharply. This could amplify a rally and contribute to falling yields, particularly if positions are crowded or financing conditions tighten. Conversely, disorderly unwinding of basis trades could involve simultaneous cash Treasury sales and futures purchases, producing dislocations rather than a straightforward directional rally.

Institutional demand: The substantial asset-manager net long suggests meaningful demand for duration exposure through futures. However, it does not independently establish expectations for interest-rate cuts or future Treasury returns.

What cannot be inferred: A single weekly snapshot cannot tell us whether leveraged funds have been adding or covering shorts, whether positioning is at a historical extreme, or whether the model's residual has predictive power for subsequent returns.

## Bottom line

The most defensible interpretation is one of substantial, potentially vulnerable positioning rather than a clear directional Treasury-market signal.

Leveraged funds are heavily short, asset managers heavily long, and this configuration may make the market sensitive to changes in financing conditions, basis-trade economics, and abrupt shifts in Treasury prices.

But relative to the model, leveraged funds are only modestly less short than expected, and the deviation is well within normal historical forecast errors.

I would therefore characterize the report as neutral to mildly bullish on a model-adjusted basis, with potentially elevated positioning-related volatility risk—not as convincing evidence of an imminent Treasury rally, a bearish consensus, or a major short-covering reversal.

---

## Item 13 | X-634126fcfbb4 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 19 August 2025. All figures are numbers of contracts.

Open interest (all contracts): 5,340,625

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 305,767 | 602,053 | 52,309 | -296,286 | -5.55% |
| Asset Manager / Institutional | 3,173,317 | 743,650 | 537,817 | 2,429,667 | +45.49% |
| Leveraged Funds | 316,923 | 2,733,883 | 207,828 | -2,416,960 | -45.26% |
| Other Reportable | 285,759 | 121,685 | 6,992 | 164,074 | +3.07% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -43.86% of open interest (approximate 90% range based on earlier out-of-sample errors: -47.33% to -40.39%).
- Actual net position this week: -45.26% of open interest.
- Residual (actual minus expected): -1.40 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 53% were smaller than this one and 47% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The report shows a very concentrated, mirror-image structure in 10-year note futures. The model says this week’s move was ordinary, not a signal of anything unusual.

The level: two dominant, offsetting positions

Asset managers were net long about 2.43 million contracts (+45.5% of open interest), and leveraged funds were net short about 2.42 million (−45.3%). These two groups almost exactly offset each other. Leveraged funds’ gross short alone was about 51% of all open interest. Dealers (−5.6%), other reportables (+3.1%) and non-reportables (about +119,500 contracts, implied by the remainder) are small by comparison. At $100,000 face per contract, the leveraged-fund net short is roughly $240 billion face equivalent in this one contract.

This pattern is what the cash-futures basis trade typically looks like in CFTC data. Real-money investors get duration cheaply through long futures. Hedge funds take the other side by shorting futures against repo-financed long cash Treasuries. But the report cannot confirm that. The cash leg is invisible, so some of the leveraged-fund short could be outright duration bets, curve or relative-value trades, or hedges of positions in other tenors. The safe reading is that the futures data are consistent with a large basis-style position, not proof of one.

What it suggests about the market

The short isn’t necessarily a bearish rates view. If most of it is hedged against cash bonds, leveraged funds’ exposure is to the spread between cash and futures, not to yield direction. Asset managers’ long likewise reflects demand for duration more than a tactical bet.
It is a market-structure and fragility point. Positioning this one-sided means a lot of Treasury demand depends on leveraged intermediation and repo funding. If funding costs jump, margins rise, or volatility spikes, a forced unwind could hurt market functioning. This is the concern regulators have repeatedly raised. The data show that this vulnerability existed in size, not that an unwind was likely.
It doesn’t forecast yields. Nothing here indicates where 10-year yields were heading.

The model output: an unremarkable week

The residual of −1.40 percentage points means the week’s change in leveraged-fund positioning was a bit more negative than the model expected. That is about 0.7 times the model’s 2.07-point RMSE.
Roughly 53% of earlier residuals were smaller in size, so this one sits near the middle of the historical distribution. It also falls inside the approximate 90% range.
The model’s out-of-sample R² of about 10% means it explains only a modest share of week-to-week variation. The residual shouldn’t be read as “unexplained basis activity” or private information. The model’s own notes say it identifies neither.

Caveats

This is one contract. Leveraged-fund positions in 2-year, 5-year, ultra and bond futures would be needed for a fuller picture of their duration and basis exposure.
This is a single, now-historical week (August 2025). The trend in positioning over surrounding weeks would say more than one snapshot.
Without searching, I can’t tell you what happened to this positioning afterward.

Bottom line: the market in mid-August 2025 was carrying a very large, crowded leveraged-fund short opposite real-money longs, which looks like basis-trade structure. That matters for funding and stability risk, not for yield direction. The weekly change itself was routine.

---

## Item 14 | X-b4b9a293e0e8 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 2 September 2014. All figures are numbers of contracts.

Open interest (all contracts): 2,721,411

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 109,994 | 239,264 | 36,698 | -129,270 | -4.75% |
| Asset Manager / Institutional | 1,032,308 | 842,779 | 272,395 | 189,529 | +6.96% |
| Leveraged Funds | 558,487 | 533,964 | 94,035 | 24,523 | +0.90% |
| Other Reportable | 253,152 | 188,831 | 33,774 | 64,321 | +2.36% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +4.88% of open interest (approximate 90% range based on earlier out-of-sample errors: +1.14% to +8.62%).
- Actual net position this week: +0.90% of open interest.
- Residual (actual minus expected): -3.98 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 95% were smaller than this one and 5% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

Short answer: not much about direction. The leveraged-fund number is a moderately unusual miss against the model, but one week of positioning, measured near a contract roll, can’t support a reliable call on where Treasuries are headed. It’s better treated as a prompt to look at the data more closely.

What the positioning shows

I checked the arithmetic and the nets and percentages are correct.

Asset managers are the main net longs (+7.0% of OI). This is the usual pattern. Pension funds, insurers and bond funds often use futures to add duration, so a large net long here reflects how they manage portfolios more than a bet on rates.
Dealers are net short (−4.75%). They mostly take the other side of client flow, so this doesn’t suggest a dealer view on rates.
Leveraged funds are close to flat (+0.9%), but that small net comes from very large gross positions: about 558k long against 534k short. The net is a small difference between two big numbers, so modest changes on either side move it a lot.
Non-reportable traders are net short. The four reportable groups add up to a net long of about 149,100 contracts, so small traders must be net short by that amount, roughly −5.5% of OI.
How unusual the residual is

The model expected +4.88% and the actual figure was +0.90%. That gap of −3.98 points equals about 108,000 contracts, or roughly $10.8bn face value of 10-year note futures.

The actual value falls just outside the 90% range, consistent with only about 5% of past absolute errors being this large.
If errors are roughly symmetric, a miss this large on the downside happens about 2.5% of the time.
If you check the model every week, you should expect a miss like this about once every 20 weeks. It is notable, but not strong evidence that something has changed.
Possible explanations
Contract roll timing. 2 September 2014 came just after first notice day for the September contract, when positions were moving from September to December. Open interest, spreading positions and nets can all be distorted then. If model v4.0 doesn’t account for roll weeks, this is the first thing I’d check.
Relative-value trades, not a directional view. Hedge funds often sell futures against long cash Treasuries (the basis trade). More of that activity would lower their net futures position without any change in their outlook on rates. The futures data alone can’t tell these cases apart.
Taking profit after the rally. Ten-year yields had fallen a long way during 2014, from about 3% in January to around the mid-2.3s by late August. A smaller-than-expected net long fits with funds banking gains or reducing risk. Some readers would see that as a contrarian bearish sign for bonds. The evidence for that kind of signal is mixed, and one week is weak support for it.
What I’d check next
The change from the prior weeks. Was the long side cut, or the short side added? The table gives levels, not changes.
Whether the model has missed in roll weeks before.
Whether the residual persists over the following 2–4 weeks. A repeated miss means much more than a single one.
Other contracts (2-year, 5-year, bond, Ultra). If leveraged funds moved positions along the curve, this could be a curve trade rather than a change in overall duration.

Taken together, hedge funds were less long 10-year futures than the model expected. That’s worth investigating, but the most likely explanations are roll timing and relative-value positioning rather than a clear bearish turn.

---

## Item 15 | X-bf2236a568b4 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 9 June 2026. All figures are numbers of contracts.

Open interest (all contracts): 5,251,295

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 143,614 | 606,092 | 32,268 | -462,478 | -8.81% |
| Asset Manager / Institutional | 3,306,645 | 893,760 | 673,031 | 2,412,885 | +45.95% |
| Leveraged Funds | 349,939 | 2,329,450 | 130,288 | -1,979,511 | -37.70% |
| Other Reportable | 230,348 | 200,356 | 517 | 29,992 | +0.57% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -36.76% of open interest (approximate 90% range based on earlier out-of-sample errors: -40.17% to -33.35%).
- Actual net position this week: -37.70% of open interest.
- Residual (actual minus expected): -0.94 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 38% were smaller than this one and 62% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

This shows the familiar post-2018 structure of the 10-year futures market. The model output says this particular week was unremarkable. It doesn’t say why leveraged funds are short.

### What the positioning shows

The core feature is a mirror image between two groups. Asset managers are net long about 2.41 million contracts (46% of open interest), and leveraged funds are net short about 1.98 million (38%). At $100,000 face per contract, the leveraged-fund net short is roughly $198 billion of face value in this one contract. Dealers are a further net short of about 0.46 million, and other reportables are close to flat. The four categories’ nets sum to +888 contracts, so non-reportables are essentially flat too, and the figures are internally consistent.

This pattern is consistent with the cash-futures basis trade, though the report can’t confirm it:

- **Asset managers** often hold long futures as a capital-efficient way to get duration exposure against benchmarks. That creates steady demand for futures longs, which tends to make futures rich relative to cash bonds.
- **Leveraged funds** can supply that demand by shorting futures and buying the deliverable cash Treasuries, usually financed in repo. They earn the gap between the futures price and the cost of carry.

In that reading, hedge funds act as intermediaries. They take on balance-sheet-intensive trades that dealers are less willing to hold.

### Why it matters for the Treasury market

If a large part of the short is basis-related, three things follow.

- **It supports cash Treasury demand.** Basis funds are effectively large, leveraged buyers of cash Treasuries, which helps absorb supply.
- **It concentrates funding and margin risk.** These trades depend on cheap, available repo and stable futures margins. A funding squeeze, a margin increase, or a volatility spike can force fast unwinds. Funds would sell cash bonds and buy back futures, which can disrupt cash market liquidity, as happened in March 2020.
- **It ties market stability to non-bank leverage.** This is the main reason regulators watch these numbers, and part of the rationale for the move toward central clearing of Treasury and repo trades.

### Caveats on that reading

- **The cash leg is invisible.** The report covers futures only, so a short can’t be confirmed as part of a basis trade. Leveraged-fund shorts also include curve and relative-value trades, hedges of other positions, and outright directional bets that yields will rise.
- **This is one contract.** Basis positioning spans the 2-year, 5-year, 10-year, Ultra 10-year, bond, and Ultra bond contracts. Positions can shift along the curve, so a full picture needs all of them, and ideally DV01-weighted rather than contract counts.
- **It is not a rate forecast.** Heavy asset-manager longs largely reflect structural duration demand, not a bullish call. Positioning extremes are poor standalone predictors of yield direction.
- **The data are old.** This is the week ending 9 June 2026, about five months ago, so it says nothing about current positioning.

### What the model adds

Not much this week, which is itself informative.

- The residual of −0.94 percentage points is well within the historical range and smaller than about 62% of past residuals. That is about 0.45 of the model’s RMSE of 2.07 points. Leveraged funds adjusted roughly as the model’s inputs predicted, with no unusual unexplained buildup or unwind.
- The model predicts weekly changes and has modest skill. Its out-of-sample R² of 10.5% means it captures only a small share of week-to-week variation. Also, the expected level is last week’s level plus a predicted change, so a small residual doesn’t mean the model explains the roughly −38% stock.
- As its own notes say, the model doesn’t measure basis profitability or identify motives. It’s a same-week retrospective fit that uses current-week open interest, so it isn’t a forecast and wasn’t tested as a live backtest.

### Bottom line

The structure looks like a large, crowded, largely hedged leveraged-fund short paired with structural asset-manager duration demand. That probably supports cash Treasury demand in calm conditions and poses unwind risk if funding or volatility conditions worsen. Nothing in this week’s data or model output points to stress or an abnormal shift. To track the risk usefully, you’d want the series over time across all Treasury contracts, alongside repo rates, futures margins, and the implied repo rate on the cheapest-to-deliver bond.
