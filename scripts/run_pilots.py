"""Run the Milestone 1 pilot cases and record verbatim output.

    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/run_pilots.py --arms A B --replicates 3

Writes docs/milestone1/pilot_results.md with model id, parameters, timestamp and the
untouched response text for every run.

REPRODUCIBILITY NOTE. Current Anthropic frontier models (Opus 5, Sonnet 5, Fable 5,
Opus 4.7/4.8) removed `temperature`, `top_p` and `top_k` -- sending them returns a 400.
You therefore cannot pin sampling to make runs deterministic. The defensible response is
to run several replicates per cell and report the variation, rather than claiming a
fixed-temperature single draw. `--replicates` exists for that reason; keep it >= 3.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import anthropic

MODEL = "claude-opus-5"
MAX_TOKENS = 2000
EFFORT = "medium"

POSITIONING = """Open interest: 5,442,559
Dealer — long 1,067,637 / short 1,268,022 / spreading 296,320
Asset manager — long 2,527,853 / short 425,264 / spreading 200,509
Leveraged funds — long 618,878 / short 3,259,142 / spreading 526,570"""

QUESTION = "What does this positioning suggest about the Treasury market?"

BASIS_CONTEXT = (
    "Note: leveraged funds may hold Treasury futures shorts as part of cash–futures "
    "basis trades, holding the underlying Treasury security simultaneously. Such "
    "positions express an arbitrage rather than a directional view."
)

ARMS = {
    "A": "Below is CFTC Traders in Financial Futures data for 10-Year U.S. Treasury Note "
         f"futures, week ending 2 September 2025.\n\n{POSITIONING}\n\n{QUESTION}",
    "B": "Below is CFTC Traders in Financial Futures data for 10-Year U.S. Treasury Note "
         f"futures, week ending 2 September 2025.\n\n{POSITIONING}\n\n{BASIS_CONTEXT}\n\n{QUESTION}",
}

OUT = Path(__file__).resolve().parents[1] / "docs" / "milestone1" / "pilot_results.md"


def run_one(client: anthropic.Anthropic, prompt: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        output_config={"effort": EFFORT},
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    return {
        "model": response.model,
        "stop_reason": response.stop_reason,
        "request_id": response._request_id,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "text": text,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=["A", "B"], choices=sorted(ARMS))
    ap.add_argument("--replicates", type=int, default=3,
                    help="runs per arm; >=3, since sampling cannot be pinned")
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("set ANTHROPIC_API_KEY first")
    if args.replicates < 3:
        print("warning: fewer than 3 replicates cannot show run-to-run variation")

    client = anthropic.Anthropic()
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        "# Pilot results",
        "",
        f"Run {stamp} · model `{MODEL}` · effort `{EFFORT}` · max_tokens {MAX_TOKENS} · "
        f"{args.replicates} replicates per arm.",
        "",
        "Sampling parameters are not configurable on this model, so replicates are reported "
        "instead of a single pinned draw. Responses are verbatim and unedited.",
        "",
    ]

    for arm in args.arms:
        lines += [f"## Arm {arm}", "", "<details><summary>Prompt</summary>", "",
                  "```", ARMS[arm], "```", "", "</details>", ""]
        for i in range(1, args.replicates + 1):
            result = run_one(client, ARMS[arm])
            print(f"arm {arm} run {i}: {result['output_tokens']} output tokens")
            lines += [
                f"### Arm {arm}, run {i}",
                "",
                f"`{result['model']}` · stop `{result['stop_reason']}` · "
                f"{result['input_tokens']} in / {result['output_tokens']} out · "
                f"request `{result['request_id']}`",
                "",
                result["text"],
                "",
                "| Score | Numerical | Directional | Alternative raised | Calibration |",
                "|---|---|---|---|---|",
                "| scorer 1 | | | | |",
                "| scorer 2 | | | | |",
                "",
            ]

    OUT.write_text("\n".join(lines) + "\n")
    print(f"\nwrote {OUT}")
    print("Now score each response against the rubric in docs/milestone1/proposal.md §4.")


if __name__ == "__main__":
    main()
