---
description: "Classify a red CI run caused by a registry timeout: environment, not code."
tags: ["lean", "ci-triage", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

CI failed on main at commit 3f2a9c1. Here's the log. What kind of failure is this and what should we do?

```
Run npm ci
npm ERR! code ETIMEDOUT
npm ERR! errno ETIMEDOUT
npm ERR! network request to https://registry.npmjs.org/react-dom/-/react-dom-18.3.1.tgz failed, reason: connect ETIMEDOUT 104.16.27.34:443
npm ERR! network This is a problem related to network connectivity.
Error: Process completed with exit code 1.
```
