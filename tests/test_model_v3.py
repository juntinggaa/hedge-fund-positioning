"""v3 tests: release timing, feature construction, source alignment, preservation."""

import hashlib
import json

import numpy as np
import pandas as pd
import pytest

from hfpos import config
from hfpos.model_v3 import features as f
from hfpos.model_v3 import sources

ROOT = config.REPO_ROOT


def _auction(term, ann, auc, iss, acc, offer=None, tips="No", frn="No", typ="Note"):
    return {"security_type": typ, "original_security_term": term, "security_term": term,
            "announcemt_date": pd.Timestamp(ann), "auction_date": pd.Timestamp(auc),
            "issue_date": pd.Timestamp(iss), "total_accepted": acc,
            "offering_amt": offer if offer is not None else acc,
            "inflation_index_security": tips, "floating_rate": frn}


SNAPS = pd.DatetimeIndex(["2025-01-07", "2025-01-14", "2025-01-21", "2025-01-28"])


def test_settlement_interval_is_prev_snapshot_exclusive_to_t_inclusive():
    a = pd.DataFrame([
        _auction("10-Year", "2025-01-02", "2025-01-08", "2025-01-14", 39.0),  # settles ON t=01-14
        _auction("7-Year", "2025-01-09", "2025-01-13", "2025-01-15", 10.0),   # settles 01-15 -> 01-21
    ])
    raw = f.supply_raw(SNAPS, a)
    assert raw.loc["2025-01-14", "settle_10s"] == 39.0
    assert raw.loc["2025-01-21", "settle_10s"] == 10.0
    assert raw["settle_10s"].sum() == 49.0          # nothing double counted


def test_no_auction_result_before_auction_date():
    a = pd.DataFrame([_auction("10-Year", "2025-01-09", "2025-01-15", "2025-01-22", 42.0, offer=40.0)])
    raw = f.supply_raw(SNAPS, a)
    # 01-14: announced, not auctioned -> only offering amount, never the result
    assert raw.loc["2025-01-14", "announced_10s"] == 40.0
    assert raw.loc["2025-01-14", "pending_10s"] == 0.0
    # 01-21: auctioned, not settled -> result
    assert raw.loc["2025-01-21", "pending_10s"] == 42.0
    assert raw.loc["2025-01-21", "announced_10s"] == 0.0
    assert raw.loc["2025-01-28", "settle_10s"] == 42.0


def test_tips_frn_excluded_and_holiday_week_interval():
    a = pd.DataFrame([
        _auction("10-Year", "2025-01-02", "2025-01-08", "2025-01-10", 20.0, tips="Yes"),
        _auction("2-Year", "2025-01-02", "2025-01-08", "2025-01-10", 30.0, frn="Yes"),
        _auction("5-Year", "2025-01-02", "2025-01-08", "2025-01-10", 50.0),
    ])
    snaps = pd.DatetimeIndex(["2025-01-07", "2025-01-15"])   # 8-day (holiday-shifted) gap
    raw = f.supply_raw(snaps, a)
    assert raw.loc["2025-01-15", "settle_10s"] == 0.0
    assert raw.loc["2025-01-15", "settle_dur_all"] == pytest.approx(50.0 * 0.53)


def test_term_parsing_and_duration_weight():
    assert f.term_years("5-Year 2-Month") == pytest.approx(5 + 2 / 12)
    assert f.dur_weight("10-Year") == 1.0
    assert f.dur_weight("4-Year") == pytest.approx((0.32 + 0.53) / 2)


def test_scaling_and_z_are_prior_only():
    x = pd.Series(np.arange(1.0, 400.0))
    y = x.copy(); y.iloc[-1] = 1e6
    assert f.prior_mean_scale(x).iloc[:-1].equals(f.prior_mean_scale(y).iloc[:-1])
    # the baseline at the last point does not include that point
    base = x.iloc[-53:-1].mean()
    assert f.prior_mean_scale(y).iloc[-1] == pytest.approx(np.log1p(1e6 / base))
    assert f.prior_z(x).iloc[:-1].equals(f.prior_z(y).iloc[:-1])


def test_pd_release_rule_tuesday_uses_wednesday_13_days_earlier():
    asof = pd.date_range("2024-01-03", periods=10, freq="W-WED")
    pdw = pd.DataFrame({"v": np.arange(10.0)}, index=asof)
    t = pd.Timestamp("2024-02-27")                      # Tuesday
    got = f.pd_available(pdw, pd.DatetimeIndex([t]))
    assert got["pd_asof"].iloc[0] == t - pd.Timedelta(days=13)
    assert (got["pd_asof"] + pd.Timedelta(days=f.PD_RELEASE_LAG_DAYS) <= t).all()


def test_dealer_features_ignore_values_not_yet_released():
    asof = pd.date_range("2016-01-06", periods=300, freq="W-WED")
    rng = np.random.default_rng(0)
    cols = ["PDPOSGSC-G7L11", "PDPOSGST-TOT", "PDFTD-USTET", "PDFTR-USTET"]
    pdw = pd.DataFrame(rng.normal(100, 10, (300, 4)).cumsum(0) + 5000, index=asof, columns=cols)
    t = pd.DatetimeIndex([asof[250] + pd.Timedelta(days=6)])   # the Tuesday after asof[250]
    base = f.dealer_block(t, pdw)
    bumped = pdw.copy(); bumped.iloc[250:] *= 3                # releases after t's cutoff change
    cutoff = t[0] - pd.Timedelta(days=f.PD_RELEASE_LAG_DAYS)
    assert bumped.index[250] > cutoff and bumped.index[249] <= cutoff
    pd.testing.assert_frame_equal(base, f.dealer_block(t, bumped))


def test_placeholders_become_nan_and_are_not_filled(tmp_path, monkeypatch):
    raw = pd.DataFrame({"asofdate": ["2024-01-03", "2024-01-10", "2024-01-17"],
                        "keyid": ["K"] * 3, "value": ["1", "*", "3"]})
    raw.to_parquet(tmp_path / "nyfed_pd_weekly.parquet", index=False)
    monkeypatch.setattr(sources, "RAW", tmp_path)
    w = sources.load_pd()
    assert np.isnan(w.loc["2024-01-10", "K"]) and w["K"].notna().sum() == 2


pinned = pytest.mark.skipif(not (sources.RAW / "treasury_coupon_auctions.parquet").exists(),
                            reason="v3 raw files not fetched")


@pinned
def test_source_alignment_auction_dates_ordered():
    a = f.coupon_universe(sources.load_auctions())
    assert (a["announcemt_date"] <= a["auction_date"]).all()
    assert (a["auction_date"] < a["issue_date"]).all()
    past = a[a["auction_date"] <= "2026-09-08"]
    assert past["total_accepted"].notna().all()       # every in-sample auction has a result


@pinned
def test_source_alignment_pd_weekly_wednesdays_and_lag():
    pdw = sources.load_pd()
    assert (pdw.index.day_of_week == 2).all()
    snaps = pd.DatetimeIndex(pd.read_parquet(ROOT / "data/processed/model_v3/full_M3.parquet").index)
    d = f.dealer_block(snaps, pdw)
    ok = d["pd_asof"].notna()
    assert ((pd.Series(snaps[ok], index=snaps[ok]) - d.loc[ok, "pd_asof"]).dt.days >= f.PD_RELEASE_LAG_DAYS).all()


def test_v1_v2_outputs_preserved():
    rec = json.loads((ROOT / "docs/model_v3/preservation_before.json").read_text())["sha256"]
    changed = [p for p, h in rec.items()
               if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]
    assert changed == []
