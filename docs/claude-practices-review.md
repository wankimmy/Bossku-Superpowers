# Claude Code practices and Hindsight coverage review

Reviewed on 2026-09-29. Scope: apply the practical guidance and relevant gaps, not import every external library cataloged in the README.

## Sources and evidence

- Claude Code course checkout: [`shanraisshan/claude-code-best-practice`](https://github.com/shanraisshan/claude-code-best-practice/tree/7722ef772764ed3b99503305afc6d90918b9fef7).
- Hindsight checkout: [`vectorize-io/hindsight`](https://github.com/vectorize-io/hindsight/tree/ccfe85b4851957ac2adf88b4a9ddf9668b2882f1).
- BosskuAI baseline: `141a984`; existing skill names and packs checked against `skills/`, `skills/vendored.json`, and `bossku/index.py`.
- Version-sensitive Claude behavior was checked against the primary [skills](https://code.claude.com/docs/en/skills), [memory](https://code.claude.com/docs/en/memory), and [subagent](https://code.claude.com/docs/en/sub-agents) docs. Do not treat course version badges or feature counts as compatibility guarantees.

The source collection is large. These short extracts anchor the analysis:

1. Course `README.md:507`: “Read this repo as a course, not as a workflow or skill.”
2. Course `README.md:287`: “build a Gotchas section in every skill”.
3. Course `README.md:288`: “skill description field is a trigger, not a summary”.
4. Course `README.md:323`: “invest in product verification”.
5. Hindsight `skills/hindsight-docs/references/best-practices.md`, Memory Banks: “All operations (retain, recall, reflect) target a single bank.”
6. The same file, Taxonomy: reflect “searches memory, synthesizes an answer”.
7. Course `best-practice/claude-subagents.md:27`: “Maximum number of agentic turns before the subagent stops”.
8. Course `best-practice/claude-subagents.md:25`: “default: `inherit`”.

Quotes 1–4 justify improving the existing skills and adding observed product verification rather than installing a course wholesale. Quotes 5–6 justify explicit bank isolation and distinguishing generated synthesis from verified evidence.

## All nine README skill tips

Source: course `README.md:280–292`. “Applied” here means actionable guidance exists in the checked-in BosskuAI surfaces; it does not mean every host supports or automatically executes every feature.

| Tip | BosskuAI application | State |
|---|---|---|
| `context: fork` isolation | Practice playbook explains task boundaries, outputs, budget, and Claude-only support | Conditional on host/task |
| Skills in monorepo subfolders | Setup and instruction-management skills inspect launch directory and discovery; playbook describes scope | Applied |
| Skills are folders; progressive disclosure | Creator/checklist require portable sidecars; existing installer copies support files | Applied |
| Gotchas and failure points | Creator, stocktake, setup, management, and new skills include specific failure checks; existing specific Guardrails remain valid | Applied without modifying vendored text |
| Description is a trigger | Existing curated index plus creator guidance and routing regressions | Applied |
| Omit obvious advice | Creator and stocktake ask for useful behavioral deltas, not general tutorials | Applied |
| Goals and constraints over railroading | Creator and practice playbook distinguish invariants from implementation judgment | Applied |
| Scripts and libraries for reuse | Creator/checklist verify helper prerequisites, side effects, and installed sidecars | Applied |
| Dynamic `!` shell context | Playbook covers execution, shell/OS checks, and read-only use; portable explicit tools remain the default | Conditional, no automatic command injection |

The adjacent README hook/measurement tips are also covered: deterministic enforcement belongs in supported permissions/hooks; static `bossku skills audit` is distinguished from actual host usage. New capture or enforcement hooks are not installed as a side effect of this review.

## All nine skill categories from Thariq's guide

Source: `tips/claude-thariq-tips-17-mar-26.md`. These are example jobs, not a requirement to install every illustrative skill name.

| Category / illustrative examples | Existing or added BosskuAI coverage |
|---|---|
| Library/API reference (`billing-lib`, `internal-platform-cli`, `frontend-design`) | `bosskuai-documentation-lookup`, framework skills, `mcp-server-patterns`, frontend design skills |
| Product verification (`signup-flow-driver`, `checkout-verifier`, `tmux-cli-driver`) | New `bosskuai-product-verification`, existing `bosskuai-browser-automation` and `e2e-testing` |
| Data fetching/analysis (`funnel-query`, `cohort-compare`, `grafana`) | `analytics`, `bosskuai-analytics-metrics`, `bosskuai-observability-sre` |
| Business/team automation (`standup-post`, ticket creation, weekly recap) | `bosskuai-github-workflow`, `bosskuai-operations`; delivery supports summaries; messaging still needs authorization |
| Scaffolding/templates (new workflow, migration, app) | `bosskuai-rapid-prototype`, framework skills, `database-migrations` |
| Code quality/review (`adversarial-review`, style/testing practices) | `bosskuai-rigorous-code-review`, `bosskuai-coding-best-practices`, testing skills |
| CI/CD/deployment (`babysit-pr`, deploy, cherry-pick) | `bosskuai-github-workflow`, `bosskuai-ci-cd-pipelines`, `ci-triage`, deployment skills |
| Runbooks (debugging, on-call, log correlation) | `bosskuai-diagnose-loop`, `bosskuai-incident-response`, `bosskuai-observability-sre` |
| Infrastructure operations (orphan resources, dependencies, costs) | `bosskuai-devops-iac`, `dependency-triage`, `bosskuai-cost-optimization` |

These mappings establish workflow coverage, not identical implementation of the source author's example tools or project-specific services. No new generic synonym skills were added for those examples.

## README usage and other guidance

| README concern | Applied surface / boundary |
|---|---|
| Prompting, specs, gated planning | Existing `bosskuai-grill-with-docs`, planning and Superpowers skills; delivery goals are observable |
| Context/session management | Existing context-budget, handoff, continuation, Headroom skills; delivery now re-plans after invalidated assumptions |
| `CLAUDE.md` / rules | Actual loaded context including imports, ancestor/nested scope, live imports, specific repeated corrections |
| Agents / commands / skills | Practice playbook separates entry points, isolated work, full-body skill preloading, and supported invocation controls |
| Hooks / deterministic settings | Existing hooks remain; setup distinguishes prompt guidance from permission enforcement and warns that `allowed-tools` is not a sandbox |
| Product workflow / `/go` pattern | Delivery links observed verification; review and publication remain scoped to the user's authorization, rather than a new unconditional auto-ship command |
| Git/PR review, debugging | Existing GitHub workflow, diagnosis, review, and cross-model skills; no new provider routing |
| Utilities/daily use, custom sounds | Host/user preferences rather than portable repo requirements; no sound, notification, subscription, or account configuration |
| Advanced features | Document supported host/version before using agent teams, scheduling, computer use, long-running loops, or other optional features |
| Measuring usage and reducing prompts | Static audit versus actual usage is explicit; recommend narrow reviewed permission rules rather than broad bypass |
| Fixed “context rot” percentages / throughput claims | Treated as source-author heuristics; no universal numeric thresholds or performance claims added |

## Concrete course demo skills

Checked the course's `.claude/skills/` folders as well as the README.

| Skill / example | Decision |
|---|---|
| `weather-fetcher`, `weather-svg-creator`, `/weather-orchestrator` | Weather demo of command → agent → skill; apply the orchestration pattern to delivery and verification, do not add weather-specific defaults |
| `time-skill` | Use host-provided time tooling or ordinary date commands; not a missing recurring BosskuAI job |
| `agent-browser` | Existing `browser-use`, `remote-browser`, and browser-automation coverage; runtime/tool availability checked per task |
| `presentation-structure`, `presentation-styling`, `vibe-to-agentic-framework` | Course-specific presentation content; not portable engineering defaults or automatically installed Office tooling |
| Built-in `/code-review`, `/batch`, `/simplify`, `/run`, `/verify` | Host-provided features; discover availability before using, never claim bundled in BosskuAI |
| `/techdebt`, context-dump/analytics commands, `/careful`, `/freeze`, `/less-permission-prompts` | Illustrative or host-specific workflows; covered by maintenance, data-analysis, permissions, and scoped-hook guidance without globally installing a duplicate command |

## External workflow and skill catalogs

README sections Development Workflows, Cross-Model Workflows, Skill Collections, and Agent Collections were inventoried. A catalog entry is not an install instruction (quote 1); the user chose practical guidance and relevant gaps.

| Entries | Verified coverage / decision |
|---|---|
| Superpowers | Existing vendored pack in `skills/vendored.json` |
| Everything Claude Code | Existing curated `ecc` subset and Bossku first-party adaptations; not the full upstream catalog |
| Matt Pocock Skills | Relevant interview/docs, TDD, and architecture jobs covered by first-party skills; upstream library not vendored wholesale |
| Spec Kit, gstack, OpenSpec, Get Shit Done, BMAD-METHOD, oh-my-claudecode, Compound Engineering, HumanLayer, addyosmani/agent-skills | Alternative methodologies; apply research/plan/implement/verify principles through existing process/delivery skills, no competing stack installed |
| musistudio/claude-code-router, CLIProxyAPI, codex-plugin-cc, pal-mcp-server | Provider/cross-model integrations, not missing portable skills; existing cross-model guidance checks configured capabilities |
| anthropics/skills, Understand-Anything, scientific-agent-skills, wshobson/agents, awesome-agent-skills, impeccable, alirezarezvani/claude-skills, draw-json-architecture-skill | Reference collections; relevant generic jobs covered, domain-specific catalogs not imported or claimed installed |
| agency-agents, awesome-claude-code-subagents | Alternative agent catalogs; preserve BosskuAI's five contracts rather than adding hundreds of overlapping agents |

## Hindsight analysis and application

Hindsight is a memory service with model-driven extraction and synthesis, not just a directory of Markdown skills. Its README and five `skills/` entries were inventoried: `hindsight-docs`, `hindsight-local`, `hindsight-cloud`, `hindsight-self-hosted`, and `hindsight-architect`.

| Upstream feature | BosskuAI application |
|---|---|
| Retain / recall / reflect | New `bosskuai-hindsight-memory` distinguishes ingestion, evidence retrieval, and generated reasoning |
| Isolated memory banks | Explicit project/audience bank; tags cannot substitute for access isolation |
| Missions and durable observations | Playbook favors verified decisions/outcomes, contradiction handling, and provenance before promotion |
| Rich transcript ingestion and automatic hooks | Intentionally replaced with approved redacted curated notes; existing Bossku sync does not capture conversations |
| Local/cloud/self-hosted skills that set up providers | One guarded first-party workflow checks an existing CLI/MCP connection; no automatic installation or credential prompts |
| Documentation/architect skills | Narrow reference playbook with pinned sources; no huge generated documentation bundle added to every host |
| Async retain / derived mental models | Separate accepted versus searchable state; audit support and freshness before relying on synthesis |
| Service unavailable | Configured Markdown memory remains usable when its storage is available; report the Hindsight runtime gap explicitly |

This applies the reusable memory workflow and provides integration instructions for configured Hindsight. It does **not** deploy the service, install the upstream automatic-capture plugin, or claim live Hindsight behavior was tested.

## Confirmed activation fix

At the baseline, `claude_imports_agents_md("```markdown\n@AGENTS.md\n```\n")` returned true; `init_project` also treated any mention of the import as activation. Claude's primary memory docs state that import parsing skips code spans and fences.

The shared bare-import predicate now ignores fenced/inline/indented examples. `init`, repository validation, and doctor agree on whether the adapter is present. Regression tests exercise repair, preservation, idempotency, fence characters/lengths, and a live import after a closed example.

## Portable guidance follow-up, 2026-10-01

The supplied course checkout still matches the pinned revision above (`git rev-parse HEAD`; clean `git status --short`). This follow-up closes inconsistencies in BosskuAI's existing adaptation:

- The practice playbook now resolves canonical memory through `bossku memory-path`, preserving the configured Obsidian vault and reporting an unavailable vault without repository fallback.
- Delegation now uses bounded tasks and inherited models (quotes 7 and 8), explicitly checks context and skill preloading, and assigns exclusive file ownership or supported isolation. OpenCode/OMP use the same contract with capability discovery and a sequential fallback; host-specific schemas remain conditional.
- Skill evaluations include named skills, paraphrases, negated requests, mixed concerns, installed-profile limits, complementary coverage, and excluded overlaps. Selection evidence remains separate from artifact quality and actual host execution.

These are portable guidance changes. Live host discovery, fork execution, and real prompt-to-artifact behavior require separate checks; coverage of a source practice is not a universal compatibility or quality guarantee.

## Verification and limits, 2026-09-29

- Generated `skills/skill-index.json` from the actual skills and curated triggers; repository validation passed.
- Full unittest suite passed: 85 tests, including routing, context-budget, and activation regressions.
- Core and full install/init/doctor CLI smoke checks passed in isolated temporary homes/projects; confirmed live import repair, instruction preservation, repeat-run idempotency, and full-profile installation of both new skills and playbooks.
- Host-specific behavior such as Claude fork execution, live product browser journeys, and a live Hindsight backend must be verified when those runtimes are available; static skill and routing tests do not establish those results.

See the [implementation plan](superpowers/plans/2026-09-29-claude-practices-hindsight.md), [practice playbook](../references/playbooks/claude-code-practices-playbook.md), and [Hindsight playbook](../references/playbooks/hindsight-memory-playbook.md).
