---
name: bosskuai-quarkus-security
description: "Use when the task explicitly concerns quarkus security. Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation and custom validators, parameterized Panache queries, BCrypt password hashing, CORS and security headers, rate limiting, audit logging, Vault or environment-variable secrets, and dependency CVE scanning. Use when adding authentication or authorization, validating input, managing secrets, or hardening a Quarkus application."
metadata:
  origin: ECC-adaptation
---

# Quarkus Security Review — portable workflow

Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation and custom validators, parameterized Panache queries, BCrypt password hashing, CORS and security headers, rate limiting, audit logging, Vault or environment-variable secrets, and dependency CVE scanning. Use when adding authentication or authorization, validating input, managing secrets, or hardening a Quarkus application.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-springboot-security`, `bosskuai-cybersecurity-risk`, `bosskuai-django-verification`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Authentication.
2. JWT Authentication.
3. OIDC.
4. Custom Authentication Filter.
5. Authorization.
6. Role-Based Access Control.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: the Quarkus platform version in `pom.xml` or `gradle.properties`, and the security extensions the build resolves (`mvn dependency:tree` or `./gradlew dependencies --configuration runtimeClasspath`). Check the latest Quarkus release on quarkus.io and the OWASP guidance on owasp.org at work time. Use only APIs present in the installed version. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Apply the source “Authentication”, “JWT Authentication” guidance to the concrete request. Return the resulting quarkus security review artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

- A role check is not an ownership check. A test shows that user A cannot read or change user B's record.
- Every endpoint has an explicit rule (`@RolesAllowed` or a policy), and a test covers anonymous, wrong-role and other-tenant requests.
- Queries use Panache parameters, never string concatenation with user input.
- Full quality bar, with version and type checks: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
