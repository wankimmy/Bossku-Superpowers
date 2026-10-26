# Fresh held-out routing set

## What is here

- `fresh.json`: 200 prompts. Kinds: 60 multi, 40 short, 100 followup.
- `trivial.json`: 100 prompts. Kind: 100 trivial (no skill needed).

Each file is a JSON list. Each item has `id`, `prompt`, `domain`, `style`, `kind`, `agreement` and `concerns`. `concerns` is a list of lists of skill ids, one list per concern. It is empty when no skill is needed. `agreement` is `both` when the two labellers matched, and `tiebreak` when the third agent decided.

## How it was made

- Written on 2026-10-10 by 4 persona writer agents. They saw only the skill catalog (skill ids and descriptions). They never saw the router, the skill bodies or earlier prompts.
- Labelled independently by two labeller agents. A third agent broke ties.
- Agreement: 285 of 300 items matched between the two labellers (both files together). The 15 that needed a tie-break are all in `fresh.json`.

## Counts per kind

| File | multi | short | followup | trivial | Total |
|---|---|---|---|---|---|
| fresh.json | 60 | 40 | 100 | 0 | 200 |
| trivial.json | 0 | 0 | 0 | 100 | 100 |

## Limits

- These prompts are agent-written and agent-labelled. They are not human-labelled.
- Use: the decision split for the smart-lean gate only.
- Never use this set for tuning. Do not change triggers, weights or thresholds based on it.
- Cleanup after labelling: 9 labels named skills that are not in this repo (code-review, security-review, dataviz: Claude Code's own built-in skills the labeller agents knew about). They were removed, and 2 concerns that had no other acceptable skill were dropped.

## Out-of-catalog set

`out-of-catalog.json`: 120 prompts (kind `out_of_catalog`) for real work that no skill in the catalog covers: explanations, worked calculations, letters and plans from everyday life, science, engineering, teaching, accounting, law and medicine. The right answer for each is no skill. It measures how often the hint names a skill when nothing fits.

- Written on 2026-10-26 by 2 persona writer agents (60 prompts each): a Malaysian founder who types everything into the agent, and specialists or non-software professionals. They saw only the skill catalog (ids and descriptions, all 672 skills) and checked every prompt against it.
- Labelled by two other agents, each on its own, in opposite order. Each listed any skill whose description covered any part of the request. Both labelled all 120 as needing no skill, so `agreement` is `both` and `concerns` is empty for every row; no tie-break was needed.
- Styles: 40 terse, 40 casual, 20 rojak, 20 detailed. Domains: 44 engineering, 40 general, 23 science, 13 creative.
- The same limits apply: agent-written and agent-labelled, and never to be used for tuning.

```bash
python scripts/benchmark_routing_heldout.py --policy v1 v2 confident_router \
    --prompts benchmarks/routing-heldout/out-of-catalog.json --split fresh
```
