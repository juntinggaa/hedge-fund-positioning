# Main-v1.3 results (machine coders; disputes resolved by humans where available)

Replies: 180 main + 16 effort-check. Composite disputes between the two machine coders: 17 replies (7 resolved by humans). Unresolved disputes are shown under two rules: **both** (overreach only if both coders flag it) / **either** (if either does).

## Rates, rule = both

| Product | Arm | n | Common composite (B2|B3 ≥2) | B2≥2 | B3≥2 | R≥2 | Model-block composite |
|---|---|---|---|---|---|---|---|
| ChatGPT (GPT-6 Sol, High) | A | 20 | 2/20 (10%) | 2/20 (10%) | 0/20 (0%) | n/a | n/a |
| ChatGPT (GPT-6 Sol, High) | C-bare | 20 | 1/20 (5%) | 0/20 (0%) | 0/20 (0%) | 1/20 (5%) | 1/20 (5%) |
| ChatGPT (GPT-6 Sol, High) | C-ann | 20 | 0/20 (0%) | 0/20 (0%) | 0/20 (0%) | 0/20 (0%) | 0/20 (0%) |
| Claude (Opus 5.5, High) | A | 20 | 18/20 (90%) | 18/20 (90%) | 16/20 (80%) | n/a | n/a |
| Claude (Opus 5.5, High) | C-bare | 20 | 16/20 (80%) | 16/20 (80%) | 11/20 (55%) | 0/20 (0%) | 16/20 (80%) |
| Claude (Opus 5.5, High) | C-ann | 20 | 3/20 (15%) | 2/20 (10%) | 2/20 (10%) | 0/20 (0%) | 3/20 (15%) |
| Gemini (4 Argon, Low) | A | 20 | 20/20 (100%) | 20/20 (100%) | 11/20 (55%) | n/a | n/a |
| Gemini (4 Argon, Low) | C-bare | 20 | 19/20 (95%) | 18/20 (90%) | 6/20 (30%) | 6/20 (30%) | 19/20 (95%) |
| Gemini (4 Argon, Low) | C-ann | 20 | 10/20 (50%) | 8/20 (40%) | 0/20 (0%) | 1/20 (5%) | 10/20 (50%) |

### Paired contrasts, rule = both (20 weeks per product)

b = weeks where only the first arm overreaches; c = only the second. Exact two-sided McNemar.

| Product | Contrast | Endpoint | both | neither | b (first only) | c (second only) | p | Holm p (primary) |
|---|---|---|---|---|---|---|---|---|
| ChatGPT (GPT-6 Sol, High) | C-bare vs C-ann | model-block | 0 | 19 | 1 | 0 | 1.000 | 1.000 |
| ChatGPT (GPT-6 Sol, High) | A vs C-bare | common | 0 | 17 | 2 | 1 | 1.000 | – |
| ChatGPT (GPT-6 Sol, High) | A vs C-ann | common | 0 | 18 | 2 | 0 | 0.500 | – |
| Claude (Opus 5.5, High) | C-bare vs C-ann | model-block | 3 | 4 | 13 | 0 | 0.000 | 0.001 |
| Claude (Opus 5.5, High) | A vs C-bare | common | 14 | 0 | 4 | 2 | 0.688 | – |
| Claude (Opus 5.5, High) | A vs C-ann | common | 2 | 1 | 16 | 1 | 0.000 | – |
| Gemini (4 Argon, Low) | C-bare vs C-ann | model-block | 9 | 0 | 10 | 1 | 0.012 | 0.023 |
| Gemini (4 Argon, Low) | A vs C-bare | common | 19 | 0 | 1 | 0 | 1.000 | – |
| Gemini (4 Argon, Low) | A vs C-ann | common | 10 | 0 | 10 | 0 | 0.002 | – |

## Rates, rule = either

| Product | Arm | n | Common composite (B2|B3 ≥2) | B2≥2 | B3≥2 | R≥2 | Model-block composite |
|---|---|---|---|---|---|---|---|
| ChatGPT (GPT-6 Sol, High) | A | 20 | 4/20 (20%) | 4/20 (20%) | 0/20 (0%) | n/a | n/a |
| ChatGPT (GPT-6 Sol, High) | C-bare | 20 | 3/20 (15%) | 4/20 (20%) | 0/20 (0%) | 1/20 (5%) | 3/20 (15%) |
| ChatGPT (GPT-6 Sol, High) | C-ann | 20 | 0/20 (0%) | 0/20 (0%) | 0/20 (0%) | 0/20 (0%) | 0/20 (0%) |
| Claude (Opus 5.5, High) | A | 20 | 18/20 (90%) | 18/20 (90%) | 18/20 (90%) | n/a | n/a |
| Claude (Opus 5.5, High) | C-bare | 20 | 17/20 (85%) | 17/20 (85%) | 12/20 (60%) | 1/20 (5%) | 17/20 (85%) |
| Claude (Opus 5.5, High) | C-ann | 20 | 6/20 (30%) | 7/20 (35%) | 3/20 (15%) | 0/20 (0%) | 6/20 (30%) |
| Gemini (4 Argon, Low) | A | 20 | 20/20 (100%) | 20/20 (100%) | 14/20 (70%) | n/a | n/a |
| Gemini (4 Argon, Low) | C-bare | 20 | 19/20 (95%) | 19/20 (95%) | 8/20 (40%) | 9/20 (45%) | 19/20 (95%) |
| Gemini (4 Argon, Low) | C-ann | 20 | 10/20 (50%) | 10/20 (50%) | 0/20 (0%) | 3/20 (15%) | 11/20 (55%) |

### Paired contrasts, rule = either (20 weeks per product)

b = weeks where only the first arm overreaches; c = only the second. Exact two-sided McNemar.

| Product | Contrast | Endpoint | both | neither | b (first only) | c (second only) | p | Holm p (primary) |
|---|---|---|---|---|---|---|---|---|
| ChatGPT (GPT-6 Sol, High) | C-bare vs C-ann | model-block | 0 | 17 | 3 | 0 | 0.250 | 0.250 |
| ChatGPT (GPT-6 Sol, High) | A vs C-bare | common | 1 | 14 | 3 | 2 | 1.000 | – |
| ChatGPT (GPT-6 Sol, High) | A vs C-ann | common | 0 | 16 | 4 | 0 | 0.125 | – |
| Claude (Opus 5.5, High) | C-bare vs C-ann | model-block | 6 | 3 | 11 | 0 | 0.001 | 0.003 |
| Claude (Opus 5.5, High) | A vs C-bare | common | 15 | 0 | 3 | 2 | 1.000 | – |
| Claude (Opus 5.5, High) | A vs C-ann | common | 5 | 1 | 13 | 1 | 0.002 | – |
| Gemini (4 Argon, Low) | C-bare vs C-ann | model-block | 10 | 0 | 9 | 1 | 0.021 | 0.043 |
| Gemini (4 Argon, Low) | A vs C-bare | common | 19 | 0 | 1 | 0 | 1.000 | – |
| Gemini (4 Argon, Low) | A vs C-ann | common | 10 | 0 | 10 | 0 | 0.002 | – |

## Effort check: Gemini low vs high effort, same 16 prompts (descriptive)

| Endpoint | rule | agree | low only | high only | low rate | high rate |
|---|---|---|---|---|---|---|
| common | both | 11/16 | 3 | 2 | 75% | 69% |
| common | either | 10/16 | 3 | 3 | 75% | 75% |
| model-block | both | 5/9 | 2 | 2 | 56% | 56% |
| model-block | either | 4/9 | 2 | 3 | 56% | 67% |

GEM-045 (high) has uncertain effort (cap reached around that reply).

Machine-machine agreement is not human reliability; see the human sample.
