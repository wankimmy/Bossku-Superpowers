---
name: bosskuai-fsharp-testing
description: "Use when the task explicitly concerns fsharp testing. F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integration tests, and test organization best practices. Use when writing F# tests with xUnit, FsUnit, Unquote, or FsCheck."
metadata:
  origin: ECC-adaptation
---

# F# Testing Patterns — portable workflow

F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integration tests, and test organization best practices. Use when writing F# tests with xUnit, FsUnit, Unquote, or FsCheck.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-csharp-testing`, `bosskuai-kotlin-testing`, `bosskuai-go-development`, `bosskuai-dotnet-patterns`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Test Framework Stack.
2. Unit Tests with xUnit + FsUnit.
3. Basic Test Structure.
4. Assertions with Unquote.
5. Async Tests.
6. Parameterized Tests with Theory.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: `dotnet --info`, the SDK in `global.json`, `<TargetFramework>` in the test `.fsproj`, and the xUnit, FsUnit, Unquote and FsCheck versions in the `.fsproj` or `Directory.Packages.props`. Run `dotnet list package --outdated` and `dotnet list package --vulnerable`. Check the latest releases on nuget.org at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Test Framework Stack”, “Unit Tests with xUnit + FsUnit” guidance to the concrete request. Return the resulting f# testing patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Money literals need the `m` suffix (`0.01m`), since `0.01` is a float.
- Run and await every async block. One that is never started passes silently.
- FsCheck generators produce the shapes production sends: empty lists, `null` from .NET APIs, and the real decimal scale.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
