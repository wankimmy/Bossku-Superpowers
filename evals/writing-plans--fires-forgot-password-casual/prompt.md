---
description: "Casual 'break it down for the dev': small tasks, tests first, the security edges."
tags: ["lean", "writing-plans", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

ok spec is approved, break it down into a step by step plan for our dev (small tasks, tests first). don't write code yet, just the plan in your reply.

spec: add 'forgot password' to our Express + Postgres app. user enters email → we email a reset link. token valid 30 minutes, single use. reset form sets new password (min 12 chars). always show the same message whether or not the email exists.
