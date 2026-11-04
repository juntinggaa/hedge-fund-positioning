"""v2 estimators (spec sections 3-4).

Audit fix A: the scaler sits INSIDE a pipeline that GridSearchCV refits on every
inner TimeSeriesSplit training fold, so no inner validation fold contributes to
the scaling it is evaluated under. Audit fix B: boosting without a random
early-stopping holdout.
"""

from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RIDGE_ALPHAS = np.logspace(-2, 4, 13)
FUSED_GAMMAS = np.logspace(-1, 3, 9)
INNER = TimeSeriesSplit(n_splits=4)


class FusedRidge(BaseEstimator, RegressorMixin):
    """Ridge with a first-difference smoothness penalty on ordered coefficients.

    Minimises ||y - a - Xb||^2 + gamma^2 * (sum (b_i - b_{i+1})^2 + b_{n-1}^2)
    (Boos & Grob 2023, eq. 7, uniform smoothing). The intercept is unpenalised.
    Solved as augmented least squares.
    """

    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma

    def fit(self, X, y):
        X, y = np.asarray(X, float), np.asarray(y, float)
        self.x_mean_, self.y_mean_ = X.mean(axis=0), y.mean()
        n = X.shape[1]
        D = np.zeros((n, n))
        D[np.arange(n - 1), np.arange(n - 1)] = 1.0
        D[np.arange(n - 1), np.arange(1, n)] = -1.0
        D[n - 1, n - 1] = 1.0
        A = np.vstack([X - self.x_mean_, self.gamma * D])
        b = np.concatenate([y - self.y_mean_, np.zeros(n)])
        self.coef_ = np.linalg.lstsq(A, b, rcond=None)[0]
        return self

    def predict(self, X):
        return self.y_mean_ + (np.asarray(X, float) - self.x_mean_) @ self.coef_


def make(name: str):
    if name == "ridge":
        pipe = Pipeline([("scale", StandardScaler()), ("est", Ridge())])
        return GridSearchCV(pipe, {"est__alpha": RIDGE_ALPHAS}, cv=INNER,
                            scoring="neg_mean_squared_error")
    if name == "fused":
        return GridSearchCV(FusedRidge(), {"gamma": FUSED_GAMMAS}, cv=INNER,
                            scoring="neg_mean_squared_error")
    if name == "ar1":
        return LinearRegression()
    if name == "gbm_fixed":
        return Pipeline([("scale", StandardScaler()), ("est", HistGradientBoostingRegressor(
            max_depth=3, max_iter=150, learning_rate=0.05, min_samples_leaf=20,
            l2_regularization=1.0, early_stopping=False, random_state=0))])
    raise ValueError(name)
