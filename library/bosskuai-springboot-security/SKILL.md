---
name: bosskuai-springboot-security
description: "Use when the task explicitly concerns springboot security. Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring Boot services. Use when reviewing Spring Security authn/authz, validation, CSRF, secrets, headers, or rate limiting."
metadata:
  origin: ECC-adaptation
---

# Spring Boot Security Review — portable workflow

Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring Boot services. Use when reviewing Spring Security authn/authz, validation, CSRF, secrets, headers, or rate limiting.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-quarkus-security`, `bosskuai-springboot-patterns`, `bosskuai-django-security`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Authentication.
2. Authorization.
3. Input Validation.
4. SQL Injection Prevention.
5. Password Encoding.
6. CSRF Protection.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Spring Boot version in `pom.xml` or `build.gradle(.kts)`, and the Spring Security version the build resolves (`mvn dependency:tree` or `./gradlew dependencies --configuration runtimeClasspath`). Check the latest Spring Security release on spring.io at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Checklist Before Release” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Each endpoint has an explicit authorization rule, and a new route fails closed.
- Check that the caller owns the record on read, update and delete, not only that the caller has the role.
- Keep CSRF on for cookie-session apps. If it is off for a token API, document why.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
