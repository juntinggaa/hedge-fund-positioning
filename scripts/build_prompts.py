"""Generate every experimental prompt from the pinned data.

No number in any prompt is ever typed by a human. This module exists because the
Milestone 1 pilot stimulus was assembled by hand and its figures could not later be
reproduced from the pinned CFTC frame: the leveraged-fund net/OI share was right,
the contract counts were not. A hand-built stimulus is unreproducible by
construction, so the fix is structural rather than a correction.

    python scripts/build_prompts.py --week 2025-09-02 --arm A
    python scripts/build_prompts.py --all > docs/milestone2/prompts.jsonl

Arms, and what each adds. The arms are NOT cumulative: every arm starts from A.
B's mechanism paragraph appears in B only, so B vs C is not a nested comparison
(checked 2026-11-05; an earlier description presented C as "B plus the model").

    A        the CFTC table and the question
    B        A + market-structure mechanism, stated with NO magnitudes
    C-bare   A + model expected position, actual, residual, unlabelled
    C-ann    C-bare + the frozen annotation below
    D        A + a PLACEBO residual: another week's residual, with the expected
             position recomputed so the arithmetic still ties out

`--model-version v2` builds PROPOSED materials from model v2.0
(docs/model_v2/model_card_v2.json); the default v1 reproduces the pilot exactly.

Arm D is the quantitative analogue of the net-long template check. The v1 residual
correlates 0.957 with the raw weekly change, so the real model output carries
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


#: v2 annotation, FROZEN 2026-11-05 as a template: every number is filled from
#: docs/model_v2/model_card_v2.json, and tests/test_model_v2.py checks the filled text
#: against the card. The v1 ANNOTATION above is left byte-for-byte unchanged so the
#: responses already collected under it stay interpretable.
ANNOTATION_V2_TEMPLATE = """\
How to read the model output above (model {model_version}). The model predicts the weekly \
CHANGE in leveraged funds' net position, as a share of open interest, from conditions \
observed in the same week: price returns, realised volatility, yield levels and curve shape, \
equity volatility, a funding-stress measure, the change in open interest, the change in Fed \
Treasury holdings, a quarter-end flag, and the previous week's net positions of all four \
trader categories in this contract and of leveraged funds in the 2-, 5- and 30-year contracts. \
The expected position is last week's actual position plus the predicted change. It is a \
statistical association, not a decomposition by strategy. Specifically:

- The residual is the part of this week's CHANGE the model did not predict, given where \
the position stood last week. It is not the unexplained part of the whole outstanding \
position, not a quantity of basis trading, and not a directional signal. It contains \
misspecification, omitted variables and data error as well as anything informative.
- The model assigns no share of any position to any motive. It cannot: the cash leg of a \
basis trade is not in this dataset, and none of its inputs measures the cash-futures basis.
- Out of sample ({eval_start} to {eval_end}, {eval_n} weeks) the model explains about \
{r2_pct}% of the variance of weekly positioning changes. Its typical error is \
{rmse} percentage points of open interest, and the residual correlates about {corr} with \
the raw weekly change, so most of what you see in the residual is simply the raw change.
- The expected-position range is approximate: in past weeks it contained the actual \
position {coverage_pct}% of the time. A residual inside the range is within the model's \
ordinary error."""


def annotation_v2(card: dict) -> str:
    start, end, n = card["eval_weeks"]
    return ANNOTATION_V2_TEMPLATE.format(
        model_version=card["model_version"], eval_start=start, eval_end=end, eval_n=n,
        r2_pct=f"{card['oos_r2_vs_historical_mean'] * 100:.0f}",
        rmse=f"{card['oos_rmse_pp_of_oi']:.1f}", corr=f"{card['corr_residual_actual_change']:.2f}",
        coverage_pct=f"{card['band90_historical_coverage'] * 100:.0f}")


def model_block_v2(stimuli: pd.DataFrame, week: str, placebo: bool) -> str | None:
    """v2 block. Wording revised 2026-11-05 after the v2 pilot: "larger in size than 4% of
    past residuals" was misread as 96% by 2 of 12 responses, so the line now states both
    directions explicitly ("4% were smaller ... 96% were larger")."""
    row = stimuli[stimuli["week"] == week]
    if row.empty or not bool(row.iloc[0]["has_model_output"]):
        return None
    row = row.iloc[0]
    exp_col, res_col, pct_col = (
        ("placebo_expected_net_over_oi", "placebo_residual", "placebo_residual_abs_pct_vs_prior")
        if placebo else ("expected_net_over_oi", "residual", "residual_abs_pct_vs_prior"))
    exp, res, band = row[exp_col] * 100, row[res_col] * 100, row["band90_halfwidth"] * 100
    return (
        f"Output of a supervised model of leveraged-fund positioning (model {row['model_version']}):\n\n"
        f"- Expected net position this week: {exp:+.2f}% of open interest "
        f"(approximate 90% range based on the model's past errors: {exp - band:+.2f}% to {exp + band:+.2f}%)\n"
        f"- Actual net position this week: {row['actual_net_over_oi'] * 100:+.2f}% of open interest\n"
        f"- Residual (actual minus expected): {res:+.2f}% of open interest. Of the model's past "
        f"out-of-sample residuals, {row[pct_col] * 100:.0f}% were smaller in size than this one and "
        f"{100 - round(row[pct_col] * 100):.0f}% were larger."
    )


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


def build(week: str, arm: str, frame: pd.DataFrame, stimuli: pd.DataFrame,
          model_version: str = "v1", card: dict | None = None) -> str:
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
        if model_version == "v2":
            block = model_block_v2(stimuli, str(stamp.date()), placebo=arm == "D")
        else:
            source = placebo_stimuli(stimuli) if arm == "D" else stimuli
            block = model_block(source, str(stamp.date()))
        if block is None:
            raise ValueError(f"no out-of-sample model output for {week}; arm {arm} cannot run")
        parts += ["", block]
    if arm == "C-ann":
        parts += ["", annotation_v2(card) if model_version == "v2" else ANNOTATION]

    parts += ["", QUESTION]
    return "\n".join(parts)


ARMS = ("A", "B", "C-bare", "C-ann", "D")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week")
    parser.add_argument("--arm", choices=ARMS, default="A")
    parser.add_argument("--all", action="store_true", help="emit every (week, arm) as JSONL")
    parser.add_argument("--model-version", choices=("v1", "v2"), default="v1",
                        help="v1 reproduces the Milestone 2 pilot materials; v2 is PROPOSED")
    args = parser.parse_args()

    frame = cftc.load("UST_10Y")
    card = None
    if args.model_version == "v2":
        stimuli = pd.read_csv(config.REPO_ROOT / "docs/milestone2/arm_c_stimuli_v2.csv")
        card = json.loads((config.REPO_ROOT / "docs/model_v2/model_card_v2.json").read_text())
    else:
        stimuli = pd.read_csv(config.REPO_ROOT / "docs/milestone2/arm_c_stimuli.csv")

    if args.all:
        sample = pd.read_csv(config.REPO_ROOT / "docs/milestone1/sample.csv", parse_dates=["week"])
        for week in sample["week"].dt.strftime("%Y-%m-%d"):
            for arm in ARMS:
                try:
                    text = build(week, arm, frame, stimuli, args.model_version, card)
                except ValueError as exc:
                    print(json.dumps({"week": week, "arm": arm, "skipped": str(exc)}), file=sys.stderr)
                    continue
                print(json.dumps({"week": week, "arm": arm, "prompt": text}))
        return

    if not args.week:
        parser.error("--week is required unless --all is given")
    print(build(args.week, args.arm, frame, stimuli, args.model_version, card))


if __name__ == "__main__":
    main()
