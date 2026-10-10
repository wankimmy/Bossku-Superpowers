"""Order bookkeeping."""
import logging

logger = logging.getLogger(__name__)


def _find(orders, order_id):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise KeyError(order_id)


def place_order(orders, order_id, total_cents):
    order = {"id": order_id, "total_cents": total_cents, "status": "placed"}
    orders.append(order)
    logger.info("event=order_placed order_id=%s total_cents=%s", order_id, total_cents)
    return order


def cancel_order(orders, order_id):
    order = _find(orders, order_id)
    order["status"] = "cancelled"
    logger.info("event=order_cancelled order_id=%s", order_id)
    return order


def refund_order(orders, order_id, reason):
    order = _find(orders, order_id)
    if order["status"] != "placed":
        raise ValueError("order is not refundable")
    order["status"] = "refunded"
    logger.info("event=order_refunded order_id=%s reason=%s", order_id, str(reason).replace(" ", "_"))
    return order
