---
name: bosskuai-laravel-development
description: "Use when building, refactoring, or auditing Laravel code: Eloquent, validation, policies, jobs, events, migrations, service boundaries, and performance. Security hardening, test-first work, and pre-deploy checks have their own Laravel skills."
---

# BosskuAI Laravel Development

Use this skill when building, auditing, or refactoring Laravel applications.

## How this differs from nearby skills

- **`bosskuai-laravel-security`**: security review and hardening before a sensitive merge or release.
- **`bosskuai-laravel-tdd`**: writing Pest/PHPUnit tests first.
- **`bosskuai-laravel-verification`**: the pre-PR and pre-deploy check loop.
- **`bosskuai-redis-caching-queues`**: Redis, Horizon, queue and cache operations.

## Operating principles

- Follow the current project conventions first; improve only where the convention creates risk.
- Prefer Laravel-native features before custom abstractions: Form Requests, Policies, Jobs, Events, Notifications, Resources, Collections, casts, scopes, service container, config, queues, scheduler, and tests.
- Keep controllers thin: validate, authorize, call use case/service, return response.
- Put business rules in explicit domain/application services when they are reused or stateful.
- Treat migrations, queues, jobs, scheduled commands, and webhooks as production surfaces.

## Checklist

- Auth and authorization: policies/gates present for tenant/user-sensitive actions.
- Input boundaries: Form Request or explicit validation; no trusted request payloads.
- Eloquent: avoid N+1, ambiguous mass assignment, hidden lazy loading, over-broad `select *`, and model events with surprising side effects.
- Database: transactions around multi-write state changes; constraints match business rules.
- Queues: idempotent jobs, retry/backoff, timeout, failure logging, and safe serialization.
- APIs/webhooks: signature verification, replay protection, idempotency keys, response contracts, and audit trail.
- Testing: feature tests for user-visible behavior, unit tests for domain rules, integration tests for external boundaries.
- Performance: pagination, indexes, eager loading, caching with invalidation, and query profiling.

## Filament admin panels

When restructuring Filament resources, read the actual resource file first and check the installed Filament version before using any API below. Improve structure before decoration; icons, hints, and labels alone are not an improvement.

- A form with more than about 8 fields in one flat list needs a structural alternative: tabs for distinct groups (`persistTabInQueryString()` keeps the tab on reload), or related sections side by side in a grid.
- Sections that are usually empty become collapsible and collapsed. Repeaters get an `itemLabel()` so entries are recognisable. A repeater whose entries stand on their own may belong in a relation manager.
- Replace a row of ten radio buttons with a range slider or a compact inline radio grid. Edit forms can open with a short read-only summary of the record.
- Group navigation (about 7 items per group at most) and collapse rarely used groups.
- Keep guidance light: short labels, one guidance layer per field, no helper text on obvious fields, icons only where they help scanning.

## Guardrails

- Do not add repositories/services just to look enterprise.
- Do not bypass authorization because an admin route exists.
- Do not swallow exceptions without observability.
- Do not use raw SQL unless the performance or database feature justifies it; parameterize when used.
- Do not recommend package installs before checking Laravel built-ins.

## Output format

```text
Laravel version / evidence checked: [files]
Main finding: [one sentence]
Risks:
  P0/P1/P2 — [issue] — [why it matters] — [fix]
Implementation notes: [files / commands]
Verification: [tests / static analysis / commands]
Unverified: [anything not checked]
```

## References

- `../../references/playbooks/bosskuai-laravel-development-playbook.md`
- `../../references/checklists/laravel-development-checklist.md`
- `../../references/checklists/expert-cofounder-stack-checklist.md`

Filament section adapted in part from engineering/engineering-filament-optimization-specialist.md (agency-agents, MIT).
