import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report import generate_report, top_category


class ReportCharacterizationTests(unittest.TestCase):
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

    def test_by_category_stats(self):
        report = generate_report(self.entries)
        self.assertEqual(
            report["by_category"]["fruit"],
            {"count": 2, "total": 40.0, "average": 20.0, "min": 10.0, "max": 30.0},
        )

    def test_non_positive_amounts_are_ignored(self):
        report = generate_report(self.entries + [("fruit", -5.0), ("fruit", 0.0)])
        self.assertEqual(report["overall"]["count"], 5)

    def test_top_category(self):
        self.assertEqual(top_category(self.entries), "veg")


if __name__ == "__main__":
    unittest.main()
