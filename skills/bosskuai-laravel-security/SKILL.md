---
name: bosskuai-laravel-security
description: "Use when reviewing or hardening a Laravel codebase before a security-sensitive merge or release: auth, authorization, Eloquent safety, CSRF/XSS, API security, production config."
license: MIT
metadata:
  author: affaan-m/ECC
  source: laravel-security
---

# Laravel Security Best Practices

Comprehensive security guidelines for Laravel applications to protect against common vulnerabilities.

> Laravel 11+ apps have no `app/Http/Kernel.php`, `RouteServiceProvider`, `AuthServiceProvider`, or `VerifyCsrfToken` class. Register middleware, CSRF exceptions, and trusted proxies in `bootstrap/app.php` (`->withMiddleware(function (Middleware $middleware) { $middleware->validateCsrfTokens(except: ['stripe/*']); })`) and gates, policies, and rate limiters in `AppServiceProvider::boot()`. Snippets below that name those classes apply only to Laravel 10 and earlier: check `bootstrap/app.php` first.

## When to Activate

- Setting up Laravel authentication and authorization (Sanctum, Passport, Jetstream, Breeze)
- Implementing user roles, permissions, and policies
- Configuring production security settings and environment variables
- Reviewing Laravel applications for security vulnerabilities
- Deploying Laravel applications to production
- Writing secure Eloquent queries and migrations

## How to use this skill

Work through the checklist below. For each item that applies, open the matching section of [`reference.md`](reference.md) for the code: production configuration and HTTPS, authentication (Sanctum, passwords, sessions), authorization (gates, policies, middleware), Eloquent mass assignment and SQL injection, CSRF, XSS, input validation, API security (rate limits, Sanctum vs Passport, CORS), file uploads, dependencies and secrets, queues, and security logging.

## Quick Security Checklist

| Check | Description |
|-------|-------------|
| `APP_DEBUG=false` | Never run with debug enabled in production |
| `APP_KEY` set | Always run `php artisan key:generate` |
| HTTPS enforced | Force HTTPS in production via middleware or proxy |
| `$fillable` whitelisted | Never use `$guarded = []` |
| CSRF active | `@csrf` on all state-changing forms |
| Sanctum/Passport configured | API authentication with token abilities/scopes |
| Rate limiting applied | Throttle API and auth endpoints |
| Input validation | FormRequest with specific rules, never `$request->all()` |
| File upload restrictions | Validate MIME types, size, dimensions |
| `composer audit` in CI | Check dependencies for known vulnerabilities |
| `password_hash` / `password_verify` | Use Laravel's built-in hashing (bcrypt/Argon2) |
| Session regeneration on login | Call `$request->session()->regenerate()` |
| Security headers middleware | CSP, X-Frame-Options, X-Content-Type-Options |
| Logged security events | Audit log for auth failures, role changes, suspicious activity |
| `.env` not committed | Verify `.gitignore` includes `.env` |
| `APP_KEY` exposure | A leaked key lets attackers forge encrypted cookies and payloads; rotate with `APP_PREVIOUS_KEYS` (Laravel 11+) so sessions survive |
| `hash_equals()` for tokens and signatures | Never use `==`. PHP reads numeric strings such as `0e123` as numbers, so two different hashes can compare equal |
| Webhook signatures | Verify over the raw body (`$request->getContent()`) before parsing, reject old timestamps, and skip event ids you have already handled |
| Queued jobs | A job keeps the ids it was queued with. Re-check tenant, owner and state inside `handle()`, because the row may have changed or moved |
| One-time actions | Coupons, refunds, invites and OTPs run once. Inside `DB::transaction()`, either lock the row with `lockForUpdate()`, or run a conditional update such as `WHERE used_at IS NULL` and act only when the update returns 1. Test that a repeated request has no second effect |
| Server-side money | Recompute prices and totals on the server. Accept amounts as integer cents, and reject negatives, zero where it is wrong, and huge values |
| Trusted proxies | Behind a load balancer, set trusted proxies in `bootstrap/app.php`. If `X-Forwarded-For` is trusted from any address, a client can fake its IP and dodge IP rate limits |

## Review output

```text
Laravel: [version] - Skeleton: [10-style Kernel | 11+ bootstrap/app.php]
Findings: P0/P1/P2 - [file:line] - [issue] - [fix]
Verification: composer audit; php artisan route:list -v (auth and throttle middleware on every sensitive route); grep for `$guarded = []`, `{!!`, `$request->all()` into create/update, raw SQL with interpolation
Unverified: [...]
```

## Related Skills

- `bosskuai-laravel-development` — Laravel architecture, routing, Eloquent, and API patterns
- `bosskuai-laravel-tdd` — Laravel testing with PHPUnit and Pest
- `bosskuai-laravel-verification` — full lint → test → security → deploy-readiness gate
- `bosskuai-cybersecurity-risk` — broader threat modeling beyond the Laravel layer
- `bosskuai-tenant-isolation-security` — tenant scoping and data-leak review
- `../../references/checklists/engineering-quality-bar.md`: the shared bar, with the scenario walk and production data checks.
