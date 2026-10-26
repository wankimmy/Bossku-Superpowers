---
name: bosskuai-salesforce-architect
description: "Use when designing or reviewing a Salesforce org: data model, governor-limit budget, bulkified Apex and triggers, Flow vs code, integration patterns (Platform Events vs CDC), CI/CD, and ADRs."
---

# BosskuAI Salesforce Architect

Use this skill to design or review Salesforce solutions so they stay inside platform limits, tolerate bulk data, and fail safely when integrations fail.

## How this differs from nearby skills

- **`bosskuai-software-architecture`**: general module and layering decisions. This skill covers Salesforce-specific limits and patterns.
- **`bosskuai-api-design`**: REST/GraphQL/event contracts. Use it for the contract of an integration; use this skill for how Salesforce sends and receives it.
- **`architecture-decision-records`**: the ADR format and storage. This skill provides Salesforce-flavored content for them.
- **`bosskuai-data-architecture`**: cross-system modeling and ownership.
- **`revops`**: CRM process and lead lifecycle. This skill is the technical build.

## Workflow

1. Org assessment: objects and volumes, automations (Flows, triggers, legacy rules), integrations, known limit hot spots, technical debt. Use the platform's limits tooling to observe actual use.
2. Data model first: relationship types (master-detail vs lookup) with reasons, record types, sharing model, large-volume strategy, external IDs for integration objects, field-level security, justified polymorphic lookups.
3. Automation layering: declarative tools first (Flow, formulas, validation) and code when logic needs bulk handling or clear tests. One trigger per object that delegates to handler classes; no business logic in the trigger body. Avoid overlapping automation on one object.
4. Governor-limit budget: for each transaction list queries, DML, CPU, heap, callouts, and async calls used and remaining. Design every code path to work on a batch of records (the platform processes records in chunks), with no query or DML inside loops. Take current numeric limits from Salesforce's documentation for the release in use.
5. Integration pattern per system: sync versus async, push versus pull, platform events versus change data capture (custom business events versus data-change sync), middleware, auth, retry with backoff, dead-letter handling, rate limits, idempotency keys.
6. Security: CRUD and field-level checks, query injection prevention, encryption for sensitive fields, data residency needs.
7. Delivery: source-tracked metadata, scratch orgs or sandboxes by purpose, automated tests and deploy pipeline, destructive-change handling, rollback plan.
8. Record each significant decision as an ADR with alternatives and the limits it affects.

## Guardrails

- Platform limits, feature availability (GA vs beta), and license-dependent features change by release. Check the current release notes and documentation before committing a design.
- Do not deploy to, or change data in, a production org without explicit user approval and a tested rollback.
- Do not store sensitive personal data in unencrypted custom fields.
- Do not design callouts without failure handling.

## Output format

```text
Context: [clouds, volumes, integrations]
Data model decisions: [object / relationship - reason]
Automation layering: [what runs in Flow vs Apex, ordering]
Limit budget: [limit - used - remaining, per transaction]
Integration table: [system - pattern - failure handling]
ADRs: [title - status - review date]
Delivery and rollback: [pipeline, tests, undo]
```

Adapted from agency-agents/specialized/specialized-salesforce-architect.md (agency-agents, MIT).
