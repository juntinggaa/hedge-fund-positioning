"""Stage-2 predictive test (issues #14, #15).

r[t+h] = a + b*surprise[t] + c'X[t] + e[t+h]

Baseline X only vs augmented X + surprise, compared on out-of-sample R-squared
(Campbell-Thompson) and Clark-West for nested models -- NOT in-sample t-stats.

Runs all four definitions of 'unusual' through an identical pipeline: raw,
52-week z-score, Ridge residual, XGBoost residual. If the ML residuals do not beat
the z-score, the machine learning contributed nothing and the paper says so.

H1 is two-sided: unusual shorting preceding rising prices is crowded positioning
and forced unwinds, which is an equally real finding."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def run(frame: pd.DataFrame, horizon_weeks: int, timing: str, surprise: str) -> dict:
    """Baseline vs augmented comparison for one specification."""
    raise NotImplementedError("issue #14: Stage 2 primary test")
