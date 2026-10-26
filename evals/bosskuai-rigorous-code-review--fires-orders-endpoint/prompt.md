---
description: "Pre-merge review of an endpoint with injection, missing ownership and a crash."
tags: ["lean", "bosskuai-rigorous-code-review", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Please review this PR before I merge. It adds an endpoint so customers can see an order.

```diff
+@app.route("/orders/<order_id>")
+@login_required
+def get_order(order_id):
+    row = db.execute(f"SELECT * FROM orders WHERE id = {order_id}").fetchone()
+    return jsonify(dict(row))
```
