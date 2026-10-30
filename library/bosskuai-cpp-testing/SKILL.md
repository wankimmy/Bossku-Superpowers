---
name: bosskuai-cpp-testing
description: "Use when the task explicitly concerns cpp testing. Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers."
metadata:
  origin: ECC-adaptation
---

# C++ Testing (Agent Skill) — portable workflow

Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-tdd-loop`, `e2e-testing`, `bosskuai-django-tdd`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Concepts.
2. TDD Workflow.
3. Basic Unit Test (gtest).
4. Fixture (gtest).
5. Mock (gmock).
6. CMake/CTest Quickstart.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: `cmake --version`, `g++ --version` or `clang++ --version`, and the GoogleTest version in `CMakeLists.txt` (`FetchContent_Declare`), `vcpkg.json` or `conanfile.txt`. Check the latest GoogleTest release on github.com/google/googletest and the CMake releases on cmake.org at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Run the affected GoogleTest/CTest target and retain the failing/passing test output.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Run the test target under the sanitizers the code needs: `-fsanitize=address,undefined`, and `-fsanitize=thread` in its own build for threaded code. These flags are for GCC and Clang. MSVC supports only `/fsanitize=address`, on x86 and x64. Skip the thread build on Windows: MSVC has no ThreadSanitizer, and Clang's ThreadSanitizer docs do not list Windows. Keep that output.
- A new test runs against the old code first and fails there. Keep both results.
- Test money and sizes with the production integer types and scale, not `double` literals.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
