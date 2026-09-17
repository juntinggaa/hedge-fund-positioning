# Milestone 1 — submission pack

Due **20 September 2026, 23:59 SGT**. One PDF per group.

| File | Purpose | Limit |
|---|---|---|
| `proposal.md` | Main proposal, all 7 required sections, three-arm design | 3 pages excl. references/appendices |
| `appendix.md` | Evidence appendix | 1 page, not counted |

## Before you submit — blocking items

1. **Run the two pilots.** §B of the appendix has verbatim prompts and empty result
   slots. Nothing may be reported that the group has not run itself.
2. **Verify every citation at source.** Retrieve each reference and confirm it says
   what §3 claims. Replace source 6 with specific Fed/OFR publications.
3. **Fill the bracketed placeholders** — names, dates, owners, and test cases TC2/TC3.
4. **Confirm the pivot with your teaching team** if you can reach them.
5. **Check the page count** after converting to PDF.

## Requirements coverage

| Required (guidelines §3) | Where |
|---|---|
| Question and claim | Proposal §1 |
| System and mechanism | Proposal §2 |
| Prior work, ≥4 sources, ≥2 academic | Proposal §3 — 4 academic + CFTC + Fed/OFR |
| Technical investigation plan | Proposal §4 |
| Societal and philosophical stakes | Proposal §5 |
| Feasibility and roles | Proposal §6 |
| AI-use plan | Proposal §7 |
| Appendix: diagram/table | Appendix §A |
| Appendix: two pilot cases + output | Appendix §B — **prompts ready, outputs pending** |

## The three arms

| Arm | Configuration | Tests |
|---|---|---|
| A | Bare model | H1: unaided failure rate |
| B | + retrieval grounding | H2: do correct facts fix framing? |
| C | + decomposition tool | H3: does structured evidence fix framing? |

Arms A and B are runnable now. Arm C needs the decomposition model (week 3) and is the
named fallback to drop if time runs short.
| Appendix: AI-use and decision log | Appendix §C, §D |
