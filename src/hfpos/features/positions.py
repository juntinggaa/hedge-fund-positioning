"""Cross-group and cross-contract positioning features (issue #9, extended set).

Two sources of information the baseline feature set ignored entirely.

**Other trader groups.** The CFTC panel reports four groups against the same open
interest, and reportable net positions nearly sum to zero. So the contemporaneous
asset-manager net change is close to MINUS the leveraged-fund net change: putting
it in the model would hand over the target by an accounting identity and produce a
near-perfect R-squared that means nothing. Every cross-group term is therefore
LAGGED. A lagged dealer or asset-manager position is legitimate information about
who was on the other side last week; the contemporaneous one is the answer key.

**Other contracts.** Leveraged funds run curve trades, so 2Y, 5Y and 30Y
positioning carries information about the 10Y that the 10Y series alone does not.
These are lagged for the same reason -- they are measured on the same snapshot
date and are not independent of it.
"""

from __future__ import annotations

import pandas as pd

from hfpos.ingest import cftc

OTHER_GROUPS = ("dealer", "asset_manager", "other_reportable")
CURVE_CONTRACTS = ("UST_2Y", "UST_5Y", "UST_30Y")


def cross_group(positions: pd.DataFrame) -> pd.DataFrame:
    """Lagged net positions and changes for the groups other than the subject."""
    out = pd.DataFrame(index=positions.index)
    oi = positions["open_interest"]
    for group in OTHER_GROUPS:
        share = positions[f"{group}_net"] / oi
        out[f"{group}_net_oi_lag1"] = share.shift(1)
        out[f"{group}_d_net_oi_lag1"] = share.diff().shift(1)
    return out


def cross_contract(group: str, snapshots: pd.DatetimeIndex) -> pd.DataFrame:
    """Lagged positioning of the same group in the other Treasury contracts."""
    out = pd.DataFrame(index=snapshots)
    for contract in CURVE_CONTRACTS:
        frame = cftc.load(contract)
        share = (frame[f"{group}_net"] / frame["open_interest"]).reindex(snapshots)
        tag = contract.lower().replace("ust_", "")
        out[f"{tag}_net_oi_lag1"] = share.shift(1)
        out[f"{tag}_d_net_oi_lag1"] = share.diff().shift(1)
    return out


def build(positions: pd.DataFrame, group: str) -> pd.DataFrame:
    """All cross-group and cross-contract features, every one lagged."""
    return pd.concat(
        [cross_group(positions), cross_contract(group, positions.index)], axis=1
    )
