"""Price-based features on the CFTC snapshot grid (issue #9).

Stage 0 exists to establish whether positions lead or lag returns. If they lag,
these features are load-bearing: omit them and the Stage-1 "surprise" is just
momentum wearing a hat.

Returns are log returns of the front-month series between consecutive snapshots.
Roll weeks are flagged rather than adjusted away -- see `ingest.prices`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from hfpos.features.align import as_of, between
from hfpos.ingest.prices import is_roll_week

TRADING_DAYS = 252


def build(prices: pd.DataFrame, snapshots: pd.DatetimeIndex) -> pd.DataFrame:
    """Weekly momentum and realized-volatility features."""
    close = as_of(prices["close"], snapshots)
    daily_ret = np.log(prices["close"]).diff().dropna()

    out = pd.DataFrame(index=snapshots)
    log_close = np.log(close)
    for weeks in (1, 4, 12):
        out[f"ret_{weeks}w"] = log_close.diff(weeks)

    realized = between(daily_ret, snapshots, lambda c: float(c.std()))
    out["rvol_4w"] = realized.rolling(4).mean() * np.sqrt(TRADING_DAYS)
    out["rvol_12w"] = realized.rolling(12).mean() * np.sqrt(TRADING_DAYS)
    out["rvol_change"] = out["rvol_4w"] - out["rvol_12w"]

    out["roll_week"] = between(
        pd.Series(1.0, index=prices.index), snapshots,
        lambda c: float(any(is_roll_week(d) for d in c.index)),
    ).fillna(0.0)
    return out
