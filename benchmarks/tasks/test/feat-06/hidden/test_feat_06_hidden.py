import unittest

from retry import RetryPolicy


class FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def recording_sleep(clock):
    calls = []

    def sleep(seconds):
        calls.append(seconds)
        clock.advance(seconds)

    sleep.calls = calls
    return sleep


class FlakyCallsError(Exception):
    pass


def fails_n_times_then_returns(n, result, exc=FlakyCallsError):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= n:
            raise exc(f"attempt {state['calls']}")
        return result

    return fn


class DelayForTests(unittest.TestCase):
    def test_exponential_growth(self):
        policy = RetryPolicy(5, base_delay=1.0, multiplier=2.0)
        delays = [policy.delay_for(i) for i in (1, 2, 3, 4)]
        self.assertEqual(delays, [1.0, 2.0, 4.0, 8.0])

    def test_capped_at_max_delay(self):
        policy = RetryPolicy(6, base_delay=1.0, multiplier=2.0, max_delay=5.0)
        delays = [policy.delay_for(i) for i in (1, 2, 3, 4, 5)]
        self.assertEqual(delays, [1.0, 2.0, 4.0, 5.0, 5.0])


class ConstructionTests(unittest.TestCase):
    def test_invalid_arguments_raise(self):
        bad = [
            dict(max_attempts=0, base_delay=1.0),
            dict(max_attempts=-1, base_delay=1.0),
            dict(max_attempts=3, base_delay=-1.0),
            dict(max_attempts=3, base_delay=1.0, multiplier=0.5),
            dict(max_attempts=3, base_delay=5.0, max_delay=1.0),
        ]
        for kwargs in bad:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    RetryPolicy(**kwargs)


class CallTests(unittest.TestCase):
    def test_success_on_first_try_never_sleeps(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(3, base_delay=1.0, clock=clock, sleep=sleep)
        result = policy.call(lambda: 42)
        self.assertEqual(result, 42)
        self.assertEqual(sleep.calls, [])
        self.assertEqual(policy.attempts_used, 1)

    def test_retries_then_succeeds_sleeps_expected_delays(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(5, base_delay=1.0, multiplier=3.0,
                              retry_on=(FlakyCallsError,), clock=clock, sleep=sleep)
        fn = fails_n_times_then_returns(2, "done")
        result = policy.call(fn)
        self.assertEqual(result, "done")
        self.assertEqual(sleep.calls, [1.0, 3.0])
        self.assertEqual(policy.attempts_used, 3)

    def test_exhausting_attempts_reraises_original_exception_type(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(3, base_delay=1.0, retry_on=(FlakyCallsError,),
                              clock=clock, sleep=sleep)
        fn = fails_n_times_then_returns(10, "never")
        with self.assertRaises(FlakyCallsError):
            policy.call(fn)
        self.assertEqual(len(sleep.calls), 2)
        self.assertEqual(policy.attempts_used, 3)

    def test_non_retryable_exception_propagates_immediately(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(5, base_delay=1.0, retry_on=(ValueError,),
                              clock=clock, sleep=sleep)

        def fn():
            raise TypeError("nope")

        with self.assertRaises(TypeError):
            policy.call(fn)
        self.assertEqual(sleep.calls, [])
        self.assertEqual(policy.attempts_used, 1)

    def test_narrow_retry_on_stops_retrying_for_a_different_exception_type(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(5, base_delay=1.0, retry_on=(ValueError,),
                              clock=clock, sleep=sleep)
        state = {"calls": 0}

        def fn():
            state["calls"] += 1
            if state["calls"] == 1:
                raise ValueError("retryable")
            raise TypeError("not retryable")

        with self.assertRaises(TypeError):
            policy.call(fn)
        self.assertEqual(len(sleep.calls), 1)
        self.assertEqual(policy.attempts_used, 2)

    def test_attempts_used_resets_across_separate_calls(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(5, base_delay=1.0, retry_on=(FlakyCallsError,),
                              clock=clock, sleep=sleep)
        policy.call(fails_n_times_then_returns(2, "first"))
        self.assertEqual(policy.attempts_used, 3)
        policy.call(lambda: "second")
        self.assertEqual(policy.attempts_used, 1)

    def test_elapsed_matches_total_slept_time_on_the_fake_clock(self):
        clock = FakeClock(start=100.0)
        sleep = recording_sleep(clock)
        policy = RetryPolicy(5, base_delay=1.0, multiplier=3.0,
                              retry_on=(FlakyCallsError,), clock=clock, sleep=sleep)
        policy.call(fails_n_times_then_returns(2, "done"))
        self.assertEqual(policy.elapsed, 4.0)  # delay_for(1)=1.0, delay_for(2)=3.0

    def test_args_and_kwargs_are_forwarded_on_every_attempt(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(3, base_delay=1.0, clock=clock, sleep=sleep)

        def fn(a, b, x=None):
            return (a, b, x)

        self.assertEqual(policy.call(fn, 1, 2, x=3), (1, 2, 3))

    def test_max_attempts_one_never_sleeps_or_retries(self):
        clock = FakeClock()
        sleep = recording_sleep(clock)
        policy = RetryPolicy(1, base_delay=1.0, retry_on=(FlakyCallsError,),
                              clock=clock, sleep=sleep)
        with self.assertRaises(FlakyCallsError):
            policy.call(fails_n_times_then_returns(10, "never"))
        self.assertEqual(sleep.calls, [])
        self.assertEqual(policy.attempts_used, 1)


if __name__ == "__main__":
    unittest.main()
