---
name: bosskuai-token-saver
description: Use when the user explicitly asks for terse output, lower token use, caveman mode, compressed prompts, shorter rules, or reducing prompt bloat without losing meaning.
---

# BosskuAI Token Saver

Use this skill to reduce output or instruction bloat while keeping technical meaning intact.
Public-facing name: **compressed output mode**.
Compatibility alias: `bosskuai-caveman`.

## Modes

- `lite`: concise full sentences. Best default for professional work.
- `full`: fragments allowed. Good for debugging, code review, and terminal-style notes.
- `ultra`: abbreviations and arrows. Use only when the user explicitly wants maximum compression.

## Compression Rules

Remove:

- greetings, apologies, filler, hedging
- repeated context already known
- generic motivational language
- long summaries before the answer
- protocol chatter unless useful to the user

Keep:

- exact commands
- file paths
- warnings for destructive actions
- security, payment, legal, or data-loss caveats
- verification status and unknowns

## Prompt-Bloat Rules

When compressing repo instructions:

1. Keep mandatory boundaries and safety rules intact.
2. Turn long philosophy into operational checks.
3. Move examples into references when they are not needed on every run.
4. Prefer one routing rule over many overlapping specialist rules.
5. Preserve aliases for old prompts.

## Decision brief shape

When asked to condense a long report for a decision-maker, make it readable in about three minutes and answer first:

1. Situation: what is happening, why now, and the gap to the target.
2. Key findings: three to five, most important first, each with a number or comparison and its implication in bold.
3. Business impact: gain or loss, size of the risk, and time horizon.
4. Recommendations: prioritised, each with an owner, a date, and the expected result.
5. Next steps.

Use only figures in the source; list data gaps and uncertainties instead of filling them. The summary supports the decision, it does not make it.

## Do Not Compress

- destructive operation confirmations
- legal/compliance wording where precision matters
- security warnings
- migration steps where order matters
- user-facing copy being edited for tone, unless requested

## Output Shape

```txt
Mode: lite/full/ultra
Result: ...
Notes: only if meaning changed or risk remains
```

## References

- `../../references/checklists/token-saver-checklist.md`

Decision brief shape adapted in part from support/support-executive-summary-generator.md (agency-agents, MIT).
