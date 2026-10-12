# Local process and PDF pack audit

Initial read-only comparison followed by the authorised coordinated Superpowers local-snapshot refresh. The classification and per-file hash appendix below record the pre-refresh baseline; the execution section records the resulting files. No runtime installation, commit or upstream publication was performed. Local snapshots are evidence of their contents, not proof of the latest official release.

## Numbered source quotes

### Quote 1
> **Each step is one action with a checkable result:**

Source: [SKILL.md:45](C:/dev/Tenant-Management-System/skills/superpowers/skills/writing-plans/SKILL.md:45).

### Quote 2
> Execute the plan yourself, task by task, in this session: no implementer

Source: [SKILL.md:8](C:/dev/Tenant-Management-System/skills/superpowers/skills/executing-plans/SKILL.md:8).

### Quote 3
> **Core principle:** Every finding cites `path:line`. No citation, no

Source: [SKILL.md:15](C:/dev/Tenant-Management-System/skills/superpowers/skills/diagnosing-superpowers/SKILL.md:15).

### Quote 4
> 1. **Installed `--help` / `-h`** — the truth for the user's version. Always wins.

Source: [SKILL.md:50](C:/dev/Tenant-Management-System/skills/opendataloader-pdf/skills/odl-pdf/SKILL.md:50).

### Quote 5
> **Minimum code that solves the problem. Nothing speculative.**

Source: [SKILL.md:25](C:/dev/Tenant-Management-System/skills/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md:25).

### Quote 6
> - Don't "improve" adjacent code, comments, or formatting.

Source: [SKILL.md:40](C:/dev/Tenant-Management-System/skills/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md:40).

### Quote 7
> 4. **Make the smallest change that passes.** Update every call site: search for the old name, signature or behaviour across code, scripts and docs. Leave unrelated code alone; remove only what your change orphaned.

Source: [SKILL.md:13](C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-engineering-delivery/SKILL.md:13).

### Quote 8
> 2. **Stdlib does it?** Use it.

Source: [SKILL.md:29](C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-ponytail/SKILL.md:29).

### Quote 9
> `superpowers` has one local addition to re-apply on any re-vendor: `verification-before-completion/SKILL.md` has a section "Match Evidence to the Intended Outcome" (a build or test run supports only the behaviour it covers; for documentation and agent instructions, check how the consumer discovers and loads them; keep local runs, external CI and assumptions apart) and two extra rows in the "Common Failures" table. The upstream text is otherwise unchanged.

Source: [third-party.md:28](C:/Users/mspc0/OneDrive/Documents/Bossku-AI/docs/third-party.md:28).

### Quote 10
> Copyright (c) 2025 Jesse Vincent

Source: [LICENSE:3](C:/dev/Tenant-Management-System/skills/superpowers/LICENSE:3).

### Quote 11
> license: MIT

Source: [SKILL.md:4](C:/dev/Tenant-Management-System/skills/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md:4).

### Quote 12
> Apache License

Source: [LICENSE:1](C:/dev/Tenant-Management-System/skills/opendataloader-pdf/LICENSE:1).

### Quote 13
> git merge-base --is-ancestor "$base" "$head" || { echo "HEAD is not a descendant of BASE: ${base}..${head}" >&2; exit 3; }

Source: [review-package:27](C:/dev/Tenant-Management-System/skills/superpowers/skills/subagent-driven-development/scripts/review-package:27).

### Quote 14
> # a plan-path marker (repo-relative in-repo, absolute outside). A workspace

Source: [sdd-workspace:13](C:/dev/Tenant-Management-System/skills/superpowers/skills/subagent-driven-development/scripts/sdd-workspace:13).

### Quote 15
> return renderBranding(frameTemplate).replace('<!-- CONTENT -->', () => content);

Source: [server.cjs:264](C:/dev/Tenant-Management-System/skills/superpowers/skills/brainstorming/scripts/server.cjs:264).

### Quote 16
> ## Declined to judge

Source: [code-reviewer.md:43](C:/dev/Tenant-Management-System/skills/superpowers/skills/requesting-code-review/code-reviewer.md:43).

### Quote 17
> Invoke bundled scripts through their interpreter in the prose (`bash scripts/tool.sh`, `node scripts/tool.js`), never by bare path: some harness plugin packagers strip executable bits, and a bare `scripts/tool.sh` fails there with `Permission denied`.

Source: [SKILL.md:374](C:/dev/Tenant-Management-System/skills/superpowers/skills/writing-skills/SKILL.md:374).

## Canonical skill classification

Hashes below are SHA-256 of original file bytes, abbreviated to 16 hexadecimal characters for display. The per-file appendix contains full hashes. Text comparison normalizes CRLF to LF only; resource comparisons do the same for detecting substantive changes. All 17 canonical skills in these three local packs are classified.

| Skill | Classification | Local SHA-256 prefix | Bossku prefix | Minimal action |
|---|---|---|---|---|
| [brainstorming](C:/dev/Tenant-Management-System/skills/superpowers/skills/brainstorming/SKILL.md) | Content/resource delta | `6ee10d1481b8a258` | `99476557e55f9daa` | Refresh only as a full documented Superpowers snapshot: rewrite plus companion scripts and prompt change together. Re-check Bossku bounded-task approval exception. |
| [diagnosing-superpowers](C:/dev/Tenant-Management-System/skills/superpowers/skills/diagnosing-superpowers/SKILL.md) | Absent from Bossku | `5a652f8132cc901e` | `absent` | Add useful unique diagnostic capability as the full 20-file bundle; preserve privacy and explicit export controls, without automatic transcript capture. |
| [dispatching-parallel-agents](C:/dev/Tenant-Management-System/skills/superpowers/skills/dispatching-parallel-agents/SKILL.md) | Line endings only | `1968923066f3b707` | `fc9875393a1dcd6b` | Keep current skill; only normalize line endings during a coordinated pack refresh. |
| [executing-plans](C:/dev/Tenant-Management-System/skills/superpowers/skills/executing-plans/SKILL.md) | Content/resource delta | `f38e8f2ddcf079f6` | `fe85231f6c15b83d` | Refresh inline execution with both task ledger scripts; align selector with same-session inline vs subagent mode. |
| [finishing-a-development-branch](C:/dev/Tenant-Management-System/skills/superpowers/skills/finishing-a-development-branch/SKILL.md) | Line endings only | `8db5a922b242dd4e` | `2b8cb8f9cabb1951` | Keep current skill; only normalize line endings during a coordinated pack refresh. |
| [receiving-code-review](C:/dev/Tenant-Management-System/skills/superpowers/skills/receiving-code-review/SKILL.md) | Line endings only | `091df1629510af1b` | `bbe7eb200ac9feb9` | Keep current skill; only normalize line endings during a coordinated pack refresh. |
| [requesting-code-review](C:/dev/Tenant-Management-System/skills/superpowers/skills/requesting-code-review/SKILL.md) | Content/resource delta | `2180e14a448e9410` | `7681db08bd8697f9` | Refresh reviewer resource and merge-base example together. |
| [subagent-driven-development](C:/dev/Tenant-Management-System/skills/superpowers/skills/subagent-driven-development/SKILL.md) | Content/resource delta | `8dde5589ee083fb4` | `ca15b1b17cabe882` | Refresh all changed scripts/prompts together; validate multi-commit review range and workspace compatibility. |
| [systematic-debugging](C:/dev/Tenant-Management-System/skills/superpowers/skills/systematic-debugging/SKILL.md) | Content/resource delta | `51c6435d98c83c42` | `23f249e47a3a4b06` | Refresh the safer environment-presence example without printing secret values, using documented upstream snapshot. |
| [test-driven-development](C:/dev/Tenant-Management-System/skills/superpowers/skills/test-driven-development/SKILL.md) | Content/resource delta | `64b03fce4aee5a97` | `fad42344223013a5` | Refresh suite verification paragraph, keeping task-specific user testing constraints authoritative. |
| [using-git-worktrees](C:/dev/Tenant-Management-System/skills/superpowers/skills/using-git-worktrees/SKILL.md) | Line endings only | `8cfb86f121269e8f` | `49ac647dd5a65e0e` | Keep current skill; only normalize line endings during a coordinated pack refresh. |
| [using-superpowers](C:/dev/Tenant-Management-System/skills/superpowers/skills/using-superpowers/SKILL.md) | Content/resource delta | `82c5c8866ad7f5dd` | `3ff749d00d9baa18` | Include new Claude Code and Muse references when refreshing; keep Bossku activation precedence. |
| [verification-before-completion](C:/dev/Tenant-Management-System/skills/superpowers/skills/verification-before-completion/SKILL.md) | Content/resource delta | `2befe7fc55bcadaa` | `36095dec795942e0` | Preserve and re-apply documented Bossku outcome-evidence overlay (quote 9); upstream refresh alone would remove it. |
| [writing-plans](C:/dev/Tenant-Management-System/skills/superpowers/skills/writing-plans/SKILL.md) | Content/resource delta | `a6c67c1900064347` | `82e7d50b27b5f460` | Refresh checkable-step/review-focus guidance; decide removal of obsolete plan reviewer resource from upstream dependency references. |
| [writing-skills](C:/dev/Tenant-Management-System/skills/superpowers/skills/writing-skills/SKILL.md) | Content/resource delta | `bbdfe742f853562e` | `09de7d4b8e865ab3` | Refresh interpreter-explicit script calls; keep bundled Node renderer resources. |
| [odl-pdf](C:/dev/Tenant-Management-System/skills/opendataloader-pdf/skills/odl-pdf/SKILL.md) | Byte-identical bundle | `b5d0644007c8badc` | `b5d0644007c8badc` | Keep exact 12-file bundle, LICENSE and NOTICE; runtime remains opt-in and installed help stays authority (quote 4). |
| [karpathy-guidelines](C:/dev/Tenant-Management-System/skills/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md) | Absent from Bossku | `e2553e9b66299fbc` | `absent` | Do not vendor now: existing Ponytail and engineering delivery cover simplicity and surgical changes (quotes 5–8). Clarify first-party assumption/success criteria only if a concrete gap appears. |

## Actual upstream modifications and useful unique additions

The user chose to add every useful unique skill, including niche domains. In these packs, diagnosing-superpowers is the only absent skill with a distinct workflow: transcript-backed skill invocation, cost/time, repeated-work and plan-adherence diagnosis, with scrubbed exports on explicit request (quote 3 and its full workflow). Add the complete 20-file bundle during the coordinated refresh. Karpathy is absent as a named skill but its capabilities already exist in Ponytail and engineering delivery; a duplicate always-on skill would not be a unique addition. ODL is already complete.

Actual substantive resource deltas: brainstorming changes server.cjs replacement to a callback so generated content is inserted literally, swaps spec-document-reviewer for builder-check prompt, and makes companion calls interpreter-explicit. Executing-plans adds task-start and task-done ledger scripts. Subagent review-package now rejects non-descendant and empty ranges; sdd-workspace records plan identity to avoid basename collisions; task-brief invokes scripts through bash. Requesting-code-review adds reviewer guidance for unstated realistic inputs and situations it declined to judge. Writing-plans replaces fixed 2–5 minute granularity with checkable outcomes and adds review-focus tests, while removing its upstream plan-document-reviewer resource. Writing-skills adds interpreter-explicit script guidance. Systematic-debugging changes environment examples to report presence without displaying the value. Using-superpowers adds Claude Code and Muse tool references. The full hash appendix distinguishes these from CRLF-only changes.

## Minimal update sequence

1. Treat Superpowers as one coordinated upstream refresh, not piecemeal rewrites. The local plugin manifest says version 7.0.0; Bossku records last sync 2026-09-07 in skills/vendored.json. Verify the chosen official commit/tag before mutation; record commit, date and license, and preserve complete referenced resources. Local content alone does not authenticate an official upstream commit.
2. Preserve the outcome-evidence addition already documented in docs/third-party.md (quote 9). Reapply it after refresh and keep its consumer-loading distinction. Do not adopt the local upstream removal as a quality regression.
3. Test execution mode handoff, interpreter calls, ledger persistence and review ranges before changing routing. Version 7 inline execution is a coherent option (quote 2), not a reason to force subagents for every task. Keep Bossku smallest-stack selection and user authorisation precedence.
4. Keep ODL unchanged. It is byte-identical including all resources; existing first-party grounding and product verification complement its installed-help and output-verification procedure. No new runtime dependency or automatic install is warranted.
5. Keep Karpathy as studied guidance rather than another always-on skill. Its concrete simplicity/surgical rules overlap first-party Ponytail and engineering delivery (quotes 5–8). If enhancing first-party guidance, add only an explicit assumption plus observable-success check where missing; do not copy the full skill or create a duplicate routing target.

## License and trust evidence

- Superpowers local LICENSE is MIT, copyright Jesse Vincent (quote 10); Bossku attribution exists in [third-party.md:8](C:/Users/mspc0/OneDrive/Documents/Bossku-AI/docs/third-party.md:8). Preserve the MIT notice on refresh.
- ODL local Apache-2.0 LICENSE and NOTICE compare to Bossku copies below. The exact bundled skill/resources need no refresh. Attribution: [third-party.md:22](C:/Users/mspc0/OneDrive/Documents/Bossku-AI/docs/third-party.md:22).
- Karpathy declares MIT in its skill (quote 11) and README, but the local tree has no standalone LICENSE file. Do not redistribute copied text until the original upstream license/copyright notice is verified and preserved. This audit proposes no copied content.
- Applicable local source AGENTS.md was read. Its upstream-PR requirements concern contributions to that source repository; this read-only comparison creates no upstream PR.

## Scoped router final adjudication

The resolved round-5 regressions passed: plain React animation retains animate and excludes animate-expo; report reading/summarising excludes loop-triage; explicit animate-expo remains allowed. The exact regression plus three signature tests passed (4 tests, 0.906 seconds). Fresh signature measurements were 23.84–30.46 ms, median 25.83 ms, under the unchanged 50 ms bar. This is scoped evidence only; the broad suite result is not declared green here.

## Executed refresh and remaining limits

- Refreshed all 15 Superpowers skill bundles from the audited local snapshot: 74 files total, including the new 20-file diagnosing-superpowers bundle. Removed the two obsolete upstream reviewer resources: brainstorming/spec-document-reviewer-prompt.md and writing-plans/plan-document-reviewer-prompt.md.
- Preserved the exact documented verification-before-completion outcome-evidence section and its two Common Failures rows. Removing only those additions reconstructs the upstream skill text exactly. Every other copied file matches its local snapshot byte-for-byte at initial validation.
- Provenance: .git/HEAD resolves refs/heads/main to bb92a77741419a4ab5f06e711a283343f1ada0c3; origin/main is the same. The configured remote is https://github.com/obra/superpowers.git. The plugin manifest says 7.0.0, while the local v7.0.0 tag points to 7f043e5eaf3522dc19178c673b76328de9b0c355. Therefore record this as a main-branch local snapshot at the explicit commit, not as the exact v7.0.0 tag.
- All 74 source skill files match their tracked Git index blob hashes after normalising checkout CRLF to LF; no untracked source skill files were found. Git status could not run against this source path in the sandbox, so full-repository staged/dirty status remains unverified. This source-skill comparison does not establish that its Git index matches HEAD.
- Validation: exact inventory and file-content comparison passed for 74 files, with only the preserved overlay excluded. All 27 Markdown local links were inspected; 12 resolve and 15 are illustrative fictitious resource names in writing-skills/anthropic-best-practices.md (PDF/DOCX/finance examples), unchanged from upstream. Required diagnosing prompts/references/templates, new using-superpowers harness references, and executing-plans cross-skill scripts/reviewer are present. No bundled Python scripts exist, so Python AST parsing is not applicable.
- ODL's 12-file bundle and Apache LICENSE/NOTICE remain unchanged. Karpathy was not duplicated. Shared provenance, routing metadata and index updates belong to the root agent and were not edited by this refresh task.
- Not verified by this task: live Claude/Codex skill invocation, transcript-diagnostic privacy behaviour in a real session, Bash/Node script execution, upstream commit/tag authenticity over the network, or the post-refresh broad suite. The prior baseline broad-suite result does not prove the refreshed packs.

## Pre-refresh per-file hash evidence

ODL LICENSE: normalized identical = `True`; local `c95bae1d1ce0235ecccd3560b772ec1efb97f348a79f0fbe0a634f0c2ccefe2c`; Bossku `c95bae1d1ce0235ecccd3560b772ec1efb97f348a79f0fbe0a634f0c2ccefe2c`.

ODL NOTICE: normalized identical = `True`; local `5d9c19bfdbbf656c87869f597b8629517d27c4affdf3e71b14e19a14c2e2ef8b`; Bossku `5d9c19bfdbbf656c87869f597b8629517d27c4affdf3e71b14e19a14c2e2ef8b`.

### brainstorming
Local `8` files; Bossku `8` files. Content changes after line-ending normalization: SKILL.md, scripts/server.cjs, visual-companion.md. Local-only: builder-check-prompt.md. Bossku-only: spec-document-reviewer-prompt.md.

- `SKILL.md`: local `6ee10d1481b8a2580d5336ff66c5c08acc9d4b251b13bbc3bfd31be99c261d43`; Bossku `99476557e55f9daa60bee5ba350c2c2800fae621c54f5aca3c32ecb85f803a1a`.
- `builder-check-prompt.md`: local `36d51a4723d6f0a3ce5811a0ea3b3a8424f07533947e1355f5d8cb8cce40c55e`; Bossku `absent`.
- `scripts/frame-template.html`: local `7b9418e9939dded0cf8e6a5549a18162b7c7e5495deeefa83a12f3394b81395d`; Bossku `7b9418e9939dded0cf8e6a5549a18162b7c7e5495deeefa83a12f3394b81395d`.
- `scripts/helper.js`: local `43c6d69954a46ec34a2a262bcc62a9a7e83e839c739f199cb72646d397c686e3`; Bossku `78c3a22dd5e799623cab8908b0b03e764404efde2d2edc94a8814cf450a09e81`.
- `scripts/server.cjs`: local `a2397d59c7f7bd1a110e258c707ccf47ede42ba8dfc765c03669a3ee81cf3791`; Bossku `ee89af11506ac4933324c89a2cfb36b391fe611f82efb9eeb3b814e40825145f`.
- `scripts/start-server.sh`: local `a4e5ae84275bcaacd2f84345afeabe59cf7b00ba080e123da7cc1fb226f12847`; Bossku `526f3fc34bbdc56d97532d84bf861a1113f9f08fec6479c3553c13ec627c2448`.
- `scripts/stop-server.sh`: local `0b5ccbbd57f62d3ed88993f7940b5ee0e5c0fc9b21c550c623da4f6292e47daf`; Bossku `6a2f3f3b7ca84fde8ef3c43825d392e1f12126b52a93b42c4d4940779bac884d`.
- `spec-document-reviewer-prompt.md`: local `absent`; Bossku `793f2546815a28f2712f0dcb926ab96dc4a60145fbea6f9a08d88287ec8e15bc`.
- `visual-companion.md`: local `6ffcb038b53254bd31debaa15e12dcd4ff24bd63d690e0b644ac6396701cf2e2`; Bossku `770ba4339dd33b24b11100b20e4343670442764087f32b710390704755f9778a`.

### diagnosing-superpowers
Local `20` files; Bossku `0` files. Content changes after line-ending normalization: none. Local-only: SKILL.md, prompts/analyst-common.md, prompts/cost-and-time.md, prompts/plan-adherence.md, prompts/quality-evidence.md, prompts/repeated-work.md, prompts/request-conflicts.md, prompts/scrub-audit.md, prompts/scrub.md, prompts/similar-session.md, prompts/skill-timeline.md, prompts/stumbles.md, references/context-safety.md, references/github-issues.md, references/redaction-policy.md, references/session-discovery.md, templates/bundle-README.md, templates/case.md, templates/issue.md, templates/report.md. Bossku-only: none.

- `SKILL.md`: local `5a652f8132cc901eb5ca61f89157839f87a2f20aed037fc7a2b51051bc37cd19`; Bossku `absent`.
- `prompts/analyst-common.md`: local `88801c36070be2a54a8a9a29632b01ab21db053e2e76ee49b5252a9b74ca4090`; Bossku `absent`.
- `prompts/cost-and-time.md`: local `fe97a66d4db3b436816ef82694bda413b522b3a862dd41978da01e358fffecc4`; Bossku `absent`.
- `prompts/plan-adherence.md`: local `1dcbab82033598a2e9c9ee42e950d4b1822d2c871c02cef9e102cdd5cbbda113`; Bossku `absent`.
- `prompts/quality-evidence.md`: local `749d11cf678f379ed77a29274cad456634e0284aa523639a1a214a9f2b986eb1`; Bossku `absent`.
- `prompts/repeated-work.md`: local `895027f2dfa4b1b8bcdb7ac9aec8d45a80bff212fad6ec6cad5ab38fa68322f5`; Bossku `absent`.
- `prompts/request-conflicts.md`: local `e800e38d8b7752c212c76c5c3ed75cd78b749684263ea0c313586f26af6f4b5c`; Bossku `absent`.
- `prompts/scrub-audit.md`: local `5cc48f05a7f81f5f7e05e0c7ceafc0fb8774bcaf75fe88dcb5c7e408026c70ad`; Bossku `absent`.
- `prompts/scrub.md`: local `854cb3320cc5377b493cea2f72519d67983464882db68a0f408a7d0a0f040b8c`; Bossku `absent`.
- `prompts/similar-session.md`: local `b190f713b463df2bb5ec3914647e204074d1bd50643a53159db6d13cace916c1`; Bossku `absent`.
- `prompts/skill-timeline.md`: local `45d604d583b57a77b9033eced8eb875ef342af70fcd66cf7d15c6dc89964890f`; Bossku `absent`.
- `prompts/stumbles.md`: local `1f2d1f048aff7b8b400006301f1ce8c232ecc7e9d5f705af27a849b2c03ea2e7`; Bossku `absent`.
- `references/context-safety.md`: local `e6be2bd3495f454d4bedee9484d728d245d1fa656e11fc4ceec5693c16e4730a`; Bossku `absent`.
- `references/github-issues.md`: local `a656f5e15b21c7a200c39c038f5ede74b9d6ea3ceeb90f39af7e930c8d8424d6`; Bossku `absent`.
- `references/redaction-policy.md`: local `96b16f47074838fe2d7e609577d6f8b0ad460f8378b281a3f96ee23cb5a08bde`; Bossku `absent`.
- `references/session-discovery.md`: local `6d1dced083e5d978448a78df298cf515531b0eb39b2854a4a2afbffeb69a7435`; Bossku `absent`.
- `templates/bundle-README.md`: local `2e6ddc6b106028d5ebd00a50ad93a77111d675c219ee1273cd0857869e8d51ec`; Bossku `absent`.
- `templates/case.md`: local `597892462be83bc478536ec91f7c285f6dd25d119c560734a3a180fe8471301d`; Bossku `absent`.
- `templates/issue.md`: local `8f28dbfe60602f77dda76d81815cb4e2dce7d3e2a93348890e1581be8310ac1f`; Bossku `absent`.
- `templates/report.md`: local `38295d0fd785e8608f330815c59ebd7047942002ec7085aecbed54681f56b0c1`; Bossku `absent`.

### dispatching-parallel-agents
Local `1` files; Bossku `1` files. Content changes after line-ending normalization: none. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `1968923066f3b707eb01d1992cdf4c42284c3855f70253b9cd5000ff45fca13c`; Bossku `fc9875393a1dcd6b649bf22d9ff62f3a02080c0ce365932451bc73e63d87ddab`.

### executing-plans
Local `3` files; Bossku `1` files. Content changes after line-ending normalization: SKILL.md. Local-only: scripts/task-done, scripts/task-start. Bossku-only: none.

- `SKILL.md`: local `f38e8f2ddcf079f65493adc713c1fed78421dfaf5f4dbf6b3a6b2b1d95466e71`; Bossku `fe85231f6c15b83dfadf1409535d01f304c43b920bc937b1dcc0907ec7824984`.
- `scripts/task-done`: local `91e1a68e50a2c9b31193e8ca7feeba9f21e81eee9aa409ba05e5d407ff926bd6`; Bossku `absent`.
- `scripts/task-start`: local `5eb4db5457bfe9d201712fd7322896afd2f7f12b277b563900331b4e2ddfb114`; Bossku `absent`.

### finishing-a-development-branch
Local `1` files; Bossku `1` files. Content changes after line-ending normalization: none. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `8db5a922b242dd4e1bf824cb91c13b3e8d8e8a86d6ceaf7f0774eb9cce909d65`; Bossku `2b8cb8f9cabb1951be2ebb1d72da90d3313f7e3705fd25f5b8f2d0432e139bae`.

### receiving-code-review
Local `1` files; Bossku `1` files. Content changes after line-ending normalization: none. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `091df1629510af1b92fc4abd6f96732ebedb4cb2c0f3457e8f2740b0504a2438`; Bossku `bbe7eb200ac9feb97f2620308ba8ecb517837465009a858bc5687695f3d0a6ae`.

### requesting-code-review
Local `2` files; Bossku `2` files. Content changes after line-ending normalization: SKILL.md, code-reviewer.md. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `2180e14a448e9410bec88e6646a2d1f0ce7fdd58de27388c1e052e929679d2bc`; Bossku `7681db08bd8697f94295c7689e1fc059b7ea76136995b181d8a53f5cbbde7973`.
- `code-reviewer.md`: local `82e370be6b3447523816286195571e4216ba56ba1ad6ad0e87862294c4c78dcb`; Bossku `8bf83519a1cd1c40de0f2c1ee98939d872bf2b151064ea90876dd3a14530c94a`.

### subagent-driven-development
Local `7` files; Bossku `7` files. Content changes after line-ending normalization: SKILL.md, re-review-prompt.md, scripts/review-package, scripts/sdd-workspace, scripts/task-brief, task-reviewer-prompt.md. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `8dde5589ee083fb4999106d116f01c8fdaf3116a8a9813fdedeb80329de49046`; Bossku `ca15b1b17cabe88289d0b30294b8ba5ae83a4199615584a58778b6620b516fb7`.
- `implementer-prompt.md`: local `81dd9d5a3fb0b09b96b5829f03b9796842f3199ef7591d1ba1c2db2a515f64d0`; Bossku `bda42c4969d1578eab92bc1cca864397203329d22dbc143a8c6a896adb548b42`.
- `re-review-prompt.md`: local `0828a5e9cbb12ba49f14621dd8c3953c48c0fc383e75bb5494f055ed0d6d824f`; Bossku `39bf775586e5be93da98c4f16be5c556195fc806509d22e3f3a79f96c1a0c5d7`.
- `scripts/review-package`: local `f617c52c538f09b13bd19a301cf5201584dcfd7aaf552eedefb3405f3f90fe0e`; Bossku `7cfee68ad5c53dea3532acd4c34d85148d3e591f2f8da94853478ffd57bf4211`.
- `scripts/sdd-workspace`: local `882dd51412f09717fadad6a84c5e60266a8d8a902f43b49bc07f8cc739222c79`; Bossku `36c0cad20d4891dace227110c17624e09a1e607329841b5de02fb84fd37d4207`.
- `scripts/task-brief`: local `51bb3fb73b07f85fd19d8f29f178451f7557b8c3d084a85835c5bc6bc15869f3`; Bossku `be4896abf0918da67832e81cad80d39599f85e461e721f4613828a3810f3e493`.
- `task-reviewer-prompt.md`: local `bfed55c8f19d0ff6ed57b0fe09127c92890e9311c6c73917129598826bf9ebe8`; Bossku `d9a35c4c09034622606061414b988ef618d47940cef1be6bdd91e70a524395c8`.

### systematic-debugging
Local `11` files; Bossku `11` files. Content changes after line-ending normalization: SKILL.md, root-cause-tracing.md. Local-only: none. Bossku-only: none.

- `CREATION-LOG.md`: local `c24733a5b1821bd6bed1fc950261f0b9f4e90097e0bbb96459d8179713730789`; Bossku `397f122f115f994372a1805e30071fc0ad86c0dc1e427fbf5b5f1b14143399f5`.
- `SKILL.md`: local `51c6435d98c83c42c96ba7c35725a0b2c376cd487fb1a4e6bd0ddbe7e33ef202`; Bossku `23f249e47a3a4b06c3a5030e37aaf3ced12a54f406782766b384ed127d21eca4`.
- `condition-based-waiting-example.ts`: local `40ae5ebe497fdf310200e43fe986552546d0a22837c0d39e855db1cfd33eb88e`; Bossku `0602407671f97439acc9e3cc2fe27ad42a22eb0dbca62f56d610fb223daadb0f`.
- `condition-based-waiting.md`: local `e89fec8400d6cd50f43407cec9fab50976ba4d55d0ec2eb51c0bd68036b54c26`; Bossku `02aa854bd9e761f275e1450d7136ba60f1a4d103fe94b552fdce822dd3c99506`.
- `defense-in-depth.md`: local `1e175fb86fc357e58c6aebf5441e481e1b7868b4380c0456b63a17eefbd18ba7`; Bossku `9407efcbd028a5ec45edfdf6692b988716c0a7b34d1fb5e05d60146171d8041e`.
- `find-polluter.sh`: local `dd7b8f13c4cc2a24b33ff87b18da9248f3e1c80a085c3316224f69ff0fa5c43c`; Bossku `31aa8bbab625ffae398c357de90fe3f4cb8f6dd39b23101bf81ef6dd53638b7c`.
- `root-cause-tracing.md`: local `75b933b6a8c40bdb2031b10f21654395b56ec6ab6bc7b018c18d3fe57aeb7fb8`; Bossku `cb00878f1b5b79442dc474f0e0d67b44f8175e741ba90abbf5e9778b67ba4854`.
- `test-academic.md`: local `fe2ba480d78ac0d686dc025f41c2a32a43d642bf533f91b0c6053a04d35d6486`; Bossku `51e07c1c56052a6c46cde8e7d42d6612598ea076f128086fd85911f4d2d3e8dd`.
- `test-pressure-1.md`: local `0b6a915db0054577819834c79be9eb614e97bddba10d73768e1fbe91cfed048a`; Bossku `fbf04219c44460e76d96642d7dc16960a2390936e0a6937d0b133e013fa55afb`.
- `test-pressure-2.md`: local `b2030aeffba07050e8ad573ddf87486457c4a016a786bb326235bebd856f2016`; Bossku `fc6b2594bed3f2a15ece75d0a211b55cb9a4668d85b9873f2bab5ee54ed31cbf`.
- `test-pressure-3.md`: local `96b50a52e2c7989c9cf20fb752c47c1e9a3a70dc362f8f7989f8f5b64dac7708`; Bossku `69ed6a5a59dac92d58d284519991a46b90978bc40a229776dac0ffa3a6123bfe`.

### test-driven-development
Local `2` files; Bossku `2` files. Content changes after line-ending normalization: SKILL.md. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `64b03fce4aee5a97a93160cea8111f3ba13a17b7c001db4bd5836d67fd10705d`; Bossku `fad42344223013a560fb3f2a9ad40509c5ea569595bab7f064dbf13149e9c53f`.
- `writing-good-tests.md`: local `51471c853306ff92ca8bb41dcaea05f31c0e46b03651f8f3c99754b7172f4ae1`; Bossku `87f56d0a4236f804165149ec038787d20062afc9b37aa240a167c394b39d2065`.

### using-git-worktrees
Local `1` files; Bossku `1` files. Content changes after line-ending normalization: none. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `8cfb86f121269e8f7f12361e6795c4f6738828340e28964c9229d365666c9edd`; Bossku `49ac647dd5a65e0e79f87d346005dde8ce27c6886bccf966164917ee8bb4df80`.

### using-superpowers
Local `8` files; Bossku `6` files. Content changes after line-ending normalization: SKILL.md. Local-only: references/claude-code-tools.md, references/muse-tools.md. Bossku-only: none.

- `SKILL.md`: local `82c5c8866ad7f5dd4440ce66bd7806ba48a2f13771beae5cf112e53f08fe36ba`; Bossku `3ff749d00d9baa18813a2ec2a114d09b6c0bf6e9938b030aac617c0ea12added`.
- `references/antigravity-tools.md`: local `4880f6de3da4e32f9659ebe7a72b9e0ebfff04e028c2ed96173f86d0387a04c0`; Bossku `343af08abab2936a4063399ec0908a0d3a129f66a54a42ef1f14e9b9edc0b8fa`.
- `references/claude-code-tools.md`: local `21479a3fee27448cab8748a3b5687e53bb257883bda9c070426f9a1ab5cebf1b`; Bossku `absent`.
- `references/codex-tools.md`: local `1a38ad9b188c393052f58d95657a1c35ea6aafc8b5a27f198f3922912f70bbe7`; Bossku `51d2e878aac90809bfdd0358c974281e2fb88c7d46571e6310587d9df6cd55ea`.
- `references/gemini-tools.md`: local `62b9157bcb0ee3c6784e3d0da0798ddfa5872f9e0c34bea48f3079dabea71965`; Bossku `3e0e732356eaf1780da7cfd93773723a68ff1fe03dbc519aaac38cd7e9b62e87`.
- `references/hermes-tools.md`: local `e2185c976a3c87503910e05e2aea58cc89bc8e569bb624b93df9958ac47a9190`; Bossku `32c262e22da268ac1bc33f2b318e597e78539f10be170a7453dee07ff432f36b`.
- `references/muse-tools.md`: local `5a1da5c575fe18456ca71cd47ebfd8a38c745f8d82a67fe64d5b83080000eeb3`; Bossku `absent`.
- `references/pi-tools.md`: local `703dbc83d23ecab9c6f388460c38abc482e9dee2fe6772a8c7a255152ad3a4d5`; Bossku `fb6db6991508e958b0117861b6107fb1cafcc752210c7cfe66def13f1e34d371`.

### verification-before-completion
Local `1` files; Bossku `1` files. Content changes after line-ending normalization: SKILL.md. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `2befe7fc55bcadaa3d97dd9e8efeb633d2561c0ebe74c5a8b17c4d9e7e4520b3`; Bossku `36095dec795942e008f81f6dcb9f62453595b1a48fafec119fa78aafae20fc61`.

### writing-plans
Local `1` files; Bossku `2` files. Content changes after line-ending normalization: SKILL.md. Local-only: none. Bossku-only: plan-document-reviewer-prompt.md.

- `SKILL.md`: local `a6c67c1900064347c2a329990dd3c555657c51c3ec53b259a08aa01a2c26139a`; Bossku `82e7d50b27b5f460a1f30858408483cbbdda55b1b3da78e3fd86fa7b60573081`.
- `plan-document-reviewer-prompt.md`: local `absent`; Bossku `5e9997798714b4e7275a2b87374c75211122b4449a17aee61b936e9097e3c449`.

### writing-skills
Local `7` files; Bossku `7` files. Content changes after line-ending normalization: SKILL.md. Local-only: none. Bossku-only: none.

- `SKILL.md`: local `bbdfe742f853562e643a3d40d64476359d47881e39cef80a189283fa26d11ab9`; Bossku `09de7d4b8e865ab333438520ce772a006b04da6a3a7beb81b4e3b4bbe94d268b`.
- `anthropic-best-practices.md`: local `217629b356c09c9bd11017c9788e8fc654ca1b32c92d4a51cd490e16dd65e59a`; Bossku `26f2fc231b4bea7ad7ec034a61615f8fe8bfff6c436ad77e60d5734be16a6a15`.
- `examples/CLAUDE_MD_TESTING.md`: local `0b379a3415e185d3c434b3ad283d8aa132f3022c2a4f210f168865b5986bcef0`; Bossku `3648a10c414546fdea2eae3a8f21345cda2234aca54a084042e5f933a6b332ca`.
- `graphviz-conventions.dot`: local `b18a02773875f6c7b92f2a260e88550c92a62549b0009df9d680f7e9541d0ecc`; Bossku `b18a02773875f6c7b92f2a260e88550c92a62549b0009df9d680f7e9541d0ecc`.
- `persuasion-principles.md`: local `a51bc9bf75189ea73a27b3fb504a2fdfdb966fb1f7f1cdf03203230a216ccc03`; Bossku `73ffb3d9d9f510f82296de0e3509bdcc1bae13379ef56354877e3f33303b44bf`.
- `render-graphs.js`: local `c7f412cc629461c4d10287e668731874c0497707023e3e3f74a5355eb2cee196`; Bossku `7f558e910dc0dc1c24a30fda9b0595643399f16014f8cd12b56e1ef1ad113a84`.
- `testing-skills-with-subagents.md`: local `c711346852c911b24a84aa161e0cff06a4cd7f4e2fa9e9c0a266cead5afcbade`; Bossku `134a5d0f695d717f6d34609dff44ec9316a593c2f6db981ec94a61750fcce1bb`.

### odl-pdf
Local `12` files; Bossku `12` files. Content changes after line-ending normalization: none. Local-only: none. Bossku-only: none.

- `README.md`: local `2898b259d9f7e5403d61485d14daef63d2c0aa2e1d86dd440cf8025b4aafdbc7`; Bossku `2898b259d9f7e5403d61485d14daef63d2c0aa2e1d86dd440cf8025b4aafdbc7`.
- `SKILL.md`: local `b5d0644007c8badcb918e8456e601457bd0731f10db8173b4b78b77d92abfaba`; Bossku `b5d0644007c8badcb918e8456e601457bd0731f10db8173b4b78b77d92abfaba`.
- `references/eval-metrics.md`: local `999b308539645d1892f50afe575d258e77538af9cfcba8ae1eb08fec8f192240`; Bossku `999b308539645d1892f50afe575d258e77538af9cfcba8ae1eb08fec8f192240`.
- `references/format-guide.md`: local `1b1e8206329a6f73ee01a393e1078211efd95948016f4184364ef7aa0d49c25a`; Bossku `1b1e8206329a6f73ee01a393e1078211efd95948016f4184364ef7aa0d49c25a`.
- `references/hybrid-guide.md`: local `659db118c2809b24f696274a12bb29b97686a2f151ed4fc685ab330f54d501fe`; Bossku `659db118c2809b24f696274a12bb29b97686a2f151ed4fc685ab330f54d501fe`.
- `references/installation-matrix.md`: local `5bc6bd9d8a392dc37538a2c01019e4957ba498dfa3f4faf3d49f1f7ad57df6d7`; Bossku `5bc6bd9d8a392dc37538a2c01019e4957ba498dfa3f4faf3d49f1f7ad57df6d7`.
- `references/integration-examples.md`: local `5c671b54c8cb44a71d948a3327d5676624ca476a2cf0c8c37189925041c75f35`; Bossku `5c671b54c8cb44a71d948a3327d5676624ca476a2cf0c8c37189925041c75f35`.
- `references/option-interactions.md`: local `3a982049ca18311d6db81a2c1d5cdd2bdeefe31ec9477c2d3ef0aa62cd5e7b28`; Bossku `3a982049ca18311d6db81a2c1d5cdd2bdeefe31ec9477c2d3ef0aa62cd5e7b28`.
- `scripts/detect-env.sh`: local `25a749fe23d97f784a38045e8c72bdf5ff27002c4ef5a3d35f508ea7e269e264`; Bossku `25a749fe23d97f784a38045e8c72bdf5ff27002c4ef5a3d35f508ea7e269e264`.
- `scripts/hybrid-health.sh`: local `9613194850b449715328e58586d9442bfae7994cfb125944b737bfff83822a5a`; Bossku `9613194850b449715328e58586d9442bfae7994cfb125944b737bfff83822a5a`.
- `scripts/quick-eval.py`: local `81ac6c78c70a4618a67295744bfd301b5df373d95e80c7379e09b743bcbaad36`; Bossku `81ac6c78c70a4618a67295744bfd301b5df373d95e80c7379e09b743bcbaad36`.
- `scripts/verify-json.py`: local `f2c622c93f584ba656d50d7b46cb587fad1edaaefea5b99e80065f80b5b8b43f`; Bossku `f2c622c93f584ba656d50d7b46cb587fad1edaaefea5b99e80065f80b5b8b43f`.

### karpathy-guidelines
Local `1` files; Bossku `0` files. Content changes after line-ending normalization: none. Local-only: SKILL.md. Bossku-only: none.

- `SKILL.md`: local `e2553e9b66299fbca399804d6c44dfa44b2384b979ca5bf8b933b4916bb3141b`; Bossku `absent`.

