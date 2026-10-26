---
description: "Casual 'flake or real?': the same commit passed and failed."
tags: ["lean", "ci-triage", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

test job red again on PR #88. `test_checkout_total` failed with `AssertionError: 107.0 != 108.0`. same commit passed when we re-ran it yesterday, today it failed again. flake or real bug? what do we do?
