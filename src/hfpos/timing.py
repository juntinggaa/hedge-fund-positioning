"""CFTC release timing.

TFF positions are measured at the close of a snapshot day and published later that
week. That gives two distinct, non-interchangeable return windows:

    information : starts at the snapshot. Answers "did the positioning contain
                  information?". NOT tradable -- nobody could act on it yet.
    tradable    : starts after publication. Answers "could anyone have used it?".
                  This is the economically meaningful one.

Mixing them is the easiest way to manufacture a look-ahead result, so windows are
always requested by name and every downstream result records which it used.

On snapshot days: the snapshot is *usually* Tuesday, but not always. In the live
10Y series (2006-06-13 to 2026-09-08) 14 of 1057 observations fall on a Monday or
Wednesday, all in holiday weeks. Code that assumes Tuesday will crash on real data.

On publication: the report normally goes out Friday afternoon. `release_date`
returns that Friday, which is the EARLIEST possible publication -- a holiday can
push the actual release later. For the tradable test, prefer a positive
`buffer_days` so the window cannot start before the data was genuinely public.

See issue #6.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Literal

Timing = Literal["information", "tradable"]

MONDAY, TUESDAY, FRIDAY = 0, 1, 4

#: Conservative default gap between the nominal Friday release and the start of a
#: tradable return window. Absorbs holiday-shifted releases.
DEFAULT_BUFFER_DAYS = 3


def is_standard_as_of_day(day: date) -> bool:
    """True if `day` is a Tuesday, the usual TFF snapshot day.

    Holiday weeks shift the snapshot. Use this to *count* shifted observations,
    never to reject them.
    """
    return day.weekday() == TUESDAY


def release_date(as_of: date) -> date:
    """Earliest possible publication date for a snapshot taken on `as_of`.

    Returns the first Friday strictly after `as_of`. Holidays can delay the actual
    release, so treat this as a lower bound and add `buffer_days` when the answer
    must be conservative.
    """
    if as_of.weekday() > FRIDAY:
        raise ValueError(f"{as_of} is a weekend; TFF snapshots are taken on business days")
    days_ahead = (FRIDAY - as_of.weekday()) % 7 or 7
    return as_of + timedelta(days=days_ahead)


def window(
    as_of: date,
    horizon_weeks: int,
    timing: Timing,
    buffer_days: int = DEFAULT_BUFFER_DAYS,
) -> tuple[date, date]:
    """Return (start, end) of the forward return window for one observation.

    The start is what separates the two questions: `information` measures from the
    snapshot itself, `tradable` only from the moment the data was public.
    `buffer_days` applies to `tradable` only and is ignored otherwise.
    """
    if horizon_weeks < 1:
        raise ValueError("horizon_weeks must be >= 1")
    if buffer_days < 0:
        raise ValueError("buffer_days must be >= 0")

    if timing == "information":
        start = as_of
    elif timing == "tradable":
        start = release_date(as_of) + timedelta(days=buffer_days)
    else:
        raise ValueError(f"unknown timing {timing!r}; expected 'information' or 'tradable'")
    return start, start + timedelta(weeks=horizon_weeks)
