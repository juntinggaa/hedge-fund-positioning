"""Select v2 pilot cases by a FIXED rule and write their prompts.

    python scripts/pilot_v2_select.py

Four case types, each defined numerically BEFORE looking at which weeks qualify.
Pool: weeks with a v2 model output and a band (>= 52 prior errors), EXCLUDING every
main-sample week (docs/milestone1/sample.csv), so the pilot cannot contaminate
the main run.

  a  anticipated large move: |raw| >= 90th pct of |raw|, prediction has the same sign,
     and the residual is inside the approximate 90% range
  b  modest move, surprising: |raw| <= median |raw| and |residual| percentile vs
     prior errors >= 85
  c  ordinary: |residual| percentile <= 25 and |raw| between the 25th and 75th pct
  d  large residual: outside the range and |residual| percentile >= 97

Pick: within each type, the two most recent qualifying weeks, at least 13 weeks
apart, not already picked. Arms: C-bare and C-ann (model v2), neutral question.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.ingest import cftc

ROOT = config.REPO_ROOT
sys.path.insert(0, str(ROOT / "scripts"))
import build_prompts as bp  # noqa: E402
from build_stimuli_v2 import MIN_PRIOR, Z90  # noqa: E402

OUT = ROOT / "docs/milestone2/pilot_v2"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    card = json.loads((ROOT / "docs/model_v2/model_card_v2.json").read_text())
    pred = pd.read_parquet(ROOT / f"data/processed/model_v2/{card['model_id']}.parquet")
    pos = cftc.load("UST_10Y")
    s = pos["leveraged_funds_net"] / pos["open_interest"]
    err = (pred["actual"] - pred["pred"]).to_numpy()

    rows = []
    for i in range(MIN_PRIOR, len(err)):
        w = pred.index[i]
        prior = np.abs(err[:i])
        band = Z90 * np.sqrt(np.mean(err[:i] ** 2))
        rows.append({"week": w, "raw": pred["actual"].iloc[i], "pred": pred["pred"].iloc[i],
                     "resid": err[i], "band": band, "pct": float((prior < abs(err[i])).mean())})
    d = pd.DataFrame(rows).set_index("week")
    sample = set(pd.read_csv(ROOT / "docs/milestone1/sample.csv", parse_dates=["week"])["week"])
    d = d[~d.index.isin(sample)]
    a_raw = d["raw"].abs()
    q = a_raw.quantile([0.25, 0.5, 0.75, 0.9])
    rules = {
        "a_anticipated_large": (a_raw >= q[0.9]) & (np.sign(d["pred"]) == np.sign(d["raw"]))
                               & (d["resid"].abs() <= d["band"]),
        "b_modest_surprising": (a_raw <= q[0.5]) & (d["pct"] >= 0.85),
        "c_ordinary": (d["pct"] <= 0.25) & (a_raw >= q[0.25]) & (a_raw <= q[0.75]),
        "d_large_residual": (d["resid"].abs() > d["band"]) & (d["pct"] >= 0.97),
    }
    picked, chosen = set(), []
    for kind, mask in rules.items():
        got = []
        for w in sorted(d.index[mask], reverse=True):
            if w in picked or any(abs((w - g).days) < 91 for g in got):
                continue
            got.append(w)
            if len(got) == 2:
                break
        print(f"{kind}: {int(mask.sum())} qualify -> {[str(g.date()) for g in got]}")
        picked |= set(got)
        chosen += [(kind, g) for g in got]

    stim = []
    for kind, w in chosen:
        r = d.loc[w]
        stim.append({"case_type": kind, "week": str(w.date()), "model_version": card["model_version"],
                     "has_model_output": True,
                     "actual_net_over_oi": float(s[w]),
                     "expected_net_over_oi": float(s.shift(1)[w] + r["pred"]),
                     "residual": float(r["resid"]), "band90_halfwidth": float(r["band"]),
                     "residual_abs_pct_vs_prior": r["pct"], "raw_change": float(r["raw"]),
                     "prev_net_over_oi": float(s.shift(1)[w])})
    stim = pd.DataFrame(stim)
    stim.to_csv(OUT / "cases.csv", index=False)

    rng = np.random.default_rng(20261105)
    jobs = [(c["week"], arm) for c in stim.to_dict("records") for arm in ("C-bare", "C-ann")]
    order = rng.permutation(len(jobs))
    with open(OUT / "prompts.jsonl", "w") as fh:
        for k, j in enumerate(order):
            week, arm = jobs[j]
            text = bp.build(week, arm, pos, stim, "v2", card)
            fh.write(json.dumps({"run_id": f"P{k + 1:02d}", "week": week, "arm": arm,
                                 "case_type": stim.set_index("week").loc[week, "case_type"],
                                 "prompt": text}) + "\n")
    print(stim.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
