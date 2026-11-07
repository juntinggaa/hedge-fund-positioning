# Replies for JunTing (15 replies)

Code each one in SHEET_JunTing.csv, same item number.

---

## Item 1 | X-50bc0731c545 | R applicable: YES

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

## Item 2 | X-020732f2b84e | R applicable: NO

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 9 February 2016. All figures are numbers of contracts.

Open interest (all contracts): 3,034,110

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 80,778 | 303,547 | 77,823 | -222,769 | -7.34% |
| Asset Manager / Institutional | 1,168,268 | 745,867 | 370,007 | 422,401 | +13.92% |
| Leveraged Funds | 459,277 | 773,971 | 142,387 | -314,694 | -10.37% |
| Other Reportable | 344,830 | 167,093 | 17,219 | 177,737 | +5.86% |

What does this positioning suggest about the Treasury market?

### REPLY

The positioning suggests a significant divergence between institutional investors and leveraged speculative traders, with asset managers strongly positioned for higher Treasury prices (lower yields), while leveraged funds and dealers are heavily net short.

### 1. Institutional investors show a bullish duration bias

Asset managers are net long 422,401 contracts (+13.92% of open interest), the largest positive net position among the reported categories.

This suggests substantial institutional demand for Treasury duration, potentially reflecting expectations of falling interest rates, concerns about economic growth, or demand for safe-haven assets.

Because Treasury futures prices generally move inversely to yields, this positioning is consistent with a bullish view on Treasury prices.

### 2. Leveraged funds are positioned on the opposite side

Leveraged funds are net short 314,694 contracts (-10.37% of open interest).

This could reflect expectations of rising yields or a reversal in Treasury prices. However, leveraged funds also engage in relative-value strategies, including cash-futures basis trades, where short futures positions may hedge long cash Treasury holdings.

Therefore, their net short position should not automatically be interpreted as an outright bearish macroeconomic view.

### 3. Dealers are also heavily net short

Dealers are net short 222,769 contracts (-7.34% of open interest).

Dealer positioning often reflects market-making, inventory hedging, and facilitating institutional client demand rather than independent directional speculation.

Their short exposure may therefore partly represent the other side of institutional demand for Treasury futures.

### 4. The market shows substantial positioning divergence

Net positions as a percentage of total open interest

Asset Manager

+13.92%

Other Reportable

+5.86%

Dealer

-7.34%

Leveraged Funds

-10.37%

Net shortNet long

The principal divide is between asset managers holding substantial net long exposure and leveraged funds holding substantial net short exposure.

This divergence creates the potential for sharp price adjustments if one side is forced to unwind.

For example, a continued decline in Treasury yields could pressure leveraged funds to cover short futures positions, potentially reinforcing a rally. Conversely, rising yields could induce institutional long liquidation, adding selling pressure.

### 5. What the figures cannot establish

The report is a snapshot rather than a record of changes in positioning. Without previous weeks' data, we cannot determine whether these positions have recently increased, whether they are historically extreme, or whether a reversal is already underway.

Furthermore, futures positioning alone does not establish the full economic exposure of each category because traders may hold offsetting positions in cash Treasuries, swaps, options, or other instruments.

### Overall interpretation

The Treasury market appears divided between substantial institutional demand for duration and significant short futures exposure among leveraged funds and dealers.

The institutional net long position is consistent with a defensive or lower-yield outlook, while leveraged funds' net shorts may reflect bearish expectations, hedging, or relative-value trading.

The most important implication is not that the overall market is unambiguously bullish or bearish, but that the divergence in positioning could amplify Treasury price movements, particularly if leveraged funds are compelled to cover shorts during a bond rally.

The report therefore suggests an institutional bullish-duration bias alongside meaningful potential for short-covering pressure, but it does not by itself provide a reliable directional forecast.

---

## Item 3 | X-8b5e5fd77636 | R applicable: YES

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

## Item 4 | X-bde31a9dfa2a | R applicable: NO

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

## Item 5 | X-0d128f720625 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 1 September 2015. All figures are numbers of contracts.

Open interest (all contracts): 2,804,430

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 64,173 | 182,172 | 33,325 | -117,999 | -4.21% |
| Asset Manager / Institutional | 1,168,462 | 674,496 | 329,852 | 493,966 | +17.61% |
| Leveraged Funds | 395,489 | 758,920 | 132,946 | -363,431 | -12.96% |
| Other Reportable | 316,242 | 226,386 | 24,659 | 89,856 | +3.20% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -12.60% of open interest (approximate 90% range based on earlier out-of-sample errors: -16.49% to -8.71%).
- Actual net position this week: -12.96% of open interest.
- Residual (actual minus expected): -0.36 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 17% were smaller than this one and 83% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

For the week ending September 1, 2015, the 10-Year U.S. Treasury Note futures market displays a classic **institutional-versus-speculative structural divergence**, combined with leveraged-fund positioning that evolved closely in line with its conditional statistical relationship to market conditions and lagged positioning.

---

### 1. Structural Balance of the Futures Market

The CFTC breakdown across the **2,804,430** open contracts highlights a polarized distribution of duration exposure across reportable segments:

* **Asset Managers as the Dominant Long Anchor (+493,966 net contracts | +17.61% of OI):** Real-money institutional investors (pension funds, mutual funds, insurance companies) hold massive gross long exposure (1,168,462 contracts, or ~41.7% of total open interest). They also account for the largest spreading activity (329,852 contracts), reflecting active portfolio duration matching and calendar-spread management.
* **Leveraged Funds as the Primary Net Shorts (-363,431 net contracts | -12.96% of OI):** Hedge funds and CTAs hold 758,920 gross short contracts against 395,489 gross longs—nearly a 2-to-1 short-to-long ratio. Alongside **Dealers / Intermediaries** (-117,999 net contracts | -4.21% of OI), leveraged funds supply the short futures liquidity that offsets institutional long demand.
* **Other Reportables (+89,856 net contracts | +3.20% of OI) & Non-Reportable Balance:** Corporate treasuries, central banks, and smaller reportable traders hold a modest net long stance. Notably, summing the four reportable categories leaves a net long reportable balance of **+102,392 contracts** (+3.65% of OI), implying that **non-reportable (small) traders** hold an offsetting net short position of **-102,392 contracts** (-3.65% of OI).

---

### 2. What the Supervised Model (v4.0) Indicates About Leveraged Funds

Comparing the actual leveraged-fund net position (**-12.96% of OI**) against the model's conditional expectation (**-12.60% of OI**) yields a very small residual of **-0.36 percentage points of OI** (roughly 10,096 contracts more net short than projected):

* **No Abnormal Positioning Shock:** A residual of -0.36 percentage points is tiny relative to the model's out-of-sample RMSE of **2.07 percentage points** and sits well inside the approximate 90% error interval (-16.49% to -8.71%). Because **83%** of earlier out-of-sample weeks produced an absolute residual at least this large, the weekly shift in leveraged-fund positioning was completely routine given that week's yield changes, volatility, funding proxies, open-interest shifts, and lagged positioning.
* **Alignment with Concurrent Market Dynamics:** Rather than representing an idiosyncratic positioning squeeze or sudden regime break, the -12.96% net short reading largely reflects persistence from the prior week's positioning plus standard conditional adjustments to contemporary market and open-interest variables.

---

### 3. Essential Analytical Caveats (What the Data *Cannot* Tell Us)

Interpreting futures-only CFTC data alongside Model v4.0 requires strict boundaries on inference:

1. **Unobserved Cash Legs & Ambiguous Motives:** A -12.96% leveraged-fund net short position in 10-year futures **cannot** be automatically equated to a directional bet on rising yields. Leveraged funds frequently short Treasury futures against long cash Treasuries (the cash-futures basis trade), trade yield-curve spreads against 2-year or 30-year contracts, or hedge corporate credit and MBS books. Because cash positions are unobserved and the model lacks direct cash-futures basis profitability inputs, neither the CFTC table nor the model can separate directional shorts from relative-value or basis positions.
2. **Modest Incremental Explanatory Power:** While the -0.36 pp residual is small, the model's overall out-of-sample $R^2$ is **10.47%** relative to an expanding historical-mean change benchmark, and its 90% prediction interval spans **7.78 percentage points of OI** (-16.49% to -8.71%, equivalent to ~218,000 contracts). A near-zero residual in a single week indicates the absence of an unexpected weekly shock, not that the model captures the underlying economic strategy of the entire -363,431 contract position.
3. **Diagnostic Rather Than Predictive:** Because Model v4.0 relies on same-week market variables and concurrent CFTC open interest—and was specified retrospectively—it serves as a **contemporaneous attribution check** (confirming that the week's flow behaved normally relative to observable market moves) rather than a forward-looking trading signal for subsequent Treasury yields.

---

## Item 6 | X-0a72effc75f9 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 12 July 2016. All figures are numbers of contracts.

Open interest (all contracts): 2,877,360

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 151,097 | 163,256 | 42,092 | -12,159 | -0.42% |
| Asset Manager / Institutional | 866,601 | 1,047,093 | 396,958 | -180,492 | -6.27% |
| Leveraged Funds | 621,257 | 595,127 | 54,961 | 26,130 | +0.91% |
| Other Reportable | 353,456 | 161,842 | 19,435 | 191,614 | +6.66% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +0.41% of open interest (approximate 90% range based on earlier out-of-sample errors: -3.33% to +4.15%).
- Actual net position this week: +0.91% of open interest.
- Residual (actual minus expected): +0.50 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 22% were smaller than this one and 78% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

## Treasury market positioning — 12 July 2016

Bottom line: Positioning in 10-Year U.S. Treasury Note futures suggests a relatively balanced leveraged-fund market, with a modest net long bias. There is little evidence of an unusually strong speculative bullish position, an extreme crowding of leveraged investors, or a positioning imbalance that independently signals a major reversal.

### 1. Leveraged funds are modestly net long

Leveraged funds hold 621,257 long contracts against 595,127 short contracts, producing a net long position of 26,130 contracts, or +0.91% of total open interest.

Because Treasury futures prices generally rise when yields fall, this position represents a modest directional tilt toward higher Treasury prices and lower yields.

However, the gross long and short positions are both substantial and relatively close in size. This suggests that leveraged funds are engaged in considerable two-sided activity rather than expressing a strong, unified directional view.

### 2. The model shows no meaningful positioning anomaly

Leveraged-fund net positioning, % of open interest

The actual position exceeds the model expectation by +0.50 percentage points of open interest.

That deviation is small relative to the model's historical forecasting errors:

- The actual position is comfortably inside the approximate 90% error range of −3.33% to +4.15%.
- Approximately 78% of earlier absolute out-of-sample residuals were at least as large.
- Consequently, the residual provides little evidence of unusual bullish positioning once the model's expected positioning is accounted for.

The key distinction is between being net long and being unexpectedly net long. Leveraged funds are slightly net long, but their positioning is broadly consistent with what the model predicts.

### 3. Other trader categories show more pronounced differences

| Category                      | Net % of OI | Interpretation     |
| ----------------------------- | ----------- | ------------------ |
| Dealer / Intermediary         | −0.42%      | Nearly balanced    |
| Asset Manager / Institutional | −6.27%      | Material net short |
| Leveraged Funds               | +0.91%      | Slight net long    |
| Other Reportable              | +6.66%      | Material net long  |

The contrast between asset managers and other reportable traders is notable. Asset managers hold a substantial net short, while other reportable traders hold a similarly large net long.

However, these positions should not automatically be interpreted as opposing outright forecasts for Treasury yields. Asset managers may use futures to hedge cash Treasury holdings or manage portfolio duration. Likewise, other reportable positions may reflect hedging, relative-value transactions, or other strategies.

Therefore, these category-level imbalances identify where exposures are concentrated but do not establish the underlying economic motivations.

### 4. Implications for Treasury prices and yields

Near-term directional implications: Mildly bullish from leveraged-fund net exposure alone, but essentially neutral when compared with model expectations. The data do not support a strong prediction of falling or rising yields.

Positioning-driven reversal risk: There is no clear evidence of an exceptionally crowded leveraged-fund long that would make the market particularly vulnerable to forced long liquidation. Nor is there an extreme leveraged-fund short that would obviously suggest substantial short-covering potential.

Market vulnerability: Asset managers' net shorts and other reportable traders' net longs could matter if market conditions shift abruptly. But identifying which positions are vulnerable requires additional information about hedging, leverage, funding, and recent position changes.

Important limitation: This is a single weekly snapshot. It does not reveal whether positions were recently accumulated or reduced, and the reported futures positions cannot be equated directly with all investors' aggregate Treasury duration exposures.

## Overall assessment

The 12 July 2016 report is best interpreted as neutral to mildly bullish Treasury positioning among leveraged funds, without an unusual model-adjusted signal.

The slightly positive leveraged-fund net position indicates a small preference for higher Treasury futures prices (lower yields), but the +0.50-percentage-point residual is unremarkable by historical out-of-sample standards.

The larger cross-category differences are worth monitoring, particularly the asset-manager net short versus other-reportable net long. Nevertheless, they are not sufficient to conclude that the Treasury market is either excessively bullish or excessively bearish.

Trading implication: This report alone does not provide a compelling contrarian signal, a strong directional yield forecast, or evidence of a significant leveraged-fund positioning squeeze. A meaningful conclusion would require positioning trends, price and yield changes, and broader market context.

---

## Item 7 | X-b4b9a293e0e8 | R applicable: YES

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

## Item 8 | X-634126fcfbb4 | R applicable: YES

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

## Item 9 | X-4bb9bd3f1065 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 14 April 2026. All figures are numbers of contracts.

Open interest (all contracts): 5,187,440

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 206,647 | 601,050 | 71,358 | -394,403 | -7.60% |
| Asset Manager / Institutional | 3,049,475 | 836,218 | 682,383 | 2,213,257 | +42.67% |
| Leveraged Funds | 328,463 | 2,338,434 | 125,587 | -2,009,971 | -38.75% |
| Other Reportable | 317,570 | 168,861 | 251 | 148,709 | +2.87% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -38.38% of open interest (approximate 90% range based on earlier out-of-sample errors: -41.80% to -34.96%).
- Actual net position this week: -38.75% of open interest.
- Residual (actual minus expected): -0.36 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 16% were smaller than this one and 84% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

**Short version:** this snapshot shows the familiar mirror-image structure of Treasury futures. Asset managers are heavily long, leveraged funds are heavily short, and dealers are modestly short. The model output says this week was ordinary. It tells you almost nothing new about where yields are going, and it can’t confirm a basis trade.

**What the positioning itself shows**

The two dominant groups are almost exact offsets. Asset managers are net long about 2.21 million contracts (+42.7% of OI), and leveraged funds are net short about 2.01 million (−38.7%). Gross concentration is high on both sides:

- Asset managers hold about 59% of all reportable long positions measured against OI.
- Leveraged funds hold about 45% of the short side.

At $100,000 face per contract, the leveraged-fund net short is roughly $200bn face of 10-year exposure. The nets reconcile cleanly: the four categories sum to −42,408, so non-reportable traders are net long by that amount, about +0.8% of OI.

This pattern fits a well-known division of labour:

- Asset managers use futures as a capital-efficient way to hold duration against benchmarks.
- Leveraged funds take the other side, often (but not provably) as the short-futures leg of a cash-futures basis trade: long cash Treasuries financed in repo, short futures.

The CFTC data only show the futures leg, so the same short could also be:

- an outright bearish bet,
- a curve or cross-tenor trade against other Treasury contracts,
- a hedge of something else.

**What the model output adds**

Very little, and that is the informative part.

- The actual level (−38.75%) sits 0.36pp below the model’s expectation. That is about 19,000 contracts, against a historical RMSE of about 2.07pp (roughly 107,000 contracts).
- 84% of earlier out-of-sample residuals were at least this large, so this is a quiet week.
- The leveraged-fund adjustment was about what returns, volatility, funding conditions, OI changes and lagged positions would typically be associated with.
- There is no sign of an unusual build-up or an unexpected unwind.

Three caveats limit how far you can push this:

- **Weekly change is unknown.** The expected level is last week’s level plus a predicted change, and last week’s level isn’t given. A small residual doesn’t mean little happened, only that whatever happened was roughly in line with the inputs.
- **Modest predictive power.** The out-of-sample R² of about 10% means most weekly variation in leveraged-fund positioning is unexplained even in a quiet week.
- **No motive or basis inference.** By the model’s own description, neither the fitted part nor the residual measures basis profitability or identifies motives.

**What it suggests about the Treasury market**

*Market structure.* A large share of 10-year futures demand from real-money investors is being met by leveraged, likely repo-financed intermediaries. In normal conditions this is benign and arguably useful: it connects cash and futures pricing and lets asset managers get duration cheaply.

*Vulnerability.* The risk is in the tails. If much of that short is basis-related, the position depends on stable repo funding and margin requirements. A funding shock, margin hikes, or a sharp volatility spike could force simultaneous unwinds, with leveraged funds selling cash Treasuries into a thin market. That was the dynamic in March 2020. Positions of this size are why regulators watch this metric. Still, nothing in this week’s data signals that such stress was starting; the residual is unremarkable.

*Direction.* Don’t read the leveraged-fund short as a bearish signal, or as a contrarian “crowded short” buy signal. If it is largely hedged by cash holdings, it carries little net duration view.

**Context**

This report is for mid-April 2026, nearly seven months before today. Without the surrounding weeks, I can’t say whether −38.75% is high or low relative to the recent range or which way the trend was running. If you have the prior weeks’ levels, the actual weekly change and the trajectory would be more informative than this single snapshot.

---

## Item 10 | X-655bcdd9779e | R applicable: YES

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

## Item 11 | X-bf2236a568b4 | R applicable: YES

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

---

## Item 12 | X-c9b932c5e664 | R applicable: YES

### NUMERIC REFERENCE

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 14 April 2026. All figures are numbers of contracts.

Open interest (all contracts): 5,187,440

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 206,647 | 601,050 | 71,358 | -394,403 | -7.60% |
| Asset Manager / Institutional | 3,049,475 | 836,218 | 682,383 | 2,213,257 | +42.67% |
| Leveraged Funds | 328,463 | 2,338,434 | 125,587 | -2,009,971 | -38.75% |
| Other Reportable | 317,570 | 168,861 | 251 | 148,709 | +2.87% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -38.38% of open interest (approximate 90% range based on earlier out-of-sample errors: -41.80% to -34.96%).
- Actual net position this week: -38.75% of open interest.
- Residual (actual minus expected): -0.36 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 16% were smaller than this one and 84% were at least as large.

What does this positioning suggest about the Treasury market?

### REPLY

The positioning data points to a heavily bifurcated 10-Year U.S. Treasury futures market where institutional asset managers rely on futures for long duration exposure and leveraged funds act as the primary short-side counterparty, while the model output indicates that the latest weekly shift was routine given prevailing market conditions.

Structural Counterparty Split

Institutional duration demand: Asset managers are net long 2,213,257 contracts (+42.67% of the 5,187,440 open interest), reflecting strong structural demand for synthetic long duration via futures rather than cash bonds.

Leveraged fund and dealer supply: Leveraged funds absorb the vast majority of this demand on the short side at -2,009,971 contracts (-38.75%), supplemented by dealers at -394,403 contracts (-7.60%).

Minority balance: Other reportable traders (+148,709 net, or +2.87%) and implied non-reportable participants (+42,408 net, or +0.82%) hold small net long positions that balance total market open interest.

Spreading concentration: Asset managers also dominate spreading positions with 682,383 contracts (over 77% of all reportable spreading), pointing to active intra-category calendar rolling or portfolio hedging.

Weekly Adjustment vs. Historical Norms

Routine weekly flow: The actual leveraged-fund net short exceeded the model's conditional expectation of -38.38% by a residual of just -0.36 percentage points, sitting near the center of the -41.80% to -34.96% historical range.

No positioning shock: Because 84% of prior out-of-sample absolute errors were at least as large (against a 2.07 percentage point RMSE), this week's adjustment reflects normal responsiveness to market, open-interest, and funding inputs.

Limits on Inferring Motives and the Basis Trade

Unobserved cash legs: While opposing asset-manager longs and leveraged-fund shorts are a classic footprint of the cash-futures basis trade, futures-only CFTC data omits cash Treasuries, repo financing, and swaps.

Indeterminate strategy mix: Consequently, the data cannot separate how much of the leveraged-fund short is hedged against cash bonds (basis or relative-value trades) versus unhedged directional bets on higher yields.

Model scope: Because the expected level simply adds an estimated weekly change to last week's position, neither the expectation nor the residual identifies basis profitability, strategy share, or private information.

Market Structure and Forecasting Implications

Roll and funding sensitivity: Heavy concentration on opposing sides makes quarterly rolls and market liquidity sensitive to repo funding stress, margin shifts, and dealer intermediation capacity regardless of trader motive.

No directional signal: Because the model relies on same-week open interest, was chosen retrospectively, and explains 10.47% of out-of-sample variance, it describes contemporaneous alignment rather than forecasting future yields.

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

## Item 14 | X-fbe48fdabbca | R applicable: YES

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

## Item 15 | X-02609bbb3182 | R applicable: YES

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
