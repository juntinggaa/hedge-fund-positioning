"""Walk-forward runner and evaluation metrics for v2 (spec section 5)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

MIN_TRAIN, STEP, ROLLING = 260, 13, 260


def walk(frame: pd.DataFrame, features: list[str], target: str, make_est,
         window: str = "expanding") -> pd.DataFrame:
    """Out-of-sample predictions. `make_est` returns a fresh unfitted estimator."""
    data = frame[features + [target]].dropna()
    X, y = data[features].to_numpy(float), data[target].to_numpy(float)
    pred, bench = np.full(len(y), np.nan), np.full(len(y), np.nan)
    for start in range(MIN_TRAIN, len(y), STEP):
        lo = max(0, start - ROLLING) if window == "rolling" else 0
        tr, te = slice(lo, start), slice(start, min(start + STEP, len(y)))
        est = make_est().fit(X[tr], y[tr])
        pred[te] = est.predict(X[te])
        bench[te] = y[tr].mean()
    out = pd.DataFrame({"actual": y, "pred": pred, "mean_bench": bench}, index=data.index)
    return out.dropna()


def benchmark_series(frame: pd.DataFrame, target: str, kind: str) -> pd.DataFrame:
    """B0 zero change and B1 expanding mean of all prior weeks."""
    y = frame[target].dropna()
    pred = pd.Series(0.0, index=y.index) if kind == "zero" else y.expanding().mean().shift(1)
    return pd.DataFrame({"actual": y, "pred": pred}).dropna()


def r2(actual, pred, bench) -> float:
    return float(1 - ((actual - pred) ** 2).sum() / ((actual - bench) ** 2).sum())


def metrics(actual: pd.Series, pred: pd.Series, mean_bench: pd.Series) -> dict:
    e = actual - pred
    mz = sm.OLS(actual.to_numpy(), sm.add_constant(pred.to_numpy())).fit()
    return {
        "n": len(actual),
        "r2_vs_mean": r2(actual, pred, mean_bench),
        "r2_vs_zero": r2(actual, pred, 0.0),
        "mae": float(e.abs().mean()),
        "rmse": float(np.sqrt((e ** 2).mean())),
        "bias": float(e.mean()),
        "pred_sd": float(pred.std()),
        "mz_intercept": float(mz.params[0]),
        "mz_slope": float(mz.params[1]) if len(mz.params) > 1 else float("nan"),
        "resid_ac1": float(e.autocorr(1)),
        "resid_ac2": float(e.autocorr(2)),
        "corr_resid_actual": float(e.corr(actual)),
        "sqrt_1_minus_r2": float(np.sqrt(max(0.0, 1 - r2(actual, pred, mean_bench)))),
    }


def hac_test(loss_diff: pd.Series, lags: int = 4) -> tuple[float, float]:
    """Mean loss differential (ref minus candidate), Newey-West t, one-sided p."""
    from scipy import stats
    d = loss_diff.to_numpy()
    fit = sm.OLS(d, np.ones_like(d)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    t = float(fit.tvalues[0])
    return t, float(1 - stats.norm.cdf(t))


def stationary_bootstrap_ci(d: np.ndarray, mean_block: int = 13, reps: int = 1000,
                            seed: int = 20260918, level: float = 0.90) -> tuple[float, float]:
    """Politis-Romano stationary bootstrap CI for the mean of d."""
    rng = np.random.default_rng(seed)
    n, p = len(d), 1.0 / mean_block
    means = np.empty(reps)
    for b in range(reps):
        idx = np.empty(n, dtype=int)
        idx[0] = rng.integers(n)
        for i in range(1, n):
            idx[i] = rng.integers(n) if rng.random() < p else (idx[i - 1] + 1) % n
        means[b] = d[idx].mean()
    a = (1 - level) / 2
    return float(np.quantile(means, a)), float(np.quantile(means, 1 - a))
