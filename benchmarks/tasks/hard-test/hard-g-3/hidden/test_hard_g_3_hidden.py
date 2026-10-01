import dataclasses
import datetime
import logging
import unittest
from unittest import mock

import allocation
import clock
import errors
import inventory


def L(lot_id, sku, qty, received_day, expires=None):
    return inventory.Lot(
        lot_id=lot_id,
        sku=sku,
        quantity_on_hand=qty,
        received_at=datetime.datetime(2024, 1, received_day),
        expires_on=expires,
    )


def OL(sku, qty):
    return inventory.OrderLine(sku=sku, quantity=qty)


TODAY = datetime.date(2024, 6, 1)


class _ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class InventoryExistingBehaviorTests(unittest.TestCase):
    """inventory.py already works; these pin its behavior so it stays untouched."""

    def test_excludes_zero_quantity_lots(self):
        lots = [L("L1", "W", 0, 1)]
        self.assertEqual(inventory.available_lots_for_sku(lots, "W", TODAY), [])

    def test_excludes_expired_lots(self):
        lots = [L("L1", "W", 5, 1, datetime.date(2024, 1, 1))]
        self.assertEqual(inventory.available_lots_for_sku(lots, "W", TODAY), [])

    def test_lot_expiring_today_is_not_expired(self):
        lot = L("L1", "W", 5, 1, TODAY)
        self.assertFalse(inventory.is_lot_expired(lot, TODAY))

    def test_lot_expiring_yesterday_is_expired(self):
        lot = L("L1", "W", 5, 1, TODAY - datetime.timedelta(days=1))
        self.assertTrue(inventory.is_lot_expired(lot, TODAY))

    def test_wrong_lot_type_raises_warehouse_error(self):
        with self.assertRaises(errors.WarehouseError):
            inventory.is_lot_expired("not-a-lot", TODAY)

    def test_lot_is_frozen(self):
        lot = L("L1", "W", 5, 1)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            lot.quantity_on_hand = 0

    def test_order_line_is_frozen(self):
        line = OL("W", 1)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            line.quantity = 2


class StrategyOrderingTests(unittest.TestCase):
    def setUp(self):
        self.lots = [L("L1", "W", 5, 1), L("L2", "W", 5, 2), L("L3", "W", 5, 3)]

    def test_fifo_draws_oldest_received_first(self):
        r = allocation.allocate_order([OL("W", 12)], self.lots, strategy="FIFO", clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].lot_allocations, (("L1", 5), ("L2", 5), ("L3", 2)))

    def test_lifo_draws_newest_received_first(self):
        r = allocation.allocate_order([OL("W", 12)], self.lots, strategy="LIFO", clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].lot_allocations, (("L3", 5), ("L2", 5), ("L1", 2)))

    def test_default_strategy_is_fifo(self):
        r = allocation.allocate_order([OL("W", 12)], self.lots, clock=clock.FixedClock(TODAY))
        self.assertEqual(r.strategy, "FIFO")
        self.assertEqual(r.lines[0].lot_allocations, (("L1", 5), ("L2", 5), ("L3", 2)))

    def test_lot_never_drawn_from_is_absent_from_result(self):
        r = allocation.allocate_order([OL("W", 7)], self.lots, strategy="FIFO", clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].lot_allocations, (("L1", 5), ("L2", 2)))
        self.assertEqual(r.lines[0].allocated_quantity, 7)
        self.assertEqual(r.lines[0].backorder_quantity, 0)

    def test_fifo_tie_break_alphabetical_by_lot_id(self):
        tied = [L("Zeta", "W", 5, 1), L("Alpha", "W", 5, 1)]
        r = allocation.allocate_order([OL("W", 8)], tied, strategy="FIFO", clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].lot_allocations, (("Alpha", 5), ("Zeta", 3)))

    def test_fefo_draws_soonest_expiry_first(self):
        lots = [
            L("Never2", "F", 5, 1, None),
            L("Never1", "F", 5, 5, None),
            L("Soon", "F", 5, 2, datetime.date(2024, 6, 10)),
            L("Later", "F", 5, 3, datetime.date(2024, 7, 1)),
        ]
        r = allocation.allocate_order([OL("F", 20)], lots, strategy="FEFO", clock=clock.FixedClock(TODAY))
        self.assertEqual([lot_id for lot_id, _ in r.lines[0].lot_allocations], ["Soon", "Later", "Never1", "Never2"])

    def test_fefo_none_expiry_tie_break_is_lot_id_not_received_at(self):
        # Never1 arrived later (day 5) than Never2 (day 1), but since both
        # never expire, the tie-break must be lot_id alone: Never1 < Never2.
        lots = [L("Never2", "F", 5, 1, None), L("Never1", "F", 5, 5, None)]
        r = allocation.allocate_order([OL("F", 10)], lots, strategy="FEFO", clock=clock.FixedClock(TODAY))
        self.assertEqual([lot_id for lot_id, _ in r.lines[0].lot_allocations], ["Never1", "Never2"])

    def test_expired_lots_excluded_under_every_strategy(self):
        lots = [
            L("Expired", "E", 5, 1, datetime.date(2024, 5, 1)),
            L("Today", "E", 5, 2, TODAY),
            L("Future", "E", 5, 3, datetime.date(2024, 12, 1)),
        ]
        for strategy in ("FIFO", "LIFO", "FEFO"):
            with self.subTest(strategy=strategy):
                r = allocation.allocate_order(
                    [OL("E", 15)], lots, strategy=strategy, clock=clock.FixedClock(TODAY)
                )
                used = {lot_id for lot_id, _ in r.lines[0].lot_allocations}
                self.assertNotIn("Expired", used)
                self.assertEqual(r.lines[0].allocated_quantity, 10)
                self.assertEqual(r.lines[0].backorder_quantity, 5)


class PartialAndFullModeTests(unittest.TestCase):
    def test_shortfall_becomes_backorder_by_default(self):
        lots = [L("S1", "SHORT", 3, 1)]
        r = allocation.allocate_order([OL("SHORT", 10)], lots, clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].allocated_quantity, 3)
        self.assertEqual(r.lines[0].backorder_quantity, 7)

    def test_allocated_plus_backorder_always_equals_requested(self):
        lots = [L("S1", "SHORT", 3, 1)]
        for qty in (1, 3, 4, 10):
            with self.subTest(qty=qty):
                r = allocation.allocate_order([OL("SHORT", qty)], lots, clock=clock.FixedClock(TODAY))
                line = r.lines[0]
                self.assertEqual(line.allocated_quantity + line.backorder_quantity, qty)

    def test_allow_partial_false_raises_naming_first_failing_line_in_order(self):
        stock = [L("S1", "ZEBRA", 2, 1), L("S2", "APPLE", 2, 1)]
        with self.assertRaises(errors.InsufficientStockError) as ctx:
            allocation.allocate_order(
                [OL("ZEBRA", 10), OL("APPLE", 10)], stock, allow_partial=False, clock=clock.FixedClock(TODAY)
            )
        self.assertEqual(str(ctx.exception), "insufficient_stock: ZEBRA cannot be fully allocated")

        with self.assertRaises(errors.InsufficientStockError) as ctx:
            allocation.allocate_order(
                [OL("APPLE", 10), OL("ZEBRA", 10)], stock, allow_partial=False, clock=clock.FixedClock(TODAY)
            )
        self.assertEqual(str(ctx.exception), "insufficient_stock: APPLE cannot be fully allocated")

    def test_allow_partial_false_fails_even_if_other_lines_are_fully_stocked(self):
        stock = [L("S1", "OK", 10, 1), L("S2", "SHORT", 3, 1)]
        with self.assertRaises(errors.InsufficientStockError):
            allocation.allocate_order(
                [OL("OK", 5), OL("SHORT", 10)], stock, allow_partial=False, clock=clock.FixedClock(TODAY)
            )

    def test_allow_partial_false_succeeds_with_zero_backorder_when_satisfiable(self):
        stock = [L("S1", "OK", 10, 1)]
        r = allocation.allocate_order([OL("OK", 5)], stock, allow_partial=False, clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].backorder_quantity, 0)
        self.assertEqual(r.lines[0].allocated_quantity, 5)

    def test_insufficient_stock_error_is_warehouse_error_but_not_validation_error(self):
        self.assertTrue(issubclass(errors.InsufficientStockError, errors.WarehouseError))
        self.assertFalse(issubclass(errors.InsufficientStockError, errors.ValidationError))


class OutputShapeTests(unittest.TestCase):
    def test_lines_preserve_input_order_not_sorted(self):
        lines = [OL("ZZZ", 1), OL("AAA", 1)]
        lots = [L("L1", "ZZZ", 5, 1), L("L2", "AAA", 5, 1)]
        r = allocation.allocate_order(lines, lots, clock=clock.FixedClock(TODAY))
        self.assertEqual([line.sku for line in r.lines], ["ZZZ", "AAA"])

    def test_lot_allocations_is_tuple_of_plain_tuples(self):
        lots = [L("L1", "W", 5, 1)]
        r = allocation.allocate_order([OL("W", 3)], lots, clock=clock.FixedClock(TODAY))
        self.assertIsInstance(r.lines[0].lot_allocations, tuple)
        self.assertEqual(r.lines[0].lot_allocations[0], ("L1", 3))
        self.assertNotIsInstance(r.lines[0].lot_allocations[0], inventory.Lot)

    def test_allocation_result_is_frozen(self):
        r = allocation.allocate_order([OL("W", 1)], [L("L1", "W", 5, 1)], clock=clock.FixedClock(TODAY))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.strategy = "LIFO"

    def test_allocation_line_is_frozen(self):
        r = allocation.allocate_order([OL("W", 1)], [L("L1", "W", 5, 1)], clock=clock.FixedClock(TODAY))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.lines[0].allocated_quantity = 0

    def test_keyword_call_matches_documented_signature(self):
        r = allocation.allocate_order(
            order_lines=[OL("W", 1)],
            lots=[L("L1", "W", 5, 1)],
            strategy="LIFO",
            allow_partial=True,
            clock=clock.FixedClock(datetime.date(2024, 8, 8)),
        )
        self.assertEqual(r.allocation_date, datetime.date(2024, 8, 8))
        self.assertEqual(r.strategy, "LIFO")


class ValidationTests(unittest.TestCase):
    def test_order_lines_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order("not-a-list", [])
        self.assertEqual(str(ctx.exception), "invalid: order_lines must be a list or tuple")

    def test_order_lines_empty_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([], [])
        self.assertEqual(str(ctx.exception), "invalid: order_lines must not be empty")

    def test_order_line_element_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 1), "nope"], [])
        self.assertEqual(str(ctx.exception), "invalid: order_lines[1] must be a OrderLine")

    def test_quantity_zero_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 0)], [])
        self.assertEqual(str(ctx.exception), "invalid: order_lines[0].quantity must be a positive int")

    def test_quantity_bool_rejected(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", True)], [])
        self.assertEqual(str(ctx.exception), "invalid: order_lines[0].quantity must be a int")

    def test_duplicate_sku_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 1), OL("A", 2)], [])
        self.assertEqual(str(ctx.exception), "invalid: duplicate order line for sku A")

    def test_lots_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 1)], "not-a-list")
        self.assertEqual(str(ctx.exception), "invalid: lots must be a list or tuple")

    def test_lot_element_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 1)], ["nope"])
        self.assertEqual(str(ctx.exception), "invalid: lots[0] must be a Lot")

    def test_strategy_invalid_value_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 1)], [], strategy="BOGUS")
        self.assertEqual(str(ctx.exception), "invalid: strategy must be one of FIFO, LIFO, FEFO")

    def test_allow_partial_wrong_type_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            allocation.allocate_order([OL("A", 1)], [], allow_partial="yes")
        self.assertEqual(str(ctx.exception), "invalid: allow_partial must be a bool")

    def test_empty_lots_is_valid_and_fully_backorders(self):
        r = allocation.allocate_order([OL("A", 5)], [], clock=clock.FixedClock(TODAY))
        self.assertEqual(r.lines[0].allocated_quantity, 0)
        self.assertEqual(r.lines[0].backorder_quantity, 5)

    def test_all_validation_errors_are_warehouse_errors(self):
        with self.assertRaises(errors.WarehouseError):
            allocation.allocate_order([], [])


class ClockLoggingReuseMutationTests(unittest.TestCase):
    def setUp(self):
        self.stock = [L("S1", "OK", 10, 1), L("S2", "SHORT", 3, 1)]
        self.logger = logging.getLogger("warehouse.allocation")

    def test_clock_called_exactly_once(self):
        class CountingClock:
            def __init__(self, value):
                self.calls = 0
                self.value = value

            def now(self):
                self.calls += 1
                return self.value

        cc = CountingClock(TODAY)
        r = allocation.allocate_order([OL("OK", 2)], self.stock, clock=cc)
        self.assertEqual(cc.calls, 1)
        self.assertEqual(r.allocation_date, TODAY)

    def test_default_clock_comes_from_clock_module(self):
        with mock.patch("clock.SystemClock") as fake_system:
            fake_system.return_value.now.return_value = datetime.date(2031, 1, 1)
            r = allocation.allocate_order([OL("OK", 2)], self.stock)
        self.assertEqual(r.allocation_date, datetime.date(2031, 1, 1))

    def test_success_logs_exactly_one_info_record_with_exact_message(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            allocation.allocate_order([OL("SHORT", 10), OL("OK", 2)], self.stock, clock=clock.FixedClock(TODAY))
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 1)
        self.assertEqual(handler.records[0].levelname, "INFO")
        self.assertEqual(
            handler.records[0].getMessage(), "allocation lines=2 strategy=FIFO backordered=7"
        )

    def test_failure_logs_nothing_on_validation_error(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            with self.assertRaises(errors.ValidationError):
                allocation.allocate_order([], [])
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 0)

    def test_failure_logs_nothing_on_insufficient_stock(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            with self.assertRaises(errors.InsufficientStockError):
                allocation.allocate_order(
                    [OL("SHORT", 10)], self.stock, allow_partial=False, clock=clock.FixedClock(TODAY)
                )
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 0)

    def test_reuses_available_lots_for_sku_once_per_line(self):
        with mock.patch("inventory.available_lots_for_sku", wraps=inventory.available_lots_for_sku) as spy:
            allocation.allocate_order(
                [OL("OK", 2), OL("SHORT", 1)], self.stock, clock=clock.FixedClock(TODAY)
            )
        self.assertEqual(spy.call_count, 2)
        self.assertEqual(spy.call_args_list[0].args, (self.stock, "OK", TODAY))

    def test_does_not_mutate_lots_or_order_lines(self):
        lots = [L("S1", "OK", 10, 1)]
        lines = [OL("OK", 5)]
        allocation.allocate_order(lines, lots, clock=clock.FixedClock(TODAY))
        self.assertEqual(lots[0].quantity_on_hand, 10)
        self.assertEqual(lines[0].quantity, 5)


if __name__ == "__main__":
    unittest.main()
