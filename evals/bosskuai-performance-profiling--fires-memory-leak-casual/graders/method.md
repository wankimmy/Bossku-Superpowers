---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Reproduces it faster (a load test or replayed traffic) and watches memory over time.
- Takes heap snapshots over time (for example node --inspect with Chrome DevTools, or --heapsnapshot-signal) and compares them to see which objects keep growing.
- Lists likely causes to check against that evidence (unbounded caches or maps, listeners or timers never removed, global arrays, closures holding requests).
- Confirms a fix by re-running the same scenario and seeing memory level off.

Pass only if every point holds.
