---
description: "Speed up a slow GitHub Actions workflow for a Node monorepo, safely."
tags: ["lean", "bosskuai-ci-cd-pipelines", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Our GitHub Actions CI takes about 25 minutes on every PR. It's a Node monorepo with 6 packages under packages/. How do we speed it up safely?

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm run lint --workspaces
      - run: npm test --workspaces
      - run: npm run build --workspaces
```
