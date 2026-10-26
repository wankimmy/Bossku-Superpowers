---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Ordered small tasks that name the parts touched (routes, a token table or migration, the mailer, views, tests).
- Covers the 30-minute expiry and single use, with tests for an expired token and a reused token.
- Covers the same response for unknown emails, plus at least one safeguard beyond the spec (for example storing only a hash of the token, or rate-limiting reset requests).
- Each task has a verification step.

Pass only if every point holds.
