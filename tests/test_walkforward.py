"""Leakage guards for the walk-forward splitter (issues #10, #12).

If any of these fail, every out-of-sample number in the project is suspect.
"""

from __future__ import annotations

import numpy as np
import pytest

from hfpos.stage1.walkforward import ExpandingWindowSplitter

N = 1000  # roughly the real sample: TFF weekly, mid-2006 onward


@pytest.fixture
def splitter():
    return ExpandingWindowSplitter(min_train=260, step=13, embargo=0)


def test_train_strictly_precedes_test(splitter):
    for s in splitter.split(N):
        assert s.train_end < s.test_start


def test_no_index_is_both_train_and_test(splitter):
    for s in splitter.split(N):
        assert not set(s.train.tolist()) & set(s.test.tolist())


def test_training_window_expands(splitter):
    sizes = [len(s.train) for s in splitter.split(N)]
    assert sizes == sorted(sizes)
    assert len(set(sizes)) > 1, "expanding window should grow, not slide"


def test_first_train_block_respects_min_train(splitter):
    first = next(splitter.split(N))
    assert len(first.train) == splitter.min_train


def test_test_blocks_tile_the_tail_without_gaps_or_overlap(splitter):
    covered = np.concatenate([s.test for s in splitter.split(N)])
    expected = np.arange(splitter.min_train, N)
    np.testing.assert_array_equal(covered, expected)


@pytest.mark.parametrize("embargo", [0, 1, 3, 12])
def test_embargo_gap_is_exact(embargo):
    sp = ExpandingWindowSplitter(min_train=260, step=13, embargo=embargo)
    for s in sp.split(N):
        assert s.test_start - s.train_end - 1 == embargo


def test_embargo_keeps_overlapping_targets_out_of_training():
    """A 4-week target at time t is unobserved until t+4, so the last 3
    training rows before a test block would leak it."""
    horizon = 4
    sp = ExpandingWindowSplitter(min_train=260, step=13, embargo=horizon - 1)
    for s in sp.split(N):
        assert s.train_end + horizon > s.test_start - 1  # target would have overlapped
        assert s.train_end < s.test_start                 # but it is excluded


def test_no_splits_when_sample_too_short(splitter):
    assert splitter.n_splits(100) == 0
    assert list(splitter.split(100)) == []


def test_n_splits_matches_split(splitter):
    assert splitter.n_splits(N) == len(list(splitter.split(N)))


@pytest.mark.parametrize("bad", [dict(min_train=0), dict(step=0), dict(embargo=-1)])
def test_rejects_invalid_params(bad):
    kwargs = dict(min_train=260, step=13, embargo=0) | bad
    with pytest.raises(ValueError):
        ExpandingWindowSplitter(**kwargs)
