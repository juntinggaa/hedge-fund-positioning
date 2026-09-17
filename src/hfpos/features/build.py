"""Assemble the modelling frame (issue #9).

Joins positions, prices, basis, momentum and macro onto the TFF Tuesday grid and
writes data/processed. Everything reproducible from raw via 'make features'."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def build(contract: str) -> pd.DataFrame:
    """Full weekly feature matrix plus the Stage-1 target."""
    raise NotImplementedError("issue #9: feature assembly")
