---
name: bosskuai-platform-engineering
description: "Use when building an internal developer platform: golden paths, service scaffolding templates, self-serve CLI or portal, a paved-road catalog, adoption tracking and deprecation or migration of old paths."
---

# BosskuAI Platform Engineering

Use this skill when product teams keep filing tickets or hand-building infrastructure, and you want opinionated, self-serve paths that are easier than the alternative.

## How this differs from nearby skills

- **`bosskuai-devops-iac`**: infrastructure as code, environments and release strategy. This skill is about the developer-facing product built on top.
- **`bosskuai-ci-cd-pipelines`**: pipeline YAML and stages; a golden path usually includes a pipeline but is broader.
- **`bosskuai-kubernetes-patterns`**: workload patterns a golden path may encode.
- **`bosskuai-software-architecture`** and **`architecture-decision-records`**: general design and decision records; here ADRs record why a default was chosen.

## Principles

- Treat the platform as a product with users (engineers), a roadmap and adoption measures.
- The recommended way is the default and the easiest way. Customisation is opt-in, with an escape hatch for power users.
- Pick one framework per golden path and document the trade-off, instead of offering many choices.
- A feature nobody uses is cost without value. Measure adoption before calling it shipped.

## Workflow

1. Discover: interview a handful of teams about friction, mine platform-request tickets, and list the manual workflows people repeat ("dirt roads").
2. Rank candidates by frequency, time cost and strategic value.
3. For the top candidate, write a golden path spec: parameters with validation, opinionated defaults, outputs (repo, pipeline, namespace, dashboards, on-call service). Form and YAML inputs can arrive as text, and an empty string is not a missing value, so validate every parameter before the scaffold runs.
4. Record defaults and trade-offs in an ADR.
5. Build the self-serve entry: a CLI command or portal template, with clear errors and a diagnose command. Two people can run the same scaffold at once, so make creation idempotent: check and create in one atomic step, and never overwrite an existing service.
6. Register services in a catalog with owner, on-call, runbook and dependencies.
7. Pilot with two or three friendly teams, iterate, then launch with a short doc explaining why and how.
8. Track adoption, time to first deploy, and delivery measures (deployment frequency, lead time, change failure rate, recovery time). Talk to non-adopters when adoption is low and fix friction before adding features.
9. Retire or rebuild paths nobody uses. Migrate old paths with tooling and a stated deprecation window; never break a paved road silently. Keep the old and new paths working side by side until adoption is done.

## Guardrails

- Version the abstractions. Breaking a paved road affects every team on it.
- Do not ban dirt roads; make the paved road better.
- Set numeric targets from your own baseline, not from other organisations.
- Read each tool's current version from the project's manifest, lockfile or runtime, using the command in the version table of ../../references/checklists/engineering-quality-bar.md (for example `go version` or `java -version`). Check the latest stable release on the tool's official site at work time, and use only APIs present in the installed version.

## Output format

```text
Friction found: [workflow, frequency, cost]
Golden path spec: [parameters, defaults, outputs]
Entry point: [CLI or portal, escape hatch]
ADR: [decision, trade-off]
Adoption plan: [pilot teams, launch, metrics, review date]
Migration or retirement: [path, window, tooling]
```

Adapted from agency-agents/engineering/engineering-platform-engineer.md (agency-agents, MIT).
