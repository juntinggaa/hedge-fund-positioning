"""Release-timing guards (issue #6).

The information and tradable windows must never be interchangeable.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from hfpos.timing import is_standard_as_of_day, release_date, window

TUE = date(2026, 9, 15)
MON = date(2026, 9, 14)
WED = date(2026, 9, 16)


def test_release_is_the_following_friday():
    assert release_date(TUE) == date(2026, 9, 18)


@pytest.mark.parametrize("as_of", [MON, TUE, WED])
def test_release_is_always_a_later_friday(as_of):
    """Holiday weeks shift the snapshot off Tuesday; publication stays Friday."""
    rel = release_date(as_of)
    assert rel.weekday() == 4
    assert rel > as_of


def test_holiday_shifted_snapshots_are_accepted_not_rejected():
    """14 of 1057 real 10Y snapshots fall on a Monday or Wednesday. Code that
    rejects them crashes on live data."""
    for as_of in (MON, WED):
        assert not is_standard_as_of_day(as_of)
        release_date(as_of)  # must not raise
    assert is_standard_as_of_day(TUE)


def test_weekend_snapshot_is_rejected():
    with pytest.raises(ValueError):
        release_date(date(2026, 9, 19))  # Saturday


def test_information_window_starts_at_the_snapshot():
    start, end = window(TUE, 1, "information")
    assert start == TUE
    assert end == TUE + timedelta(weeks=1)


def test_tradable_window_starts_only_after_publication():
    start, _ = window(TUE, 1, "tradable")
    assert start >= release_date(TUE)


def test_tradable_never_starts_before_information():
    """The point: tradable concedes the release lag, information does not."""
    for h in (1, 2, 4):
        info_start, _ = window(TUE, h, "information")
        trad_start, _ = window(TUE, h, "tradable")
        assert trad_start > info_start


def test_buffer_pushes_the_tradable_start_later():
    """A holiday can delay the actual release past the nominal Friday."""
    plain, _ = window(TUE, 1, "tradable", buffer_days=0)
    buffered, _ = window(TUE, 1, "tradable", buffer_days=3)
    assert buffered == plain + timedelta(days=3)


def test_buffer_is_ignored_for_information_timing():
    assert window(TUE, 1, "information", buffer_days=9)[0] == TUE


@pytest.mark.parametrize("h", [1, 2, 4])
def test_window_length_matches_horizon(h):
    for timing in ("information", "tradable"):
        start, end = window(TUE, h, timing)
        assert (end - start).days == 7 * h


def test_rejects_bad_inputs():
    with pytest.raises(ValueError):
        window(TUE, 0, "information")
    with pytest.raises(ValueError):
        window(TUE, 1, "whenever")
    with pytest.raises(ValueError):
        window(TUE, 1, "tradable", buffer_days=-1)
