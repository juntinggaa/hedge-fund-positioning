"""Forecast comparison metrics (issue #14).

Campbell-Thompson out-of-sample R-squared and the Clark-West statistic for nested
model comparison. In-sample R-squared is not reported anywhere in this project."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def oos_r2(y_true: pd.Series, y_pred: pd.Series, y_bench: pd.Series) -> float:
    """Campbell-Thompson OOS R-squared against a benchmark forecast."""
    raise NotImplementedError("issue #14: OOS metrics")
