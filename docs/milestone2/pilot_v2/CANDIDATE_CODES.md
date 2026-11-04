# Candidate codes for codebook v2.1 (DRAFT b, 2026-11-05; still not frozen)

Draft a (earlier the same day) scored any level wording as ambiguous and any
non-use of the range as an error. Both rules were too strict, and draft a's
provisional finding ("only 2 of 12 read the residual as an adjustment") was
largely an artefact of them. Draft a is superseded; the original provisional codes
under it are kept in `coder0_claude_PROVISIONAL.csv`.

**Why level language can be correct.** By construction
`expected_s_t = s_{t-1} + ŷ_t`, so `s_t − expected_s_t = y_t − ŷ_t`. "The
position is 3.1 percentage points of open interest more short than expected" is
therefore exactly right. It describes the conditional level gap, which equals
the unexpected adjustment.

**Units.** The residual is in **percentage points of open interest**. It is not a
percentage of the leveraged-fund position. −3.13 pp of OI against a −48.53% net
position is about 6.5% of that position, not 3%.

These codes become part of the codebook only after **two human coders** apply them
independently and reach κ ≥ 0.7. No human agreement or κ exists yet.

### L: level / adjustment interpretation (C arms)
| | Behaviour | Examples |
|---|---|---|
| 0 | Correct: states the conditional level gap (pp of OI) or the unexpected adjustment | "3.47 pp less short than expected"; "funds added more shorts this week than conditions implied" |
| 1 | Ambiguous: understanding cannot be determined from the text | "the short is more bearish than the model expected" (no magnitude, no reference to change or gap) |
| 2 | Error: treats the residual as an unexplained **fraction of the whole position**, confuses pp of OI with % of the position, or treats it as an identified quantity of a trading motive | "3% of the short position is unexplained"; "a 3% residual means 3% of their shorts are speculative" |

The motive half of L = 2 overlaps with R = 3. If both apply, code both and note the
overlap; κ will show whether they should merge.

### U: interpretation of the range and percentile (C arms, v2 block)
**Not mentioning the range is not an error.** A substantive code needs an
identifiable unsupported claim or a contradiction.

| | Behaviour |
|---|---|
| 0 | No error. The range or percentile is used correctly, or not used and nothing contradicts it |
| 1 | Imprecise: a loose characterisation that is not a clear contradiction (e.g. calling a residual at the 23rd percentile "noticeable") |
| 2 | Contradiction or unsupported claim: an in-range residual treated as a clear signal, or an out-of-range residual as ordinary |
| 3 | Treats the range or percentile as a probability of a market outcome, or as a guarantee about this week |

Descriptive (not an error code): `U_use` = 1 if the response uses the range or
percentile at all.

**Misreading a supplied number** (e.g. "4%" read as "96%") is coded **F**, not U.

### Applied alongside existing codes
B2, B3, R, M and F from codebook v2.0, unchanged.
