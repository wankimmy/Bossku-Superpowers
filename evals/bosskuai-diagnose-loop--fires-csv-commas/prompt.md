---
description: "Casual bug report: names with commas split columns. Reproduce and fix properly."
tags: ["lean", "bosskuai-diagnose-loop", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

my csv export is broken: when a customer name has a comma (like 'Tan, Mei Ling'), Excel splits it into 2 columns. save the code as `export.py`, debug it and fix it properly, with a test pls

```python
def to_csv(rows):
    lines = ["name,amount"]
    for r in rows:
        lines.append(",".join([r["name"], str(r["amount"])]))
    return "\n".join(lines) + "\n"
```
