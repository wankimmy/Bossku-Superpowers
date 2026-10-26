---
description: "Rojak ask to trace an order cancellation and its external side effects."
tags: ["lean", "bosskuai-codebase-analysis", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

tolong trace flow bila customer cancel order dalam code ni: function mana dipanggil ikut turutan, side effect apa, dan ada risiko tak?

```python
def cancel_order(order_id, user):
    order = Order.get(order_id)
    if order.user_id != user.id:
        raise Forbidden()
    restock(order)
    refund(order)
    order.status = "cancelled"
    order.save()
    notify(user, f"Order {order_id} cancelled")

def restock(order):
    for line in order.lines:
        Product.increment_stock(line.product_id, line.qty)

def refund(order):
    gateway.refund(order.payment_id, order.total)  # external API, may raise

def notify(user, text):
    sms.send(user.phone, text)  # external API
```
