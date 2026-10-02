import ast
import inspect
import os
import re
import unittest

import scheduler
from scheduler import Job, Scheduler


def _source_tree():
    path = os.path.abspath(scheduler.__file__)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


DURATION_WORD = re.compile(r"(delay|interval|timeout|wait|duration)", re.IGNORECASE)


class SchedulerFunctionalityTests(unittest.TestCase):
    # ---- session 1: add_job / due_jobs / cancel_job / next_job ----

    def test_due_jobs_basic(self):
        s = Scheduler()
        s.add_job(Job("j1", "first", 10))
        self.assertEqual([j.job_id for j in s.due_jobs(10)], ["j1"])
        self.assertEqual([j.job_id for j in s.due_jobs(5)], [])
        self.assertEqual([j.job_id for j in s.due_jobs(15)], ["j1"])

    def test_due_jobs_sorted_earliest_first(self):
        s = Scheduler()
        s.add_job(Job("j30", "c", 30))
        s.add_job(Job("j10", "a", 10))
        s.add_job(Job("j20", "b", 20))
        self.assertEqual([j.job_id for j in s.due_jobs(30)], ["j10", "j20", "j30"])

    def test_cancel_job_removes_it(self):
        s = Scheduler()
        s.add_job(Job("j1", "a", 10))
        s.cancel_job("j1")
        self.assertEqual(s.due_jobs(100), [])

    def test_cancel_job_missing_is_noop(self):
        s = Scheduler()
        s.cancel_job("nope")  # must not raise

    def test_next_job_returns_smallest_future(self):
        s = Scheduler()
        s.add_job(Job("past", "a", 5))
        s.add_job(Job("soon", "b", 15))
        s.add_job(Job("later", "c", 20))
        self.assertEqual(s.next_job(10).job_id, "soon")

    def test_next_job_none_when_no_upcoming(self):
        s = Scheduler()
        s.add_job(Job("past", "a", 5))
        self.assertIsNone(s.next_job(10))

    # ---- session 2: add_recurring_job / run_due / mark_failed ----

    def test_add_recurring_job_reschedules_after_firing(self):
        s = Scheduler()
        s.add_recurring_job(Job("r1", "ping", 100), 50)
        fired = s.run_due(100)
        self.assertEqual([j.job_id for j in fired], ["r1"])
        self.assertEqual(s.due_jobs(149), [])
        self.assertEqual([j.job_id for j in s.due_jobs(150)], ["r1"])

    def test_run_due_removes_one_off_after_firing(self):
        s = Scheduler()
        s.add_job(Job("o1", "once", 200))
        fired = s.run_due(200)
        self.assertEqual([j.job_id for j in fired], ["o1"])
        self.assertEqual(s.due_jobs(10000), [])

    def test_run_due_order_earliest_first(self):
        s = Scheduler()
        s.add_job(Job("b", "b", 5))
        s.add_job(Job("a", "a", 10))
        fired = s.run_due(10)
        self.assertEqual([j.job_id for j in fired], ["b", "a"])

    def test_run_due_returns_empty_when_nothing_due(self):
        s = Scheduler()
        s.add_job(Job("future", "f", 100))
        self.assertEqual(s.run_due(50), [])

    def test_mark_failed_reschedules_relative_to_current_run_at(self):
        s = Scheduler()
        s.add_job(Job("m1", "flaky", 100))
        s.mark_failed("m1", 30)
        self.assertEqual(s.due_jobs(129), [])
        self.assertEqual([j.job_id for j in s.due_jobs(130)], ["m1"])

    def test_mark_failed_does_not_change_job_name(self):
        s = Scheduler()
        s.add_job(Job("m1", "flaky", 100))
        s.mark_failed("m1", 30)
        job = s.due_jobs(130)[0]
        self.assertEqual(job.name, "flaky")


class DurationUnitRuleTests(unittest.TestCase):
    """The project rule: relative durations are int milliseconds, named `*_ms`."""

    def test_add_recurring_job_duration_param_ends_in_ms(self):
        name = self._duration_param_name(Scheduler.add_recurring_job, {"self", "job"})
        self.assertTrue(name.endswith("_ms"), f"param {name!r} should end in _ms")

    def test_mark_failed_duration_param_ends_in_ms(self):
        name = self._duration_param_name(Scheduler.mark_failed, {"self", "job_id"})
        self.assertTrue(name.endswith("_ms"), f"param {name!r} should end in _ms")

    def _duration_param_name(self, method, exclude):
        params = [p for p in inspect.signature(method).parameters if p not in exclude]
        assert len(params) == 1, f"expected exactly one extra parameter on {method}"
        return params[0]

    def test_no_duration_like_param_without_ms_suffix_anywhere(self):
        tree = _source_tree()
        offenders = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            args = node.args
            for arg in list(args.args) + list(args.kwonlyargs):
                if arg.arg in ("self", "job", "job_id"):
                    continue
                if DURATION_WORD.search(arg.arg) and not arg.arg.endswith("_ms"):
                    offenders.append((node.name, arg.arg))
        self.assertEqual(offenders, [], f"duration-like parameters missing _ms suffix: {offenders}")

    def test_rescheduled_run_at_stays_plain_int(self):
        s = Scheduler()
        s.add_recurring_job(Job("r1", "ping", 100), 50)
        fired = s.run_due(100)
        self.assertIsInstance(fired[0].run_at, int)
        s2 = Scheduler()
        s2.add_job(Job("m1", "flaky", 100))
        s2.mark_failed("m1", 30)
        self.assertIsInstance(s2.due_jobs(130)[0].run_at, int)


if __name__ == "__main__":
    unittest.main()
