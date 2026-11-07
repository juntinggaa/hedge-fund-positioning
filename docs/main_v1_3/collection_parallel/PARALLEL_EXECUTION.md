# Parallel execution amendment — 6 November 2026

The user requested maximum practical subagent parallelism to finish GPT and Claude first. At allocation, canonical reply files existed through GPT-017 and CLA-038 (55 files, not a claim that all source audits have passed). Gemini remains queued.

Allocate fixed disjoint sequential ranges: original Claude collector CLA-039–060; new GPT worker A GPT-018–039; new GPT worker B GPT-040–060. Confirm any already-sent GPT assignment at handoff before enabling its new lease. Canonical files already present are never regenerated or overwritten.

This changes execution order prospectively: the two GPT ranges can overlap in wall-clock time, so global GPT send order can differ from the original runsheet. Preserve ascending order within each range and log actual timestamps and worker IDs. The split uses assignment numbers only, not answer content, residuals or outcomes. Prompt texts, sample, arms, accounts, requested models/effort, and scoring definitions are unchanged. The user authorized this operational parallelization directly; no other team signatures are inferred.

Use separate owned DOM tabs with no concurrent native/global Chrome input. Every worker checks/claims its ID before sending and uses exclusive creation for raw outputs. The two GPT workers keep at most one generation in flight each; the original Claude collector may keep two, for four live generations in total. The shared clipboard lock covers Copy/read only and must be released before DOM/screenshot/metadata work. Prefer the known clean assistant body DOM fallback after documented Copy failures, retaining full source and the capture-method deviation.

Save the completed answer and full DOM to disk before requesting one viewport screenshot; avoid full-page screenshots. Record screenshots unavailable honestly. For a frontend load error, preserve it and first attempt recovery of the same generated response through one normal reload/open of its exact observed URL, before generating another response. Never select/rerun for answer quality. Every actual retry remains logged. No model/account substitution, purchases, limit bypass, or fabricated text/timestamps.

Original source concerns, including identical CLA-007/008 files and earlier missing screenshots, remain separate audit flags. Parallel collection does not validate them or human scoring reliability.
