---
description: "Casual slow MySQL query: the right composite index, checked with EXPLAIN."
tags: ["lean", "bosskuai-database-engineering", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

our mysql query is slow: SELECT * FROM orders WHERE status = 'paid' AND created_at > '2025-01-01' ORDER BY created_at DESC LIMIT 50; table has 8 million rows and the only index is the primary key on id. what index should we add?
