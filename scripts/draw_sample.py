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


def main() -> None:
    frame = cftc.load("UST_10Y")
    net_oi = frame["leveraged_funds_net"] / frame["open_interest"]
    cut = net_oi[net_oi < 0].quantile(EXTREME_QUANTILE)
    print(f"extreme-short threshold (net/OI): {cut:.3f}\n")
    for i, (name, mask) in enumerate(strata(frame).items()):
        picks = draw(frame.index[mask], N_PER_STRATUM, BASE_SEED + i)
        print(f"{name} — pool {int(mask.sum())}, drawn {len(picks)}")
        print("  " + ", ".join(f"{p.date()} ({net_oi[p]:+.3f})" for p in picks) + "\n")


if __name__ == "__main__":
    main()
