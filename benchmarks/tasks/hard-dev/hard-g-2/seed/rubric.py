"""Grading rubric primitives.

This module is already correct and in production use -- do not change its
behavior. It exists here so new features can reuse it instead of
re-deriving a question's percent score by hand.
"""
from dataclasses import dataclass
from decimal import Decimal

import errors
import validation


@dataclass(frozen=True)
class Question:
    """One question on a rubric.

    Fields:
        id: ``str`` unique identifier for the question.
        max_points: ``Decimal`` the question is worth; must be > 0.
        category: ``str`` grouping used for weighted category averages
            (e.g. ``"homework"``, ``"exam"``, ``"quiz"``).
    """

    id: str
    max_points: Decimal
    category: str


@dataclass(frozen=True)
class GradedResponse:
    """One student's response to one question.

    ``points_earned`` may be any value from ``0`` up to (and including)
    the matching question's ``max_points`` -- partial credit is allowed.
    This dataclass performs no validation of its own; that happens in
    :func:`score_question`.
    """

    question_id: str
    points_earned: Decimal


def score_question(question, points_earned):
    """Score one response as a percent of ``question.max_points``.

    Validates, in this order:

    1. ``question`` is a :class:`Question` and ``points_earned`` is a
       ``Decimal`` (``errors.ValidationError`` otherwise).
    2. ``question.max_points`` is greater than ``0``.
    3. ``points_earned`` is between ``0`` and ``question.max_points``,
       inclusive.

    Returns an **unrounded** ``Decimal`` percent
    (``points_earned / max_points * 100``). This function never rounds --
    rounding is a display concern for callers, not a scoring concern, so
    that averaging several questions together never compounds an early
    rounding error.
    """
    validation.require_type("question", question, Question)
    validation.require_type("points_earned", points_earned, Decimal)
    if question.max_points <= 0:
        raise errors.ValidationError("invalid: max_points must be greater than 0")
    if points_earned < 0 or points_earned > question.max_points:
        raise errors.ValidationError(
            f"invalid: points_earned must be between 0 and {question.max_points}"
        )
    return (points_earned / question.max_points) * Decimal(100)
