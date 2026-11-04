"""Assemble the modelling frame (issue #9).

Joins positions, prices, basis conditions, momentum and macro onto the CFTC
snapshot grid and writes data/processed.

**What the target is.** `d_net_over_oi` is the change in the group's net position
scaled by open interest. Scaling matters: open interest in this contract ranges
from 888,595 to 6,254,472 contracts across the sample, a factor of 7, so a model
trained on raw net contracts would spend its capacity learning that the market got
bigger. Differencing matters too: the level of net/OI has a lag-1 autocorrelation
of 0.991, which makes predicting it almost free and almost meaningless.

**This is a contemporaneous model, not a forecast.** Features at snapshot t
describe market state measured at t, and the target is the positioning change
realised at t. That is the right design for a decomposition -- we are asking what
share of this week's positioning change ordinary market conditions account for --
but it means the Stage-1 R-squared is NOT a forecasting result and must never be
reported as one. Only the lagged own-position terms look backwards, and they are
lagged precisely so the model cannot see its own target.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.features import basis, macro, momentum, positions as position_features
from hfpos.ingest import cftc, fred, prices

log = logging.getLogger(__name__)

TARGET = "d_net_over_oi"


def build(
    contract: str = "UST_10Y",
    group: str = "leveraged_funds",
    feature_set: str = "extended",
) -> pd.DataFrame:
    """Full weekly feature matrix plus the Stage-1 target.

    `feature_set` is "baseline" (market state only, the Milestone 1 specification)
    or "extended" (adds lagged cross-group and cross-contract positioning, the Fed
    balance sheet and a quarter-end dummy). Both are kept so the gain from the
    extra variables is measurable rather than asserted.
    """
    positions = cftc.load(contract)
    price_frame = prices.load()
    fred_frame = fred.load()
    snapshots = positions.index

    net_over_oi = positions[f"{group}_net"] / positions["open_interest"]
    frame = pd.DataFrame(index=snapshots)
    frame[TARGET] = net_over_oi.diff()

    # Lagged own position: the model may use where positioning WAS, never where it
    # went. Both terms are shifted, so neither contains the target.
    frame["net_over_oi_lag1"] = net_over_oi.shift(1)
    frame["d_net_over_oi_lag1"] = net_over_oi.diff().shift(1)
    frame["d_log_oi"] = np.log(positions["open_interest"]).diff()

    mom = momentum.build(price_frame, snapshots)
    mac = macro.build(fred_frame, snapshots)
    bas = basis.build(mom["ret_1w"], fred_frame, snapshots, mac["dy_10"])
    if feature_set == "baseline":
        # The Milestone 1 specification: market state only.
        mac = mac.drop(columns=[c for c in ("d_log_soma", "quarter_end_week") if c in mac])
        blocks = [frame, mom, mac, bas]
    elif feature_set == "extended":
        blocks = [frame, mom, mac, bas, position_features.build(positions, group)]
    else:
        raise ValueError(f"unknown feature_set {feature_set!r}")
    frame = pd.concat(blocks, axis=1)

    frame.index.name = "as_of"
    return frame


def feature_columns(frame: pd.DataFrame) -> list[str]:
    """Model inputs: everything except the target and bookkeeping columns."""
    drop = {TARGET, "funding_rung", "empirical_duration"}
    return [c for c in frame.columns if c not in drop]


def write(contract: str = "UST_10Y", group: str = "leveraged_funds") -> pd.DataFrame:
    """Build and persist the modelling frame."""
    frame = build(contract, group)
    path = config.path("processed") / f"features_{contract.lower()}_{group}.parquet"
    frame.to_parquet(path)
    log.info("wrote %s  %d rows x %d cols", path.name, len(frame), frame.shape[1])
    return frame


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    frame = write()
    usable = frame.dropna()
    log.info(
        "complete rows %d of %d  (%s -> %s)",
        len(usable), len(frame), usable.index[0].date(), usable.index[-1].date(),
    )
    log.info("features: %s", ", ".join(feature_columns(frame)))


if __name__ == "__main__":
    main()
