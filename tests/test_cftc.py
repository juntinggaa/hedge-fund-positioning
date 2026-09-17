"""CFTC ingest guards (issue #3).

Shaping and validation are tested offline against synthetic records, so the suite
does not depend on the CFTC endpoint being up.
"""

from __future__ import annotations

import pandas as pd
import pytest

from hfpos.ingest import cftc


def record(day: str, **overrides) -> dict:
    """One Socrata row with plausible values."""
    row = {
        cftc.DATE_COLUMN: f"{day}T00:00:00.000",
        cftc.OI_COLUMN: "4000000",
        "dealer_positions_long_all": "500000",
        "dealer_positions_short_all": "300000",
        "dealer_positions_spread_all": "10000",
        "asset_mgr_positions_long": "1200000",
        "asset_mgr_positions_short": "200000",
        "asset_mgr_positions_spread": "20000",
        "lev_money_positions_long": "400000",
        "lev_money_positions_short": "1500000",
        "lev_money_positions_spread": "30000",
        "other_rept_positions_long": "100000",
        "other_rept_positions_short": "150000",
        "other_rept_positions_spread": "5000",
    }
    return row | {k: str(v) for k, v in overrides.items()}


@pytest.fixture
def frame():
    return cftc.to_frame([record("2026-09-01"), record("2026-09-08"), record("2026-09-15")])


def test_index_is_sorted_named_and_dated(frame):
    assert frame.index.name == "as_of"
    assert frame.index.is_monotonic_increasing
    assert isinstance(frame.index, pd.DatetimeIndex)


def test_net_is_long_minus_short(frame):
    assert (frame["leveraged_funds_net"] == 400000 - 1500000).all()
    assert (frame["asset_manager_net"] == 1200000 - 200000).all()


def test_leveraged_funds_are_net_short_and_asset_managers_net_long(frame):
    """The structural fact the whole project rests on."""
    assert (frame["leveraged_funds_net"] < 0).all()
    assert (frame["asset_manager_net"] > 0).all()


def test_all_groups_present(frame):
    for group in cftc.GROUP_COLUMNS:
        for leg in ("long", "short", "spread", "net"):
            assert f"{group}_{leg}" in frame.columns
    assert "open_interest" in frame.columns


def test_unsorted_input_is_sorted(frame):
    out = cftc.to_frame([record("2026-09-15"), record("2026-09-01")])
    assert out.index.is_monotonic_increasing


def test_empty_records_rejected():
    with pytest.raises(ValueError, match="no records"):
        cftc.to_frame([])


def test_missing_column_rejected():
    bad = record("2026-09-01")
    del bad["lev_money_positions_short"]
    with pytest.raises(ValueError, match="missing expected columns"):
        cftc.to_frame([bad])


def test_validate_accepts_clean_frame(frame):
    diag = cftc.validate(frame)
    assert diag["rows"] == 3
    assert diag["non_tuesday_snapshots"] == 0
    assert diag["irregular_gaps"] == 0


def test_validate_reports_holiday_shifted_snapshots_without_raising():
    """Real data has Monday snapshots in holiday weeks; they must not be dropped."""
    frame = cftc.to_frame([record("2026-09-08"), record("2026-09-14")])  # Tue, Mon
    diag = cftc.validate(frame)
    assert diag["non_tuesday_snapshots"] == 1
    assert diag["irregular_gaps"] == 1


def test_validate_rejects_duplicate_dates():
    frame = cftc.to_frame([record("2026-09-08"), record("2026-09-08")])
    with pytest.raises(ValueError, match="duplicate"):
        cftc.validate(frame)


def test_validate_rejects_negative_positions():
    frame = cftc.to_frame([record("2026-09-08", lev_money_positions_long=-1)])
    with pytest.raises(ValueError, match="negative gross positions"):
        cftc.validate(frame)


def test_validate_rejects_zero_open_interest():
    frame = cftc.to_frame([record("2026-09-08", open_interest_all=0)])
    with pytest.raises(ValueError, match="open interest"):
        cftc.validate(frame)


def test_validate_rejects_missing_values():
    frame = cftc.to_frame([record("2026-09-08", open_interest_all="")])
    with pytest.raises(ValueError, match="missing values"):
        cftc.validate(frame)


def test_contract_code_resolves_verified_aliases():
    assert cftc.contract_code("UST_10Y") == "043602"
    assert cftc.contract_code("UST_30Y") == "020601"


def test_unknown_contract_rejected():
    with pytest.raises(cftc.ContractNotConfigured):
        cftc.contract_code("GILT_10Y")


def test_placeholder_code_rejected(monkeypatch):
    """A VERIFY_ME placeholder must fail loudly, not fetch the wrong contract."""
    cfg = cftc.config.load()
    monkeypatch.setitem(cfg["cftc"]["contracts"], "UST_10Y", "VERIFY_ME")
    with pytest.raises(cftc.ContractNotConfigured, match="placeholder"):
        cftc.contract_code("UST_10Y")
