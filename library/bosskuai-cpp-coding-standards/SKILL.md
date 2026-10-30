---
name: bosskuai-cpp-coding-standards
description: "Use when the task explicitly concerns cpp coding standards. C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and idiomatic practices."
metadata:
  origin: ECC-adaptation
---

# C++ Coding Standards (C++ Core Guidelines) — portable workflow

C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and idiomatic practices.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-rust-patterns`, `bosskuai-web-performance`, `python-patterns`, `error-handling`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Cross-Cutting Principles.
2. Philosophy & Interfaces (P.*, I.*).
3. Key Rules.
4. DO.
5. DON'T.
6. Functions (F.*).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: `g++ --version` or `clang++ --version` (or the MSVC version), `cmake --version`, and the standard set by `CMAKE_CXX_STANDARD` in `CMakeLists.txt` or `CMakePresets.json`. Check the latest compiler and CMake releases on gcc.gnu.org, clang.llvm.org and cmake.org at work time. Use only language features and APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Complete the source “Quick Reference Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Money uses a signed fixed-width integer, such as `std::int64_t`, in minor units (cents). Sizes and counts use `std::size_t`, the type of `sizeof` and the usual container `size_type`. Check sign and overflow, and build with `-Wall -Wextra -Wsign-conversion` so signed and unsigned comparisons and implicit conversions that change the sign show as warnings.
- Run AddressSanitizer and UBSan on the tests. With GCC or Clang, use `-fsanitize=address,undefined`. MSVC (`cl.exe`) supports only `/fsanitize=address`, so UBSan does not run there.
- Run threaded code under ThreadSanitizer in its own build. With GCC or Clang, use `-fsanitize=thread`. MSVC has no ThreadSanitizer.
- No `string_view` or `std::span` outlives the object it views, and no iterator is used after `insert` or `erase` changes its container.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
