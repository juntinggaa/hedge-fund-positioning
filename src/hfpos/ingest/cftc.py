"""Ingest CFTC Traders in Financial Futures, futures-only (issue #3).

Source is the CFTC public reporting Socrata endpoint rather than the annual zip
archives: same data, no unzip step, and it supports server-side filtering.

Two verified facts drive the design:

1. **Filter by contract code, never by name.** CFTC renamed the 10Y contract in
   February 2022 ("10-YEAR U.S. TREASURY NOTES" -> "UST 10Y NOTE"). A name filter
   silently returns 817 or 240 rows instead of 1057. Codes below were checked
   against the live endpoint on 2026-09-18.

2. **Snapshot days are not always Tuesday.** 14 of 1057 10Y observations fall on a
   Monday or Wednesday, all holiday weeks. Validation counts them; it does not
   reject them.

Set CFTC_APP_TOKEN to raise the anonymous rate limit (optional).
"""

from __future__ import annotations

import logging
import os
from datetime import date
from pathlib import Path
from typing import Any, Iterator

import pandas as pd
import requests

from hfpos import config, manifest
from hfpos.timing import is_standard_as_of_day

log = logging.getLogger(__name__)

DATASET = "gpe5-46if"  # Traders in Financial Futures, futures-only
BASE_URL = f"https://publicreporting.cftc.gov/resource/{DATASET}.json"
PAGE_SIZE = 5000
TIMEOUT = 60

DATE_COLUMN = "report_date_as_yyyy_mm_dd"
CODE_COLUMN = "cftc_contract_market_code"
OI_COLUMN = "open_interest_all"

#: group -> (long, short, spread) source columns
GROUP_COLUMNS: dict[str, tuple[str, str, str]] = {
    "dealer": (
        "dealer_positions_long_all",
        "dealer_positions_short_all",
        "dealer_positions_spread_all",
    ),
    "asset_manager": (
        "asset_mgr_positions_long",
        "asset_mgr_positions_short",
        "asset_mgr_positions_spread",
    ),
    "leveraged_funds": (
        "lev_money_positions_long",
        "lev_money_positions_short",
        "lev_money_positions_spread",
    ),
    "other_reportable": (
        "other_rept_positions_long",
        "other_rept_positions_short",
        "other_rept_positions_spread",
    ),
}

SELECT = [DATE_COLUMN, OI_COLUMN] + [c for cols in GROUP_COLUMNS.values() for c in cols]


class ContractNotConfigured(KeyError):
    """Raised when a contract alias has no verified code in config.yaml."""


def contract_code(contract: str) -> str:
    """Resolve an alias such as ``UST_10Y`` to its CFTC contract market code."""
    codes = config.load()["cftc"]["contracts"]
    try:
        code = codes[contract]
    except KeyError as exc:
        raise ContractNotConfigured(
            f"{contract!r} not in config.yaml cftc.contracts (have: {sorted(codes)})"
        ) from exc
    if not str(code).strip() or str(code).startswith("VERIFY"):
        raise ContractNotConfigured(
            f"{contract!r} has placeholder code {code!r}; verify it against the "
            "CFTC report header before use (issue #3)"
        )
    return str(code)


def _paged(params: dict[str, Any], headers: dict[str, str]) -> Iterator[list[dict]]:
    offset = 0
    while True:
        page = dict(params, **{"$limit": PAGE_SIZE, "$offset": offset})
        resp = requests.get(BASE_URL, params=page, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        rows = resp.json()
        if not rows:
            return
        yield rows
        if len(rows) < PAGE_SIZE:
            return
        offset += PAGE_SIZE


def fetch_records(code: str, start: str | None = None) -> list[dict]:
    """Download every futures-only TFF row for one contract code."""
    where = f"{CODE_COLUMN}='{code}'"
    if start:
        where += f" AND {DATE_COLUMN} >= '{start}T00:00:00.000'"
    params = {"$select": ",".join(SELECT), "$where": where, "$order": DATE_COLUMN}

    headers = {}
    if token := os.environ.get("CFTC_APP_TOKEN"):
        headers["X-App-Token"] = token

    records: list[dict] = []
    for page in _paged(params, headers):
        records.extend(page)
    log.info("fetched %d rows for contract %s", len(records), code)
    return records


def to_frame(records: list[dict]) -> pd.DataFrame:
    """Shape raw Socrata records into the weekly position panel.

    Pure function -- no network -- so it can be tested against a fixture.
    Emits ``{group}_long/short/spread/net`` for each group plus ``open_interest``,
    indexed by the snapshot date.
    """
    if not records:
        raise ValueError("no records to shape; check the contract code and date filter")

    raw = pd.DataFrame.from_records(records)
    missing = (set(SELECT) - set(raw.columns)) - {DATE_COLUMN}
    if missing:
        raise ValueError(f"response is missing expected columns: {sorted(missing)}")

    out = pd.DataFrame(index=pd.to_datetime(raw[DATE_COLUMN]).dt.normalize())
    out.index.name = "as_of"

    for group, (long_col, short_col, spread_col) in GROUP_COLUMNS.items():
        long_ = pd.to_numeric(raw[long_col], errors="coerce").to_numpy()
        short = pd.to_numeric(raw[short_col], errors="coerce").to_numpy()
        spread = pd.to_numeric(raw[spread_col], errors="coerce").to_numpy()
        out[f"{group}_long"] = long_
        out[f"{group}_short"] = short
        out[f"{group}_spread"] = spread
        out[f"{group}_net"] = long_ - short

    out["open_interest"] = pd.to_numeric(raw[OI_COLUMN], errors="coerce").to_numpy()
    return out.sort_index()


def validate(frame: pd.DataFrame) -> dict[str, Any]:
    """Check structural invariants; return diagnostics worth printing.

    Raises on anything that would corrupt the analysis. Holiday-shifted snapshot
    days and irregular gaps are reported, not rejected -- they are real features
    of the data.
    """
    if frame.empty:
        raise ValueError("empty frame")
    if not frame.index.is_monotonic_increasing:
        raise ValueError("index is not sorted")
    if frame.index.has_duplicates:
        dupes = frame.index[frame.index.duplicated()].tolist()
        raise ValueError(f"duplicate snapshot dates: {dupes[:5]}")
    if frame.isna().any().any():
        cols = frame.columns[frame.isna().any()].tolist()
        raise ValueError(f"missing values in {cols}")

    position_cols = [c for c in frame.columns if c.endswith(("_long", "_short", "_spread"))]
    if (frame[position_cols] < 0).any().any():
        raise ValueError("negative gross positions")
    if (frame["open_interest"] <= 0).any():
        raise ValueError("non-positive open interest")

    for group in GROUP_COLUMNS:
        recomputed = frame[f"{group}_long"] - frame[f"{group}_short"]
        if not recomputed.equals(frame[f"{group}_net"]):
            raise ValueError(f"{group}_net is not long minus short")

    days = frame.index.to_series().diff().dt.days.dropna()
    shifted = [d.date() for d in frame.index if not is_standard_as_of_day(d.date())]
    return {
        "rows": len(frame),
        "first": frame.index[0].date(),
        "last": frame.index[-1].date(),
        "non_tuesday_snapshots": len(shifted),
        "non_tuesday_dates": shifted,
        "irregular_gaps": int((days != 7).sum()),
    }


def cache_path(contract: str) -> Path:
    return config.path("raw") / f"cftc_tff_{contract.lower()}.parquet"


def load(contract: str, refresh: bool = False, start: str | None = None) -> pd.DataFrame:
    """Return the weekly position panel, downloading and caching on first use.

    Cached reads are checked against the pinned manifest, so a changed vintage
    surfaces as an error rather than silently shifting your results.
    """
    path = cache_path(contract)
    name = f"cftc_tff_{contract.lower()}"

    if path.exists() and not refresh:
        frame = pd.read_parquet(path)
        manifest.verify(name, frame)
        return frame

    start = start or config.load()["cftc"].get("start")
    code = contract_code(contract)
    frame = to_frame(fetch_records(code, start=start))
    diagnostics = validate(frame)
    frame.to_parquet(path)
    manifest.write(
        name,
        frame,
        source=f"cftc-socrata:{DATASET}",
        contract=contract,
        contract_market_code=code,
        non_tuesday_snapshots=diagnostics["non_tuesday_snapshots"],
        irregular_gaps=diagnostics["irregular_gaps"],
    )
    return frame


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for contract in config.load()["cftc"]["contracts"]:
        try:
            frame = load(contract, refresh=True)
        except ContractNotConfigured as exc:
            log.warning("skipping %s: %s", contract, exc)
            continue
        diag = validate(frame)
        log.info(
            "%-8s %4d rows  %s -> %s  | non-Tuesday: %d  irregular gaps: %d",
            contract,
            diag["rows"],
            diag["first"],
            diag["last"],
            diag["non_tuesday_snapshots"],
            diag["irregular_gaps"],
        )


if __name__ == "__main__":
    main()
