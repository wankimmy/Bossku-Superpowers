import io
import unittest
import warnings
from contextlib import redirect_stdout

import cli
import report
from checker import PasswordReport, check_strength, evaluate_password


STRONG = "Abcdef1234!@"
TOO_SHORT = "Ab1!"
MISSING_THREE = "aaaaaaaaaaaa"
HAS_SPACE = "Abcdefg 123!"
HAS_TAB = "Ab\tcdefgh123!"


class EvaluatePasswordTests(unittest.TestCase):
    def test_all_criteria_pass(self):
        report_ = evaluate_password(STRONG)
        self.assertEqual(report_.score, 5)
        self.assertEqual(report_.reasons, ())

    def test_returns_passwordreport_with_tuple_reasons(self):
        report_ = evaluate_password(TOO_SHORT)
        self.assertIsInstance(report_, PasswordReport)
        self.assertIsInstance(report_.reasons, tuple)

    def test_too_short_single_reason(self):
        report_ = evaluate_password(TOO_SHORT)
        self.assertEqual(report_.score, 4)
        self.assertEqual(
            report_.reasons, ("too short (needs at least 12 characters)",)
        )

    def test_missing_multiple_reasons_in_fixed_order(self):
        report_ = evaluate_password(MISSING_THREE)
        self.assertEqual(report_.score, 2)
        self.assertEqual(
            report_.reasons,
            ("missing an uppercase letter", "missing a digit", "missing a symbol"),
        )

    def test_whitespace_shortcircuits_other_reasons(self):
        report_ = evaluate_password(HAS_SPACE)
        self.assertEqual(report_.score, 0)
        self.assertEqual(report_.reasons, ("passwords may not contain whitespace",))

    def test_tab_counts_as_whitespace(self):
        report_ = evaluate_password(HAS_TAB)
        self.assertEqual(report_.score, 0)
        self.assertEqual(report_.reasons, ("passwords may not contain whitespace",))

    def test_empty_string_all_five_reasons(self):
        report_ = evaluate_password("")
        self.assertEqual(report_.score, 0)
        self.assertEqual(
            report_.reasons,
            (
                "too short (needs at least 12 characters)",
                "missing a lowercase letter",
                "missing an uppercase letter",
                "missing a digit",
                "missing a symbol",
            ),
        )

    def test_non_string_raises_typeerror(self):
        with self.assertRaises(TypeError):
            evaluate_password(12345)

    def test_report_is_immutable(self):
        report_ = evaluate_password(STRONG)
        with self.assertRaises(Exception):
            report_.score = 0


class CheckStrengthAliasTests(unittest.TestCase):
    def test_returns_old_tuple_shape(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            score, reasons = check_strength(TOO_SHORT)
        self.assertIsInstance(reasons, list)
        self.assertEqual(score, 4)
        self.assertEqual(reasons, ["too short (needs at least 12 characters)"])

    def test_matches_evaluate_password_values(self):
        for pw in (STRONG, TOO_SHORT, MISSING_THREE, HAS_SPACE, ""):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                score, reasons = check_strength(pw)
            report_ = evaluate_password(pw)
            self.assertEqual(score, report_.score)
            self.assertEqual(reasons, list(report_.reasons))

    def test_emits_deprecation_warning_mentioning_new_name(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            check_strength("x")
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)
        self.assertIn("evaluate_password", str(caught[0].message))


class ReportCallSitesTests(unittest.TestCase):
    def test_summarize_one_no_deprecation_warning(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            result = report.summarize_one(STRONG)
        self.assertEqual(result, f"{STRONG}: 5/5")

    def test_summarize_one_lists_missing_reasons(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            result = report.summarize_one(TOO_SHORT)
        self.assertEqual(
            result,
            f"{TOO_SHORT}: 4/5 (missing: too short (needs at least 12 characters))",
        )

    def test_summarize_many_matches_individual_calls(self):
        passwords = [STRONG, TOO_SHORT]
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            combined = report.summarize_many(passwords)
        expected = "\n".join(report.summarize_one(p) for p in passwords)
        self.assertEqual(combined, expected)

    def test_rank_by_strength_sorts_descending_no_warning(self):
        # STRONG scores 5/5, TOO_SHORT scores 4/5 (only length fails),
        # MISSING_THREE scores 2/5 (upper/digit/symbol all fail).
        passwords = [TOO_SHORT, STRONG, MISSING_THREE]
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            ranked = report.rank_by_strength(passwords)
        self.assertEqual(ranked, [STRONG, TOO_SHORT, MISSING_THREE])

    def test_rank_by_strength_stable_for_ties(self):
        a = "bbbbbbbbbbbb"
        b = "cccccccccccc"
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            ranked = report.rank_by_strength([a, b])
        self.assertEqual(ranked, [a, b])


class CliTests(unittest.TestCase):
    def test_cli_no_deprecation_warning(self):
        buf = io.StringIO()
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            with redirect_stdout(buf):
                cli.main([TOO_SHORT, STRONG])
        output = buf.getvalue()
        self.assertIn(f"strongest: {STRONG} (5/5)", output)

    def test_cli_output_format(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main([TOO_SHORT, STRONG])
        lines = buf.getvalue().splitlines()
        self.assertEqual(lines[0], f"strongest: {STRONG} (5/5)")
        self.assertIn(f"{STRONG}: 5/5", lines[1:])
        self.assertIn(
            f"{TOO_SHORT}: 4/5 (missing: too short (needs at least 12 characters))",
            lines[1:],
        )


if __name__ == "__main__":
    unittest.main()
