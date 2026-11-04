"""v3 feature blocks S (coupon supply) and D (primary-dealer inventory).

Every value at snapshot t uses only information dated at or before t under the
timing rules in docs/model_v3/SPEC_2026-11-05.md section 3.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from hfpos.model_v3 import sources

SECTOR_10 = {"7-Year", "10-Year"}
#: APPROXIMATE 10y-equivalent duration weights by original term (fixed; labelled).
DUR_W = {2: 0.22, 3: 0.32, 5: 0.53, 7: 0.72, 10: 1.0, 20: 1.6, 30: 2.1}
SCALE_WINDOW = 52
Z_WINDOW = 156
PD_RELEASE_LAG_DAYS = 9


def term_years(term: str) -> float:
    """'5-Year 2-Month' -> 5.1667."""
    parts = term.replace("-", " ").split()
    years = float(parts[0]) if "Year" in term else 0.0
    months = float(parts[parts.index("Month") - 1]) if "Month" in term else 0.0
    return years + months / 12


def dur_weight(term: str) -> float:
    """Linear interpolation of DUR_W over years (implementation note, spec amendment 1)."""
    k = np.array(sorted(DUR_W)); v = np.array([DUR_W[x] for x in k])
    return float(np.interp(term_years(term), k, v))


def coupon_universe(a: pd.DataFrame) -> pd.DataFrame:
    a = a[(a["inflation_index_security"] != "Yes") & (a["floating_rate"] != "Yes")]
    return a[a["security_type"].isin(["Note", "Bond"])].copy()


def supply_raw(snapshots: pd.DatetimeIndex, auctions: pd.DataFrame) -> pd.DataFrame:
    """Raw $ sums per snapshot interval (prev snapshot, t]. No result used before auction_date."""
    a = coupon_universe(auctions)
    a["is10"] = a["original_security_term"].isin(SECTOR_10)
    a["dur_w"] = a["original_security_term"].map(dur_weight)
    snaps = pd.DatetimeIndex(snapshots).sort_values()
    out = pd.DataFrame(index=snaps, columns=["settle_10s", "pending_10s", "announced_10s",
                                             "settle_dur_all"], dtype=float)
    prev = snaps[0] - pd.Timedelta(days=7)
    for t in snaps:
        settle = a[(a["issue_date"] > prev) & (a["issue_date"] <= t)]
        out.loc[t, "settle_10s"] = settle.loc[settle["is10"], "total_accepted"].sum()
        out.loc[t, "settle_dur_all"] = (settle["total_accepted"] * settle["dur_w"]).sum()
        pend = a[a["is10"] & (a["auction_date"] <= t) & (a["issue_date"] > t)]
        out.loc[t, "pending_10s"] = pend["total_accepted"].sum()
        ann = a[a["is10"] & (a["announcemt_date"] <= t) & (a["auction_date"] > t)]
        out.loc[t, "announced_10s"] = ann["offering_amt"].sum()
        prev = t
    return out


def prior_mean_scale(x: pd.Series, window: int = SCALE_WINDOW) -> pd.Series:
    """log1p(x_t / mean(x_{t-window..t-1})); t excluded."""
    base = x.shift(1).rolling(window, min_periods=window).mean()
    return np.log1p(x / base)


def supply_block(snapshots: pd.DatetimeIndex, auctions: pd.DataFrame | None = None,
                 history_start: str = "2000-01-01") -> pd.DataFrame:
    """Scaled S features. Raw sums are computed on a weekly grid from history_start so
    the trailing mean exists from the first CFTC snapshot; then restricted."""
    auctions = sources.load_auctions() if auctions is None else auctions
    snaps = pd.DatetimeIndex(snapshots).sort_values()
    pre = pd.date_range(history_start, snaps[0] - pd.Timedelta(days=1), freq="W-TUE")
    grid = pre.union(snaps)
    raw = supply_raw(grid, auctions)
    out = pd.DataFrame({f"s_{c}": prior_mean_scale(raw[c]) for c in raw.columns})
    return out.reindex(snaps)


def pd_available(pdw: pd.DataFrame, snapshots: pd.DatetimeIndex,
                 lag_days: int = PD_RELEASE_LAG_DAYS) -> pd.DataFrame:
    """For each snapshot t, the row of the latest as-of date a with a + lag_days <= t.
    Returns the as-of date used in column 'pd_asof'."""
    asof = pdw.index.to_numpy()
    rows = []
    for t in snapshots:
        ok = asof[asof + np.timedelta64(lag_days, "D") <= np.datetime64(t)]
        rows.append(ok.max() if len(ok) else np.datetime64("NaT"))
    used = pd.DatetimeIndex(rows)
    out = pdw.reindex(used)
    out.index = snapshots
    out["pd_asof"] = used
    return out


def prior_z(x: pd.Series, window: int = Z_WINDOW) -> pd.Series:
    """(x_t - mean) / sd over the previous `window` observations, t excluded."""
    past = x.shift(1).rolling(window, min_periods=window)
    return (x - past.mean()) / past.std()


def _release_features(pdw: pd.DataFrame) -> pd.DataFrame:
    """Features on the release (as-of) grid, then mapped to snapshots by availability."""
    f = pd.DataFrame(index=pdw.index)
    for key, name in (("PDPOSGSC-G7L11", "coup711"), ("PDPOSGST-TOT", "ust_tot")):
        x = pdw[key]
        f[f"d_{name}_z"] = prior_z(x)
        ch4 = x.diff(4)
        f[f"d_{name}_ch4_z"] = ch4 / ch4.shift(1).rolling(Z_WINDOW, min_periods=Z_WINDOW).std()
    fails = pdw["PDFTD-USTET"] + pdw["PDFTR-USTET"]
    f["d_fails_z"] = prior_z(np.log(fails))
    return f


def dealer_block(snapshots: pd.DatetimeIndex, pdw: pd.DataFrame | None = None,
                 reset_after: str | None = None) -> pd.DataFrame:
    """D features at each snapshot from the latest release available by then.

    reset_after: sensitivity check only; history before this as-of date is dropped,
    so z-scores restart with a full burn-in after a flagged break."""
    pdw = sources.load_pd() if pdw is None else pdw
    if reset_after is not None:
        pdw = pdw[pdw.index >= pd.Timestamp(reset_after)]
    feats = _release_features(pdw)
    return pd_available(feats, pd.DatetimeIndex(snapshots))


def break_audit(pdw: pd.DataFrame, breaks: list[dict], keys: tuple[str, ...]) -> pd.DataFrame:
    """First post-break weekly change as a percentile of |weekly change| over prior 156."""
    rows = []
    for b in breaks:
        start = pd.Timestamp(b["startdate"])
        if start <= pdw.index.min():
            continue
        for k in keys:
            d = pdw[k].diff()
            post = d[d.index >= start].dropna()
            prior = d[d.index < start].dropna().abs().tail(Z_WINDOW)
            if post.empty or len(prior) < 52:
                continue
            first = post.iloc[0]
            rows.append({"break": b["seriesbreak"], "start": start.date(), "series": k,
                         "first_asof": post.index[0].date(), "change": first,
                         "pct_of_prior_abs": float((prior < abs(first)).mean()),
                         "flag_gt_p99": bool((prior < abs(first)).mean() > 0.99)})
    return pd.DataFrame(rows)
