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

Check before you finish: no internal DB shape leaks into the public contract without a reason, no versioning was added without a named compatibility problem it solves, and every webhook/event flow has replay, idempotency, and authenticity.

Full design-lens checklist and output template: `reference.md`.
