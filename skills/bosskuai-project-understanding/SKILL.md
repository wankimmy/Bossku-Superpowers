---
name: bosskuai-project-understanding
description: "Read a repo to learn what the project is, who it serves, what defines behavior, and which skills to load next — oriented reading plus selective sampling over full-tree dumps."
---

# BosskuAI Project Understanding

## Configured memory location

Run `bossku memory-path --project <project-root>` to resolve `<memory-dir>` before reading or writing memory. Automatically save verified durable notes with `bossku remember` without waiting for the user to ask. When memory_storage is obsidian, all memory including handoffs lives directly in the vault; never create .bossku/memory in a code repo. The configured storage overrides legacy export wording below.

Use this skill when the first task is understanding the workspace before going deeper.

## Boundaries

- This skill answers: what is this project, for whom, with what stack, and where does truth live?
- For execution-path tracing or behavior-level debugging, switch to `bosskuai-codebase-analysis`.

## Workflow

Set the scope first: resolve the actual project root, the user's question, and the revision or working-tree state being read when available. Identify a focused reading budget and expand it only to close material uncertainties; non-Git projects remain supported.

1. Read orientation artifacts first: nearest README, `AGENTS.md`, `CLAUDE.md`, docs, manifests, env examples, CI/runtime config.
2. Read `<memory-dir>/handoff.md` and `<memory-dir>/project.md` first if they exist; leave the rest of memory until a task needs it.
3. Confirm documentation claims from real source code. Do not stop at README-level understanding.
4. Sample source intelligently:
   - entry points and framework config
   - one representative business/domain slice
   - data/model layer
   - integration boundaries
   - a few high-signal tests
5. Synthesize:
   - project purpose and likely users
   - stack and architecture style
   - code organization and source-of-truth files
   - confirmed facts vs inference vs unknowns
6. Save verified durable understanding with `bossku remember --project <project-root> --kind project`. The CLI chooses the configured memory location; do not write inferred or unknown claims into memory.
7. Recommend the next 1-3 most relevant available skills for distinct concerns. Explain what each will resolve; avoid stacking several orientation skills for the same question.

## Guardrails

- Do not guess project purpose or constraints.
- Mark unsupported business details as `Inferred:` or `Unknown`.
- For large repos, prefer stratified sampling over “read everything”.
- Cite the source locations supporting the summary, report sampled and unread areas, and distinguish source inspection from behavior actually tested. Re-check old memory and maps against the current source before treating them as current facts.

## Output

Return a concise summary covering:

- what the project is
- analysis scope and sampling limits
- who it likely serves
- stack and architecture
- source-of-truth files
- confirmed vs inferred vs unknown
- recommended next skills
- memory files updated

## References

- `../../references/playbooks/project-understanding-playbook.md`
- `../../references/checklists/project-understanding-checklist.md`
- `<memory-dir>/project.md`
- `<memory-dir>/handoff.md`
