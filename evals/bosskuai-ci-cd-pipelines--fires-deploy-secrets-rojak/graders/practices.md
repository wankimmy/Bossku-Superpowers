---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Uses OIDC (short-lived cloud credentials) instead of long-lived keys stored as secrets, where the cloud supports it.
- Puts production deploys behind a protected environment with required reviewers, with least-privilege workflow permissions.
- Avoids leaks: never print secrets, keep them away from fork pull requests (no pull_request_target that checks out PR code), and pin third-party actions to a commit SHA.

Pass only if every point holds.
