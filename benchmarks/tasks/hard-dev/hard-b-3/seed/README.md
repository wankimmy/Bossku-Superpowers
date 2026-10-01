# Library Loan System

Tracks book checkouts, returns, and late fees. "Today" is always passed
in explicitly as a plain integer day number (never read from the clock),
so all the examples below just use small integers.

Run tests: `python -m unittest discover -s tests`

## Members

- `Members.add_member(member_id, name)` registers a member. Member ids
  are matched **case-insensitively** and ignoring leading/trailing
  whitespace everywhere (`"Alice@Lib"`, `"alice@lib"` and `" ALICE@LIB "`
  all refer to the same member). Adding a member whose normalized id is
  already registered raises `ValueError`.
- `Members.get(member_id)` looks up a member (same normalization);
  raises `KeyError` if no such member exists.
- Each member has a `balance` (a `Decimal`, starts at `0.00`) and a
  `loan_history` list of every loan id they've ever had, in the order
  they were checked out. A brand-new member always starts with an
  **empty** `loan_history` of their own — it is never shared with any
  other member.
- A member whose `balance` is **$5.00 or more** is blocked from
  checking out new books (see `is_blocked` below) until they pay it back
  down below $5.00.

## Catalog

- `Catalog.add_title(isbn, title, copies)` registers a title with that
  many copies. Raises `ValueError` if the isbn is already registered.
- `Catalog.available(isbn)` / `Catalog.title_of(isbn)` look up a title;
  raise `KeyError` for an unknown isbn.

## Checkout

`LibrarySystem.checkout(isbn, member_id, today)`:

- raises `KeyError` if `isbn` or `member_id` is unknown;
- raises `ValueError` if the member `is_blocked(member_id)`;
- raises `ValueError` if there are no available copies of `isbn`;
- otherwise creates a loan due back on `today + 14`, decrements the
  book's available copies by one, appends the new loan id to the
  member's `loan_history`, and returns the new `loan_id` (an int,
  starting at 1 and incrementing by 1 per loan made on a given
  `LibrarySystem`).

## Returning a book and late fees

`LibrarySystem.return_book(loan_id, today)`:

- raises `KeyError` if `loan_id` was never issued by this system;
- raises `ValueError` if that loan was already returned;
- otherwise marks the loan returned, gives the copy back to the catalog
  (increasing `available` by one), charges any late fee (below) to the
  member's balance, and returns the fee that was charged (a `Decimal`,
  `0.00` if the book wasn't late).

**Grace period:** members get one full day after the due date with no
fee. A book is only *billable* starting on the **second** day after the
due date. In other words, if `days_late = today - due_day`, the number
of **billable late days** is `max(0, days_late - 1)`.

**Fee schedule:** `fee_for_billable_days(n)` (in `library/loans.py`) is
the amount charged for `n` billable late days: **25 cents per billable
day**, capped at **$10.00** per returned loan. `return_book` charges
exactly `fee_for_billable_days(billable_late_days)`.

For example, with a due day of 14: returning on day 14 or 15 owes
nothing (day 15 is the grace day); returning on day 16 is 1 billable
day ($0.25); returning on day 54 or later is capped at $10.00.

## Paying fees and blocking

- `LibrarySystem.is_blocked(member_id)` returns whether that member is
  currently blocked (balance >= $5.00, see "Members" above). This must
  always reflect the member's **current** balance — immediately after
  any `return_book` fee is charged or any `pay_fee` payment is made,
  the very next `is_blocked` call already reflects it.
- `LibrarySystem.pay_fee(member_id, amount)` reduces the member's
  balance by `amount`. Raises `ValueError` if `amount` is not positive,
  or if `amount` is more than the member's current balance (no
  overpaying / no negative balances).
