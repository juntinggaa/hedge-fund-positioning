"""Versioned candidate stimuli and prior-only uncertainty for weighted_104."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

MODEL_VERSION = "v4.0"
MATERIAL_VERSION = "v4.0-review-1"
MODEL_ID = "weighted_104"
MIN_PRIOR = 52
Z90 = 1.645
PLACEBO_SEED = 20261104
ARMS = ("A", "B", "C-bare", "C-ann", "D")


def prior_uncertainty(predictions: pd.DataFrame, min_prior: int = MIN_PRIOR) -> pd.DataFrame:
    """Expected-change bands and ranks: the current error is never in its reference set."""
    if not predictions.index.is_monotonic_increasing or predictions.index.has_duplicates:
        raise ValueError("prediction dates must be unique and ordered")
    errors = predictions.actual - predictions.pred
    rows = []
    for i, (date, error) in enumerate(errors.items()):
        past = errors.iloc[:i].dropna().to_numpy(float)
        enough = len(past) >= min_prior
        halfwidth = Z90 * float(np.sqrt(np.mean(past ** 2))) if enough else np.nan
        pct = float(np.mean(np.abs(past) < abs(error))) if enough else np.nan
        rows.append({"week": date, "n_prior_errors": len(past),
                     "prior_error_end": errors.index[i - 1] if i else pd.NaT,
                     "band90_halfwidth": halfwidth, "residual_abs_pct_vs_prior": pct,
                     "inside_band": bool(abs(error) <= halfwidth) if enough else None})
    return pd.DataFrame(rows).set_index("week")


def percentile_for_value(errors: pd.Series, date: pd.Timestamp, value: float) -> float:
    past = errors.loc[errors.index < date].dropna().abs()
    return float((past < abs(value)).mean()) if len(past) >= MIN_PRIOR else np.nan


def coverage_table(predictions: pd.DataFrame, stats: pd.DataFrame) -> pd.DataFrame:
    rows = []
    eligible = stats.band90_halfwidth.notna()
    for label, start, end in [("all", 1900, 2100), ("2013-16", 2013, 2016),
                               ("2017-19", 2017, 2019), ("2020-22", 2020, 2022),
                               ("2023-26", 2023, 2026)]:
        mask = eligible & (stats.index.year >= start) & (stats.index.year <= end)
        s = stats.loc[mask]
        rows.append({"era": label, "n": len(s),
                     "coverage": float(s.inside_band.astype(float).mean()),
                     "mean_band_halfwidth_pp": float(s.band90_halfwidth.mean() * 100),
                     "first": str(s.index[0].date()) if len(s) else None,
                     "last": str(s.index[-1].date()) if len(s) else None})
    return pd.DataFrame(rows)


def build_stimuli(sample: pd.DataFrame, positions: pd.DataFrame,
                  predictions: pd.DataFrame, stats: pd.DataFrame) -> pd.DataFrame:
    """Retain all 41 cases, explicitly identifying unavailable model/range rows."""
    s = positions.leveraged_funds_net / positions.open_interest
    previous = s.shift(1)
    errors = predictions.actual - predictions.pred
    rows = []
    for _, case in sample.iterrows():
        date = pd.Timestamp(case.week)
        has_prediction = date in predictions.index
        has = has_prediction and pd.notna(stats.loc[date, "band90_halfwidth"])
        if date not in s.index:
            raise ValueError(f"sample week not found in pinned CFTC data: {date}")
        if has_prediction:
            actual_change = float(s.loc[date] - previous.loc[date])
            np.testing.assert_allclose(actual_change, predictions.loc[date, "actual"], atol=1e-12)
        reason = "eligible" if has else ("fewer than 52 earlier OOS errors" if has_prediction
                                         else "before eligible OOS prediction history")
        expected = float(previous.loc[date] + predictions.loc[date, "pred"]) if has else np.nan
        rows.append({
            "week": date.date().isoformat(), "frame": case.frame, "stratum": case.stratum,
            "model_version": MODEL_VERSION, "material_version": MATERIAL_VERSION,
            "model_id": MODEL_ID, "has_model_output": has, "availability_reason": reason,
            "prev_net_over_oi": float(previous.loc[date]),
            "actual_net_over_oi": float(s.loc[date]),
            "actual_change": float(s.loc[date] - previous.loc[date]),
            "predicted_change": float(predictions.loc[date, "pred"]) if has else np.nan,
            "expected_net_over_oi": expected,
            "residual": float(errors.loc[date]) if has else np.nan,
            "band90_halfwidth": float(stats.loc[date, "band90_halfwidth"]) if has else np.nan,
            "residual_abs_pct_vs_prior": float(stats.loc[date, "residual_abs_pct_vs_prior"]) if has else np.nan,
            "n_prior_errors": int(stats.loc[date, "n_prior_errors"]) if has_prediction else 0,
        })
    out = pd.DataFrame(rows)
    covered = out.index[out.has_model_output]
    permutation = np.random.default_rng(PLACEBO_SEED).permutation(len(covered))
    out["placebo_source_week"] = None
    out["placebo_residual"] = np.nan
    out["placebo_expected_net_over_oi"] = np.nan
    out["placebo_residual_abs_pct_vs_prior"] = np.nan
    for destination, source in zip(covered, covered[permutation]):
        date = pd.Timestamp(out.loc[destination, "week"])
        value = float(out.loc[source, "residual"])
        out.loc[destination, "placebo_source_week"] = out.loc[source, "week"]
        out.loc[destination, "placebo_residual"] = value
        out.loc[destination, "placebo_expected_net_over_oi"] = out.loc[destination, "actual_net_over_oi"] - value
        out.loc[destination, "placebo_residual_abs_pct_vs_prior"] = percentile_for_value(errors, date, value)
    return out


def legacy_module(root: Path):
    """Read the existing table/question/arm definitions without changing its CLI."""
    spec = importlib.util.spec_from_file_location("hfpos_legacy_prompts", root / "scripts/build_prompts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def annotation(card: dict) -> str:
    perf = card["all_raw_predictions_evaluation"]
    cov = card["uncertainty"]["historical_coverage"]
    return (
        f"How to read the model output above (model {card['model_version']}). "
        "This is a retrospective same-week conditional estimate of the weekly CHANGE in "
        "leveraged funds' net position as a share of open interest. It uses returns, realised "
        "volatility, yield levels and curve shape, equity volatility, a funding-stress proxy, "
        "a futures-yield return residual, current-week open-interest change, changes in Fed "
        "Treasury holdings, a quarter-end flag, and lagged own, other-group and cross-contract "
        "positions. More recent training observations receive more weight, with a two-year half-life.\n\n"
        "- The expected level equals last week's actual level plus the model's estimated weekly "
        "change. The residual is equivalently the conditional level gap or the unexpected weekly "
        "adjustment, measured in percentage points of open interest. It is not an identified "
        "fraction of the whole position attributable to any strategy.\n"
        "- These are statistical associations. The cash leg of a basis trade is unobserved; "
        "none of the inputs directly measures genuine cash-futures basis profitability. Neither "
        "the expected component nor the residual identifies motives, basis quantities or private information.\n"
        f"- Across {perf['n']} out-of-sample weeks ({perf['first']} to {perf['last']}), squared "
        f"prediction error was {perf['r2_vs_mean'] * 100:.2f}% lower than an expanding historical-mean "
        f"change benchmark (out-of-sample R²). RMSE was {perf['rmse_pp']:.2f} percentage points of "
        f"open interest. This R² is not a percentage of the outstanding position explained by a strategy.\n"
        "- The approximate range uses only errors from earlier out-of-sample weeks. Its realised "
        f"historical coverage was {cov * 100:.1f}% across {card['uncertainty']['n_eligible']} eligible "
        "weeks, with variation across eras. This is not a guaranteed probability for this individual week. "
        "Being inside a broad range does not mean the point prediction closely anticipated the move.\n"
        "- The model includes current-week CFTC open interest, so this is not a pre-Friday "
        "nowcast or a next-week forecast. The model and performance summary were selected "
        "retrospectively; this is not a historically deployable untouched backtest."
    )


def model_block(row: pd.Series, placebo: bool = False) -> str:
    if not bool(row.has_model_output):
        raise ValueError(f"no eligible model output for {row.week}")
    exp = float(row.placebo_expected_net_over_oi if placebo else row.expected_net_over_oi) * 100
    res = float(row.placebo_residual if placebo else row.residual) * 100
    pct = float(row.placebo_residual_abs_pct_vs_prior if placebo else row.residual_abs_pct_vs_prior)
    smaller = int(round(pct * 100))
    band = float(row.band90_halfwidth) * 100
    return (
        f"Output of a supervised model of leveraged-fund positioning (model {MODEL_VERSION}):\n\n"
        f"- Expected net position this week: {exp:+.2f}% of open interest "
        f"(approximate 90% range based on earlier out-of-sample errors: {exp - band:+.2f}% to {exp + band:+.2f}%).\n"
        f"- Actual net position this week: {row.actual_net_over_oi * 100:+.2f}% of open interest.\n"
        f"- Residual (actual minus expected): {res:+.2f} percentage points of open interest. "
        f"Among earlier absolute out-of-sample residuals, approximately {smaller}% were smaller "
        f"than this one and {100 - smaller}% were at least as large."
    )


def build_prompt(week: str, arm: str, positions: pd.DataFrame, stimuli: pd.DataFrame,
                 card: dict, legacy) -> str:
    if arm not in ARMS:
        raise ValueError(f"unknown arm: {arm}")
    if arm in ("A", "B"):
        return legacy.build(week, arm, positions, pd.DataFrame())
    row = stimuli.loc[stimuli.week == week]
    if len(row) != 1:
        raise ValueError(f"expected exactly one stimulus row for {week}")
    baseline = legacy.build(week, "A", positions, pd.DataFrame())
    suffix = "\n\n" + legacy.QUESTION
    if not baseline.endswith(suffix):
        raise ValueError("legacy question layout changed")
    pieces = [baseline[:-len(suffix)], model_block(row.iloc[0], placebo=arm == "D")]
    if arm == "C-ann":
        pieces.append(annotation(card))
    pieces.append(legacy.QUESTION)
    return "\n\n".join(pieces)
