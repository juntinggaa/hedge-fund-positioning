"""v2 feature blocks (spec section 3). Every block is causal: values at snapshot t
use market data through t and CFTC data through t-1 only."""

from __future__ import annotations

import numpy as np
import pandas as pd

from hfpos.features.align import as_of
from hfpos.features.build import TARGET, build as build_v1, feature_columns as v1_columns
from hfpos.ingest import cftc, cftc_traders, prices

GROUP = "leveraged_funds"
CONTRACTS = ("UST_2Y", "UST_5Y", "UST_10Y", "UST_30Y")
#: APPROXIMATE dollar value of a basis point per contract: face value x a typical
#: CTD modified duration. Fixed over time -- an approximation, labelled as such.
DV01_APPROX = {"UST_2Y": 38.0, "UST_5Y": 42.0, "UST_10Y": 63.0, "UST_30Y": 150.0}
EWMA_PAIRS = ((8, 24), (16, 48), (32, 96))
VOL_WINDOW = 63
LAG_DAYS = 250

ALT_TARGET = "d_net_over_prev_oi"
RENAME = {"futures_cash_spread": "futures_yield_residual",
          "futures_cash_spread_13w": "futures_yield_residual_13w"}


def base_frame() -> pd.DataFrame:
    """v1 extended frame with the mislabelled 'basis' column renamed, plus targets."""
    frame = build_v1(feature_set="extended").rename(columns=RENAME)
    pos = cftc.load("UST_10Y")
    net, oi = pos[f"{GROUP}_net"], pos["open_interest"]
    frame[ALT_TARGET] = (net.diff() / oi.shift(1)).reindex(frame.index)
    frame["s_level"] = (net / oi).reindex(frame.index)
    frame["s_level_lag1"] = frame["s_level"].shift(1)
    return frame


def v1_features(frame: pd.DataFrame) -> list[str]:
    drop = {ALT_TARGET, "s_level", "s_level_lag1"}
    return [RENAME.get(c, c) for c in v1_columns(frame) if c not in drop]


def trend_block(snapshots: pd.DatetimeIndex) -> pd.DataFrame:
    close = prices.load()["close"].sort_index()
    log_p = np.log(close)
    daily_ret = log_p.diff()
    vol = daily_ret.rolling(VOL_WINDOW).std()           # trailing, causal
    out = pd.DataFrame(index=snapshots)
    lp = as_of(log_p, snapshots)
    out["ret_26w"] = lp.diff(26)
    out["ret_52w"] = lp.diff(52)
    for fast, slow in EWMA_PAIRS:
        cross = (log_p.ewm(halflife=fast).mean() - log_p.ewm(halflife=slow).mean()) / vol
        weekly = as_of(cross, snapshots)
        out[f"xmac_{fast}_{slow}"] = weekly
        out[f"d_xmac_{fast}_{slow}"] = weekly.diff()
    return out


def econ_block(frame: pd.DataFrame) -> pd.DataFrame:
    snapshots = frame.index
    pos = cftc.load("UST_10Y").reindex(snapshots)
    oi = pos["open_interest"]
    out = pd.DataFrame(index=snapshots)
    for side in ("long", "short", "spread"):
        out[f"lev_{side}_oi_lag1"] = (pos[f"{GROUP}_{side}"] / oi).shift(1)

    tr = cftc_traders.load("UST_10Y").reindex(snapshots)
    out["log_traders_long_lag1"] = np.log(tr["traders_lev_long"]).shift(1)
    out["log_traders_short_lag1"] = np.log(tr["traders_lev_short"]).shift(1)
    out["d_log_traders_short_lag1"] = np.log(tr["traders_lev_short"]).diff().shift(1)

    dv01 = pd.DataFrame({c: cftc.load(c)[f"{GROUP}_net"].reindex(snapshots) * DV01_APPROX[c]
                         for c in CONTRACTS})
    gross = dv01.abs().sum(axis=1)
    out["dv01_share_10y_lag1"] = (dv01["UST_10Y"] / gross).shift(1)
    out["dv01_curve_tilt_lag1"] = (((dv01["UST_10Y"] + dv01["UST_30Y"])
                                    - (dv01["UST_2Y"] + dv01["UST_5Y"])) / gross).shift(1)

    out["d_rvol_4w"] = frame["rvol_4w"].diff()
    out["pos_x_rvol"] = frame["net_over_oi_lag1"] * frame["rvol_4w"]
    out["funding_x_vix"] = frame["funding_spread"] * frame["vix"]
    return out


def lag_matrix(snapshots: pd.DatetimeIndex, n_lags: int = LAG_DAYS) -> pd.DataFrame:
    """Boos-Grob regressors: r_{p_t - i} - r_{p_{t-1} - i}, i = 0..n_lags-1.

    p_t is the trading-day position of the last price at or before snapshot t.
    Differencing against the ACTUAL previous snapshot (not a fixed 5 days) makes
    the regressor exactly trend_t - trend_{t-1} in holiday weeks too. Percent units.
    """
    ret = (np.log(prices.load()["close"].sort_index()).diff() * 100).to_numpy()
    days = prices.load().sort_index().index
    pos = days.searchsorted(snapshots, side="right") - 1
    rows = np.full((len(snapshots), n_lags), np.nan)
    for k in range(1, len(snapshots)):
        p, q = pos[k], pos[k - 1]
        if q - n_lags + 1 < 1:          # need n_lags valid returns for both dates
            continue
        rows[k] = ret[p - np.arange(n_lags)] - ret[q - np.arange(n_lags)]
    return pd.DataFrame(rows, index=snapshots, columns=[f"dr_{i}" for i in range(n_lags)])


def trailing_percentile(level: pd.Series, window: int = 260) -> pd.Series:
    """Percentile of s_t among the previous `window` observations (t excluded)."""
    vals = level.to_numpy()
    out = np.full(len(vals), np.nan)
    for t in range(window, len(vals)):
        past = vals[t - window:t]
        out[t] = (past < vals[t]).mean()
    return pd.Series(out, index=level.index)


def assemble() -> tuple[pd.DataFrame, dict[str, list[str]]]:
    """Full v2 frame and the feature list of each candidate."""
    frame = base_frame()
    m3 = v1_features(frame)          # taken BEFORE the v2 blocks are attached
    trend, econ = trend_block(frame.index), econ_block(frame)
    lags = lag_matrix(frame.index)
    frame = pd.concat([frame, trend, econ, lags], axis=1)
    sets = {
        "M3": m3,
        "M4": m3 + list(trend.columns),
        "M5": m3 + list(trend.columns) + list(econ.columns),
        "M6": list(lags.columns),
        "B2": ["d_net_over_oi_lag1"],
    }
    return frame, sets


__all__ = ["TARGET", "ALT_TARGET", "assemble", "trailing_percentile", "lag_matrix"]
