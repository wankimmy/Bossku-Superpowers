import ast
import os
import unittest

import runsched


def _tree():
    with open(os.path.abspath(runsched.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


from datetime import datetime, timedelta, timezone

import runsched as sched

KL = timezone(timedelta(hours=8))


class SchedHiddenTests(unittest.TestCase):
    def test_parse_iso_offset(self):
        dt = sched.parse_iso("2026-03-01T09:30:00+08:00")
        self.assertEqual(dt.utcoffset(), timedelta(0))
        self.assertEqual((dt.hour, dt.minute), (1, 30))

    def test_parse_iso_no_offset_is_utc(self):
        dt = sched.parse_iso("2026-03-01T09:30:00")
        self.assertEqual(dt.utcoffset(), timedelta(0))
        self.assertEqual(dt.hour, 9)

    def test_is_expired(self):
        now = sched.parse_iso("2026-03-01T10:00:00")
        self.assertTrue(sched.is_expired(sched.parse_iso("2026-03-01T09:00:00"), now))
        self.assertFalse(sched.is_expired(sched.parse_iso("2026-03-01T11:00:00"), now))

    def test_is_expired_default_now(self):
        self.assertTrue(sched.is_expired(sched.parse_iso("2001-01-01T00:00:00")))
        self.assertFalse(sched.is_expired(sched.parse_iso("2999-01-01T00:00:00")))

    def test_age_seconds(self):
        created = sched.parse_iso("2026-03-01T09:00:00")
        now = sched.parse_iso("2026-03-01T09:01:30")
        self.assertEqual(sched.age_seconds(created, now), 90.0)

    def test_age_seconds_default_now_works_with_aware_input(self):
        created = sched.parse_iso("2001-01-01T00:00:00")
        self.assertGreater(sched.age_seconds(created), 1e8)

    def test_next_run_value(self):
        last = sched.parse_iso("2026-03-01T09:00:00")
        self.assertEqual(sched.next_run(last, 6), sched.parse_iso("2026-03-01T15:00:00"))

    def test_next_run_result_is_utc_even_for_local_input(self):
        last = datetime(2026, 3, 1, 9, 0, tzinfo=KL)
        out = sched.next_run(last, 1)
        self.assertEqual(out.utcoffset(), timedelta(0))
        self.assertEqual((out.day, out.hour), (1, 2))

    # ---- rule: UTC-aware datetimes only ----

    def test_no_naive_clock_calls(self):
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                name = node.func.attr
                self.assertNotIn(name, ("utcnow", "today", "utcfromtimestamp"))
                if name == "now":
                    self.assertTrue(node.args or node.keywords, "datetime.now() needs a tz argument")


if __name__ == "__main__":
    unittest.main()
