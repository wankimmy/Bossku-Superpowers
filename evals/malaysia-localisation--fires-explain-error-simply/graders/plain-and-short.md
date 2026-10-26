---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- No more than about 4 short lines of explanation.
- Plain words a non-technical reader understands: someone tried to register or save an email address that is already in the system.
- Suggests a sensible action (for example tell the user the email is already registered and offer log in or password reset, or check for a double sign-up).
- Matches the user's language (BM/rojak or simple English).

Pass only if every point holds.
