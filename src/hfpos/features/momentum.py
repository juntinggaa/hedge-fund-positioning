"""Price-based features: lagged returns 1/4/12w, realized volatility (issue #9).

Stage 0 exists to establish whether positions lead or lag returns. If they lag,
these features are load-bearing: omit them and the 'surprise' is just momentum."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def build(prices: pd.DataFrame) -> pd.DataFrame:
    """Weekly momentum and realized-vol features."""
    raise NotImplementedError("issue #9: momentum features")
