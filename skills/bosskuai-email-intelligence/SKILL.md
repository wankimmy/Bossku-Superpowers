---
name: bosskuai-email-intelligence
description: "Use when turning raw email threads into structured context for an AI agent: MIME parsing, thread reconstruction, quoted-reply dedup, participant-bound action items, hybrid retrieval with citations, and tenant isolation."
---

# BosskuAI Email Intelligence

Use this skill to build a pipeline that converts messy email into clean, attributable context that an agent can reason over without inventing who said what.

## How this differs from nearby skills

- **`bosskuai-email-ops`**: operating a mailbox (triage, drafts, follow-ups). This skill builds the data pipeline underneath.
- **`bosskuai-mailtrap-email-integration`**: sending transactional email. This skill is about reading and structuring inbound mail.
- **`bosskuai-rag-pipelines`**: general retrieval. This skill covers the email-specific parsing and thread problems before retrieval.
- **`bosskuai-data-pipelines`**: generic ETL. Email structure is the special case here.

## Workflow

1. Ingest raw messages with full MIME structure (IMAP, Gmail API, Microsoft Graph). Check each provider's current API docs for limits and fields.
2. Normalize: decode charsets, convert HTML to text keeping structure, list attachments and inline images.
3. Validate identity before building anything: each message needs a non-empty, unique Message-ID. Quarantine missing or duplicate IDs and cyclic In-Reply-To chains instead of overwriting a message.
4. Rebuild the thread as a graph from In-Reply-To and References, with subject-based fallback. Keep forks; do not flatten a thread into one document.
5. Strip quoted text per message (prefix `>` lines, "On ... wrote:" delimiters, Outlook quoting, nested forwards) and keep provenance. Quoting differs by client, so test on real samples from each provider.
6. Bind every participant to the message they sent (From header). First-person statements ("I will send it") are only meaningful with that binding; this is how action items stay on the right owner.
7. Extract participants, decisions, and action items with the source message ID. Treat "no objection" as a weak signal and mark it as implicit.
8. Chunk on message boundaries, never mid-message. Retrieve with a mix of semantic search, full text, and metadata filters (date, participant, attachment), fuse the ranks, and fit a token budget.
9. Return structured output with a citation (message ID, sender, date) for every claim.
10. Measure on a labelled set of threads: thread placement, attribution accuracy, retrieval relevance, and token reduction.

## Guardrails

- Keep tenant data strictly isolated; test that one tenant's queries never reach another's index.
- Redact PII as a pipeline stage, honour retention and deletion rules, and do not log raw email content in monitoring.
- Quoted text may be superseded; do not treat it as the current state.
- Email may contain legal, medical, or HR content; do not act on extracted items (send, file, pay) without the user's approval.

## Output format

```text
Thread: [id, message count, participants + roles]
Timeline: [date, sender, key point, message id]
Decisions: [text, explicit/implicit, source ids]
Action items: [task, owner, source id, date]
Open issues: [ambiguous identity, orphaned attachments]
```

Adapted from agency-agents/engineering/engineering-email-intelligence-engineer.md (agency-agents, MIT).
