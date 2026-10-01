import unittest

from intervals import merge


class MergeTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(merge([]), [])

    def test_single_range_returned_as_is(self):
        self.assertEqual(merge([(1, 4, "a")]), [(1, 4, "a")])

    def test_disjoint_ranges_sorted_by_start(self):
        ranges = [(10, 12, "z"), (1, 2, "a"), (5, 6, "m")]
        self.assertEqual(merge(ranges), [(1, 2, "a"), (5, 6, "m"), (10, 12, "z")])

    def test_overlapping_ranges_merge(self):
        self.assertEqual(merge([(1, 5, "a"), (3, 8, "b")]), [(1, 8, "a")])

    def test_touching_ranges_merge_when_inclusive(self):
        self.assertEqual(merge([(1, 5, "a"), (5, 8, "b")], inclusive=True), [(1, 8, "a")])

    def test_touching_ranges_stay_separate_when_exclusive(self):
        result = merge([(1, 5, "a"), (5, 8, "b")], inclusive=False)
        self.assertEqual(result, [(1, 5, "a"), (5, 8, "b")])

    def test_transitive_merge_across_three_ranges(self):
        ranges = [(1, 3, "a"), (2, 6, "b"), (5, 9, "c")]
        self.assertEqual(merge(ranges), [(1, 9, "a")])

    def test_contained_range_merges_into_outer(self):
        self.assertEqual(merge([(1, 10, "outer"), (3, 5, "inner")]), [(1, 10, "outer")])

    def test_label_tiebreak_by_start(self):
        # Different starts: label of the smaller start wins, regardless of input order.
        self.assertEqual(merge([(5, 9, "b"), (1, 6, "a")]), [(1, 9, "a")])

    def test_label_tiebreak_by_end_when_start_ties(self):
        self.assertEqual(merge([(2, 4, "short"), (2, 9, "long")]), [(2, 9, "long")])

    def test_label_tiebreak_by_input_order_when_start_and_end_tie(self):
        ranges = [(3, 6, "first"), (3, 6, "second")]
        self.assertEqual(merge(ranges), [(3, 6, "first")])

    def test_zero_length_point_merges_when_inclusive(self):
        result = merge([(3, 3, "pt"), (3, 7, "x")], inclusive=True)
        self.assertEqual(result, [(3, 7, "x")])

    def test_zero_length_point_dropped_and_does_not_bridge_when_exclusive(self):
        ranges = [(1, 3, "a"), (3, 3, "pt"), (3, 6, "b")]
        result = merge(ranges, inclusive=False)
        self.assertEqual(result, [(1, 3, "a"), (3, 6, "b")])

    def test_start_greater_than_end_raises(self):
        with self.assertRaises(ValueError):
            merge([(5, 1, "bad")])

    def test_floats_are_supported(self):
        self.assertEqual(merge([(1.0, 2.5, "a"), (2.5, 4.0, "b")]), [(1.0, 4.0, "a")])

    def test_many_disjoint_and_overlapping_mixed(self):
        ranges = [(1, 2, "a"), (10, 11, "d"), (2, 3, "b"), (20, 21, "e"), (2.5, 9, "c")]
        # a,b,c overlap/touch in a chain (1-2, 2-3, 2.5-9) -> (1,9); d and e stay separate.
        self.assertEqual(
            merge(ranges),
            [(1, 9, "a"), (10, 11, "d"), (20, 21, "e")],
        )


if __name__ == "__main__":
    unittest.main()
