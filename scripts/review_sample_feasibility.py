"""Non-destructive, dated data extension and pre-experiment sampling review.

Never writes legacy caches, samples, prompts, or model results. No LLM calls.
Run with the project virtualenv. Live downloads are retained in a new namespace.
"""
from __future__ import annotations

import hashlib
import io
import json
import random
import re
import subprocess
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from hfpos import config
from hfpos.features import basis, macro, momentum, positions as pf
from hfpos.ingest import cftc, cftc_archive, fred, prices
from hfpos.model_v2.features import ALT_TARGET, RENAME, base_frame, v1_features
from hfpos.model_v4.adaptation import RecencyRidge
from hfpos.model_v4.materials import prior_uncertainty

ROOT = config.REPO_ROOT
STAMP = "2026-11-05"
LAST = pd.Timestamp("2026-10-27")  # confirmed official report header, not API maximum
RAW = ROOT / "data/raw" / f"sampling_review_{STAMP}"
OUT = ROOT / "reports" / f"sampling_review_{STAMP}"
DOC = ROOT / "docs" / f"sampling_review_{STAMP}"
EXPORT = Path("/Users/lipjunting/Documents/Codex/2026-11-04/can-u/outputs/sampling_feasibility")
SEED = 20261105
PILOT = pd.Timestamp("2025-09-02")
# Identifiers from prior pilot design; responses are never read or used.
DEVELOPMENT = pd.DatetimeIndex(["2026-09-01", "2023-07-11", "2026-06-30",
                              "2025-06-17", "2026-08-25", "2025-02-18"])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, default=str) + "\n")


def preserved_files():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    paths = {ROOT / f for f in tracked} | set((ROOT / "data").rglob("*.parquet"))
    return {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)
            if p.is_file() and not any(str(p).startswith(str(d)) for d in (RAW, OUT, DOC))}


def get_bytes(url, name):
    dest = RAW / name
    if not dest.exists():
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
    return dest.read_bytes()


def cftc_panel(alias):
    code = cftc.contract_code(alias)
    dest = RAW / f"socrata_{code}.json"
    if not dest.exists():
        save_json(dest, cftc.fetch_records(code, start="2026-01-01"))
    live = cftc.to_frame(json.loads(dest.read_text())).loc[:LAST]
    old = cftc.load(alias)
    overlap = old.index.intersection(live.index)
    changes = []
    for day in overlap:
        for col in old:
            if old.at[day, col] != live.at[day, col]:
                changes.append({"week": day, "column": col, "pinned": old.at[day, col],
                                "downloaded": live.at[day, col]})
    pd.DataFrame(changes, columns=["week", "column", "pinned", "downloaded"]).to_csv(
        OUT / f"overlap_revisions_{alias}.csv", index=False)
    extended = pd.concat([old, live.loc[live.index > old.index.max()]]).sort_index()
    cftc.validate(extended)
    extended.to_parquet(RAW / f"cftc_tff_{alias.lower()}.parquet")
    return alias, extended, len(changes)


def market_extension(kind):
    old = prices.load() if kind == "prices" else fred.load()
    dest = RAW / f"{kind}_download.parquet"
    if not dest.exists():
        if kind == "prices":
            fresh = prices.fetch("2026-08-31", "2026-10-28")
        else:
            fresh = fred.fetch(fred.SERIES, "2026-08-31", "2026-10-27")
        fresh.to_parquet(dest)
    fresh = pd.read_parquet(dest)
    if fresh.empty or fresh.index.max() < LAST:
        raise ValueError(f"{kind}: incomplete source endpoint")
    overlap = old.index.intersection(fresh.index)
    revisions = []
    for day in overlap:
        for col in old:
            a, b = old.at[day, col], fresh.at[day, col]
            if not ((pd.isna(a) and pd.isna(b)) or a == b):
                revisions.append({"date": day, "column": col, "pinned": a, "downloaded": b})
    pd.DataFrame(revisions, columns=["date", "column", "pinned", "downloaded"]).to_csv(
        OUT / f"overlap_revisions_{kind}.csv", index=False)
    # Preserve every pinned observation, including missing cells and historical revisions.
    combined = pd.concat([old, fresh.loc[fresh.index > old.index.max()]]).sort_index()
    combined.to_parquet(RAW / f"{kind}_extended.parquet")
    return kind, combined


def feature_frame(panels, price, macrodata):
    pos = panels["UST_10Y"]
    snapshots = pos.index
    s = pos.leveraged_funds_net / pos.open_interest
    f = pd.DataFrame({"d_net_over_oi": s.diff(), "net_over_oi_lag1": s.shift(),
                      "d_net_over_oi_lag1": s.diff().shift(),
                      "d_log_oi": np.log(pos.open_interest).diff()})
    mom = momentum.build(price, snapshots)
    mac = macro.build(macrodata, snapshots)
    bas = basis.build(mom.ret_1w, macrodata, snapshots, mac.dy_10)
    cross = pd.DataFrame(index=snapshots)
    for alias in pf.CURVE_CONTRACTS:
        panel = panels[alias]
        share = (panel.leveraged_funds_net / panel.open_interest).reindex(snapshots)
        tag = alias.lower().replace("ust_", "")
        cross[f"{tag}_net_oi_lag1"] = share.shift()
        cross[f"{tag}_d_net_oi_lag1"] = share.diff().shift()
    f = pd.concat([f, mom, mac, bas, pf.cross_group(pos), cross], axis=1).rename(columns=RENAME)
    f[ALT_TARGET] = pos.leveraged_funds_net.diff() / pos.open_interest.shift()
    f["s_level"] = s
    f["s_level_lag1"] = s.shift()
    f.index.name = "as_of"
    return f


def earliest_maximum(index, gap):
    """Exact maximum cardinality for equal-gap intervals (earliest-finish greedy)."""
    chosen = []
    for day in pd.DatetimeIndex(index).sort_values():
        if not chosen or day - chosen[-1] >= pd.Timedelta(weeks=gap):
            chosen.append(day)
    return pd.DatetimeIndex(chosen)


def uniform_feasible(index, count, gap, seed):
    """Uniform draw over all feasible count-subsets using exact integer DP."""
    idx = pd.DatetimeIndex(index).sort_values()
    nxt = idx.searchsorted(idx + pd.Timedelta(weeks=gap))
    ways = [[0] * (count + 1) for _ in range(len(idx) + 1)]
    for row in ways:
        row[0] = 1
    for i in range(len(idx) - 1, -1, -1):
        for k in range(1, count + 1):
            ways[i][k] = ways[i + 1][k] + ways[nxt[i]][k - 1]
    if not ways[0][count]:
        raise ValueError("infeasible quota")
    rng, i, k, chosen = random.Random(seed), 0, count, []
    while k:
        take = ways[nxt[i]][k - 1]
        if rng.randrange(ways[i][k]) < take:
            chosen.append(idx[i]); k -= 1; i = int(nxt[i])
        else:
            i += 1
    return pd.DatetimeIndex(chosen)


def global_sample(pool, quotas, gap):
    """Feasibility sensitivity: gaps across strata too; fixed date-only objective."""
    pool = pool.sort_values("week").reset_index(drop=True)
    idx = pd.DatetimeIndex(pool.week)
    n = len(pool)
    a = lil_matrix((n + 4, n), dtype=float)
    for i in range(n):
        j = idx.searchsorted(idx[i] + pd.Timedelta(weeks=gap))
        a[i, i:j] = 1
    for j, s in enumerate(("S1", "S2", "S3", "S4")):
        a[n + j, np.flatnonzero(pool.stratum.eq(s))] = 1
    q = np.array([quotas[s] for s in ("S1", "S2", "S3", "S4")])
    lo, hi = np.r_[np.zeros(n), q], np.r_[np.ones(n), q]
    # A deterministic pseudorandom ordering, independent of positions/residuals/responses.
    costs = np.random.default_rng(SEED).uniform(size=n)
    result = milp(costs, integrality=np.ones(n), bounds=Bounds(0, 1),
                  constraints=LinearConstraint(a.tocsr(), lo, hi),
                  options={"time_limit": 45})
    if result.x is None:
        return None, {"status": int(result.status), "message": result.message}
    chosen = pool.loc[result.x > .5].copy()
    assert (chosen.week.sort_values().diff().dropna() >= pd.Timedelta(weeks=gap)).all()
    assert chosen.stratum.value_counts().to_dict() == quotas
    return chosen, {"status": int(result.status), "message": result.message}


def main():
    for d in (RAW, OUT, DOC, EXPORT):
        d.mkdir(parents=True, exist_ok=True)
    preserve_path = DOC / "preservation_before.json"
    if not preserve_path.exists():
        save_json(preserve_path, preserved_files())
    # Record rules before constructing candidate samples. This is a proposal, not approval.
    save_json(DOC / "proposal_rules.json", {
        "date": STAMP, "status": "candidate feasibility only; not frozen",
        "gaps_weeks": [4, 6, 8], "original_gap_scope": "within stratum",
        "stratum_cut": "original pinned negative-net/OI 10th percentile; never recompute",
        "seed": SEED, "selection": "uniform feasible subsets via exact DP; dates/eligibility only",
        "primary_pool_exclusions": [str(x.date()) for x in DEVELOPMENT] + [str(PILOT.date())],
        "B_quotas": "min(10, exact feasible maximum) per original stratum",
        "C_quotas_8": {"S1":13,"S2":2,"S3":13,"S4":12},
        "C_quotas_6": {"S1":13,"S2":3,"S3":12,"S4":12},
        "C_quotas_4": {"S1":12,"S2":4,"S3":12,"S4":12},
        "pilot": "2025-09-02 retained as separate qualitative case, outside inferential totals",
        "global_gap": "additional sensitivity; not the original sampler rule",
        "model": "reconstruct final Aug-04-trained weighted_104 with frozen alpha; no CV/refit on extension",
        "new_dates": "never selected by LLM responses or prediction residuals",
    })
    print("Downloading versioned inputs", flush=True)
    sources = {
        "financial_lf.html": "https://www.cftc.gov/dea/futures/financial_lf.htm",
        "release_schedule.html": "https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm",
        "fut_fin_txt_2026.zip": cftc_archive.ARCHIVE_URL.format(year=2026),
    }
    jobs = {}
    panels, markets, errors, overlap_revisions = {}, {}, {}, {}
    with ThreadPoolExecutor(max_workers=7) as ex:
        for name, url in sources.items():
            jobs[ex.submit(get_bytes, url, name)] = ("source", name)
        for alias in ("UST_10Y", "UST_2Y", "UST_5Y", "UST_30Y"):
            jobs[ex.submit(cftc_panel, alias)] = ("cftc", alias)
        for kind in ("prices", "fred"):
            jobs[ex.submit(market_extension, kind)] = ("market", kind)
        for future, (kind, name) in jobs.items():
            try:
                result = future.result()
                if kind == "cftc":
                    alias, panel, count = result
                    panels[alias] = panel; overlap_revisions[alias] = count
                elif kind == "market":
                    markets[result[0]] = result[1]
                print(kind, name, "OK", flush=True)
            except Exception as exc:
                errors[name] = repr(exc)
                print(kind, name, repr(exc), flush=True)
    save_json(OUT / "download_errors.json", errors)
    if "UST_10Y" not in panels:
        raise RuntimeError("flagship download unavailable; cannot claim dataset update")
    pos = panels["UST_10Y"]
    old = cftc.load("UST_10Y")
    new_idx = pos.index[pos.index > old.index[-1]]
    expected = pd.date_range("2026-09-15", LAST, freq="W-TUE")
    assert new_idx.equals(expected), (new_idx, expected)
    # Reconcile every additional record and every field to the annual official file.
    archive_verified = False
    if (RAW / "fut_fin_txt_2026.zip").exists():
        with zipfile.ZipFile(RAW / "fut_fin_txt_2026.zip") as z:
            archived = pd.read_csv(io.BytesIO(z.read(z.namelist()[0])), low_memory=False)
        archived.columns = archived.columns.str.strip().str.strip('"')
        arch = cftc_archive.to_frame(archived, "043602")
        np.testing.assert_array_equal(pos.loc[new_idx].values, arch.loc[new_idx].values)
        archive_verified = True
    header_verified = False
    if (RAW / "financial_lf.html").exists():
        html = (RAW / "financial_lf.html").read_text()
        assert "October 27, 2026" in html
        match = re.search(r"CFTC Code #043602.*?Open Interest is\s+([\d,]+).*?Positions\s*\n\s*([\d,\s]+)\n", html, re.S)
        if match:
            oi = int(match[1].replace(",", ""))
            nums = [int(x.replace(",", "")) for x in match[2].split()]
            assert oi == pos.loc[LAST, "open_interest"]
            fields = [f"{g}_{leg}" for g in cftc.GROUP_COLUMNS for leg in ("long", "short", "spread")]
            np.testing.assert_array_equal(pos.loc[LAST, fields].values, nums[:12])
            header_verified = True
    oldpred = pd.read_parquet(ROOT / "data/processed/model_v4/weighted_104.parquet")
    pred = oldpred.copy()
    extension_status = {"new_position_rows": len(new_idx), "last_official_as_of": str(LAST.date()),
                        "last_release": "2026-10-30 15:30 America/New_York",
                        "archive_all_new_fields_equal": archive_verified,
                        "latest_text_header_and_positions_equal": header_verified,
                        "2026_overlap_revised_cells": overlap_revisions,
                        "market_errors": errors, "new_ml_rows": 0}
    extension_status["market_overlap_revised_cells"] = {
        kind: len(pd.read_csv(OUT / f"overlap_revisions_{kind}.csv")) for kind in markets}
    if len(panels) == 4 and set(markets) == {"prices", "fred"}:
        f = feature_frame(panels, markets["prices"], markets["fred"])
        orig = base_frame()
        feats = v1_features(orig)
        assert list(f.columns) == list(orig.columns)
        np.testing.assert_allclose(f.loc[orig.index, feats + ["d_net_over_oi"]],
                                   orig[feats + ["d_net_over_oi"]], equal_nan=True, atol=1e-12, rtol=1e-12)
        fitlog = pd.read_csv(ROOT / "reports/model_v4/fits_weighted_104.csv").iloc[-1]
        train = f[feats + ["d_net_over_oi"]].dropna().loc[:fitlog.train_end]
        assert len(train) == fitlog.n_train
        est = RecencyRidge(alpha=float(fitlog.alpha), half_life=104).fit(train[feats], train.d_net_over_oi)
        block = oldpred.loc[oldpred.block_start.eq(pd.Timestamp(fitlog.block_start))]
        np.testing.assert_allclose(est.predict(f.loc[block.index, feats]), block.pred, atol=1e-12, rtol=1e-12)
        assert len(block) + len(new_idx) <= 13  # stay inside last scheduled outer test block
        assert np.isfinite(f.loc[new_idx, feats].to_numpy()).all()
        newpred = pd.DataFrame({"actual": f.loc[new_idx, "d_net_over_oi"],
                                "pred": est.predict(f.loc[new_idx, feats]),
                                "block_start": pd.Timestamp(fitlog.block_start),
                                "train_end": pd.Timestamp(fitlog.train_end)}, index=new_idx)
        pred = pd.concat([oldpred, newpred])
        pred.to_parquet(RAW / "weighted_104_extended.parquet")
        f.to_parquet(RAW / "features_extended.parquet")
        extension_status.update(new_ml_rows=len(newpred), features=len(feats), training_rows=len(train),
                                alpha=float(fitlog.alpha), train_end=fitlog.train_end,
                                historical_features_equal=True, prior_final_block_predictions_equal=True)
        # Record the actual observation date used, separately from its publication date.
        availability = []
        for day in new_idx:
            for code in fred.SERIES:
                src = markets["fred"][code].dropna().loc[:day]
                availability.append({"week": day, "source": code, "observation_date": src.index[-1],
                                     "staleness_days": (day - src.index[-1]).days})
            px = markets["prices"].close.dropna().loc[:day]
            availability.append({"week": day, "source": "ZN=F", "observation_date": px.index[-1],
                                 "staleness_days": (day - px.index[-1]).days})
        pd.DataFrame(availability).to_csv(OUT / "feature_observation_dates.csv", index=False)
    stats = prior_uncertainty(pred)
    assert (stats.loc[new_idx.intersection(stats.index), "n_prior_errors"] >= 52).all()
    assert (stats.loc[stats.band90_halfwidth.notna(), "prior_error_end"] < stats.index[stats.band90_halfwidth.notna()]).all()
    s = pos.leveraged_funds_net / pos.open_interest
    valid = stats.index[stats.band90_halfwidth.notna()]
    arm_c = pd.DataFrame(index=valid)
    arm_c["actual_net_over_oi"] = s.reindex(valid)
    arm_c["expected_net_over_oi"] = s.shift().reindex(valid) + pred.pred.reindex(valid)
    arm_c["predicted_weekly_change"] = pred.pred.reindex(valid)
    arm_c["actual_weekly_change"] = pred.actual.reindex(valid)
    arm_c["residual"] = arm_c.actual_net_over_oi - arm_c.expected_net_over_oi
    arm_c = arm_c.join(stats)
    arm_c["range90_low"] = arm_c.expected_net_over_oi - arm_c.band90_halfwidth
    arm_c["range90_high"] = arm_c.expected_net_over_oi + arm_c.band90_halfwidth
    np.testing.assert_allclose(arm_c.residual, (pred.actual - pred.pred).reindex(valid), atol=1e-12)
    arm_c.to_csv(OUT / "arm_c_available_all_dates.csv", index_label="week")
    original_s = old.leveraged_funds_net / old.open_interest
    cut = float(original_s[original_s < 0].quantile(.1))
    labels = pd.Series("", index=pos.index)
    labels.loc[s > 0] = "S1"
    labels.loc[(s < 0) & (s > cut) & (s.index < "2015-01-01")] = "S2"
    labels.loc[(s < 0) & (s > cut) & (s.index >= "2015-01-01")] = "S3"
    labels.loc[(s <= cut) & (s.index >= "2015-01-01")] = "S4"
    eligibility = pd.DataFrame({"week": pos.index, "stratum": labels.values,
                                "net_over_oi": s.values,
                                "valid_Arm_C": pos.index.isin(stats.index[stats.band90_halfwidth.notna()])})
    eligibility["prior_development_case"] = eligibility.week.isin(DEVELOPMENT)
    eligibility["purposive_case"] = eligibility.week.eq(PILOT)
    eligibility.to_csv(OUT / "all_historical_eligibility.csv", index=False)
    pool = eligibility.loc[eligibility.valid_Arm_C & eligibility.stratum.ne("")]
    pool.to_csv(OUT / "all_eligible_dates.csv", index=False)
    designpool = pool.loc[~pool.prior_development_case & ~pool.purposive_case]
    maxima, witnesses, samples, counts, global_status = [], [], [], [], []
    for gap in (1, 2, 3, 4, 6, 8):
        for name, p in (("all_eligible", pool), ("exclude_development_and_purposive", designpool)):
            for label in ("S1", "S2", "S3", "S4"):
                idx = pd.DatetimeIndex(p.loc[p.stratum.eq(label), "week"])
                witness = earliest_maximum(idx, gap)
                maxima.append({"pool": name, "gap_weeks": gap, "stratum": label,
                               "eligible_weeks": len(idx), "maximum": len(witness)})
                for day in witness:
                    witnesses.append({"pool": name, "gap_weeks": gap, "stratum": label, "week": day})
    mx = pd.DataFrame(maxima)
    mx.to_csv(OUT / "spacing_maxima.csv", index=False)
    pd.DataFrame(witnesses).to_csv(OUT / "maximum_witness_dates.csv", index=False)
    original = pd.read_csv(ROOT / "docs/milestone1/sample.csv", parse_dates=["week"])
    a = original.merge(eligibility[["week", "valid_Arm_C"]], on="week", validate="one_to_one")
    a["option"] = "A_original"; a["gap_weeks"] = 8
    a["arms"] = np.where(a.valid_Arm_C, "A|B|C-bare|C-ann|D", "A|B")
    a["responses_two_models"] = np.where(a.valid_Arm_C, 10, 4)
    samples.append(a)
    for gap in (4, 6, 8):
        caps = mx.loc[mx.pool.eq("exclude_development_and_purposive") & mx.gap_weeks.eq(gap)].set_index("stratum").maximum
        bq = {k: min(10, int(caps[k])) for k in ("S1", "S2", "S3", "S4")}
        cq = {4: {"S1":12,"S2":4,"S3":12,"S4":12},
              6: {"S1":13,"S2":3,"S3":12,"S4":12},
              8: {"S1":13,"S2":2,"S3":13,"S4":12}}[gap]
        for option, quotas in (("B", bq), ("C", cq)):
            pieces = []
            for j, (label, quota) in enumerate(quotas.items()):
                subset = designpool.loc[designpool.stratum.eq(label)]
                selected = uniform_feasible(subset.week, quota, gap, SEED + j)
                pieces.append(subset.loc[subset.week.isin(selected)])
            candidate = pd.concat(pieces).copy()
            candidate["option"] = f"{option}_{gap}w"
            candidate["gap_weeks"] = gap
            candidate["frame"] = "stratified"
            candidate["arms"] = "A|B|C-bare|C-ann|D"
            candidate["responses_two_models"] = 10
            samples.append(candidate)
            glob, status = global_sample(designpool, quotas, gap)
            global_status.append({"option": f"{option}_{gap}w", **status, "feasible": glob is not None})
            if glob is not None:
                glob["option"] = f"{option}_{gap}w_global_sensitivity"
                glob.to_csv(OUT / f"{option}_{gap}w_global_dates.csv", index=False)
    allsamples = pd.concat(samples, ignore_index=True)
    allsamples.to_csv(OUT / "candidate_samples_all_dates.csv", index=False)
    for option, group in allsamples.groupby("option", sort=False):
        group.to_csv(OUT / f"{option}_dates.csv", index=False)
        counts.append({"option": option, "n_stratified": int(group.frame.eq("stratified").sum()),
                       "n_purposive": int(group.frame.eq("purposive").sum()),
                       **{k: int(group.stratum.eq(k).sum()) for k in ("S1","S2","S3","S4")},
                       "complete_stratified": int((group.frame.eq("stratified") & group.valid_Arm_C).sum()),
                       "responses_two_models": int(group.responses_two_models.sum()),
                       "first": group.week.min(), "last": group.week.max()})
    pd.DataFrame(counts).to_csv(OUT / "option_counts.csv", index=False)
    pd.DataFrame(global_status).to_csv(OUT / "global_spacing_sensitivity.csv", index=False)
    new = pos.loc[new_idx].copy()
    new["net_over_oi"] = s.loc[new_idx]
    new["stratum"] = labels.loc[new_idx]
    new = new.join(pred[["actual", "pred", "train_end"]]).join(stats)
    new["scheduled_publication_date"] = new.index + pd.Timedelta(days=3)
    new.to_csv(OUT / "additional_weeks.csv")
    # Descriptive dependence checks do not pretend to measure LLM response dependence.
    diagnostics = [{"gap_weeks": gap, "net_level_autocorrelation": original_s.autocorr(gap),
                    "weekly_change_autocorrelation": original_s.diff().autocorr(gap)}
                   for gap in (1,2,3,4,6,8)]
    pd.DataFrame(diagnostics).to_csv(OUT / "dependence_descriptive.csv", index=False)
    save_json(OUT / "extension_validation.json", extension_status)
    save_json(OUT / "data_manifest.json", {
        "date": STAMP, "official_endpoint": str(LAST.date()), "stratum_cut_frozen": cut,
        "sources": sources, "socrata_dataset": cftc.DATASET,
        "contract_codes": {a: cftc.contract_code(a) for a in panels},
        "scope": "original pinned history + new suffix; not a revised-history vintage",
        "files": {str(p.relative_to(ROOT)): digest(p) for p in sorted(RAW.iterdir()) if p.is_file()},
    })
    before = json.loads(preserve_path.read_text())
    changed = [f for f, h in before.items() if digest(ROOT / f) != h]
    if changed:
        raise RuntimeError(f"preservation violation: {changed}")
    save_json(OUT / "preservation_check.json", {"checked_files": len(before), "changed": changed})
    for p in OUT.glob("*.csv"):
        (EXPORT / p.name).write_bytes(p.read_bytes())
    for name in ("extension_validation.json", "data_manifest.json", "preservation_check.json"):
        (EXPORT / name).write_bytes((OUT / name).read_bytes())
    pos.to_csv(EXPORT / "cftc_tff_043602_append_only_v2026-11-05.csv", index_label="as_of")
    for name in ("cftc_tff_ust_10y.parquet", "weighted_104_extended.parquet"):
        if (RAW / name).exists():
            (EXPORT / name).write_bytes((RAW / name).read_bytes())
    print(json.dumps(extension_status, indent=2, default=str), flush=True)
    print(pd.DataFrame(counts).to_string(index=False), flush=True)
    print(mx.loc[mx.gap_weeks.isin([4,6,8])].to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
