"""FRED series (issue #5).

Note MOVE is ICE-proprietary and is NOT on FRED; use realized vol from futures
returns instead. Watch release-date vs reference-date alignment on macro series --
CPI for reference month M is not public until well into M+1."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def load(series_ids: list[str], start: str | None = None) -> pd.DataFrame:
    """Daily frame, one column per FRED series id."""
    raise NotImplementedError("issue #5: FRED ingest")
