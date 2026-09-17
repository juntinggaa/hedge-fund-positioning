"""Fallback ingest from the CFTC annual zip archives (issue #3).

The API is the primary source. This exists so the project is not single-sourced:
if the endpoint changes, throttles, or disappears mid-project, the archives still
work, and they are also what a reviewer is most likely to reach for.

Two limitations, both verified on 2026-09-18 rather than assumed:

1. **Coverage starts at 2010.** `fut_fin_txt_2006..2009.zip` return 404 under this
   URL pattern, so the archive route cannot reproduce the full TFF history. Roughly
   the first 190 weeks of the sample are API-only. This is why the API is primary.

2. **The header drifts.** The report date column is `Report_Date_as_MM_DD_YYYY` in
   older files and `Report_Date_as_YYYY-MM-DD` from about 2019. Code that hardcodes
   either one breaks on half the sample.

Output is column-identical to `cftc.to_frame`, so the two sources are directly
comparable and interchangeable downstream.
"""

from __future__ import annotations

import io
import logging
import zipfile
from typing import Iterable

import pandas as pd
import requests

from hfpos.ingest.cftc import GROUP_COLUMNS

log = logging.getLogger(__name__)

ARCHIVE_URL = "https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"
MEMBER = "FinFutYY.txt"
TIMEOUT = 120

#: Earliest year available under ARCHIVE_URL. Earlier years 404.
FIRST_ARCHIVE_YEAR = 2010

CODE_COLUMN = "CFTC_Contract_Market_Code"
OI_COLUMN = "Open_Interest_All"

#: our column -> archive column. Archive uses the `_All` suffix on every group.
ARCHIVE_COLUMNS = {
    "dealer": ("Dealer_Positions_Long_All", "Dealer_Positions_Short_All",
               "Dealer_Positions_Spread_All"),
    "asset_manager": ("Asset_Mgr_Positions_Long_All", "Asset_Mgr_Positions_Short_All",
                      "Asset_Mgr_Positions_Spread_All"),
    "leveraged_funds": ("Lev_Money_Positions_Long_All", "Lev_Money_Positions_Short_All",
                        "Lev_Money_Positions_Spread_All"),
    "other_reportable": ("Other_Rept_Positions_Long_All", "Other_Rept_Positions_Short_All",
                         "Other_Rept_Positions_Spread_All"),
}


class ArchiveYearUnavailable(RuntimeError):
    """The requested year is not published under ARCHIVE_URL."""


def fetch_year(year: int) -> pd.DataFrame:
    """Download and parse one annual archive."""
    if year < FIRST_ARCHIVE_YEAR:
        raise ArchiveYearUnavailable(
            f"{year} predates the archive series (first available: {FIRST_ARCHIVE_YEAR}). "
            "Use the API source for the early sample."
        )
    resp = requests.get(ARCHIVE_URL.format(year=year), timeout=TIMEOUT)
    if resp.status_code == 404:
        raise ArchiveYearUnavailable(f"no archive published for {year}")
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        member = MEMBER if MEMBER in zf.namelist() else zf.namelist()[0]
        with zf.open(member) as fh:
            frame = pd.read_csv(fh, low_memory=False)

    frame.columns = [c.strip().strip('"') for c in frame.columns]
    return frame


def _date_column(frame: pd.DataFrame) -> str:
    """Find the report-date column, whichever spelling this vintage used."""
    for col in frame.columns:
        if col.startswith("Report_Date"):
            return col
    raise ValueError(f"no Report_Date column; header drifted again: {list(frame.columns)[:6]}")


def to_frame(raw: pd.DataFrame, code: str) -> pd.DataFrame:
    """Shape one archive year into the same schema as `cftc.to_frame`."""
    subset = raw[raw[CODE_COLUMN].astype(str).str.strip() == code]
    if subset.empty:
        raise ValueError(f"contract code {code!r} not present in this archive year")

    dates = pd.to_datetime(subset[_date_column(subset)], format="mixed").dt.normalize()
    out = pd.DataFrame(index=pd.DatetimeIndex(dates))
    out.index.name = "as_of"

    for group, (long_col, short_col, spread_col) in ARCHIVE_COLUMNS.items():
        long_ = pd.to_numeric(subset[long_col], errors="coerce").to_numpy()
        short = pd.to_numeric(subset[short_col], errors="coerce").to_numpy()
        out[f"{group}_long"] = long_
        out[f"{group}_short"] = short
        out[f"{group}_spread"] = pd.to_numeric(subset[spread_col], errors="coerce").to_numpy()
        out[f"{group}_net"] = long_ - short

    out["open_interest"] = pd.to_numeric(subset[OI_COLUMN], errors="coerce").to_numpy()

    # Column order must match the API path exactly so the two are comparable.
    ordered = [f"{g}_{leg}" for g in GROUP_COLUMNS for leg in ("long", "short", "spread", "net")]
    return out[ordered + ["open_interest"]].sort_index()


def load_years(code: str, years: Iterable[int]) -> pd.DataFrame:
    """Concatenate several archive years for one contract code."""
    frames = []
    for year in years:
        try:
            frames.append(to_frame(fetch_year(year), code))
        except ArchiveYearUnavailable as exc:
            log.warning("skipping %d: %s", year, exc)
    if not frames:
        raise ValueError("no archive years could be loaded")
    return pd.concat(frames).sort_index()
