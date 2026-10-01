"""Order allocation, built on top of inventory.available_lots_for_sku."""
import datetime
import logging
from dataclasses import dataclass

import clock as clock_module
import errors
import inventory
import validation

_LOGGER = logging.getLogger("warehouse.allocation")

_STRATEGIES = ("FIFO", "LIFO", "FEFO")


@dataclass(frozen=True)
class AllocationLine:
    sku: str
    requested_quantity: int
    allocated_quantity: int
    backorder_quantity: int
    lot_allocations: tuple


@dataclass(frozen=True)
class AllocationResult:
    allocation_date: object
    strategy: str
    lines: tuple


def _sorted_eligible(eligible_lots, strategy):
    """Put eligible lots into draw-down order for ``strategy``.

    LIFO needs a descending primary key with an ascending lot_id
    tie-break, which a single tuple key can't express directly (reversing
    the whole tuple would also reverse the tie-break). Instead this sorts
    by the tie-break first, then stable-sorts by the primary key -- the
    second (stable) sort preserves the first sort's relative order among
    ties, giving exactly "descending received_at, ascending lot_id".
    """
    if strategy == "FIFO":
        return sorted(eligible_lots, key=lambda lot: (lot.received_at, lot.lot_id))
    if strategy == "LIFO":
        by_lot_id = sorted(eligible_lots, key=lambda lot: lot.lot_id)
        return sorted(by_lot_id, key=lambda lot: lot.received_at, reverse=True)
    # FEFO: dated lots first (ascending expires_on), None-expiry lots last,
    # each group tie-broken by lot_id -- all ascending, so one tuple key
    # works. Every None-expiry lot uses the same placeholder (date.max) so
    # that group's order is decided purely by lot_id, never by received_at.
    return sorted(
        eligible_lots,
        key=lambda lot: (
            lot.expires_on is None,
            lot.expires_on if lot.expires_on is not None else datetime.date.max,
            lot.lot_id,
        ),
    )


def _draw_plan(eligible_lots_sorted, quantity_needed):
    lot_allocations = []
    remaining = quantity_needed
    for lot in eligible_lots_sorted:
        if remaining <= 0:
            break
        take = min(remaining, lot.quantity_on_hand)
        if take > 0:
            lot_allocations.append((lot.lot_id, take))
            remaining -= take
    allocated = quantity_needed - remaining
    return tuple(lot_allocations), allocated, remaining


def allocate_order(order_lines, lots, strategy="FIFO", allow_partial=True, clock=None):
    validation.require_nonempty_sequence("order_lines", order_lines)
    for index, line in enumerate(order_lines):
        validation.require_type(f"order_lines[{index}]", line, inventory.OrderLine)
        validation.require_positive_int(f"order_lines[{index}].quantity", line.quantity)
    validation.require_list_or_tuple("lots", lots)
    for index, lot in enumerate(lots):
        validation.require_type(f"lots[{index}]", lot, inventory.Lot)
    if strategy not in _STRATEGIES:
        raise errors.ValidationError(
            f"invalid: strategy must be one of {', '.join(_STRATEGIES)}"
        )
    validation.require_type("allow_partial", allow_partial, bool)

    seen_skus = set()
    for line in order_lines:
        if line.sku in seen_skus:
            raise errors.ValidationError(f"invalid: duplicate order line for sku {line.sku}")
        seen_skus.add(line.sku)

    active_clock = clock if clock is not None else clock_module.SystemClock()
    as_of_date = active_clock.now()

    plans = {}
    for line in order_lines:
        eligible = inventory.available_lots_for_sku(lots, line.sku, as_of_date)
        eligible_sorted = _sorted_eligible(eligible, strategy)
        plans[line.sku] = _draw_plan(eligible_sorted, line.quantity)

    if not allow_partial:
        for line in order_lines:
            _, allocated, remaining = plans[line.sku]
            if remaining > 0:
                raise errors.InsufficientStockError(
                    f"insufficient_stock: {line.sku} cannot be fully allocated"
                )

    result_lines = []
    total_backordered = 0
    for line in order_lines:
        lot_allocations, allocated, remaining = plans[line.sku]
        total_backordered += remaining
        result_lines.append(
            AllocationLine(
                sku=line.sku,
                requested_quantity=line.quantity,
                allocated_quantity=allocated,
                backorder_quantity=remaining,
                lot_allocations=lot_allocations,
            )
        )

    _LOGGER.info(
        f"allocation lines={len(order_lines)} strategy={strategy} "
        f"backordered={total_backordered}"
    )

    return AllocationResult(
        allocation_date=as_of_date,
        strategy=strategy,
        lines=tuple(result_lines),
    )
