import dataclasses
import datetime
import logging
import unittest
from decimal import Decimal
from unittest import mock

import clock
import errors
import formatting
import report_card
import rubric


def Q(id, max_points, category):
    return rubric.Question(id=id, max_points=Decimal(max_points), category=category)


def R(question_id, points):
    return rubric.GradedResponse(question_id=question_id, points_earned=Decimal(points))


class _ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class RubricExistingBehaviorTests(unittest.TestCase):
    """rubric.py already works; these pin its behavior so it stays untouched."""

    def setUp(self):
        self.question = Q("q1", "10", "homework")

    def test_full_credit_is_100(self):
        self.assertEqual(rubric.score_question(self.question, Decimal("10")), Decimal("100"))

    def test_zero_credit_is_0(self):
        self.assertEqual(rubric.score_question(self.question, Decimal("0")), Decimal("0"))

    def test_score_is_unrounded(self):
        q = Q("q2", "3", "homework")
        result = rubric.score_question(q, Decimal("1"))
        self.assertNotEqual(result, Decimal("33.3"))
        self.assertGreater(result, Decimal("33.333"))
        self.assertLess(result, Decimal("33.334"))

    def test_points_above_max_raises(self):
        with self.assertRaises(errors.GradebookError):
            rubric.score_question(self.question, Decimal("11"))

    def test_points_negative_raises(self):
        with self.assertRaises(errors.GradebookError):
            rubric.score_question(self.question, Decimal("-1"))

    def test_max_points_zero_raises(self):
        q = Q("q3", "0", "homework")
        with self.assertRaises(errors.GradebookError):
            rubric.score_question(q, Decimal("0"))

    def test_wrong_type_points_earned_raises(self):
        with self.assertRaises(errors.GradebookError):
            rubric.score_question(self.question, 5)

    def test_question_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.question.max_points = Decimal("5")

    def test_graded_response_is_frozen(self):
        r = R("q1", "5")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.points_earned = Decimal("1")


class ReportCardComputationTests(unittest.TestCase):
    def test_overall_percent_computed_from_unrounded_category_averages(self):
        # exam: 1 question, 0/2 -> 0% exactly. quiz: 1 question, 2/3 -> 66.6...%.
        # Correct (combine unrounded, round once): 0*0.5 + 66.666..*0.5 = 33.333.. -> 33.3
        # Buggy (round each category first): 0.0*0.5 + 66.7*0.5 = 33.35 -> 33.4
        questions = [Q("e1", "2", "exam"), Q("z1", "3", "quiz")]
        responses = [R("e1", "0"), R("z1", "2")]
        rc = report_card.build_report_card("stu1", questions, responses, {"exam": 50, "quiz": 50})
        self.assertEqual(rc.overall_percent, Decimal("33.3"))

    def test_category_breakdown_shows_rounded_average_for_display(self):
        questions = [Q("e1", "2", "exam"), Q("z1", "3", "quiz")]
        responses = [R("e1", "0"), R("z1", "2")]
        rc = report_card.build_report_card("stu1", questions, responses, {"exam": 50, "quiz": 50})
        by_cat = {c.category: c.average_percent for c in rc.category_breakdown}
        self.assertEqual(by_cat["exam"], Decimal("0.0"))
        self.assertEqual(by_cat["quiz"], Decimal("66.7"))

    def test_letter_grade_boundaries(self):
        cases = [("90", "A"), ("80", "B"), ("70", "C"), ("60", "D"), ("59.9", "F")]
        for points, expected_grade in cases:
            with self.subTest(points=points):
                qs = [Q("q1", "100", "exam")]
                rs = [R("q1", points)]
                rc = report_card.build_report_card("s", qs, rs, {"exam": 100})
                self.assertEqual(rc.letter_grade, expected_grade)
                self.assertEqual(rc.overall_percent, Decimal(points))

    def test_category_average_is_equally_weighted_per_question(self):
        # a is worth 100 points and scores 0%; b is worth 2 points and scores
        # 100%. An average weighted by max_points would be close to 0%; the
        # equally-per-question average is exactly 50%.
        qs = [Q("a", "100", "cat"), Q("b", "2", "cat")]
        rs = [R("a", "0"), R("b", "2")]
        rc = report_card.build_report_card("s", qs, rs, {"cat": 100})
        self.assertEqual(rc.category_breakdown[0].average_percent, Decimal("50.0"))

    def test_category_breakdown_sorted_alphabetically_not_by_appearance(self):
        qs = [Q("q1", "10", "zeta"), Q("q2", "10", "alpha"), Q("q3", "10", "mid")]
        rs = [R("q1", "10"), R("q2", "5"), R("q3", "0")]
        rc = report_card.build_report_card("s", qs, rs, {"zeta": 20, "alpha": 50, "mid": 30})
        self.assertEqual([c.category for c in rc.category_breakdown], ["alpha", "mid", "zeta"])

    def test_category_breakdown_is_tuple_of_categoryscore(self):
        qs = [Q("q1", "10", "c")]
        rs = [R("q1", "5")]
        rc = report_card.build_report_card("s", qs, rs, {"c": 100})
        self.assertIsInstance(rc.category_breakdown, tuple)
        self.assertEqual(rc.category_breakdown[0].category, "c")

    def test_report_card_is_frozen(self):
        qs = [Q("q1", "10", "c")]
        rc = report_card.build_report_card("s", qs, [R("q1", "5")], {"c": 100})
        with self.assertRaises(dataclasses.FrozenInstanceError):
            rc.overall_percent = Decimal("0")

    def test_category_score_is_frozen(self):
        qs = [Q("q1", "10", "c")]
        rc = report_card.build_report_card("s", qs, [R("q1", "5")], {"c": 100})
        with self.assertRaises(dataclasses.FrozenInstanceError):
            rc.category_breakdown[0].average_percent = Decimal("0")

    def test_keyword_call_matches_documented_signature(self):
        qs = [Q("q1", "10", "c")]
        rc = report_card.build_report_card(
            student_id="stu9",
            questions=qs,
            responses=[R("q1", "10")],
            category_weights={"c": 100},
            clock=clock.FixedClock(datetime.date(2024, 7, 7)),
        )
        self.assertEqual(rc.student_id, "stu9")
        self.assertEqual(rc.graded_on, datetime.date(2024, 7, 7))


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.qs = [Q("q1", "10", "c")]

    def test_student_id_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card(1, self.qs, [R("q1", "5")], {"c": 100})
        self.assertEqual(str(ctx.exception), "invalid: student_id must be a str")

    def test_student_id_empty(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("  ", self.qs, [R("q1", "5")], {"c": 100})
        self.assertEqual(str(ctx.exception), "invalid: student_id must not be empty")

    def test_questions_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", "not-a-list", [], {})
        self.assertEqual(str(ctx.exception), "invalid: questions must be a list or tuple")

    def test_questions_empty_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", [], [], {})
        self.assertEqual(str(ctx.exception), "invalid: questions must not be empty")

    def test_question_element_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", [self.qs[0], "nope"], [R("q1", "5")], {"c": 100})
        self.assertEqual(str(ctx.exception), "invalid: questions[1] must be a Question")

    def test_responses_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, "not-a-list", {"c": 100})
        self.assertEqual(str(ctx.exception), "invalid: responses must be a list or tuple")

    def test_response_element_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, [R("q1", "5"), "nope"], {"c": 100})
        self.assertEqual(str(ctx.exception), "invalid: responses[1] must be a GradedResponse")

    def test_category_weights_wrong_type(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, [R("q1", "5")], "not-a-dict")
        self.assertEqual(str(ctx.exception), "invalid: category_weights must be a dict")

    def test_question_with_no_response_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, [], {"c": 100})
        self.assertEqual(str(ctx.exception), "invalid: question q1 has no response")

    def test_question_with_duplicate_response_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card(
                "s", self.qs, [R("q1", "5"), R("q1", "3")], {"c": 100}
            )
        self.assertEqual(str(ctx.exception), "invalid: question q1 has more than one response")

    def test_orphan_response_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card(
                "s", self.qs, [R("q1", "5"), R("ghost", "3")], {"c": 100}
            )
        self.assertEqual(str(ctx.exception), "invalid: response references unknown question ghost")

    def test_category_missing_weight_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, [R("q1", "5")], {})
        self.assertEqual(str(ctx.exception), "invalid: category c is missing a weight")

    def test_category_weights_unknown_category_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card(
                "s", self.qs, [R("q1", "5")], {"c": 100, "ghost": 1}
            )
        self.assertEqual(str(ctx.exception), "invalid: category_weights has an unknown category ghost")

    def test_category_weights_negative_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, [R("q1", "5")], {"c": -10})
        self.assertEqual(str(ctx.exception), "invalid: category_weights[c] must not be negative")

    def test_category_weights_sum_mismatch_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            report_card.build_report_card("s", self.qs, [R("q1", "5")], {"c": 99})
        self.assertEqual(str(ctx.exception), "invalid: category_weights must sum to 100")

    def test_all_validation_errors_are_gradebook_errors(self):
        with self.assertRaises(errors.GradebookError):
            report_card.build_report_card("", self.qs, [], {})


class ClockAndLoggingTests(unittest.TestCase):
    def setUp(self):
        self.qs = [Q("q1", "10", "c")]
        self.rs = [R("q1", "5")]
        self.logger = logging.getLogger("gradebook.report_card")

    def test_injected_clock_used_and_called_exactly_once(self):
        class CountingClock:
            def __init__(self, value):
                self.calls = 0
                self.value = value

            def now(self):
                self.calls += 1
                return self.value

        cc = CountingClock(datetime.date(2024, 3, 3))
        rc = report_card.build_report_card("s", self.qs, self.rs, {"c": 100}, clock=cc)
        self.assertEqual(cc.calls, 1)
        self.assertEqual(rc.graded_on, datetime.date(2024, 3, 3))

    def test_default_clock_comes_from_clock_module(self):
        with mock.patch("clock.SystemClock") as fake_system:
            fake_system.return_value.now.return_value = datetime.date(2031, 1, 1)
            rc = report_card.build_report_card("s", self.qs, self.rs, {"c": 100})
        self.assertEqual(rc.graded_on, datetime.date(2031, 1, 1))

    def test_success_logs_exactly_one_info_record_with_exact_message(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            report_card.build_report_card("stu42", self.qs, self.rs, {"c": 100})
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 1)
        self.assertEqual(handler.records[0].levelname, "INFO")
        self.assertEqual(
            handler.records[0].getMessage(),
            "report student=stu42 categories=1 overall=50.0% grade=F",
        )

    def test_failure_logs_nothing(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            with self.assertRaises(errors.ValidationError):
                report_card.build_report_card("s", self.qs, [], {"c": 100})
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 0)


class ReuseTests(unittest.TestCase):
    def test_reuses_score_question_once_per_question(self):
        qs = [Q("q1", "10", "c")]
        rs = [R("q1", "5")]
        with mock.patch("rubric.score_question", wraps=rubric.score_question) as spy:
            report_card.build_report_card("s", qs, rs, {"c": 100})
        self.assertEqual(spy.call_count, 1)

    def test_reuses_score_question_for_each_of_several_questions(self):
        qs = [Q("q1", "10", "c"), Q("q2", "5", "c")]
        rs = [R("q1", "5"), R("q2", "5")]
        with mock.patch("rubric.score_question", wraps=rubric.score_question) as spy:
            report_card.build_report_card("s", qs, rs, {"c": 100})
        self.assertEqual(spy.call_count, 2)

    def test_reuses_require_nonempty_str_for_student_id(self):
        import validation

        qs = [Q("q1", "10", "c")]
        with mock.patch("validation.require_nonempty_str", wraps=validation.require_nonempty_str) as spy:
            report_card.build_report_card("stu7", qs, [R("q1", "5")], {"c": 100})
        spy.assert_any_call("student_id", "stu7")

    def test_reuses_require_non_negative_decimal_for_weights(self):
        import validation

        qs = [Q("q1", "10", "c")]
        with mock.patch(
            "validation.require_non_negative_decimal", wraps=validation.require_non_negative_decimal
        ) as spy:
            report_card.build_report_card("s", qs, [R("q1", "5")], {"c": 100})
        spy.assert_any_call("category_weights[c]", 100)

    def test_reuses_round_percent_for_overall_and_category_display(self):
        import formatting as formatting_module

        qs = [Q("e1", "2", "exam"), Q("z1", "3", "quiz")]
        rs = [R("e1", "0"), R("z1", "2")]
        with mock.patch(
            "formatting.round_percent", wraps=formatting_module.round_percent
        ) as spy:
            report_card.build_report_card("s", qs, rs, {"exam": 50, "quiz": 50})
        # once for the overall percent, once per category (2 categories), and
        # once more inside format_percent when the success log line is built.
        self.assertEqual(spy.call_count, 4)


class MutationSafetyTests(unittest.TestCase):
    def test_does_not_mutate_category_weights(self):
        qs = [Q("q1", "10", "c")]
        weights = {"c": 100}
        report_card.build_report_card("s", qs, [R("q1", "5")], weights)
        self.assertEqual(weights, {"c": 100})

    def test_does_not_mutate_questions_or_responses_lists(self):
        qs = [Q("z", "10", "c"), Q("a", "10", "c")]
        rs = [R("z", "5"), R("a", "5")]
        qs_ids_before = [q.id for q in qs]
        rs_ids_before = [r.question_id for r in rs]
        report_card.build_report_card("s", qs, rs, {"c": 100})
        self.assertEqual([q.id for q in qs], qs_ids_before)
        self.assertEqual([r.question_id for r in rs], rs_ids_before)


if __name__ == "__main__":
    unittest.main()
