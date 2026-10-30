---
name: bosskuai-csharp-testing
description: "Use when the task explicitly concerns csharp testing. C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. Use when writing or reviewing xUnit tests, mocks, or integration tests in a C# / .NET project."
metadata:
  origin: ECC-adaptation
---

# C# Testing Patterns — portable workflow

C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. Use when writing or reviewing xUnit tests, mocks, or integration tests in a C# / .NET project.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-fsharp-testing`, `bosskuai-fastapi-development`, `bosskuai-go-development`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Test Framework Stack.
2. Unit Test Structure.
3. Arrange-Act-Assert.
4. Parameterized Tests with Theory.
5. Mocking with NSubstitute.
6. ASP.NET Core Integration Tests.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: `dotnet --info`, the SDK in `global.json`, `<TargetFramework>` in the test project, and the xUnit, NSubstitute and `Microsoft.AspNetCore.Mvc.Testing` versions in `Directory.Packages.props` or the `.csproj`. Run `dotnet list package --outdated` and `dotnet list package --vulnerable`. Check the latest releases on nuget.org and xunit.net at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Test Framework Stack”, “Unit Test Structure” guidance to the concrete request. Return the resulting c# testing patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Integration tests use the production database engine and version through Testcontainers. EF Core's in-memory provider is not a relational database and ignores transactions, so it is not a stand-in. Where the step 6 example uses UseInMemoryDatabase, replace it with a Testcontainers database of the production engine and version.
- Code that reads time takes a `TimeProvider`, not `DateTime.Now`, so tests can fix the time.
- Money assertions use `decimal` at the production scale, and one JSON test sends a quoted number.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
