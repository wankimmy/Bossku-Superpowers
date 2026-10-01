# Applying Claude Code practices to BosskuAI

Use this reference from the setup, instruction-management, skill-creator, and verification skills. The coverage review is in `docs/claude-practices-review.md` in the source repo. Do not load the whole reference collection at startup.

## Choose the correct extension

| Need | Surface |
|---|---|
| Portable startup behavior | Project `AGENTS.md`, imported by the existing `CLAUDE.md` adapter |
| Claude-only scoped convention | `.claude/rules/*.md` with relevant `paths` when supported |
| Reusable procedure | A folder containing `SKILL.md` and necessary sidecars |
| Repeated user-triggered workflow | A skill; `.claude/commands/` remains a legacy supported surface |
| Isolated research or validation | A focused subagent when authorized, with a bounded task and evidence output |
| Deterministic enforcement | Host permissions or a narrowly scoped hook, not prose alone |
| Durable facts and decisions | Configured memory resolved with `bossku memory-path --project <project-root>` and written through `bossku remember` |
| Distribution | Either standalone skills or a plugin bundle; verify the selected install path |

With Obsidian storage, the vault is canonical, including handoffs. If it is unavailable, report the unsaved note; do not create repository memory or sync-state files as a fallback.

## Keep startup context useful

- Count the actual loaded instructions, including imports, ancestor files, and unconditional rules. An import moves text between files but does not make it lazy.
- Keep `CLAUDE.md` concise; the Claude docs recommend under 200 lines per file. This is guidance, not a guarantee of adherence or a new Bossku validator limit.
- Put component-only conventions in scoped rules or nested instruction files. Ancestor instructions load at startup; descendant instructions load on demand when Claude works there.
- Put personal preferences in gitignored local files. Keep credentials and private machine paths out of shared examples.
- Keep setup/build/test commands discoverable and runnable. Put long procedures in references rather than expanding every startup file.
- Use `/context` and `/memory` in Claude to inspect what loaded; verify command availability for the installed version.

## Apply all nine README skill-design tips

1. **Isolated execution.** Use Claude-only `context: fork` for a self-contained task where isolation helps. Supply a real task; a guidelines-only fork has no work to do. Define inputs, outputs, tool restrictions, and a budget. Do not add Claude-only fields blindly to portable skills.
2. **Monorepo scope.** Put a project skill near its owning package when appropriate and verify discovery from the actual launch directory. Scope does not eliminate the need for trigger clarity.
3. **Folders and progressive disclosure.** Package scripts, examples, assets, and references with the skill. Link only resources needed for the task and confirm they survive user-level installation.
4. **Gotchas.** Include observed failure modes that change behavior. Existing specific Guardrails sections can serve this purpose; do not append boilerplate Gotchas to every vendored file.
5. **Descriptions are triggers.** Say when the skill should fire, with adjacent exclusions. Keep the always-listed description compact; store wider routing vocabulary in `bossku/index.py`.
6. **Useful deltas.** Include conventions or failure modes the model cannot reliably infer. Remove elementary tutorials that add context without changing behavior.
7. **Goals and constraints.** Specify observable outcomes and boundaries. Prescribe commands only for genuine invariants, reproducible checks, or known failure paths; allow implementation judgment elsewhere.
8. **Reusable helpers.** Reuse existing scripts or standard tools instead of reconstructing boilerplate. Document prerequisites and side effects; do not add a dependency just for one example.
9. **Dynamic context.** Claude's `!` shell-injection syntax runs at invocation. Use it only for narrow approved read-only inspection; verify shell/OS quoting and avoid credentials, network writes, or installs. Portable Bossku skills normally call tools explicitly instead.

## Invocation and permissions

Claude's `disable-model-invocation: true` means user-only invocation; `user-invocable: false` hides the command from the user menu, not from model invocation. These are distinct controls. Bossku's portable schema is narrower than every host's schema: validate new fields before adding them, and document unsupported fields in the host adapter rather than silently assuming they work.

`allowed-tools` can pre-approve tools in Claude; it does not turn a skill into a sandbox. Use explicit permissions, tool denials, or a restricted subagent where enforcement matters. A subagent's `skills` field preloads the full bodies and does not inherit the parent skill selection automatically. Preload only what the task needs, and verify a skill is allowed to run through that path.

Inspect actual tool and agent schemas before using fields such as `maxTurns`, background execution, or worktree isolation. Keep the configured/inherited model, bounded tasks, and exclusive writer ownership as portable defaults. Follow `bosskuai-subagent-delegation` for the common contract and sequential fallback; host controls do not confer permission for consequential actions.

## Verify discoverability and behavior

1. Inspect the installed host/version, personal/project skill roots, plugin state, duplicate names, YAML validity, and skill permission restrictions.
2. Confirm file presence, then separately confirm the host discovers the skill, then test an actual invocation when available. Report each level independently.
3. Use the name exposed by the host: standalone `/skill-name` versus plugin `/plugin-name:skill-name` may differ. Re-open a session if its cached inventory is stale.
4. Check the ideal trigger, an adjacent non-trigger, ambiguous wording, and a risky request. Add explicit names, paraphrases, negated requests, mixed concerns, and unavailable or profile-limited skills when relevant. Evaluate primary choice, complementary coverage, excluded overlaps, and invocation restrictions; rebuild the index and test routing when its inputs change.
5. Run `bossku skills audit` for prompt cost and sidecar integrity. This reports static inventory, not actual invocation frequency. Host usage measurements or hooks are separate opt-in tooling.
6. For product checks, define prerequisites, a launch command, readiness signal, inputs, expected results, observed evidence, and cleanup. Do not substitute a test-suite pass for a user path that was never run.

## Sources

- [Reviewed course README](https://github.com/shanraisshan/claude-code-best-practice/blob/7722ef7/README.md), especially How to Use, Skills, CLAUDE.md, and Workflows.
- [Claude skills](https://code.claude.com/docs/en/skills), [memory](https://code.claude.com/docs/en/memory), and [subagents](https://code.claude.com/docs/en/sub-agents). Check current primary docs before relying on version-sensitive features.
