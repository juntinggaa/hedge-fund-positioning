"""Check spacing feasibility against exhaustive tiny examples, not sampled outcomes."""
import importlib.util
from itertools import combinations
from pathlib import Path

import pandas as pd
import pytest


spec = importlib.util.spec_from_file_location(
    "sample_review", Path(__file__).parents[1] / "scripts/review_sample_feasibility.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


@pytest.mark.parametrize("gap", [1, 4, 6, 8])
def test_maximum_matches_exhaustive_subsets(gap):
    # Includes an irregular holiday gap and the exact 28-/56-day boundaries.
    dates = pd.to_datetime(["2014-09-16", "2014-09-30", "2014-10-14",
                            "2014-11-11", "2014-11-17", "2014-12-09"])
    valid = [c for n in range(len(dates) + 1) for c in combinations(dates, n)
             if all((b - a).days >= gap * 7 for a, b in zip(c, c[1:]))]
    assert len(review.earliest_maximum(dates, gap)) == max(map(len, valid))
    maximum = max(map(len, valid))
    possible = {tuple(c) for c in valid if len(c) == maximum}
    for seed in range(12):
        assert tuple(review.uniform_feasible(dates, maximum, gap, seed)) in possible


def test_dp_refuses_infeasible_quota():
    dates = pd.date_range("2014-09-16", "2014-12-30", freq="W-TUE")
    with pytest.raises(ValueError, match="infeasible"):
        review.uniform_feasible(dates, 10, 4, 1)


def test_global_spacing_applies_across_strata():
    pool = pd.DataFrame({"week": pd.to_datetime(["2020-01-07", "2020-01-14", "2020-02-04", "2020-03-03", "2020-03-31"]),
                         "stratum": ["S1", "S2", "S2", "S3", "S4"]})
    selected, status = review.global_sample(pool, dict(S1=1, S2=1, S3=1, S4=1), 4)
    assert status["status"] == 0
    assert pd.Timestamp("2020-01-14") not in set(selected.week)
    assert len(selected) == 4


def test_empty_pool_maximum():
    assert len(review.earliest_maximum(pd.DatetimeIndex([]), 8)) == 0
