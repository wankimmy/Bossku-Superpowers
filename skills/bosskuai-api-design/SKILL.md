---
name: bosskuai-api-design
description: "Use when designing an API contract across REST, GraphQL, and event-driven interfaces: resource modeling, versioning, errors, pagination, idempotency, and integration-facing correctness."
---

# API design

Use when the open question is the shape of the contract between systems, not just the code behind it.

1. **Read the current contract surface** before proposing anything: docs, OpenAPI/GraphQL schema, event schemas, handlers, and their tests.
2. **Model the domain**: name resources and operations after business concepts, not database tables, and make side effects explicit in the operation name.
3. **Pick the contract style on purpose** — REST, GraphQL, events, or mixed — matched to who actually consumes it, and say why.
4. **Design the unhappy paths as part of the contract, not an afterthought**: auth failure, validation errors, conflicts, timeouts, async completion, rate limits. Make errors structured and machine-readable, never a freeform string.
5. **Make the safe path the easy path**: idempotency keys for retry-safe operations, stable pagination, predictable filtering and sorting.
6. **State what's additive vs breaking for every change**, and the versioning or deprecation path for the breaking ones.
7. **For events and webhooks**, settle ordering, replay, deduplication, and signature verification before calling the design done.
8. **When a requirement is ambiguous and nobody can confirm it**, default to the additive, backward-compatible reading and say so in one line rather than guessing at the breaking one.

For public or partner APIs, also settle these:

- **Contract first.** Review the spec for naming, resource model, and long-term fit before any implementation, and validate the whole document with an OpenAPI validator before generating clients. Generate SDKs and reference docs from the spec so they cannot drift.
- **Be consistent everywhere:** one field-naming style, one date format (ISO 8601), one ID format, one pagination style, one error shape.
- **Additive or breaking.** Safe: a new optional response field, a new endpoint, a new optional parameter, a new error code inside the existing shape, a looser validation rule, a new enum value (only if clients are documented to tolerate unknown values). Breaking: removing or renaming a field, changing a type or format, making an optional parameter required, removing an enum value, changing default behaviour or error structure, a tighter validation rule. Run a spec-diff in CI to block breaking changes without a version bump.
- **Deprecation runway:** announce with a migration guide, send `Deprecation` and `Sunset` headers, log who still calls it, contact the remaining callers, and remove only after usage is near zero and the date has passed.
- **Errors:** a stable machine-readable code, a readable message, a request id, and correct HTTP status. A 200 with an error body is a bug.
- **Rate limits are communicated:** return limit, remaining, and reset headers, and a 429 with `Retry-After`.

Check before you finish: no internal DB shape leaks into the public contract without a reason, no versioning was added without a named compatibility problem it solves, and every webhook/event flow has replay, idempotency, and authenticity.

Full design-lens checklist and output template: `reference.md`.

Public API checks adapted in part from engineering/engineering-api-platform-engineer.md (agency-agents, MIT).
