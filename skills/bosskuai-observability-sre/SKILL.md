---
name: bosskuai-observability-sre
description: Use when adding logs, metrics, tracing, alerts, SLOs, health checks, dashboards, incident detection, or production reliability instrumentation.
---

# BosskuAI Observability & SRE

Use this skill when the question is **whether production failure would be noticed**, and how fast.

## How this differs from nearby skills

- **`bosskuai-incident-response`**: runs an incident already in progress; this skill builds the detection that starts it.
- **`bosskuai-performance-profiling`**: diagnoses a known slow path; this skill tells you which path is slow in production.
- **`bosskuai-devops-iac`**: builds the deployment pipeline; this skill instruments what the pipeline ships.

## Start from user impact, not dashboards

Define the SLI first: the measurable thing a user experiences (request success rate, checkout latency, job completion time). Dashboards and alerts derive from it. A dashboard built before an SLI measures whatever was easy to collect.

## Instrument for correlation

Every log line for a request or job should carry enough identity to reconstruct a story:

- Request id, propagated across services and into background jobs.
- Tenant/org id and user id where privacy allows.
- Job id and attempt number for queued work.
- Domain ids that matter for recovery: payment, invoice, refund, webhook event.
- Trace/span id when distributed tracing exists.
- The release (version on metrics; version or git SHA on logs and traces), so a bad deploy shows up as its own number during a rolling deploy or canary.
- The SDK and collector you ship (OpenTelemetry or the vendor's agent): check the latest stable release live, and confirm each API you call exists in the version you run.

## Alert on symptoms, not causes

Alert when users are affected: error rate, latency percentile breach, queue age growth, failed payment or webhook spikes, drop in a core business event (invoices issued, payments received, webhooks processed). Cause-based alerts (CPU, memory) belong on dashboards unless they directly predict user pain. Every alert needs an owner and a runbook link, or it trains people to ignore alerts.

Page on SLO burn rate over a fast and a slow window rather than raw thresholds; propagate trace context through queue headers and job payloads so one request can be followed into its jobs. Alert on missing data too: a stopped exporter or a dead log shipper looks like zero errors unless an alert fires when the series disappears. A flow that quietly stops throws no errors.

## Health checks

Separate **liveness** (is the process up) from **readiness** (can it serve). Readiness should check the dependencies the app truly needs: database, cache, queue, storage, and critical external services. A readiness check that always returns 200 is worse than none. Readiness must not flap on one slow dependency: use a short timeout and several failures in a row. A blip that takes every instance out of rotation is an outage you caused.

## Guardrails

- Never log secrets, tokens, full card data, passwords, or unredacted personal data.
- Watch cardinality: unbounded label values on metrics get expensive fast.
- Sample high-volume traces, but never sample away errors.
- Do not add an alert without defining the response to it.
- Retention and sampling are cost decisions; state them explicitly rather than defaulting.
- Test every new alert: cause the failure in staging and confirm it reaches a person. An alert that has never fired is untested.

## Output format

```text
User-impacting SLI: [what it measures]
SLO (if set): [target and window]

Current coverage:
  Logs: [what exists, what is missing]
  Metrics: [what exists, what is missing]
  Traces: [what exists, what is missing]
  Health checks: [liveness / readiness state]

Gaps:
  P0/P1/P2 - [blind spot] - [what would go unnoticed] - [instrumentation to add]

Alerts: [signal - threshold - owner - runbook]
Cost note: [retention / cardinality / sampling implications]
Verification: [how the signal was confirmed to fire]
```

## References

- `../../references/checklists/observability-sre-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`
