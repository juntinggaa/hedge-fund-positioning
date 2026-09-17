"""Stationary block bootstrap over the full two-stage pipeline (issue #16).

Mean block ~13 weeks, 1000 replications, seeded from config. This resamples and
refits Stage 1 as well as Stage 2 -- bootstrapping only Stage 2 does not fix the
generated-regressor problem. Budget real compute time."""

from __future__ import annotations

import pandas as pd

from hfpos import config  # noqa: F401


def run(frame: pd.DataFrame, statistic, n_rep: int, mean_block: int, seed: int):
    """Bootstrap distribution of a pipeline statistic."""
    raise NotImplementedError("issue #16: block bootstrap")
