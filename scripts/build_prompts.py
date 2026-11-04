"""Generate every experimental prompt from the pinned data.

No number in any prompt is ever typed by a human. This module exists because the
Milestone 1 pilot stimulus was assembled by hand and its figures could not later be
reproduced from the pinned CFTC frame: the leveraged-fund net/OI share was right,
the contract counts were not. A hand-built stimulus is unreproducible by
construction, so the fix is structural rather than a correction.

    python scripts/build_prompts.py --week 2025-09-02 --arm A
    python scripts/build_prompts.py --all > docs/milestone2/prompts.jsonl

Arms, and what each adds:

    A        the CFTC table and the question
    B        + market-structure mechanism, stated with NO magnitudes
    C-bare   + model expected position, actual, residual, unlabelled
    C-ann    + the frozen annotation below
    D        + a PLACEBO residual: another week's residual, with the expected
             position recomputed so the arithmetic still ties out

Arm D is the quantitative analogue of the net-long template check. The residual
correlates 0.977 with the raw weekly change, so the real model output carries
almost no information the table does not already contain. If responses causalise
the placebo at the same rate as the real residual, the causalisation is driven by
the FORM of a model output rather than its content, and no improvement to the
model would change it. The placebo is undetectable by inspection: real residuals
span -5.21% to +4.03% of open interest, so any drawn value is plausible anywhere.

The arm B paragraph deliberately contains no proportion. If it said how much of a
typical short is basis-related it would hand over the very claim the primary
outcome measures, and the comparison against the C arms would be confounded.
"""

from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from hfpos import config
from hfpos.ingest import cftc

GROUPS = [
    ("dealer", "Dealer / Intermediary"),
    ("asset_manager", "Asset Manager / Institutional"),
    ("leveraged_funds", "Leveraged Funds"),
    ("other_reportable", "Other Reportable"),
]

QUESTION = "What does this positioning suggest about the Treasury market?"

#: Seed for the arm D placebo draw. Fixed, so the placebo is reproducible.
PLACEBO_SEED = 20261104

MECHANISM = """\
Context you may find relevant: leveraged funds sometimes hold short positions in Treasury \
futures as one leg of a cash-futures basis trade, in which the fund buys the underlying \
Treasury security, finances it in the repo market, and sells the corresponding futures \
contract. A position held for that reason expresses a relative-value view about the spread \
between the cash and futures markets rather than a directional view about the level of \
yields. Asset managers may likewise hold futures for duration management, benchmark \
replication or liability hedging rather than as a discretionary forecast."""

#: FROZEN 2026-11-04. Changing this text invalidates every C-ann response collected
#: under it. Written as statements about what the statistic is, not as instructions
#: about how to answer -- it is still an intervention on the prompt, and the report
#: says so.
ANNOTATION = """\
How to read the model output above. The model predicts the weekly CHANGE in net \
positioning from market conditions observed in the same week: price returns, realised \
volatility, yield levels and curve shape, the futures-cash spread, a funding-stress \
measure, open-interest change, and the previous week's position. It is a statistical \
association, not a decomposition by strategy. Specifically:

- The residual is the part of this week's positioning change the model did not predict. It \
is not a quantity of basis trading, and it is not a directional signal. It contains \
misspecification, omitted variables and data error as well as anything informative.
- The model assigns no share of any position to any motive. It cannot: the cash leg of a \
basis trade is not in this dataset.
- Out of sample the model explains about 5% of the variance of weekly positioning changes, \
so the residual correlates about 0.98 with the raw weekly change. Most of what you see in \
the residual is simply the raw change."""


def positioning_table(row: pd.Series) -> str:
    oi = float(row["open_interest"])
    lines = [
        f"Open interest (all contracts): {int(oi):,}",
        "",
        "| Trader category | Long | Short | Spreading | Net | Net as % of OI |",
        "|---|---|---|---|---|---|",
    ]
    for key, label in GROUPS:
        net = float(row[f"{key}_net"])
        lines.append(
            f"| {label} | {int(row[f'{key}_long']):,} | {int(row[f'{key}_short']):,} | "
            f"{int(row[f'{key}_spread']):,} | {int(net):,} | {net / oi * 100:+.2f}% |"
        )
    return "\n".join(lines)


def placebo_stimuli(stimuli: pd.DataFrame, seed: int = PLACEBO_SEED) -> pd.DataFrame:
    """Reassign residuals across weeks, keeping actual - residual = expected.

    The actual position stays true to the data; only the model's claimed
    expectation moves. A response cannot detect the swap by arithmetic.
    """
    import numpy as np

    out = stimuli.copy()
    covered = out["has_model_output"].fillna(False).to_numpy(dtype=bool)
    residuals = out.loc[covered, "residual"].to_numpy()
    shuffled = np.random.default_rng(seed).permutation(residuals)
    out.loc[covered, "residual"] = shuffled
    out.loc[covered, "expected_net_over_oi"] = (
        out.loc[covered, "actual_net_over_oi"].to_numpy() - shuffled
    )
    return out


def model_block(stimuli: pd.DataFrame, week: str) -> str | None:
    row = stimuli[stimuli["week"] == week]
    if row.empty or not bool(row.iloc[0]["has_model_output"]):
        return None
    row = row.iloc[0]
    return (
        "Output of a supervised model of leveraged-fund positioning:\n\n"
        f"- Expected net position this week: {row['expected_net_over_oi'] * 100:+.2f}% of open interest\n"
        f"- Actual net position this week: {row['actual_net_over_oi'] * 100:+.2f}% of open interest\n"
        f"- Residual (actual minus expected): {row['residual'] * 100:+.2f}% of open interest"
    )


def build(week: str, arm: str, frame: pd.DataFrame, stimuli: pd.DataFrame) -> str:
    stamp = pd.Timestamp(week)
    if stamp not in frame.index:
        raise ValueError(f"{week} is not a CFTC snapshot date")
    row = frame.loc[stamp]

    header = (
        "Below is the CFTC Traders in Financial Futures report (futures-only) for 10-Year "
        f"U.S. Treasury Note futures, contract market code 043602, for the week ending "
        f"{stamp:%-d %B %Y}. All figures are numbers of contracts."
    )
    parts = [header, "", positioning_table(row)]

    if arm in ("B",):
        parts += ["", MECHANISM]
    if arm in ("C-bare", "C-ann", "D"):
        source = placebo_stimuli(stimuli) if arm == "D" else stimuli
        block = model_block(source, str(stamp.date()))
        if block is None:
            raise ValueError(f"no out-of-sample model output for {week}; arm {arm} cannot run")
        parts += ["", block]
    if arm == "C-ann":
        parts += ["", ANNOTATION]

    parts += ["", QUESTION]
    return "\n".join(parts)


ARMS = ("A", "B", "C-bare", "C-ann", "D")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week")
    parser.add_argument("--arm", choices=ARMS, default="A")
    parser.add_argument("--all", action="store_true", help="emit every (week, arm) as JSONL")
    args = parser.parse_args()

    frame = cftc.load("UST_10Y")
    stimuli = pd.read_csv(config.REPO_ROOT / "docs/milestone2/arm_c_stimuli.csv")

    if args.all:
        sample = pd.read_csv(config.REPO_ROOT / "docs/milestone1/sample.csv", parse_dates=["week"])
        for week in sample["week"].dt.strftime("%Y-%m-%d"):
            for arm in ARMS:
                try:
                    text = build(week, arm, frame, stimuli)
                except ValueError as exc:
                    print(json.dumps({"week": week, "arm": arm, "skipped": str(exc)}), file=sys.stderr)
                    continue
                print(json.dumps({"week": week, "arm": arm, "prompt": text}))
        return

    if not args.week:
        parser.error("--week is required unless --all is given")
    print(build(args.week, args.arm, frame, stimuli))


if __name__ == "__main__":
    main()
