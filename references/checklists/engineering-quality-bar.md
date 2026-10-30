# Engineering Quality Bar

The bar every engineering skill builds, verifies and reviews against (user rules, 2026-10-30). Zero tolerance: a known bug, an error, or a path that does not work is never "done" and never a nit. No section is skipped: a section that cannot apply is marked "not applicable: <reason>" in the result, which is not a skip. When something a section needs is missing (a production data copy, access, the linked issue, screenshots), ask the user to prepare it; until it arrives, the result is "provisional (missing: <input>)" and nothing is approved or called done.

## 1. Goal, requirements and the current system

- [ ] Before writing code, map the project's current infra architecture: where each part runs (hosting, containers or serverless), the web, worker and scheduler processes, databases, caches, queues, storage and CDN, how config and secrets reach each environment, how deploys and migrations run, and how many instances run at once. Read it from the repo (compose files, Dockerfiles, IaC, CI/CD workflows, env examples, deploy docs) and ask the user for what is not there.
- [ ] Judge the change against that map: several instances at once (in-memory state, local files, sessions, a cron or scheduler running twice), workers and queues, each environment, and the moment of deploy.
- [ ] The goal is stated from the request, the PR description and the linked issue (Linear, GitHub).
- [ ] Every requirement in the issue is numbered and mapped to the code and the test that prove it.
- [ ] The PR description matches the diff: nothing claimed that is not there, nothing changed that is not described.
- [ ] The whole diff is read against its base, on a re-review too, not only the new commits.

## 2. Versions: know the current and the latest

- [ ] **Current:** read the version the project really runs from its manifest, lockfile or runtime (table below), not from memory or the newest docs.
- [ ] **Latest:** check the latest stable release and its support dates at work time on the official page (or endoflife.date, for example `https://endoflife.date/php`), and write down the date you checked.
- [ ] Use only APIs that exist in the installed version; read the docs for that version (Context7 or the official docs). A feature from a newer version needs an upgrade decision, not a silent bump.
- [ ] Flag a runtime or framework that is end-of-life or security-only, and list breaking changes between current and target before any upgrade.

| Ecosystem | Current version from | Latest and support from |
| --- | --- | --- |
| PHP | `php -v`, `composer.json` `require.php`, `composer.lock` | php.net/supported-versions.php |
| Node.js, TypeScript | `node -v`, `.nvmrc` or `.node-version`, `package.json` `engines`, the lockfile; `npx tsc -v` | nodejs.org/en/about/previous-releases |
| Python | `python --version`, `pyproject.toml` `requires-python`, `uv.lock`, `poetry.lock` or `requirements*.txt` | devguide.python.org/versions |
| Go | `go.mod` `go` and `toolchain` lines, `go version` | go.dev/doc/devel/release |
| Rust | `rust-toolchain.toml`, `Cargo.toml` `rust-version` and `edition`, `Cargo.lock` | blog.rust-lang.org release posts |
| Java, Kotlin | build toolchain (`maven.compiler.release`, Gradle `jvmToolchain`), `java -version`, Kotlin plugin version | endoflife.date/java, kotlinlang.org/docs/releases.html |
| .NET (C#, F#) | `global.json`, `<TargetFramework>` in project files, `dotnet --info` | dotnet.microsoft.com/platform/support/policy/dotnet-core |
| Dart, Flutter | `pubspec.yaml` `environment: sdk`, `pubspec.lock`, `flutter --version` | docs.flutter.dev/install/archive (release dates only, no support dates) |
| Swift | `Package.swift` `swift-tools-version`, Xcode version, `swift --version` | swift.org/download |
| Ruby, Rails | `.ruby-version`, `Gemfile.lock` | ruby-lang.org/en/downloads/branches, rubyonrails.org/maintenance |
| Databases | `SELECT VERSION();` (MySQL, MariaDB), `SELECT version();` (PostgreSQL), `db.version()` (MongoDB), `INFO server` (Redis) | the vendor's release page or endoflife.date |
| Containers | base image tag and digest in the Dockerfile | the image's official registry page |

## 3. Correctness and scenarios

- [ ] Edge cases: empty, one, many, duplicates, zero, negative, maximum, boundaries, null, wrong type, very long input, non-ASCII text.
- [ ] Walk every scenario through the code: who (anonymous, a normal user, another tenant, each role, admin, a background job), what (valid, boundary, empty, malformed, wrong type), when (first time, repeated, concurrent, retried, delayed, out of order), the record's state (new, in progress, done, cancelled, deleted, locked) and each dependency (up, down, slow, changed response).
- [ ] Race conditions: two users or jobs on the same row, double submits, check-then-act. Guard with a transaction and row lock, an atomic update, a unique constraint or an idempotency key.
- [ ] Retries and partial failure: no side effect happens twice, and a failure halfway leaves no half-written state.
- [ ] Business logic: new rules do not clash with existing flows, roles or data.
- [ ] UI: each state (empty, loading, error, success, disabled) shows a message that matches the result, a disabled control says why, and the same thing uses the same words everywhere. A confusing or wrong-for-the-state message is a bug to fix, not a nit.

## 4. Data: no data issues, no gaps

- [ ] Run the change (migration, backfill, queries, new rules) against a production data copy with personal data and secrets masked (types and formats kept), never production itself, and compare counts and results with what deploy should give. Keep that copy out of git, logs, test output and test fixtures.
- [ ] Find the rows it would miss, break or change by surprise: nulls, legacy values, duplicates, orphans, soft-deleted rows, very old records, other locales and time zones.
- [ ] Types and structure match production, not just fixtures: numeric types, money as a string or a number (0.01 vs "0.01"), JSON shapes and missing keys, enum values the code does not know, date formats and time zones, encodings and collations, ID types.
- [ ] Test fixtures are shaped like production data.

The same value can arrive with a different type:

| Language | Watch for |
| --- | --- |
| PHP | DECIMAL columns come back as strings. Before PHP 8.1, integers and floats also come back as strings through PDO with emulated prepares. From PHP 8.1 they come back as int and float unless PDO::ATTR_STRINGIFY_FETCHES is set to true. `==` still juggles numeric strings (`"1" == "01"` is true). Cast on purpose, compare with `===`, keep money in integer cents or bcmath. |
| JavaScript, TypeScript | JSON numbers are doubles: `0.1 + 0.2 !== 0.3`, and integers above 2^53 − 1 lose precision, so send big IDs as strings. TypeScript types do not check runtime JSON; validate at the boundary with a schema. |
| Python | `json.loads` turns 0.01 into a float unless you pass `parse_float=Decimal`. `"0.01" == 0.01` is False, so mixed types compare unequal without an error. |
| Go | Decoding into `any` makes every number a float64; use typed structs or `Decoder.UseNumber()`. A quoted number fails to decode unless the field has the `,string` tag option. |
| Java, Kotlin | Build `BigDecimal` from a string; `equals` compares scale (2.0 is not 2.00), so use `compareTo`. Jackson coerces "0.01" into number fields by default; decide that on purpose. |
| C# | Use `decimal` for money. System.Text.Json rejects a quoted number unless `JsonNumberHandling.AllowReadingFromString` is set, which the web defaults do. |
| Rust | serde rejects a string where a number is expected unless the field has a custom deserializer; keep money in integer cents or a decimal crate. |
| Dart | On the Dart VM, `jsonDecode` gives an int for `1` and a double for `1.5`, so `as double` throws on whole numbers; use `(value as num).toDouble()`. |
| Swift | `Codable` throws `typeMismatch` when a number arrives as a string; handle both shapes or fail loudly. Use `Decimal` for money. |
| Ruby | `JSON.parse` turns 0.01 into a Float; pass `decimal_class: BigDecimal` for money. |
| SQL | Money in DECIMAL, never FLOAT. MySQL casts when a string column is compared with a number: `'123abc' = 123` matches and the index is skipped. |

## 5. API integrations (calling or serving an API)

- [ ] The endpoint down, slow or timing out: explicit connect and read timeouts, and a clear result for the caller.
- [ ] Retries only for calls that are safe to repeat (idempotent methods such as GET, PUT and DELETE, or a POST with an idempotency key), with exponential backoff, jitter, a capped wait and an attempt limit; decide whether that is enough.
- [ ] Delay: can the caller wait? If not, move the call to a queue; stop calling a dependency that keeps failing.
- [ ] Logs record each request and response (method, URL, status, duration, correlation id) with secrets and personal data masked.
- [ ] Response drift: extra fields are ignored; missing fields, changed types and unknown enum values are validated and rejected loudly, never coerced silently.
- [ ] Rate limits (429 and `Retry-After`), pagination to the last page, webhook signatures, duplicates and out-of-order delivery.
- [ ] A test for each case above, with recorded or faked responses.

## 6. Users, operations and deploy

- [ ] The effect on existing users, roles, data and day-to-day operations is known; risky changes go behind a flag.
- [ ] Zero downtime: old code runs on the new schema and new code on the old (expand, migrate, contract); no long locks on large tables; backfills in chunks.
- [ ] Jobs queued before the deploy still run on the new code; cache keys or formats that change are versioned; config and env vars exist before the code reads them.
- [ ] The rollback path is known and safe for data written after the deploy.
- [ ] Logs, metrics and alerts show whether it works after deploy.

## 7. Code quality

- [ ] Follows best practice and the repo's own patterns, structure and naming; no second copy of an existing helper.
- [ ] No errors: build, type-check, lint and tests run clean in this session, with no new warnings and no swallowed exceptions.
- [ ] Security at High and Critical, business and logic flaws included: `bosskuai-security-gate`. A High or Critical advisory is fixed by upgrading, even a major version, never by an exception. If no fixed release exists (check the registry for a later version first), the advisory stays open and the gate stays BLOCK. Name it in the reply, add a mitigation that cuts the exposure now, and ask the user to choose: wait for a fixed release, replace the package, or remove the feature. A mitigation does not close it, and accepting the risk is not an option for High or Critical. Check every security severity. Medium and Low may be excepted with a written reason, as the security gate's Alert threshold says; that covers security hardening only. A business or logic flaw that makes the product do the wrong thing is a bug, fixed at any rating.
- [ ] Performance: no queries or calls in loops, bounded memory, indexes for new queries.

## 8. Proof

- [ ] CI is green on the head being shipped or reviewed. Never approve or call ready with a red or pending check, even a known flake.
- [ ] Every visual change has screenshots at the sizes the repo asks for, each checked against the change.
- [ ] Each fix has a test that failed before it and passes after.
- [ ] The PR carries only files that belong to the change. Agent working files (plans, work-item notes, handoffs, scratch scripts, logs, local config) stay out unless the repo keeps them on purpose, and then they are current and match the code.

## 9. Investigating a problem

- [ ] Map the whole surface first: every screen, endpoint and job under the reported path (list, detail, edit, create, each tab, modals, exports), read from the routing config, not only the one URL named.
- [ ] Measure each part on a masked production data copy: time each call and read what it loads (query count, eager-loaded relations, rows scanned, payload size).
- [ ] Re-read the output you already have before running more; anything surprising is a lead.
- [ ] Keep a coverage table (part, call, time, what it loads, checked yes or no). Never conclude "not the cause" while a row is unchecked; name the unchecked parts and why.
- [ ] With no masked copy, ask the user to prepare one and keep that check open. Ask the user to measure production only as a last resort, after checking everything you can reach yourself, and say exactly what you need.
