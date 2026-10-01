"""Core inventory primitives.

This module is already correct and in production use -- do not change its
behavior. It exists here so new features can reuse it instead of
re-deriving which lots are usable by hand.
"""
import datetime
from dataclasses import dataclass
from typing import Optional

import validation


@dataclass(frozen=True)
class Lot:
    """One physical batch of stock.

    Fields:
        lot_id: ``str`` unique identifier, used as a sort tie-break.
        sku: ``str`` the stock-keeping unit this lot holds.
        quantity_on_hand: ``int`` units currently in this lot (may be 0).
        received_at: ``datetime.datetime`` when this lot arrived.
        expires_on: ``datetime.date`` or ``None``. ``None`` means the lot
            never expires.
    """

    lot_id: str
    sku: str
    quantity_on_hand: int
    received_at: datetime.datetime
    expires_on: Optional[datetime.date]


@dataclass(frozen=True)
class OrderLine:
    """One line of a customer order: a SKU and the quantity requested."""

    sku: str
    quantity: int


def is_lot_expired(lot, as_of_date):
    """A lot is expired if ``expires_on`` is not ``None`` and is strictly
    before ``as_of_date``. A lot expiring exactly on ``as_of_date`` is
    NOT yet expired -- it's still usable that day.
    """
    validation.require_type("lot", lot, Lot)
    return lot.expires_on is not None and lot.expires_on < as_of_date


def available_lots_for_sku(lots, sku, as_of_date):
    """Return the lots of ``lots`` that hold ``sku``, have
    ``quantity_on_hand > 0``, and are not expired as of ``as_of_date``.

    Returned in no particular order -- callers that care about draw-down
    order (FIFO/LIFO/FEFO) must sort the result themselves.
    """
    validation.require_nonempty_str("sku", sku)
    validation.require_list_or_tuple("lots", lots)
    return [
        lot
        for lot in lots
        if lot.sku == sku
        and lot.quantity_on_hand > 0
        and not is_lot_expired(lot, as_of_date)
    ]
