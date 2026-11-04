"""Align daily market data to the CFTC snapshot grid.

Everything in the feature pipeline is measured between consecutive CFTC snapshots
rather than on a calendar week. That matters because 14 of the 1,057 snapshots are
not Tuesdays: a calendar-week grid would silently compare a 6-day positioning
change against a 7-day return.

`as_of` lookups take the last observation at or before the snapshot date, so a
market holiday never reaches forward for a value that did not exist yet.
"""

from __future__ import annotations

import pandas as pd


def as_of(daily: pd.Series | pd.DataFrame, snapshots: pd.DatetimeIndex) -> pd.Series | pd.DataFrame:
    """Value of a daily series at the last observation on or before each snapshot."""
    return daily.sort_index().reindex(snapshots, method="ffill")


def between(daily: pd.Series, snapshots: pd.DatetimeIndex, func) -> pd.Series:
    """Apply `func` to the daily observations in each (previous, current] window."""
    daily = daily.sort_index()
    out = {}
    for prev, cur in zip(snapshots[:-1], snapshots[1:]):
        chunk = daily.loc[(daily.index > prev) & (daily.index <= cur)]
        out[cur] = func(chunk) if len(chunk) else float("nan")
    return pd.Series(out).reindex(snapshots)
