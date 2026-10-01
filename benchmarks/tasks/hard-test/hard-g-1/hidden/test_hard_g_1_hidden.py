import dataclasses
import datetime
import logging
import unittest
from decimal import Decimal
from unittest import mock

import clock
import errors
import money
import sessions
import statements


def dt(day, hour, minute=0):
    return datetime.datetime(2024, 1, day, hour, minute)


class _ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class SessionsExistingBehaviorTests(unittest.TestCase):
    """sessions.py already works; these pin its behavior so it stays untouched."""

    def setUp(self):
        self.rc = sessions.RateCard(
            hourly_rate=Decimal("4.00"),
            max_fee=Decimal("24.00"),
            grace_minutes=10,
            round_increment_minutes=30,
        )

    def test_duration_under_grace_is_free(self):
        s = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 5))
        self.assertEqual(sessions.compute_session_fee(self.rc, s), Decimal("0.00"))

    def test_duration_exactly_at_grace_is_free(self):
        s = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 10))
        self.assertEqual(sessions.compute_session_fee(self.rc, s), Decimal("0.00"))

    def test_duration_just_over_grace_bills_one_increment(self):
        s = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 11))
        self.assertEqual(sessions.compute_session_fee(self.rc, s), Decimal("4.00"))

    def test_duration_exactly_on_increment_boundary(self):
        s = sessions.SessionRecord("a", dt(1, 0, 0), dt(1, 1, 0))  # 60 min
        self.assertEqual(sessions.compute_session_fee(self.rc, s), Decimal("4.00"))

    def test_duration_just_past_increment_boundary_rounds_to_next(self):
        s = sessions.SessionRecord("a", dt(1, 0, 0), dt(1, 1, 1))  # 61 min
        self.assertEqual(sessions.compute_session_fee(self.rc, s), Decimal("8.00"))

    def test_fee_capped_at_max_fee(self):
        s = sessions.SessionRecord("a", dt(1, 0, 0), dt(1, 10, 0))
        self.assertEqual(sessions.compute_session_fee(self.rc, s), Decimal("24.00"))

    def test_exit_equal_to_entry_raises(self):
        s = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 0))
        with self.assertRaises(errors.ValidationError):
            sessions.compute_session_fee(self.rc, s)

    def test_exit_before_entry_raises(self):
        s = sessions.SessionRecord("a", dt(1, 9, 30), dt(1, 9, 0))
        with self.assertRaises(errors.ValidationError):
            sessions.compute_session_fee(self.rc, s)

    def test_wrong_rate_card_type_raises_garage_error(self):
        s = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 30))
        with self.assertRaises(errors.GarageError):
            sessions.compute_session_fee("not-a-ratecard", s)

    def test_rate_card_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.rc.hourly_rate = Decimal("1.00")

    def test_session_record_is_frozen(self):
        s = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 30))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            s.vehicle_id = "b"


class BuildStatementBasicsTests(unittest.TestCase):
    def setUp(self):
        self.rc = sessions.RateCard(
            hourly_rate=Decimal("4.00"),
            max_fee=Decimal("24.00"),
            grace_minutes=10,
            round_increment_minutes=30,
        )

    def test_empty_sessions_non_member(self):
        stmt = statements.build_statement("acct2", [], self.rc, is_member=False)
        self.assertEqual(stmt.line_count, 0)
        self.assertEqual(stmt.gross_total, Decimal("0.00"))
        self.assertEqual(stmt.discount_percent, 0)
        self.assertEqual(stmt.discount_amount, Decimal("0.00"))
        self.assertEqual(stmt.statement_fee, Decimal("5.00"))
        self.assertEqual(stmt.final_total, Decimal("5.00"))
        self.assertEqual(stmt.lines, ())

    def test_empty_sessions_member_waives_fee(self):
        stmt = statements.build_statement("acct2", [], self.rc, is_member=True)
        self.assertEqual(stmt.statement_fee, Decimal("0.00"))
        self.assertEqual(stmt.final_total, Decimal("0.00"))

    def test_sessions_accepts_tuple_not_just_list(self):
        s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))
        stmt = statements.build_statement("acct1", (s,), self.rc)
        self.assertEqual(stmt.line_count, 1)

    def test_lines_sorted_by_entry_time_then_vehicle_id(self):
        zeta = sessions.SessionRecord("zeta", dt(1, 9, 0), dt(1, 9, 11))
        alpha = sessions.SessionRecord("alpha", dt(1, 9, 0), dt(1, 9, 11))
        mid = sessions.SessionRecord("mid", dt(1, 8, 0), dt(1, 10, 0))
        stmt = statements.build_statement("acct1", [zeta, alpha, mid], self.rc)
        self.assertEqual([l.vehicle_id for l in stmt.lines], ["mid", "alpha", "zeta"])
        self.assertEqual(stmt.gross_total, Decimal("16.00"))
        self.assertEqual(stmt.final_total, Decimal("21.00"))

    def test_lines_is_a_tuple_of_statementline(self):
        s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))
        stmt = statements.build_statement("acct1", [s], self.rc)
        self.assertIsInstance(stmt.lines, tuple)
        line = stmt.lines[0]
        self.assertEqual((line.vehicle_id, line.entry_time, line.exit_time, line.fee),
                          ("car1", dt(1, 9, 0), dt(1, 9, 11), Decimal("4.00")))

    def test_statement_is_frozen(self):
        stmt = statements.build_statement("acct1", [], self.rc)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            stmt.final_total = Decimal("0")

    def test_statement_line_is_frozen(self):
        s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))
        stmt = statements.build_statement("acct1", [s], self.rc)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            stmt.lines[0].fee = Decimal("0")

    def test_does_not_mutate_input_sessions_list_order(self):
        zeta = sessions.SessionRecord("zeta", dt(1, 9, 0), dt(1, 9, 11))
        alpha = sessions.SessionRecord("alpha", dt(1, 9, 0), dt(1, 9, 11))
        original = [zeta, alpha]
        statements.build_statement("acct1", original, self.rc)
        self.assertEqual([x.vehicle_id for x in original], ["zeta", "alpha"])

    def test_keyword_call_matches_documented_signature(self):
        s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))
        stmt = statements.build_statement(
            account_id="acct9", sessions=[s], rate_card=self.rc, is_member=True, clock=clock.FixedClock(datetime.date(2024, 6, 1))
        )
        self.assertEqual(stmt.account_id, "acct9")
        self.assertEqual(stmt.generated_on, datetime.date(2024, 6, 1))


class DiscountTierTests(unittest.TestCase):
    def _single_session_gross(self, hourly_rate, minutes=60):
        rc = sessions.RateCard(hourly_rate, Decimal("100000.00"), 0, 60)
        start = dt(1, 0, 0)
        s = sessions.SessionRecord("x", start, start + datetime.timedelta(minutes=minutes))
        return statements.build_statement("a", [s], rc)

    def test_below_fifty_no_discount(self):
        stmt = self._single_session_gross(Decimal("49.99"))
        self.assertEqual(stmt.discount_percent, 0)
        self.assertEqual(stmt.discount_amount, Decimal("0.00"))

    def test_exactly_fifty_is_five_percent_tier(self):
        stmt = self._single_session_gross(Decimal("50.00"))
        self.assertEqual(stmt.discount_percent, 5)
        self.assertEqual(stmt.discount_amount, Decimal("2.50"))
        self.assertEqual(stmt.final_total, Decimal("52.50"))

    def test_exactly_two_hundred_is_ten_percent_tier(self):
        stmt = self._single_session_gross(Decimal("200.00"))
        self.assertEqual(stmt.discount_percent, 10)
        self.assertEqual(stmt.discount_amount, Decimal("20.00"))
        self.assertEqual(stmt.final_total, Decimal("185.00"))

    def test_exactly_five_hundred_is_fifteen_percent_tier(self):
        stmt = self._single_session_gross(Decimal("500.00"))
        self.assertEqual(stmt.discount_percent, 15)
        self.assertEqual(stmt.discount_amount, Decimal("75.00"))
        self.assertEqual(stmt.final_total, Decimal("430.00"))

    def test_member_waives_statement_fee_at_top_tier(self):
        rc = sessions.RateCard(Decimal("500.00"), Decimal("100000.00"), 0, 60)
        start = dt(1, 0, 0)
        s = sessions.SessionRecord("x", start, start + datetime.timedelta(minutes=60))
        stmt = statements.build_statement("a", [s], rc, is_member=True)
        self.assertEqual(stmt.final_total, Decimal("425.00"))

    def test_discount_rounding_is_half_up_not_banker(self):
        rc = sessions.RateCard(Decimal("201.25"), Decimal("100000.00"), 0, 60)
        start = dt(1, 0, 0)
        s = sessions.SessionRecord("x", start, start + datetime.timedelta(minutes=60))
        stmt = statements.build_statement("a", [s], rc)
        self.assertEqual(stmt.gross_total, Decimal("201.25"))
        self.assertEqual(stmt.discount_percent, 10)
        # 201.25 * 10 / 100 = 20.125 exactly -- ROUND_HALF_UP must give 20.13,
        # not the 20.12 that Decimal's default ROUND_HALF_EVEN would give.
        self.assertEqual(stmt.discount_amount, Decimal("20.13"))
        self.assertEqual(stmt.final_total, Decimal("186.12"))


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.rc = sessions.RateCard(Decimal("4.00"), Decimal("24.00"), 10, 30)
        self.s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))

    def test_account_id_wrong_type_raises_with_prefix(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            statements.build_statement(123, [], self.rc)
        self.assertEqual(str(ctx.exception), "invalid: account_id must be a str")

    def test_account_id_empty_raises_with_prefix(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            statements.build_statement("   ", [], self.rc)
        self.assertEqual(str(ctx.exception), "invalid: account_id must not be empty")

    def test_sessions_wrong_type_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            statements.build_statement("a", "not-a-list", self.rc)
        self.assertEqual(str(ctx.exception), "invalid: sessions must be a list or tuple")

    def test_session_element_wrong_type_names_index(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            statements.build_statement("a", [self.s, "nope"], self.rc)
        self.assertEqual(str(ctx.exception), "invalid: sessions[1] must be a SessionRecord")

    def test_rate_card_wrong_type_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            statements.build_statement("a", [], "not-a-ratecard")
        self.assertEqual(str(ctx.exception), "invalid: rate_card must be a RateCard")

    def test_is_member_wrong_type_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            statements.build_statement("a", [], self.rc, is_member=1)
        self.assertEqual(str(ctx.exception), "invalid: is_member must be a bool")

    def test_all_validation_errors_are_garage_errors(self):
        with self.assertRaises(errors.GarageError):
            statements.build_statement("", [], self.rc)


class ClockAndLoggingTests(unittest.TestCase):
    def setUp(self):
        self.rc = sessions.RateCard(Decimal("4.00"), Decimal("24.00"), 10, 30)
        self.s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))
        self.logger = logging.getLogger("garage.statements")

    def test_injected_clock_is_used_and_called_exactly_once(self):
        class CountingClock:
            def __init__(self, value):
                self.calls = 0
                self.value = value

            def now(self):
                self.calls += 1
                return self.value

        cc = CountingClock(datetime.date(2024, 3, 3))
        stmt = statements.build_statement("a", [self.s], self.rc, clock=cc)
        self.assertEqual(cc.calls, 1)
        self.assertEqual(stmt.generated_on, datetime.date(2024, 3, 3))

    def test_default_clock_comes_from_clock_module(self):
        with mock.patch("clock.SystemClock") as fake_system:
            fake_system.return_value.now.return_value = datetime.date(2030, 5, 5)
            stmt = statements.build_statement("a", [self.s], self.rc)
        self.assertEqual(stmt.generated_on, datetime.date(2030, 5, 5))

    def test_success_logs_exactly_one_info_record_with_exact_message(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            statements.build_statement("acctX", [self.s], self.rc, is_member=False)
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 1)
        self.assertEqual(handler.records[0].levelname, "INFO")
        self.assertEqual(handler.records[0].getMessage(), "statement account=acctX sessions=1 total=$9.00")

    def test_failure_logs_nothing(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            with self.assertRaises(errors.ValidationError):
                statements.build_statement("", [self.s], self.rc)
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 0)


class ReuseTests(unittest.TestCase):
    """These confirm the new feature reuses the shared helpers rather than
    re-implementing their logic -- per this project's documented convention
    of calling sibling modules by their module-qualified name."""

    def setUp(self):
        self.rc = sessions.RateCard(Decimal("4.00"), Decimal("24.00"), 10, 30)
        self.s = sessions.SessionRecord("car1", dt(1, 9, 0), dt(1, 9, 11))

    def test_reuses_compute_session_fee_once_per_session(self):
        with mock.patch("sessions.compute_session_fee", wraps=sessions.compute_session_fee) as spy:
            statements.build_statement("a", [self.s], self.rc)
        self.assertEqual(spy.call_count, 1)
        called_rate_card, called_session = spy.call_args[0]
        self.assertIs(called_rate_card, self.rc)
        self.assertIs(called_session, self.s)

    def test_reuses_compute_session_fee_for_each_of_several_sessions(self):
        s2 = sessions.SessionRecord("car2", dt(1, 10, 0), dt(1, 10, 20))
        with mock.patch("sessions.compute_session_fee", wraps=sessions.compute_session_fee) as spy:
            statements.build_statement("a", [self.s, s2], self.rc)
        self.assertEqual(spy.call_count, 2)

    def test_reuses_round_money_for_the_discount_step(self):
        with mock.patch("money.round_money", wraps=money.round_money) as spy:
            statements.build_statement("a", [self.s], self.rc)
        # one call inside compute_session_fee, one for the discount amount,
        # and one inside money.format_money for the log line.
        self.assertEqual(spy.call_count, 3)

    def test_reuses_require_nonempty_str_for_account_id(self):
        import validation

        with mock.patch("validation.require_nonempty_str", wraps=validation.require_nonempty_str) as spy:
            statements.build_statement("a", [], self.rc)
        spy.assert_any_call("account_id", "a")

    def test_reuses_require_type_for_rate_card(self):
        import validation

        with mock.patch("validation.require_type", wraps=validation.require_type) as spy:
            statements.build_statement("a", [], self.rc)
        found = [c for c in spy.call_args_list if c.args[0] == "rate_card"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].args[1:], (self.rc, sessions.RateCard))

    def test_does_not_reimplement_discount_tiers_independently_of_gross_total(self):
        # Two different sets of sessions with the same gross_total must get
        # the same discount tier -- the tier is a function of gross_total
        # alone, not of how many lines or which vehicles produced it.
        rc = sessions.RateCard(Decimal("50.00"), Decimal("100000.00"), 0, 60)
        start = dt(1, 0, 0)
        one_session = [sessions.SessionRecord("a", start, start + datetime.timedelta(minutes=240))]  # 4h -> 200.00
        two_sessions = [
            sessions.SessionRecord("a", start, start + datetime.timedelta(minutes=120)),  # 2h -> 100.00
            sessions.SessionRecord("b", start, start + datetime.timedelta(minutes=120)),  # 2h -> 100.00
        ]
        stmt1 = statements.build_statement("a", one_session, rc)
        stmt2 = statements.build_statement("a", two_sessions, rc)
        self.assertEqual(stmt1.gross_total, stmt2.gross_total)
        self.assertEqual(stmt1.discount_percent, stmt2.discount_percent)
        self.assertEqual(stmt1.final_total, stmt2.final_total)


class IndependenceTests(unittest.TestCase):
    """No module-level state: consecutive calls must not leak into each other."""

    def test_two_calls_in_a_row_do_not_interfere(self):
        rc = sessions.RateCard(Decimal("4.00"), Decimal("24.00"), 10, 30)
        s_small = sessions.SessionRecord("a", dt(1, 9, 0), dt(1, 9, 11))
        s_big = sessions.SessionRecord("b", dt(1, 0, 0), dt(1, 10, 0))

        first = statements.build_statement("acct1", [s_small], rc, is_member=True)
        second = statements.build_statement("acct2", [s_big], rc, is_member=False)

        self.assertEqual(first.final_total, Decimal("4.00"))
        self.assertEqual(second.final_total, Decimal("29.00"))


if __name__ == "__main__":
    unittest.main()
