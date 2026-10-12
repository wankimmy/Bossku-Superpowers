---
name: bosskuai-malaysia-pdpa-privacy
description: "Use when doing a Malaysia PDPA-aware privacy review: data minimization, consent, retention, user rights, vendor processors, and privacy-safe SaaS operations."
---

# BosskuAI Malaysia PDPA Privacy

Use this skill for **product and engineering privacy posture** on Malaysian personal data. This is product guidance, not legal advice; a lawyer signs off on obligations.

## How this differs from nearby skills

- **`bosskuai-legal-compliance`**: broader compliance and policy alignment; this skill is PDPA-specific and implementation-facing.
- **`bosskuai-cybersecurity-risk`**: protects data from attackers; this skill governs what is collected and kept in the first place.
- **`bosskuai-data-architecture`**: designs storage and pipelines; this skill constrains what may flow through them.

## The PDPA principles, as engineering requirements

Malaysia's PDPA is built on principles that map to concrete product decisions:

- **General/consent**: processing needs a lawful basis and a clear notice. Consent must be recorded, not assumed.
- **Notice and choice**: tell users what is collected, why, who receives it, and how to reach you, in both English and Bahasa Malaysia where users expect it.
- **Disclosure**: do not share beyond the stated purpose without consent.
- **Security**: protect against loss, misuse, and unauthorized access.
- **Retention**: do not keep personal data longer than the purpose requires.
- **Data integrity**: keep it accurate and current.
- **Access**: users can access and correct their data.

Amendment duties in force since 1 June 2025 (PDPA (Amendment) Act 2024): notify the Personal Data Protection Commissioner within 72 hours of becoming aware of a personal data breach, and affected individuals within 7 days where significant harm is likely; appoint a Data Protection Officer and register them with the Commissioner where processing is large-scale; honour data portability requests. Thresholds and forms come from the Commissioner's guidelines: confirm them with counsel.

## Design decisions this drives

- **Minimize at the form**: the cheapest privacy control is not collecting the field. Challenge every optional field, especially IC number, full address, and date of birth.
- **Sensitive data**: health, biometric, religion, political opinion, and similar categories carry stricter conditions. Avoid storing them unless the product genuinely requires it.
- **Retention schedule**: define per data type, with an actual deletion job, not an intention.
- **Access, correction, export, deletion**: build the workflow before scale makes it manual and painful.
- **Processors and vendors**: every third party receiving personal data (analytics, support, email, AI APIs) needs a purpose and an agreement. Sending customer records to an external model API is a disclosure.
- **Cross-border transfer**: know where data physically lands, including your hosting region and each vendor's.
- **Breach readiness**: a tested runbook that meets the 72-hour Commissioner deadline: who assesses harm, who notifies, and what evidence is kept.

## Enforcement checks

- **Find it first**: build the data map across every store, including logs, error traces, caches, queues, search indexes, analytics streams and backups. Free-text fields drift into holding personal data; re-scan on a schedule.
- **Consent gates the write**: a stored opt-out that the analytics or marketing pipeline never reads is not consent. Check at the point of write or use, per purpose.
- **Deletion needs proof**: the request must reach every primary, replica, warehouse, index, cache and vendor, and leave an auditable record. A delete that clears one table is a false promise.
- **Anonymization is tested**: postcode plus birth date plus gender can still re-identify. Aggregate or generalize, then test re-identification risk before calling data anonymous.
- **Review at design time**: check data flows in the design doc, not after an incident. A new vendor, region or purpose needs a basis and a data-map entry.

## Guardrails

- Do not present this as legal advice or claim compliance certainty. Flag where counsel is needed.
- Do not log personal data into application logs, error trackers, or analytics events.
- Do not use production personal data in development, testing, or model prompts.
- Deletion means deletion, including backups policy, search indexes, caches, and vendor copies.
- Anonymization must actually prevent re-identification; a hashed IC number is still identifying.

## Output format

```text
Personal data inventory:
  [field] - [purpose] - [lawful basis] - [retention] - [where stored]

Sensitive data: [any, and justification]
Vendors/processors: [vendor - data shared - region]

Findings:
  P0/P1/P2 - [issue] - [principle affected] - [fix]

User rights workflow: [access / correct / export / delete - built or missing]
Retention enforcement: [job or process that actually deletes]
Needs legal review: [items]
DPO: [appointed and registered / not required, why]
Breach path: [owner, last 72h drill]
```

## References

- `../../references/checklists/malaysia-pdpa-privacy-checklist.md`

Adapted from engineering/engineering-privacy-engineer.md (agency-agents, MIT).
