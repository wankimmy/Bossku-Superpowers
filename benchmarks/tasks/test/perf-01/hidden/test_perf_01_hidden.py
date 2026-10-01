import random
import time
import unittest

from inversions import count_inversions


class CorrectnessTests(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(count_inversions([]), 0)

    def test_single_element(self):
        self.assertEqual(count_inversions([5]), 0)

    def test_sorted_ascending_has_no_inversions(self):
        self.assertEqual(count_inversions(list(range(100))), 0)

    def test_sorted_descending_has_maximum_inversions(self):
        n = 50
        data = list(range(n, 0, -1))
        self.assertEqual(count_inversions(data), n * (n - 1) // 2)

    def test_small_known_case(self):
        self.assertEqual(count_inversions([3, 1, 2]), 2)

    def test_duplicates_are_not_inversions(self):
        self.assertEqual(count_inversions([2, 2, 2]), 0)
        self.assertEqual(count_inversions([1, 2, 1]), 1)

    def test_negative_numbers(self):
        self.assertEqual(count_inversions([-1, -5, 0, -3]), 3)

    def test_does_not_mutate_input(self):
        data = [5, 3, 1, 4, 2]
        original = list(data)
        count_inversions(data)
        self.assertEqual(data, original)

    def test_type_error_on_non_list(self):
        with self.assertRaises(TypeError):
            count_inversions("12345")
        with self.assertRaises(TypeError):
            count_inversions((1, 2, 3))

    def test_matches_brute_force_on_random_small_input(self):
        rng = random.Random(99)
        data = [rng.randint(-100, 100) for _ in range(300)]
        expected = 0
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                if data[i] > data[j]:
                    expected += 1
        self.assertEqual(count_inversions(data), expected)


class PerformanceTests(unittest.TestCase):
    def test_large_input_is_fast_and_correct(self):
        rng = random.Random(20261001)
        data = list(range(100000))
        rng.shuffle(data)
        t0 = time.perf_counter()
        result = count_inversions(data)
        elapsed = time.perf_counter() - t0
        self.assertEqual(result, 2503094025)
        self.assertLess(elapsed, 8.0, f"count_inversions took too long: {elapsed:.2f}s")


if __name__ == "__main__":
    unittest.main()
