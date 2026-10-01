import unittest

from sales_report import generate_report


class GenerateReportHiddenTests(unittest.TestCase):
    def test_worked_example(self):
        text = (
            "order_id,category,amount\n"
            "1001,Books,12.50\n"
            '1002,"Electronics, Used",99.99\n'
            "1003,Books,33.00\n"
            "1001,Books,15.00\n"
            "\n"
            '1004,"Electronics, Used",99.99\n'
        )
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            "Books                      2       48.00\n"
            "Electronics, Used          2      199.98\n"
            "TOTAL                      4      247.98"
        )
        self.assertEqual(generate_report(text), expected)

    def test_single_row(self):
        text = "order_id,category,amount\n1,Books,10\n"
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            "Books                      1       10.00\n"
            "TOTAL                      1       10.00"
        )
        self.assertEqual(generate_report(text), expected)

    def test_categories_sorted_alphabetically(self):
        text = "order_id,category,amount\n1,Zoo,1\n2,Air,1\n3,Mid,1\n"
        out = generate_report(text)
        category_lines = out.splitlines()[1:-1]
        names = [line.split()[0] for line in category_lines]
        self.assertEqual(names, ["Air", "Mid", "Zoo"])

    def test_blank_lines_are_skipped(self):
        text = "order_id,category,amount\n\n1,Books,10\n   \n2,Books,5\n\n"
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            "Books                      2       15.00\n"
            "TOTAL                      2       15.00"
        )
        self.assertEqual(generate_report(text), expected)

    def test_duplicate_order_id_last_row_wins(self):
        text = "order_id,category,amount\n1,Books,10\n1,Books,15\n"
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            "Books                      1       15.00\n"
            "TOTAL                      1       15.00"
        )
        self.assertEqual(generate_report(text), expected)

    def test_duplicate_order_id_last_row_replaces_category_too(self):
        text = "order_id,category,amount\n3001,Books,10\n3001,Toys,20\n"
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            "Toys                       1       20.00\n"
            "TOTAL                      1       20.00"
        )
        self.assertEqual(generate_report(text), expected)

    def test_quoted_field_with_embedded_comma(self):
        text = 'order_id,category,amount\n1,"Electronics, Used",50\n'
        out = generate_report(text)
        self.assertIn("Electronics, Used", out)

    def test_doubled_quotes_inside_quoted_field(self):
        text = 'order_id,category,amount\n1,"Sci-Fi ""Classics""",10\n'
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            'Sci-Fi "Classics"          1       10.00\n'
            "TOTAL                      1       10.00"
        )
        self.assertEqual(generate_report(text), expected)

    def test_amounts_are_rounded_to_two_decimals(self):
        text = "order_id,category,amount\n1,Books,10\n2,Books,3.336\n"
        out = generate_report(text)
        self.assertIn("13.34", out)

    def test_header_only_input_produces_zero_total(self):
        text = "order_id,category,amount\n"
        expected = (
            "CATEGORY               COUNT       TOTAL\n"
            "TOTAL                      0        0.00"
        )
        self.assertEqual(generate_report(text), expected)

    def test_total_count_reflects_deduped_rows_not_raw_rows(self):
        text = "order_id,category,amount\n1,Books,10\n1,Books,20\n2,Toys,5\n"
        out = generate_report(text)
        total_line = out.splitlines()[-1]
        self.assertEqual(total_line.split()[1], "2")

    def test_result_is_a_string_with_no_trailing_newline(self):
        text = "order_id,category,amount\n1,Books,10\n"
        out = generate_report(text)
        self.assertIsInstance(out, str)
        self.assertFalse(out.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
