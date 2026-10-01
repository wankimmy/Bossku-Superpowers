import unittest

from calc import evaluate


class BasicArithmeticTests(unittest.TestCase):
    def test_addition_and_subtraction(self):
        self.assertEqual(evaluate("2 + 3"), 5.0)
        self.assertEqual(evaluate("10 - 4"), 6.0)

    def test_multiplication_and_division(self):
        self.assertEqual(evaluate("3 * 4"), 12.0)
        self.assertEqual(evaluate("7 / 2"), 3.5)

    def test_left_to_right_for_same_precedence(self):
        self.assertEqual(evaluate("10 - 3 - 2"), 5.0)
        self.assertEqual(evaluate("20 / 2 / 5"), 2.0)

    def test_result_is_always_a_float(self):
        self.assertIsInstance(evaluate("2 + 2"), float)


class PrecedenceTests(unittest.TestCase):
    def test_multiplication_before_addition(self):
        self.assertEqual(evaluate("2 + 3 * 4"), 14.0)

    def test_division_before_subtraction(self):
        self.assertEqual(evaluate("20 - 8 / 2"), 16.0)

    def test_parentheses_override_precedence(self):
        self.assertEqual(evaluate("(2 + 3) * 4"), 20.0)
        self.assertEqual(evaluate("2 * (3 + 4) - 5"), 9.0)

    def test_nested_parentheses(self):
        self.assertEqual(evaluate("((2 + 3) * (1 + 1))"), 10.0)


class UnaryMinusTests(unittest.TestCase):
    def test_leading_unary_minus(self):
        self.assertEqual(evaluate("-3 + 5"), 2.0)

    def test_unary_minus_after_operator(self):
        self.assertEqual(evaluate("4 * -2"), -8.0)

    def test_unary_minus_on_parenthesized_expression(self):
        self.assertEqual(evaluate("-(2 + 3)"), -5.0)


class DecimalsAndWhitespaceTests(unittest.TestCase):
    def test_decimal_literals(self):
        self.assertEqual(evaluate("1.5 + 2.5"), 4.0)

    def test_whitespace_is_ignored(self):
        self.assertEqual(evaluate("  2   +   2  "), 4.0)
        self.assertEqual(evaluate("2+2"), 4.0)


class DivisionByZeroTests(unittest.TestCase):
    def test_division_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            evaluate("5 / 0")

    def test_division_by_zero_inside_parentheses(self):
        with self.assertRaises(ValueError):
            evaluate("1 / (2 - 2)")


class MalformedExpressionTests(unittest.TestCase):
    def test_empty_or_blank_string_raises(self):
        for expr in ("", "   "):
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    evaluate(expr)

    def test_unbalanced_parentheses_raises(self):
        for expr in ("(2 + 3", "2 + 3)", "((2+3)"):
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    evaluate(expr)

    def test_invalid_characters_raise(self):
        for expr in ("2 + a", "abc", "2 & 3"):
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    evaluate(expr)

    def test_trailing_operator_raises(self):
        with self.assertRaises(ValueError):
            evaluate("2 +")

    def test_missing_operator_between_operands_raises(self):
        with self.assertRaises(ValueError):
            evaluate("2 3")

    def test_non_string_input_raises(self):
        with self.assertRaises(ValueError):
            evaluate(123)


if __name__ == "__main__":
    unittest.main()
