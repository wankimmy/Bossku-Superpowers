---
description: "Add a NOT NULL column to a 30M-row live Postgres table without downtime."
tags: ["lean", "bosskuai-database-engineering", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

We need to add a NOT NULL `tenant_id` column to our `invoices` table in PostgreSQL 15. It has 30 million rows and live traffic all day. How do we do this migration without downtime?
