# ratelimit

Token-bucket rate limiting for the API gateway.

## Modules

- `errors.py` - shared exception hierarchy.
- `validation.py` - shared input-validation helpers.
- `clock.py` - dependency-injected clock (never call `time.time()` directly).
- `buckets.py` - `TokenBucket` and `refill` (the per-bucket refill engine).

## Conventions

- Every error raised anywhere in this package subclasses `errors.RateLimitError`; never raise a bare `ValueError`/`KeyError` from feature code.
  - `errors.ValidationError` messages always start with `"invalid: "`.
- Reuse `validation.py`'s helpers for argument checking instead of writing new `isinstance`/range checks; they already produce the exact right error type and message shape.
- Every token count, rate, and timestamp is a `decimal.Decimal`; never a `float` -- this keeps refill math exact instead of drifting over a long-running bucket.
- Every dataclass in this package is declared with `@dataclass(frozen=True)`. A `TokenBucket` is never mutated in place -- an updated bucket is always a *new* object (`dataclasses.replace`, or building a new instance), and it is the caller's job to keep using the returned bucket afterward.
- No module holds mutable module-level state; everything a function needs comes in through its parameters.
- Nothing calls `time.time()` directly. Anything that needs "the current time" takes a `clock` parameter defaulting to `clock.SystemClock()`, and calls `clock.now()` exactly once per top-level call.
- Public function names are `verb_noun` (`refill`, `check_requests`); dataclasses are `CamelCase` nouns.
- Import sibling modules with `import <module>` and call `<module>.<name>(...)`. Don't write `from <module> import <name>` for anything this README calls a shared helper -- some of our tests patch these helpers at the module level, and that only works if callers go through the module.
- Logging goes through `logging.getLogger(<name>)` using a dotted name starting with `"ratelimit."`. Log at `INFO` exactly once per successful top-level call, with a plain `f"..."` message -- and never log anything if the call raised.
- Nothing in this package mutates a caller's list, tuple, or dataclass argument.

## Behaviour notes

`buckets.refill` (already implemented -- summarized here only so new code knows what it can rely on): tops a bucket's tokens up based on elapsed time since its last refill, capped at capacity, and raises if asked to refill to a time before the bucket's own last refill.

We need a new feature for processing a batch of requests against one bucket: `limiter.check_requests(bucket, costs, clock=None)`, returning a frozen `BatchDecision`. Running out of tokens is a normal, expected outcome here -- it is never an error; a denied request is reported in the result, not raised.

- `bucket` must be a `buckets.TokenBucket`. `costs` must be a non-empty `list`/`tuple` of positive `int`s -- one entry per queued request, in the order those requests should be considered. `costs` itself represents "how many tokens would this request cost", not an identifier.
- Refill the bucket exactly once, by calling `buckets.refill(bucket, now)` -- never re-derive the refill amount any other way -- where `now` comes from the clock (the provided `clock`, or `clock.SystemClock()` when none is given), called exactly once. That one refill is the only time-based update for the whole batch, no matter how many requests are in `costs`; if `buckets.refill` itself raises because `now` precedes the bucket's own `last_refill_at`, let that propagate unchanged.
- Walk `costs` **in order**, starting from the refilled token count, and decide each request independently against the *running* token count so far in this batch:
  - If the running count is `>=` that request's cost, it is **allowed**: subtract the cost from the running count.
  - Otherwise it is **denied**: the running count is left exactly as it was -- a denied request never consumes any tokens, so a later, cheaper request in the same batch can still be allowed even after an earlier, costlier one was denied. Every entry in `costs` gets a decision; a denial does not stop the batch.
- `decisions` is a `tuple` of frozen `RequestDecision` entries, one per entry in `costs`, **in the same order as `costs`** -- fields `cost`, `allowed`, `tokens_remaining` (in that order), where `tokens_remaining` is the running token count immediately *after* that request's decision was applied (unchanged from before it, if denied).
- `bucket_after` is a new `buckets.TokenBucket` with the same `bucket_id`, `capacity`, and `refill_rate` as the input `bucket`, but with `tokens` equal to the running count after the very last decision, and `last_refill_at` equal to `now`.
- On completion (this function does not have a failure mode of its own beyond input validation), log exactly one `INFO` record through `logging.getLogger("ratelimit.limiter")`, with message `f"batch bucket={bucket.bucket_id} requests={len(costs)} allowed={allowed_count} denied={denied_count}"`, where `allowed_count`/`denied_count` are how many of this batch's decisions were allowed/denied.
- Return a frozen `BatchDecision` with exactly these fields, in this order: `evaluated_at` (the same `now` used for the refill), `bucket_after`, `decisions`.
