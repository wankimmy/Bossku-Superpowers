import datetime
import os
import sys
import unittest
from dataclasses import FrozenInstanceError

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import errors
import inventory


class AvailableLotsForSkuTests(unittest.TestCase):
    """Shows the style this project expects: frozen dataclasses built
    directly, dates injected explicitly (never read from the real clock
    in a test), and errors checked against the shared base class."""

    def setUp(self):
        self.today = datetime.date(2024, 6, 1)
        self.fresh = inventory.Lot(
            lot_id="L1", sku="WIDGET", quantity_on_hand=10,
            received_at=datetime.datetime(2024, 1, 1), expires_on=datetime.date(2024, 12, 31),
        )
        self.expired = inventory.Lot(
            lot_id="L2", sku="WIDGET", quantity_on_hand=5,
            received_at=datetime.datetime(2024, 1, 2), expires_on=datetime.date(2024, 1, 1),
        )
        self.empty = inventory.Lot(
            lot_id="L3", sku="WIDGET", quantity_on_hand=0,
            received_at=datetime.datetime(2024, 1, 3), expires_on=None,
        )

    def test_excludes_expired_lots(self):
        result = inventory.available_lots_for_sku(
            [self.fresh, self.expired, self.empty], "WIDGET", self.today
        )
        self.assertEqual([lot.lot_id for lot in result], ["L1"])

    def test_lot_expiring_today_is_not_yet_expired(self):
        lot = inventory.Lot(
            lot_id="L4", sku="GIZMO", quantity_on_hand=3,
            received_at=datetime.datetime(2024, 1, 1), expires_on=self.today,
        )
        self.assertFalse(inventory.is_lot_expired(lot, self.today))

    def test_wrong_lot_type_raises_warehouse_error(self):
        with self.assertRaises(errors.WarehouseError):
            inventory.is_lot_expired("not-a-lot", self.today)

    def test_lot_is_frozen(self):
        with self.assertRaises(FrozenInstanceError):
            self.fresh.quantity_on_hand = 0


if __name__ == "__main__":
    unittest.main()
