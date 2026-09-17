"""Inference corrections (issues #16, #17, #18).

1. Overlapping returns: Newey-West with lag >= h-1, or Hodrick.
2. Generated regressor: the Stage-2 regressor is estimated, so ordinary standard
   errors are wrong (Pagan 1984). No analytic fix exists with an ML first stage --
   block-bootstrap the WHOLE pipeline including Stage-1 refits.
3. Multiplicity: primary test unadjusted; all secondaries Romano-Wolf or
   Benjamini-Hochberg, with the family size stated."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def newey_west(resid: pd.Series, horizon_weeks: int) -> float:
    """HAC standard error for an overlapping-returns regression."""
    raise NotImplementedError("issue #17: overlapping-returns correction")
