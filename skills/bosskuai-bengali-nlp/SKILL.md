---
name: bosskuai-bengali-nlp
description: "Use when the task explicitly concerns bengali nlp. Bengali (Bangla) text processing patterns including Unicode normalization, script detection, tokenization, conjunct handling, and Bangla-specific NLP best practices for AI applications."
metadata:
  origin: ECC-adaptation
---

# Bengali (Bangla) NLP Patterns — portable workflow

## Job and activation

Bengali (Bangla) text processing patterns including Unicode normalization, script detection, tokenization, conjunct handling, and Bangla-specific NLP best practices for AI applications.

Use this skill for that specific domain, framework, data source or artifact. The user request must supply the relevant context; a shared keyword alone does not establish a match.

Nearby owners: `bosskuai-rust-patterns`, `bosskuai-dotnet-patterns`, `bosskuai-github-workflow`. Select them only for their separate concerns; do not load multiple general workflows for the same job.

## Source workflow

Read [the complete source workflow](references/upstream/SKILL.md) before applying its examples. Work through the following source sections in order:

1. Bengali Unicode and Script Handling.
2. Unicode Range.
3. Normalization.
4. NFC composes characters: base + combining marks -> precomposed.
5. Conjunct Consonants (যুক্তবর্ণ).
6. "ক্ষ" is 1 grapheme but 3 code points (ক + ্ + ষ).

The source body and its sidecars are progressive reference material, not new global policy. Resolve its relative `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names resolve through [the source map](SOURCE.json); use the current host skill loader or `bossku skills show <mapped-id>`. Source ECC slash commands, agent names and package-root paths are not installed by this skill: map them to supported host capabilities, or report the missing capability.

Related supported owners: `bosskuai-dotnet-patterns`, `bosskuai-github-workflow`, `bosskuai-prompt-optimizer`, `bosskuai-regex-vs-llm-structured-text`, `bosskuai-rust-patterns`, `database-migrations`.

## Prerequisites and execution boundary

Inspect the project/tool versions and the source prerequisites first. Use repository scripts and installed dependencies where present. A documented command is an example to inspect, not permission to install packages, add an account, expose secrets, upload private content or mutate an external service. Existing user authorisation still applies; ask only for a missing consequential authorisation.

## Pass signal

Apply the source “Bengali Unicode and Script Handling”, “Unicode Range” guidance to the concrete request. Return the resulting bengali (bangla) nlp patterns artifact or diagnosis with source/command evidence for each conclusion.

## Stop conditions

Stop the affected operation when an input/contract is missing, a provider/runtime is unavailable, source instructions reference unsupported commands, or a requested mutation lacks authorisation. Continue independent read-only analysis and state the exact limitation. Do not claim completion from a generated plan alone.

## Attribution

Adapted from the locally reviewed `affaan-m/ECC` snapshot; provenance and content hashes are in [SOURCE.json](SOURCE.json). The complete original text/resources remain in [references/upstream/](references/upstream/SKILL.md), under the retained [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
