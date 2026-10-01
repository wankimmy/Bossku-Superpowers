import datetime
import os
import sys
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import errors
import sessions


def _dt(hour, minute=0):
    return datetime.datetime(2024, 1, 1, hour, minute)


class ComputeSessionFeeTests(unittest.TestCase):
    """Shows the style this project expects: frozen dataclasses built
    directly, rate cards injected explicitly, and errors checked against
    the shared base class rather than a bare builtin exception."""

    def setUp(self):
        self.rate_card = sessions.RateCard(
            hourly_rate=Decimal("4.00"),
            max_fee=Decimal("24.00"),
            grace_minutes=10,
            round_increment_minutes=30,
        )

    def test_within_grace_period_is_free(self):
        session = sessions.SessionRecord("ABC123", _dt(9, 0), _dt(9, 10))
        self.assertEqual(sessions.compute_session_fee(self.rate_card, session), Decimal("0.00"))

    def test_just_over_grace_rounds_up_one_increment(self):
        session = sessions.SessionRecord("ABC123", _dt(9, 0), _dt(9, 11))
        self.assertEqual(sessions.compute_session_fee(self.rate_card, session), Decimal("4.00"))

    def test_fee_is_capped_at_max_fee(self):
        session = sessions.SessionRecord("ABC123", _dt(0, 0), _dt(10, 0))
        self.assertEqual(sessions.compute_session_fee(self.rate_card, session), Decimal("24.00"))

    def test_exit_before_entry_raises_validation_error(self):
        session = sessions.SessionRecord("ABC123", _dt(9, 30), _dt(9, 0))
        with self.assertRaises(errors.GarageError):
            sessions.compute_session_fee(self.rate_card, session)

    def test_rate_card_is_frozen(self):
        with self.assertRaises(FrozenInstanceError):
            self.rate_card.hourly_rate = Decimal("1.00")


if __name__ == "__main__":
    unittest.main()
