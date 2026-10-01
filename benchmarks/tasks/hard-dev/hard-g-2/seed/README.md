# gradebook

Grading engine for the quiz/exam platform.

## Modules

- `errors.py` - shared exception hierarchy.
- `validation.py` - shared input-validation helpers.
- `clock.py` - dependency-injected clock (never call `datetime`/`date` "now" directly).
- `formatting.py` - shared `Decimal` percentage rounding/formatting helpers.
- `rubric.py` - `Question`, `GradedResponse`, and `score_question` (the per-question scoring engine).

## Conventions

- Every error raised anywhere in this package subclasses `errors.GradebookError`; never raise a bare `ValueError`/`KeyError` from feature code.
  - `errors.ValidationError` messages always start with `"invalid: "`.
- Reuse `validation.py`'s helpers for argument checking instead of writing new `isinstance`/range checks; they already produce the exact right error type and message shape.
- Every percentage is a `decimal.Decimal`; never a `float`. Round with `formatting.round_percent` (ROUND_HALF_UP) and display with `formatting.format_percent`; nothing outside `formatting.py` calls `.quantize()` or formats a percentage itself.
- Every dataclass in this package is declared with `@dataclass(frozen=True)`.
- No module holds mutable module-level state; everything a function needs comes in through its parameters.
- Nothing calls `datetime.date.today()` directly. Anything that needs "the current date" takes a `clock` parameter defaulting to `clock.SystemClock()`, and calls `clock.now()` exactly once per top-level call.
- Public function names are `verb_noun` (`score_question`, `build_report_card`); dataclasses are `CamelCase` nouns.
- Import sibling modules with `import <module>` and call `<module>.<name>(...)`. Don't write `from <module> import <name>` for anything this README calls a shared helper -- some of our tests patch these helpers at the module level, and that only works if callers go through the module.
- Logging goes through `logging.getLogger(<name>)` using a dotted name starting with `"gradebook."`. Log at `INFO` exactly once per successful top-level call, with a plain `f"..."` message -- and never log anything if validation raised.
- Nothing in this package mutates a caller's list, tuple, or dict argument.

## Behaviour notes

`rubric.score_question` (already implemented -- summarized here only so new code knows what it can rely on): scores one response as `points_earned / max_points * 100`, **without rounding** -- rounding is deliberately left to callers that display a value, so that averaging several scores together never compounds an early rounding error.

We need a new report-card feature: `report_card.build_report_card(student_id, questions, responses, category_weights, clock=None)`, returning a frozen `ReportCard`.

- `student_id` must be a non-empty `str`. `questions` must be a non-empty `list`/`tuple` of `rubric.Question`. `responses` must be a `list`/`tuple` of `rubric.GradedResponse`. `category_weights` must be a `dict`.
- Every question must have **exactly one** response whose `question_id` matches it -- zero matches or more than one are both invalid (`"invalid: question {id} has no response"` / `"invalid: question {id} has more than one response"`). Every response's `question_id` must match some question -- a response for a question that doesn't exist is also invalid (`"invalid: response references unknown question {question_id}"`), not silently ignored.
- Every distinct `category` that appears among `questions` must have a matching key in `category_weights` (`"invalid: category {category} is missing a weight"`), and `category_weights` must not contain a key for a category that no question uses (`"invalid: category_weights has an unknown category {category}"`). Each weight is coerced the same way `validation.require_non_negative_decimal` coerces any other number, and the weights for exactly those categories must sum to precisely `100` (`"invalid: category_weights must sum to 100"`).
- For each category, compute its average as the plain arithmetic mean of `rubric.score_question(question, response.points_earned)` across every question in that category -- weighted equally **per question**, never weighted by `max_points`. Never recompute a question's percent any way other than calling `rubric.score_question`.
- `overall_percent` is the weighted sum of the **category averages**, using each category's weight from `category_weights` divided by `100`. This sum must be computed from the unrounded category averages -- not from the rounded values shown in `category_breakdown` -- and the result is rounded with `formatting.round_percent` exactly once, at the very end.
- `category_breakdown` is a `tuple` of frozen `CategoryScore(category, average_percent)` entries, one per distinct category, sorted alphabetically by `category`; each entry's `average_percent` is that category's average, rounded with `formatting.round_percent` for display.
- The letter grade is derived from the final, rounded `overall_percent`: `"A"` at `>= 90`, `"B"` at `>= 80`, `"C"` at `>= 70`, `"D"` at `>= 60`, otherwise `"F"`. Thresholds are inclusive at their lower bound.
- `graded_on` comes from calling the clock's `now()` -- the provided `clock`, or `clock.SystemClock()` when none is given. Call it exactly once.
- On success, log exactly one `INFO` record through `logging.getLogger("gradebook.report_card")`, with message `f"report student={student_id} categories={len(category_breakdown)} overall={formatting.format_percent(overall_percent)} grade={letter_grade}"`.
- Return a frozen `ReportCard` with exactly these fields, in this order: `student_id`, `graded_on`, `overall_percent`, `letter_grade`, `category_breakdown`.
