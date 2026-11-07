# Pilot prompts (collector only)

## 2021-09-21 — A

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 21 September 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,934,302

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 211,953 | 227,582 | 41,198 | -15,629 | -0.40% |
| Asset Manager / Institutional | 1,458,078 | 1,409,497 | 788,616 | 48,581 | +1.23% |
| Leveraged Funds | 853,740 | 498,222 | 99,743 | 355,518 | +9.04% |
| Other Reportable | 133,901 | 292,990 | 9,644 | -159,089 | -4.04% |

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2021-09-21 — B

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 21 September 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,934,302

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 211,953 | 227,582 | 41,198 | -15,629 | -0.40% |
| Asset Manager / Institutional | 1,458,078 | 1,409,497 | 788,616 | 48,581 | +1.23% |
| Leveraged Funds | 853,740 | 498,222 | 99,743 | 355,518 | +9.04% |
| Other Reportable | 133,901 | 292,990 | 9,644 | -159,089 | -4.04% |

Context you may find relevant: leveraged funds sometimes hold short positions in Treasury futures as one leg of a cash-futures basis trade, in which the fund buys the underlying Treasury security, finances it in the repo market, and sells the corresponding futures contract. A position held for that reason expresses a relative-value view about the spread between the cash and futures markets rather than a directional view about the level of yields. Asset managers may likewise hold futures for duration management, benchmark replication or liability hedging rather than as a discretionary forecast.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2021-09-21 — C-bare

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 21 September 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,934,302

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 211,953 | 227,582 | 41,198 | -15,629 | -0.40% |
| Asset Manager / Institutional | 1,458,078 | 1,409,497 | 788,616 | 48,581 | +1.23% |
| Leveraged Funds | 853,740 | 498,222 | 99,743 | 355,518 | +9.04% |
| Other Reportable | 133,901 | 292,990 | 9,644 | -159,089 | -4.04% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +7.31% of open interest (approximate 90% range based on earlier out-of-sample errors: +3.74% to +10.88%).
- Actual net position this week: +9.04% of open interest.
- Residual (actual minus expected): +1.73 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 61% were smaller than this one and 39% were at least as large.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2021-09-21 — C-ann

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 21 September 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,934,302

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 211,953 | 227,582 | 41,198 | -15,629 | -0.40% |
| Asset Manager / Institutional | 1,458,078 | 1,409,497 | 788,616 | 48,581 | +1.23% |
| Leveraged Funds | 853,740 | 498,222 | 99,743 | 355,518 | +9.04% |
| Other Reportable | 133,901 | 292,990 | 9,644 | -159,089 | -4.04% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +7.31% of open interest (approximate 90% range based on earlier out-of-sample errors: +3.74% to +10.88%).
- Actual net position this week: +9.04% of open interest.
- Residual (actual minus expected): +1.73 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 61% were smaller than this one and 39% were at least as large.

How to read the model output above (model v4.0). This is a retrospective same-week conditional estimate of the weekly CHANGE in leveraged funds' net position as a share of open interest. It uses returns, realised volatility, yield levels and curve shape, equity volatility, a funding-stress proxy, a futures-yield return residual, current-week open-interest change, changes in Fed Treasury holdings, a quarter-end flag, and lagged own, other-group and cross-contract positions. More recent training observations receive more weight, with a two-year half-life.

- The expected level equals last week's actual level plus the model's estimated weekly change. The residual is equivalently the conditional level gap or the unexpected weekly adjustment, measured in percentage points of open interest. It is not an identified fraction of the whole position attributable to any strategy.
- These are statistical associations. The cash leg of a basis trade is unobserved; none of the inputs directly measures genuine cash-futures basis profitability. Neither the expected component nor the residual identifies motives, basis quantities or private information.
- Across 720 out-of-sample weeks (2012-11-27 to 2026-09-08), squared prediction error was 10.47% lower than an expanding historical-mean change benchmark (out-of-sample R²). RMSE was 2.07 percentage points of open interest. This R² is not a percentage of the outstanding position explained by a strategy.
- The approximate range uses only errors from earlier out-of-sample weeks. Its realised historical coverage was 91.9% across 668 eligible weeks, with variation across eras. This is not a guaranteed probability for this individual week. Being inside a broad range does not mean the point prediction closely anticipated the move.
- The model includes current-week CFTC open interest, so this is not a pre-Friday nowcast or a next-week forecast. The model and performance summary were selected retrospectively; this is not a historically deployable untouched backtest.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2021-09-21 — D

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 21 September 2021. All figures are numbers of contracts.

Open interest (all contracts): 3,934,302

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 211,953 | 227,582 | 41,198 | -15,629 | -0.40% |
| Asset Manager / Institutional | 1,458,078 | 1,409,497 | 788,616 | 48,581 | +1.23% |
| Leveraged Funds | 853,740 | 498,222 | 99,743 | 355,518 | +9.04% |
| Other Reportable | 133,901 | 292,990 | 9,644 | -159,089 | -4.04% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: +9.23% of open interest (approximate 90% range based on earlier out-of-sample errors: +5.66% to +12.79%).
- Actual net position this week: +9.04% of open interest.
- Residual (actual minus expected): -0.19 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 9% were smaller than this one and 91% were at least as large.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2020-11-03 — A

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 3 November 2020. All figures are numbers of contracts.

Open interest (all contracts): 3,077,241

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 184,831 | 254,045 | 13,600 | -69,214 | -2.25% |
| Asset Manager / Institutional | 1,294,482 | 1,093,048 | 594,378 | 201,434 | +6.55% |
| Leveraged Funds | 317,487 | 565,227 | 62,759 | -247,740 | -8.05% |
| Other Reportable | 242,382 | 107,170 | 780 | 135,212 | +4.39% |

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2020-11-03 — B

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 3 November 2020. All figures are numbers of contracts.

Open interest (all contracts): 3,077,241

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 184,831 | 254,045 | 13,600 | -69,214 | -2.25% |
| Asset Manager / Institutional | 1,294,482 | 1,093,048 | 594,378 | 201,434 | +6.55% |
| Leveraged Funds | 317,487 | 565,227 | 62,759 | -247,740 | -8.05% |
| Other Reportable | 242,382 | 107,170 | 780 | 135,212 | +4.39% |

Context you may find relevant: leveraged funds sometimes hold short positions in Treasury futures as one leg of a cash-futures basis trade, in which the fund buys the underlying Treasury security, finances it in the repo market, and sells the corresponding futures contract. A position held for that reason expresses a relative-value view about the spread between the cash and futures markets rather than a directional view about the level of yields. Asset managers may likewise hold futures for duration management, benchmark replication or liability hedging rather than as a discretionary forecast.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2020-11-03 — C-bare

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 3 November 2020. All figures are numbers of contracts.

Open interest (all contracts): 3,077,241

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 184,831 | 254,045 | 13,600 | -69,214 | -2.25% |
| Asset Manager / Institutional | 1,294,482 | 1,093,048 | 594,378 | 201,434 | +6.55% |
| Leveraged Funds | 317,487 | 565,227 | 62,759 | -247,740 | -8.05% |
| Other Reportable | 242,382 | 107,170 | 780 | 135,212 | +4.39% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -7.86% of open interest (approximate 90% range based on earlier out-of-sample errors: -11.38% to -4.34%).
- Actual net position this week: -8.05% of open interest.
- Residual (actual minus expected): -0.19 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 9% were smaller than this one and 91% were at least as large.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2020-11-03 — C-ann

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 3 November 2020. All figures are numbers of contracts.

Open interest (all contracts): 3,077,241

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 184,831 | 254,045 | 13,600 | -69,214 | -2.25% |
| Asset Manager / Institutional | 1,294,482 | 1,093,048 | 594,378 | 201,434 | +6.55% |
| Leveraged Funds | 317,487 | 565,227 | 62,759 | -247,740 | -8.05% |
| Other Reportable | 242,382 | 107,170 | 780 | 135,212 | +4.39% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -7.86% of open interest (approximate 90% range based on earlier out-of-sample errors: -11.38% to -4.34%).
- Actual net position this week: -8.05% of open interest.
- Residual (actual minus expected): -0.19 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 9% were smaller than this one and 91% were at least as large.

How to read the model output above (model v4.0). This is a retrospective same-week conditional estimate of the weekly CHANGE in leveraged funds' net position as a share of open interest. It uses returns, realised volatility, yield levels and curve shape, equity volatility, a funding-stress proxy, a futures-yield return residual, current-week open-interest change, changes in Fed Treasury holdings, a quarter-end flag, and lagged own, other-group and cross-contract positions. More recent training observations receive more weight, with a two-year half-life.

- The expected level equals last week's actual level plus the model's estimated weekly change. The residual is equivalently the conditional level gap or the unexpected weekly adjustment, measured in percentage points of open interest. It is not an identified fraction of the whole position attributable to any strategy.
- These are statistical associations. The cash leg of a basis trade is unobserved; none of the inputs directly measures genuine cash-futures basis profitability. Neither the expected component nor the residual identifies motives, basis quantities or private information.
- Across 720 out-of-sample weeks (2012-11-27 to 2026-09-08), squared prediction error was 10.47% lower than an expanding historical-mean change benchmark (out-of-sample R²). RMSE was 2.07 percentage points of open interest. This R² is not a percentage of the outstanding position explained by a strategy.
- The approximate range uses only errors from earlier out-of-sample weeks. Its realised historical coverage was 91.9% across 668 eligible weeks, with variation across eras. This is not a guaranteed probability for this individual week. Being inside a broad range does not mean the point prediction closely anticipated the move.
- The model includes current-week CFTC open interest, so this is not a pre-Friday nowcast or a next-week forecast. The model and performance summary were selected retrospectively; this is not a historically deployable untouched backtest.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2020-11-03 — D

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 3 November 2020. All figures are numbers of contracts.

Open interest (all contracts): 3,077,241

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 184,831 | 254,045 | 13,600 | -69,214 | -2.25% |
| Asset Manager / Institutional | 1,294,482 | 1,093,048 | 594,378 | 201,434 | +6.55% |
| Leveraged Funds | 317,487 | 565,227 | 62,759 | -247,740 | -8.05% |
| Other Reportable | 242,382 | 107,170 | 780 | 135,212 | +4.39% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -8.17% of open interest (approximate 90% range based on earlier out-of-sample errors: -11.69% to -4.65%).
- Actual net position this week: -8.05% of open interest.
- Residual (actual minus expected): +0.12 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 6% were smaller than this one and 94% were at least as large.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2025-08-05 — A

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 5 August 2025. All figures are numbers of contracts.

Open interest (all contracts): 5,127,634

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 304,410 | 533,304 | 47,851 | -228,894 | -4.46% |
| Asset Manager / Institutional | 3,055,050 | 843,663 | 528,459 | 2,211,387 | +43.13% |
| Leveraged Funds | 392,296 | 2,638,835 | 92,321 | -2,246,539 | -43.81% |
| Other Reportable | 263,720 | 116,058 | 1,464 | 147,662 | +2.88% |

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2025-08-05 — B

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 5 August 2025. All figures are numbers of contracts.

Open interest (all contracts): 5,127,634

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 304,410 | 533,304 | 47,851 | -228,894 | -4.46% |
| Asset Manager / Institutional | 3,055,050 | 843,663 | 528,459 | 2,211,387 | +43.13% |
| Leveraged Funds | 392,296 | 2,638,835 | 92,321 | -2,246,539 | -43.81% |
| Other Reportable | 263,720 | 116,058 | 1,464 | 147,662 | +2.88% |

Context you may find relevant: leveraged funds sometimes hold short positions in Treasury futures as one leg of a cash-futures basis trade, in which the fund buys the underlying Treasury security, finances it in the repo market, and sells the corresponding futures contract. A position held for that reason expresses a relative-value view about the spread between the cash and futures markets rather than a directional view about the level of yields. Asset managers may likewise hold futures for duration management, benchmark replication or liability hedging rather than as a discretionary forecast.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2025-08-05 — C-bare

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 5 August 2025. All figures are numbers of contracts.

Open interest (all contracts): 5,127,634

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 304,410 | 533,304 | 47,851 | -228,894 | -4.46% |
| Asset Manager / Institutional | 3,055,050 | 843,663 | 528,459 | 2,211,387 | +43.13% |
| Leveraged Funds | 392,296 | 2,638,835 | 92,321 | -2,246,539 | -43.81% |
| Other Reportable | 263,720 | 116,058 | 1,464 | 147,662 | +2.88% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -43.93% of open interest (approximate 90% range based on earlier out-of-sample errors: -47.40% to -40.46%).
- Actual net position this week: -43.81% of open interest.
- Residual (actual minus expected): +0.12 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 6% were smaller than this one and 94% were at least as large.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2025-08-05 — C-ann

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 5 August 2025. All figures are numbers of contracts.

Open interest (all contracts): 5,127,634

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 304,410 | 533,304 | 47,851 | -228,894 | -4.46% |
| Asset Manager / Institutional | 3,055,050 | 843,663 | 528,459 | 2,211,387 | +43.13% |
| Leveraged Funds | 392,296 | 2,638,835 | 92,321 | -2,246,539 | -43.81% |
| Other Reportable | 263,720 | 116,058 | 1,464 | 147,662 | +2.88% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -43.93% of open interest (approximate 90% range based on earlier out-of-sample errors: -47.40% to -40.46%).
- Actual net position this week: -43.81% of open interest.
- Residual (actual minus expected): +0.12 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 6% were smaller than this one and 94% were at least as large.

How to read the model output above (model v4.0). This is a retrospective same-week conditional estimate of the weekly CHANGE in leveraged funds' net position as a share of open interest. It uses returns, realised volatility, yield levels and curve shape, equity volatility, a funding-stress proxy, a futures-yield return residual, current-week open-interest change, changes in Fed Treasury holdings, a quarter-end flag, and lagged own, other-group and cross-contract positions. More recent training observations receive more weight, with a two-year half-life.

- The expected level equals last week's actual level plus the model's estimated weekly change. The residual is equivalently the conditional level gap or the unexpected weekly adjustment, measured in percentage points of open interest. It is not an identified fraction of the whole position attributable to any strategy.
- These are statistical associations. The cash leg of a basis trade is unobserved; none of the inputs directly measures genuine cash-futures basis profitability. Neither the expected component nor the residual identifies motives, basis quantities or private information.
- Across 720 out-of-sample weeks (2012-11-27 to 2026-09-08), squared prediction error was 10.47% lower than an expanding historical-mean change benchmark (out-of-sample R²). RMSE was 2.07 percentage points of open interest. This R² is not a percentage of the outstanding position explained by a strategy.
- The approximate range uses only errors from earlier out-of-sample weeks. Its realised historical coverage was 91.9% across 668 eligible weeks, with variation across eras. This is not a guaranteed probability for this individual week. Being inside a broad range does not mean the point prediction closely anticipated the move.
- The model includes current-week CFTC open interest, so this is not a pre-Friday nowcast or a next-week forecast. The model and performance summary were selected retrospectively; this is not a historically deployable untouched backtest.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

## 2025-08-05 — D

Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year U.S. Treasury Note futures, contract market code 043602, for the week ending 5 August 2025. All figures are numbers of contracts.

Open interest (all contracts): 5,127,634

| Trader category | Long | Short | Spreading | Net | Net as % of OI |
|---|---|---|---|---|---|
| Dealer / Intermediary | 304,410 | 533,304 | 47,851 | -228,894 | -4.46% |
| Asset Manager / Institutional | 3,055,050 | 843,663 | 528,459 | 2,211,387 | +43.13% |
| Leveraged Funds | 392,296 | 2,638,835 | 92,321 | -2,246,539 | -43.81% |
| Other Reportable | 263,720 | 116,058 | 1,464 | 147,662 | +2.88% |

Output of a supervised model of leveraged-fund positioning (model v4.0):

- Expected net position this week: -45.54% of open interest (approximate 90% range based on earlier out-of-sample errors: -49.01% to -42.06%).
- Actual net position this week: -43.81% of open interest.
- Residual (actual minus expected): +1.73 percentage points of open interest. Among earlier absolute out-of-sample residuals, approximately 62% were smaller than this one and 38% were at least as large.

What does this positioning suggest about the Treasury market?

Please answer without using web search.

---

