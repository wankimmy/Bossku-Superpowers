import datetime
import unittest

from orders_csv import parse_orders, export_csv


class OrdersCsvHiddenTests(unittest.TestCase):
    def test_parse(self):
        got = parse_orders("17,Aisyah Tan,2026-03-05\n\n18,Wei Jie,2026-12-31\n")
        self.assertEqual(got, [{"id": 17, "customer": "Aisyah Tan", "date": datetime.date(2026, 3, 5)},
                               {"id": 18, "customer": "Wei Jie", "date": datetime.date(2026, 12, 31)}])

    def test_parse_bad(self):
        for bad in ("17,Aisyah", "x,Aisyah,2026-03-05", "17,Aisyah,2026-13-01"):
            with self.assertRaises(ValueError):
                parse_orders(bad)

    def _export(self):
        return export_csv(parse_orders("17,Aisyah Tan,2026-03-05\n18,Wei Jie,2026-12-31"))

    def test_export_shape(self):
        lines = self._export().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(self._export().endswith("\n"))

    # ---- the three-part rule ----

    def test_semicolon_delimiter(self):
        for line in self._export().splitlines():
            self.assertEqual(line.count(";"), 2, line)
            self.assertNotIn(",", line)

    def test_header_is_lower_snake_case(self):
        header = self._export().splitlines()[0].split(";")
        self.assertEqual(header, ["order_id", "customer_name", "order_date"])

    def test_dates_are_dd_mm_yyyy(self):
        rows = [l.split(";") for l in self._export().splitlines()[1:]]
        self.assertEqual(rows[0], ["17", "Aisyah Tan", "05/03/2026"])
        self.assertEqual(rows[1], ["18", "Wei Jie", "31/12/2026"])


if __name__ == "__main__":
    unittest.main()
