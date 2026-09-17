"""Do positions lead or lag returns? (issue #8)

Cross-correlations and a small VAR, run BEFORE Stage 1. If positioning purely
follows returns, the Stage-1 feature set must include lagged returns."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def run(frame: pd.DataFrame) -> pd.DataFrame:
    """Lead-lag correlation table and VAR summary."""
    raise NotImplementedError("issue #8: Stage 0 lead-lag and VAR")
