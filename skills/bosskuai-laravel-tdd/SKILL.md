---
name: bosskuai-laravel-tdd
description: Use when writing or testing Laravel features test-first, with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage.
license: MIT
metadata:
  author: affaan-m/ECC
  source: laravel-tdd
---

# Laravel Testing with TDD

Test-driven development for Laravel applications using PHPUnit, Pest, Laravel factories, and testing helpers.

## When to Activate

- Writing new Laravel applications or features
- Implementing API endpoints with Sanctum or Passport authentication
- Testing Eloquent models, relationships, scopes, and accessors
- Setting up testing infrastructure for Laravel projects
- Writing feature tests for HTTP controllers and form requests
- Mocking external services (queues, mail, notifications, HTTP)

## TDD Workflow for Laravel

### Red-Green-Refactor Cycle

```php
// Step 1: RED — Write a failing test
public function test_a_product_can_be_created(): void
{
    $product = Product::factory()->create(['name' => 'Test Product']);
    $this->assertDatabaseHas('products', ['name' => 'Test Product']);
}

// Step 2: GREEN — Write the migration, model, and factory
// Step 3: REFACTOR — Improve while keeping tests green
```

## Where the patterns are

[`reference.md`](reference.md) holds the code for each step: PHPUnit and base TestCase setup, model factories, model, feature/HTTP, JSON API and Sanctum tests, fakes (HTTP, mail, notification, queue, storage, event), Artisan command and authorization tests, Pest, and coverage. Open the section the current test needs.

## Testing Best Practices

### DO

- Use factories over manual `create()` calls
- One logical assertion per test
- Descriptive names: `test_guests_cannot_create_products`
- Test edge cases and authorization boundaries
- Mock external services with `Http::fake()`, `Mail::fake()`
- Use `RefreshDatabase` for clean state
- Run feature tests on the same database engine and version as production (MySQL, MariaDB or PostgreSQL), not SQLite. Type coercion, collation and strict mode differ, so a SQLite pass proves little. Use a separate, disposable test database. Never point tests at production or at a production data copy, because RefreshDatabase drops every table on its connection.
- Build fixtures from production shapes: money as the string production returns, `NULL` in legacy columns, soft-deleted rows, and old JSON shapes. Add one case per shape.
- Fake the failures of every outbound call: `Http::sequence()` for a 503 and then a success, `Http::failedConnection()` for a timeout (it raises `Illuminate\Http\Client\ConnectionException`), and a body with a missing or re-typed field.
- For jobs, call `handle()` twice with the same payload and assert one effect. Also run a payload shaped like one queued before the last deploy.
- For webhooks, replay the same event, send an older event after a newer one, and send a bad signature. The bad one must change nothing. Sign the raw body in the test.
- For one-time actions (coupon, refund, invite, OTP), send the same request twice and assert one effect. That catches a missing guard, but a single-threaded test cannot show a real race. So also write a two-connection race test, as bosskuai-integration-testing requires: two real connections, one shared row, started behind a barrier. Assert that one request wins, the other gets the defined error, and there is still one effect. Check that the unique key or lock stops the second request. Do not put this test in RefreshDatabase, because it runs in one transaction and the second connection cannot see the fixture row. Commit the fixtures and reset with DatabaseTruncation instead.
- Check the PHPUnit or Pest version in `composer.lock`, and read the docs for that version before you use an API.

### DON'T

- Don't test Laravel internals (trust the framework)
- Don't make tests dependent on each other
- Don't over-mock — mock only service boundaries
- Don't test private methods — test through the public interface
- Don't couple tests to HTML structure

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `RefreshDatabase` | Reset database between tests |
| `$this->actingAs($user)` | Authenticate as user |
| `$this->withToken($token)` | Bearer token auth for APIs |
| `Model::factory()->create()` | Create model with factory |
| `Model::factory()->count(5)->create()` | Create multiple records |
| `Http::fake([...])` | Mock HTTP calls |
| `Mail::fake()` | Trap sent mail |
| `Notification::fake()` | Trap sent notifications |
| `Queue::fake()` | Trap queued jobs |
| `Event::fake()` | Trap dispatched events |
| `Storage::fake('public')` | Trap file operations |
| `assertDatabaseHas` | Assert DB row exists |
| `assertSoftDeleted` | Assert soft-delete |
| `assertSessionHasErrors` | Assert validation errors |
| `assertForbidden` | Assert 403 status |

## Related Skills

- `bosskuai-laravel-development` — Laravel architecture, Eloquent, routing, and API patterns
- `bosskuai-laravel-security` — Laravel authentication, authorization, and secure coding
- `bosskuai-tdd-loop` — The repo-wide RED -> GREEN -> REFACTOR loop
- `bosskuai-laravel-verification` — verification gate to run after the tests are green
- `../../references/checklists/engineering-quality-bar.md`: the shared bar, with the scenario walk and production data checks.
