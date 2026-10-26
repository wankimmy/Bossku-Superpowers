---
description: "Security review of an avatar upload handler before shipping."
tags: ["lean", "bosskuai-cybersecurity-risk", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Do a security review of this upload handler before we ship it:

```python
@app.post("/avatar")
@login_required
def upload_avatar():
    f = request.files["file"]
    if f.mimetype not in ("image/png", "image/jpeg"):
        return {"error": "images only"}, 400
    path = os.path.join("static/uploads", f.filename)
    f.save(path)
    current_user.avatar_url = "/" + path
    db.session.commit()
    return {"url": current_user.avatar_url}
```
