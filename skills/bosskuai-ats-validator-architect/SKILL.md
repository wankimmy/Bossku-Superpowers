---
name: bosskuai-ats-validator-architect
description: "Use when checking if a resume or CV parses cleanly in applicant tracking systems: layout reading order, PDF text layer, keyword gaps against a job post, bullet impact scoring, and explainable, bias-aware scoring rules."
---

# BosskuAI ATS Validator Architect

Use this skill to audit a resume (or build a resume checker) so that machines can read it and people can see the fit. Every score must be explainable from a visible rule.

## How this differs from nearby skills

- **`bosskuai-search-relevance`**: ranking quality of a search engine. This skill borrows its BM25 and rank-fusion ideas only for keyword matching of one resume against one job post.
- **`odl-pdf`**: general PDF extraction (tables, OCR, bounding boxes). Use it to get the text out; use this skill to judge whether the extracted text is what a parser would see.
- **`bosskuai-regex-vs-llm-structured-text`**: choosing regex or an LLM for structured text. Here the rules are deterministic by design.
- **`bosskuai-legal-compliance`**: product-level legal readiness. Hiring-law questions go there and to a qualified human.

## Workflow

1. Text layer check: extract text from the real file. Fail if the PDF is image-only, or the text has replacement characters or Private Use Area codepoints (a sign of fonts without a Unicode map).
2. Layout check: confirm reading order is linear. Two-column or sidebar designs, tables, text boxes, and full-width rules across a gutter can interleave lines when parsers sort by vertical position. Prefer one column, or a layout whose content stream is sequential.
3. Section check: standard headings (Experience, Education, Skills, Projects), dates in one consistent format, plain contact block with working email and links.
4. Keyword check: tokenise resume and job post, drop stopwords per language, compare unigrams to trigrams, list matched terms and gaps. Match acronyms and expansions both ways (for example CI/CD and continuous integration).
5. Bullet check: each bullet should say what was done, the measurable result, and the method. Flag duty-style openers ("responsible for"), numbers with no business meaning, over-long bullets, and the same opening verb repeated. Do not count version numbers, ports, or standard names as results.
6. Score with a published formula. Choose pillar weights up front (keywords, impact, structure, density), write them in the report, and tie every deduction to one rule.
7. Report gaps and suggested rewrites, then stop. The owner decides what to change.

## Guardrails

- Never invent metrics, tools, employers, titles, or credentials. A missing item is a gap for the user to fill with true evidence.
- Do not recommend hidden text, tiny fonts, or keyword stuffing. Parsers and reviewers can detect them.
- Do not use proxy signals (name, address, graduation year, photo) in any score.
- Automated hiring tools are regulated in some places. This skill organises checks and evidence; it is not legal advice. Current law (for example EU AI Act high-risk rules, NYC Local Law 144 bias audits) needs authoritative sources and a qualified reviewer before any screening tool is used on real candidates.
- Vendor parser behaviour changes. Treat claims about a named ATS as unverified unless tested on that system.

## Output format

```text
File checked: [name, format, pages]
Text layer: [pass/fail, evidence]
Layout and sections: [findings]
Keyword gaps: [term, where in job post, true/false in resume]
Bullet findings: [bullet, rule broken, suggested rewrite using only user facts]
Score: [pillar weights, per-pillar score, rule behind each deduction]
Open questions for the user: [facts needed]
```

Adapted from agency-agents/engineering/engineering-ats-validator-architect.md (agency-agents, MIT).
