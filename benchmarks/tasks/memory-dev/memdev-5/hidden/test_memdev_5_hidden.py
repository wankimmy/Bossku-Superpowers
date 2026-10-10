import ast
import os
import unittest

import cache


def _tree():
    with open(os.path.abspath(cache.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


import cache

_DURATION_WORDS = ("TTL", "TIMEOUT", "DELAY", "BACKOFF", "INTERVAL", "WAIT", "DURATION", "EXPIR")


def _duration_constants():
    found = {}
    for node in _tree().body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, (int, float)) and not isinstance(node.value.value, bool):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper() \
                        and any(w in target.id for w in _DURATION_WORDS):
                    found[target.id] = node.value.value
    return found


class CacheHiddenTests(unittest.TestCase):
    def test_ttl_cache(self):
        now = [0.0]
        c = cache.TTLCache(10, clock=lambda: now[0])
        c.set("a", 1)
        now[0] = 9
        self.assertEqual(c.get("a"), 1)
        now[0] = 11
        self.assertIsNone(c.get("a"))
        self.assertEqual(c.get("a", "d"), "d")

    def test_retry_succeeds_after_failures(self):
        calls, waits = [], []

        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise RuntimeError("boom")
            return "ok"

        self.assertEqual(cache.fetch_with_retry(flaky, sleep=waits.append), "ok")
        self.assertEqual(waits, [2, 2])

    def test_retry_gives_up_and_reraises(self):
        waits = []

        def bad():
            raise KeyError("nope")

        with self.assertRaises(KeyError):
            cache.fetch_with_retry(bad, attempts=2, sleep=waits.append)
        self.assertEqual(waits, [2])

    def test_constants_exist_with_seconds_values(self):
        consts = _duration_constants()
        self.assertIn(300, consts.values())
        self.assertIn(2, consts.values())
        self.assertIn(30, consts.values())

    # ---- rule: every duration constant ends in _SECONDS ----

    def test_duration_constants_use_seconds_suffix(self):
        consts = _duration_constants()
        self.assertGreaterEqual(len(consts), 3)
        for name in consts:
            self.assertTrue(name.endswith("_SECONDS"), name)
        # a value of 30000 / 120 under a *_SECONDS name would mean milliseconds or minutes
        for name, value in consts.items():
            self.assertLessEqual(value, 3600, name)


if __name__ == "__main__":
    unittest.main()
