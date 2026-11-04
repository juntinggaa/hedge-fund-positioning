# Model v3 factor experiment: results (2026-11-05)

Spec: `docs/model_v3/SPEC_2026-11-05.md`, frozen before fitting, with one
amendment made before fitting. **Outcome: no block passes the gate. M3 (v2.0) is
retained.** v1/v2 files are unchanged; hashes are checked by
`tests/test_model_v3.py::test_v1_v2_outputs_preserved`.

```
python scripts/fetch_v3_sources.py   # network; writes data/raw/v3/ + data/manifests/v3_*.json
python scripts/model_v3.py           # offline; writes reports/model_v3/, data/processed/model_v3/
pytest tests/test_model_v3.py
```

## 1. Sources, coverage and timing

| block | source | series | coverage used | known at snapshot *t* (Tuesday) when | notes |
|---|---|---|---|---|---|
| S | FiscalData `auctions_query` (fetched 2026-11-04 UTC, 2,793 Note/Bond rows) | nominal coupon auctions; TIPS and FRNs excluded | auctions from 1979; features from the first CFTC snapshot | settlement: `issue_date` in (prev snapshot, *t*]; result: `auction_date` ≤ *t*; offering size: `announcemt_date` ≤ *t* | gross supply only; net issuance not built |
| D | NY Fed PD API | `PDPOSGSC-G7L11` (net coupons 7–11y), `PDPOSGST-TOT` (net UST ex-TIPS) | as-of 2013-04-03 onward; features from 2016-05-10 after the 156-release z burn-in | value as of Wednesday *a* used only if *a* + 9 days ≤ *t*. That is the Wednesday 13 days earlier (12 in Monday-snapshot weeks). | API has no release timestamps, so the rule is conservative |
| D secondary | NY Fed PD API | fails to deliver + fails to receive, UST ex-TIPS | same | same | reported, not eligible |
| not used | NY Fed PD API | repo / reverse repo totals | – | – | `*` placeholders in 14–30% of weeks since 2022 (runs ≤ 12 weeks); not harmonisable without imputation |

**PD series-break audit** (`reports/model_v3/pd_break_audit.csv`). The first
weekly change after each break (2015-01, 2022-01, 2024-07), as a percentile of
|weekly change| over the prior 156 weeks, ranged from the 3rd to the 80th. None
was above the 99th percentile, so the reset sensitivity run was not triggered.
This audit only detects level jumps. A redefinition that leaves the level smooth
would pass it.

## 2. Results (primary target, pp of OI)

`reports/model_v3/comparison.csv`. In each sample, every model is evaluated on
identical out-of-sample weeks against the M3 refitted on that same sample.

**Full sample**, 720 weeks, 2012-11-27 .. 2026-09-08. M3 here reproduces v2.0's
predictions exactly.

| model | R² vs B1 | R² vs B0 | RMSE | MAE | MZ slope | ΔMSE vs M3 | HAC p (1-sided) | 90% bootstrap CI | gate |
|---|---|---|---|---|---|---|---|---|---|
| B2 AR(1) | 1.82% | 1.67% | 2.167 | 1.662 | 0.70 | | | | |
| **M3** | 7.40% | 7.26% | 2.105 | 1.630 | 1.13 | ref | | | |
| M3+S | 8.41% | 8.27% | 2.093 | 1.614 | 1.02 | +1.09% | 0.151 | [−0.91%, +3.07%] | fail |

**D sample**, 280 weeks, 2021-05-04 .. 2026-09-08. Models are trained only on
weeks with D features (from 2016-05-10), so the first out-of-sample week is
260 weeks later.

| model | R² vs B1 | R² vs B0 | RMSE | MAE | MZ slope | ΔMSE vs matched M3 | HAC p | 90% CI | gate |
|---|---|---|---|---|---|---|---|---|---|
| B2 AR(1) | −1.87% | −1.86% | 2.033 | 1.593 | 0.02 | | | | |
| **M3 (matched)** | 9.05% | 9.06% | 1.921 | 1.500 | 1.95 | ref | | | |
| M3+D | 8.04% | 8.06% | 1.932 | 1.509 | 2.13 | −1.11% | 0.850 | [−3.24%, +0.35%] | fail |
| M3+S+D | 8.15% | 8.16% | 1.930 | 1.510 | 2.15 | −0.99% | 0.848 | [−2.67%, +0.28%] | fail |
| M3+D+fails *(secondary)* | 8.84% | 8.86% | 1.923 | 1.505 | 2.05 | −0.23% | 0.687 | [−0.90%, +0.39%] | n/a |
| *v2.0 M3 as fitted (context)* | 7.39% | 7.41% | 1.938 | 1.533 | 1.16 | −1.82% | 0.764 | [−5.13%, +1.88%] | n/a |

(Positive ΔMSE means the candidate is better.)

**Era stability** (`eras.csv`, ΔMSE vs matched M3):
- M3+S: 2013–16 +3.5%, 2017–19 +5.6%, 2020–22 **−6.4%**, 2023–26 +1.0%. The
  sign flips by era.
- M3+D: −0.0% and −1.8%.
- M3+S+D: −0.6% and −1.3%.

**Residual rankings.**
- M3+S shares 63 of its top-72 |residual| weeks with M3.
- M3+D and M3+S+D share 27 of 28 with the matched M3.
- The supply block would move 9 of the extreme weeks. That is about the same
  churn as v2's M4 (64/72), and it comes from a block that failed the gate.

**Robustness target** (`alt_target.csv`, R² vs its own B1):
- Full sample: M3 5.89%, M3+S 6.67%.
- D sample: M3 2.31%, M3+D 2.60%, M3+S+D 2.66%.
- The alt-target gains are small, and they are not tested by the gate (spec §2:
  the primary target is not swapped).

**Fitted associations** (`coefficients_descriptive.csv`, standardised ridge
coefficients, pp per SD, full-sample fit, α = 316):
- `s_settle_10s` −0.13, `s_pending_10s` −0.10, `s_announced_10s` +0.09,
  `d_ust_tot_ch4_z` +0.12. The rest are |coef| < 0.06.
- These are associations in a model that did not pass the gate. They do not show
  that supply or dealer inventory causes positioning changes.

## 3. Reading the results

1. **Supply (S).** The point estimate is a 1.1% MSE reduction, about R² +1 pp. It
   is not distinguishable from zero (p = 0.15, CI spans 0) and it reverses in
   2020–22. That is close to v2's M4 result (+1.0%, p = 0.095), which was also not
   adopted. It is not evidence that supply is irrelevant. Weekly gross settlement
   is a coarse measure, and net issuance, the maturity mix within the 10y sector
   and the CTD were not modelled.
2. **Dealer inventory (D).** It is slightly worse than the matched M3 on 280
   weeks. It is also tested on a short, recent sample with only two eras, the
   fortnight release lag, and no financing data. A weak result here does not
   show that dealer balance sheets are unrelated to leveraged-fund positioning.
3. **The matched M3 does better on recent weeks when trained only on 2016+**
   (R² 9.05% vs 7.39% for v2.0 as fitted). Its MZ slope of 1.95 says its
   predictions are too compressed. This is an observation on one sample, not a
   tested result. It hints that the expanding window may underweight recent
   behaviour. That is a separate question and is **not** acted on here: a window
   choice selected on these 280 weeks would be fitted to them.
4. **Nothing here identifies private information or basis quantities.** A
   residual is the part of this week's change the model's features did not
   capture. That includes unmodelled public information, noise, and features
   that were never tried.

## 4. Genuine basis data (investigation, not fitted)

| candidate | what it is | downloadable? | usable here? |
|---|---|---|---|
| Fed FEDS Note, "Quantifying Treasury cash-futures basis trades" (Glicoes et al., 2024), Fig. 1 | option-adjusted cash–futures basis, net of carry, active 2/5/10y contracts, annualised return, 20-day MA, 2017–2023 | **No** data files or download links on the note or its accessible-data page. The source is J.P. Morgan Markets (proprietary), and the sign convention is not stated | no: ends 2023, not maintained, convention undocumented |
| Same note, Figs. 3–6 | Form PF hedge-fund Treasury and repo positions; TRACE proxy | no files; Form PF is confidential microdata | no |
| OFR Hedge Fund Monitor API (`data.financialresearch.gov/hf/v1`) | Form PF aggregates, FICC sponsored repo, CFTC TFF | yes (monthly or quarterly aggregates) | not a basis; monthly or quarterly with publication lags; could be a low-frequency control (untested) |
| OFR short-term funding API (`data.financialresearch.gov/v1`) | repo rates and volumes (DVP, GCF, tri-party), NY Fed reference rates | yes | gives the **financing** leg only. An implied repo rate also needs CTD prices, conversion factors, futures prices and delivery-option value |
| CME implied repo / CTD analytics | implied repo by contract | commercial | no |

Missing for a genuine net basis: daily CTD identity and cash price, conversion
factors per deliverable, matched futures settlement, term repo to delivery, and a
delivery-option valuation. Event-window figures in papers are **not**
extrapolated into a series. The v2 feature `futures_yield_residual` (formerly
mislabelled `futures_cash_spread`) is a return residual. It is not a basis.

## 5. Recommendation

**Retain M3 (v2.0).** No v3 block passed the pre-specified gate, which is the same
gate as v2. The v2 gate outcome stays disclosed (M4: p = 0.095, CI includes 0, not
adopted). No stimuli, model card or LLM dataset were regenerated.

## 6. Not tested

- Net issuance (maturities, buybacks), within-sector maturity mix, CTD-specific
  supply.
- Dealer financing (repo / reverse repo), because of the placeholders.
  Maturity-bucket fails, because those series are sparse (`PDST10F-TD` is about
  50% `*`).
- Any genuine basis or implied-repo measure (§4).
- OFR Form PF / sponsored-repo aggregates (monthly or quarterly; would need
  release-date alignment).
- Window choice (expanding vs recent-weighted) for recent weeks (§3.3).
- Definitional breaks that do not produce a level jump.

## 7. Team decisions

1. Accept "retain M3" for the stimuli, or decide to investigate the window
   question (a new, separately specified experiment).
2. Whether the supply block's sign pattern is worth a pre-registered follow-up
   on fresh weeks. The 7 post-cutoff CFTC weeks are too few on their own.
