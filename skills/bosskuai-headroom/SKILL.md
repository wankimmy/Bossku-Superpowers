---
name: bosskuai-headroom
description: "Use when large tool outputs, logs, files, search results, or agent context need local reversible compression with Headroom, or when configuring and verifying Headroom for Claude Code, Codex, Cursor, or MCP clients."
license: MIT
metadata:
  author: bosskuai
  documents: headroomlabs-ai/headroom (Apache-2.0, not bundled; see docs/third-party.md)
---

# Headroom Context Compression

Use Headroom for bulky input context. Use `bosskuai-token-saver` for shorter instructions or responses.

## Gate

1. Check whether `headroom` is on `PATH`.
2. If it is absent, explain the install path. Do not install packages or alter provider routing unless the user requests it.
3. Before a proxy, persistent configuration, or provider change, show the exact targets and get approval.

## Choose the lightest mode

| Need | Mode |
|---|---|
| Compress or retrieve one result | MCP `headroom_compress` / `headroom_retrieve` |
| Compress tool output automatically for one session | `headroom wrap <tool>` |
| Persist integration | `headroom deploy` or `headroom install apply` |
| Measure savings | `headroom savings` or `headroom_stats` |

Headroom provides wrappers for Claude Code and Codex. Cursor setup is manual; verify its current integration instructions before changing settings.

## Quality rules

- Preserve errors, identifiers, paths, commands, and decision-relevant evidence.
- Treat compressed output as a reversible view; retain and retrieve the original while its handle is valid.
- Skip tiny outputs and avoid repeatedly compressing the same content.
- Prefer the local proxy so tools need no per-command rewrite.
- Report measured savings, not estimated marketing claims.
- When compression is unavailable, fall back to narrow reads, targeted search, and summaries that preserve evidence.

## Verification

After configuration, verify the installed version, integration status, one compressed request, savings statistics, and retrieval of the original. For a temporary wrapper, also verify that exiting restores the original command path.
