"""Draw the stratified 40-week sample for the Milestone 1 investigation.

Deterministic: same seeds give the same weeks, so the appendix table is reproducible.
Strata span the interpretive space rather than the calendar, because a random draw
would over-represent ordinary weeks. Draws are spaced >= 8 weeks apart because
positioning is strongly autocorrelated and adjacent weeks are near-duplicates.

    python scripts/draw_sample.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from hfpos import config
from hfpos.ingest import cftc

BASE_SEED = 20260918
N_PER_STRATUM = 10
MIN_GAP_WEEKS = 8
EXTREME_QUANTILE = 0.10


def draw(index: pd.DatetimeIndex, n: int, seed: int, gap_weeks: int = MIN_GAP_WEEKS):
    """Randomly draw `n` dates at least `gap_weeks` apart."""
    pool = list(pd.DatetimeIndex(index).sort_values())
    rng = np.random.default_rng(seed)
    chosen: list[pd.Timestamp] = []
    for i in rng.permutation(len(pool)):
        cand = pd.Timestamp(pool[i])
        if all(abs((cand - c).days) >= gap_weeks * 7 for c in chosen):
            chosen.append(cand)
        if len(chosen) == n:
            break
    return sorted(chosen)


def strata(frame: pd.DataFrame) -> dict[str, pd.Series]:
    net_oi = frame["leveraged_funds_net"] / frame["open_interest"]
    pre2015 = net_oi.index < pd.Timestamp("2015-01-01")
    cut = net_oi[net_oi < 0].quantile(EXTREME_QUANTILE)
    moderate = (net_oi < 0) & (net_oi > cut)
    return {
        "S1 LF net long": net_oi > 0,
        "S2 moderate short, pre-2015": moderate & pre2015,
        "S3 moderate short, 2015+": moderate & ~pre2015,
        "S4 extreme short, 2015+": (net_oi <= cut) & ~pre2015,
    }


#: Chosen deliberately, NOT drawn — they probe specific behaviours and are analysed
#: qualitatively. Kept separate from the stratified sample, which estimates rates.
PURPOSIVE = {
    "2025-09-02": "most negative week in the full sample (-48.5% of OI); the pilot case",
}


def main() -> None:
    frame = cftc.load("UST_10Y")
    net_oi = frame["leveraged_funds_net"] / frame["open_interest"]
    cut = net_oi[net_oi < 0].quantile(EXTREME_QUANTILE)
    print(f"extreme-short threshold (net/OI): {cut:.3f}\n")

    rows = []
    for i, (name, mask) in enumerate(strata(frame).items()):
        picks = draw(frame.index[mask], N_PER_STRATUM, BASE_SEED + i)
        print(f"{name} — pool {int(mask.sum())}, drawn {len(picks)}")
        print("  " + ", ".join(f"{p.date()} ({net_oi[p]:+.3f})" for p in picks) + "\n")
        for p in picks:
            rows.append({"frame": "stratified", "stratum": name.split()[0],
                         "stratum_label": name, "pool": int(mask.sum()),
                         "week": p.date(), "net_over_oi": round(float(net_oi[p]), 4),
                         "note": ""})

    for day, why in PURPOSIVE.items():
        ts = pd.Timestamp(day)
        rows.append({"frame": "purposive", "stratum": "P", "stratum_label": "purposive",
                     "pool": "", "week": ts.date(),
                     "net_over_oi": round(float(net_oi[ts]), 4), "note": why})
        print(f"purposive — {ts.date()} ({net_oi[ts]:+.3f}): {why}")

    out = config.REPO_ROOT / "docs" / "milestone1" / "sample.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"\nwrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
