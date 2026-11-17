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

## Vendored probes

`vendored-probes.json`: 790 prompts for 248 vendored skills (4 per skill, 2 per `mengto` technique skill). Each item has `id`, `prompt`, `domain` (`vendored:<pack>`), `style`, `target` (the vendored skill the prompt was written for) and `concerns`. It has no `kind`, so it splits into dev (404) and test (386) by the hash of its id, like `prompts.json`.

- Written on 2026-11-11 by 29 writer agents. Each saw only the skill catalog (ids and descriptions), never the router, its tests or the skill bodies.
- Labelled by the writer only: `concerns` lists the target and any other skill the writer judged equally right. One labeller is weaker than the two-labeller sets above.
- Styles: 260 detailed, 260 terse, 135 mixed (two asks), 133 rojak or Bahasa Malaysia, 2 casual. `using-superpowers`, `glass-dark-ui` and `schema` have no prompts.
- The dev half was used once, on 2026-11-11, to propose curated triggers. None of the 316 proposed phrases was kept, so no shipped routing was tuned on either half. Treat the dev half as seen and report the test half.

```bash
python scripts/benchmark_routing_heldout.py --arm now=.     --prompts benchmarks/routing-heldout/vendored-probes.json --split all
```

Measured on 2026-11-17: top-1 46% dev and 42% test, top-3 64% and 63%. The description-only baseline scores 49% and 45% top-1 on the same prompts, so on vendored skills the router is no better than keyword search at first pick.

## Lures

`lures.json`: 173 prompts (kind `lure`). Each one contains a phrase, or its words, that points at one vendored skill (`lure_skill`, `lure_phrase`) but asks for work that belongs to another skill (`concerns`). `lure_skill_acceptable` is true in the few cases where the lured skill would still be an acceptable pick.

- Written on 2026-11-11 and 2026-11-17 by 12 agents that saw only the catalog and a list of candidate trigger phrases. Labelled by the writer only.
- Use: a negative-routing check. A router or a hint that follows surface wording picks the lured skill; a good one picks the owner of the task.
- Never use this set for tuning.

```bash
python scripts/benchmark_routing_heldout.py --policy v1 v2 confident_router     --prompts benchmarks/routing-heldout/lures.json --split fresh
```

Measured on 2026-11-17: the router's first pick is right on 27% of lures (49% in the top three). The shipped hint (v2) shows a hint on 64% of them, and 30% of the skills it names are right.
