---
description: "A React effect that refetches forever: the cause and the right fix."
tags: ["lean", "bosskuai-react-development", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

This React component refetches in an endless loop. Why, and what's the right fix?

```tsx
function Orders({ page }: { page: number }) {
  const [orders, setOrders] = useState<Order[]>([]);
  const params = { page, size: 20 };

  useEffect(() => {
    fetch(`/api/orders?page=${params.page}&size=${params.size}`)
      .then((r) => r.json())
      .then(setOrders);
  }, [params]);

  return <OrderTable orders={orders} />;
}
```
