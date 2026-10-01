import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from allocate import allocate, allocate_with_minimums, AllocationError


class AllocateBasicTests(unittest.TestCase):
    def test_exact_divisible(self):
        self.assertEqual(allocate(100, [50, 30, 20]), [50, 30, 20])

    def test_zero_total(self):
        self.assertEqual(allocate(0, [1, 1, 1]), [0, 0, 0])

    def test_empty_weights_raises(self):
        with self.assertRaises(AllocationError):
            allocate(5, [])

    def test_with_minimums_default(self):
        self.assertEqual(
            allocate_with_minimums(10, [1, 1, 1], None),
            allocate(10, [1, 1, 1]),
        )


if __name__ == "__main__":
    unittest.main()
