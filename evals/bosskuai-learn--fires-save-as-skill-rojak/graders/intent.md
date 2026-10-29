---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Shows one JSON intent for `bossku learn apply` with `action`, `name`, `reason`, `evidence` and a SKILL.md `body` whose frontmatter has `learned: true` and a `description` starting with "Use when".
- The rule keeps the order: migrate first, then config:cache, with the reason (a stale config cache pointing at the old database).
- The name is class-level (staging deploys), not tied to last week's incident.
- Replies in a register that suits the user's mix of English and Malay, and stays short.

Pass only if every point holds.
