---
name: bosskuai-quarkus-verification
description: "Use when the task explicitly concerns quarkus verification. Verification loop for Quarkus projects: build, static analysis (Checkstyle, PMD, SpotBugs), tests with JaCoCo coverage, OWASP dependency and container security scans, GraalVM native compilation, health checks, and config validation. Use when verifying a Quarkus service before a PR, after major refactoring or dependency upgrades, or pre-deploy."
metadata:
  origin: ECC-adaptation
---

# Quarkus Verification Loop — portable workflow

Verification loop for Quarkus projects: build, static analysis (Checkstyle, PMD, SpotBugs), tests with JaCoCo coverage, OWASP dependency and container security scans, GraalVM native compilation, health checks, and config validation. Use when verifying a Quarkus service before a PR, after major refactoring or dependency upgrades, or pre-deploy.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-springboot-verification`, `bosskuai-laravel-verification`, `verification-before-completion`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Phase 1: Build.
2. Maven.
3. Gradle.
4. Phase 2: Static Analysis.
5. Checkstyle, PMD, SpotBugs (Maven).
6. SonarQube (if configured).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Maven or Gradle wrapper version in `.mvn/wrapper/maven-wrapper.properties` or `gradle/wrapper/gradle-wrapper.properties`, the Quarkus platform version in `pom.xml` or `gradle.properties`, and the GraalVM version (`native-image --version`) if native builds are in scope. Check the latest Quarkus release on quarkus.io and GraalVM on graalvm.org at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Quarkus Verification Loop”, “Verification Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- Run the build and tests on the versions the project targets. If native is in scope, the native build runs too, since a JVM pass does not prove a native image works.
- Every `quarkus.*` setting the production profile needs exists in production config or the environment before the code reads it.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
