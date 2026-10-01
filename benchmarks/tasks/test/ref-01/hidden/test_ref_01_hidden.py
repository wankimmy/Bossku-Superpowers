import unittest

from report import generate_report, top_category


class ReportCharacterizationHiddenTests(unittest.TestCase):
    def setUp(self):
        self.entries = [
            ("fruit", 10.0),
            ("fruit", 30.0),
            ("veg", 5.0),
            ("veg", 15.0),
            ("veg", 25.0),
        ]

    def test_overall_stats(self):
        report = generate_report(self.entries)
        self.assertEqual(
            report["overall"],
            {"count": 5, "total": 85.0, "average": 17.0, "min": 5.0, "max": 30.0},
        )

    def test_by_category_stats_for_both_categories(self):
        report = generate_report(self.entries)
        self.assertEqual(
            report["by_category"]["fruit"],
            {"count": 2, "total": 40.0, "average": 20.0, "min": 10.0, "max": 30.0},
        )
        self.assertEqual(
            report["by_category"]["veg"],
            {"count": 3, "total": 45.0, "average": 15.0, "min": 5.0, "max": 25.0},
        )

    def test_non_positive_amounts_excluded_from_overall_and_category(self):
        report = generate_report(self.entries + [("fruit", -5.0), ("fruit", 0.0)])
        self.assertEqual(report["overall"]["count"], 5)
        self.assertEqual(report["by_category"]["fruit"]["count"], 2)

    def test_generate_report_raises_when_nothing_left(self):
        with self.assertRaises(ValueError):
            generate_report([("a", -1.0), ("a", 0.0)])

    def test_single_entry_single_category(self):
        report = generate_report([("solo", 7.0)])
        self.assertEqual(
            report,
            {
                "overall": {"count": 1, "total": 7.0, "average": 7.0, "min": 7.0, "max": 7.0},
                "by_category": {
                    "solo": {"count": 1, "total": 7.0, "average": 7.0, "min": 7.0, "max": 7.0}
                },
            },
        )

    def test_values_are_rounded_to_two_decimals(self):
        report = generate_report([("a", 10.0), ("a", 10.0), ("a", 10.01)])
        self.assertEqual(
            report["by_category"]["a"],
            {"count": 3, "total": 30.01, "average": 10.0, "min": 10.0, "max": 10.01},
        )

    def test_top_category_picks_highest_total(self):
        self.assertEqual(top_category(self.entries), "veg")

    def test_top_category_tie_break_alphabetical(self):
        self.assertEqual(top_category([("b", 10.0), ("a", 10.0)]), "a")

    def test_top_category_applies_same_filter(self):
        self.assertEqual(top_category([("a", -1.0), ("b", 5.0)]), "b")


class StatsStructuralHiddenTests(unittest.TestCase):
    def test_stats_module_basic_properties(self):
        import stats

        s = stats.Stats([3, 1, 2])
        self.assertEqual(s.count, 3)
        self.assertEqual(s.total, 6)
        self.assertEqual(s.average, 2.0)
        self.assertEqual(s.minimum, 1)
        self.assertEqual(s.maximum, 3)

    def test_stats_raises_on_empty(self):
        import stats

        with self.assertRaises(ValueError):
            stats.Stats([])

    def test_stats_as_dict_matches_properties(self):
        import stats

        s = stats.Stats([10.0, 10.0, 10.01])
        self.assertEqual(
            s.as_dict(),
            {"count": 3, "total": 30.01, "average": 10.0, "min": 10.0, "max": 10.01},
        )

    def test_stats_single_value(self):
        import stats

        s = stats.Stats([7.0])
        self.assertEqual(s.as_dict(), {"count": 1, "total": 7.0, "average": 7.0, "min": 7.0, "max": 7.0})

    def test_report_category_stats_match_independent_stats_computation(self):
        import stats

        entries = [("fruit", 10.0), ("fruit", 30.0), ("veg", 5.0), ("veg", 15.0), ("veg", 25.0)]
        report = generate_report(entries)
        expected = stats.Stats([5.0, 15.0, 25.0]).as_dict()
        self.assertEqual(report["by_category"]["veg"], expected)


if __name__ == "__main__":
    unittest.main()
