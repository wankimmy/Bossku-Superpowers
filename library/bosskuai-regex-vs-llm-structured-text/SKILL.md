---
name: bosskuai-regex-vs-llm-structured-text
description: "Use when the task explicitly concerns regex vs llm structured text. Decision framework for parsing structured text (quizzes, forms, invoices, receipts, tables) with a hybrid regex-first pipeline — regex extraction handles 95%+ cheaply, a confidence scorer flags low-confidence items, and an LLM validator fixes only the edge cases. Use when choosing between regex and LLM for text extraction, building a cheap document parser, or optimizing extraction cost and accuracy."
metadata:
  origin: ECC-adaptation
---

# Regex vs LLM for Structured Text Parsing — portable workflow

Decision framework for parsing structured text (quizzes, forms, invoices, receipts, tables) with a hybrid regex-first pipeline — regex extraction handles 95%+ cheaply, a confidence scorer flags low-confidence items, and an LLM validator fixes only the edge cases. Use when choosing between regex and LLM for text extraction, building a cheap document parser, or optimizing extraction cost and accuracy.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-agent-architecture-audit`, `bosskuai-agent-benchmark-comparison`, `bosskuai-product-strategy`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Decision Framework.
2. Architecture Pattern.
3. Implementation.
4. 1. Regex Parser (Handles the Majority).
5. 2. Confidence Scoring.
6. 3. LLM Validator (Edge Cases Only).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the language and LLM SDK versions in the lockfile or manifest, and the provider's current model deprecation notes, both checked live at work time, and the source prerequisites first. Pin the exact model version in config, since an alias can change. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Decision Framework”, “Architecture Pattern” guidance to the concrete request. Return the resulting regex vs llm for structured text parsing artifact or diagnosis with source/command evidence for each conclusion.

- Test each regex on long inputs with near-misses and nested repeats, and time it. Some patterns take exponential time on certain input (ReDoS).
- Run the regex path on a production data copy, not clean fixtures. For the LLM path, mask a sample from that copy locally, keeping each field's format, and send it to the provider only after the user approves it. Check dates (`01/02/2026` can mean either month first), decimal and thousands separators, and money (integer cents or a decimal string).
- Validate every LLM answer against a JSON schema. Reject missing or wrong-typed fields, and never coerce them silently.
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
