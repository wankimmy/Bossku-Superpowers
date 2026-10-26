---
name: bosskuai-visa-doc-translate
description: "Use when the task explicitly concerns visa doc translate. Translate visa document images (bank deposit, employment, income, and retirement certificates; HEIC, PNG, or JPG) into English via OCR and produce a bilingual PDF pairing the original image with a formatted certified-style translation. Use when a visa application needs a document translated to English, an official certificate OCR'd and translated, or a bilingual translation PDF for immigration paperwork."
metadata:
  origin: ECC-adaptation
---

# Instructions — portable workflow

Translate visa document images (bank deposit, employment, income, and retirement certificates; HEIC, PNG, or JPG) into English via OCR and produce a bilingual PDF pairing the original image with a formatted certified-style translation. Use when a visa application needs a document translated to English, an official certificate OCR'd and translated, or a bilingual translation PDF for immigration paperwork.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-video-style-application`, `bosskuai-fal-ai-media`, `bosskuai-nutrient-document-processing`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Technical Implementation.
2. OCR Methods (tried in order).
3. Required Python Libraries.
4. Important Guidelines.
5. Output Example.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 1 sidecar file. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.

## Done when

Complete the source “Output Example” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
