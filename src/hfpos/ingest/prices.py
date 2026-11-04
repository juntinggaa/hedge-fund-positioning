"""Ingest 10-Year Treasury Note futures prices (issue #4).

Source is Yahoo's `ZN=F`, a stitched front-month series. Two consequences:

1. **The series has roll discontinuities.** A weekly return computed straight
   across a quarterly roll boundary mixes two different contracts and injects a
   jump that no trader experienced. We flag roll weeks with a dummy rather than
   back-adjusting, because back-adjusting needs the per-contract history that this
   source does not provide. The dummy is a feature in Stage 1 and the flagged weeks
   are reported in the robustness check, so the handling is visible rather than
   assumed away.

2. **It is a free redistribution of exchange data, not CME settlements.** We
   therefore cross-check it against an independent source: weekly ZN returns are
   compared with the duration-implied return from the FRED 10-year constant
   maturity yield. See `features.basis.futures_cash_spread`.

The fetch window ends at the pinned `vintage.end` so that re-running tomorrow does
not silently extend the sample.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from hfpos import config, manifest

log = logging.getLogger(__name__)

TICKER = "ZN=F"
NAME = "prices_zn"

#: Quarterly delivery months for CBOT Treasury futures (Mar/Jun/Sep/Dec). Liquidity
#: migrates to the next contract during the last week of the month BEFORE delivery.
DELIVERY_MONTHS = (3, 6, 9, 12)
ROLL_MONTHS = tuple((m - 1) or 12 for m in DELIVERY_MONTHS)  # (2, 5, 8, 11)


def cache_path() -> Path:
    return config.path("raw") / f"{NAME}.parquet"


def fetch(start: str, end: str) -> pd.DataFrame:
    """Daily OHLCV for the front-month contract."""
    import yfinance as yf

    raw = yf.download(
        TICKER, start=start, end=end, interval="1d", auto_adjust=False, progress=False
    )
    if raw.empty:
        raise RuntimeError(f"no price data returned for {TICKER}")
    if isinstance(raw.columns, pd.MultiIndex):  # single-ticker downloads still nest
        raw.columns = raw.columns.get_level_values(0)
    frame = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    frame.columns = [c.lower() for c in frame.columns]
    frame.index = pd.to_datetime(frame.index).tz_localize(None).normalize()
    frame.index.name = "date"
    return frame.sort_index().dropna(subset=["close"])


def is_roll_week(day: pd.Timestamp) -> bool:
    """True if `day` falls in the week liquidity rolls to the next contract.

    CBOT first notice day is the last business day of the month preceding the
    delivery month, and the volume roll runs ahead of it. We mark the final seven
    days of February, May, August and November.
    """
    if day.month not in ROLL_MONTHS:
        return False
    month_end = day + pd.offsets.MonthEnd(0)
    return (month_end - day).days < 7


def load(refresh: bool = False) -> pd.DataFrame:
    """Return the cached daily price frame, downloading on first use."""
    path = cache_path()
    if path.exists() and not refresh:
        frame = pd.read_parquet(path)
        manifest.verify(NAME, frame)
        return frame

    cfg = config.load()
    frame = fetch(cfg["vintage"]["start"], cfg["vintage"]["end"])
    frame.to_parquet(path)
    manifest.write(NAME, frame, source=f"yahoo:{TICKER}", ticker=TICKER)
    return frame


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    frame = load(refresh=True)
    log.info("%s  %d rows  %s -> %s", TICKER, len(frame), frame.index[0].date(), frame.index[-1].date())


if __name__ == "__main__":
    main()
