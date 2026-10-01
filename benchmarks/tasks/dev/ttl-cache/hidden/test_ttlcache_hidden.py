import unittest
from ttlcache import TTLCache


class FakeClock:
    def __init__(self, now=1000.0):
        self.now = now

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class TTLCacheTests(unittest.TestCase):
    def make(self, maxsize=3, ttl=10):
        clock = FakeClock()
        return TTLCache(maxsize, ttl, clock=clock), clock

    def test_set_and_get(self):
        cache, _ = self.make()
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)

    def test_missing_key_returns_default(self):
        cache, _ = self.make()
        self.assertIsNone(cache.get("x"))
        self.assertEqual(cache.get("x", 5), 5)

    def test_expires_after_ttl(self):
        cache, clock = self.make(ttl=10)
        cache.set("a", 1)
        clock.advance(9.9)
        self.assertEqual(cache.get("a"), 1)
        clock.advance(0.2)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("a", "gone"), "gone")

    def test_get_does_not_extend_ttl(self):
        cache, clock = self.make(ttl=10)
        cache.set("a", 1)
        clock.advance(6)
        self.assertEqual(cache.get("a"), 1)
        clock.advance(5)
        self.assertIsNone(cache.get("a"))

    def test_contains_and_len_ignore_expired(self):
        cache, clock = self.make(ttl=10)
        cache.set("a", 1)
        clock.advance(6)
        cache.set("b", 2)
        self.assertEqual(len(cache), 2)
        clock.advance(5)
        self.assertNotIn("a", cache)
        self.assertIn("b", cache)
        self.assertEqual(len(cache), 1)

    def test_overwrite_restarts_ttl(self):
        cache, clock = self.make(ttl=10)
        cache.set("a", 1)
        clock.advance(8)
        cache.set("a", 2)
        clock.advance(8)
        self.assertEqual(cache.get("a"), 2)

    def test_lru_eviction_uses_get_as_use(self):
        cache, _ = self.make(maxsize=3)
        for key in "abc":
            cache.set(key, key.upper())
        self.assertEqual(cache.get("a"), "A")
        cache.set("d", "D")
        self.assertNotIn("b", cache)
        for key in "acd":
            self.assertIn(key, cache)
        self.assertEqual(len(cache), 3)

    def test_overwriting_a_key_does_not_evict_and_counts_as_use(self):
        cache, _ = self.make(maxsize=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("a", 10)
        self.assertEqual(len(cache), 2)
        cache.set("c", 3)
        self.assertNotIn("b", cache)
        self.assertEqual(cache.get("a"), 10)
        self.assertEqual(cache.get("c"), 3)

    def test_expired_entries_never_push_out_live_ones(self):
        cache, clock = self.make(maxsize=2, ttl=10)
        cache.set("a", 1)            # expires at t=10
        clock.advance(1)
        cache.set("b", 2)            # expires at t=11
        self.assertEqual(cache.get("a"), 1)   # a is now the most recently used
        clock.advance(9.5)           # t=10.5: a expired, b still alive
        cache.set("c", 3)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        self.assertEqual(len(cache), 2)

    def test_purge_returns_number_removed(self):
        cache, clock = self.make(maxsize=5, ttl=10)
        cache.set("a", 1)
        cache.set("b", 2)
        clock.advance(6)
        cache.set("c", 3)
        clock.advance(5)
        self.assertEqual(cache.purge(), 2)
        self.assertEqual(cache.purge(), 0)
        self.assertEqual(len(cache), 1)
        self.assertEqual(cache.get("c"), 3)

    def test_invalid_arguments(self):
        for maxsize, ttl in [(0, 1), (-1, 1), (1, 0), (1, -5)]:
            with self.subTest(maxsize=maxsize, ttl=ttl):
                with self.assertRaises(ValueError):
                    TTLCache(maxsize, ttl)

    def test_falsy_values_are_real_values(self):
        cache, _ = self.make()
        cache.set("zero", 0)
        cache.set("none", None)
        self.assertEqual(cache.get("zero", "dflt"), 0)
        self.assertIn("none", cache)
        self.assertIsNone(cache.get("none", "dflt"))

    def test_default_clock_works(self):
        cache = TTLCache(2, 60)
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(len(cache), 1)

    def test_maxsize_one(self):
        cache, _ = self.make(maxsize=1)
        cache.set("a", 1)
        cache.set("b", 2)
        self.assertNotIn("a", cache)
        self.assertEqual(cache.get("b"), 2)


if __name__ == "__main__":
    unittest.main()
