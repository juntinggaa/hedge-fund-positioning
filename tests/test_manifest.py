"""Vintage pinning (issue #3).

A revision on CFTC's side would move the API and the archives together, so a
cross-source check cannot catch it. A recorded content hash can.
"""

from __future__ import annotations

import pandas as pd
import pytest

from hfpos import manifest


@pytest.fixture
def frame():
    idx = pd.DatetimeIndex(pd.to_datetime(["2026-09-01", "2026-09-08"]), name="as_of")
    return pd.DataFrame({"leveraged_funds_net": [-1_100_000, -1_150_000],
                         "open_interest": [4_000_000, 4_100_000]}, index=idx)


@pytest.fixture(autouse=True)
def isolated_manifest_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(manifest.config, "REPO_ROOT", tmp_path)


def test_write_then_read_round_trips(frame):
    written = manifest.write("demo", frame, source="test")
    assert manifest.read("demo") == written
    assert written["rows"] == 2
    assert written["first"] == "2026-09-01"
    assert written["last"] == "2026-09-08"


def test_extra_fields_are_recorded(frame):
    rec = manifest.write("demo", frame, source="test", contract_market_code="043602")
    assert rec["contract_market_code"] == "043602"


def test_verify_passes_on_unchanged_data(frame):
    manifest.write("demo", frame, source="test")
    assert manifest.verify("demo", frame)["rows"] == 2


def test_verify_detects_a_changed_value(frame):
    """The case a cross-source check cannot catch: CFTC revises one week."""
    manifest.write("demo", frame, source="test")
    revised = frame.copy()
    revised.iloc[0, 0] -= 5_000
    with pytest.raises(manifest.VintageMismatch, match="data has changed"):
        manifest.verify("demo", revised)


def test_verify_detects_appended_rows(frame):
    manifest.write("demo", frame, source="test")
    extra = pd.DataFrame({"leveraged_funds_net": [-1_200_000], "open_interest": [4_200_000]},
                         index=pd.DatetimeIndex(pd.to_datetime(["2026-09-15"]), name="as_of"))
    with pytest.raises(manifest.VintageMismatch):
        manifest.verify("demo", pd.concat([frame, extra]))


def test_unpinned_dataset_is_not_an_error(frame):
    assert manifest.verify("never_pinned", frame) == {}


def test_hash_is_stable_across_identical_frames(frame):
    assert manifest.content_hash(frame) == manifest.content_hash(frame.copy())
