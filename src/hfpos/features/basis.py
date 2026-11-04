"""Conditions favouring the cash-futures basis trade (issue #7).

**This module does not measure the basis trade.** It measures conditions under
which the trade is attractive, which is a weaker thing, and the write-up must not
upgrade it. The cash leg is not in the CFTC dataset at all, so no feature built
here can tell you what fraction of a futures short is arbitrage. That limit is the
premise of the whole project.

Two features, each with a named construction.

1. `futures_cash_spread` -- MISNAMED; model v2 renames it `futures_yield_residual`.
   It is the part of the weekly ZN=F futures RETURN not explained by the change in
   the 10-year constant-maturity yield, using an expanding-window empirical duration
   (data strictly before the observation). It is NOT a cash-futures valuation basis
   and not an expected arbitrage return: it mixes CTD switches, roll effects,
   convexity, the CMT curve-fitting error and the 3pm-vs-close timing mismatch.
   Correction (2026-11-05): an earlier version of this docstring said a negative
   residual means futures cheapened and so "pulls basis traders in". That has the
   direction backwards. The long-cash / short-futures basis trade pays when futures
   are RICH relative to cash (positive net basis; Glicoes et al. 2024), and in any
   case a return residual measures a change, not the level of the basis. A genuine
   basis needs CTD prices, conversion factors and term repo, which we lack. The
   numbers are unchanged; only the interpretation is corrected.

2. `funding_spread` -- a funding-stress ladder, because no single spread spans
   2006-2026:

       rung 1  SOFR - IORB    from 2021-07-29   (the textbook measure)
       rung 2  SOFR - DFF     from 2018-04-03
       rung 3  DFF  - DTB3    before 2018       (bill richness / collateral scarcity)

   The three rungs are not on a common scale, so splicing their raw levels would
   inject a step change at each handover and the model would learn the handover.
   Each rung is standardised WITHIN ITS OWN ERA before splicing, making the feature
   "funding stress relative to this regime". The standardisation is EXPANDING --
   mean and standard deviation of that rung's own history up to each date -- because
   a full-era mean would put information from the end of the era into features at
   the start of it. `funding_rung` records which rung produced each observation so
   results can be split by era.

Known limitation, stated once here and carried into the report: the preferred rung
of the original plan -- cheapest-to-deliver implied repo against general collateral
-- needs the deliverable basket and conversion factors, which we do not have. The
basis trade was also small before roughly 2015. "Conditions favouring basis
trading" therefore does not mean the same thing in 2008 as in 2024.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from hfpos.features.align import as_of

MIN_DURATION_OBS = 52
MIN_STANDARDISE_OBS = 26

RUNGS = (
    ("sofr_iorb", ("SOFR", "IORB")),
    ("sofr_dff", ("SOFR", "DFF")),
    ("dff_dtb3", ("DFF", "DTB3")),
)


def empirical_duration(returns: pd.Series, yield_change: pd.Series) -> pd.Series:
    """Expanding-window slope of futures returns on yield changes.

    Fitted on observations strictly before each date, so the duration used at time
    t could have been known at time t. Returns NaN until `MIN_DURATION_OBS` pairs
    are available.
    """
    pairs = pd.concat([returns, yield_change], axis=1).dropna()
    betas = pd.Series(index=returns.index, dtype=float)
    for i in range(MIN_DURATION_OBS, len(pairs)):
        past = pairs.iloc[:i]
        x, y = past.iloc[:, 1].to_numpy(), past.iloc[:, 0].to_numpy()
        var = float(((x - x.mean()) ** 2).sum())
        if var > 0:
            betas.loc[pairs.index[i]] = float(((x - x.mean()) * (y - y.mean())).sum() / var)
    return betas


def futures_cash_spread(returns: pd.Series, yield_change: pd.Series) -> pd.DataFrame:
    """Futures return unexplained by the contemporaneous cash yield move."""
    beta = empirical_duration(returns, yield_change)
    implied = beta * yield_change
    spread = returns - implied
    return pd.DataFrame(
        {
            "futures_cash_spread": spread,
            "futures_cash_spread_13w": spread.rolling(13).sum(),
            "empirical_duration": beta,
        }
    )


def funding_spread(fred: pd.DataFrame, snapshots: pd.DatetimeIndex) -> pd.DataFrame:
    """Era-standardised funding-stress ladder, plus the rung used at each date."""
    levels = as_of(fred, snapshots)

    spread = pd.Series(index=snapshots, dtype=float)
    rung_id = pd.Series(index=snapshots, dtype=float)
    for number, (name, (high, low)) in enumerate(RUNGS, start=1):
        if high not in levels or low not in levels:
            continue
        candidate = levels[high] - levels[low]
        fillable = spread.isna() & candidate.notna()
        if not fillable.any():
            continue
        era = candidate[fillable]
        mean = era.expanding(MIN_STANDARDISE_OBS).mean()
        sigma = era.expanding(MIN_STANDARDISE_OBS).std()
        spread.loc[fillable] = (era - mean) / sigma
        rung_id.loc[fillable] = float(number)

    return pd.DataFrame({"funding_spread": spread, "funding_rung": rung_id})


def build(
    prices_returns: pd.Series,
    fred: pd.DataFrame,
    snapshots: pd.DatetimeIndex,
    yield_change: pd.Series,
) -> pd.DataFrame:
    """All basis-condition features on the snapshot grid."""
    return pd.concat(
        [futures_cash_spread(prices_returns, yield_change), funding_spread(fred, snapshots)],
        axis=1,
    )
