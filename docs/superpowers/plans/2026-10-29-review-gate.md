# Brief: Bossku reviews its own changes by default (review gate)

Status: approved (option B) and built on 2026-10-29 in `4e1e928`, released in v2.13.0. The tests went into `tests/hooks.test.mjs`, the home of the Node stop gate's tests, not `tests/test_hooks_gate_hint.py`.

## Goal

After any turn that changed code, the agent reviews its own diff before it says "done", fixes what it finds, and
feeds reusable lessons into auto-learn. On by default after `bossku install`, with an off switch.

## Why a hook, not only a rule

A rule in `AGENTS.md` is advice the agent may skip. The stop gate already holds a turn for two things (code that never
ran, and a missing `Security gate:` line). A review check fits the same place and the same once-per-turn rule.

## Proposed change (option B, recommended)

1. `hooks/stop-gate.mjs`: a third check. If the turn edited source files (the same edit detection the run-your-code
   check uses, scratch files excluded) and the last reply has no `Review:` line, send the agent back once with:
   review your own diff with `bosskuai-rigorous-code-review` (correctness, risk, missing tests, does it meet the
   goal), fix what you find, end with `Review: CLEAN | FIXED <n> | OPEN <n>`, and save any reusable lesson with
   `bossku remember --kind learning`. When the security line is also missing, both asks go in one push-back, so a
   turn costs at most one extra round.
2. Off switch `BOSSKU_REVIEW_GATE=off`; `bossku doctor` lists it with the other switches.
3. Self-learning link: the `bosskuai-learn` pass already runs every 50 tool calls; it gains one line telling it to
   turn review findings that repeat into a learned skill (through `bossku learn apply`, as today).
4. Docs: `AGENTS.md` and the session-start contract line, `hooks/README.md`, `README.md` switch list, `CHANGELOG.md`.
5. Tests in `tests/test_hooks_gate_hint.py`: blocks once on a code edit without `Review:`; passes with it; skips
   doc-only and scratch edits; respects `stop_hook_active` and the off switch; one combined message with the
   security ask.

## Options not recommended

- **A. Instruction only** (`AGENTS.md` line, no hook). Cheapest, but not enforced: the same gap the audit found in
  the security gate.
- **C. A fresh auditor subagent on every change.** Catches blind spots a self-review shares with the author, but
  costs a full extra context each turn. Could be added later for large diffs only.

## Costs and risks

- One extra round per code-changing turn, so more tokens (the published runs already show 1.1x to 4.7x).
- A self-review shares the author's blind spots; it is a floor, not a second opinion.
- Like the security line, the hook checks that a `Review:` line exists, not that the review was good. Docs must say so.

## Done means

All five steps above, the new tests and the full suite green, `bossku validate` ok, and docs that state what the
hook does and does not check.
