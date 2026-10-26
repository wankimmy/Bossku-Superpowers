---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Signs each delivery (for example HMAC of the raw body with a shared secret) and includes a timestamp so partners can reject replays.
- Retries failed deliveries with backoff, and treats a 2xx response as success.
- Gives each event a unique id for deduplication, and says deliveries can arrive out of order (or adds a sequence or updated_at).
- Uses a versioned, documented payload.

Pass only if every point holds.
