"""Meaningful temporal and weighted-fitting checks for the adaptation experiment."""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from hfpos import config
from hfpos.model_v4.adaptation import RecencyRidge, Scheme, calibrate, recency_weights, walk


def frame(n=45):
    rng = np.random.default_rng(5)
    index = pd.date_range("2010-01-05", periods=n, freq="W-TUE")
    x = rng.normal(size=(n, 2))
    return pd.DataFrame({"x1": x[:, 0], "x2": x[:, 1],
                         "target": 0.5 * x[:, 0] - 0.3 * x[:, 1]
                                   + rng.normal(scale=0.1, size=n)}, index=index)


def test_calendar_half_life_and_weight_normalisation():
    dates = pd.DatetimeIndex(["2020-01-07", "2020-01-14", "2020-01-28"])
    w = recency_weights(dates, half_life=1)
    assert w.mean() == pytest.approx(1)
    assert w[0] / w[-1] == pytest.approx(1 / 8)
    assert w[1] / w[-1] == pytest.approx(1 / 4)
    with pytest.raises(ValueError):
        recency_weights(dates[::-1], 1)


def test_unweighted_estimator_matches_the_original_pipeline():
    d = frame()
    a = RecencyRidge(alpha=3).fit(d[["x1", "x2"]], d.target)
    b = Pipeline([("s", StandardScaler()), ("r", Ridge(alpha=3))]).fit(
        d[["x1", "x2"]].to_numpy(), d.target.to_numpy())
    np.testing.assert_allclose(a.predict(d[["x1", "x2"]]),
                               b.predict(d[["x1", "x2"]].to_numpy()), atol=1e-12)


def test_weighted_scaler_and_ridge_use_the_same_weights():
    d = frame()
    a = RecencyRidge(alpha=2, half_life=5).fit(d[["x1", "x2"]], d.target)
    w = recency_weights(d.index, 5)
    x = d[["x1", "x2"]].to_numpy()
    mean = np.average(x, axis=0, weights=w)
    sd = np.sqrt(np.average((x - mean) ** 2, axis=0, weights=w))
    np.testing.assert_allclose(a.scaler_.mean_, mean)
    expected = Ridge(alpha=2).fit((x - mean) / sd, d.target, sample_weight=w)
    np.testing.assert_allclose(a.predict(d[["x1", "x2"]]),
                               expected.predict((x - mean) / sd), atol=1e-12)


def test_inner_cv_recomputes_weights_inside_each_training_fold(monkeypatch):
    seen = []
    original = RecencyRidge.fit

    def record(self, X, y):
        out = original(self, X, y)
        seen.append((X.index.copy(), self.weights_.copy()))
        return out

    monkeypatch.setattr(RecencyRidge, "fit", record)
    d = frame(24)
    GridSearchCV(RecencyRidge(half_life=5), {"alpha": [1]},
                 cv=TimeSeriesSplit(3), scoring="neg_mean_squared_error").fit(
                     d[["x1", "x2"]], d.target)
    assert [len(dates) for dates, _ in seen] == [6, 12, 18, 24]
    for dates, w in seen:
        assert w.mean() == pytest.approx(1)
        assert w[0] / w[-1] == pytest.approx(2 ** (-(len(dates) - 1) / 5))


@pytest.mark.parametrize("scheme", [Scheme("expanding"), Scheme("rolling", window=12),
                                    Scheme("weighted", half_life=8)])
def test_outer_predictions_do_not_use_current_or_future_targets(scheme):
    d = frame()
    first, fits = walk(d, ["x1", "x2"], "target", scheme,
                       min_train=20, step=5, alphas=[0.1, 1], inner_splits=2)
    altered = d.copy()
    altered.loc[d.index[30]:, "target"] += 100
    second, _ = walk(altered, ["x1", "x2"], "target", scheme,
                      min_train=20, step=5, alphas=[0.1, 1], inner_splits=2)
    # The block starting at index 30 cannot use its own altered targets either.
    np.testing.assert_allclose(first.loc[:d.index[34], "pred"],
                               second.loc[:d.index[34], "pred"], atol=1e-12)
    assert (pd.to_datetime(fits.train_end) < pd.to_datetime(fits.block_start)).all()
    if scheme.window:
        assert (fits.n_train == scheme.window).all()


def raw_predictions(n=32, step=4):
    index = pd.date_range("2010-01-05", periods=n, freq="W-TUE")
    x = np.linspace(-0.02, 0.03, n)
    return pd.DataFrame({"actual": 0.01 + 2 * x, "pred": x,
                         "block_start": index[np.arange(n) // step * step]}, index=index)


def test_calibration_learns_only_earlier_oos_pairs_and_respects_warmup():
    raw = raw_predictions()
    got, log = calibrate(raw, window=12, min_prior=8)
    assert got.pred.iloc[:8].isna().all()
    np.testing.assert_allclose(got.pred.iloc[8:], raw.actual.iloc[8:], atol=1e-12)
    assert (log.calibration_end < log.block_start).all()
    assert log.n_prior_oos.min() == 8
    assert log.n_prior_oos.max() == 12


def test_calibration_does_not_learn_from_current_block_or_future_labels():
    raw = raw_predictions()
    base, log = calibrate(raw, window=12, min_prior=8)
    altered = raw.copy()
    altered.loc[raw.index[16]:, "actual"] += 1000
    changed, changed_log = calibrate(altered, window=12, min_prior=8)
    np.testing.assert_allclose(base.pred.iloc[:20], changed.pred.iloc[:20], equal_nan=True)
    pd.testing.assert_frame_equal(log[log.block_start <= raw.index[16]],
                                  changed_log[changed_log.block_start <= raw.index[16]])


def test_degenerate_calibration_is_recorded_and_uses_past_mean_error():
    raw = raw_predictions()
    raw["pred"] = 0.0
    got, logs = calibrate(raw, window=12, min_prior=8)
    assert logs.fallback.all()
    assert got.pred.iloc[8] == pytest.approx(raw.actual.iloc[:8].mean())


def test_preexisting_artifacts_and_user_changes_are_preserved():
    root = config.REPO_ROOT
    rec = json.loads((root / "docs/model_v4/preservation_before.json").read_text())["sha256"]
    altered = [p for p, h in rec.items()
               if not (root / p).exists()
               or hashlib.sha256((root / p).read_bytes()).hexdigest() != h]
    assert altered == []
