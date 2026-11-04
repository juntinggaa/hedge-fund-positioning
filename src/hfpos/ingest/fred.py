"""Ingest macro-financial series from FRED (issue #5).

No API key is required for the series used here. Everything is daily or is
forward-filled to daily; weekly alignment happens later, in `features.build`,
against the CFTC snapshot dates rather than a calendar grid.

Coverage is uneven and that drives a design decision downstream:

    DGS2/5/10/30, DFF, VIXCLS, DTB3   full sample from 2006
    SOFR                              from 2018-04-03
    IORB                              from 2021-07-29

So the funding-spread feature cannot be SOFR-IORB across the sample. The ladder in
`features.basis` picks the best rung available in each era and records which one it
used, because "conditions favouring the basis trade" is not the same measurement in
2008 as in 2024 and the write-up has to say so.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from hfpos import config, manifest

log = logging.getLogger(__name__)

NAME = "fred"

#: Everything the feature pipeline may ask for, grouped as in config.yaml.
SERIES = ["DGS2", "DGS5", "DGS10", "DGS30", "DFF", "IORB", "SOFR", "DTB3", "VIXCLS", "T10Y2Y",
          "TREAST"]  # Fed Treasury securities held outright, weekly Wednesday level


def cache_path() -> Path:
    return config.path("raw") / f"{NAME}.parquet"


def fetch(series: list[str], start: str, end: str) -> pd.DataFrame:
    """Daily frame of FRED series, one column each, index-aligned on the union."""
    from pandas_datareader import data as pdr

    frames = []
    for code in series:
        got = pdr.DataReader(code, "fred", start, end)
        log.info("%-8s %5d obs  %s -> %s", code, len(got), got.index.min().date(), got.index.max().date())
        frames.append(got)
    frame = pd.concat(frames, axis=1).sort_index()
    frame.index = pd.to_datetime(frame.index).normalize()
    frame.index.name = "date"
    return frame


def load(refresh: bool = False) -> pd.DataFrame:
    """Return the cached FRED frame, downloading on first use."""
    path = cache_path()
    if path.exists() and not refresh:
        frame = pd.read_parquet(path)
        manifest.verify(NAME, frame)
        return frame

    cfg = config.load()
    frame = fetch(SERIES, cfg["vintage"]["start"], cfg["vintage"]["end"])
    frame.to_parquet(path)
    manifest.write(NAME, frame, source="fred", series=SERIES)
    return frame


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    frame = load(refresh=True)
    log.info("fred  %d rows  %s -> %s", len(frame), frame.index[0].date(), frame.index[-1].date())


if __name__ == "__main__":
    main()
