---
description: "Explicit test-first request: a failing run before the code, then green."
tags: ["lean", "bosskuai-tdd-loop", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

Let's do this test-first. I need `parse_duration(text)` in a new module `duration.py` that turns strings like '1h30m', '45s' or '2h5s' into seconds (5400, 45, 7205). Units are h, m and s, each used at most once, in that order. Empty strings and unknown units raise ValueError. Use Python's built-in unittest only.
