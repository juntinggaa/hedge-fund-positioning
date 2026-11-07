# Replies for Tia (15 replies)

Code each one in SHEET_Tia.csv, same item number.

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

## Item 2 | X-fbe48fdabbca | R applicable: YES

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

## Bottom line

Treasury futures positioning is heavily polarized, but leveraged funds are not unusually bearish relative to what the model expects. The data point to substantial structural positioning, potentially associated with Treasury cash–futures basis trades, rather than a clear signal that yields are about to rise.

### 1. The large short position is real, but its interpretation matters

Leveraged funds are net short approximately 2.42 million 10-year Treasury futures contracts, equivalent to 45.26% of total open interest. Asset managers are net long roughly 2.43 million contracts, or 45.49% of open interest.

This is a striking division between the two groups. However, it does not necessarily represent an equally striking disagreement about the direction of Treasury yields.

A plausible explanation is that leveraged funds are using futures shorts to hedge long positions in cash Treasuries as part of cash–futures basis trades, while asset managers use futures to obtain duration exposure. The report cannot establish how much of either position reflects these strategies.

Consequently, leveraged funds' large futures shorts should not automatically be interpreted as a massive outright bet on falling Treasury prices.

### 2. The model does not identify an exceptional bearish positioning imbalance

Expected leveraged-fund net

# -43.86%

Of open interest

Actual leveraged-fund net

# -45.26%

Of open interest

Model's approximate 90% historical-error range

-47.33% to -40.39%

Actual

Expected

The actual net position is only 1.40 percentage points more negative than expected and falls comfortably within the model's approximate historical-error range.

Moreover, 53% of earlier absolute out-of-sample residuals were smaller. That puts this week's deviation near the middle of the historical error distribution, rather than in its tail.

This distinction is central: the absolute short position is exceptionally large in economic terms, but the model-adjusted deviation is ordinary. The supplied evidence therefore does not support treating this observation as a statistically unusual bearish extreme.

### 3. The positioning nevertheless creates market vulnerabilities

The large leveraged-fund futures short can matter for market dynamics even if it largely reflects hedging rather than outright bearish speculation.

If Treasury prices rally sharply, directional short positions could face pressure to cover, potentially amplifying the futures rally. But for basis traders, a simultaneous unwind of long cash Treasuries and short futures could create selling pressure in the cash market, even while futures shorts are covered.

Funding conditions, repo financing, margin requirements, and changes in the cash–futures basis could therefore be more important than the net futures position alone.

The report signals potential positioning-related fragility, but it does not establish that a forced unwind is likely or imminent.

### 4. What does this imply for Treasury yields?

The positioning offers three different conclusions depending on the question.

| Question                                            | Assessment                                                   |
| --------------------------------------------------- | ------------------------------------------------------------ |
| Are leveraged funds heavily short Treasury futures? | Yes, substantially.                                          |
| Are they unusually short relative to the model?     | No compelling evidence.                                      |
| Does this predict higher or lower Treasury yields?  | No reliable directional conclusion from this snapshot alone. |

Large short positions can sometimes provide fuel for a rally if they are unwound, but the model's ordinary residual weakens any argument that leveraged-fund positioning is unusually stretched after accounting for the model's predictors.

## Overall assessment

The strongest interpretation is structural polarization with potential positioning-related fragility, not an exceptional bearish signal.

Asset managers hold very large net long Treasury futures exposure, while leveraged funds hold almost equally large net short exposure. This is consistent with the possibility that intermediation and relative-value strategies play a major role in the market.

The model adds an important qualification: the leveraged-fund short position is broadly what would be expected under the conditions represented by its predictors.

Thus, the report warrants monitoring of basis-trade leverage, funding conditions, and the potential for disorderly position unwinds. But it does not, by itself, provide a strong reason to forecast either a Treasury selloff or an imminent short-covering rally.

The key analytical distinction is between large positioning and unexpected positioning. The former is clearly present; the latter is not meaningfully evident in these data.

---

## Item 3 | X-f9b513f6daa0 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 7 May 2019. All figures are numbers of contracts.

Open interest (all contracts): 4,015,511

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 197,596 | 173,983 | 59,386 | 23,613 | +0.59% |
| Asset Manager / Institutional | 1,707,346 | 954,169 | 767,698 | 753,177 | +18.76% |
| Leveraged Funds | 356,404 | 1,259,989 | 128,279 | -903,585 | -22.50% |
| Other Reportable | 317,986 | 229,563 | 23,460 | 88,423 | +2.20% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -21.10% of open interest (approximate 90% range based on earlier out-of-sample errors: -24.66% to -17.53%).
- Actual net position this week: -22.50% of open interest.
- Residual (actual minus expected): -1.41 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 55% were smaller than this one and 45% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The short version: this snapshot shows a very large, mirror-image positioning pattern between asset managers and leveraged funds, of a kind often associated with Treasury relative-value activity. But it isn’t a directional bet on yields that can be read off the table, and the model output says this particular week was unremarkable.

What the positions show

The numbers are internally consistent. For example, 356,404 − 1,259,989 = −903,585, and dividing by the 4,015,511 open interest gives −22.50%. The structure is the striking part:

Asset managers are net long about 753,000 contracts (+18.8% of OI).
Leveraged funds are net short about 904,000 (−22.5%).
Dealers and other reportables are close to flat.

These two groups take up most of the market’s two sides, and each is a large share of open interest.

This pattern fits a well-known story. Asset managers such as pension funds, insurers and bond funds use long futures to get duration exposure cheaply and with little capital. That demand can make futures rich relative to cash bonds. Leveraged funds then sell the futures and buy the deliverable cash bonds, financed in repo, capturing the gap. That is the cash-futures basis trade.

Because this data covers futures only, it can’t confirm that story:

The cash leg is invisible, so you can’t tell whether a leveraged-fund short is hedged by cash bonds.
The short could also be an outright bearish view, a hedge of other holdings, or part of a curve trade across contracts.

The model note makes the same point: nothing in its inputs measures basis profitability or identifies motives.

What the model adds

Very little stands out this week:

Small residual. At −1.41 percentage points, the residual is smaller than the model’s 2.07-point typical error (RMSE).
Ordinary percentile. About 45% of earlier residuals were at least this large in absolute terms.
Inside the range. The actual −22.50% sits within the approximate 90% range of −24.66% to −17.53%.

Leveraged funds became somewhat more net short than the model’s conditional estimate, by roughly 57,000 contracts’ worth of open interest. That is an ordinary miss, not evidence of unusual selling, private information, or a surprise build-up of a trade.

Two further cautions:

The close fit says little about skill. The expected level is last week’s actual level plus a predicted change, so being close mostly reflects week-to-week persistence. The model explains only about 10% more of the variance in weekly changes than a simple historical-average benchmark.
It is not a forecast. The model uses current-week open interest and was built in hindsight, so it couldn’t have been used to predict this week in real time.
What it suggests about the market

The most defensible takeaway is about concentration and funding sensitivity, not direction:

Large one-sided positions. Net short positions near a quarter of open interest in the most traded Treasury futures contract mean a lot of exposure sits with leveraged, repo-funded holders.
Vulnerability to funding stress. If much of that short is basis-related, the positions depend on cheap, stable repo financing and margin terms. Stress in funding or volatility could force unwinds that disrupt the relationship between cash bonds and futures.
Strong duration demand. The asset-manager long reflects heavy real-money demand for duration held through futures.

With hindsight, that vulnerability theme mattered. The September 2019 repo spike and the March 2020 Treasury dislocation were both linked in later analysis to leveraged relative-value positions. That is my own recollection, not something this table or model shows, and the data here didn’t predict either episode.

The trap to avoid is reading “leveraged funds heavily net short” as a bearish signal on bonds. As I recall, yields actually fell during May 2019 as trade tensions escalated.

What would sharpen the picture
The full curve. Positions in the 2-, 5-, Ultra-10, bond and Ultra-bond contracts, converted to DV01 (sensitivity to rate moves) rather than contract counts, so they compare across maturities.
The trend. Several months of weekly changes, to see whether the short is building or stable.
Pricing and funding. Implied repo rates versus actual repo rates, to show whether the basis was attractive.
Funding conditions. Repo volumes and margin requirements over the same period.

---

## Item 4 | X-c784b9498736 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 15 April 2025. All figures are numbers of contracts.

Open interest (all contracts): 4,760,884

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 176,229 | 717,119 | 71,172 | -540,890 | -11.36% |
| Asset Manager / Institutional | 2,755,221 | 672,787 | 584,703 | 2,082,434 | +43.74% |
| Leveraged Funds | 201,132 | 2,012,009 | 85,571 | -1,810,877 | -38.04% |
| Other Reportable | 431,789 | 302,963 | 3,011 | 128,826 | +2.71% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -38.40% of open interest (approximate 90% range based on earlier out-of-sample errors: -41.88% to -34.92%).
- Actual net position this week: -38.04% of open interest.
- Residual (actual minus expected): +0.37 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 15% were smaller than this one and 85% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The CFTC positioning data and model output for the week ending 15 April 2025 point to a Treasury futures market dominated by its classic institutional structure—where asset managers hold massive net long duration exposure while leveraged funds and dealers take the opposing short side—alongside a weekly adjustment in leveraged fund positioning that was completely in line with contemporaneous market conditions and recent positioning baselines.

### 1. Structural Market Segmentation (The CFTC Table)

The raw positioning figures highlight a deeply entrenched division of labor across trader categories across the 4,760,884 contracts of open interest:

* **Asset Managers as Dominant Longs (+43.74% of OI):** Real-money institutional investors (pension funds, mutual funds, insurance companies) hold a net long position of **2,082,434 contracts** (2,755,221 long vs. 672,787 short). In the Treasury ecosystem, asset managers often use futures to match liability duration, maintain benchmark duration targets, or obtain synthetic long exposure without tying up as much balance-sheet cash as outright Treasury purchases.
* **Leveraged Funds as the Primary Counterparty (-38.04% of OI):** Hedge funds and CTAs hold a massive net short position of **-1,810,877 contracts** (201,132 long vs. 2,012,009 short). Their gross short holdings alone represent over 42% of total open interest. While market commentary often links this structural short to the cash-futures basis trade, relative-value curve trades, or directional macro shorts, **the CFTC futures-only report cannot distinguish between these motives** because the offsetting cash bond and repo positions are unobserved.
* **Dealers Net Short (-11.36% of OI):** Broker-dealers and intermediaries are net short **-540,890 contracts**, absorbing residual imbalances and warehousing risk from client flows across both futures and cash markets.
* **Non-Reportable ("Small") Traders Implicitly Net Long (+2.95% of OI):** Summing the net positions across the four reportable categories leaves a combined reportable net balance of **-140,497 contracts**:

$$\text{Reportable Net} = -540,890 + 2,082,434 - 1,810,877 + 128,826 = -140,497$$



Because every futures contract has both a long and a short side, non-reportable traders must hold the offsetting **+140,497 contracts net long** (+2.95% of open interest).

---

### 2. What the Model Output Tells Us About the Weekly Shift

The supervised model (v4.0) evaluates whether the *weekly change* in leveraged funds' net position was unusual given concurrent market dynamics (yield changes, volatility, funding stress proxies, Fed holdings, open interest shifts, and lagged positioning):

* **No Surprising Weekly Adjustment:** The actual leveraged fund net position (**-38.04% of OI**) landed very close to the model's conditional expectation (**-38.40% of OI**), leaving a tiny positive residual of **+0.37 percentage points of OI** (meaning leveraged funds were slightly less net short—by roughly 17,600 contracts—than the model's point estimate).
* **Routine Statistical Noise:** A residual of 0.37 percentage points is small relative to the model's historical out-of-sample RMSE of **2.07 percentage points of OI**. Historically, **85% of earlier out-of-sample weeks saw an absolute residual at least as large as this one**, and only 15% saw a smaller gap. It also sits comfortably near the center of the approximate 90% historical error range (-41.88% to -34.92%).
* **Interpretation:** Whatever weekly change occurred in leveraged fund net positioning during the week ending 15 April 2025 was virtually indistinguishable from normal statistical variation around the relationship captured by contemporaneous market variables and prior week positioning. There is no statistical evidence of an abnormal positioning shock, forced liquidation, or anomalous surge in shorting during that specific week.

---

### 3. Critical Caveats and Analytical Boundaries

When drawing conclusions about the broader Treasury market from these numbers, several strict methodological limits apply:

* **Unobserved Cash Legs & Strategy Ambiguity:** Neither the raw -38.04% net short position nor the +0.37 pp residual tells us how much of the leveraged fund short is hedged via long cash Treasuries (the cash-futures basis trade) versus unhedged directional bets on higher yields. Furthermore, the model does not directly observe cash-futures basis profitability; it only captures statistical associations with market proxies.
* **Level vs. Weekly Change:** The model predicts the *weekly change* added to last week's level, not the structural composition of the entire -38.04% stock of short contracts. Similarly, the model's **10.47% out-of-sample $R^2$** means its squared prediction error on weekly changes beats an expanding historical-mean change benchmark by 10.47%—it does *not* mean that 10.47% of leveraged funds' total positioning is explained by a specific trading strategy.
* **Not a Forecast or Real-Time Signal:** Because the model relies on same-week market variables and current-week CFTC open interest, and was selected retrospectively, it serves as a **contemporaneous diagnostic tool** rather than a forward-looking predictor of where Treasury yields or positioning will move next week.

---

## Item 5 | X-bde31a9dfa2a | R applicable: NO

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 12 July 2016. All figures are numbers of contracts.

Open interest (all contracts): 2,877,360

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 151,097 | 163,256 | 42,092 | -12,159 | -0.42% |
| Asset Manager / Institutional | 866,601 | 1,047,093 | 396,958 | -180,492 | -6.27% |
| Leveraged Funds | 621,257 | 595,127 | 54,961 | 26,130 | +0.91% |
| Other Reportable | 353,456 | 161,842 | 19,435 | 191,614 | +6.66% |

What does this positioning suggest about the Treasury market?

### REPLY

The CFTC positioning data for 12 July 2016 suggests a divided Treasury market, with institutional investors positioned defensively, speculative funds close to neutral, and other reportable traders taking a substantial bullish position.

The key distinction is that being long Treasury futures generally benefits from rising Treasury prices and falling yields, while being short benefits from falling prices and rising yields.

## 1. What each trader category suggests

| Trader category               | Net contracts | Interpretation                                                   |
| ----------------------------- | ------------- | ---------------------------------------------------------------- |
| Dealer / Intermediary         | −12,159       | Slightly short; broadly neutral                                  |
| Asset Manager / Institutional | −180,492      | Significantly net short; potentially bearish or hedging duration |
| Leveraged Funds               | +26,130       | Slightly net long; limited directional conviction                |
| Other Reportable              | +191,614      | Strongly net long; bullish on Treasury prices                    |

Asset managers are the most notable institutional short position. Their net short of 180,492 contracts, equivalent to 6.27% of open interest, indicates substantial exposure that would benefit from rising yields. However, institutional short positions often reflect hedging of existing bond portfolios rather than outright predictions of falling Treasury prices.

Leveraged funds are only modestly bullish. Their net long of 26,130 contracts represents just 0.91% of open interest. This suggests relatively balanced speculative positioning, rather than a strong consensus among hedge funds that Treasury yields will decline.

Other reportable traders are the strongest net buyers. Their 191,614-contract net long, equivalent to 6.66% of open interest, largely offsets the institutional short exposure. This group is positioned to benefit from higher Treasury futures prices and lower yields.

Dealers are almost neutral, consistent with their role as intermediaries and hedgers.

## 2. What the overall positioning reveals

Net positions as a percentage of total open interest

-8%-4%0%4%8%DealerAsset managerLeveraged fundsOther reportable

Negative = net short; positive = net long. Spreading positions excluded from directional net calculations.

The most important observation is that the largest long and short positions are held by different categories of traders.

Asset managers' substantial net short is nearly balanced by other reportable traders' substantial net long. Leveraged funds and dealers contribute comparatively little directional imbalance.

Collectively, the four reportable categories hold a net long of 25,093 contracts, approximately 0.87% of total open interest. The corresponding nonreportable position must therefore be net short by the same amount.

This is not evidence that the entire market is net bullish: every futures long has an offsetting short.

## 3. Implications for Treasury yields

Three interpretations are plausible.

- Potential upward pressure on yields: Asset managers' net short positions could reflect expectations of rising yields or efforts to protect portfolios against interest-rate increases.
- Continued demand for duration: The large net long among other reportable traders indicates meaningful positioning in favor of rising Treasury prices and declining yields.
- Limited speculative consensus: Leveraged funds are close to neutral, suggesting that sophisticated speculative participants, in aggregate, have not taken a particularly strong directional stance.

The large spreading positions among asset managers also highlight the importance of separating directional exposure from relative-value and hedging activity.

## 4. Does this signal a Treasury sell-off?

Not necessarily.

Although institutional net shorts are substantial, the data do not establish whether these positions reflect bearish forecasts, portfolio hedging, or relative-value strategies.

Nor can one weekly snapshot establish whether positioning is unusually extreme, whether traders are accumulating or unwinding exposure, or whether a reversal is imminent. Those conclusions require historical comparisons and changes in positioning over time.

## Bottom line

The report points to conflicting views on Treasury duration rather than a clear consensus about the direction of yields.

Asset managers are meaningfully net short, other reportable traders are meaningfully net long, and leveraged funds are relatively neutral.

The strongest defensible conclusion is that Treasury futures positioning was polarized across trader categories but broadly balanced in aggregate, with no unambiguous speculative signal of an imminent rise or fall in 10-year Treasury yields.

---

## Item 6 | X-8b5e5fd77636 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 27 October 2026. All figures are numbers of contracts.

Open interest (all contracts): 5,881,588

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 153,034 | 783,060 | 17,982 | -630,026 | -10.71% |
| Asset Manager / Institutional | 3,709,233 | 709,069 | 772,382 | 3,000,164 | +51.01% |
| Leveraged Funds | 506,310 | 2,733,585 | 133,302 | -2,227,275 | -37.87% |
| Other Reportable | 166,232 | 332,672 | 2,644 | -166,440 | -2.83% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -37.13% of open interest (approximate 90% range based on earlier out-of-sample errors: -40.53% to -33.73%).
- Actual net position this week: -37.87% of open interest.
- Residual (actual minus expected): -0.74 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 32% were smaller than this one and 68% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The short version is that this is a structurally stretched but, for this week, unsurprising picture. It’s consistent with heavy leveraged-fund intermediation of Treasury demand, possibly through the cash-futures basis trade. It says little about which way yields are headed.

The cross-sectional picture

The numbers check out. The four reportable nets sum to about −23,600 contracts, which implies non-reportables are net long roughly +23,600. The core pattern is a near mirror image:

Asset managers are net long about 3.0 million contracts, +51% of open interest.
Leveraged funds are net short about 2.23 million contracts, −38% of open interest.
Dealers are net short about 0.63 million, −11%.

This is the textbook configuration associated with the basis trade. Asset managers often prefer futures for duration exposure because futures are capital-efficient, and that demand tends to make futures rich relative to cash. Leveraged funds can then short the futures, buy deliverable cash Treasuries, and finance them in repo, earning the spread. A net short of this size in one contract is about $220bn of face value. A basis book of that scale would imply a similarly large repo-financed cash holding.

You can’t verify that from this report. The cash leg is invisible here, and CFTC categories classify traders, not motives. Some of the leveraged-fund short could be outright duration bets, curve or relative-value positions, or hedges against swaps or other holdings. “Consistent with a large basis trade” is the defensible claim; “the basis trade is $220bn” is not.

What it implies for the market

Demand for duration is being intermediated through leverage. Real-money investors are taking duration via futures, and leveraged funds are warehousing the cash bonds. That supports Treasury demand and auction absorption while funding is cheap and stable.

The vulnerability is in funding and margins, not rates direction. A position like this is exposed to repo rate spikes, higher futures initial margins, rising volatility, or tighter dealer balance sheets. Forced unwinds in such conditions mean selling cash Treasuries into a market that may lack balance-sheet capacity. That dynamic contributed to the March 2020 dislocation, and it’s why regulators watch this positioning.

It isn’t a directional signal. The leveraged-fund short isn’t necessarily a bet on higher yields, and the asset-manager long isn’t necessarily a bet on lower yields. It’s largely benchmark duration exposure. Reading this as “hedge funds are bearish bonds” would be a mistake.

What the model adds

Not much this week, and that is informative in its own way. The residual of −0.74pp is about a third of the model’s historical RMSE of 2.07pp. About 68% of earlier out-of-sample residuals were at least as large, and the actual value sits comfortably inside the approximate −40.5% to −33.7% range. So the week’s change in leveraged-fund positioning was roughly what the market and positioning inputs predicted. There’s no sign of an unusual build or unwind beyond those conditions.

Two caveats keep this modest. First, the out-of-sample R² of about 10% means weekly changes are mostly unpredictable even with these inputs, so “in line with the model” is a weak statement. Second, the model uses same-week open interest and was selected retrospectively. It describes the week after the fact rather than forecasting anything.

What this snapshot can’t tell you
Historical context: with no history here, I can’t say whether −38% is extreme for this contract.
Other tenors: basis positions are spread across 2-, 5-year, Ultra 10-year and bond contracts, so the 10-year alone understates or misstates the aggregate.
Spread positions: spreading positions are excluded from the nets.

The more useful signals would be the trend across several weeks and across contracts. Alongside that, it would help to watch:

repo and SOFR conditions relative to implied repo rates
CME margin changes
swap spreads
Treasury volatility

Those are what would show whether the structure is getting more fragile or staying comfortably funded.

---

## Item 7 | X-b83fc93101b8 | R applicable: YES

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

## Item 8 | X-0f126908128f | R applicable: YES

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

## Item 9 | X-828822b996ea | R applicable: NO

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

## Item 10 | X-704a7d1c1250 | R applicable: YES

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

The 10-Year U.S. Treasury Note futures market as of June 9, 2026, exhibits its classic structural divide: institutional asset managers hold a substantial net long position (+45.95% of open interest), which is almost entirely offset by combined net short positions across leveraged funds (-37.70% of open interest) and dealers (-8.81% of open interest). Furthermore, the model output indicates that the current leveraged-fund net short—and its weekly adjustment—is completely routine given contemporaneous market conditions and recent positioning history.

### 1. Structural Market Balance & Counterparty Flows

The CFTC breakdown highlights how risk and balance-sheet capacity are distributed across the 5,251,295 contracts of open interest:

| Trader Category | Net Contracts | Net % of OI | Structural Role in the Ecosystem |
| --- | --- | --- | --- |
| **Asset Manager / Institutional** | +2,412,885 | +45.95% | **Primary Long Demand:** Pension funds, insurance companies, and mutual funds using futures to acquire duration, match liabilities, or track bond indices without tying up upfront cash. |
| **Leveraged Funds** | -1,979,511 | -37.70% | **Primary Short Counterparty:** Hedge funds and CTAs taking the other side of institutional long demand—whether via relative-value arbitrage (such as cash-futures basis trades), curve trades, or directional macro shorts. |
| **Dealer / Intermediary** | -462,478 | -8.81% | **Intermediation & Hedging:** Banks and primary dealers warehousing residual net short exposure to facilitate client flow and hedge cash-market inventory. |
| **Other Reportable** | +29,992 | +0.57% | **Marginal Net Impact:** Corporate treasuries, non-registered entities, and smaller proprietary traders with balanced aggregate exposure. |
| **Non-Reportable (Implied)** | -888 | -0.02% | **Small Traders:** Since reportable net positions sum to +888 contracts, non-reportable smaller participants hold a negligible net short of 888 contracts to balance the market to zero. |

### 2. What the Model Output Tells Us About Leveraged Funds

While a headline leveraged-fund net short of nearly 2 million contracts (-37.70% of OI) might appear extreme in isolation, the v4.0 conditional model frames this week's positioning as **statistically unremarkable**:

* **No Anomalous Weekly Shift:** The actual net position (-37.70% of OI) came in just **-0.94 percentage points** more short than the model's conditional expectation (-36.76% of OI), which incorporates lagged positioning plus the expected weekly change given yields, volatility, funding proxies, and open-interest changes.
* **Routine Residual Size:** An unexpected adjustment of -0.94 percentage points is well inside the historical 90% error band (-40.17% to -33.35%) and smaller than the model's long-run RMSE of 2.07 percentage points. Because 62% of prior out-of-sample weeks saw residuals at least this large, there is no evidence of an unusual positioning shock, forced liquidation, or sudden speculative pile-on during this specific week.

### 3. Key Analytical Caveats & Limits of Inference

Both the raw CFTC figures and the model specifications enforce strict limits on what you can conclude about the broader Treasury market:

* **Cannot Isolate the Cash-Futures Basis Trade:** It is common market practice to treat the massive divergence between Asset Manager longs (+45.95%) and Leveraged Fund shorts (-37.70%) as a proxy for the Treasury cash-futures basis trade (where hedge funds buy cash Treasuries via repo and sell futures to asset managers). However, because the CFTC report is **futures-only**, the cash leg and repo financing are completely unobserved. You cannot determine what share of the -1,979,511 net short contracts represents delta-neutral basis arbitrage versus outright directional macro bets on higher yields.
* **Model Expectation $\neq$ "Fundamental" or "Basis" Share:** The model's expected level (-36.76%) is simply last week's position plus a statistical estimate of the weekly change (with a modest out-of-sample $R^2$ of 10.47% against a historical-mean change benchmark). Neither the expected value nor the -0.94 percentage point residual identifies trader motives, basis quantities, or private information.
* **Contemporaneous Accounting, Not a Forecast:** Because the model relies on same-week market variables and current-week CFTC open interest, it serves as a contemporaneous diagnostic tool rather than a predictive signal for future Treasury yield movements or next week's positioning.

---

## Item 11 | X-050767ec1572 | R applicable: YES

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

**Short answer:** not much about direction. The report shows a fairly ordinary 2014-era positioning structure. The model flags one unusual feature: leveraged funds ended the week noticeably less net long than their recent behaviour and market conditions would have predicted. That is worth noting, but it doesn't reveal why they did it or where yields go next.

## The cross-section

The configuration is the standard one for 10-year futures. **Asset managers are the big net longs** (+189.5k contracts, +6.96% of OI), consistent with real-money accounts using futures to add or hold duration. **Dealers are net short** (−129.3k, −4.75%), largely as the other side of that demand. **Leveraged funds are nearly flat** (+24.5k, +0.90%), but they hold about 1.09 million contracts across both sides plus 94k in spreads. Their tiny net position sits on large, offsetting gross positions, so it hides a lot of relative-value, curve and hedged activity. The category doesn't express a single directional view.

The four reported nets sum to +149.1k. That implies non-reportable traders were net short about 149k contracts (−5.5% of OI), a gap the table doesn't show.

It also matters what this structure doesn't show. In later years leveraged funds became very large net shorts in Treasury futures, widely associated with the cash-futures basis trade. In September 2014 that pattern isn't present at the level shown here. The basis trade may still have existed on a smaller scale, but the cash leg is invisible in this data, so the report can't confirm it either way.

## The model residual

- **Expected:** +4.88% of OI. **Actual:** +0.90%. **Residual:** −3.98 pp.
- That is about 108,000 contracts, or roughly $10.8 billion of face value, below what the model expected.
- It is about 1.9 times the model's RMSE. Only about 5% of earlier out-of-sample residuals were this large, and the actual level falls below the approximate 90% range.

So by the model's own history this is a genuine surprise. Four qualifiers keep it in proportion:

1. **We don't know the actual weekly change.** The expected level is last week's level plus the predicted change, and neither component is given. If the predicted change was near zero, funds cut net length by roughly 4 pp this week. If the model expected a big increase, the actual move may have been small. Either way, the residual is a gap relative to expectations, not a confirmed sell-off by funds.
2. **The model is weak to begin with.** An out-of-sample R² of about 10% means most weekly variation is unexplained. Residuals this size should turn up about once every 20 weeks, so roughly three dozen times across 720 weeks. One flagged week is not rare enough to read much into on its own.
3. **The calendar is unusual.** The week ended Tuesday 2 September, right after the Labor Day holiday. It also sits in the September-to-December contract roll, around first notice day. Open interest of 2.72 million is elevated, which is typical of roll periods. The model includes open-interest change and a quarter-end flag, but roll timing and holiday-thin trading can still distort a single week's positioning in ways it may not capture.
4. **Motive isn't identified.** As the documentation states, the residual doesn't distinguish a bearish duration view, added short-futures hedges against cash longs (basis), curve trades against other contracts, risk reduction, or reclassification noise.

## Market context

From memory, so treat this loosely: 10-year yields had fallen through August 2014 to around the 2.3–2.4% area. Drivers included falling European yields after Draghi's Jackson Hole speech raised ECB easing expectations, geopolitical risk, and the approaching end of Fed asset purchases. Against that backdrop, funds being less long than expected *could* be consistent with reluctance to chase a rally or with positioning for a rebound in yields. That is a plausible story, not something the data establish.

## What would sharpen the read

- Last week's leveraged-fund level and the model's predicted change, to turn the residual into an actual flow.
- Changes in gross long, short and spreading positions, to see whether funds cut longs, added shorts, or shifted into spreads.
- The same report for 2-year, 5-year, bond and ultra-bond futures, to check whether this was a curve trade rather than an outright duration move.
- The following two or three weeks, to see whether the gap persists, which suggests a real repositioning, or reverses, which points to roll or holiday noise.
- Cash-futures basis and repo data for the period, if you want to test the hedging explanation.

Bottom line: real-money investors were long duration through futures, dealers were warehousing the other side, and hedge funds were roughly neutral on a net basis but less long than the model expected. That is a mild, unexplained shift worth following up, not a signal about Treasury direction by itself.

---

## Item 12 | X-a6a02827483b | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 21 June 2016. All figures are numbers of contracts.

Open interest (all contracts): 2,812,962

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 106,836 | 246,143 | 35,772 | -139,307 | -4.95% |
| Asset Manager / Institutional | 923,902 | 822,392 | 370,406 | 101,510 | +3.61% |
| Leveraged Funds | 546,112 | 647,076 | 65,194 | -100,964 | -3.59% |
| Other Reportable | 375,251 | 182,004 | 19,338 | 193,247 | +6.87% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -2.74% of open interest (approximate 90% range based on earlier out-of-sample errors: -6.50% to +1.02%).
- Actual net position this week: -3.59% of open interest.
- Residual (actual minus expected): -0.85 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 31% were smaller than this one and 69% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

Not much, directionally. Leveraged funds were net short, but by about the amount the model expected. The rest of the table looks like the normal structure of the Treasury futures market, not a strong bet in either direction.

The model result is unremarkable. Leveraged funds were net short 3.59% of open interest against an expected 2.74%. The −0.85 point residual sits well inside the 90% range (−6.50% to +1.02%). About 69% of past out-of-sample misses were as large or larger, so this one is close to the 31st percentile of absolute errors. That means no unusual crowding on the short side and nothing pointing to a squeeze. The 90% band is also about 7.5 points wide, so even a larger residual would need care before reading much into it.

The short is probably not a bearish view. In 10-year note futures, leveraged funds tend to be short partly because of the cash-futures basis trade: long cash Treasuries, short futures, earning the gap between them. A net short in futures can therefore sit alongside a flat or even long exposure to rates overall. Asset managers usually take the other side, using long futures to add duration cheaply. Their +3.61% net long fits that pattern. Dealers (−4.95%) and other reportables (+6.87%) look like the intermediary and hedging flows that typically fill out the book. The four reportable groups net to about +54,500 contracts, so non-reportable traders were net short roughly 1.9% of open interest.

The timing. Positions are as of Tuesday 21 June 2016, two days before the Brexit referendum. The data don’t show hedge funds positioned for a big risk-off move. They also don’t show a heavy bet against bonds. Looking back, Treasuries rallied hard after the vote, and the 10-year yield fell to record lows in early July. A positioning signal measured just beforehand would not have flagged that, which is a reminder that this kind of data describes the market’s structure better than it predicts the next move in yields.

Limits of a single snapshot:

One week of levels says less than the week-on-week change, or where this residual falls in the model’s history over recent months.
The report covers futures only. It leaves out cash bonds, swaps and options, which is where the other side of a basis trade sits.
Grouping by trader category mixes very different motives within each group.

In short: positioning was mildly short in line with the model and structurally normal. It doesn’t support a strong call on yields, though it does suggest there was no crowded trade waiting to unwind.

---

## Item 13 | X-0cae2719ff82 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 7 May 2019. All figures are numbers of contracts.

Open interest (all contracts): 4,015,511

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 197,596 | 173,983 | 59,386 | 23,613 | +0.59% |
| Asset Manager / Institutional | 1,707,346 | 954,169 | 767,698 | 753,177 | +18.76% |
| Leveraged Funds | 356,404 | 1,259,989 | 128,279 | -903,585 | -22.50% |
| Other Reportable | 317,986 | 229,563 | 23,460 | 88,423 | +2.20% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -21.10% of open interest (approximate 90% range based on earlier out-of-sample errors: -24.66% to -17.53%).
- Actual net position this week: -22.50% of open interest.
- Residual (actual minus expected): -1.41 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 55% were smaller than this one and 45% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The CFTC report and model output point to a classic structural standoff between real-money institutions and leveraged speculators, with speculator positioning sitting comfortably in line with model expectations rather than signaling a fresh market dislocation.

### 1. Structural Polarization: Asset Managers vs. Leveraged Funds

The core dynamic in 10-Year Treasury Note futures is an opposition between long-term institutional asset managers and leveraged funds (hedge funds and CTAs):

* **Leveraged Funds (-22.50% of OI, net -903,585 contracts):** Speculators hold a substantial net short position, with outright shorts outnumbering longs by more than 3.5 to 1. In isolation, this looks like a strong directional bet on higher 10-year yields (lower futures prices). However, in Treasury markets, leveraged fund futures shorts frequently reflect **cash-futures basis trading** (buying cheap-to-deliver cash Treasuries and shorting the futures contract to capture arbitrage spread) or curve/swap spread trades rather than pure macroeconomic bets against bonds.
* **Asset Managers / Institutional (+18.76% of OI, net +753,177 contracts):** Real-money accounts—such as pension funds, insurance companies, and mutual funds—absorb the bulk of the leveraged funds' short supply. Asset managers systematically use Treasury futures to add duration efficiently without tying up balance sheet cash, providing the structural bid on the other side of the basis trade. Total institutional activity is also notable for its large **spreading** component (767,698 contracts, or ~19.1% of total OI), indicating heavy calendar-roll or relative-value positioning within the institutional complex.
* **Dealers (+0.59% of OI) & Other Reportables (+2.20% of OI):** Both groups hold modest net long positions. Dealers are nearly flat on a net basis, functioning primarily as market-making intermediaries rather than warehousers of directional futures risk.
* **Implied Non-Reportable Positioning (+0.95% of OI):** Summing the four reportable net positions yields -38,372 contracts (-0.95% of OI). By market identity, non-reportable (smaller/retail) traders hold the offsetting net long position of +38,372 contracts (+0.95% of OI), confirming that small traders have negligible influence on the market's clearing balance.

---

### 2. Model Evaluation: No Positioning Anomaly

While a -22.50% net short by leveraged funds appears large at face value, the supervised model (v4.0) shows this positioning is completely normal relative to prevailing macro, curve, or basis drivers:

* **Well Within Expected Bounds:** The actual net position (-22.50%) sits comfortably inside the model’s 90% prediction interval (-24.66% to -17.53%).
* **Typical Residual Noise:** The residual of -1.41 percentage points (leveraged funds are slightly more net short than the -21.10% forecast) sits near the median of historical out-of-sample errors, with 45% of prior absolute residuals being at least this large. Statistically, a -1.41% deviation is indistinguishable from routine weekly noise.

---

### 3. Market Implications & Risks

Because leveraged fund positioning aligns closely with model fundamentals, the report offers **no contrarian trading signal** on its own—speculators are neither abnormally stretched nor diverging from the variables driving the model.

However, the **absolute magnitude** of the positioning carries latent liquidity and unwind risks:

1. **Short-Covering / Basis Unwind Vulnerability:** With leveraged funds holding 1.26 million short contracts (over 31% of total open interest), the market remains vulnerable to sudden volatility shocks. If a sharp flight-to-quality rally sends yields plunging, or if repo financing rates spike, leveraged funds can be forced to cover shorts rapidly, accelerating a rally in Treasury futures.
2. **Orderly Equilibrium for Now:** As long as financing conditions remain stable and asset managers continue to demand futures duration (+18.76% of OI), this large speculative short serves as a stable structural feature of the market rather than an immediate catalyst for repricing.

---

## Item 14 | X-655bcdd9779e | R applicable: YES

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

## Treasury market positioning: Week ending 24 June 2025

The positioning suggests a heavily crowded Treasury basis trade, with leveraged funds substantially short 10-year Treasury futures and asset managers strongly long. However, leveraged funds are less short than the model would expect, providing a modestly constructive signal for Treasuries relative to the prevailing positioning environment.

The distinction is between absolute positioning, which remains extremely short for leveraged funds, and positioning relative to expectations, which is moderately less bearish.

### 1. The market has a pronounced structural positioning imbalance

Net positions as a percentage of open interest

Asset managers

+42.19%

Other reportables

+2.11%

Dealers

-7.35%

Leveraged funds

-38.92%

Positive values indicate net long futures; negative values indicate net short futures.

Leveraged funds are net short approximately 1.91 million contracts, or 38.92% of total open interest. Asset managers are net long approximately 2.08 million contracts, or 42.19% of open interest.

This is consistent with substantial participation in the cash-futures basis trade, in which leveraged funds buy cash Treasuries and short Treasury futures, while institutional investors hold long futures exposure.

Consequently, the large leveraged-fund futures short does not necessarily represent an outright bearish view on Treasury prices or a prediction of rising yields. It may primarily reflect hedging of long cash Treasury positions and relative-value activity.

The report does not disclose the corresponding cash positions, financing arrangements, or motivations of these traders, so it cannot establish how much of the short is attributable to basis trading.

### 2. The model shows moderately less short positioning than expected

Leveraged-fund net position versus model expectation

Expected

## -41.90%

Actual

## -38.92%

Residual

## +2.98 pp

Shaded interval: approximate 90% range based on previous out-of-sample errors.

The model predicts leveraged funds should be net short 41.90% of open interest, whereas they are actually short 38.92%.

The positive residual of +2.98 percentage points indicates that leveraged funds are less net short than the model predicts given its inputs.

That is potentially Treasury-supportive in a relative sense: there is less futures short exposure than the modeled baseline would suggest.

But the strength of this signal should not be overstated:

- The actual position falls within the model's approximate 90% error range, although close to its upper boundary.
- Approximately 16% of earlier absolute out-of-sample residuals were at least this large.
- The observation is therefore somewhat unusual, but not an extreme statistical outlier.

Importantly, a positive residual describes positioning relative to the model, not necessarily actual short covering during the reporting week. Establishing whether funds reduced shorts would require the previous week's positions.

### 3. Implications for Treasury prices and yields

Three interpretations matter.

First, the crowded positioning creates potential deleveraging risk. If leveraged funds are substantially engaged in basis trading, adverse financing conditions, margin pressures, or volatility could prompt them to unwind. That could involve buying back Treasury futures shorts while selling cash Treasuries. The resulting effect on Treasury yields is ambiguous because futures and cash-market transactions could exert opposing pressures, and market liquidity matters.

Second, the positive residual suggests relatively less pressure from leveraged-fund futures shorts than expected. This can be interpreted as a mildly constructive positioning signal for Treasury futures, but it does not establish that leveraged funds have become outright bullish.

Third, the model residual alone does not establish predictive power for subsequent Treasury returns. That would require historical evidence linking residuals to future changes in Treasury futures prices, yields, or basis spreads, ideally measured out of sample.

### 4. Overall assessment

| Dimension                                 | Interpretation                                                |
| ----------------------------------------- | ------------------------------------------------------------- |
| Absolute leveraged-fund positioning       | Extremely large net futures short                             |
| Asset-manager positioning                 | Strong net futures long                                       |
| Likely market structure                   | Consistent with substantial basis/relative-value activity     |
| Model-adjusted leveraged-fund positioning | Moderately less short than expected                           |
| Statistical significance                  | Unusual but within the approximate 90% error range            |
| Directional Treasury signal               | Mildly constructive, but not independently decisive           |
| Principal vulnerability                   | Crowded positions and possible disorderly basis-trade unwinds |

Bottom line: The Treasury market displays substantial leveraged-fund short futures exposure matched by large institutional longs, a configuration consistent with a significant cash-futures basis trade. Yet leveraged funds are less short than the supervised model anticipates, generating a moderately positive positioning surprise.

This suggests a somewhat more supportive Treasury futures positioning backdrop than the headline shorts alone imply, without providing strong evidence for an imminent rally or falling Treasury yields.

The critical distinction is that the residual measures unexpected positioning, not necessarily unexpected directional conviction. Whether it carries a bullish return signal depends on evidence that this particular model's residuals predict subsequent market outcomes.

---

## Item 15 | X-e71e9fec1715 | R applicable: YES

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
