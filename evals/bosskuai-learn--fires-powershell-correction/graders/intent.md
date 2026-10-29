---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Shows one JSON intent with `action` (create or patch), `name`, `reason`, `evidence` and, for create, a full SKILL.md `body`.
- The name describes the class of work (PowerShell or Windows commands), not this one session.
- The body's frontmatter has `name`, a `description` that starts with "Use when", a `category`, and `learned: true`; the rule itself is short (well under 25 lines).
- The evidence quotes the user's correction rather than inventing one.

Pass only if every point holds.
