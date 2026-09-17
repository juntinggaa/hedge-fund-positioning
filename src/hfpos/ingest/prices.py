"""Treasury futures prices and the roll (issue #4).

ZN=F is a stitched front-month series with discontinuities at each quarterly roll.
Naive weekly returns across a roll boundary inject a spurious jump that will be
picked up as signal. Set prices.roll_method in config.yaml and document the choice."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def load(symbol: str, roll_method: str) -> pd.DataFrame:
    """Daily prices with a roll-consistent return column."""
    raise NotImplementedError("issue #4: price ingest + roll handling")
