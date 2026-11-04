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
    """Value of a daily series at the last observation on or before each snapshot.

    The forward fill runs over VALUES before the reindex, not only over missing
    dates. The distinction matters: the FRED frame is a union index over every
    series, so a weekly series such as the Fed balance sheet has a row for every
    weekday with NaN in all but one. `reindex(method="ffill")` fills absent labels
    only, so it would return NaN for almost every snapshot -- silently, as an
    all-empty feature column. A market holiday on a snapshot day does the same to a
    daily series.
    """
    return daily.sort_index().ffill().reindex(snapshots, method="ffill")


def between(daily: pd.Series, snapshots: pd.DatetimeIndex, func) -> pd.Series:
    """Apply `func` to the daily observations in each (previous, current] window."""
    daily = daily.sort_index()
    out = {}
    for prev, cur in zip(snapshots[:-1], snapshots[1:]):
        chunk = daily.loc[(daily.index > prev) & (daily.index <= cur)]
        out[cur] = func(chunk) if len(chunk) else float("nan")
    return pd.Series(out).reindex(snapshots)
