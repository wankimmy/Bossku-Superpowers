---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Resource-style endpoints (for example POST /appointments, PATCH or a POST action to reschedule, DELETE or POST /appointments/{id}/cancel), without verbs in ordinary resource paths.
- A structured error body with a machine-readable code, and 409 Conflict for a slot that is already taken.
- Retry safety for booking: an idempotency key (or equivalent) so a retried POST does not create two appointments.
- Pagination for the list endpoint, and a rule that patients only see and change their own appointments.

Pass only if every point holds.
