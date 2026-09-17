"""Release-timing guards (issue #6).

The information and tradable windows must never be interchangeable.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from hfpos.timing import release_date, window

TUE = date(2026, 9, 15)  # a Tuesday


def test_release_is_the_following_friday():
    assert release_date(TUE) == date(2026, 9, 18)
    assert release_date(TUE).weekday() == 4


def test_non_tuesday_snapshot_is_rejected():
    with pytest.raises(ValueError):
        release_date(date(2026, 9, 16))


def test_information_window_starts_at_the_snapshot():
    start, end = window(TUE, 1, "information")
    assert start == TUE
    assert end == TUE + timedelta(weeks=1)


def test_tradable_window_starts_only_after_publication():
    start, _ = window(TUE, 1, "tradable")
    assert start >= release_date(TUE)


def test_tradable_never_starts_before_information():
    """The whole point: tradable concedes the release lag, information does not."""
    for h in (1, 2, 4):
        info_start, _ = window(TUE, h, "information")
        trad_start, _ = window(TUE, h, "tradable")
        assert trad_start > info_start


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
