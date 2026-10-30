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

- Versions: read PHP and Laravel from `composer.json` (`require.php`, `laravel/framework`) and `composer.lock`, and confirm them with `php -v` and `php artisan --version`. Check the support dates on laravel.com/docs/releases, write down the date, and use only APIs that exist in the installed version.
- Auth and authorization: policies/gates present for tenant/user-sensitive actions.
- Input boundaries: Form Request or explicit validation; no trusted request payloads.
- Eloquent: avoid N+1, ambiguous mass assignment, hidden lazy loading, over-broad `select *`, and model events with surprising side effects. Outside production, turn hidden lazy loads into errors with `Model::preventLazyLoading(! $this->app->isProduction())` in `AppServiceProvider::boot()`.
- Database: transactions around multi-write state changes; constraints match business rules. Two requests can both pass a check and then insert: `firstOrCreate` and `updateOrCreate` are select-then-insert. Put a unique index on the key. `firstOrCreate` and `updateOrCreate` re-read the row after a duplicate-key error, but only when the unique index covers the lookup attributes; otherwise the error is rethrown. A plain `create()` does not re-read, so catch `UniqueConstraintViolationException` around it, and lock balances and counters with `lockForUpdate()` inside `DB::transaction()`.
- Queues: idempotent jobs, retry/backoff, timeout, failure logging, and safe serialization. Dispatch after commit with `->afterCommit()` or the `after_commit` queue option, so a worker never runs before the rows it needs are committed.
- APIs/webhooks: signature verification, replay protection, idempotency keys, response contracts, and audit trail.
- Testing: feature tests for user-visible behavior, unit tests for domain rules, integration tests for external boundaries.
- Performance: pagination, indexes, eager loading, caching with invalidation, and query profiling.
- Types: a DECIMAL column can come back as a string, so read a real row before you compare money, and keep money in integer cents. PHP compares two numeric strings as numbers ("1e3" == "1000" is true), so use `===` and `in_array($x, $list, true)`.

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
Laravel and PHP version (`php -v`, `php artisan --version`, `composer.lock`; latest stable checked [date]) / evidence checked: [files]
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
- `../../references/checklists/engineering-quality-bar.md`

Filament section adapted in part from engineering/engineering-filament-optimization-specialist.md (agency-agents, MIT).

## Routing, models and migrations

- Use `Route::scopeBindings()` for nested routes so a child must belong to its parent in the URL (blocks cross-tenant access), and still authorize in a policy. Keep one parameter name per bound model (`{conversation}` for `Conversation`) and avoid double-nested prefixes; if a name maps to a different class, use `Route::model()` or `resolveRouteBinding()`.
- Models: explicit `$fillable`, enum or value-object casts (`Attribute::make` for money in cents), named scopes for reusable filters. Use a global scope or a named scope for the same filter, not both, unless you want layered behaviour; remember global scopes silently affect every query, including admin and job code.
- Controllers call a Form Request (rules plus `authorize()`), which can build a small DTO via `toDto()`, then an action or service. Return API Resources with a consistent envelope and paginated meta (page, per_page, total).
- Cache read-heavy queries and invalidate on the model events that change them; use cache tags for related groups.
- Migrations: anonymous-class files, plural snake_case tables, foreign keys with `constrained()` and an explicit delete rule, indexes on filtered columns, money stored as integer cents, and a working `down()`.
- Keep secrets in `.env` and read them only through `config/*.php`; run `config:cache` in production. After `config:cache`, `.env` is no longer loaded, so `env()` outside `config/*.php` returns null for any value that lives only in `.env`, and no error is raised.

Adapted in part from ECC skills/laravel-patterns (affaan-m/ECC, MIT).
