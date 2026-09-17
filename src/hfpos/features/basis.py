"""Cash-futures basis proxy -- the highest-risk item (issue #7).

The claim 'we removed basis trading' rests entirely on this. Fallback ladder, best
first: CTD implied repo vs GC repo; futures-implied yield vs cash yield; swap
spreads; SOFR-IORB. SOFR begins 2018, so the early sample needs a fallback, and the
basis trade was small before ~2015 -- 'removing basis' means different things by era.
Record which rung was actually used and downgrade the claim accordingly."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def build(prices: pd.DataFrame, fred: pd.DataFrame, method: str) -> pd.Series:
    """Weekly basis proxy aligned to the TFF as-of Tuesday."""
    raise NotImplementedError("issue #7: basis proxy")
