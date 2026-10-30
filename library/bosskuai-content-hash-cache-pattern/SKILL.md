---
name: bosskuai-content-hash-cache-pattern
description: "Use when the task explicitly concerns content hash cache pattern. Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation. Use when repeated file processing is slow and results should be cached and invalidated by content rather than path."
metadata:
  origin: ECC-adaptation
---

# Content-Hash File Cache Pattern — portable workflow

Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation. Use when repeated file processing is slow and results should be cached and invalidated by content rather than path.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-subagent-delegation`, `bosskuai-swift-actor-persistence`, `bosskuai-agent-benchmark-comparison`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Core Pattern.
2. 1. Content-Hash Based Cache Key.
3. 2. Frozen Dataclass for Cache Entry.
4. 3. File-Based Cache Storage.
5. 4. Service Layer Wrapper (SRP).
6. Key Design Decisions.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the language runtime and hash library versions in the lockfile or manifest, and the hash API for that version, each against its latest stable release, checked live at work time, and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.

## Done when

Apply the source “Core Pattern”, “1. Content-Hash Based Cache Key” guidance to the concrete request. Return the resulting content-hash file cache pattern artifact or diagnosis with source/command evidence for each conclusion.

- Hash the raw bytes, as the source code does. A CRLF file and the same text saved with LF get different hashes; if that difference should not count as a change, normalise line endings before hashing and say so in the code.
- Put the processing version in the cache key. A parser or library upgrade then misses old entries instead of returning stale results.
- Test that identical copies hit the cache, a one-byte change misses it, and two writers at once leave one whole entry (write a temp file in the same folder as the entry, then rename it over the entry; if that rename fails and the entry already exists, keep the existing entry, since the same key gives the same result, and delete the temp file).
- Meet every check in the [shared quality bar](../../references/checklists/engineering-quality-bar.md).

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
