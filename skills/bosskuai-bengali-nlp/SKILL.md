---
name: bosskuai-bengali-nlp
description: "Use when the task explicitly concerns bengali nlp. Bengali (Bangla) text processing patterns including Unicode normalization, script detection, tokenization, conjunct handling, and Bangla-specific NLP best practices for AI applications."
metadata:
  origin: ECC-adaptation
---

# Bengali (Bangla) NLP Patterns — portable workflow

Bengali (Bangla) text processing patterns including Unicode normalization, script detection, tokenization, conjunct handling, and Bangla-specific NLP best practices for AI applications.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-rust-patterns`, `bosskuai-dotnet-patterns`, `bosskuai-github-workflow`, `bosskuai-prompt-optimizer`, `bosskuai-regex-vs-llm-structured-text`, `database-migrations`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Bengali Unicode and Script Handling.
2. Unicode Range.
3. Normalization.
4. NFC composes characters: base + combining marks -> precomposed.
5. Conjunct Consonants (যুক্তবর্ণ).
6. "ক্ষ" is 1 grapheme but 3 code points (ক + ্ + ষ).

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Bengali Unicode and Script Handling”, “Unicode Range” guidance to the concrete request. Return the resulting bengali (bangla) nlp patterns artifact or diagnosis with source/command evidence for each conclusion.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
