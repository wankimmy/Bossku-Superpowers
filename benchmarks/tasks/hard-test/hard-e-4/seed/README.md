# allocate

A fair-division helper for splitting an integer total (seats, budget
units, server shards -- whatever's indivisible) proportionally across
several weighted recipients, using the **largest-remainder method**
(also called Hamilton's method): a real, named apportionment convention
with one genuinely tricky part (exact tie-breaking) that most informal
descriptions of it leave out. Add a new `allocate.py` module at the
project root with two functions and one exception class, following this
spec exactly.

`AllocationError` (a `ValueError` subclass) covers every "structurally
valid types, but can't be allocated" case below. `TypeError` covers wrong
argument types.

## `allocate(total, weights)`

- `total` must be a non-negative `int` (`TypeError` if it's not an `int`,
  including a `bool`; `AllocationError` if it's negative).
- `weights` must be a non-empty `list` or `tuple` of non-negative `int`s
  (`TypeError` for the wrong container type or a non-`int`/`bool` element;
  `AllocationError` for an empty `weights`, or a negative element).
  Weights are relative shares (vote counts, population, whatever) --
  never a `float`, to keep every computation exact.
- If `total == 0`, the result is `[0] * len(weights)`, **even if every
  weight is 0 too** -- there's nothing to allocate, so there's nothing to
  divide by zero over.
- Otherwise, if every weight is `0` (and `total > 0`), raise
  `AllocationError` -- there's no proportional basis to allocate against.
- Otherwise, compute each entry's *exact* quota,
  `total * weights[i] / sum(weights)`, as an exact fraction (use
  `fractions.Fraction`, not `float` -- a `float` computation can round
  two different quotas' fractional parts into the wrong order when
  they're very close, which would silently change who gets the extra
  seat). Each entry's base allocation is the integer floor of its quota.
- The bases always sum to at most `total`; the difference
  (`total - sum(bases)`, an integer between `0` and `len(weights) - 1`
  inclusive) is the number of leftover units still to hand out. Give one
  extra unit each to the entries with the **largest fractional
  remainder** (`exact quota - floor(quota)`), one at a time, until the
  leftover is used up.
- **Tie-break**: when two or more entries have exactly equal fractional
  remainders and only some of them can receive an extra unit, the ones
  with the **lower original index in `weights`** win first.
- The result is a `list` of `int`s, the same length as `weights`, that
  always sums to exactly `total`. `weights` (and `minimums`, below) is
  never mutated.

## `allocate_with_minimums(total, weights, minimums=None)`

Same as `allocate`, except every entry is first guaranteed a minimum
amount before the largest-remainder method distributes whatever's left.

- `minimums`, if given, must be a `list`/`tuple` of non-negative `int`s
  the same length as `weights` (`TypeError` for the wrong container type
  or a non-`int`/`bool` element; `AllocationError` for a length mismatch
  or a negative element). `minimums=None` (the default) means every
  entry's minimum is `0`, making this function behave exactly like plain
  `allocate`.
- If `sum(minimums) > total`, raise `AllocationError` -- the guarantees
  can't all be honored.
- Otherwise, run the **same largest-remainder method** described above
  on `total - sum(minimums)` (the leftover after guarantees) using the
  **original, unreduced `weights`** -- not weights adjusted for the
  minimums already granted -- and add each entry's share of that to its
  minimum. (So an entry's weight still determines its proportional claim
  on the *remaining* pool, same as if the minimums didn't exist; the
  minimums only set a floor underneath that.)
- The result sums to exactly `total`, same guarantee as `allocate`.

A couple of basic checks are sketched in `tests/test_allocate.py`.
