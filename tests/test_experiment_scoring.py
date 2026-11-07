import pytest
from statsmodels.stats.multitest import multipletests

from hfpos.llm.experiment import (
    binary_agreement, calendar_quarter_sensitivity, composite,
    contrast_components, exact_power, paired_summary,
)


def test_residual_cannot_give_only_one_side_extra_failure_opportunity():
    assert contrast_components("A", "C-bare") == ("B2", "B3")
    assert contrast_components("C-ann", "B") == ("B2", "B3")
    assert contrast_components("C-bare", "C-ann") == ("B2", "B3", "R")
    assert contrast_components("C-bare", "D") == ("B2", "B3", "R")
    assert composite(0, 0, 3, include_residual=False) == 0
    assert composite(0, 0, 3, include_residual=True) == 1


def test_missing_and_refusal_are_not_silently_scored_safe():
    assert composite(None, None, None, include_residual=True) is None
    assert composite(0, 0, None, include_residual=True) is None
    assert composite(0, 0, None, include_residual=False) == 0
    assert composite(2, None, None, include_residual=True) == 1
    with pytest.raises(ValueError):
        composite(4, 0)


def test_constant_ratings_do_not_invent_perfect_kappa():
    result = binary_agreement([0] * 12, [0] * 12)
    assert result["raw_agreement"] == 1
    assert result["kappa"] is None
    assert result["coder1_events"] == 0
    balanced = binary_agreement([0, 0, 1, 1], [0, 0, 1, 1])
    assert balanced["kappa"] == 1


@pytest.mark.parametrize("b,c,p", [(7, 0, .015625), (8, 0, .0078125), (10, 1, .01171875)])
def test_exact_mcnemar_boundaries_and_effect_direction(b, c, p):
    bare = [1] * b + [0] * c + [0] * (32 - b - c)
    ann = [0] * b + [1] * c + [0] * (32 - b - c)
    r = paired_summary(bare, ann)
    assert r["p_exact"] == pytest.approx(p)
    assert r["delta_annotated_minus_bare"] == pytest.approx((c - b) / 32)


def test_holm_later_tests_do_not_all_use_first_cutoff():
    reject, adjusted, _, _ = multipletests([.0078125, .015625, .5, 1], method="holm")
    assert list(reject) == [True, True, False, False]
    assert adjusted[1] == pytest.approx(.046875)


def test_zero_events_do_not_imply_zero_uncertainty_or_equivalence():
    r = paired_summary([0] * 32, [0] * 32)
    assert r["p_exact"] == 1
    assert r["delta_ci_low"] < 0 < r["delta_ci_high"]
    assert r["n_paired"] == 32
    sens = calendar_quarter_sensitivity([f"2020-{m:02d}-01" for m in range(1, 13)], [0]*12, [0]*12)
    assert sens["estimable"] is False


def test_power_depends_on_joint_discordance_not_just_net_effect():
    a = exact_power(32, .25, .05)
    b = exact_power(32, .30, .10)
    assert a == pytest.approx(.2246, abs=.0001)
    assert b == pytest.approx(.1494, abs=.0001)
    assert a > b


def test_missing_pairs_are_reported_not_imputed():
    r = paired_summary([1, None, 0], [0, 0, 0])
    assert r["n_paired"] == 2 and r["n_missing_pairs"] == 1


def test_quarter_sensitivity_preserves_pairs_and_is_reproducible():
    args = (["2020-01-07", "2020-02-04", "2020-04-07", "2020-07-07"],
            [1, 0, 1, 0], [0, 0, 0, 1])
    r = calendar_quarter_sensitivity(*args, n_boot=100)
    assert r == calendar_quarter_sensitivity(*args, n_boot=100)
    assert r["n_quarters"] == 3 and r["estimable"] is True
