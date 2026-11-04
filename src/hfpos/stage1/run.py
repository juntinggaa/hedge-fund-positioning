"""Stage-1 walk-forward driver (issues #10, #11, #13).

Produces the positioning residual and the two gate diagnostics that decide whether
the residual is worth handing to anything downstream:

  1. Out-of-sample R-squared against an expanding-mean benchmark (Campbell-Thompson
     form). Near zero means the model explains nothing and the residual is the raw
     series with extra steps.
  2. corr(residual, raw d(Net/OI)). Above ~0.9 and the decomposition is cosmetic.

Both belong in the main text of the report, not an appendix. Anyone competent will
compute the second one themselves.

Scalers and hyperparameters are fitted per fold, inside the splitter, never on the
full sample.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.features.build import TARGET, feature_columns
from hfpos.stage1.models import MODELS, fit_predict
from hfpos.stage1.walkforward import ExpandingWindowSplitter

log = logging.getLogger(__name__)


def oos_r2(y_true: np.ndarray, y_pred: np.ndarray, y_bench: np.ndarray) -> float:
    """Out-of-sample R-squared against a benchmark forecast (Campbell-Thompson)."""
    sse = float(((y_true - y_pred) ** 2).sum())
    sst = float(((y_true - y_bench) ** 2).sum())
    return 1.0 - sse / sst if sst > 0 else float("nan")


def run(frame: pd.DataFrame, model: str) -> pd.DataFrame:
    """Out-of-sample predictions and residuals for one model."""
    cfg = config.load()["stage1"]
    seed = config.load()["inference"]["bootstrap"]["seed"]
    usable = frame.dropna()
    features = feature_columns(usable)

    X = usable[features].to_numpy(dtype=float)
    y = usable[TARGET].to_numpy(dtype=float)

    splitter = ExpandingWindowSplitter(
        min_train=cfg["min_train_weeks"], step=cfg["refit_every_weeks"], embargo=0
    )
    predictions = np.full(len(usable), np.nan)
    benchmark = np.full(len(usable), np.nan)
    for split in splitter.split(len(usable)):
        predictions[split.test] = fit_predict(
            X[split.train], y[split.train], X[split.test], model, seed
        )
        benchmark[split.test] = y[split.train].mean()

    out = pd.DataFrame(
        {
            "actual": y,
            "expected": predictions,
            "benchmark": benchmark,
            "residual": y - predictions,
        },
        index=usable.index,
    )
    return out.dropna()


def diagnostics(result: pd.DataFrame, model: str) -> dict:
    """The two gate numbers, plus context for reading them."""
    return {
        "model": model,
        "n_predicted": int(len(result)),
        "first": str(result.index[0].date()),
        "last": str(result.index[-1].date()),
        "oos_r2": oos_r2(result["actual"].to_numpy(), result["expected"].to_numpy(),
                         result["benchmark"].to_numpy()),
        "corr_residual_raw": float(result["residual"].corr(result["actual"])),
        "residual_sd": float(result["residual"].std()),
        "actual_sd": float(result["actual"].std()),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    from hfpos.features.build import build

    frame = build()
    rows = []
    for model in MODELS:
        result = run(frame, model)
        diag = diagnostics(result, model)
        rows.append(diag)
        result.to_parquet(config.path("processed") / f"stage1_{model}.parquet")
        log.info(
            "%-6s n=%d  OOS R2 = %+.4f   corr(resid, raw) = %.4f   resid sd / raw sd = %.3f",
            model, diag["n_predicted"], diag["oos_r2"], diag["corr_residual_raw"],
            diag["residual_sd"] / diag["actual_sd"],
        )
    table = pd.DataFrame(rows)
    table.to_csv(config.path("tables") / "stage1_diagnostics.csv", index=False)


if __name__ == "__main__":
    main()
