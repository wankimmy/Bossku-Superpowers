---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- States the goal and the status split into done, not done and blocked (the blocker being the sandbox keys from finance).
- Keeps the decision with its reason (Stripe stays for SGD because Billplz only does MYR).
- Lists the files by path and separates verification done (unit tests passing) from not done (no sandbox testing).
- Ends with ordered, concrete next steps (for example the webhook handler, then refunds, then sandbox tests once the keys arrive).

Pass only if every point holds.
