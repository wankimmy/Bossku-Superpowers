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
    return order


def cancel_order(orders, order_id):
    order = _find(orders, order_id)
    order["status"] = "cancelled"
    return order


def refund_order(orders, order_id, reason):
    tag = str(reason).replace(" ", "_")
    try:
        order = _find(orders, order_id)
    except KeyError:
        logger.warning("event=refund_rejected order_id=%s reason=%s why=unknown_order", order_id, tag)
        raise
    if order["status"] != "placed":
        logger.warning("event=refund_rejected order_id=%s reason=%s why=not_refundable", order_id, tag)
        raise ValueError("order is not refundable")
    order["status"] = "refunded"
    logger.info("event=order_refunded order_id=%s reason=%s", order_id, tag)
    return order
