"""Do positions lead or lag returns? (issue #8)

This runs BEFORE Stage 1 and it is not a formality. If positioning merely follows
past returns, then a feature set without lagged returns produces a "surprise" that
is really momentum in disguise -- the model would be removing nothing and the
residual would inherit the thing we claim to have taken out.

Two diagnostics:

  * cross-correlations of d(Net/OI) against futures returns at leads and lags. A
    significant correlation at a NEGATIVE lag means returns move first and
    positioning follows (Sanders-Irwin-Merrin); at a POSITIVE lag it means
    positioning moves first.
  * a small two-variable VAR with Granger-causality tests in both directions.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

MAX_LAG = 6
VAR_LAGS = 4


def cross_correlations(positions: pd.Series, returns: pd.Series, max_lag: int = MAX_LAG) -> pd.DataFrame:
    """corr(d position at t, return at t+k) for k in [-max_lag, max_lag]."""
    joined = pd.concat([positions.rename("pos"), returns.rename("ret")], axis=1).dropna()
    n = len(joined)
    rows = []
    for k in range(-max_lag, max_lag + 1):
        corr = float(joined["pos"].corr(joined["ret"].shift(-k)))
        rows.append(
            {
                "lag_k": k,
                "corr": corr,
                "reads_as": "returns lead positioning" if k < 0
                else ("positioning leads returns" if k > 0 else "contemporaneous"),
                "abs_t": abs(corr) * np.sqrt(max(n - abs(k) - 2, 1)) / np.sqrt(max(1 - corr**2, 1e-12)),
            }
        )
    return pd.DataFrame(rows)


def granger(positions: pd.Series, returns: pd.Series, lags: int = VAR_LAGS) -> pd.DataFrame:
    """Granger-causality p-values in both directions from a two-variable VAR."""
    from statsmodels.tsa.api import VAR

    joined = pd.concat([positions.rename("pos"), returns.rename("ret")], axis=1).dropna()
    fitted = VAR(joined).fit(lags)
    rows = []
    for caused, causing in (("pos", "ret"), ("ret", "pos")):
        test = fitted.test_causality(caused, causing, kind="f")
        rows.append({"caused": caused, "causing": causing,
                     "statistic": float(test.test_statistic), "p_value": float(test.pvalue)})
    return pd.DataFrame(rows)


def run(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Lead-lag correlation table and Granger summary."""
    return {
        "cross_correlations": cross_correlations(frame["d_net_over_oi"], frame["ret_1w"]),
        "granger": granger(frame["d_net_over_oi"], frame["ret_1w"]),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    from hfpos import config
    from hfpos.features.build import build

    result = run(build().dropna())
    for name, table in result.items():
        table.to_csv(config.path("tables") / f"stage0_{name}.csv", index=False)
        log.info("\n%s\n%s", name, table.to_string(index=False, float_format=lambda v: f"{v:8.4f}"))


if __name__ == "__main__":
    main()
