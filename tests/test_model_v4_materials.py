"""Prior-only ranges, numeric consistency, matched prompts and artifact preservation."""

from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd
import pytest

from hfpos import config
from hfpos.ingest import cftc
from hfpos.model_v4.materials import (
    ARMS, MIN_PRIOR, Z90, annotation, build_prompt, legacy_module,
    model_block, percentile_for_value, prior_uncertainty,
)

ROOT = config.REPO_ROOT
DOC = ROOT / "docs/model_v4/materials"


def synthetic_predictions(n=60):
    dates = pd.date_range("2020-01-07", periods=n, freq="W-TUE")
    return pd.DataFrame({"actual": np.linspace(-.02, .02, n),
                         "pred": np.zeros(n)}, index=dates)


def test_range_excludes_current_and_future_errors():
    p = synthetic_predictions()
    base = prior_uncertainty(p)
    altered = p.copy()
    altered.loc[p.index[55]:, "actual"] += 100
    changed = prior_uncertainty(altered)
    pd.testing.assert_series_equal(base.band90_halfwidth.iloc[:56], changed.band90_halfwidth.iloc[:56])
    pd.testing.assert_series_equal(base.residual_abs_pct_vs_prior.iloc[:55],
                                  changed.residual_abs_pct_vs_prior.iloc[:55])
    assert base.band90_halfwidth.iloc[:MIN_PRIOR].isna().all()
    expected = Z90 * np.sqrt(np.mean(p.actual.iloc[:MIN_PRIOR] ** 2))
    assert base.band90_halfwidth.iloc[MIN_PRIOR] == pytest.approx(expected)
    assert (base.prior_error_end.dropna().to_numpy() < base.index[1:].to_numpy()).all()


def test_percentile_excludes_current_error_and_handles_ties():
    dates = pd.date_range("2020-01-07", periods=54, freq="W-TUE")
    errors = pd.Series([.01] * 26 + [.02] * 26 + [999, 999], index=dates)
    assert percentile_for_value(errors, dates[52], .02) == .5
    assert percentile_for_value(errors, dates[52], .01) == 0
    assert percentile_for_value(errors, dates[52], .03) == 1


def test_unsorted_prediction_history_is_rejected():
    with pytest.raises(ValueError):
        prior_uncertainty(synthetic_predictions().iloc[::-1])


def load_materials():
    return (json.loads((DOC / "model_card_v4.json").read_text()),
            pd.read_csv(DOC / "stimuli_v4.csv"),
            pd.read_parquet(ROOT / "data/processed/model_v4/weighted_104.parquet"))


def test_stimulus_values_reconstruct_the_actual_pinned_position():
    card, s, p = load_materials()
    eligible = s[s.has_model_output]
    assert len(s) == 41 and len(eligible) == 27
    np.testing.assert_allclose(eligible.prev_net_over_oi + eligible.predicted_change,
                               eligible.expected_net_over_oi, atol=1e-12)
    np.testing.assert_allclose(eligible.actual_net_over_oi - eligible.expected_net_over_oi,
                               eligible.residual, atol=1e-12)
    np.testing.assert_allclose(eligible.actual_change - eligible.predicted_change,
                               eligible.residual, atol=1e-12)
    for _, row in eligible.iterrows():
        w = pd.Timestamp(row.week)
        past = (p.actual - p.pred).loc[p.index < w]
        assert row.n_prior_errors == len(past)
        assert row.band90_halfwidth == pytest.approx(Z90 * np.sqrt(np.mean(past ** 2)))
    assert card["sample"]["eligible_n"] == 27


def test_coverage_and_two_performance_samples_are_not_confused():
    card, _, p = load_materials()
    errors = p.actual - p.pred
    actual_hits = []
    for i in range(MIN_PRIOR, len(p)):
        actual_hits.append(abs(errors.iloc[i]) <= Z90 * np.sqrt(np.mean(errors.iloc[:i] ** 2)))
    assert card["uncertainty"]["historical_coverage"] == pytest.approx(np.mean(actual_hits))
    assert card["uncertainty"]["n_eligible"] == 668
    assert card["all_raw_predictions_evaluation"]["n"] == 720
    assert card["selection"]["matched_n"] == 668
    assert card["all_raw_predictions_evaluation"]["r2_vs_mean"] != card["selection"]["candidate_r2_vs_mean"]
    text = annotation(card)
    assert "720" in text and "10.47%" in text
    assert "91.9%" in text and "not a pre-Friday" in text


def test_placebo_uses_recorded_other_week_and_preserves_arithmetic():
    _, s, _ = load_materials()
    eligible = s[s.has_model_output].set_index("week")
    for week, row in eligible.iterrows():
        assert row.placebo_source_week != week
        assert row.placebo_residual == pytest.approx(eligible.loc[row.placebo_source_week, "residual"])
        assert row.actual_net_over_oi - row.placebo_expected_net_over_oi == pytest.approx(row.placebo_residual)


def test_prompts_are_matched_and_preserve_A_B_and_only_C_ann_has_annotation():
    card, stimuli, _ = load_materials()
    legacy = legacy_module(ROOT)
    positions = cftc.load("UST_10Y")
    records = [json.loads(line) for line in (DOC / "review_prompts.jsonl").read_text().splitlines()]
    assert len(records) == 135
    pairs = {(r["week"], r["arm"]) for r in records}
    assert len(pairs) == 135
    for week in stimuli.loc[stimuli.has_model_output, "week"]:
        assert {a for w, a in pairs if w == week} == set(ARMS)
    for r in records:
        prompt = r["prompt"]
        assert prompt == build_prompt(r["week"], r["arm"], positions, stimuli, card, legacy)
        assert r["prompt_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()
        if r["arm"] in ("A", "B"):
            assert prompt == legacy.build(r["week"], r["arm"], positions, pd.DataFrame())
        else:
            assert "model v4.0" in prompt
            assert "percentage points of open interest" in prompt
            assert "were at least as large" in prompt
            assert legacy.MECHANISM not in prompt
        assert ("How to read the model output above" in prompt) == (r["arm"] == "C-ann")


def test_missing_history_cannot_silently_produce_a_model_prompt():
    card, s, _ = load_materials()
    row = s[~s.has_model_output].iloc[0]
    with pytest.raises(ValueError):
        model_block(row)
    with pytest.raises(ValueError):
        build_prompt(row.week, "C-bare", cftc.load("UST_10Y"), s, card, legacy_module(ROOT))


def test_generated_files_and_prompt_provenance_match_manifest():
    manifest = json.loads((DOC / "materials_manifest.json").read_text())
    for path, expected in manifest["generated_files_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    card, _, _ = load_materials()
    for path, expected in card["source_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    card_hash = hashlib.sha256((DOC / "model_card_v4.json").read_bytes()).hexdigest()
    for line in (DOC / "review_prompts.jsonl").read_text().splitlines():
        assert json.loads(line)["model_card_sha256"] == card_hash


def test_all_preexisting_outputs_and_user_work_are_preserved():
    rec = json.loads((DOC / "preservation_before.json").read_text())["sha256"]
    changed = [name for name, h in rec.items()
               if not (ROOT / name).exists()
               or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != h]
    assert changed == []
