import unittest

from allocate import allocate, allocate_with_minimums, AllocationError


class AllocateTests(unittest.TestCase):
    def test_tie_broken_by_lower_index(self):
        self.assertEqual(allocate(10, [1, 1, 1]), [4, 3, 3])
        self.assertEqual(allocate(1, [1, 1, 1]), [1, 0, 0])

    def test_exact_divisible_no_remainder(self):
        self.assertEqual(allocate(100, [50, 30, 20]), [50, 30, 20])

    def test_distinct_remainders_largest_wins(self):
        self.assertEqual(allocate(11, [5, 3, 2]), [6, 3, 2])

    def test_zero_total_returns_all_zero(self):
        self.assertEqual(allocate(0, [1, 1, 1]), [0, 0, 0])

    def test_zero_total_with_zero_weights_is_ok(self):
        self.assertEqual(allocate(0, [0, 0, 0]), [0, 0, 0])

    def test_single_weight_gets_everything(self):
        self.assertEqual(allocate(7, [1]), [7])

    def test_zero_weight_entry_gets_nothing(self):
        self.assertEqual(allocate(10, [0, 1, 1]), [0, 5, 5])

    def test_tie_with_unequal_weights_still_broken_by_index(self):
        # weights [1, 3] with total 2: exact quotas are 0.5 and 1.5 -- a
        # tied fractional remainder despite unequal weights. The lower
        # index wins the tie regardless of which entry has the larger
        # weight.
        self.assertEqual(allocate(2, [1, 3]), [1, 1])

    def test_positive_total_all_zero_weights_raises(self):
        with self.assertRaises(AllocationError):
            allocate(5, [0, 0, 0])

    def test_negative_weight_raises_allocation_error(self):
        with self.assertRaises(AllocationError):
            allocate(5, [-1, 2, 3])

    def test_float_weight_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate(5, [1.5, 2, 3])

    def test_bool_weight_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate(5, [True, 2, 3])

    def test_string_weight_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate(5, ["1", 2, 3])

    def test_bool_total_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate(True, [1, 2, 3])

    def test_non_int_total_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate("5", [1, 2, 3])

    def test_negative_total_raises_allocation_error(self):
        with self.assertRaises(AllocationError):
            allocate(-5, [1, 2, 3])

    def test_non_sequence_weights_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate(5, "abc")

    def test_empty_weights_raises_allocation_error(self):
        with self.assertRaises(AllocationError):
            allocate(5, [])

    def test_weights_not_mutated(self):
        weights = [1, 1, 1]
        original = list(weights)
        allocate(10, weights)
        self.assertEqual(weights, original)

    def test_result_length_matches_weights(self):
        self.assertEqual(len(allocate(10, [1, 2, 3, 4, 5])), 5)

    def test_sum_always_equals_total(self):
        combos = [
            (10, [1, 1, 1]),
            (100, [50, 30, 20]),
            (11, [5, 3, 2]),
            (23, [7, 11, 13, 17]),
            (1000, [1, 2, 3, 4, 5, 6, 7]),
            (1, [1, 1, 1, 1, 1]),
            (0, [3, 2, 1]),
        ]
        for total, weights in combos:
            result = allocate(total, weights)
            self.assertEqual(sum(result), total)
            self.assertEqual(len(result), len(weights))


class AllocateWithMinimumsTests(unittest.TestCase):
    def test_none_minimums_same_as_plain_allocate(self):
        self.assertEqual(
            allocate_with_minimums(10, [1, 1, 1], None),
            allocate(10, [1, 1, 1]),
        )

    def test_minimums_floor_then_distribute_on_original_weights(self):
        # remaining = 10 - 6 = 4, distributed over weights [1,1,1] same as
        # allocate(4, [1,1,1]) = [2,1,1], then + minimums [2,2,2] = [4,3,3]
        self.assertEqual(allocate_with_minimums(10, [1, 1, 1], [2, 2, 2]), [4, 3, 3])

    def test_minimums_exactly_equal_total(self):
        self.assertEqual(allocate_with_minimums(6, [1, 1, 1], [2, 2, 2]), [2, 2, 2])

    def test_minimums_use_unreduced_weights_not_leftover_shares(self):
        # weights are deliberately skewed so that reducing them by the
        # minimums (a wrong implementation might do this) would change
        # the proportional split of the remainder.
        result = allocate_with_minimums(20, [1, 9], [5, 5])
        # remaining = 10, allocate(10, [1, 9]) = [1, 9] (9*10/10=9 exact,
        # 1*10/10=1 exact) -> final = [5+1, 5+9] = [6, 14]
        self.assertEqual(result, [6, 14])

    def test_minimums_exceed_total_raises(self):
        with self.assertRaises(AllocationError):
            allocate_with_minimums(5, [1, 1, 1], [3, 3, 3])

    def test_minimums_length_mismatch_raises(self):
        with self.assertRaises(AllocationError):
            allocate_with_minimums(5, [1, 1, 1], [1, 1])

    def test_minimums_negative_raises(self):
        with self.assertRaises(AllocationError):
            allocate_with_minimums(5, [1, 1, 1], [1, -1, 1])

    def test_minimums_non_int_element_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate_with_minimums(5, [1, 1, 1], [1, 1.0, 1])

    def test_minimums_bool_element_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate_with_minimums(5, [1, 1, 1], [1, True, 1])

    def test_minimums_wrong_container_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            allocate_with_minimums(5, [1, 1, 1], "abc")

    def test_minimums_not_mutated(self):
        minimums = [1, 1, 1]
        original = list(minimums)
        allocate_with_minimums(10, [1, 1, 1], minimums)
        self.assertEqual(minimums, original)

    def test_zero_weights_ok_when_minimums_cover_everything(self):
        # remaining = 0, so the "all-zero weights with positive total"
        # error must not fire here -- there is nothing left to allocate.
        self.assertEqual(allocate_with_minimums(6, [0, 0, 0], [2, 2, 2]), [2, 2, 2])

    def test_sum_always_equals_total_with_minimums(self):
        combos = [
            (10, [1, 1, 1], [2, 2, 2]),
            (23, [7, 11, 13, 17], [1, 1, 1, 1]),
            (6, [1, 1, 1], None),
            (6, [0, 0, 0], [2, 2, 2]),
        ]
        for total, weights, minimums in combos:
            result = allocate_with_minimums(total, weights, minimums)
            self.assertEqual(sum(result), total)
            self.assertEqual(len(result), len(weights))


if __name__ == "__main__":
    unittest.main()
