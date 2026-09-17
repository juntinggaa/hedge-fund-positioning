"""CFTC release timing.

TFF positions are measured at Tuesday close and published the following Friday
afternoon. That gives two distinct, non-interchangeable return windows:

    information : starts Tuesday close. Answers "did the positioning contain
                  information?". NOT tradable — nobody could act on it yet.
    tradable    : starts after the Friday release. Answers "could anyone have
                  used it?". This is the economically meaningful one.

Mixing them is the single easiest way to manufacture a look-ahead result, so the
window is always requested by name and every downstream test records which it used.
See issue #6.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Literal

Timing = Literal["information", "tradable"]

TUESDAY = 1  # date.weekday(): Monday == 0
_RELEASE_LAG_DAYS = 3  # Tuesday -> Friday


def is_as_of_day(day: date) -> bool:
    """TFF position snapshots are taken on Tuesdays."""
    return day.weekday() == TUESDAY


def release_date(as_of: date) -> date:
    """Publication date for a Tuesday snapshot.

    Returns the same week's Friday. Federal holidays push the release later;
    when a holiday calendar is wired in (issue #6) this must shift forward, never
    back. Treat the returned date as the *earliest* possible release.
    """
    if not is_as_of_day(as_of):
        raise ValueError(f"{as_of} is not a Tuesday; TFF snapshots are as of Tuesday close")
    return as_of + timedelta(days=_RELEASE_LAG_DAYS)


def window(as_of: date, horizon_weeks: int, timing: Timing) -> tuple[date, date]:
    """Return (start, end) of the forward return window for one observation.

    The start is what separates the two questions: `information` measures from the
    snapshot itself, `tradable` measures only from the moment the data was public.
    """
    if horizon_weeks < 1:
        raise ValueError("horizon_weeks must be >= 1")
    if timing == "information":
        start = as_of
    elif timing == "tradable":
        start = release_date(as_of)
    else:
        raise ValueError(f"unknown timing {timing!r}; expected 'information' or 'tradable'")
    return start, start + timedelta(weeks=horizon_weeks)
