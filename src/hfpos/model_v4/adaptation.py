"""Chronological ridge fits and calibration from earlier outer OOS predictions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

from hfpos.model_v2.estimators import RIDGE_ALPHAS


@dataclass(frozen=True)
class Scheme:
    name: str
    window: int | None = None
    half_life: float | None = None


SCHEMES = (
    Scheme("expanding"),
    Scheme("rolling_156", window=156),
    Scheme("rolling_260", window=260),
    Scheme("rolling_520", window=520),
    Scheme("weighted_104", half_life=104),
    Scheme("weighted_260", half_life=260),
)


def recency_weights(index: pd.DatetimeIndex, half_life: float) -> np.ndarray:
    """Calendar-time weights; recomputed and normalised independently per fit."""
    if half_life <= 0:
        raise ValueError("half_life must be positive")
    index = pd.DatetimeIndex(index)
    if not index.is_monotonic_increasing or index.has_duplicates or len(index) == 0:
        raise ValueError("training dates must be nonempty, unique, and ordered")
    age = np.asarray((index[-1] - index).days, dtype=float) / 7.0
    weights = np.exp2(-age / half_life)
    return weights / weights.mean()


class RecencyRidge(RegressorMixin, BaseEstimator):
    """A fold-local scaler and ridge with the same observation weights.

    Keeping the weighting inside fit prevents inner CV from using an outer
    fold's time origin or weight normalisation. Unweighted fits match M3.
    """

    def __init__(self, alpha: float = 1.0, half_life: float | None = None):
        self.alpha = alpha
        self.half_life = half_life

    def fit(self, X: pd.DataFrame, y):
        if not isinstance(X, pd.DataFrame) or not isinstance(X.index, pd.DatetimeIndex):
            raise TypeError("X must be a date-indexed DataFrame")
        if not X.index.is_monotonic_increasing or X.index.has_duplicates:
            raise ValueError("training dates must be unique and ordered")
        self.fit_start_, self.fit_end_ = X.index[0], X.index[-1]
        self.n_features_in_ = X.shape[1]
        weights = None if self.half_life is None else recency_weights(X.index, self.half_life)
        self.weights_ = np.ones(len(X)) if weights is None else weights
        self.effective_n_ = float(self.weights_.sum() ** 2 / (self.weights_ ** 2).sum())
        self.scaler_ = StandardScaler().fit(X.to_numpy(float), sample_weight=weights)
        scaled = self.scaler_.transform(X.to_numpy(float))
        self.ridge_ = Ridge(alpha=self.alpha).fit(scaled, np.asarray(y, float), sample_weight=weights)
        return self

    def predict(self, X):
        return self.ridge_.predict(self.scaler_.transform(np.asarray(X, float)))


def walk(
    data: pd.DataFrame, features: list[str], target: str, scheme: Scheme,
    min_train: int = 260, step: int = 13,
    alphas=RIDGE_ALPHAS, inner_splits: int = 4,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Outer test blocks never enter scaling, fitting, or alpha selection."""
    frame = data[features + [target]].dropna()
    if not frame.index.is_monotonic_increasing or frame.index.has_duplicates:
        raise ValueError("modelling dates must be unique and ordered")
    rows, fits = [], []
    for start in range(min_train, len(frame), step):
        lo = max(0, start - scheme.window) if scheme.window else 0
        train, test = frame.iloc[lo:start], frame.iloc[start:start + step]
        search = GridSearchCV(
            RecencyRidge(half_life=scheme.half_life), {"alpha": alphas},
            cv=TimeSeriesSplit(n_splits=inner_splits), scoring="neg_mean_squared_error",
            error_score="raise", n_jobs=1,
        ).fit(train[features], train[target])
        est = search.best_estimator_
        pred = search.predict(test[features])
        rows.append(pd.DataFrame({
            "actual": test[target], "pred": pred,
            "block_start": test.index[0], "train_end": train.index[-1],
        }, index=test.index))
        fits.append({
            "scheme": scheme.name, "block_start": test.index[0],
            "block_end": test.index[-1], "train_start": train.index[0],
            "train_end": train.index[-1], "n_train": len(train),
            "effective_n": est.effective_n_, "alpha": search.best_params_["alpha"],
            "inner_cv_mse": -float(search.best_score_),
        })
    if not rows:
        raise ValueError("not enough observations for an outer test block")
    return pd.concat(rows), pd.DataFrame(fits)


def calibrate(
    raw: pd.DataFrame, window: int = 104, min_prior: int = 52,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit affine calibration to earlier OUTER OOS pairs, fixed per test block.

    No in-sample fitted values or observations from the current block are used.
    Missing warm-up predictions are retained as NaN, never passed through as if
    calibration had been available.
    """
    if min_prior < 2 or window < min_prior:
        raise ValueError("need 2 <= min_prior <= window")
    if not raw.index.is_monotonic_increasing or raw.index.has_duplicates:
        raise ValueError("OOS dates must be unique and ordered")
    result = raw.copy()
    result["raw_pred"] = result["pred"]
    result["pred"] = np.nan
    logs = []
    for stamp, block in raw.groupby("block_start", sort=True):
        stamp = pd.Timestamp(stamp)
        past = raw.loc[raw.index < stamp, ["actual", "pred"]].dropna().tail(window)
        if len(past) < min_prior:
            continue
        x, y = past["pred"].to_numpy(float), past["actual"].to_numpy(float)
        xc = x - x.mean()
        ssx = float(xc @ xc)
        fallback = ssx <= np.finfo(float).eps * max(1.0, float(x @ x))
        slope = 1.0 if fallback else float(xc @ (y - y.mean()) / ssx)
        intercept = float(y.mean() - slope * x.mean())
        result.loc[block.index, "pred"] = intercept + slope * block["pred"]
        logs.append({
            "block_start": stamp, "block_end": block.index[-1],
            "calibration_start": past.index[0], "calibration_end": past.index[-1],
            "n_prior_oos": len(past), "intercept": intercept, "slope": slope,
            "fallback": bool(fallback),
        })
    return result, pd.DataFrame(logs)
