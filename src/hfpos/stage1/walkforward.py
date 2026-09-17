"""Expanding-window walk-forward splitter.

Every guard against look-ahead bias in this project routes through here. Two
properties matter and are enforced by tests:

1. Training data always lies strictly before the test block.
2. An `embargo` gap sits between them. This exists because forward-looking targets
   overlap: a 4-week return labelled at time t is not fully observed until t+4, so
   training on observations within 4 steps of the test block leaks the answer.
   Stage 1 targets are contemporaneous (embargo 0); Stage 2 must pass
   embargo = horizon - 1.

Anything fitted on training data — scalers, hyperparameters, feature selection —
must be fitted inside the loop, per fold. See issues #10 and #12.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np


@dataclass(frozen=True)
class Split:
    """Positional indices for one walk-forward fold."""

    train: np.ndarray
    test: np.ndarray

    @property
    def train_end(self) -> int:
        return int(self.train[-1])

    @property
    def test_start(self) -> int:
        return int(self.test[0])


class ExpandingWindowSplitter:
    """Expanding training window, fixed-size contiguous test blocks.

    Args:
        min_train: observations required before the first prediction is made.
        step: size of each test block, i.e. how often the model is refitted.
        embargo: observations dropped from the end of training, to keep
            overlapping forward targets out of the training set.
    """

    def __init__(self, min_train: int, step: int, embargo: int = 0) -> None:
        if min_train < 1:
            raise ValueError("min_train must be >= 1")
        if step < 1:
            raise ValueError("step must be >= 1")
        if embargo < 0:
            raise ValueError("embargo must be >= 0")
        self.min_train = min_train
        self.step = step
        self.embargo = embargo

    def _first_test_start(self) -> int:
        return self.min_train + self.embargo

    def n_splits(self, n: int) -> int:
        first = self._first_test_start()
        if n <= first:
            return 0
        return -(-(n - first) // self.step)  # ceil division

    def split(self, n: int) -> Iterator[Split]:
        """Yield folds covering every observation from `min_train + embargo` onward.

        Test blocks tile the tail of the sample contiguously: no gaps, no overlap,
        every eligible observation predicted exactly once.
        """
        idx = np.arange(n)
        for start in range(self._first_test_start(), n, self.step):
            train_end = start - self.embargo
            yield Split(train=idx[:train_end], test=idx[start : start + self.step])
