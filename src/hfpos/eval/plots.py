"""Figures (issue #22).

The decomposition figure is a deliverable in its own right: how the drivers of
leveraged-fund Treasury positioning shift across 2006-2026 -- GFC, ZIRP, March 2020,
the 2022 hiking cycle, the 2023-25 basis build-up. It does not depend on Stage 2
returning a significant result."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def decomposition(attribution: pd.DataFrame, out_path) -> None:
    """Stacked attribution of positioning drivers over time."""
    raise NotImplementedError("issue #22: decomposition figure")
