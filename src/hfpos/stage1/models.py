"""Stage-1 estimators: Ridge, Lasso, XGBoost (issue #11).

Target is d(Net/OI), not raw net contracts -- open interest grows by an order of
magnitude across the sample. Report OOS R-squared for every model. With ~1000
observations and 20-40 features the linear model may win; that is a finding about
the data, not a failure, and it goes in the paper."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def fit_predict(X_train, y_train, X_test, model: str, seed: int):
    """Fit one model on a fold and return test-set predictions."""
    raise NotImplementedError("issue #11: Stage 1 models")
