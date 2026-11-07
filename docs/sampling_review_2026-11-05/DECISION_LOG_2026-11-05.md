# Decision log — 5 November 2026

Status: proposed design review, awaiting team sample freeze. This log records new work and proposals; it does not alter the original protocol.

| Item | Evidence / proposed deviation | Status |
|---|---|---|
| Endpoint | Optional append-only extension from 2026-09-08 to official 2026-10-27, released Oct 30. Original panel and manifests preserved. | New version created; main endpoint not adopted |
| Supporting inputs | New suffixes for 2Y/5Y/30Y CFTC and FRED/ZN inputs needed by frozen 40-feature v4. All original historical values preserved. | Completed in separate namespace |
| Estimator | Reconstruct final Aug-04-trained weighted_104, alpha 316.22776601683796; reproduce old final-block predictions; extend seven dates. | Completed; no retuning or new-week fitting |
| Intervals | Same prior-only RMS-error policy, min 52; earlier new errors may inform later new intervals. | Unchanged method; 720–726 prior errors available |
| Strata | Retain exact definitions and pinned negative-decile cutoff −0.37567236606810045. | No definition change |
| S2 feasibility | 15 candidates in Sep–Dec 2014; maxima 2/3/4 at 8/6/4-week gaps. No balanced ten-per-stratum complete-case design. | Established before main responses |
| Gap interpretation | Original sampler applies gap within stratum; original whole stratified sample has a 14-day minimum gap. | Documented clarification |
| Looser spacing | Evaluate 4 and 6 weeks alongside original 8. Four-week candidate doubles S2 from two to four but still one short episode. | Proposed only; no independence claim |
| Global spacing | Test additional across-strata gap for all B/C candidates. Same counts feasible; separate date files. | Sensitivity only; not silently adopted |
| A | Preserve original 41 weeks; A/B for all, C-bare/C-ann/D only for 26 stratified plus purposive case. Separate matched analysis sets. | Recommended for stated historical-diversity priority; not frozen |
| B | Complete case quotas 10/2/10/10 (8w), 10/3/10/10 (6w), 10/4/10/10 (4w). | Four-week/34-case version preferred if full five-arm pairing is primary; not frozen |
| C | 40 complete cases with 13/2/13/12 (8w), 13/3/12/12 (6w), 12/4/12/12 (4w). Historical weighting and question change. | Feasible alternative; not recommended just to reach 40 |
| Development exclusions | For B/C, exclude six known pilot weeks and separate purposive date based on identifiers only. Report unrestricted capacities separately. A necessarily preserves one known development overlap. | Proposed amendment; no response scores/content consulted |
| Date selection | Fixed seed and exact feasible-subset draw; global checks have a fixed date-only objective. No residual or LLM-score selection. | Recorded before candidate generation |
| Purposive case | 2025-09-02 remains qualitative; add ten responses for two models/five arms, zero inferential cases. | Proposed consistently across options |
| Statistical plan | Preserve week pairing; report scopes/strata; predeclare dependence sensitivity and primary contrast. S2 cannot identify a broad pre-2015 era effect. | Analysis plan still to freeze |
| Main experiment | No LLM calls, scoring-based selection, main prompt replacement, or generation. | Not launched |
| Approval / repo | All candidates stay in dated files; original sample and pinned data unchanged. No commit/push requested for this review. | Awaiting design choice |
