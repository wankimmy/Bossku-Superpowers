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
