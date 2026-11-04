"""Rates, curve and volatility state on the CFTC snapshot grid (issue #9).

Levels and weekly changes for the 2/5/10/30-year constant-maturity yields, the
10Y-2Y slope, a standard butterfly curvature, and equity volatility.

Two series named in the original plan are absent and the absence is deliberate:
MOVE (rate volatility) is ICE-proprietary and not on FRED, so realized futures
volatility in `momentum` stands in for it; FOMC-meeting dummies would need a
hand-maintained meeting calendar, which is not worth its error surface here, so
the omission is recorded rather than approximated.
"""

from __future__ import annotations

import pandas as pd

from hfpos.features.align import as_of

YIELDS = ["DGS2", "DGS5", "DGS10", "DGS30"]


def build(fred: pd.DataFrame, snapshots: pd.DatetimeIndex) -> pd.DataFrame:
    """Weekly macro-financial state features."""
    levels = as_of(fred[YIELDS + ["VIXCLS"]], snapshots)

    out = pd.DataFrame(index=snapshots)
    for code in YIELDS:
        out[f"y_{code[3:].lower()}"] = levels[code]
        out[f"dy_{code[3:].lower()}"] = levels[code].diff()

    out["slope_10_2"] = levels["DGS10"] - levels["DGS2"]
    out["d_slope"] = out["slope_10_2"].diff()
    out["curvature"] = 2 * levels["DGS5"] - levels["DGS2"] - levels["DGS10"]
    out["vix"] = levels["VIXCLS"]
    out["d_vix"] = levels["VIXCLS"].diff()
    return out
