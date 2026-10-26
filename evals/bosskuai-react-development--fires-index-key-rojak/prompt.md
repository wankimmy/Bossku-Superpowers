---
description: "Rojak bug report: typed text jumps rows after a delete (index keys)."
tags: ["lean", "bosskuai-react-development", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

list dalam React aku, bila delete satu item, text yang user tengah taip dalam row lain pindah ke row sebelah. kenapa jadi macam ni?

```tsx
{items.map((item, index) => (
  <li key={index}>
    {item.label} <input placeholder="note" />
    <button onClick={() => remove(item.id)}>x</button>
  </li>
))}
```
