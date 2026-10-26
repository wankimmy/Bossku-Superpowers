---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives the order: signup → validate_signup → create_user → add and flush → cache.delete → events.emit → send_welcome (enqueue) and start_trial (billing API) → commit → 201.
- Notes that the handlers run synchronously, before the commit.
- Flags the consistency risks: the welcome email job and the external trial can happen for a user whose commit then fails, and a billing error inside create_user stops the user from being committed at all.
- Labels at least one thing as assumed or not shown (for example how queue.enqueue or billing.create_trial behave).

Pass only if every point holds.
