---
name: bosskuai-polyglot-engineering
description: Use when a task spans several languages, frameworks, or runtimes, or ecosystem context changes the answer, rather than assuming one default stack.
---

# BosskuAI Polyglot Engineering

Use this skill when the task spans or depends on multiple languages, frameworks, or runtimes, or when language/ecosystem context materially changes the right recommendation.

## How this differs from nearby skills

- **`bosskuai-coding-best-practices`**: general quality patterns; this skill applies those patterns in a stack-aware way and adds ecosystem-specific gotchas.
- **`bosskuai-codebase-analysis`**: maps what exists; this skill explains why a stack behaves a certain way and what the ecosystem-native approach is.
- **`bosskuai-engineering-delivery`**: delivery workflow; this skill informs the stack-specific parts of that workflow.

## Mindset

- There is no universally correct language or framework — only the best fit for the constraints at hand.
- Native idioms beat ported patterns. A Go solution that looks like Java is wrong twice.
- Ecosystem maturity matters as much as language features: test tooling, deployment story, security advisory velocity, community momentum.
- Cross-language interop surfaces are the highest-risk seam in any polyglot system.

## Language ecosystem quick reference

| Language | Primary strengths | Common gotchas | Native test style |
|----------|------------------|----------------|-------------------|
| **TypeScript** | Type safety, ecosystem breadth, full-stack | `any` escape hatches, implicit coercion, bundler complexity | Jest / Vitest, `describe/it` |
| **Python** | Data, scripting, AI/ML, fast iteration | GIL limits true parallelism, mutable defaults, dynamic typing hides errors | pytest, fixtures-first |
| **Go** | Concurrency, performance, ops tooling | Verbose error handling, no generics before 1.18, import cycle restrictions | `testing` package, table-driven |
| **Rust** | Memory safety, systems, WASM | Steep learning curve, borrow checker, longer compile times | `#[test]`, `cargo test` |
| **Dart/Flutter** | Cross-platform mobile/desktop/web | Tree shake requires `const`, async gaps with `BuildContext`, widget rebuild cost | `flutter_test`, widget/unit/integration split |
| **Java/Kotlin** | JVM ecosystem, enterprise, Android | JVM startup latency, verbose boilerplate (Java), coroutine scope management (Kotlin) | JUnit, Mockito; KoTest for Kotlin |
| **Swift** | iOS/macOS, strong typing, ARC | ARC retain cycles, main-thread UI rules, Sendable/concurrency model | XCTest, async/await testing |
| **Ruby** | Developer ergonomics, Rails ecosystem | Duck typing hides contract violations, global state in Rails, slower runtime | RSpec, minitest |
| **PHP** | Web, WordPress/Laravel ecosystem | Legacy codebases, global state, inconsistent stdlib naming | PHPUnit, Pest |

## Ecosystem quality signals

Before recommending a library or framework, evaluate:
- **Maintenance**: last commit date, open issues trend, active maintainers
- **Community**: stars, downloads/week, StackOverflow presence
- **Security**: CVE history, security advisory response time
- **Compatibility**: version support for your runtime, breaking change policy
- **Alternatives**: if the library disappeared tomorrow, what would replace it?

## Cross-language interop surfaces (highest-risk seams)

When two languages or runtimes exchange data:
- Agree on a **schema contract** (JSON Schema, Protobuf, OpenAPI) — don't trust implicit serialization.
- Null/None/nil handling differs across languages — make it explicit in the schema.
- Date/time formats: always UTC ISO 8601 at the boundary; convert at the consuming end.
- Error representation: languages handle errors differently — standardize error shape at the API contract.
- Numeric types: integer overflow, float precision, and bigint handling differ — validate at the boundary.
- **String length:** PHP `strlen` counts bytes, `mb_strlen` counts characters, and JavaScript `length` counts UTF-16 units. Validate a maximum length in one unit, at the boundary.
- **Several runtimes:** a web app, a queue worker and CI can run different versions of one language. Check each one.
- **Money:** send integer minor units or a decimal string, and check how each side parses it. The type table in the shared bar (section 4) lists the traps for each language.

## CLI and developer-tool contract checks

A CLI's flags, output format, and exit codes are a contract with every script that calls it, whatever language it is written in.

- **Errors name the cause and the next step**, not just the failure. Keep stack traces behind `--verbose`.
- **Respect the pipe.** Detect a TTY: colour and tables for humans, plain stable output when piped. Offer `--json` or another parseable mode, `--quiet`, and honour `NO_COLOR`.
- **Exit codes are an API.** 0 for success, nonzero for failure, distinct codes for distinct failure classes.
- **Flags mean the same thing in every subcommand.** Document precedence: flag, then env var, then config file.
- **`--help` at every level**, with a one-line summary and real usage examples; the bare command shows an overview, not an error.
- **Safe by default.** Destructive actions confirm or need `--force`; anything that changes state has `--dry-run`.
- **Do not break the interface silently.** Renamed flags, changed output, or new exit codes get a deprecation warning and a migration note.
- **Keep startup fast.** Lazy-load subcommands, keep network calls off the hot path, and check startup time in CI for tools run many times a day. Pick the runtime with startup in mind.
- **First run:** the shortest path to a real result should not need sign-up or key setup. Test it with someone who has not used the tool.

## Testing note for TypeScript

For large typed fixtures in tests, check whether `@total-typescript/shoehorn` (`fromPartial`, `fromAny`) is already installed or acceptable before writing `as unknown as Type`. Use it in test code only, never in production code.

## Workflow

1. **Identify the actual stack**: language, version, framework, runtime, and build/deploy tools in use. Read each version from the file that proves it (the manifest, the lockfile, or the runtime's version command), and check the latest stable release live. The shared table in `../../references/checklists/engineering-quality-bar.md` (section 2) names the file and the source for each ecosystem.
2. **Apply native idioms first**: before recommending a pattern from another ecosystem, check whether the current language has a built-in or idiomatic equivalent.
3. **Minimal safe change**: prefer the framework-native solution before proposing a dependency or abstraction.
4. **Surface gotchas**: name the language-specific traps relevant to the current task.
5. **Ecosystem tradeoffs**: for any library or tool recommendation, give the quality signals above.
6. **Cross-language seams**: if data crosses a language boundary, apply the interop checklist.
7. **State what is universal vs stack-specific**: be explicit about what is general advice vs specific to this stack.

## Guardrails

- Do not recommend patterns from a different ecosystem without explaining the translation cost.
- Do not assume the same idiom works across languages: error handling in Go is not the same as in Python.
- Do not recommend a library without checking ecosystem quality signals.
- Do not state a version is current or latest from memory. Read it from the manifest or lockfile, and check the latest stable release live, with the date.
- Do not ignore the existing repo's stack version constraints — a Go 1.18 generic solution does not help a Go 1.16 codebase.

## Output format

```
Stack identified:
  Language: [language]
  Versions (language, framework, runtime): [current, from which file] / [latest stable, checked date]
  Framework: [framework]
  Runtime: [runtime]
  Build / test tooling: [tools]

Native idioms applied:
  [recommendation] — [why it is idiomatic for this stack]

Stack-specific gotchas for this task:
  [gotcha] — [how it affects this specific work] — [mitigation]

Library / dependency recommendations (if any):
  [library] — [purpose] — [quality signals: last update / downloads / alternatives]

Cross-language interop notes (if applicable):
  [boundary] — [schema contract] — [risk] — [mitigation]

Universal vs stack-specific:
  Universal: [advice that applies regardless of stack]
  Stack-specific: [advice specific to [language/framework]]

Tradeoffs:
  [option A vs option B] — [fit / maintenance / complexity / risk]
```

## References

- `../../references/checklists/polyglot-engineering-checklist.md`

CLI checks adapted in part from engineering/engineering-developer-tooling-engineer.md and product/product-dx-engineer.md (agency-agents, MIT); shoehorn note from misc/migrate-to-shoehorn (skills pack by Matt Pocock, MIT).
