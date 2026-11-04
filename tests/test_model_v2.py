"""Model v2: temporal alignment, target construction, preprocessing isolation,
estimator correctness, and prompt/model-version consistency."""

from __future__ import annotations

import hashlib
import json
import sys

import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from hfpos import config
from hfpos.model_v2.estimators import FusedRidge, make
from hfpos.model_v2.evaluate import walk
from hfpos.model_v2.features import trailing_percentile

ROOT = config.REPO_ROOT
needs_data = pytest.mark.skipif(not (ROOT / "data/raw/prices_zn.parquet").exists(),
                                reason="pinned data not present")
needs_v2 = pytest.mark.skipif(not (ROOT / "docs/model_v2/model_card_v2.json").exists(),
                              reason="run scripts/model_v2.py and build_stimuli_v2.py first")


# ---------- preprocessing isolation (audit A) ----------

class RecordingScaler(StandardScaler):
    fits: list[int] = []

    def fit(self, X, y=None, sample_weight=None):
        RecordingScaler.fits.append(len(X))
        return super().fit(X, y, sample_weight)


def test_scaler_is_refitted_inside_every_inner_fold():
    RecordingScaler.fits = []
    est = make("ridge")
    est.set_params(estimator__scale=RecordingScaler(), param_grid={"est__alpha": [1.0]})
    rng = np.random.default_rng(0)
    est.fit(rng.normal(size=(100, 3)), rng.normal(size=100))
    # TimeSeriesSplit(4) on 100 rows trains on 20, 40, 60, 80 rows; then refit on 100.
    assert RecordingScaler.fits == [20, 40, 60, 80, 100]


def test_gbm_fixed_has_no_random_early_stopping():
    assert make("gbm_fixed").named_steps["est"].early_stopping is False


# ---------- walk-forward: no look-ahead, rolling window ----------

class Spy:
    seen: list[tuple[float, float]] = []

    def fit(self, X, y):
        self.train_max = X[:, 0].max()
        return self

    def predict(self, X):
        Spy.seen.append((self.train_max, X[:, 0].min()))
        return np.zeros(len(X))


@pytest.mark.parametrize("window", ["expanding", "rolling"])
def test_walk_trains_strictly_before_test(window):
    Spy.seen = []
    idx = pd.date_range("2000-01-04", periods=400, freq="W-TUE")
    frame = pd.DataFrame({"t": np.arange(400.0), "y": np.zeros(400)}, index=idx)
    walk(frame, ["t"], "y", Spy, window)
    assert Spy.seen and all(train_max < test_min for train_max, test_min in Spy.seen)


def test_rolling_window_is_260_weeks():
    lengths = []

    class Len(Spy):
        def fit(self, X, y):
            lengths.append(len(X))
            return super().fit(X, y)

    idx = pd.date_range("2000-01-04", periods=600, freq="W-TUE")
    frame = pd.DataFrame({"t": np.arange(600.0), "y": np.zeros(600)}, index=idx)
    walk(frame, ["t"], "y", Len, "rolling")
    assert max(lengths) == 260


def test_trailing_percentile_ignores_current_and_future():
    s = pd.Series(np.arange(300, dtype=float))
    p = trailing_percentile(s, window=260)
    assert p.iloc[:260].isna().all() and (p.iloc[260:] == 1.0).all()
    s2 = s.copy(); s2.iloc[290:] = -1e9                     # change the future only
    assert trailing_percentile(s2, 260).iloc[280] == p.iloc[280]


# ---------- fused ridge (Boos-Grob adaptation) ----------

def test_fused_ridge_recovers_smooth_signature():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(700, 120))
    beta = np.exp(-((np.arange(120) - 30) / 20) ** 2) * 0.01
    y = X @ beta + rng.normal(0, 0.03, 700)
    b = FusedRidge(gamma=30.0).fit(X, y).coef_
    assert np.corrcoef(b, beta)[0, 1] > 0.95


def test_fused_ridge_large_gamma_flattens_coefficients():
    rng = np.random.default_rng(2)
    X, y = rng.normal(size=(300, 50)), rng.normal(size=300)
    b = FusedRidge(gamma=1e6).fit(X, y).coef_
    assert np.abs(b).max() < 1e-6


# ---------- targets and temporal alignment on pinned data ----------

@needs_data
def test_targets_and_level_reconstruction():
    from hfpos.ingest import cftc
    from hfpos.model_v2.features import ALT_TARGET, TARGET, base_frame
    f = base_frame()
    pos = cftc.load("UST_10Y")
    net, oi = pos["leveraged_funds_net"], pos["open_interest"]
    w = f.index[500]; prev = pos.index[pos.index.get_loc(w) - 1]
    assert f.loc[w, TARGET] == pytest.approx(net[w] / oi[w] - net[prev] / oi[prev])
    assert f.loc[w, ALT_TARGET] == pytest.approx((net[w] - net[prev]) / oi[prev])
    # expected level = previous level + predicted change  =>  level residual == change residual
    pred = 0.0123
    assert (f.loc[w, "s_level"] - (f.loc[w, "s_level_lag1"] + pred)) == pytest.approx(
        f.loc[w, TARGET] - pred)


@needs_data
def test_lag_matrix_differences_against_actual_previous_snapshot():
    from hfpos.ingest import prices
    from hfpos.model_v2.features import lag_matrix
    snaps = pd.DatetimeIndex(["2019-11-26", "2019-12-03", "2019-12-10"])  # incl. Thanksgiving week
    m = lag_matrix(snaps, n_lags=10)
    close = prices.load()["close"].sort_index()
    ret = np.log(close).diff() * 100
    days = close.index
    p, q = days.searchsorted(snaps[2], "right") - 1, days.searchsorted(snaps[1], "right") - 1
    assert m.iloc[2, 0] == pytest.approx(ret.iloc[p] - ret.iloc[q])
    assert m.iloc[2, 3] == pytest.approx(ret.iloc[p - 3] - ret.iloc[q - 3])
    assert days[p] <= snaps[2]                                  # never a future price


@needs_data
def test_cross_group_features_are_lagged():
    from hfpos.model_v2.features import base_frame
    from hfpos.ingest import cftc
    f = base_frame(); pos = cftc.load("UST_10Y")
    am = pos["asset_manager_net"] / pos["open_interest"]
    w = f.index[600]; prev = pos.index[pos.index.get_loc(w) - 1]
    assert f.loc[w, "asset_manager_net_oi_lag1"] == pytest.approx(am[prev])


# ---------- prompt / model-version consistency ----------

@needs_v2
def test_annotation_v2_numbers_match_model_card():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_prompts as bp
    card = json.loads((ROOT / "docs/model_v2/model_card_v2.json").read_text())
    text = bp.annotation_v2(card)
    assert f"model {card['model_version']}" in text
    assert f"about {card['oos_r2_vs_historical_mean'] * 100:.0f}% of the variance" in text
    assert f"{card['oos_rmse_pp_of_oi']:.1f} percentage points" in text
    assert f"about {card['corr_residual_actual_change']:.2f} with" in text
    assert "futures-cash spread" not in text            # the mislabelled v1 wording
    assert f"{card['band90_historical_coverage'] * 100:.0f}% of the time" in text
    assert "nowcast" not in text


@needs_v2
def test_stimuli_v2_come_from_the_selected_model():
    card = json.loads((ROOT / "docs/model_v2/model_card_v2.json").read_text())
    sel = json.loads((ROOT / "reports/model_v2/selection.json").read_text())
    stim = pd.read_csv(ROOT / "docs/milestone2/arm_c_stimuli_v2.csv")
    pred = pd.read_parquet(ROOT / f"data/processed/model_v2/{sel['selected']}.parquet")
    assert card["model_id"] == sel["selected"]
    assert set(stim["model_id"]) == {sel["selected"]}
    assert set(stim["model_version"]) == {card["model_version"]}
    assert hashlib.sha256(pred.to_csv().encode()).hexdigest() == card["predictions_sha256"]
    cov = stim[stim["has_model_output"]]
    resid = (pred["actual"] - pred["pred"]).reindex(pd.to_datetime(cov["week"])).to_numpy()
    np.testing.assert_allclose(cov["residual"].to_numpy(), resid)
    np.testing.assert_allclose(cov["actual_net_over_oi"] - cov["expected_net_over_oi"],
                               cov["residual"], atol=1e-12)
    np.testing.assert_allclose(cov["actual_net_over_oi"] - cov["placebo_expected_net_over_oi"],
                               cov["placebo_residual"], atol=1e-12)
    assert sorted(cov["placebo_residual"]) == pytest.approx(sorted(cov["residual"]))


def test_v1_annotation_is_unchanged():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_prompts as bp
    assert hashlib.sha256(bp.ANNOTATION.encode()).hexdigest()[:16] == V1_ANNOTATION_SHA16


V1_ANNOTATION_SHA16 = "4a6ffd79ef918e7b"


@needs_v2
def test_v2_block_states_percentile_in_both_directions():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_prompts as bp
    stim = pd.read_csv(ROOT / "docs/milestone2/arm_c_stimuli_v2.csv")
    week = stim.loc[stim["has_model_output"], "week"].iloc[0]
    block = bp.model_block_v2(stim, week, placebo=False)
    pct = stim.set_index("week").loc[week, "residual_abs_pct_vs_prior"] * 100
    assert f"{pct:.0f}% were smaller" in block and f"{100 - round(pct):.0f}% were larger" in block
    assert "larger in size than" not in block       # the misread pilot wording
