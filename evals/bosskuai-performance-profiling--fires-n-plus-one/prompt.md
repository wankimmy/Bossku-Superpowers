---
description: "A Django endpoint got 15x slower: find the bottleneck and prove the fix."
tags: ["lean", "bosskuai-performance-profiling", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Our Django endpoint /api/orders went from about 200 ms to 3 seconds after we added customer names to the response. Here's the view. Why is it slow, and how do we prove the fix worked?

```python
def orders(request):
    data = []
    for o in Order.objects.filter(shop=request.shop).order_by("-created_at")[:500]:
        data.append({"id": o.id, "total": o.total, "customer": o.customer.name})
    return JsonResponse({"orders": data})
```
