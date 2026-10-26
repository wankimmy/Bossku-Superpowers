---
description: "WCAG 2.2 AA audit of a signup form, with fixed HTML."
tags: ["lean", "accessibility", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Audit this signup form for WCAG 2.2 AA and give me the fixed HTML.

```html
<form>
  <input type="email" placeholder="Email">
  <input type="password" placeholder="Password">
  <span style="color:#bbb">At least 12 characters</span>
  <div>Plan:</div>
  <input type="radio" name="plan" value="free"> Free
  <input type="radio" name="plan" value="pro"> Pro
  <span class="error" style="color:red"></span>
  <div class="btn" onclick="submitForm()">Sign up</div>
</form>
```
