---
name: bosskuai-kubernetes-patterns
description: "Use when the task explicitly concerns kubernetes patterns. Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Secret handling, and kubectl debugging for production-grade deployments. Use when writing or reviewing Kubernetes manifests, or debugging probes, RBAC, autoscaling, or resource limits."
metadata:
  origin: ECC-adaptation
---

# Kubernetes Patterns — portable workflow

Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Secret handling, and kubectl debugging for production-grade deployments. Use when writing or reviewing Kubernetes manifests, or debugging probes, RBAC, autoscaling, or resource limits.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-dart-flutter-patterns`, `bosskuai-api-design`, `bosskuai-django-patterns`, `bosskuai-cybersecurity-risk`, `bosskuai-devops-iac`, `bosskuai-docker`, `bosskuai-github-workflow`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. How It Works.
2. Core Workload Patterns.
3. Deployment — Production Template.
4. Probes — Liveness, Readiness, Startup.
5. Correct pattern: startupProbe covers slow startup,.
6. then liveness/readiness take over.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first: run `kubectl version` for the client and server versions, and `kubectl api-resources` to see which API versions the cluster serves. Check the latest Kubernetes release and its patch and support dates at kubernetes.io/releases at work time, and use only APIs present in the installed version. Check the version skew policy on kubernetes.io before you change the client or the cluster. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Diagnosing Common Errors”, “Best Practices Checklist” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

- Type traps: quote every value that must be a string (environment values such as `"8080"`). Write `defaultMode` in decimal (420 for 0644), because YAML parsers disagree on leading zeros.
- Concurrency: two replicas or two jobs on one row need a lock, a unique key or an idempotent write. Set `concurrencyPolicy: Forbid` on a CronJob that must not overlap.
- Zero downtime: set a readiness probe, `maxUnavailable` and `maxSurge`, a PodDisruptionBudget, and a graceful shutdown (`preStop` and `terminationGracePeriodSeconds`). Check with `kubectl rollout status`. If a rollout fails, check that the previous version can read the current schema and the data written since the deploy (quality bar section 6). Then ask the user before you run `kubectl rollout undo`.
- Full quality bar: `../../references/checklists/engineering-quality-bar.md`.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
