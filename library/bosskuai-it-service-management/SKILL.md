---
name: bosskuai-it-service-management
description: "Use when setting up or fixing ITIL-style IT service management: service catalog, incident priority matrix, problem records, change types and CAB, SLA reporting, CMDB upkeep, and a continual-improvement register."
---

# BosskuAI IT Service Management

Use this skill to design or repair the process layer that makes IT predictable: how requests, incidents, problems, and changes are recorded, prioritised, and reviewed. Targets below are examples to set with the business, not standards.

## How this differs from nearby skills

- **`bosskuai-incident-response`**: running an active incident and the blameless postmortem. This skill designs the wider process (catalog, change, SLA, CMDB) around it.
- **`bosskuai-observability-sre`**: instrumentation, SLOs, and alerts. SLA wording and reporting here can consume those signals.
- **`bosskuai-change-management-consultant`**: the people side of organisational change (ADKAR, resistance). Here "change" means controlled technical changes (RFCs).
- **`bosskuai-customer-success-support`**: customer-facing SaaS support. This skill is internal IT service delivery.
- **`bosskuai-ci-cd-pipelines`**: automated release mechanics that standard changes can use.

## Workflow

1. Service catalog: for each service record a plain-language name and description, owner, users, support hours, dependencies, service levels (availability, recovery time and point objectives, response and resolution), how to request it, approvals, and the next review date.
2. Incident priority: derive priority from impact and urgency using a matrix, then write for each level the response target, resolution target, escalation, and update interval. Priority follows business impact, not who is calling.
3. Major incidents: separate the incident commander (communication, coordination) from the technical resolvers. Use a fixed update template: status, what is affected, what is known, actions underway, next update time.
4. Problem management: open a problem record for major incidents and for recurring patterns (set a threshold, for example the same symptom several times in a month). Capture the workaround in a known-error record, use a root-cause method (five whys, cause-and-effect diagram), and track the permanent fix.
5. Change control: define standard (pre-approved, low risk), normal (review and approval; major ones go to the change advisory board), and emergency (fast approval, retrospective review). Each request states justification, scope, risk, implementation plan, backout plan, test plan, window, and approvals.
6. Risk score = impact x probability on agreed scales; set bands with the business. Review outcomes after major changes and consider promoting repeatable ones to standard.
7. SLA management: measure continuously, report honestly, exclude only agreed items (scheduled maintenance), investigate every breach, and report root cause and remediation.
8. CMDB: required attributes per item type, discovery as the primary source, scheduled audits, and updates driven by approved changes. Track coverage and accuracy.
9. Continual improvement register: each item has an owner, baseline, target, date, and result.

## Guardrails

- Do not push changes to production, close tickets, or alter live ITSM tooling without explicit approval.
- Do not alter SLA data to look better; breaches reported late are worse than breaches reported.
- Framework names and certifications (ITIL 4, ISO/IEC 20000) have licensed material; use the official current documents rather than recalling clauses.
- Tool features differ by product and version; check the installed platform docs.

## Output format

```text
Scope: [org size, tooling, current pain]
Catalog entry or process change: [..]
Priority and escalation table: [..]
Change types and approval path: [..]
SLA and CMDB metrics to track: [definition, source]
CSI items: [id, owner, baseline, target, date]
```

Adapted from agency-agents/engineering/engineering-it-service-manager.md (agency-agents, MIT).
