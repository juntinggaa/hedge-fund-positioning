"""Stage-1 estimators: Ridge, Lasso, gradient boosting (issue #11).

Target is d(Net/OI). Every model reports out-of-sample R-squared. With ~900
observations and 26 features the linear models may win; that is a finding about
the data, not a failure, and it goes in the report.

Two rules enforced here rather than trusted to discipline:

1. **The scaler is fitted on the training fold only.** Fitting it on the full
   sample is the most common silent leak in applied work: it puts the test fold's
   mean and variance into the training representation.
2. **Hyperparameters are tuned inside the training fold**, on a time-series split,
   never on the test block.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RIDGE_ALPHAS = np.logspace(-3, 4, 40)
LASSO_ALPHAS = np.logspace(-6, 0, 40)
INNER_SPLITS = 4

MODELS = ("ridge", "lasso", "gbm")


def make_estimator(model: str, seed: int):
    """Return an unfitted pipeline for `model`."""
    inner = TimeSeriesSplit(n_splits=INNER_SPLITS)
    if model == "ridge":
        return Pipeline(
            [("scale", StandardScaler()), ("est", RidgeCV(alphas=RIDGE_ALPHAS, cv=inner))]
        )
    if model == "lasso":
        return Pipeline(
            [
                ("scale", StandardScaler()),
                ("est", LassoCV(alphas=LASSO_ALPHAS, cv=inner, max_iter=20000, random_state=seed)),
            ]
        )
    if model == "gbm":
        # Shallow and heavily regularised: ~900 observations is not much data, and
        # an unconstrained booster will memorise the training window.
        return Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "est",
                    HistGradientBoostingRegressor(
                        max_depth=3,
                        max_iter=300,
                        learning_rate=0.05,
                        min_samples_leaf=20,
                        l2_regularization=1.0,
                        early_stopping=True,
                        validation_fraction=0.2,
                        random_state=seed,
                    ),
                ),
            ]
        )
    raise ValueError(f"unknown model {model!r}; expected one of {MODELS}")


def fit_predict(X_train, y_train, X_test, model: str, seed: int) -> np.ndarray:
    """Fit one model on a fold and return test-set predictions."""
    estimator = make_estimator(model, seed)
    estimator.fit(X_train, y_train)
    return estimator.predict(X_test)
