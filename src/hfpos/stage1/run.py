"""Stage-1 walk-forward driver (issues #10, #11, #13).

Produces the positioning surprise and the two gate diagnostics:
  1. Stage-1 out-of-sample R-squared
  2. corr(residual, raw d(Net/OI))  -- above ~0.9 and the decomposition is cosmetic

Both belong in the main text. Scalers and hyperparameters are fitted per fold,
inside ExpandingWindowSplitter, never on the full sample."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def run(frame: pd.DataFrame, model: str) -> pd.DataFrame:
    """Out-of-sample predictions, residuals and gate diagnostics."""
    raise NotImplementedError("issue #11: Stage 1 walk-forward driver")
