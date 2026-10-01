# warehouse

Lot-level inventory allocation engine for order fulfillment.

## Modules

- `errors.py` - shared exception hierarchy.
- `validation.py` - shared input-validation helpers.
- `clock.py` - dependency-injected clock (never call `datetime`/`date` "now" directly).
- `inventory.py` - `Lot`, `OrderLine`, `is_lot_expired`, and `available_lots_for_sku` (the lot-eligibility engine).

## Conventions

- Every error raised anywhere in this package subclasses `errors.WarehouseError`; never raise a bare `ValueError`/`KeyError` from feature code.
  - `errors.ValidationError` messages always start with `"invalid: "`.
  - `errors.InsufficientStockError` messages always start with `"insufficient_stock: "`.
- Reuse `validation.py`'s helpers for argument checking instead of writing new `isinstance`/range checks; they already produce the exact right error type and message shape.
- Every dataclass in this package is declared with `@dataclass(frozen=True)`.
- No module holds mutable module-level state; everything a function needs comes in through its parameters.
- Nothing calls `datetime.date.today()` directly. Anything that needs "today's date" takes a `clock` parameter defaulting to `clock.SystemClock()`, and calls `clock.now()` exactly once per top-level call, even if that date is used more than once inside it.
- Public function names are `verb_noun` (`is_lot_expired`, `allocate_order`); dataclasses are `CamelCase` nouns.
- Import sibling modules with `import <module>` and call `<module>.<name>(...)`. Don't write `from <module> import <name>` for anything this README calls a shared helper -- some of our tests patch these helpers at the module level, and that only works if callers go through the module.
- Logging goes through `logging.getLogger(<name>)` using a dotted name starting with `"warehouse."`. Log at `INFO` exactly once per successful top-level call, with a plain `f"..."` message -- and never log anything if the call raised.
- Nothing in this package mutates a caller's list, tuple, or dataclass argument.

## Behaviour notes

`inventory.available_lots_for_sku` (already implemented -- summarized here only so new code knows what it can rely on): returns the in-stock, non-expired lots for one SKU, in no particular order.

We need a new allocation feature: `allocation.allocate_order(order_lines, lots, strategy="FIFO", allow_partial=True, clock=None)`, returning a frozen `AllocationResult`.

- `order_lines` must be a non-empty `list`/`tuple` of `inventory.OrderLine`; no two lines may share the same `sku` (`"invalid: duplicate order line for sku {sku}"`). Each line's `quantity` must already be a positive `int` (that's `OrderLine`'s contract; this function still has to check it, the same way it checks everything else). `lots` must be a `list`/`tuple` of `inventory.Lot` (an empty `lots` sequence is valid -- it just means nothing is in stock). `strategy` must be exactly one of the strings `"FIFO"`, `"LIFO"`, or `"FEFO"`. `allow_partial` must be a `bool`.
- For each line, find that SKU's eligible lots with `inventory.available_lots_for_sku` -- never re-derive eligibility (in-stock, not expired) any other way -- then put them in draw-down order:
  - `"FIFO"`: ascending `received_at` (oldest stock first).
  - `"LIFO"`: descending `received_at` (newest stock first).
  - `"FEFO"`: ascending `expires_on`, soonest-to-expire first -- lots with `expires_on=None` (they never expire) are drawn **last**, after every dated lot, regardless of `received_at`.
  - Whenever two lots tie under the chosen strategy (equal `received_at`, or equal `expires_on` including both being `None`), break the tie alphabetically by `lot_id`.
- Draw from lots in that order, taking `min(remaining_needed, lot.quantity_on_hand)` from each lot until the line's `quantity` is met or eligible lots run out; a lot is never drawn from for more than its own `quantity_on_hand`. A lot that was eligible but never actually drawn from (because the line was already fully met before reaching it) does not appear in that line's result.
- If `allow_partial` is `True` (the default): any shortfall for a line becomes that line's `backorder_quantity` -- this is not an error. `allocated_quantity + backorder_quantity` always equals the line's requested `quantity`.
- If `allow_partial` is `False`: first determine, without allocating anything, whether *every* line's full quantity is available; if even one line's total eligible stock falls short, raise `errors.InsufficientStockError` for the **first** such line in `order_lines` order (`"insufficient_stock: {sku} cannot be fully allocated"`) and don't report any allocation for any line, including lines that did have enough stock. Only once every line clears this check does the function actually build the allocation (with every `backorder_quantity` at `0`).
- The returned `lines` are in the **same order as the input `order_lines`** -- this function does not reorder them.
- Each line's result is an `AllocationLine` with fields `sku`, `requested_quantity`, `allocated_quantity`, `backorder_quantity`, `lot_allocations` (in that order) -- `lot_allocations` is a `tuple` of plain `(lot_id, quantity)` tuples, in the order those lots were drawn from.
- `allocation_date` comes from calling the clock's `now()` -- the provided `clock`, or `clock.SystemClock()` when none is given. Call it exactly once, and use that same value both for expiry checks and for the result's `allocation_date`.
- On success (including the `allow_partial=False` case where every line clears), log exactly one `INFO` record through `logging.getLogger("warehouse.allocation")`, with message `f"allocation lines={len(order_lines)} strategy={strategy} backordered={total_backordered}"`, where `total_backordered` is the sum of every line's `backorder_quantity`.
- Return a frozen `AllocationResult` with exactly these fields, in this order: `allocation_date`, `strategy`, `lines`.
