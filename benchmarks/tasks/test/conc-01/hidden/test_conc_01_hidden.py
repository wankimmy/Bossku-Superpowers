import threading
import unittest

from workqueue import BoundedQueue, Full, Empty


def _call_with_timeout(fn, timeout, fail_fn, message):
    """Run fn() on a daemon thread; fail_fn(message) if it does not finish in time.

    Using a daemon thread means that even if fn() hangs forever (e.g. a deadlock
    in the code under test), this helper - and the test process - can still move on.
    """
    box = {}

    def runner():
        box["result"] = fn()

    t = threading.Thread(target=runner, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        fail_fn(message)
    return box.get("result")


class SingleThreadedTests(unittest.TestCase):
    def test_put_then_get_fifo_order(self):
        q = BoundedQueue(3)
        q.put("a")
        q.put("b")
        q.put("c")
        self.assertEqual(q.get(), "a")
        self.assertEqual(q.get(), "b")
        self.assertEqual(q.get(), "c")

    def test_qsize_tracks_contents(self):
        q = BoundedQueue(3)
        self.assertEqual(q.qsize(), 0)
        q.put(1)
        q.put(2)
        self.assertEqual(q.qsize(), 2)
        q.get()
        self.assertEqual(q.qsize(), 1)

    def test_put_nowait_raises_full(self):
        q = BoundedQueue(2)
        q.put_nowait(1)
        q.put_nowait(2)
        with self.assertRaises(Full):
            q.put_nowait(3)
        self.assertEqual(q.qsize(), 2)

    def test_get_nowait_raises_empty(self):
        q = BoundedQueue(2)
        with self.assertRaises(Empty):
            q.get_nowait()

    def test_get_nowait_returns_front_item(self):
        q = BoundedQueue(2)
        q.put_nowait("x")
        q.put_nowait("y")
        self.assertEqual(q.get_nowait(), "x")

    def test_interleaved_put_and_get_preserves_fifo_order(self):
        q = BoundedQueue(5)
        q.put(1)
        q.put(2)
        self.assertEqual(q.get(), 1)
        q.put(3)
        self.assertEqual(q.get(), 2)
        self.assertEqual(q.get(), 3)

    def test_invalid_maxsize_raises(self):
        for bad in (0, -1, 1.5, "3"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    BoundedQueue(bad)


class BlockingTests(unittest.TestCase):
    def test_put_blocks_when_full_until_get_frees_space(self):
        q = BoundedQueue(2)
        q.put("a")
        q.put("b")
        finished = threading.Event()

        def producer():
            q.put("c")
            finished.set()

        t = threading.Thread(target=producer, daemon=True)
        t.start()
        t.join(timeout=0.5)
        self.assertTrue(t.is_alive(), "put() should block while the queue is full")
        self.assertFalse(finished.is_set())

        freed = _call_with_timeout(
            lambda: q.get(), 5, self.fail, "get() did not return promptly on a non-empty queue"
        )
        self.assertEqual(freed, "a")

        t.join(timeout=5)
        self.assertFalse(t.is_alive(), "put() should unblock once space is available")
        self.assertTrue(finished.is_set())
        self.assertEqual(q.qsize(), 2)
        self.assertEqual(q.get(), "b")
        self.assertEqual(q.get(), "c")

    def test_get_blocks_when_empty_until_put_adds_item(self):
        q = BoundedQueue(2)
        result = []
        finished = threading.Event()

        def consumer():
            result.append(q.get())
            finished.set()

        t = threading.Thread(target=consumer, daemon=True)
        t.start()
        t.join(timeout=0.5)
        self.assertTrue(t.is_alive(), "get() should block while the queue is empty")
        self.assertFalse(finished.is_set())

        _call_with_timeout(
            lambda: q.put("value"), 5, self.fail, "put() did not return promptly on a non-full queue"
        )

        t.join(timeout=5)
        self.assertFalse(t.is_alive(), "get() should unblock once an item is available")
        self.assertEqual(result, ["value"])


class ConcurrencyStressTests(unittest.TestCase):
    def test_many_producers_and_consumers_lose_or_duplicate_nothing(self):
        q = BoundedQueue(10)
        n_producers = 8
        items_per_producer = 200
        total_items = n_producers * items_per_producer
        n_consumers = 5

        barrier = threading.Barrier(n_producers + n_consumers)
        consumed = [[] for _ in range(n_consumers)]
        consumed_count_lock = threading.Lock()
        consumed_count = 0

        def produce(i):
            barrier.wait()
            base = i * items_per_producer
            for k in range(items_per_producer):
                q.put(base + k)

        def consume(i):
            nonlocal consumed_count
            barrier.wait()
            while True:
                with consumed_count_lock:
                    if consumed_count >= total_items:
                        return
                    consumed_count += 1
                consumed[i].append(q.get())

        producers = [threading.Thread(target=produce, args=(i,), daemon=True) for i in range(n_producers)]
        consumers = [threading.Thread(target=consume, args=(i,), daemon=True) for i in range(n_consumers)]
        for t in producers + consumers:
            t.start()
        for t in producers + consumers:
            t.join(timeout=10)
            self.assertFalse(t.is_alive(), "a producer/consumer thread did not finish in time")

        all_items = [item for bucket in consumed for item in bucket]
        self.assertEqual(len(all_items), total_items)
        self.assertEqual(sorted(all_items), list(range(total_items)))
        self.assertEqual(q.qsize(), 0)

    def test_queue_never_exceeds_maxsize_under_concurrent_puts(self):
        maxsize = 4
        q = BoundedQueue(maxsize)
        n_producers = 30
        barrier = threading.Barrier(n_producers)
        max_seen = []
        max_seen_lock = threading.Lock()

        def produce(i):
            barrier.wait()
            q.put(i)
            with max_seen_lock:
                max_seen.append(q.qsize())

        threads = [threading.Thread(target=produce, args=(i,), daemon=True) for i in range(n_producers)]

        def drainer():
            drained = 0
            while drained < n_producers:
                q.get()
                drained += 1

        d = threading.Thread(target=drainer, daemon=True)
        for t in threads:
            t.start()
        d.start()
        for t in threads:
            t.join(timeout=10)
            self.assertFalse(t.is_alive(), "a producer thread did not finish in time")
        d.join(timeout=10)
        self.assertFalse(d.is_alive(), "the drainer thread did not finish in time")

        self.assertLessEqual(max(max_seen), maxsize)
        self.assertEqual(q.qsize(), 0)


if __name__ == "__main__":
    unittest.main()
