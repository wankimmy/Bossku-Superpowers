---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Triage by risk: security fixes first (checking whether the advisory affects the app), then patch and minor updates, with major versions one at a time after reading the changelog for breaking changes.
- Relies on green CI plus a look at the lockfile or changelog, merges low-risk updates in batches or groups, and does not auto-merge majors blindly.
- Sets a policy to stop the pile-up (grouped updates, a schedule, or an owner).

Pass only if every point holds.
