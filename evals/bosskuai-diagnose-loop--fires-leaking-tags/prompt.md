---
description: "Bug report with a hidden cause: reproduce, fix the cause, lock it with a regression test."
tags: ["lean", "bosskuai-diagnose-loop", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

Users report that tags from one request show up in the next one. Save the code below as `tags.py`, find the real cause, fix it, and add a regression test (unittest).

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


def tag_post(post_id, new_tags):
    result = None
    for t in new_tags:
        result = add_tag(t)
    return {"post": post_id, "tags": result}
```
