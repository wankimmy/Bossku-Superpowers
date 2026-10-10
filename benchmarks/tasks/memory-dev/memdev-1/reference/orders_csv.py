"""Order file helpers."""
import datetime


def parse_orders(text):
    orders = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) != 3:
            raise ValueError("bad line")
        order_id, customer, date = parts
        orders.append({"id": int(order_id), "customer": customer.strip(),
                       "date": datetime.date.fromisoformat(date.strip())})
    return orders


def export_csv(orders):
    lines = ["order_id;customer_name;order_date"]
    for order in orders:
        lines.append("%d;%s;%s" % (order["id"], order["customer"], order["date"].strftime("%d/%m/%Y")))
    return "\n".join(lines) + "\n"
