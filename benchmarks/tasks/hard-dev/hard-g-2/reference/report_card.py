"""Per-student report cards, built on top of rubric.score_question."""
import logging
from dataclasses import dataclass
from decimal import Decimal

import clock as clock_module
import errors
import formatting
import rubric
import validation

_LOGGER = logging.getLogger("gradebook.report_card")


@dataclass(frozen=True)
class CategoryScore:
    category: str
    average_percent: Decimal


@dataclass(frozen=True)
class ReportCard:
    student_id: str
    graded_on: object
    overall_percent: Decimal
    letter_grade: str
    category_breakdown: tuple


def _letter_grade(overall_percent):
    if overall_percent >= 90:
        return "A"
    if overall_percent >= 80:
        return "B"
    if overall_percent >= 70:
        return "C"
    if overall_percent >= 60:
        return "D"
    return "F"


def build_report_card(student_id, questions, responses, category_weights, clock=None):
    validation.require_nonempty_str("student_id", student_id)
    validation.require_nonempty_sequence("questions", questions)
    for index, question in enumerate(questions):
        validation.require_type(f"questions[{index}]", question, rubric.Question)
    validation.require_list_or_tuple("responses", responses)
    for index, response in enumerate(responses):
        validation.require_type(f"responses[{index}]", response, rubric.GradedResponse)
    validation.require_type("category_weights", category_weights, dict)

    question_ids = {question.id for question in questions}
    responses_by_qid = {}
    for response in responses:
        if response.question_id not in question_ids:
            raise errors.ValidationError(
                f"invalid: response references unknown question {response.question_id}"
            )
        responses_by_qid.setdefault(response.question_id, []).append(response)

    for question in questions:
        matches = responses_by_qid.get(question.id, [])
        if len(matches) == 0:
            raise errors.ValidationError(f"invalid: question {question.id} has no response")
        if len(matches) > 1:
            raise errors.ValidationError(
                f"invalid: question {question.id} has more than one response"
            )

    categories_in_questions = []
    for question in questions:
        if question.category not in categories_in_questions:
            categories_in_questions.append(question.category)

    for category in categories_in_questions:
        if category not in category_weights:
            raise errors.ValidationError(f"invalid: category {category} is missing a weight")
    for category in category_weights:
        if category not in categories_in_questions:
            raise errors.ValidationError(
                f"invalid: category_weights has an unknown category {category}"
            )

    weights = {}
    weight_sum = Decimal("0")
    for category in categories_in_questions:
        weight = validation.require_non_negative_decimal(
            f"category_weights[{category}]", category_weights[category]
        )
        weights[category] = weight
        weight_sum += weight
    if weight_sum != Decimal(100):
        raise errors.ValidationError("invalid: category_weights must sum to 100")

    active_clock = clock if clock is not None else clock_module.SystemClock()
    graded_on = active_clock.now()

    scores_by_category = {}
    for question in questions:
        response = responses_by_qid[question.id][0]
        percent = rubric.score_question(question, response.points_earned)
        scores_by_category.setdefault(question.category, []).append(percent)

    unrounded_averages = {
        category: sum(scores, Decimal("0")) / Decimal(len(scores))
        for category, scores in scores_by_category.items()
    }

    overall_percent_unrounded = sum(
        (unrounded_averages[category] * weights[category] / Decimal(100)
         for category in categories_in_questions),
        Decimal("0"),
    )
    overall_percent = formatting.round_percent(overall_percent_unrounded, 1)
    letter_grade = _letter_grade(overall_percent)

    category_breakdown = tuple(
        CategoryScore(category, formatting.round_percent(unrounded_averages[category], 1))
        for category in sorted(categories_in_questions)
    )

    _LOGGER.info(
        f"report student={student_id} categories={len(category_breakdown)} "
        f"overall={formatting.format_percent(overall_percent)} grade={letter_grade}"
    )

    return ReportCard(
        student_id=student_id,
        graded_on=graded_on,
        overall_percent=overall_percent,
        letter_grade=letter_grade,
        category_breakdown=category_breakdown,
    )
