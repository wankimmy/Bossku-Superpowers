---
description: "Rojak review request for code that looks fine but returns before its writes finish."
tags: ["lean", "bosskuai-rigorous-code-review", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

boleh tolong review code ni sebelum merge? rasa ok je tapi nak confirm

```js
async function saveAll(items) {
  items.forEach(async (item) => {
    await db.save(item);
  });
  return "saved";
}
```
