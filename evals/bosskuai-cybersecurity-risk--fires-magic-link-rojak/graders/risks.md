---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Token rules: long and random, single use, short expiry, stored hashed or only server-side.
- Abuse: rate limits on sending links, and the same response whether or not the email exists.
- Link leakage (email forwarding, logs, browser history or the Referer header), and that account security now rests on the user's email account.

Pass only if every point holds.
