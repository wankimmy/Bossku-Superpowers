---
description: "Write a PR description that lets reviewers merge a session-store change safely."
tags: ["lean", "bosskuai-github-workflow", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Write the GitHub PR description for this change so reviewers can merge it safely. What changed: session storage moved from local files to Redis; new required env var REDIS_URL; session tests updated and passing locally; production needs a Redis instance before this is deployed. Closes #212.
