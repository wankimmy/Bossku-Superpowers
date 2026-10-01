# garage

Fee engine for the parking garage billing system.

## Modules

- `errors.py` - shared exception hierarchy.
- `validation.py` - shared input-validation helpers.
- `clock.py` - dependency-injected clock (never call `datetime`/`date` "now" directly).
- `money.py` - shared `Decimal` rounding/formatting helpers.
- `sessions.py` - `RateCard`, `SessionRecord`, and `compute_session_fee` (the per-session billing engine).

## Conventions

- Every error raised anywhere in this package subclasses `errors.GarageError`; never raise a bare `ValueError`/`KeyError` from feature code.
  - `errors.ValidationError` messages always start with `"invalid: "`.
  - `errors.NotFoundError` messages always start with `"not_found: "`.
  - `errors.StateError` messages always start with `"conflict: "`.
- Reuse `validation.py`'s helpers for argument checking instead of writing new `isinstance`/range checks; they already produce the exact right error type and message shape.
- Every value representing money is a `decimal.Decimal`; never a `float`. Round with `money.round_money` (ROUND_HALF_UP) and display with `money.format_money`; nothing outside `money.py` calls `.quantize()` or formats a money value itself.
- Every dataclass in this package is declared with `@dataclass(frozen=True)`.
- No module holds mutable module-level state; everything a function needs comes in through its parameters.
- Nothing calls `datetime.datetime.now()` / `date.today()` directly. Anything that needs "the current date" takes a `clock` parameter defaulting to `clock.SystemClock()`, and calls `clock.now()` exactly once per top-level call.
- Public function names are `verb_noun` (`compute_session_fee`, `build_statement`); dataclasses are `CamelCase` nouns.
- Import sibling modules with `import <module>` and call `<module>.<name>(...)`. Don't write `from <module> import <name>` for anything this README calls a shared helper -- some of our tests patch these helpers at the module level, and that only works if callers go through the module.
- Logging goes through `logging.getLogger(<name>)` using a dotted name starting with `"garage."`. Log at `INFO` exactly once per successful top-level call, with a plain `f"..."` message (no `%s`-style args) -- and never log anything if validation raised.

## Behaviour notes

`sessions.compute_session_fee` (already implemented -- summarized here only so new code knows what it can rely on): a session within its rate card's grace period is free; otherwise its duration is rounded up to the nearest billing increment, charged by the full or partial hour, and capped at the rate card's `max_fee`.

We need a new monthly statement feature: `statements.build_statement(account_id, sessions, rate_card, is_member=False, clock=None)`, returning a frozen `Statement`.

- `account_id` must be a non-empty `str`. `sessions` must be a `list` or `tuple`; each element must be a `sessions.SessionRecord` (a different element type is invalid, named by its index, e.g. `"invalid: sessions[1] must be a SessionRecord"`). `rate_card` must be a `sessions.RateCard`. `is_member` must be a `bool`.
- An empty `sessions` sequence is valid: it produces a statement with zero lines and every total at `Decimal("0.00")`, except the statement fee below, which still follows the membership rule.
- Compute each session's fee by calling `sessions.compute_session_fee` -- never re-derive a per-session fee any other way.
- The statement's `lines` are the sessions sorted by `entry_time` ascending; sessions sharing an identical `entry_time` are ordered alphabetically by `vehicle_id`. Sort a copy -- never mutate the `sessions` argument (or anything inside it).
- `gross_total` is the sum of every line's fee. It is not rounded again -- each line's fee already came out of `compute_session_fee` rounded to the cent.
- A discount percentage applies to the *whole* `gross_total` (never to individual lines), based on `gross_total` alone: `15` at `>= 500`, `10` at `>= 200`, `5` at `>= 50`, `0` below `50`. Thresholds are inclusive at their lower bound.
- `discount_amount` is `gross_total * discount_percent / 100`, rounded with `money.round_money`. `net_total` is `gross_total - discount_amount`.
- A flat `Decimal("5.00")` statement fee is added to `net_total` to get `final_total` -- unless `is_member` is `True`, in which case the fee is waived entirely (it is not added, and it is not shown as a zero line). The statement fee is computed after the discount and is never itself discounted.
- `generated_on` comes from calling the clock's `now()` -- the provided `clock`, or `clock.SystemClock()` when none is given. Call it exactly once.
- On success, log exactly one `INFO` record through `logging.getLogger("garage.statements")`, with message `f"statement account={account_id} sessions={len(sessions)} total={money.format_money(final_total)}"`.
- Return a frozen `Statement` with exactly these fields, in this order: `account_id`, `generated_on`, `line_count`, `gross_total`, `discount_percent`, `discount_amount`, `statement_fee`, `final_total`, `lines`. `line_count` is `len(lines)`. `discount_percent` is an `int` (`0`, `5`, `10`, or `15`). `statement_fee` is `Decimal("0.00")` for members and `Decimal("5.00")` otherwise. `lines` is a `tuple` of frozen `StatementLine`s, each with fields `vehicle_id`, `entry_time`, `exit_time`, `fee`, in that order.
