---
description: "Implement a money function end to end: requirements, tests, a run, an honest report."
tags: ["lean", "bosskuai-engineering-delivery", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

In this folder, implement `total_with_sst(items, rate=0.08)` in a new module `invoice.py`. `items` is a list of `(unit_price, quantity)` pairs; return the total including SST, rounded half-up to 2 decimal places (it's money, so no float rounding surprises). Raise `ValueError` for a negative price or quantity. Add tests using Python's built-in unittest, run them, and tell me exactly what you verified.
