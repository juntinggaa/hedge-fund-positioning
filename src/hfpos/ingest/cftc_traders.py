"""Trader counts from CFTC TFF, plus a revision check against the pinned vintage.

Added for model v2 (docs/model_v2/SPEC_2026-11-05.md). Kept in its own files and
manifests so the pinned position panels from 2026-09-18 are never rewritten.

**Suppression.** The CFTC does not publish a trader count for a category with very
few reporting traders; the field arrives empty. Missing counts are kept as NaN and
never filled with zero: zero traders and "not disclosed" are different facts.

**Vintage.** Rows are capped at the last snapshot of the pinned position panel
(`cftc.load(contract).index[-1]`) so the v2 sample cannot silently extend past v1.

**Revisions.** `revision_check` refetches positions from the live endpoint and
compares them, cell by cell, with the pinned parquet. CFTC can revise a historical
week; a pinned hash detects a change on disk but not a change at the source.
"""

from __future__ import annotations

import logging
import os

import pandas as pd
import requests

from hfpos import config, manifest
from hfpos.ingest import cftc

log = logging.getLogger(__name__)

COUNT_COLUMNS = {
    "traders_tot_all": "traders_total",
    "traders_lev_money_long_all": "traders_lev_long",
    "traders_lev_money_short_all": "traders_lev_short",
    "traders_lev_money_spread": "traders_lev_spread",
    "traders_asset_mgr_long_all": "traders_am_long",
    "traders_asset_mgr_short_all": "traders_am_short",
}


def _fetch(code: str, select: list[str]) -> list[dict]:
    params = {
        "$select": ",".join([cftc.DATE_COLUMN] + select),
        "$where": f"{cftc.CODE_COLUMN}='{code}'",
        "$order": cftc.DATE_COLUMN,
    }
    headers = {"X-App-Token": t} if (t := os.environ.get("CFTC_APP_TOKEN")) else {}
    rows: list[dict] = []
    for page in cftc._paged(params, headers):
        rows.extend(page)
    return rows


def to_frame(records: list[dict], last: pd.Timestamp) -> pd.DataFrame:
    """Shape raw records into a count panel; empty strings and absent keys -> NaN."""
    raw = pd.DataFrame.from_records(records)
    out = pd.DataFrame(index=pd.to_datetime(raw[cftc.DATE_COLUMN]).dt.normalize())
    out.index.name = "as_of"
    for src, dst in COUNT_COLUMNS.items():
        col = raw[src] if src in raw else pd.Series(index=raw.index, dtype=object)
        out[dst] = pd.to_numeric(col, errors="coerce").to_numpy()
    out = out.sort_index()
    return out.loc[:last]


def cache_path(contract: str):
    return config.path("raw") / f"cftc_tff_traders_{contract.lower()}.parquet"


def load(contract: str, refresh: bool = False) -> pd.DataFrame:
    path = cache_path(contract)
    name = f"cftc_tff_traders_{contract.lower()}"
    if path.exists() and not refresh:
        frame = pd.read_parquet(path)
        manifest.verify(name, frame)
        return frame
    last = cftc.load(contract).index[-1]
    frame = to_frame(_fetch(cftc.contract_code(contract), list(COUNT_COLUMNS)), last)
    frame.to_parquet(path)
    manifest.write(name, frame, source=f"cftc-socrata:{cftc.DATASET}", contract=contract,
                   capped_at=str(last.date()),
                   suppressed_cells=int(frame.isna().sum().sum()))
    return frame


def revision_check(contract: str) -> dict:
    """Compare live positions with the pinned panel over the pinned date range."""
    pinned = cftc.load(contract)
    live = cftc.to_frame(cftc.fetch_records(cftc.contract_code(contract),
                                            start=str(pinned.index[0].date())))
    live = live.loc[pinned.index[0]:pinned.index[-1]]
    common = pinned.index.intersection(live.index)
    diff = (pinned.loc[common] != live.loc[common][pinned.columns])
    changed = diff.any(axis=1)
    return {
        "contract": contract,
        "pinned_rows": len(pinned), "live_rows_in_range": len(live),
        "missing_in_live": len(pinned.index.difference(live.index)),
        "extra_in_live": len(live.index.difference(pinned.index)),
        "weeks_revised": int(changed.sum()),
        "cells_revised": int(diff.to_numpy().sum()),
        "revised_weeks": [str(d.date()) for d in common[changed.to_numpy()]][:10],
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for contract in cftc_contracts():
        frame = load(contract, refresh=True)
        log.info("%s traders: %d rows, suppressed cells %d", contract, len(frame),
                 int(frame.isna().sum().sum()))
        log.info("revision check: %s", revision_check(contract))


def cftc_contracts() -> list[str]:
    return list(config.load()["cftc"]["contracts"])


if __name__ == "__main__":
    main()
