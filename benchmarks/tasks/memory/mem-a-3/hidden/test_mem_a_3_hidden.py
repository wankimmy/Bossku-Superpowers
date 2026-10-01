import ast
import inspect
import os
import unittest
from datetime import datetime, timedelta, timezone

import sessions
from sessions import DEFAULT_TIMEOUT_MINUTES, create_session, default_clock, describe_age, is_expired


def _source_tree():
    path = os.path.abspath(sessions.__file__)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


def _now_like_calls_outside(tree, allowed_function_name):
    """Collect forbidden datetime.now()/utcnow()/date.today() calls outside one allowed function.

    Scoped per top-level function body (not a flat ast.walk skip) so a call legitimately
    made inside `allowed_function_name` isn't picked up again as a bare descendant node.
    """
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name == allowed_function_name:
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                if sub.func.attr in ("now", "utcnow", "today"):
                    hits.append(sub.func.attr)
    return hits


class SessionsHiddenTests(unittest.TestCase):

    def fixed_clock(self, when):
        return lambda: when

    # ---- session 1: create_session / default_clock ----

    def test_default_clock_is_timezone_aware(self):
        self.assertIsNotNone(default_clock().tzinfo)

    def test_default_clock_is_utc(self):
        now = default_clock()
        self.assertEqual(now.utcoffset(), timedelta(0))

    def test_create_session_uses_injected_clock(self):
        fixed = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(fixed))
        self.assertEqual(session["user_id"], "u1")
        self.assertEqual(session["created_at"], fixed)

    def test_create_session_created_at_is_timezone_aware(self):
        session = create_session("u1")
        self.assertIsNotNone(session["created_at"].tzinfo)

    # ---- session 2: is_expired ----

    def test_is_expired_false_before_timeout(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(minutes=29)
        self.assertFalse(is_expired(session, timeout_minutes=30, clock=self.fixed_clock(later)))

    def test_is_expired_true_after_timeout(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(minutes=31)
        self.assertTrue(is_expired(session, timeout_minutes=30, clock=self.fixed_clock(later)))

    def test_is_expired_boundary_counts_as_expired(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(minutes=30)
        self.assertTrue(is_expired(session, timeout_minutes=30, clock=self.fixed_clock(later)))

    def test_is_expired_uses_default_timeout(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(minutes=DEFAULT_TIMEOUT_MINUTES + 1)
        self.assertTrue(is_expired(session, clock=self.fixed_clock(later)))

    # ---- session 2: describe_age ----

    def test_describe_age_just_now(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(seconds=45)
        self.assertEqual(describe_age(session, clock=self.fixed_clock(later)), "just now")

    def test_describe_age_minutes_singular(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(minutes=1)
        self.assertEqual(describe_age(session, clock=self.fixed_clock(later)), "1 minute ago")

    def test_describe_age_minutes_plural(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(minutes=5)
        self.assertEqual(describe_age(session, clock=self.fixed_clock(later)), "5 minutes ago")

    def test_describe_age_hours(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(hours=2)
        self.assertEqual(describe_age(session, clock=self.fixed_clock(later)), "2 hours ago")

    def test_describe_age_days(self):
        start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        later = start + timedelta(days=3)
        self.assertEqual(describe_age(session, clock=self.fixed_clock(later)), "3 days ago")

    # ---- rule: timezone-aware UTC + injected clock ----

    def test_is_expired_accepts_clock_parameter(self):
        params = inspect.signature(is_expired).parameters
        self.assertIn("clock", params)

    def test_describe_age_accepts_clock_parameter(self):
        params = inspect.signature(describe_age).parameters
        self.assertIn("clock", params)

    def test_no_direct_now_calls_outside_default_clock(self):
        tree = _source_tree()
        hits = _now_like_calls_outside(tree, "default_clock")
        self.assertEqual(
            hits, [],
            "found a direct datetime.now()/utcnow()/date.today() call outside default_clock; "
            "new functions must take time through an injected clock",
        )

    def test_is_expired_ignores_wall_clock(self):
        # Even though the real wall clock has moved on, a session whose injected
        # clock never advances relative to created_at must never read as expired.
        start = datetime(2030, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        session = create_session("u1", clock=self.fixed_clock(start))
        same_time = self.fixed_clock(start)
        self.assertFalse(is_expired(session, timeout_minutes=30, clock=same_time))


if __name__ == "__main__":
    unittest.main()
