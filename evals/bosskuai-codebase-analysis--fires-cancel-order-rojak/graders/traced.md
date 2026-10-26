---
type: llm
focus: last_message
---

Ignore any status header at the very top of the reply (lines that start with `bossku-superpowers`, `Skills:` or `Memory:`).

Pass criteria:
- Gives the order: ownership check → restock (stock added back per line) → refund through the external gateway → status saved as cancelled → SMS.
- Flags that if the refund raises, the stock was already added back while the order is not cancelled, and a retry would restock again.
- Flags that nothing stops cancelling an already cancelled (or shipped) order, so refunds or restocks can repeat.

Pass only if every point holds.
