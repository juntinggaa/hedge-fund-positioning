# NST2046 Milestone 2: evidence for "Where Does the Evidence End?"

Group: Lip Jun Ting, Tia Elizabeth Ansari, Upadhye Neeti Rahul, Chua Jun Yu Xavier.
This repository holds the data, prompts, replies, codes and scripts behind the Milestone 2 report.

| What | Where |
|---|---|
| Report draft (Markdown) and appendix logs | [`docs/report/`](docs/report/) |
| Frozen prompts (180) and their hashes | [`docs/main_v1_3/prompts/`](docs/main_v1_3/prompts/), [`docs/main_v1_3/manifest_v1.3.json`](docs/main_v1_3/manifest_v1.3.json) |
| Collected replies, by product | [`docs/main_v1_3/responses/`](docs/main_v1_3/responses/) |
| Gemini high-effort check (16 replies) | [`docs/main_v1_3/effort_check_GEM_high/`](docs/main_v1_3/effort_check_GEM_high/) |
| Codebook v2.3 | [`docs/main_v1/CODEBOOK_v2_3.md`](docs/main_v1/CODEBOOK_v2_3.md) |
| Masked coding packets and both machine coders' output | [`docs/coding_main_v1_3/`](docs/coding_main_v1_3/) |
| Result tables and per-reply final codes | [`docs/coding_main_v1_3/RESULTS.md`](docs/coding_main_v1_3/RESULTS.md), [`FINAL_CODES.csv`](docs/coding_main_v1_3/FINAL_CODES.csv) |
| Human coding sheets, scoring and unresolved disputes | [`docs/coding_main_v1_3/human/`](docs/coding_main_v1_3/human/) |
| Arm C model (v4), annotation and fit report | [`docs/model_v4/`](docs/model_v4/) |
| Amendments, in order | `docs/main_v1_2/AMENDMENT_main_v1_2.md`, `docs/main_v1_3/AMENDMENT_main_v1_3.md`, `docs/main_v1/AMENDMENT_2026-11-06_CODEBOOK_v2_3.md`, `docs/main_v1_3/AMENDMENT_2026-11-07_GEMINI_EFFORT.md` |
| Scripts (assemble, build packets, code, score, analyse) | [`scripts/`](scripts/) (`*_v1_3.py`) |

Reproduce the result tables: `python scripts/analyze_main_v1_3.py --human docs/coding_main_v1_3/human/RESOLVED.csv`.
Files ending `_PRIVATE.csv` are the unmasking keys, used only after coding was finished.

The original Stage-1 positioning project (Milestone 1 and earlier) follows below.

---

# Unusual Institutional Positioning and U.S. Treasury Futures

Full scope, methods, risks and milestones: [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md)

## Research question

> After removing the component of leveraged-fund Treasury futures positioning explained by
> basis-trade conditions, momentum, and macro-financial state, does the residual contain
> incremental out-of-sample information about Treasury futures returns and volatility — and
> does a machine-learned definition of "unusual" outperform a simple positioning z-score?

## Pre-registration — FROZEN

Committed before any Stage-2 code existed. Do not edit.

**Primary test.** Leveraged-fund ML surprise → 1-week-ahead 10Y Treasury futures return.
Augmented model vs. baseline. Clark–West test for nested out-of-sample forecast comparison.
Threshold 5%. **Two-sided.**

**Secondary, exploratory, multiplicity-adjusted.** Horizons 2w/4w · dealers and asset managers ·
2Y/5Y/30Y, level vs. slope · realized volatility · high-volatility interaction · surprise tails.

## Hypotheses

| # | Hypothesis |
|---|---|
| H1 | The leveraged-fund positioning surprise has incremental predictive content for 1-week 10Y returns beyond a macro/market baseline (two-sided) |
| H2 | The ML surprise outperforms a 52-week z-score of net positioning |
| H3 | Predictive content is stronger for volatility than for direction |
| H4 | Predictive content concentrates in the tails of the surprise distribution |

## The two diagnostics that decide whether this project has a thesis

Reported in the main text, week 5, before Stage 2:

1. Stage-1 out-of-sample R²
2. `corr(residual, raw Δ(Net/OI))` — above ~0.9 and the decomposition is cosmetic

## Deliverables that do not depend on a significant result

1. Decomposition of leveraged-fund positioning drivers, 2006–2026
2. Honest effect sizes with bootstrap intervals
3. ML surprise vs. z-score vs. raw, identical test windows

## Setup

```bash
bash scripts/bootstrap_github.sh    # creates repo, labels, milestones, issues, fills the board
```

## Repo layout

```
src/hfpos/
  config.py      config.yaml loader
  timing.py      information vs tradable return windows  (real, tested)
  ingest/        cftc.py  prices.py  fred.py
  features/      basis.py  momentum.py  macro.py  build.py
  stage0/        leadlag.py
  stage1/        walkforward.py (real, tested)  models.py  run.py
  stage2/        predict.py  inference.py
  eval/          metrics.py  bootstrap.py  plots.py
tests/           leakage and release-timing guards
```

Notebooks are for looking, `src/` is for results. Every number in the paper comes
from a `make` target.

## Quickstart

```bash
make setup && conda activate hfpos && pip install -e .
make test
make help
```

## What is already implemented

Two modules are real and under test, because they encode the failure modes that
quietly invalidate this kind of study:

- `stage1/walkforward.py` — expanding-window splitter with an embargo gap, so
  overlapping forward targets cannot leak into training.
- `timing.py` — the information vs tradable window distinction, which must never
  be blurred.
- `ingest/cftc.py` — TFF ingest (issue #3), verified against the live endpoint.
- `ingest/cftc_archive.py` — zip-archive fallback, so the project is not single-sourced.
- `manifest.py` — pins the data vintage; cached reads fail loudly if it shifts.

Everything else is a specified stub that raises `NotImplementedError` naming its
issue number.

## Data facts verified 2026-09-18

Checked against the CFTC public reporting endpoint, not assumed:

| Contract | Code | Rows | Range |
|---|---|---|---|
| UST 2Y NOTE | `042601` | 1057 | 2006-06-13 → 2026-09-08 |
| UST 5Y NOTE | `044601` | 1057 | 2006-06-13 → 2026-09-08 |
| **UST 10Y NOTE** | `043602` | 1057 | 2006-06-13 → 2026-09-08 |
| UST BOND | `020601` | 1057 | 2006-06-13 → 2026-09-08 |

Two traps confirmed to be real:

- **CFTC renamed the 10Y contract in Feb 2022** (`10-YEAR U.S. TREASURY NOTES` →
  `UST 10Y NOTE`). Filtering by name returns 817 or 240 rows instead of 1057.
  Always filter by contract code.
- **14 of 1057 snapshots are not Tuesdays** (13 Mondays, 1 Wednesday), all holiday
  weeks. Code that assumes Tuesday crashes on live data.

**Source.** Primary ingest is the CFTC public reporting API
(`publicreporting.cftc.gov`, dataset `gpe5-46if`) — CFTC's own publication channel,
not a third-party mirror. It was reconciled against the official zip archives on
**2,310 cells across 2012, 2019, 2024 and 2025 with zero mismatches**
(`pytest -m network`). The archives are wired up as a fallback but only reach back
to **2010**, so they cannot reproduce 2006–2009; that gap is why the API is primary.

**Vintage.** Every fetch writes a manifest to `data/manifests/` recording row count,
date range, source and a SHA-256 of the values. Cached reads verify against it, so a
CFTC revision surfaces as an error instead of silently changing your results. A
revision would move the API and the archives together, so only the hash catches it.

The structural premise also holds in the data: over 2006–2026 asset managers are
net long in 75% of weeks (mean +10.4% of open interest) while leveraged funds are
net short in 66% (mean −7.5%), reaching −48.5% of open interest in September 2025.
