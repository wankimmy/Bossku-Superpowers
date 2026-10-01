# Project Understanding Playbook

> If the request is general, ambiguous, or touches many files — ask clarifying yes/no questions **before acting**. Use numbered bullets with explicit answer format: e.g. `1-yes/no  2-A/B`.

Use this when the first job is to understand what a project is about before doing deeper work.

## Workflow

1. Resolve the actual project root and question. Run `bossku memory-path --project <project-root>` to locate `<memory-dir>`; read relevant project/handoff notes when present. Record the revision or working-tree state when available, without requiring Git or an origin remote.
2. Read the nearest README, instructions, manifests, and top-level structure, then sample entry points, one domain workflow, data ownership, integration boundaries, and high-signal tests. Verify documentation against source and expand only to resolve material uncertainties; report the areas left unread.
3. Identify the stack, framework, and likely entry points from both docs and code.
4. Distinguish confirmed facts from inference.
5. Cite source locations for the summary and separate source inspection, test results, and observed behavior. Keep `Inferred:` or `Unknown` claims in the report, not memory.
6. Recommend the next expert skills to load.
7. Save verified durable facts with `bossku remember --project <project-root> --kind project`. The CLI selects `<memory-dir>`; in Obsidian mode never create repo memory or fall back when the vault is unavailable.
8. If you are not sure about something important, ask the user instead of guessing.

## Output expectation

- project summary
- analysis scope, sampled/unread areas, and checks actually run
- likely users and purpose
- stack and architecture summary
- important source-of-truth files
- confirmed vs inferred
- `project.md` draft or update
- recommended next skills
- memory update recommendation
