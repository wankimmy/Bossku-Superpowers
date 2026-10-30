---
name: bosskuai-tinystruct-patterns
description: "Use when the task explicitly concerns tinystruct patterns. Expert guidance for developing with the tinystruct Java framework. Use when working on the tinystruct codebase or any project built on tinystruct — including generating the bin/dispatcher and bin/dispatcher.cmd launcher scripts when a project lacks them, creating Application classes, @Action-mapped routes, unit tests, ActionRegistry, HTTP/CLI dual-mode handling, the built-in HTTP server, the event system, JSON with Builder/Builders, database persistence with AbstractData, POJO generation, Server-Sent Events (SSE), file uploads, and outbound HTTP networking."
metadata:
  origin: ECC-adaptation
---

# tinystruct Development Patterns — portable workflow

Expert guidance for developing with the tinystruct Java framework. Use when working on the tinystruct codebase or any project built on tinystruct — including generating the bin/dispatcher and bin/dispatcher.cmd launcher scripts when a project lacks them, creating Application classes, @Action-mapped routes, unit tests, ActionRegistry, HTTP/CLI dual-mode handling, the built-in HTTP server, the event system, JSON with Builder/Builders, database persistence with AbstractData, POJO generation, Server-Sent Events (SSE), file uploads, and outbound HTTP networking.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-autonomous-loops`, `bosskuai-cybersecurity-risk`, `bosskuai-design-systems`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Principle.
2. Primary Development Tool: `bin/dispatcher`.
3. Run any @Action directly - the fastest way to verify a new action works.
4. (the class must be imported; see --import or default.import.applications in application.properties).
5. Start the HTTP server when you need the web-facing counterpart.
6. Import additional Application/MCP classes for the current run.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: read the Java release from `maven.compiler.release` in `pom.xml` or the Gradle `jvmToolchain`, and run `java -version` with `mvn -v` (or `./gradlew --version`). Check the latest stable Java release and its support dates at endoflife.date/java at work time, and use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 6 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Run any @Action directly - the fastest way to verify a new action works”, “Logging and Diagnostics” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Type traps: `@Action` parameters declared as numbers, booleans or dates (such as `int`, `long`, `boolean`, `Date`) are converted before the call. A value that cannot be converted throws an error. A bad boolean such as `yes` becomes `false` with no error, so check values and ranges yourself. Values read from `Request`, `Context` or `--key value` CLI options are always strings: parse and validate them before use.
- Concurrency: requests can overlap on the built-in server, so keep per-request data in local variables, not in static fields or shared application state.
- Zero downtime: a changed `@Action` path or response shape breaks clients that are still running, so keep the old route for one release, or version the new one.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
