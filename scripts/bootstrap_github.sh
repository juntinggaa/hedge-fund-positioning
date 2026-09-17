#!/usr/bin/env bash
# Creates the repo, labels, milestones and issues, and files every issue onto
# github.com/users/juntinggaa/projects/1
#
# Prerequisites:
#   brew install gh
#   gh auth login
#   gh auth refresh -s project,read:project    # the project scope is NOT granted by default
#
# Usage:  bash scripts/bootstrap_github.sh [repo-name]

set -euo pipefail

OWNER="juntinggaa"
PROJECT=1
REPO="${1:-treasury-positioning}"
SLUG="$OWNER/$REPO"

command -v gh >/dev/null || { echo "gh not installed: brew install gh"; exit 1; }
gh auth status >/dev/null || { echo "run: gh auth login"; exit 1; }

echo "==> repo"
gh repo view "$SLUG" >/dev/null 2>&1 || gh repo create "$SLUG" --private \
  --description "Unusual institutional positioning and U.S. Treasury futures"

echo "==> labels"
while IFS='|' read -r name color; do
  gh label create "$name" --color "$color" --repo "$SLUG" --force >/dev/null
done <<'LABELS'
data|0E8A16
stage-0|C2E0C6
stage-1|1D76DB
stage-2|5319E7
inference|B60205
writing|FBCA04
gate|D93F0B
infra|BFDADC
LABELS

echo "==> milestones"
for m in "W1-2 Scoping and data" "W3-5 Stage 1" "W6-7 Stage 2 and inference" "W8-10 Extensions and write-up"; do
  gh api -X POST "repos/$SLUG/milestones" -f title="$m" >/dev/null 2>&1 || true
done

echo "==> issues"
create () {   # create <labels> <milestone> <title> <body>
  url=$(gh issue create --repo "$SLUG" --title "$3" --body "$4" \
        --label "$1" --milestone "$2" 2>/dev/null) || {
          echo "   ! failed: $3"; return 0; }
  echo "   $url"
  gh project item-add "$PROJECT" --owner "$OWNER" --url "$url" >/dev/null 2>&1 \
    || echo "     (board add failed - run: gh auth refresh -s project)"
}

M1="W1-2 Scoping and data"; M2="W3-5 Stage 1"
M3="W6-7 Stage 2 and inference"; M4="W8-10 Extensions and write-up"

create "infra"     "$M1" "Freeze the pre-registered test plan in README" \
"Copy section 3 of docs/PROJECT_PLAN.md into README.md verbatim and commit it before any Stage-2 code exists. One primary test: leveraged-fund ML surprise -> 1-week 10Y return, augmented vs baseline, Clark-West, 5%. Everything else secondary and multiplicity-adjusted. Do not edit this section later."

create "infra"     "$M1" "Supervisor sign-off on null-safe framing" \
"Get written confirmation that a null result on H1 is acceptable, given the three deliverables in section 4 of the plan (decomposition, honest effect sizes, method comparison). Ask in week 1, not week 9. Also resolve: deadline, expected output format, access to swaption vol or CTD basket data."

create "data"      "$M1" "Ingest CFTC Traders in Financial Futures" \
"Pull the futures-only annual archives from cftc.gov. Parse Dealer / Asset Manager / Leveraged Funds / Other, long + short + spreading, plus open interest. VERIFY contract market codes against the report header - do not trust codes copied from a blog. Check CFTC release notes for classification changes that would put a step change in the series."

create "data"      "$M1" "Ingest Treasury futures prices and settle the roll" \
"CME settlement preferred, Yahoo ZN=F acceptable for a prototype. ZN=F is a stitched front-month series with discontinuities at each quarterly roll - naive weekly returns across a roll boundary inject a spurious jump. Either back-adjust or chain within-contract returns. Decide, document the decision in docs/, and add a plot showing the roll dates are clean."

create "data"      "$M1" "Ingest FRED series" \
"DGS2 DGS5 DGS10 DGS30, DFF, IORB, SOFR, BGCR, TGCR, VIXCLS, plus optional CPIAUCSL UNRATE T10Y2Y. Note MOVE is proprietary and NOT on FRED - plan on realized vol computed from futures returns instead. Watch release-date vs reference-date alignment on the macro series."

create "data"      "$M1" "Build the release-timing calendar" \
"TFF positions are as of Tuesday close, published Friday afternoon. Build both return windows: information-content (Tuesday close start, not tradable) and tradable (post-Friday start). These must never be mixed. Every downstream test declares which one it uses."

create "data"      "$M2" "Build the basis proxy (highest-risk item)" \
"The whole 'we removed basis trading' claim rests on this. Fallback ladder, best first: (1) CTD implied repo vs GC repo - needs deliverable basket and conversion factors, this is real work; (2) futures-implied yield vs cash 10Y; (3) swap spreads; (4) SOFR-IORB. SOFR starts 2018 so pre-2018 needs a fallback. Also: the basis trade was small before ~2015, so 'removing basis' means different things across the sample - document this. If you land on the weak end of the ladder, downgrade the claim to 'conditions favouring basis trading'."

create "stage-0"   "$M2" "Stage 0: lead-lag and VAR" \
"Do positions lead or lag returns? If positions purely follow returns (Sanders-Irwin-Merrin), the Stage-1 feature set MUST include lagged returns or the 'surprise' is just momentum wearing a hat. Write up before building Stage 1."

create "stage-1"   "$M2" "Feature pipeline" \
"Lagged returns 1/4/12w, realized vol, yield levels and changes, 10Y-2Y slope, curvature, SOFR-IORB, basis proxy, delta-OI, lagged own position level and change, VIX, roll-week dummy, FOMC-week dummy. Everything reproducible from raw with one make target."

create "stage-1"   "$M2" "Expanding-window walk-forward harness" \
"Minimum 260-week training block, refit every 13 weeks. Hyperparameter tuning on an inner time-series split INSIDE the training window only. Feature scaling fitted inside the loop. No exceptions - this is where look-ahead bias gets in."

create "stage-1"   "$M2" "Stage 1 models: Ridge, Lasso, XGBoost" \
"Target is delta(Net/OI), not raw net contracts - open interest grows by an order of magnitude over the sample. Report OOS R-squared for each model. With ~1000 obs and 20-40 features the linear model may win; if it does, report it as a finding about the data rather than hiding it."

create "stage-1"   "$M2" "Leakage audit + regression test" \
"Add a test under tests/ that fails if any future information reaches the training fold. At minimum: shuffle-the-target sanity check, and an assertion that scaler/tuning artifacts are refit per fold."

create "gate"      "$M2" "WEEK-5 GATE: is the decomposition real?" \
"Blocking. Report two numbers before any Stage-2 work: (1) Stage-1 out-of-sample R-squared; (2) corr(residual, raw delta(Net/OI)). If that correlation is above ~0.9 the strategy removal is cosmetic and the project is the old COT regression with extra steps - stop and rethink scope now. Both numbers go in the main text of the paper, not an appendix. Someone will compute them otherwise."

create "stage-2"   "$M3" "Stage 2 primary test" \
"r[t+h] = a + b*surprise + c'X + e. Baseline X only vs augmented X + surprise. Compare on out-of-sample R-squared (Campbell-Thompson) and Clark-West for nested models - NOT in-sample t-stats. One number, pre-registered, 1-week horizon, 10Y, leveraged funds. Two-sided: unusual shorting preceding rising prices is crowded-positioning/unwind and is an equally real finding."

create "stage-2"   "$M3" "Benchmark the four definitions of 'unusual'" \
"Identical Stage-2 pipeline for: (1) raw delta(Net/OI); (2) 52-week z-score of Net/OI - the classic COT index; (3) Ridge residual; (4) XGBoost residual. If (3) and (4) do not beat (2), the machine learning contributed nothing and the paper says so. This is the ML claim of the project."

create "inference" "$M3" "Block bootstrap the full two-stage pipeline" \
"The Stage-2 regressor is estimated, so ordinary standard errors are wrong (Pagan 1984 generated regressors) and there is no analytic fix with an ML first stage. Stationary bootstrap, mean block ~13 weeks, 1000 replications, resampling the WHOLE pipeline including Stage-1 refits. Budget real compute time. This is the most likely point of attack in a viva."

create "inference" "$M3" "Overlapping-returns correction" \
"2- and 4-week horizons overlap. Newey-West with lag >= h-1, or Hodrick standard errors. State which and why."

create "inference" "$M3" "Multiplicity adjustment" \
"Primary test unadjusted. All secondary tests get Romano-Wolf or Benjamini-Hochberg, with the family size stated in the paper. Roughly 3 groups x 4 horizons x 4 maturities is ~48 tests - at 5% you expect two or three false positives by construction."

create "stage-2"   "$M4" "Secondary: volatility and stress outcomes (H3)" \
"Positioning-to-volatility links are empirically stronger than positioning-to-direction. Realized vol from futures returns as the outcome. This is the main insurance against a null on H1."

create "stage-2"   "$M4" "Secondary: tails, maturities, regime (H4)" \
"Top/bottom decile of the surprise. 2Y/5Y/30Y, level vs slope. High-volatility interaction dummy - NOT a full HMM, which leaves ~150 observations per regime."

create "stage-2"   "$M4" "Economic significance test" \
"Map the surprise to a long/short 10Y position using the TRADABLE post-Friday timing. Sharpe, turnover, max drawdown, gross and net. ZN bid-ask is typically one tick (1/64 point, ~\$15.63/contract) - small, but state the assumption."

create "writing"   "$M4" "Decomposition figure" \
"How the drivers of leveraged-fund Treasury positioning shift 2006-2026: GFC, ZIRP, March 2020, 2022 hiking, 2023-25 basis build-up. This is a deliverable in its own right and does not depend on Stage 2 being significant."

create "writing"   "$M4" "Subsample stability" \
"The relationship is almost certainly unstable across regimes. Report subsample splits as a finding, not as a robustness footnote."

create "writing"   "$M4" "Write-up and reproducibility" \
"Every number in the paper comes from a make target. Notebooks are for looking, src/ is for results. README carries the frozen pre-registration."

echo
echo "Done. Board: https://github.com/users/$OWNER/projects/$PROJECT/views/1"
