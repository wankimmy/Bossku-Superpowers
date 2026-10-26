---
name: bosskuai-legal-document-review
description: "Use when doing a first-pass review of a contract, lease or similar document for an attorney: summarise key terms, flag risk clauses and missing provisions, compare versions, and list next steps. Not legal advice."
---

# BosskuAI Legal Document First-Pass Review

Use this skill to prepare a document for a qualified lawyer: a structured summary, flagged clauses, missing terms, and a version comparison. Findings are flags for attorney review, not legal conclusions.

## How this differs from nearby skills

- **`bosskuai-legal-compliance`**: product-facing privacy, consent and policy readiness. This skill reads a specific agreement clause by clause.
- **`bosskuai-contract-first`**: API contracts (OpenAPI, schemas), not legal contracts.
- **`bosskuai-grounding`**: always on; every flag here must quote or cite the clause location.
- **`bosskuai-accounts-payable-agent`**: paying invoices; commercial terms in the underlying contract come here.

## Workflow

1. Intake: document type, parties, which party the user represents, date, governing law and jurisdiction, purpose of the review (initial, negotiation, due diligence, dispute), and any priorities or risk tolerance the attorney gave.
2. Map the structure: sections, exhibits, schedules, defined terms, cross-references. Note inconsistent definitions and broken references.
3. Summarise key terms without dropping material ones: term and renewal, payment, termination, liability cap, indemnification, IP ownership, confidentiality, dispute resolution, governing law.
4. Check for missing provisions and say so explicitly (limitation of liability, indemnity, dispute resolution, IP, data protection, insurance, force majeure). Silence is not neutrality.
5. Flag risky clauses. For each: location, exact language, why it matters for the user's party, how it differs from common practice, and a suggested question or revision for the attorney. Rate as high, medium or low.
6. Note where enforceability depends on jurisdiction (restrictive covenants, arbitration, auto-renewal, class waivers) and say current local law must be checked.
7. For a version comparison, list every change, including defined terms and small wording, classed as material, administrative, addition or deletion, with who it favours.
8. Finish with prioritised next steps for the reviewing attorney.

## Guardrails

- This skill organises documents and evidence and is not legal advice. Conclusions need current authoritative sources and review by a qualified lawyer.
- Do not state that a clause is enforceable or unenforceable; say it should be checked for the stated jurisdiction.
- No sending, signing, filing or negotiating on a real matter without explicit user approval.
- Treat documents as confidential; do not reuse their content outside the current task.
- Quote exact language and cite section and page; mark anything unclear as ambiguous.

## Output format

```text
Document: [type, parties, our party, date, jurisdiction, purpose]
Key terms: [term, payment, termination, liability cap, indemnity, IP, law]
Missing terms: [list]
Flags: [high/medium/low | section | quoted language | risk | question for attorney]
Changes (if comparing): [section | version A | version B | impact | favours]
Next steps: [ranked list for the attorney]
```

Adapted from agency-agents/specialized/legal-document-review.md (agency-agents, MIT).
