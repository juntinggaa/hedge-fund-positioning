"""Cross-source reconciliation: Socrata API vs the official CFTC zip archives.

Skipped by default because it downloads tens of megabytes. Run deliberately:

    pytest -m network

This is the evidence behind the claim that the API is a faithful mirror of the
official publication. It is not evidence that CFTC's numbers are correct -- nothing
short of the confidential large-trader data could establish that.

Note the archives only go back to 2010, so this can never cover 2006-2009. That
gap is precisely why the API is the primary source.
"""

from __future__ import annotations

import pandas as pd
import pytest

from hfpos.ingest import cftc, cftc_archive

pytestmark = pytest.mark.network

CONTRACT = "UST_10Y"
YEARS = [2012, 2019, 2024, 2025]  # straddles the Feb 2022 rename and the header drift

COMPARED = [
    f"{group}_{leg}"
    for group in cftc.GROUP_COLUMNS
    for leg in ("long", "short", "spread", "net")
] + ["open_interest"]


@pytest.fixture(scope="module")
def api_frame():
    return cftc.load(CONTRACT)


@pytest.fixture(scope="module")
def archive_frame():
    return cftc_archive.load_years(cftc.contract_code(CONTRACT), YEARS)


def test_archive_before_2010_is_refused_not_silently_empty():
    """The archive series starts at 2010; asking for less must fail loudly."""
    with pytest.raises(cftc_archive.ArchiveYearUnavailable):
        cftc_archive.fetch_year(2009)


def test_schemas_match(api_frame, archive_frame):
    assert list(api_frame.columns) == list(archive_frame.columns)


def test_same_snapshot_dates(api_frame, archive_frame):
    overlap = api_frame.reindex(archive_frame.index)
    assert overlap.index.equals(archive_frame.index)
    assert not overlap.isna().any().any(), "API is missing weeks the archive has"


def test_every_value_matches(api_frame, archive_frame):
    """2,310 cells across four years reconciled to zero mismatches on 2026-09-18."""
    overlap = api_frame.reindex(archive_frame.index)
    mismatches = {
        col: int((overlap[col].to_numpy() != archive_frame[col].to_numpy()).sum())
        for col in COMPARED
    }
    assert sum(mismatches.values()) == 0, f"API and archive disagree: {mismatches}"


def test_rename_does_not_truncate_the_sample(api_frame):
    """CFTC renamed the contract in Feb 2022; filtering by code must span it."""
    assert (api_frame.index < pd.Timestamp("2022-02-08")).sum() > 800
    assert (api_frame.index >= pd.Timestamp("2022-02-08")).sum() > 200
