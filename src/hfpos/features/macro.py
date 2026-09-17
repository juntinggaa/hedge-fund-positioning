"""Rates, curve and macro state features (issue #9).

Yield levels and changes, 10Y-2Y slope, curvature, SOFR-IORB spread, VIX,
roll-week and FOMC-week dummies."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def build(fred: pd.DataFrame) -> pd.DataFrame:
    """Weekly macro-financial state features."""
    raise NotImplementedError("issue #9: macro features")
