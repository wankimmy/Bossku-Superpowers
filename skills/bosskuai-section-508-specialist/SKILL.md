---
name: bosskuai-section-508-specialist
description: "Use when auditing or remediating accessibility for a US federal or public-sector site: Section 508 versus WCAG and ADA Title II targets, assistive-technology testing, ARIA widgets, accessible forms and PDFs, and VPAT or ACR reports."
---

# BosskuAI Section 508 Specialist

Use this skill when a government or contract-driven site must demonstrably meet an accessibility standard, and a clean automated scan is not enough.

## How this differs from nearby skills

- **`accessibility`**: designing and implementing accessible UI to WCAG 2.2 AA across platforms. This skill adds the US legal framing, assistive-technology test matrix, and VPAT or ACR reporting.
- **`bosskuai-ui-ux-design-to-code`**: turning designs into UI; run an accessibility pass separately.
- **`bosskuai-legal-compliance`**: product legal readiness in general, not accessibility conformance documents.
- **`bosskuai-qa-automation-strategy`**: test strategy; here CI accessibility checks are one regression gate.

## Workflow

1. Confirm which standard applies and why, from current official sources: Section 508 incorporates a specific WCAG version by reference, which can differ from the level required under ADA Title II or a contract, and from best-practice targets. Do not overstate what any one law requires.
2. Define the test matrix: representative pages, critical task flows, document types, and screen reader and browser pairings.
3. Run automated scans (axe, WAVE, Lighthouse) as a first pass only. They find a subset of failures.
4. Test by keyboard alone: order, visible focus, no traps, every control operable.
5. Test with screen readers (for example NVDA, JAWS, VoiceOver) on the real flows, including modals, dynamic updates and error handling.
6. Check perception: contrast (normal text 4.5:1, large text and UI components 3:1), zoom and reflow, text spacing, and meaning not carried by colour alone.
7. Remediate at the source. Native HTML first; ARIA only when no native element works, following the ARIA Authoring Practices pattern completely (roles, states, keyboard).
8. Forms: every control has a programmatic label (placeholder is not a label), instructions are linked, errors are identified in text and announced.
9. Media and documents: text alternatives, captions or transcripts, tagged PDFs with reading order, titles and language.
10. Write the VPAT or ACR honestly: each "Supports" must be backed by testing; use "Partially Supports" with a remediation plan where needed.
11. Add regression prevention: CI checks, accessible component patterns, PR checklist, scheduled re-evaluation.

## Guardrails

- Do not accept an overlay widget as remediation; fix the HTML, CSS and ARIA.
- Never claim conformance from a scan alone.
- This skill organises an audit. Legal applicability and conformance claims need current authoritative sources and a qualified human reviewer, and no ACR or VPAT is published or sent to a customer or agency without explicit user approval.

## Output format

```text
Standard applied: [which, why, source checked]
Scope and methods: [pages, flows, tools, assistive technology]
Findings: [id, criterion, severity, location, user barrier, found by, fix]
Remediation plan: [priority, owner, retest method]
Conformance summary: [per criterion level with remarks]
```

Adapted from agency-agents/engineering/engineering-section-508-specialist.md (agency-agents, MIT).
