---
name: bosskuai-videodb
description: "Use when the task explicitly concerns videodb. Ingest, index, search, edit, and monitor video and audio with the VideoDB Python SDK — upload from files, URLs, or RTSP feeds, build spoken and scene indexes with timestamped search and playable clips, transcode and reframe, do timeline edits (subtitles, overlays, dubbing), and run real-time alerts on live streams or desktop capture. Use when working with video search, transcription, clipping, transcoding, streaming, or live video alerts."
metadata:
  origin: ECC-adaptation
---

# VideoDB Skill — portable workflow

Ingest, index, search, edit, and monitor video and audio with the VideoDB Python SDK — upload from files, URLs, or RTSP feeds, build spoken and scene indexes with timestamped search and playable clips, transcode and reframe, do timeline edits (subtitles, overlays, dubbing), and run real-time alerts on live streams or desktop capture. Use when working with video search, transcription, clipping, transcoding, streaming, or live video alerts.

Use it only when the request supplies this domain, framework, data source or artifact; a shared keyword is not a match. Related skills, each for its own concern: `bosskuai-video-editing`, `bosskuai-video-style-application`, `bosskuai-rapid-prototype`.

## Workflow

Read [the source workflow](references/upstream/SKILL.md) first, then work through these sections in order:

1. Desktop Perception.
2. Video ingest + stream.
3. Index + search (timestamps + evidence).
4. Timeline editing + generation.
5. Live streams (RTSP) + monitoring.
6. How it works.

- Resolve its `scripts/`, `references/`, `assets/` and template paths against `references/upstream/`, not the project root. Source skill names map through [SOURCE.json](SOURCE.json) (`bossku skills show <id>`). ECC slash commands, agent names and package-root paths are not installed: use what this host has, or say what is missing.
- Check the project's tool versions and the source prerequisites first. A documented command is an example, not permission to install packages, add an account, expose secrets, upload private content or change an external service.
- The full source bundle is kept, with 11 sidecar files. Its code is reference-only until its dependencies, paths and effects are reviewed; this import did not run it.
- It can need a named provider, MCP server or API: check that it is available and in scope, report it when it is not, and never invent its output.

## Done when

Complete the source “Common outputs”, “Transcode video (resolution / quality change)” procedure for this task. Keep its resulting artifact, command output or cited evidence, and state what remains unverified.

If an input, provider, runtime or authorisation is missing, stop that step, carry on with read-only analysis, and say exactly what is missing. A generated plan alone is not completion.

The shared quality bar: `../../references/checklists/engineering-quality-bar.md`.

Adapted from the locally reviewed `affaan-m/ECC` snapshot: provenance and hashes in [SOURCE.json](SOURCE.json), the original text and resources in [references/upstream/](references/upstream/SKILL.md) under its [MIT licence](references/upstream/LICENSE). Copyright (c) 2026 Affaan Mustafa.
