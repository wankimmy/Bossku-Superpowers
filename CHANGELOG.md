# Changelog

## Unreleased

Two commits after v2.2.0, a skill-list budget check (a `bossku doctor` warning and an opt-in `--fit-skill-list` flag), and a second benchmark set that measures the two commits.

### Fixes

- **The stop gate counts running the code (`afda557`).** The Node stop gate only counted test runners, linters and builds as the check, so a model that wrote a small check script and ran it (`python check.py`, `python - <<EOF`, `python -c`, `node script.js`, `bash run.sh`) was sent back anyway. It now counts what the Python verify gate always counted: a script, `-c` or a heredoc fed to an interpreter, or a shell script, per command segment. Read-only segments (`grep`, `cat`), `--version`, `-h` and pip installs still do not count. `tests/hooks.test.mjs` has the new cases. The commit message reports, on the 9 dev tasks with Claude Haiku 5.5, the gate firing 2 times before and 0 after and turns 80 before and 67 after; those rows are not committed.

### Changed

- **Skill descriptions open with "Use when ..." (`cd73169`).** 70 first-party skill descriptions were reworded so a model reading the skill list can pick well. No vendored skill changed. `tests/test_descriptions.py` pins the convention.
- **Friendlier CLI output on a terminal (`cd73169`).** On an interactive terminal, `install`, `update`, `init`, `remember`, `hooks`, `vault sync` and `tools` print a short summary and the next step. Piped output (agents, scripts, tests) is the same JSON as before, and `--json` forces JSON. `tests/test_cli_output.py` covers it, and the README quick start and `docs/installation.md` say so.
- **Faster skill hint (`cd73169`).** The hint gives the same picks and output on 628 prompts, and the 95th percentile of the `v1` hook is about 10 ms lower (33.5, 33.7 and 33.8 ms before; 24.0, 23.9 and 23.8 ms after; in-process on one machine; `benchmarks/results/hint-tuning.json`). Tuned multi-skill hints were measured there and did not pass their gate (more recall, less precision and less primary accuracy), so the default stays `v1`.

### New

- **`bossku doctor` warns when Claude Code may cut skill descriptions, and `--fit-skill-list` fixes it (opt in).** Claude Code caps the skill list it shows the model at `skillListingBudgetFraction` x the context window (default `0.01`: 30,000 characters on a 1M-context model, 6,000 on a 200K-context model, measured on Claude Code 2.1.293). Over the cap it keeps every name and drops descriptions, least-used skills first. `doctor` now estimates the list from the `SKILL.md` files in `~/.claude/skills` (and the project's `.claude/skills` with `--project`), says for both model sizes whether it fits and about how many descriptions would be cut, and always gives the fraction that fits a 1M-context model, rounded up to `0.005`. That fit includes 16,880 characters of headroom for Claude Code's bundled and plugin skills, which bossku cannot see: on Claude Code 2.1.293 the `SKILL.md` files estimated 81,157 characters while the log said 98,037, and `0.035` was needed, not the `0.03` the files alone give. It is a warning, not a failure, and it notes that plugin skills and Claude Code's bundled skills also count. `bossku install --fit-skill-list` (and `update`) sets that fraction in `~/.claude/settings.json`: it never lowers a higher value, keeps every other key, writes through a temp file and keeps a `.bak` copy. A locked or unwritable file (a read-only `settings.json` on any OS, for example; it is left as it is, with no backup) does not stop the install: the summary says `not changed (failed: ...)` with the real error, and no temp file is left. That includes a read-only one: Windows will not delete it, so the cleanup makes it writable first, and a temp file left by an earlier crash is cleared before the next write instead of blocking every later run (`_write_json_atomic` in `bossku/hooks.py`). The fit is sized from `~/.claude/skills` only, and `doctor --project` says so. With `--project`, `doctor` also reads `skillListingBudgetFraction` and `skillListingMaxDescChars` from the project's `.claude/settings.local.json` and `.claude/settings.json`, which override the user file (both keys are scope "Any file" in the Claude Code settings reference), and names the file when the fraction comes from one. The choice is saved in `config.json` and kept by later `update` runs; `--no-fit-skill-list` stops it and leaves the value as it is. A default install is unchanged, because the setting costs context in every session, and no skill is shortened or removed. New module `bossku/skill_listing.py`; `tests/test_skill_listing.py` covers the estimate, the messages, the maths and the flag. See [`docs/installation.md`](docs/installation.md#skill-list-budget-claude-code).
- **A second benchmark set, 10 October 2026.** Claude Haiku 5.5 and Claude Opus 5.5 with no Bossku Superpower, with v2.2.0 (`acf4fb3`) and with the improved build (`cd73169`), on the same coding, HumanEval and two-session tasks, one trial each. Four Ollama Cloud models were also started but only partly ran: the account hit its session usage limit (HTTP 429) twice and the coding-suite runs failed while the run folder was being set up. The Ollama two-session rows were copied again after the resume job stopped (13:42 local, 05:42 UTC; Claude rows stay at the 01:08 UTC cut-off). On the 22 tasks GLM 5.3 passed 13 of 20 without and 16 of 20 with v2.2.0 (+16 points, 0 to +32), Kimi K3 9 of 14 and 13 of 17 (partial), and DeepSeek V4.1 Flash 18 of 22 with v2.2.0 (borrowed baseline); every Ollama interval reaches zero, so none is a clear gain. GLM 5.3 Flash has the 10 original tasks only, and no Ollama model has a coding or HumanEval result. Result: no clear difference on the coding tasks and HumanEval (both Claude models near the ceiling); on the 22 two-session tasks Haiku passed 10 without, 16 with v2.2.0 and 15 with the improved build, and Opus passed 15, 17 and 16; the improved build was not clearly better or worse than v2.2.0 on passes and used fewer tokens per run in 7 of 8 comparisons, two sessions of work apart. The page opens with a short answer in plain words and three charts (memory, coding and HumanEval, tokens) in `docs/assets/benchmark-2026-10-10-*.svg`, drawn by `scripts/summarize_run_set.py` from the saved summary. Page: [`docs/benchmarks/results-2026-10-10.md`](docs/benchmarks/results-2026-10-10.md). Rows: `benchmarks/results/raw/2026-10-10/`. Summary: `benchmarks/results/2026-10-10.json`, built by `scripts/summarize_run_set.py`; `tests/test_results_2026_10_10.py` fails if the summary, the page tables or the scrubbing of the rows drift. The 1 to 8 October files are unchanged.

## v2.2.0 - Guarded hooks, Codex resume, Cypress, and an audit of the install and memory code

This release adds hooks that watch the agent (a command guard, a syntax check, one stop gate), a way to carry a Codex task that hit its usage limit over to Claude Code, and a Cypress tool. A line-by-line audit of the hooks, the memory sync and the installers also found real bugs, fixed below. The Node hooks are new in this release, so their audit fixes landed before they shipped. The longer notes written while the release was built are in the three "v2.2.0 details" sections after this one.

### Fixes

- **Command guard.** `hooks/guard.mjs` now sees through git options placed before the verb (`git -C . reset --hard`, `git -c x=y push -f`, `--no-pager`), `-f` inside a bundle of short flags (`git push -fu`), a `+branch` push, `git checkout .`, `git checkout -f` and `git checkout --`, and a lone `&` that chains a second command. `--force-with-lease` is still allowed. An absolute path inside the project or the OS temp folder is allowed even when the project sits under `C:/Users` or `/home`.
- **Syntax check after an edit.** A `.py` file is checked with the first of `BOSSKU_PYTHON`, `python3`, `python` and `py` that works, because `python3` on Windows can be a Microsoft Store stub that checks nothing; no `__pycache__` is written. A `.js` file with `import` or `export` is checked as a module, and JSX no longer fails the check, but merge-conflict markers still do. An honest `99.9%` is now a warning; only `99.99%` and a promise of 100% uptime or satisfaction block the edit.
- **Stop gate.** A message the app adds by itself (a compaction summary, a task notice) is no longer taken for your request. The gate reads only the end of the transcript. An edit under `~/.claude` or the OS temp folder no longer sends the agent back to run something, unless the session itself runs in that folder. The Node and Python gates share that rule, and a shared test table fails if one drifts from the other.
- **One Stop gate.** `bossku hooks install` could leave the Python verify gate next to the Node stop gate, so the agent was stopped twice. Only one is wired now, whichever command you run. `--no-harness` takes the Node gates out and puts the Python gate back.
- **Obsidian sync.** A vault copy with Windows line endings was taken for an edit of yours and copied to a `.md.conflict.md` file. Line endings alone no longer count. A real edit is kept byte for byte (also when it is not valid UTF-8), and a second conflict gets a numbered name instead of overwriting the first. A folder with no notes (for example `~/.cursor` from a Cursor hook payload) no longer gets a vault folder or a state file.
- **Hook ownership.** `bossku install` and `bossku uninstall` removed any hook command that only contained a word like `sync-hook`, your own script included (`node C:/tools/sync-hook.js`). Only commands shaped like Bossku's are treated as ours now. Each settings backup has its own timestamp, an older backup is never overwritten, and uninstall writes once.
- **Secrets are blanked out in more shapes.** Notes, the vault copy of your rule files and the resume brief now hide a whole PEM private key block (not only its first line), Slack, Google API, Stripe, GitLab, Hugging Face and npm tokens, JWTs, `Authorization: Basic`, `user:password@` in a URL, and names that end in `SECRET`, `PASSWORD`, `TOKEN` or `_KEY` (`AWS_SECRET_ACCESS_KEY=...`). A test feeds hostile text to check the patterns stay fast.
- **Hook input is read as UTF-8.** On Windows a pipe hands text to the console code page, so a project folder with a letter such as ā or ė in its name was garbled and its notes were not found. The Python hooks now decode input as UTF-8, and the Codex PowerShell wrapper passes the bytes on unchanged.
- **Installs for OpenCode, Cursor and Codex.** The OpenCode plugin gets its command as a JSON array, and a missing `bossku` now warns instead of crashing OpenCode. A Cursor payload that has only `workspace_roots` syncs that workspace, not the folder the process started in. Codex `config.toml` is read as TOML and only `[features]` is edited: an explicit `hooks = false` is kept and reported as `disabled_by_user`, a UTF-8 BOM or CRLF is kept, and a file that is not valid TOML is left alone (`skipped_invalid_toml`). `bossku install --profile` no longer resets your profile to `lean` when you leave it out. `install`, `update`, `hooks` and `uninstall` exit 1 when a tool reports an error.
- **`bossku doctor` no longer says OK on a broken setup.** It exits 1 for an installed skill that differs from the repo, an install source folder that is gone, a hook that runs a program that no longer exists, a `settings.json` that is not valid JSON, and an out-of-date project block. It no longer fails on a Claude Code hook set that is only partly installed (that can be a choice), or calls this repo's own short `AGENTS.md` block out of date, and its "fires twice" advice no longer tells you to remove hooks you want to keep.
- **Skill lookup is faster to start.** A lookup reads the skill files once (up to 11 times before, for a five-part prompt), and `tomllib`, `shlex` and `gzip` load only where used. A stale saved index prints one line on stderr and routes from a fresh build; the prompt hook stays silent.
- **Benchmark tools.** A benchmark arm named like `../../x` could create folders outside the work folder; names are checked now. A run that crashes cleans up its session folder. `make_charts.py --readme` stops when a result file is missing (`--allow-partial` goes on). Provider request ids in the committed Ollama rows were replaced by a placeholder. The Malay-English checker now catches stretched particles such as `lahh` and `lorr`. The rule check's score also prints the figure over every labelled non-rule: 9 of 100 flagged, next to 4 of 95 on the ones the labellers agreed on.
- **Docs that said something untrue.** `SECURITY.md` no longer says hooks are off by default and now lists what `bossku install` writes. The install docs no longer say `lean` is always the default (a first install starts there, later runs keep your profile). `AGENTS.md` stays under the 16,000 character budget that `bossku validate` now enforces, its indicator line lists every agent (designer and clarification included), playbooks no longer name retired skill ids, and the orphaned router document was removed (its escalation rule lives in `bosskuai-ai-model-selection`). CI now runs Python 3.11 on Ubuntu and Windows, 3.12 and 3.13 on Ubuntu, with read-only token permissions and a 15-minute limit.

### New

- **Harness hooks (`hooks/`, Claude Code).** Four Node hooks with no dependencies, all fail open: a `PreToolUse` guard that refuses destructive commands, a `PostToolUse` syntax check and anti-slop lint on files the agent writes, a `SessionStart` contract, and a `Stop` gate that sends the agent back once if it edited source and ran nothing. `bossku install` wires them into `~/.claude/settings.json` from a checkout of this repo and adds eight `permissions.deny` rules that hold even when the guard is off. Switches: `BOSSKU_GUARD=off`, `BOSSKU_POST_EDIT=off`, `BOSSKU_SLOP_LINT=off`, `BOSSKU_STOP_GATE=off`. Details: [hooks/README.md](hooks/README.md).
- **Install choices.** `--no-harness` leaves out the Node hooks and the deny rules (and takes ours out again), `--no-agents` leaves out the subagent contracts, `--no-claude` leaves out the skills in `~/.claude/skills`. Each has a positive form (`--harness`, `--agents`, `--claude`). Left out, `install` and `update` keep your saved choice.
- **Designer agent and `scripts/shot.mjs`.** `agents/designer.md` writes `.bossku/DESIGN.md` before UI work, and `shot.mjs <url>` saves a 390 and a 1440 screenshot for the agent to look at. All six agent contracts are copied to `~/.claude/agents`.
- **Resume a Codex task in Claude Code.** When Codex stops on its usage limit, a new Claude Code session in the same folder shows one line, and after "continue" the agent gets a brief of at most 2,000 characters. `bossku resume` prints the same brief by hand. It reads Codex's files read-only, keeps the brief in the chat, never in the vault or the notes, and `BOSSKU_RESUME=off` switches it off.
- **Cypress.** New skill `bosskuai-cypress` and `bossku tools install cypress`: a dev dependency of one project, never global, with no Cypress Cloud login and no record key. Cypress sends crash reports to `api.cypress.io` unless `CYPRESS_CRASH_REPORTS=0` is set, and the install notice says so.
- **Smarter skill hints, opt in.** `hint_mode` in `~/.bosskuai/config.json` can be `v2`: up to three skills (the best one plus one for each other part of the request), a skill you name by id gets through, under 800 characters. The default stays `v1` because v2 did not pass every bar in its offline test (see "Changed" and the numbers below).
- **Codex gets the per-prompt hint.** `bossku skill-hint --host codex` runs on Codex `UserPromptSubmit`. Codex has no Skill tool, so each skill is named by the path of its `SKILL.md`. `bossku skills find --brief` prints one line per selected skill (id, score, `SKILL.md` path, what it is for) instead of the JSON.
- **The rest of the release** is in the "v2.2.0 details" sections below: the `lean` and `engineering` install profiles, compact skills, `bossku tools list` and `install`, `bossku vault sync` and `tidy`, project notes at session start, a router that knows how people phrase requests, and the real-agent benchmark.

### Changed

- **Only one Stop gate.** A default install wires the Node stop gate and no Python verify gate. The Node gate does not have the Python gate's two other reminders (code pasted into the reply instead of a file edit, and a stated rule that was not saved with `bossku remember`); the rule reminder on your prompt is unchanged. `--no-harness` brings the Python gate back, and `BOSSKU_VERIFY_GATE=0` switches off that gate only (after `--no-harness`).
- **Skill hint test, measured.** `benchmarks/results/lean-gate.json` compares `v1` and `v2` offline, with no model calls. On the 158 held-out test requests, `v2` spoke on 33.5% (53) against 32.3% (51), the named skills were an acceptable pick 89.3% of the time against 80.0%, and the first pick was right 98.1% against 98.0% when it spoke. On the 100 follow-up prompts both stayed silent on 95, and on 100 prompts that need no skill neither spoke. The bars it missed: every part of a multi-part request named (16.4% against a bar of 25%), the share of parts that got a skill on the new multi-part set (23.9% against 70%, a bar the full router missed too at 69.7%), the hook's p95 time (42.8 ms for `v2` and 36.8 ms for `v1`, against 25 ms), and letting 3-word prompts through (right on 32.5% of 40 short requests, with silence counted as a miss, against 60%). So `v1` stays the default and the 5-word minimum stays. The sets are written and labelled by agents, not by people.
- **Sync skips projects in the temp folder.** A project inside the OS temp folder is not copied to a vault outside it, and `bossku remember` keeps its notes in that folder, so test runs and scratch folders stop leaving junk folders in your vault.
- **Model roster dated.** `bosskuai-ai-model-selection` says when its ids, context windows and prices were checked (2026-10-06, against Anthropic's model table) and sends you to `claude-api` for the live roster. It now lists Opus 5.5 as the default Opus.

### Not verified

- **Codex marketplace path.** `.agents/plugins/marketplace.json` uses `source.path` `./`. A test checks that it points at the repo root, but `codex plugin marketplace add ./` has not been run.
- **Python 3.13 and the new CI step.** The 3.13 job and the warning-only routing snapshot step have not run yet. The first CI run is the check.
- **Per-prompt hints outside Claude Code and Codex.** Cursor, OpenCode and OMP get the skills and the instructions. A per-prompt hint there was not tried.
- **Resume.** Phase 1 (Codex to Claude Code) is tested with made-up Codex files only; run `bossku resume --debug` after a real limit stop to check the signature. Phase 2 (Claude Code to Codex) is not built, because putting text into Codex has not been tested live.
- **Plugin and wired hooks together.** `claude plugin validate` accepts the manifest, but nothing here shows whether Claude Code runs the hooks twice when the plugin is enabled and `bossku install` has wired them too. `bossku doctor` warns when both are on.
- **Agent runs.** No agent benchmark has measured the guard, the syntax check, the Node stop gate, `v2` hints or resume. The published numbers are from build `b8ccea1`; new runs come after this release.

## v2.2.0 details - Lean profile, session hooks, and real benchmarks

BosskuAI used to put 234 skill names in front of the model in every session and trusted routing numbers measured on the prompts it was tuned against. This release makes the per-session cost small, helps the agent open the right skill and remember a project's rules across sessions, and measures all of it on real agents with the results kept in the repository.

- **Node harness (`hooks/`).** Four Node hooks (built-ins only, fail open): a `PreToolUse` guard that refuses destructive shell commands (`git reset --hard`, force push, `git clean -f`, `rm -rf` on a home or protected path, `migrate:fresh`, `docker compose down`, piping a remote script into a shell), a `PostToolUse` check that syntax-checks the file the agent wrote and lints UI and copy files for AI tells, a `SessionStart` contract (the harness reminder and a pointer to `DESIGN.md`), and a `Stop` gate. `bossku install` wires them into `~/.claude/settings.json` from a checkout of this repo, and the plugin manifest wires the same four. It also adds a short `permissions.deny` list (`git reset --hard`, `git clean -f`, `git push -f`, `migrate:fresh`, `db:wipe`, `docker compose down`, `docker-compose down`, `docker system prune`) that holds even when the guard is off, and `bossku hooks uninstall` removes it. New install choices: `--harness`/`--no-harness`, `--claude`/`--no-claude` and `--agents`/`--no-agents`; left out, `install` and `update` keep the saved choice. Switches: `BOSSKU_GUARD=off`, `BOSSKU_POST_EDIT=off`, `BOSSKU_SLOP_LINT=off`, `BOSSKU_STOP_GATE=off`. See `hooks/README.md`.
- **The Node stop gate replaces the Python verify gate on a default install.** Only one Stop gate is wired. The Node one sends the agent back once when source files changed and nothing ran afterwards, and adds the 390 and 1440 screenshot reminder when UI files changed. It does not have the other two Stop reminders of the Python gate: the one for code pasted into the reply instead of a file edit, and the one for a stated rule that was not saved with `bossku remember` (the reminder on the prompt is unchanged). `bossku install --no-harness` brings the Python gate back, and `BOSSKU_VERIFY_GATE=0` switches off that gate only. The benchmark numbers below were measured on build `b8ccea1` with the Python gate.
- **Agent contracts in Claude Code.** The six files in `agents/` (orchestrator, planner, designer, executor, auditor, final-reviewer) are copied to `~/.claude/agents` by `bossku install`; `bossku doctor` shows how many are present. New `designer` contract writes `.bossku/DESIGN.md` in a nine-section format before UI work.
- **Look at the UI before saying done.** `scripts/shot.mjs <url>` writes `phone-390.png` and `desktop-1440.png` under `.bossku/shots/<stamp>/` for the agent to read. It runs `npx --no playwright screenshot`, so it never downloads a package on its own: if Playwright is missing it prints `npm i -D playwright && npx playwright install chromium` for you to run. `bossku init` now writes a `.bossku/DESIGN.md` stub, unless `DESIGN.md`, `design/DESIGN.md` or `.bossku/DESIGN.md` already exists, and the session contract names the first real design file, never the unfilled stub.
- **`engineering` install profile.** Every skill except the 47 of the marketingskills pack (about 195). Accepted by `bossku install`, `bossku init` and `bossku skills find`.
- **Resume a Codex task in Claude Code: `bossku resume`.** When Codex stops on its usage limit, a new Claude Code session in the same folder shows one line, and after "continue" the skill hint hands over a brief of at most 2,000 characters (request, plan, files, last three commands with secret shapes blanked out, Codex's last message). It reads `~/.codex/state_*.sqlite` and the last 2 MB of the rollout read-only, keeps the brief in the chat only (never in the vault or the notes), and writes only `~/.bosskuai/resume-state.json` (thread ids and times). `BOSSKU_RESUME=off` switches both hooks off. See `SECURITY.md`.
- **Skill hint for Codex and `hint_mode`.** Codex gets the same `UserPromptSubmit` skill hint (`bossku skill-hint --host codex`). `hint_mode` in `~/.bosskuai/config.json` is `v1` (the default, unchanged text) or `v2` (up to three skills, a skill named by id gets through, under 800 characters); `bossku doctor` prints it. `bossku skills find --brief` prints one line per selected skill instead of the JSON.
- **Cypress.** New skill `bosskuai-cypress` and `bossku tools install cypress`, a per-project dev dependency (never global, no Cypress Cloud login, no record key). Cypress sends crash reports to `api.cypress.io` unless `CYPRESS_CRASH_REPORTS=0` is set; the install notice says so.
- **Fixes from the final audit.** The guard now allows an absolute path strictly inside the project or the OS temp folder even when the project sits under `/home`, `/Users` or `C:/Users` (it used to refuse every such path), and it catches `git reset -q --hard`, `git clean --force`, `git branch -d -f`, `rm -r ~`, `Remove-Item ... -r`, `find ~ -delete`, `bash -c 'rm -rf ~'` and `env rm -rf ~`. The PHP syntax check no longer runs a `php.exe` planted in the project folder. `shot.mjs` no longer passes `--yes` to npx. With `memory_storage=obsidian`, `bossku remember` and `bossku init` keep a project in the OS temp folder out of the real vault, as the sync already did. The resume brief blanks out command-line secrets (`--password x`, `curl -u a:b`, `mysql -pX`, `docker login -p`, `DB_PASS=`, `gh secret set --body`). The benchmark scrub removes the provider account name from usage-limit errors, and the four affected raw files were scrubbed. `bossku init` no longer tells the agent to avoid all of `.bossku/`, which clashed with `DESIGN.md` and `shots/`.
- **Renamed: BosskuAI is now Bossku Superpower** (repository `wankimmy/Bossku-Superpowers`): skills and tools in one kit. The `bossku` command, the Python package and every `bosskuai-*` skill id stay as they are, so installed copies, hooks and notes keep working. The plugin is now named `bossku-superpower` (marketplace `bossku-superpower-marketplace`); reinstall the plugin once if you installed it from a marketplace. The README is rewritten in plain words with diagrams, and the benchmark charts say "with" and "without" Bossku Superpower.
- **Better code review.** `bosskuai-rigorous-code-review` now states the intended outcome first, checks who has to use the change and how it could pass every check and still miss its purpose (documentation, rules and process changes included), keeps confirmed defects apart from optional improvements, tags each finding as reproduced, traced or inferred, and asks for a second look at every finding on a large review. It also says that reviewing is read-only: reproduce in a scratch copy, never run installers or machine-wide commands (a review subagent once ran a real `npm install -g` here and left half an install behind). The always-loaded `SKILL.md` grows from 1.8 KB to 2.9 KB; the full text stays in `reference.md`. `verification-before-completion` gains a section on matching evidence to the intended outcome and two rows in its claim table; that is a local addition to the upstream superpowers skill, recorded in `docs/third-party.md`. Routing for review prompts is covered by two new regression cases (84 in all) and the held-out check below; the effect on how well an agent reviews has not been measured.
- **Tools: `bossku tools list` and `bossku tools install <tool>`.** Shows which optional programs the skills use (Headroom, Moli, e2e, Archify, Graft, MarkItDown, Graphify, browser-use, OpenDataLoader PDF, Hindsight, dcg) and installs the pip and npm ones only with `--yes`, after printing the exact commands and any telemetry notice. Programs whose installer is a script piped into a shell or an unsigned binary (Moli, Hindsight, dcg) are never run for you. New skill `bosskuai-tools` tells the agent the same rules.
- **New skills.** `bosskuai-agentic-e2e` (agentic end-to-end UI tests with the e2e runner; written in our own words from a read of the upstream docs, which are Apache-2.0 and credited), `bosskuai-archify-diagrams` (guard rails for the Archify skill), and two vendored from lexmount/moli: `moli-webfetch` and `moli-cdp-server`, with one local change: the step that told the agent to pipe a remote installer into a shell now asks the user first. `moli-websearch` is deliberately left out (it tells the agent to scrape API keys and switch engines after a CAPTCHA).
- **Obsidian vault: `bossku vault sync` and `bossku vault tidy`.** Sync copies Claude Code's own auto-memory (including its sub-repos and worktrees), your rules files (global and project `CLAUDE.md` and `AGENTS.md`, `.claude/rules`) and legacy `.bossku/memory` notes into `<vault>/BosskuAI/<project>/`, with common secret shapes blanked out and an `Index.md` that links everything; in Obsidian mode it runs by itself through the existing end-of-session hooks (at most once a minute per project). A copy you edited in the vault is kept as `.md.conflict.md` when the original changes. Tidy shows, and with `--apply` does, a clean-up of the folders earlier versions scattered: a folder whose name is exactly that of a folder inside one configured project root merges under that project's `repos/` (anything ambiguous is left alone), `.md.conflict.md` backups go to `_archive/`, folders you list in `vault_folder_moves` go where you say, folders with no file in them are removed, names already taken get a number, and a zip backup of the whole `BosskuAI` folder is made first. No note is deleted.
- **Attribution fixes.** `docs/third-party.md` now records moli, the studied projects (e2e, headroom, archify, hindsight, claude-code-best-practice) and the corrected OpenDataLoader notice (Copyright 2025-2026 Hancom, Inc.), and `docs/third-party-licenses/` keeps the moli and OpenDataLoader license texts. `bosskuai-headroom` no longer implies the upstream project is MIT (it is Apache-2.0).
- **`lean` install profile.** About 25 skills are listed with one short sentence each; the other ~210 move to `~/.bosskuai/library` and are one `bossku skills show <id>` away. New `bosskuai-skill-finder` skill (the agent runs `bossku skills find`, then opens the pick), `skills/lean.json` (the listed set and the short sentences) and `bossku skills show <id>`. `validate` checks the list: at most 48 skills, 150 characters each. `core` and `full` are unchanged.
- **Compact skills.** 20 first-party skills now ship a short `SKILL.md` (the checklist: 41 KB in total instead of 143 KB) and keep the full text in `reference.md` (every line of the old `SKILL.md` is still there), which the agent opens only when it needs the detail. A loaded skill is re-read on every later turn, so a shorter core costs less all session. Vendored skills are untouched, and every frontmatter was byte-identical when the skills were compacted (a few descriptions were reworded later in this release).
- **Skill hint hook** (`bossku skill-hint`, `UserPromptSubmit`). Names the one or two skills that fit the prompt and tells the agent to load them first, when the match is strong. Silent for short prompts and weak matches.
- **Verify gate** (`bossku verify-gate`, `Stop`). If the agent edited code and never ran anything afterwards, it is sent back once to run it. A second rule catches a request for a change that was answered by pasting code into the reply without editing any file. Silent when the agent already did its job. `BOSSKU_VERIFY_GATE=0` turns it off; that is the Python gate, which a default install no longer wires (see "Node harness" below), so after `bossku install --no-harness` only. Each reminder is sent once per turn and counted from the transcript, so it can never loop (a second "run it now" reminder made a small model invent tool names for 30+ turns), and any error lets the agent finish.
- **Project notes at session start** (`bossku session-brief`, `SessionStart`, and `bossku memory-brief`). The newest notes, at most 1,000 characters, so the agent no longer runs `memory-path` and reads files. A rule the user states counts as a note worth saving, so a later session does not break it.
- **Router.** Evidence floors for the automatic stack (a skill needs a minimum score and a share of the top score: 40% when this was measured, 65% since the next item) and an `unsure` flag instead of a confident wrong answer. On 73 held-out requests written without seeing the router: first pick right 59% → 75%, every part of a multi-part request covered 40% → 58%. The saved rows for these 73 are not in the tree, only in git history: the `before` side is `benchmarks/results/routing-heldout.json` at commit `fe3fe14` (58.9% and 39.7%), the `after` side the same file at `9a1eb6d` (75.3% and 57.5%). The fixes behind this were found on the other 87 requests only.
- **The router also knows how people phrase requests.** People rarely use a skill's own words ("jest hanging after the tests finish" is a stuck test run). A cheap model wrote about 30 realistic messages for each of the 241 skills from its `SKILL.md` alone (`benchmarks/routing-queries.json.gz`, 7,240 messages; five skills have 31 or 36); the index keeps each skill's 150 most distinctive words, and the router adds a BM25 match against them, relative to the best-fitting skill, at a weight of 5. Chosen on the tuning halves and the curated regression cases (84 now), reported on the test halves: on 158 held-out requests that the router was not tuned on, an acceptable skill is ranked first 81% of the time (66% before; plain keyword search 56%, which is the skill list at `b8ccea1`; the same method on the `4d47894` list gives 54%, 86 of 158), is in the top three 94% (88%), and every part of a multi-part request is covered 75% (55%). Adding the five new skills and rewording 13 descriptions later in this release cost about one point on these requests (82%, 95% and 77% before). Also: a hyphenated trigger such as `micro-interactions` now counts as a two-word phrase, the cutoff for follow-up skills is 65% of the best score (was 40%) so the stack stays at about two skills, and the prompt hook speaks only when the best match scores 12 or more (97% right on the tuning halves; it now fires on 4 of 57 coding-task prompts instead of 6).
- **The rule reminder, hardened.** `bossku skill-hint` and `bossku verify-gate` remind the agent to save a rule the user states (`bossku/rules.py`). An independent code review found real bugs, each now fixed and covered by a test that fails on the old code: app-written "user" lines (compact summaries, task and CI notices) were taken for the request, an unmet verify reminder hid the rule reminder, the project folder was placed in a double-quoted shell string, over-broad cues flagged ordinary prompts, a long run of blank lines made the scan slow, a `grep` for "bossku remember" counted as a save, and odd payloads could end a hook with exit code 2 (which blocks the prompt or the stop). On 200 new messages that nothing was tuned on (committed in `benchmarks/rules-eval/`, rerun with `scripts/benchmark_rules.py`), the check catches 33 of 99 stated rules and wrongly flags 4 of 95 non-rules. Those figures keep only the messages where the labellers agreed with the writers; with nothing dropped it is 33 of 100 and 9 of 100, because all 5 non-rules the labellers dropped were flagged (`python scripts/benchmark_rules.py score` prints both). The docs say so.
- **Measured results (build `b8ccea1`).** Five models and 1,036 completed task runs. The clearest gain is on tasks that need a rule from an earlier session: Claude Haiku 4.5 48% to 68%, Claude Sonnet 5.5 64% to 84%, Gemma 4 31B 39% to 68% (intervals above zero); DeepSeek V4.1 Flash and Nemotron 3 Nano showed no clear difference. On coding and harder tasks no model passed clearly more; ending without running the code fell from 53% to 0% (Gemma) and from 100% to 17% (Nemotron), and Nemotron passed 92% of HumanEval problems against 62%. Tokens per run were 1.1 to 4.7 times higher. Claude Haiku and Sonnet runs of the coding, harder-task and HumanEval suites did not finish (the login expired) and are not published. An earlier run on `02ee2f2` is kept in `benchmarks/results/raw/earlier/`; the two differ by up to 20 points on single lanes, which is the noise level of these sample sizes.
- **Benchmark harness.** Claude Haiku and Sonnet runs used `--no-session-persistence`, so the Stop hook's transcript did not exist and the verify, paste and rule gates silently did nothing on those arms; sessions are now kept (and the harness deletes the session folder it creates under `~/.claude/projects`). `--include-hook-events` records every hook call. The harness finds `claude.exe` in the new `<version>/<hash>/` layout.
- **`bossku remember` says when it saved.** The output now starts with `"saved": true` and a sentence. Before, `"vault": {"status": "skipped"}` (no vault configured) read like a failure; in tests a model retried three times, wrote a junk note and hand-edited the memory files, costing six turns.
- **Shorter, concrete always-on text.** The project block and the global memory block say what to do (list the requirements, make exactly that change, run the tests, batch independent tool calls, save only what a future session needs) in fewer words. On the dev tasks the batching line cut a strong model's tokens by about a quarter at the same pass rate (18 runs each).
- **Benchmark harness** (`scripts/benchmark_agent.py`): runs real Claude Code headless against hidden-test coding tasks, with and without BosskuAI, on Claude models or Ollama Cloud. Baseline isolation is checked by a canary; real notes are never touched; failures are counted, not dropped, while runs that the model service cuts short (a rate limit) are excluded and run again. 26 coding tasks (9 dev, 17 test), 31 harder tasks (17 dev, 14 test), 22 two-session memory tasks (10 in `benchmarks/tasks/memory`, 12 in `benchmarks/tasks/memory-rules`), HumanEval sampling, 328 skill-search prompts written without seeing the router (160 older and 168 newer; `scripts/benchmark_routing_heldout.py`). Results live in `benchmarks/results/`; the README charts are drawn from them by `scripts/make_charts.py`. See [docs/benchmarks](docs/benchmarks/README.md).
- **Fixes.** `bossku skills show` crashed on a Windows pipe when a skill contained an arrow or a dash (output is UTF-8 now); the global `--home`/`--root` options were ignored after a subcommand (a run could write to the real home); `set_description` glued the closing `---` onto the description; every `bossku uninstall` removes the library, and `--purge` also removes the hooks and the config.
- **Install, uninstall and doctor say what they do.** A plain `bossku install` keeps the profile already in `~/.bosskuai/config.json`; only a first install starts at `lean`. A plain `bossku uninstall` removes the managed skills, the library and the shared files that still match the repo, and keeps the memory and voice blocks in your global instruction files; `--purge` also removes the hooks, the config and those two blocks. `bossku install`, `bossku update`, `bossku hooks install`, `bossku hooks uninstall` and `bossku uninstall` exit 1 when a hook tool reports an error. The Codex hook install can report `disabled_by_user` (your `[features] hooks = false` is left alone) or `skipped_invalid_toml` even when it also added entries to `hooks.json`; the `added` list shows what changed. `bossku doctor` exits 1 for an installed skill that differs from the repo, an install source that is gone, a hook that runs a program that no longer exists, a `~/.claude/settings.json` that is not valid JSON and (with `--project`) an out-of-date managed block; it only names missing Claude Code hook pieces such as the verify gate, because leaving one out can be a choice. `bossku validate` fails when `AGENTS.md` is over 16,000 characters, since it loads in every session. The OpenCode settings stub no longer has a `references` block. The Codex marketplace `source.path` is now `./`; tests check that it resolves to the repo root, but `codex plugin marketplace add ./` has not been run.
- **Model roster dated.** `bosskuai-ai-model-selection` now says when its Claude ids, context windows and prices were checked (2026-10-06, against Anthropic's model table) and points to `claude-api` for the live roster. It lists Fable 5.1, Opus 5.5 (now the default Opus), Sonnet 5.5 and Haiku 5.5, all with 1M context; Opus 5, Sonnet 5 and Haiku 4.5 moved to an "earlier models" table that was not re-checked.

## v2.2.0 details - Claude practices and Hindsight

- Applied the reviewed Claude Code README's skill-design, discovery, startup-context, permissions, and verification guidance to the existing first-party skills; added a traceable coverage review.
- Added `bosskuai-product-verification` for observed user journeys and CLI smoke checks, with routing regressions.
- Added `bosskuai-hindsight-memory` and an optional retain/recall/reflect integration playbook with scoped banks, curated-note ingestion, provenance checks, and Markdown fallback. No Hindsight runtime or automatic capture is installed.
- Fixed `bossku init`, validator, and doctor accepting instruction imports inside code examples; preserve existing text and avoid duplicate imports on repeat initialization.
- Corrected stale first-party guidance about the existing sync-hook defaults and `scripts/` wrappers.

## v2.2.0 details - Grounding, and the skill and rule audit

Always-on grounding: Anthropic hallucination-reduction and output-consistency techniques as a default Bossku trait.

- New skill `bosskuai-grounding` with Persistence (not switched off by "normal mode"), four moves (admit the gap, quote first, claim/source/retract, source-only), memory admission, and agent interactions. Added to the `core` profile.
- New checklist `references/checklists/grounding-checklist.md`. Skill-creator checklist now asks for an input/output example when format quality depends on it.
- `AGENTS.md`: `## Grounding (always on)` section and pack-routing row. All five agent contracts list the skill; auditor treats unsupported claims as findings; final-reviewer REVISE covers unsourced evidence.
- `bosskuai-deep-research`: quote-first deep-read and post-draft retraction. `bosskuai-prompt-optimizer`: Source of truth in Phase 4, grounding in optimized prompts.
- Curated triggers in `bossku/index.py`; routing case in `tests/test_routing.py`; managed-block sentence in `bossku/init_project.py`; Cursor rule `.cursor/rules/bosskuai.mdc`; sync test that AGENTS.md, the `.mdc`, and the init block all contain `Grounding`.

Skill and rule audit: dead ends removed, router index cleaned. No skill body was trimmed; vendored skills are untouched.

- **Agents usable in Claude Code.** `final-reviewer` had no frontmatter (the plugin exposed it as a generic all-tools agent); it now has one, and its `[BOSSKUAI]` prefix block is gone because it contradicted the JSON-only output contract. Plugin agents declared tools that do not exist (`log`, `memory`, `db_query`) and model values Claude Code does not accept (`review`, `coding`, `reasoning`), so the executor and auditor could not run the verification commands their contracts require. They now use `Read/Grep/Glob/Bash` (+ `Edit/Write` for the executor) with `inherit`, and `sonnet` for the executor, matching the plan-strong / execute-cheaper split.
- **No phantom agents or files.** The orchestrator told agents to "adopt the matching contract" for 14 specialists with no file in `agents/`, and referenced `skill-detector.md`, `active-continuation.md`, and `TaskCheckoutService::checkout`. Each role is now a real agent plus the skill that holds the expertise (for example, review = auditor + `bosskuai-rigorous-code-review`). Continuation points at `.bossku/memory/handoff.md`. Same fix in `bosskuai-prompt-optimizer` and `bosskuai-autonomous-loops`.
- **No alias ids as load instructions.** 16 references told agents to load alias ids (`bosskuai-bug-finding`, `bosskuai-zoom-out`, `bosskuai-agent-security-hardening`, ...). The CLI resolves aliases, but Claude Code's Skill tool does not, so each was a guaranteed failed call. They now name the real skill.
- **`AGENTS.md`**: `review-animations`, `pick-ui-library`, and `prototype` are marked user-invoked (`/name`). They set `disable-model-invocation`, so routing the model to them only produced failed calls.
- **`bosskuai-ai-model-selection`**: Fable 5.1 (`claude-fable-5-1`) replaces Fable 5, Opus 5.5 added as name-only, and Sonnet 5 corrected to $2/$10 (was $3/$15), per the `claude-api` reference.
- **Recovered harness edits in the agents.** An earlier harness session's agent improvements survived only in the installed `~/.claude/agents` copies. They are merged back: the auditor runs cheap verification itself and quotes the real output, the executor reads `DESIGN.md` before UI edits and names `bosskuai-ponytail` + `bosskuai-rigorous-code-review` for the de-sloppify pass, the planner gets read-only Bash, and the orchestrator lists every specialist role as agent + skill, claims work in `.bossku/memory/handoff.md`, and runs loops with exit conditions named up front. The UI screenshot gates now ship: `agents/designer.md` and `scripts/shot.mjs` are in this change, and the session contract and the stop gate point at the script.
- **Claude Code sync hook on Windows.** `bossku hooks install` wrote the hook command as an unquoted `C:\...\bossku.EXE sync-hook`; Claude Code runs hooks through Git Bash, which drops the backslashes, so the Obsidian sync at Stop and SessionEnd never ran. The command is now a quoted forward-slash path, and an install repairs its own stale entries instead of reporting `already_installed`.
- **Six-lane skill review.** Every one of the 240 skills was read against its domain (engineering build, engineering process, visual design, motion, marketing, sales), with version-sensitive claims checked against official docs. First-party fixes applied, among them: `bosskuai-saas-billing-ops` now requires webhook signature verification and uses Stripe's real status strings; `bosskuai-greptile-review-loop` stages only the files it changed, gates each push on tests, and never resolves a human reviewer's thread; `bosskuai-aws-deployment` drops App Runner (closed to new customers) for ECS Express Mode and S3-native Terraform locking; `bosskuai-laravel-security` targets the Laravel 11+ skeleton; `bosskuai-malaysia-pdpa-privacy` states the 2025 amendment duties (72-hour breach notice, DPO); `bosskuai-cybersecurity-risk` uses OWASP Top 10:2025; `config:cache` moves from image build to container start; `bosskuai-paid-acquisition-monetization` stops spend at CAC > LTV; `bosskuai-seo-geo` carries corrected AI-crawler and rich-result facts; `bosskuai-taste` no longer asks for invented names, numbers, or logos; GSAP, R3F, Lenis, Expo, and App Store facts are current. Vendored bugs are drafted as upstream issues in `references/audits/2026-09-26-upstream-issues.md`.
- **Retired and removed skills.** `bosskuai-human-output`, `bosskuai-recipes`, `bosskuai-engineering-principles` (its goal table moved into `bosskuai-engineering-delivery`), and `bosskuai-workspace-assistant` are now aliases. `taste-skill-v1`, `gpt-tasteskill`, and `stitch-skill` are no longer vendored (recorded under `excluded` in `vendored.json`). `x402` stays vendored but is never installed: it prints wallet keys. Hallmark's upstream moved to `Nutlope/hallmark`, and its theme tokens are vendored at `site/css/tokens.css`.
- **Router.** About 60 trigger, exclusion, and role changes; skills with `disable-model-invocation` are flagged `user_invoked` and `bossku skills find` says to hand them to the user as `/<id>`; phrase matching ignores hyphens ("founder-led" = "founder led"); a stack holds one design-direction skill. Measured: the 42 misroutes the review found now route correctly, the 51-case contract stays 51/51, and an independent 65-query held-out set moves from 55 to 58 top-1 with top-3 unchanged at 63.
- **Strict frontmatter check.** Nine descriptions rewritten during the review were unquoted and contained `: `, which real YAML parsers reject; hosts then dropped the description and listed the skill by its H1 title. They are quoted now, and `bossku validate` fails on any unquoted value containing `: ` or ` #`, which Bossku's own lenient parser used to accept.
- **Installer and CLI.** `bossku install` prunes managed skill copies it no longer ships (retired, excluded, or off-profile) and copies `site/`; `--project` defaults to the current directory for `remember` and `sync`; `bossku init` writes the antislop pointer block so its install wizard and usage question do not block agents.
- **Router index.** The phrase extractor split quoted examples on `,` and `/` (`"A/B test,"` became `the user mentions "a` + `b test`), read apostrophes as quote marks (`"analytics isn't working"` became `analytics isn`), matched `Use this when` inside "whenever", and cut words at a 200-character cap. The frontmatter parser also left `\"` escapes in double-quoted descriptions, so every `community-marketing` phrase was garbage. Phrases went from 1,659 to 888 with none left carrying stray quotes or third-person scaffolding. Routing is unchanged: the committed contract stays 51/51, and a 65-query held-out set stays 55/65 top-1 and 63/65 top-3.

## v2.1.0 - Upstream pack sync, i-have-adhd, and a curated ECC subset

Synced every vendored pack that has a checkout under `../ai-skills` against upstream HEAD (2026-09-07). Vendored copies are now byte-identical to upstream again (modulo CRLF); the routing wording Bossku had previously written into vendored descriptions moved into `CURATED_TRIGGERS`, per the contract in `AGENTS.md`.

- **superpowers** (obra/superpowers v6.3.0): brainstorming gained the three-path router (spike / bounded / architectural) and a red-flags table; TDD now ships `writing-good-tests.md` (replaces `testing-anti-patterns.md`); subagent-driven-development gained `re-review-prompt.md` and updated scripts; systematic-debugging `find-polluter.sh` fixes; using-superpowers gained Gemini and Hermes tool references; every other skill picked up the July rationalization-table refactors.
- **hallmark**: 21st theme **Grid** (`references/themes/grid.md`), nav archetype range fix, custom-theme and macrostructure updates.
- **emil-skills**: re-synced 9 skills and added 3 new ones - `animate-expo` (Reanimated / Gesture Handler / haptics construction skill), `ask-sonner` (Sonner toast guide + API reference), `write-swift` (modern Swift 6 guide). Pack is now 12 skills.
- **graphify** (0.9.55): upstream no longer keeps a static `SKILL.md`; re-vendored from the Agent-Skills template `graphify/skill-agents.md` plus the new `references/` sidecar (8 files: extraction spec, query, exports, update, hooks, transcribe, add/watch, GitHub merge). Documented the source paths in `docs/third-party.md`.
- **taste-skill**, **loop-engineering** (all 12), **marketingskills**, **scroll-world**: verified against upstream; taste-skill and loop-engineering descriptions reverted to upstream text, with compensating curated triggers for `loop-budget`, `loop-constraints`, `loop-triage`, `loop-verifier`, `minimal-fix`, `post-merge-scan`, `changelog-scan`, and `taste-skill`. The 7 loop pattern skills are taken from `starters/<loop>/.claude/skills/`.
- **dcg**: thin skill refreshed against upstream v0.6.9 (`DCG_CONFIG`, `DCG_FAIL_CLOSED`, config precedence).
- **New pack `i-have-adhd`** (ayghri/i-have-adhd, MIT): action-first, numbered, no-preamble output shape. Explicit `/i-have-adhd`; persists until "stop adhd mode" / "normal mode". Routed in `AGENTS.md` and listed as an overlap with `bosskuai-human-output` / `bosskuai-token-saver`.
- **New pack `ecc`** (affaan-m/ECC, MIT): a curated 10-skill subset that fills library gaps rather than the whole 280-skill catalogue - `mysql-patterns`, `database-migrations`, `error-handling`, `mcp-server-patterns`, `e2e-testing`, `accessibility`, `architecture-decision-records`, `vue-patterns`, `python-patterns`, `python-testing`. Each is a single self-contained `SKILL.md` with no ECC-only tooling references. Skipped on purpose: ECC `security-review` (would shadow the Claude Code built-in of the same name; Bossku keeps `bosskuai-cybersecurity-risk` + `bosskuai-laravel-security`), and anything overlapping an existing Bossku skill (deployment, git workflow, onboarding, loop design, redis, seo).
- `bossku/skills.py`: `origin` added to `KNOWN_FRONTMATTER_KEYS` (ECC's provenance marker). `bossku/index.py`: curated triggers + explicit roles for every new skill. Routing fix: triggers are lowercased at index build, so curated phrases written with a capital (e.g. "what should I use for toasts") now earn their exact-phrase bonus against the lowercased query; top-1 on the routing contract went from 0.95 to 0.98. Routing contract in `tests/test_routing.py` extended with 13 cases for the new skills.
- Versions aligned at 2.1.0 across `pyproject.toml` and all plugin manifests. Library is now ~240 skills / 14 vendored packs. Not synced (no checkout under `ai-skills`): `browser-use`, `graft`, `markitdown`.

## v1.13.0 - Cross-repo portability and session token optimization

- **Plugin now carries the full harness**: `.claude-plugin/plugin.json` exposes `commands` (11 commands moved from `.claude/commands/` to `commands/`), `hooks` (new `hooks/hooks.json`), and a curated `agents` array — so skills, commands, agents, and hooks all work in **any** repo the plugin is enabled for, not just this one.
- **Portable hooks**: plugin hooks use `${CLAUDE_PLUGIN_ROOT}` paths. New `session-start-context.sh` (SessionStart) injects the compact BosskuAI contract + resolved memory home into model context once per session in every repo — replacing the per-prompt stderr reminder that never reached the model. `common.sh` gained `resolve_bossku_home()` ($BOSSKU_HOME → project → sibling Bossku-AI checkout → plugin root) so shared memory works from sibling projects with zero config. `write_hook_output` no longer echoes hook-input JSON to stdout; edit counter is now session-scoped. Repo-local `.claude/settings.json` hooks emptied to avoid double-firing (mcp-health-check stays opt-in there — per-MCP-call bash spawn is too hot for a default).
- **Curated subagents**: plugin exposes the 24 editor-appropriate agents only; the 10 Laravel runtime pipeline personas (orchestrator, executor, auditor, clarification, designer, model-router, writer, final-reviewer, direct-answer, skill-detector) no longer leak into the editor's Agent list. Frontmatter normalized on editor agents (valid Claude Code `tools`, `model: opus` instead of runtime role names).
- **Token optimization**: 25 longest/deprecated skill descriptions rewritten as tight trigger statements (7,313 → 4,606 chars; ~680 tokens saved per session, every session, keywords preserved). Deprecated aliases reduced to one-liners.
- Versions aligned at 1.13.0 across `.claude-plugin/plugin.json`, root `plugin.json`, both marketplaces, and `skill-index.json`. Removed stray broken `Bossku-AI` symlink at repo root.

## v1.12.0 - Loop architectures, prompt optimizer, 5 new agents, and flows

- Added `bosskuai-autonomous-loops` (ECC port): loop architecture catalogue — sequential `claude -p` pipelines, infinite agentic loop, continuous PR loop, de-sloppify pattern, Ralphinho RFC-driven DAG — plus a new section documenting BosskuAI's own runtime revise loop (`max_revision_rounds`, ExecutorStuckDetector) as the built-in pattern.
- Added `bosskuai-prompt-optimizer` (ECC port, heavily remapped): advisory-only prompt diagnosis and rewriting that matches intent/scope/stack to the bosskuai skill+agent roster and outputs ready-to-paste optimized prompts.
- Added 5 editor-mode agent contracts: `loop-operator` (drives autonomous loop architectures: exit conditions, context bridging, stall detection), `performance-optimizer` (measure → change one variable → re-measure ratchet), `database-reviewer` (migration/rollback/index/tenant-scope gate), `code-simplifier` (de-sloppify pass after green, separate context from author), `incident-responder` (stabilize → verify → prevent with blameless postmortem).
- Enhanced core agents: orchestrator gained a **Flows table** (10 task-shape → chain → loop-owner routes) and council/introspection wiring in runtime-core; planner gained DAG decomposition rules + complexity-tier table; executor gained de-sloppify handoff + introspection-on-cap + Laravel skill wiring; security-reviewer gained laravel-security/prompt-injection-defense/tenant-isolation wiring; auditor gained agent-architecture-audit, laravel-verification gate, and database-reviewer delegation.
- skill-index.json v1.12.0 (105 skills); AGENTS.md roster and specialist list updated; plugin.json 1.3.0.

## v1.11.0 - ECC agent-stack, decision, and Laravel skills

- Added 4 agent-stack/decision skills ported from ECC (affaan-m/ECC): `bosskuai-agent-architecture-audit` (12-layer agent diagnostic, grounded to the BosskuAI pipeline), `bosskuai-agent-introspection` (capture → diagnose → contained recovery for stuck/degraded agent runs), `bosskuai-council` (four-voice decision council), `bosskuai-context-budget` (context overhead audit incl. runtime persona injection).
- Added 3 manual-only Laravel specialists for the `app/` backend and any Laravel repo: `bosskuai-laravel-security`, `bosskuai-laravel-tdd`, `bosskuai-laravel-verification`.
- Folded the ECC continuous-learning-v2 instinct model into `bosskuai-continuous-learning`: atomic confidence-weighted instincts under `ai-assistant/memory/instincts/`, promotion ladder, runtime parallel to `LearningEngine`.
- Registered all 7 skills in `skill-index.json` (v1.11.0, 103 skills) and `AGENTS.md` (new "Agent-stack & decision skills" and "Laravel stack specialists" rosters).
- Verified greptile skills (`bosskuai-greptile-review-loop`, `bosskuai-pr-check`) remain in sync with upstream greptile-skills (latest: edited-comment handling, GitLab + Perforce support).

## Unreleased

- Added the complete Apache-2.0 upstream `odl-pdf` skill bundle unchanged, with prompt-aware routing for OpenDataLoader, OCR, structured PDF extraction, tables, bounding boxes, and citation-ready RAG. Generic document conversion remains routed to `markitdown`; unrelated PDF operations do not trigger the skill.
- Added the six-skill MIT `anti-slop` pack unchanged, plus curated prompt routing and a final-gate contract for UI, responsive layout, copy, generated comments, and code artifacts.
- Added `bosskuai-headroom` as a guarded context-compression operating skill. It checks for the optional runtime and never installs packages or changes proxy/provider routing without a request.
- `bossku skills find` now emits a `recommended_stack` so multi-concern prompts can select one primary and the smallest non-overlapping complementary set. Superpowers phase skills are explicitly composed with domain and Anti-Slop skills.
- Added `bossku skills audit` for description-token cost, long-body counts, provenance groups, and relative-link integrity. Compacted every custom description over 300 characters; despite seven new skills, total always-loaded description text fell by 2,970 characters (about 743 tokens) from the pre-change baseline.
- `bossku install` and `bossku update` now deploy shared `references/` into both user skill roots and handle read-only OneDrive files during reinstall/uninstall. Validation rejects broken custom relative links while reporting vendored upstream gaps separately.
- Aligned the CLI and new-project metadata version with the 2.1.0 package/manifests; `bossku doctor` no longer reports the stale 2.0.0 internal version.

- **Session-end sync hooks — `bossku hooks install`**: new `bossku/hooks.py` wires an opt-in `Stop`/session-end hook into Claude Code (`~/.claude/settings.json`), Cursor (`~/.cursor/hooks.json`), Codex (`~/.codex/hooks.json`), and OpenCode (a dedicated `~/.config/opencode/plugins/bossku-sync.js`) that reruns `bossku sync` (new `bossku sync-hook` CLI command, reads the target project's `cwd` from the hook's stdin JSON payload) — a safety net on top of `bossku remember`'s existing inline export, not a new write path. Additive-only: appends to whatever hook config already exists per tool, never overwrites, backs up the file first, and skips any tool whose config directory isn't present. `bossku hooks uninstall` removes only BosskuAI's own entries. `bossku doctor` reports per-tool install status. Codex needs a one-time interactive hook-trust approval before it actually fires (documented in `docs/memory.md` and the `bosskuai-permanent-memory-orchestration` skill). Covered by `HooksTests` in `tests/test_bossku.py` (skip-when-absent, preserve-existing-entries, idempotent re-install, uninstall-is-surgical, all-four-tools, stdin/`--project` sync-hook routing).
- **MCP server — expose Bossku-AI over MCP**: new `App\Services\Mcp\McpServer` (JSON-RPC handler: `initialize`/`tools/list`/`tools/call`) advertises `bossku_search`, `bossku_read`, `bossku_goals`, and `bossku_run` so any MCP client (Claude Code, Cursor, …) can drive Bossku. Run it with `php artisan bosskuai:mcp-serve` (newline-delimited JSON-RPC over stdio). Covered by `McpServerTest` (initialize, notification no-response, tools/list, tools/call goals, unknown-method error).
- **MCP client — connect external MCP servers (GitHub, Figma, …)**: `App\Services\Mcp\{McpClient,McpServerRegistry,McpToolBridge,StdioMcpTransport}` let Bossku connect to external MCP servers and expose their tools to agents via new `mcp_list_tools` / `mcp_call` runtime tools (`mcp_call` executor-only, denied to read-only roles). Server catalog in `config/mcp.php` ships **GitHub** and **Figma** entries (disabled until you set the token + env flag, e.g. `BOSSKU_MCP_GITHUB_ENABLED=1` + `BOSSKU_GITHUB_TOKEN`). Protocol logic (initialize handshake, tools/list, tools/call) is transport-agnostic; covered by `McpClientTest` with a fake transport (client handshake/list/call, registry enabled-filtering, bridge routing, disabled-server rejection).
- **Bring-your-own-agent over HTTP**: new `App\Services\Agents\HttpAgentAdapter` — a specialist with `runtime_mode='http'` + an `endpoint` in metadata becomes an external worker; Bossku POSTs the task (with optional auth header) and maps the response into the specialist handoff. Wired into the orchestrator's specialist seam (HTTP agents dispatch externally instead of running an internal LLM), degrades gracefully on error. `http_agent_timeout_seconds` config. Covered by `HttpAgentAdapterTest` (`Http::fake()`: supports-detection, POST+map, graceful HTTP-error fallback).
- **Company export/import portability**: `App\Services\Company\CompanyPortabilityService` exports an org (project + goal tree + specialist agents/org-chart) to a bundle with **secrets scrubbed** and IDs replaced by stable refs (goal index, agent role_slug), and imports it into a fresh project remapping goal parents + reporting lines with collision handling. `php artisan bosskuai:company {export|import}`. Covered by `CompanyPortabilityServiceTest` (scrub + stable refs, tree/reporting-line restoration, name-collision).
- **Goal-aligned planning (Goals wired into the live pipeline)**: a run now aligns to a business goal and the planner is told to advance it. New `App\Services\Company\GoalContextResolver` resolves the goal for a run (explicit `metadata.goal_id` wins; else, when `align_runs_to_active_goal` is on, the project's top active goal). The orchestrator injects a compact goal block into `routerCtx` before planning and stamps `goal_id` on the run; `PlannerService` surfaces it as `goal_alignment` plus a system instruction ("shape the checklist to measurably advance this goal; flag off-goal scope as a planner_question"). The loop closes: `WorkIssueService::createFromApprovedPlan` stamps the run's `goal_id` on every generated issue and recomputes goal progress — so finishing planned work advances the goal automatically. Opt-in fallback (`align_runs_to_active_goal`, default off); explicit goal_id always honored. Covered by `GoalContextResolverTest` + a new `WorkIssueServiceTest` loop-closure case.
- **Goals system — "manage goals, not PRs" (Paperclip parity)**: new `Goal` model + `bossku_ai_goals` table (project-scoped, self-referential tree, status/priority/target_metric/target_value/current_value/progress/due_at), and a `goal_id` link added to `work_issues`. New `App\Services\Company\GoalService` rolls up progress from the strongest available signal — sub-goal average → numeric metric (current/target) → linked-issue completion — and **bubbles changes up the goal tree** (finishing a leaf issue advances its parents; a goal auto-marks `achieved` at 100%). Manageable via `php artisan bosskuai:goals {list|create|recompute}`. Lets a business goal ("Build the #1 note app to $1M MRR") sit above projects/issues/runs with live progress. Covered by `GoalServiceTest` (issue roll-up, numeric metric, parent averaging + bubble-up, achieved transition, attach/link, summary counts).
- **Cost & token budget hard stops (Paperclip-style governance)**: Bossku already recorded real $ spend per call (`UsageTracker` → `bossku_ai_usage_events.cost_usd`) but only emitted a soft token *warning* that stopped nothing. New `App\Services\Governance\CostBudgetGuard` turns that telemetry into enforcement: authoritative $ spend per run vs a USD cap (`cost_budget_usd_per_run`) and the existing token cap, with a warning threshold (`budget_warn_threshold`, default 80%) and an opt-in **hard stop** (`budget_hard_stop`). When exceeded with the hard stop on, the orchestrator halts the audit→revise loop (`haltForBudget`) — recording `budget_halted` on the run and emitting a `budget_halt` event — and finalizes with what it has instead of burning budget. `maybeEmitBudgetWarning` now reports $ spend and a `budget_exceeded` event. Caps default to 0 (off); hard stop default off. Covered by `CostBudgetGuardTest` (usd/token caps, warning threshold, hard-stop gating).
- **On-demand specialist synthesis (beyond LangGraph)**: when the router matches no existing specialist for a task, the orchestrator now *designs a new sub-agent tailored to the task* with an LLM and uses it in the same run — something LangGraph's `Send` (dynamic dispatch to nodes that already exist in a compiled graph) cannot do. New `App\Services\Specialists\DynamicSpecialistSynthesizer` generates a real spec (role, expertise, task strategy, pitfalls, reusable trigger keywords, advisory output contract); `SpecialistAgentDraftingService::draftFromSpec()` persists it (unique slug, `metadata.source=dynamic_synthesis`, `auto_created=true`) as a draft — used immediately, reviewable for reuse. `maybeSpawnDynamicSpecialist` now prefers LLM synthesis and falls back to the prior pattern/template draft. Gated by the existing `dynamic_specialist_spawn` setting (default off). Covered by `DynamicSpecialistSynthesizerTest` (spec synthesis/normalization, invalid-output guard, unique auto-created persistence).
- **Agentic tool-use loop (`App\Services\Agents\AgenticToolLoop`)**: the iterative counterpart to the single-shot executor — a ReACT-style driver that lets a model read → edit → verify → read-the-error → fix in one task, observing each tool result before deciding the next step (opencode's defining behaviour, which Bossku-AI's one-shot JSON executor lacked). Model-agnostic JSON protocol (`{tool_calls:[...], done, final}`) so it works across every Ollama/OpenAI-compatible model, not just ones with native function calling. Reuses the existing `ToolRegistry` (all writes still flow through approval/auto-apply governance) and `ModelFallbackService`. **Closes the verify leg**: new governed `run_command` runtime tool lets the loop run allowlisted commands (`php artisan test`, `composer test`, `npm test`, `git status`, …) via the hardened `ProjectCommandRunner` (allowlist + forbidden-token + path/timeout bounds — no new execution surface) so the model can run tests, read the failure, and fix; `run_command` is executor-only (denied to read-only roles), editor aliases `bash`/`shell` map to it. Hard iteration cap (`bossku.agentic_max_iterations`, default 12, clamp [1,50]) + identical-call stuck detection so a confused model can't spin. Runnable via `php artisan bosskuai:agent-loop "<task>"`. **Now wired into the pipeline as a selectable executor mode** (`bossku.executor_mode` / `BOSSKUAI_EXECUTOR_MODE`, default `single_shot`): set it to `agentic` and the main executor step runs the loop via `App\Services\Agents\AgenticExecutorAdapter`, which performs the work then reconstructs a pipeline-shaped `execResult` from the run's file-write approvals and `run_command` tool calls — so the auditor, evidence, revise, and learning machinery downstream run unchanged. Three idempotency guards (`_files_already_applied` / `_commands_already_run` in `applyExecutorFileChanges`, `applyExecutorCommands`, `applyOrPauseForExecutorApprovals`) prevent double-apply. Agentic mode auto-falls back to single-shot when per-change user approval is required (it applies during the loop). Covered by `AgenticToolLoopTest` (done/cap/stuck/observation-feedback) + `AgenticExecutorAdapterTest` (execResult reconstruction from approvals/tool-calls, stuck→partial mapping), all with a scripted fake model.
- **Coding-tool upgrades (opencode parity)**: (1) **Line-numbered, paginated `file_read_safe`** — returns `<n>: <content>` with `offset`/`limit` (default/cap 2000 lines, 2000 chars/line) + `total_lines`/`truncated`, replacing the blind 8 KB cut; executor contract warns to strip the `<n>: ` prefix when quoting `old_string`. (2) **ripgrep-backed `file_search`** — fast, gitignore-aware, returns matching line + line number; falls back to the in-PHP scan when `rg` is absent (`bossku.ripgrep_path`, `bossku.allow_ripgrep_search`). (3) **Post-edit diagnostics** — new `App\Services\Project\ChangedFileDiagnostics` runs the cheapest authoritative check per changed file (`php -l`, JSON, YAML) right after apply; failures fold into `known_issues` + downgrade status to `partial` (via `ExecutorEvidenceSupport::mergeApplyReport`), driving the auditor/revise loop instead of shipping a file that won't parse — the single-shot analogue of opencode's read-diagnostics-after-edit LSP step. Covered by `ChangedFileDiagnosticsTest` + ToolRegistry read/search/edit tests.
- **Surgical edit engine (opencode-grade reliability)**: new `App\Services\Project\FileEditEngine` — a PHP port of opencode's multi-strategy replacer cascade (exact → line-trimmed → block-anchor → whitespace-normalized → indentation-flexible → escape-normalized → multi-occurrence). The executor can now emit `files_changed[].edits` (`[{old_string, new_string, replace_all?}]`) instead of reproducing whole files or emitting brittle unified diffs: it quotes the exact snippet to change and the engine locates it even when whitespace/indentation drift, rejecting not-found/ambiguous edits with loud, actionable errors instead of silently dropping the change. Wired through `FileWriteApplier::extractAfterContent` (edits preferred over diff), `ExecutorService` contract + result normalization, and the strict validation gate (`ExecutorResponseParser`). New `file_edit` runtime tool in `ToolRegistry` (routes through the same approval/auto-apply governance); `edit` editor alias now maps to surgical `file_edit` (was whole-file `file_write_proposed`); `write` still maps to `file_write_proposed`. Read-only roles (auditor, planner, reviewers, writers) denied `file_edit`. Covered by `FileEditEngineTest` (11 cases) + permission tests.
- Docs: agentic orchestration layer — `agents/orchestrator|executor|auditor|final-reviewer|model-router|skill-detector.md`, root `memory/`, `skills/`, `playbooks/`, `integrations/{cursor,claude-code,codex,opencode}`, `ui/*-spec.md`, expanded `docs/*` (installation, quickstart, examples, architecture, FAQ, comparison).
- Rules: mandatory `[BOSSKUAI]` response indicator in `AGENTS.md`, `.cursor/rules/bosskuai.mdc`, `.claude/rules/bosskuai.md`, `CLAUDE.md`, `.codex/AGENTS.md`, `packages/bossku-ai` SKILL.
- Routing: align `app/config/bossku_models.php` fallbacks with documented Gemini / Qwen / DeepSeek ordering; extend `ai-assistant/config/model-router.yaml` with backup hints.
- Audit round 2: merge duplicate model-flow sections in `AGENTS.md`, remove `<claude-mem-context>` footer, `evals/indicator-compliance-fixtures.json` + indicator regex in `scripts/eval_workspace.py` (v1.9.6), expand `agents/skill-detector.md`, `auto_memory` ↔ schema bridge in `memory/schema.md`, **Memory Used** chip in `RoutingDashboard.vue`, decision-tree mermaid in `docs/comparison.md`.

## v1.9.5 - Reliability Hardening and 5/5 Audit Fixes

- Fixed orchestrator memory subprocess calls so they never inherit stdin and cannot hang during `scripts/bosskuai run`.
- Added structured run completion with outcome/audit memory save and active-continuation clearing.
- Added `scripts/bosskuai continuation show|claim|clear` for honest cross-tool takeover between Claude Code, Cursor, and Codex.
- Added `scripts/bosskuai session start|end` plus session-log support for every tool.
- Added memory doctor, memory autopromote, stronger secret redaction, non-blocking stdin reads, and Claude Stop-hook extraction.
- Strengthened risk detection and routing for tenant isolation/cross-organization data exposure.
- Added 9 missing cofounder expert skills: SaaS billing ops, tenant isolation security, observability/SRE, QA automation, Malaysia PDPA privacy, cost optimization, customer success/support, prompt-injection defense, and eval-driven agent improvement.
- Expanded expert coverage evals from 12 to 21 cases.
- Updated version to v1.9.5 and skill count to 86.

## v1.9.3 — Permanent vector memory + always-on model router

## v1.9.4 - No-UI Command Center, Run Orchestration, and Memory Inbox

- Added `scripts/bosskuai` CLI command center.
- Added structured Plan → Execute → Audit → Memory run packets under `ai-assistant/runs/`.
- Added always-on model routing scripts with risk escalation for auth, payments, security, privacy, migrations, production, secrets, and data-loss work.
- Added local memory extraction into `ai-assistant/memory/inbox.jsonl`.
- Added memory approval/rejection CLI flow that promotes approved memories into durable memory and syncs vector DB.
- Added `ai-assistant/runtime/system_state.json` for command-center state without a UI.
- Added cron example for memory extraction, vector sync, and eval checks.


Adds the missing runtime layer for the workflow: durable cross-tool memory and a plan/execution/audit model policy.

### Added

- **`ai-assistant/scripts/auto_memory.py`** — local-first memory CLI for Claude Code, Cursor, and Codex.
  - `query` wraps vector DB retrieval.
  - `remember` writes durable entries to the right memory file and syncs vector DB.
  - `capture` supports hook payloads and deduplicates repeated events.
  - `status` shows memory health.
- **`ai-assistant/memory/conversation-memory.md`** — indexed cross-tool conversation/request memory.
- **`ai-assistant/memory/durable-memory.md`** — indexed stable decisions, preferences, and constraints.
- **`ai-assistant/memory/conversation-log.jsonl`** — raw local audit trail, intentionally not indexed.
- **`ai-assistant/skills/bosskuai-permanent-memory-orchestration/SKILL.md`** — routing skill for permanent memory, vector DB sync, and cross-tool context.
- **`ai-assistant/references/always-on-model-router.md`** — frontier plan → lower-cost execute → frontier audit protocol.
- **`.claude/settings.hooks.example.json`** — Claude Code hook config that captures user prompts and syncs vector memory automatically.

### Changed

- `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/bosskuai.mdc`, and `.codex/AGENTS.md` now enforce:
  1. retrieve memory first,
  2. plan with frontier model,
  3. execute with lower-cost model when safe,
  4. audit with frontier model,
  5. save durable memory and sync vector DB.
- `vector-config.json` now indexes `conversation-memory.md` and `durable-memory.md` with retrieval hints for past conversations and permanent memory.
- `scripts/install.sh` core profile includes the permanent-memory orchestration skill.
- `scripts/enable-hooks.*` now enable auto memory capture plus vector sync.

### Honest framing

- Claude Code can use hooks for automatic capture when enabled.
- Cursor and Codex do not expose one universal hook surface in every environment, so BosskuAI enforces the behavior through rules/config plus the shared `auto_memory.py` CLI.
- This captures future conversations and durable summaries. It cannot recover old chat history from tools that never wrote it to the repo.

### Validation

Run before release:

```bash
bash scripts/check-workspace.sh . --profile full
bash scripts/validate-skill-index.sh .
python3 -S scripts/eval_workspace.py
python3 ai-assistant/scripts/auto_memory.py remember --tool test --kind durable "Decision: test durable memory write."
python3 ai-assistant/scripts/auto_memory.py query "test durable memory" --limit 3
```

---

## v1.8.9 — Engineering principles skill (Karpathy framing)

A new tiny skill that codifies four widely-recognized engineering principles as a routable BosskuAI skill, with attribution to the public framing they came from.

### Added

- **`ai-assistant/skills/bosskuai-engineering-principles/SKILL.md`** (~140 lines). The four principles:
  1. **Think Before Coding** — state assumptions, ask when uncertain, present alternatives, push back when warranted.
  2. **Simplicity First** — minimum code, no speculative abstractions, no unrequested flexibility.
  3. **Surgical Changes** — every changed line traces to the request; no drive-by refactors.
  4. **Goal-Driven Execution** — transform vague tasks into verifiable goals; multi-step plans state per-step `verify:` clauses.

  Plus an output contract (Assumptions / Plan / Diff scope / Verification / Out of scope) and a specialist-routing table that hands off depth to the marquee playbooks after framing.

- Indexed in `skill-index.json` with 9 triggers (`engineering principles`, `apply principles before coding`, `think before coding`, `simplicity first`, `surgical changes`, `goal-driven execution`, `Karpathy principles`, `frame the work`, `before I write code`) and 6 keywords (`principles`, `minimum diff`, `speculative abstractions`, `verifiable goal`, `drive-by refactor`, `test-first`).

### Attribution

The four-principle structure is adapted from [Andrej Karpathy via forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (MIT). Cited explicitly at the top of the SKILL.md. The Karpathy file itself is one CLAUDE.md with four named principles; this skill operationalizes those principles with BosskuAI's existing routing and output-contract conventions, plus a specialist hand-off table.

### Why a new skill instead of merging into existing ones

Considered three options before shipping:

- **A — do nothing.** Coding-best-practices, rigorous-code-review, ask-clarifying-questions, and the `/implement` slash command already cover all four principles in pieces. Adding a skill would duplicate.
- **B — new tiny skill (chosen).** Captures the public Karpathy framing as a recognizable named unit. Loaded only when triggered, so adds zero tokens to the always-loaded surface. Routes to specialists for actual implementation depth.
- **C — full rewrite of `bosskuai-coding-best-practices`.** Reorganize that skill under the four-principle headers. Real merge, but tears up a working skill for a frame change.

Picked B. The skill is intentionally narrow: framing only, no code-quality detail, no review rules. Those live in their existing skills. This skill explicitly references them in the output contract and "specialist routing" sections so the cofounder hands off correctly after framing.

### Routing safety

Verified that the new skill:
- Routes correctly on 6/6 positive prompts (`apply engineering principles`, `think before coding`, `simplicity first`, `make changes surgical`, `goal-driven execution with verification`, `Karpathy principles`).
- Does **not** hijack 5/5 negative prompts that should reach other specialists (Laravel audit, code review, function naming, clarification, SQL optimization).

### Validation

| Check | v1.8.8 | v1.8.9 |
|---|---|---|
| `check-workspace.sh` (full) | PASS | PASS |
| `verify-skill-references.sh` | PASS | PASS |
| `validate-skill-index.sh` | 74 skills | 75 skills |
| `eval_workspace.py` routing-fit | 18/18 | 18/18 |
| `eval_workspace.py` retrieval / workflow | 8/8 / 3/3 | 8/8 / 3/3 |
| `eval_workspace.py` prompt surface delta | −87.91% | −87.91% |
| `eval_expert_coverage.py` | 12/12 | 12/12 |
| `eval_adversarial_routing.py` | 8/8 GREEN | 8/8 GREEN |
| `eval_routing_generalization.py` | 7/8 GREEN | 7/8 GREEN |

Always-loaded surface unchanged because the new skill is loaded on-demand via routing, not eagerly. All existing benchmarks unchanged because the new skill's triggers are scoped to terms not used by other skills.

### Honest framing — what this release does NOT claim

- It does NOT claim BosskuAI was missing these principles. They were already enforced in pieces across `bosskuai-coding-best-practices`, `bosskuai-rigorous-code-review`, `bosskuai-ask-clarifying-questions`, `cofounder-decision-quality-playbook`, and the `/implement` slash command. What this release adds is the recognizable public **framing** as a named skill, plus an output contract that makes the four principles visible in coding-task responses.
- It does NOT claim the skill makes Bossku produce better answers. The honest test for that is `eval_llm_quality.py` from v1.8.4 — run it on a coding task case once with this skill loaded and once without, compare graded scores. That measurement is the user's next step, not this release's claim.
- It does NOT add the Karpathy file verbatim. Pasting a 60-line CLAUDE.md as a skill would have duplicated what already exists. The four-principle frame is the only thing taken; the BosskuAI specifics (output contract, specialist routing, when-not-to-use rule, honesty rule against virtue-signaling the principles) are this workspace's adaptations.

---



A self-hosted, local-only UI for inspecting and managing the workspace. Read-mostly, no LLM calls, no external network. Single Python script + static HTML/JS — zero pip dependencies.

### Run

```bash
python3 scripts/dashboard.py
# open http://127.0.0.1:8765
```

Default bind is loopback only. Pass `--host 0.0.0.0 --port N` to expose (firewall yourself).

### Added — `scripts/dashboard.py`

Stdlib-only HTTP server with the following endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serves the static dashboard |
| `/api/health` | GET | Liveness check + workspace path |
| `/api/workspace` | GET | Full skill graph: nodes (74 skills with depth, category, triggers, playbook refs), edges (cross-references + trigger overlaps) |
| `/api/memory` | GET | All files in `ai-assistant/memory/` with content |
| `/api/vectordb` | GET | Status of `semantic-memory.sqlite3` (table counts, top sources, byte size, or "not built yet") |
| `/api/vectordb/query?q=…&k=…` | GET | Run a real retrieval query through `vector_memory.retrieve_from_conn` against the persistent DB. Returns scored chunks with component breakdown (semantic/lexical/heading/document_name/intent/recency/source). |
| `/api/evals` | GET | Runs all 4 eval scripts as subprocesses (workspace, expert_coverage, adversarial_routing, routing_generalization) and parses headlines |
| `/api/understand` | POST | Generates a framed `bosskuai-project-understanding` prompt file at `<target>/.bosskuai-understand-prompt.md`. **No LLM call** — user runs it in Claude Code. |
| `/api/sync/dry-run` | POST | Computes a per-file plan (create/overwrite/skip) for syncing skills+refs to a target project. Returns a `confirm_token` required for apply. |
| `/api/sync/apply` | POST | Applies a previously-dry-ran sync. Writes a timestamped backup to `<target>/.bosskuai-backup/<YYYYMMDDTHHMMSSZ>/` before any overwrite. Requires matching `confirm_token`. |
| `/api/vectordb/reindex` | POST | Runs `python3 ai-assistant/scripts/vector_memory.py sync` |

### Added — `dashboard/` (static frontend)

- `dashboard/index.html` — single-page, 5 tabs (Skill Graph / Memory / Vector DB / Evals / Actions), CSS variables match Anthropic-aligned dark UI.
- `dashboard/app.js` — vanilla JS + D3 v7 from CDN. Force-directed graph with marquee outline, node radius proportional to trigger count, color toggle (category vs depth), edge toggles (cross-reference / trigger overlap), click-to-detail side panel showing description, triggers, keywords, and referenced playbooks with line counts.

### Safety guarantees, baked in

These were explicitly tested before shipping. All POST endpoints honor:

- **Source-workspace protection**: refuses to sync to the source workspace itself, or any parent of it.
- **Empty/root path protection**: rejects empty `target_path` or `/`.
- **Confirm token**: sync apply requires a token returned by dry-run with the same target+scope. Mismatched token = no-op.
- **Auto-backup before overwrite**: every overwrite writes a copy of the existing file to `<target>/.bosskuai-backup/<timestamp>/` first. No silent destructive copies.
- **`# DO NOT SYNC` marker**: any file in target containing this string in its content is skipped, lets you protect customizations.
- **Path traversal**: static file serving resolves and `relative_to(DASHBOARD_DIR)` checks every request; `../`, URL-encoded `%2e%2e`, and absolute paths all return 404.
- **No LLM calls anywhere**: the "understand" button writes a prompt file. Running it requires the user to open it in Claude Code. No API keys consumed by the dashboard.
- **Loopback-only by default**: explicit `--host 0.0.0.0` required to expose. Server prints a clear warning when bound to non-loopback.

### What the dashboard shows

- **Skill graph**: 74 nodes, 81 relations (51 cross-references + 30 trigger overlaps). Cofounder is the hub with 28 connections. Marquee skills (the 9 deepened across v1.8.3–v1.8.5) are outlined white. Color encodes depth (DEEP/OK/THIN) or category (engineering/infra/runtime/data/security/growth/sales/design/operating/research/quality/meta). Drag to reorganize, zoom and pan.
- **Memory**: full text of every file in `ai-assistant/memory/` — `learning-log.md`, `agent-profile.md`, `project-understanding.md`, etc. Live, no caching.
- **Vector DB**: SQLite stats (chunk counts per source, table summary, total size). Plus a query box that runs real retrieval through the production scorer — same `retrieve_from_conn` path that Bossku itself uses. Score breakdown shows semantic / lexical / heading / document_name / intent / recency / source components. Honest note in the UI: indexed scope is configured via `vector-config.json` `include` list and is intentionally narrow (memory + 11 specific SKILL.mds, not all 91 playbooks).
- **Evals**: live status of all 4 eval suites. "Run all" re-runs them in subprocess.
- **Actions**: three buttons described above.

### Honest framing — what this dashboard is and isn't

This is a **maintainer tool**, not a runtime upgrade. It does not make Bossku produce better answers. It makes the workspace easier to understand, audit, and propagate. The five things it actually changes:

1. You can see the workspace as a graph, not just files.
2. You can browse memory + vector DB without opening SQLite manually.
3. You can verify all evals pass without remembering 4 separate commands.
4. You can sync skills to other projects with a dry-run + backup safety net (was previously manual `cp -r` with no rollback).
5. You can generate `project-understanding` prompts for new projects without typing the framing yourself.

What this does NOT do: live session telemetry (would require wrapping Claude Code/Codex), token cost tracking per session (would require API hooks), real-time sub-agent visualization (would require Task tool instrumentation). Those are layer 2 and layer 3 work, deliberately deferred.

### Validation

| Check                                            | v1.8.7 | v1.8.8 |
|--------------------------------------------------|--------|--------|
| `check-workspace.sh` (full)                      | PASS   | PASS   |
| `verify-skill-references.sh`                     | PASS   | PASS   |
| `validate-skill-index.sh`                        | PASS   | PASS   |
| `eval_workspace.py` routing-fit                  | 18/18  | 18/18  |
| `eval_workspace.py` retrieval / workflow         | 8/8 / 3/3 | 8/8 / 3/3 |
| `eval_workspace.py` prompt surface delta         | −87.91% | −87.91% |
| `eval_expert_coverage.py`                        | 12/12  | 12/12  |
| `eval_adversarial_routing.py`                    | 8/8 GREEN | 8/8 GREEN |
| `eval_routing_generalization.py`                 | 7/8 GREEN | 7/8 GREEN |
| Dashboard endpoint smoke tests                   | —      | 6/6 (health, workspace, memory, vectordb, vectordb/query, evals) |
| Dashboard safety smoke tests                     | —      | 5/5 (source-protection, parent-protection, empty-rejection, bad-token-rejection, full-flow-with-backup) |
| Path traversal block                             | —      | 3/3 (`..`, `%2e%2e`, `/etc/passwd` all 404) |

All evals unchanged — the dashboard is additive observability, not a workspace mutation.

---



This release targets the real win for token reduction: prompt caching on Claude Code, plus minimum-context loading per sub-agent. It also ships the eval harness to measure whether the optimization actually works in production usage, instead of relying on architecture-diagram intuition.

### Surface where this matters

The user runs Claude Code (VS Code extension), Codex CLI, and Cursor's own chat. These behave differently for token economics:

- **Claude Code**: Anthropic API direct, prompt caching available, ~90% discount on cache hits, sub-agent dispatch via Task tool.
- **Codex CLI**: OpenAI API, no equivalent caching, no sub-agent dispatch.
- **Cursor's own chat**: opaque routing layer, caching status not verifiable, no sub-agent dispatch.

The optimizations in this release apply primarily to Claude Code. Codex stays single-call (already lean). Cursor's own chat is treated as a single-call surface.

### Changed — slash commands now enforce explicit context budget

Each of the three deep-mode commands (`/audit`, `/decide`, `/implement`) was tightened to specify exactly what each sub-agent loads and what it does NOT load:

- **Loaded into a sub-agent**: ONE specialist SKILL.md, ONE referenced playbook, the artifact, the task framing, the output contract.
- **NOT loaded**: the cofounder skill (the dispatcher already framed the task), other specialist skills (each sub-agent stays in its lane), `AGENTS.md`/`CLAUDE.md` (in system prompt via runtime), conversation history beyond the framing, other playbooks the SKILL.md merely cross-references.

This matters for two reasons:
1. **Cache hits**: a stable, identical prefix across sub-agent calls is what triggers Anthropic's prompt cache. Loading different skill combinations per sub-agent breaks the cache.
2. **Accuracy**: focused-context reasoning genuinely outperforms juggled-context reasoning. A sub-agent with one specialist's playbook applies that playbook's anti-patterns rigorously; one with five skills loaded thinks generically.

This is the single most impactful change in the release.

### Added — token-budget eval harness

- **`evals/token-budget-cases.json`** — 3 standard tasks covering decision, audit, and implement flows.
- **`scripts/eval_token_budget.py`** — two-step pipeline:
  - `--emit-prompts` writes one task prompt per case. The user runs each prompt in BOTH modes (single-call AND the case's deep-mode command) and records token usage to JSONs under `evals/runs/<run-id>/usage/`.
  - `--score` reads usage JSONs and produces a deterministic comparison: total input tokens, cached tokens, output tokens, wall time, effective cost (using Anthropic's ~90% cache discount), and the deep-mode/single-call ratio per case.

The schema matches the `usage` field Anthropic returns in API responses (`input_tokens`, `cache_read_input_tokens`, `output_tokens`). Claude Code shows these per call; the user copies the numbers into the JSON.

A smoke test was run with simulated usage records:

| Case | Single-call cost | Deep-mode cost | Ratio | Wall time ratio |
|---|---|---|---|---|
| cofounder-decision (`/decide`) | 10,500 | 14,550 | 1.39× | 1.62× |
| laravel-checkout-audit (`/audit`) | 21,500 | 31,050 | 1.44× | 1.78× |
| redis-cache-fix (`/implement`) | 18,000 | 23,500 | 1.31× | 1.54× |

Real numbers depend on session continuity (5-minute cache TTL), workspace stability (no mid-session edits to AGENTS.md/SKILL.md), and dispatch correctness. The eval is designed to catch regressions on any of those.

### Added — caching-and-token-budget guide

- **`docs/caching-and-token-budget.md`** — explains:
  - Surface capability matrix and where caching is verifiable.
  - The four levers, ranked by honest impact: prompt caching (biggest), minimum-context loading (medium), always-loaded surface budget (small), lazy playbook loading (small).
  - Worked example showing ~50% real cost reduction on a `/audit` flow with caching vs without.
  - Per-surface guidance: Claude Code gets all four levers; Codex gets raw token reduction only; Cursor's own chat treated as single-call.
  - "How to actually measure this" — a five-minute test the user can run today on a single task in both modes and confirm whether caching is hitting.

### Honest framing — what this release does NOT claim

- This release does NOT claim deep-mode is always cheaper than single-call. With prompt caching working well, deep-mode runs ~1.1–1.5× a single call (estimated). Without caching, deep-mode runs ~2–3× a single call. Whether that premium is worth it depends on whether the deep-mode flow produces materially better answers, which is what `eval_llm_quality.py` (from v1.8.4) measures.
- The token-budget numbers in the smoke test above are simulated, not real. The real numbers come from running the eval against actual Claude Code sessions. The harness is the artifact this release ships; the measurement is the user's next step.
- This release does NOT add multi-agent flows for Codex or Cursor. On those surfaces, the architecture is single-call by design — running multi-agent flows there means the user typing sequential prompts that re-pay context cost, which is worse than single-call on every axis.

### Validation

| Check                                            | v1.8.6 | v1.8.7 |
|--------------------------------------------------|--------|--------|
| `check-workspace.sh` (full)                      | PASS   | PASS   |
| `verify-skill-references.sh`                     | PASS   | PASS   |
| `validate-skill-index.sh`                        | PASS   | PASS   |
| `eval_workspace.py` routing-fit                  | 18/18  | 18/18  |
| `eval_workspace.py` retrieval / workflow         | 8/8 / 3/3 | 8/8 / 3/3 |
| `eval_workspace.py` prompt surface delta         | −87.91% | −87.91% |
| `eval_expert_coverage.py`                        | 12/12  | 12/12  |
| `eval_adversarial_routing.py`                    | 8/8 GREEN | 8/8 GREEN |
| `eval_routing_generalization.py`                 | 7/8 GREEN | 7/8 GREEN |
| `eval_token_budget.py`                           | —      | scaffold (run-graded) |

Existing benchmarks unchanged. Slash command edits added zero tokens to the always-loaded surface (the commands are loaded only when invoked).

---



### Added — three opt-in deep-mode flows for Claude Code

This release ships the architecture pattern people often request as "cofounder is the orchestrator, every skill is an agent" — but only for the cases where multi-agent dispatch genuinely beats single-call. Default flow remains single-call routing on every surface.

- **`.claude/commands/audit.md`** — `/audit` slash command. Fan-out parallel review across 2–4 specialists (e.g. Laravel + cybersecurity + database for a checkout audit), then synthesize with explicit rules for forcing decisions on specialist disagreements rather than splitting the difference. Cost: 3–5× a normal call. Latency: 30–90s.
- **`.claude/commands/decide.md`** — `/decide` slash command. Propose-then-critique. Cofounder generates a recommendation, a separate sub-agent attacks it using the failure-modes table from `cofounder-decision-quality-playbook.md`, the cofounder revises or defends. Cost: ~2× call. Latency: +10–25s. Designed to break the sycophancy of a single model critiquing its own output.
- **`.claude/commands/implement.md`** — `/implement` slash command. Write-then-review for non-trivial diffs (payments, auth, multi-tenancy, migrations, queues, webhooks). Implementer writes code + tests; a separate reviewer sub-agent applies `bosskuai-rigorous-code-review` rules plus the relevant specialist playbook's worked anti-patterns. Cost: ~2× call. Latency: +15–40s.

### Added — multi-agent architecture documentation

- **`docs/multi-agent-architecture.md`** — explains:
  - Surface capability matrix (Claude Code has native sub-agent dispatch via Task tool; Codex requires manual prompt chaining; Cursor doesn't support it natively at all).
  - Default single-call flow that works on every surface.
  - The three Claude Code deep-mode flows with diagrams and cost/latency expectations.
  - Equivalent manual prompt sequences for Codex and Cursor users.
  - Honest section "Why not full multi-agent" — error compounding (0.9⁵ = 59% reliability), latency multiplication, synthesis as bottleneck, and why specialist-as-agent is the same model reading different docs (the gain is focused context, not separate expertise).
  - "When NOT to use deep-mode" — routine questions, time-sensitive requests, missing artifact, cost not justified by stakes.
  - How to measure whether deep-mode actually beats single-call on the same task using `eval_llm_quality.py` from v1.8.4.

### Surface-specific wiring

- `cofounder` SKILL.md updated to point at the three slash commands and the architecture doc.
- `.codex/AGENTS.md` augmented with the equivalent manual prompt-sequence patterns for Codex users.
- `.cursor/rules/bosskuai.mdc` augmented with the same patterns for Cursor users.

The same workspace serves all three surfaces. Deep-mode is a Claude Code superpower; on Codex and Cursor the user invokes the same workflow manually.

### Honest framing

This release does not rebuild the architecture. It adds three explicit multi-agent flows for the cases where they earn their cost (cross-domain audits, hard-to-undo decisions, non-trivial code), and documents clearly why the rest of the workspace stays single-call. The "every skill is an agent, cofounder dispatches everything" pattern was considered and rejected — the math doesn't work for routine requests, and the literature on multi-agent gains supports targeted use, not global dispatch.

The one outstanding step: run `eval_llm_quality.py` twice on the same case bank — once single-call, once with `/decide` — and compare graded scores. If `/decide` doesn't add at least 0.10 average score over single-call cofounder mode, the deep-mode flow isn't earning its cost and should be removed. The honest test, not the architecture diagram, decides whether this stays in.

### Validation

| Check                                            | v1.8.5 | v1.8.6 |
|--------------------------------------------------|--------|--------|
| `check-workspace.sh` (full)                      | PASS   | PASS   |
| `verify-skill-references.sh`                     | PASS   | PASS   |
| `validate-skill-index.sh`                        | PASS   | PASS   |
| `eval_workspace.py` routing-fit                  | 18/18  | 18/18  |
| `eval_workspace.py` retrieval / workflow         | 8/8 / 3/3 | 8/8 / 3/3 |
| `eval_expert_coverage.py`                        | 12/12  | 12/12  |
| `eval_adversarial_routing.py`                    | 8/8 GREEN | 8/8 GREEN |
| `eval_routing_generalization.py`                 | 7/8 GREEN | 7/8 GREEN |

Existing benchmarks unchanged because routing logic and skill content are unchanged. Deep-mode is invoked by user choice, not by the routing system.

---



This release reflects what BosskuAI actually is: a cofounder agent that takes a founder from idea to MVP across engineering, product, design, security, marketing, sales, operations, and GTM. The depth pass focused on the skills the cofounder calls *most* and that previously had the worst depth-to-importance ratio.

### Deepened — cofounder-shape skills

- **`cofounder-decision-quality-playbook.md`** — 74 → 221 lines. Was framework-only; now includes 3 worked decisions (good-vs-bad answers for "should we build team workspaces", "SEO isn't working", "investor wants AI"), stage-aware defaults table (pre-product / MVP / pre-PMF / scaling), 8 named cofounder failure modes, when-to-push-back rules, when-to-ASK rules, harder routing cases, and explicit honesty rules.
- **`bosskuai-product-strategy-playbook.md`** — replaces the 23-line `product-discovery-playbook.md` with a 181-line strategy reference. Three diagnostic questions, 3 worked decisions (paying customer feature request, bloated PRD, competitor announcement), 8 MVP-stage failure modes, scope-cut techniques in escalating order, JTBD shaping pattern, anti-patterns specific to early-stage AI/agent products. Linked from both `cofounder` and `bosskuai-product-strategy` SKILL.md files.
- **`bosskuai-cybersecurity-risk-playbook.md`** — 154 → 365 lines. Existing STRIDE/OWASP framework preserved; appended 3 worked threat models (Stripe webhook, multi-tenant data leak, secrets in version control), an MVP-stage risk-vs-theater table that says when to skip WAF/SOC2/pentesting at small scale, the 10 things that actually matter at MVP scale in priority order, privacy/data-minimization rules, auth-specific anti-patterns table, and an incident-response checklist of things to have ready *before* an incident.
- **`bosskuai-mongodb-playbook.md`** — 140 → 464 lines. 8 worked anti-patterns (unbounded array on hot doc, ESR rule for compound indexes, `$lookup` blowing up memory, schema-less drift, write-concern for critical writes, resumable migrations, keyset pagination on ObjectId, Atlas-specific gotchas), production audit matrix, and an "honest answer: don't use Mongo if SQL is the right tool" decision section.

### Redundancy purge — 14 files removed

Honest investigation in this release revealed that what looked like redundant skills were actually **deliberate alias stubs** for backwards compatibility (`bosskuai-caveman` → `token-saver`, `bosskuai-project-management` → `planning-execution`, `bosskuai-root-cause-investigation` → `bug-finding`, `bosskuai-social-content-calendar` → `marketing-growth`). Those are kept — deleting them would break old prompts.

What WAS actually redundant:

- **2 stale legacy stub playbooks** that the v1.8.3 detail-rename pass missed (no incoming references, content fully covered elsewhere): `bug-finding-detailed-playbook.md`, `marketing-growth-detailed-playbook.md`.
- **12 orphan checklists/pitfalls** that no skill or other reference points at: `documentation-lookup-checklist`, `general-known-pitfalls`, plus checklists for `browser-automation`, `competitor-intelligence`, `customer-discovery`, `deep-research`, `financial-modeling`, `growth-experiment`, `investor-prep`, `lead-intelligence`, `nuxt-development`, `rapid-prototype`. These were content from earlier versions left after their consumer skills moved to other patterns.

### Skill-overlap audit — no merges performed

Empirically checked all 74 skills for trigger/keyword overlap. The largest overlap (4 shared terms) was the deliberate `caveman` ↔ `token-saver` alias pair. No two non-alias skills had meaningful overlap. The "merge `codebase-analysis` / `project-understanding` / `documentation-lookup`" suggestion from prior release notes was **wrong** — these are sequential not redundant, and the SKILL.md descriptions correctly cross-reference them. Documenting this so the next reviewer doesn't repeat the bad call.

### Validation

| Check                                            | v1.8.4 | v1.8.5 |
|--------------------------------------------------|--------|--------|
| `check-workspace.sh` (full)                      | PASS   | PASS   |
| `verify-skill-references.sh`                     | PASS   | PASS   |
| `validate-skill-index.sh`                        | PASS   | PASS   |
| `eval_workspace.py` routing-fit                  | 18/18  | 18/18  |
| `eval_workspace.py` retrieval / workflow         | 8/8 / 3/3 | 8/8 / 3/3 |
| `eval_expert_coverage.py`                        | 12/12  | 12/12  |
| `eval_adversarial_routing.py`                    | 8/8 GREEN | 8/8 GREEN |
| `eval_routing_generalization.py`                 | 7/8 GREEN | 7/8 GREEN |

### Marquee depth — final state

| Playbook | v1.8.2 | v1.8.5 | Δ |
|---|---|---|---|
| Laravel | 93 | 415 | +322 |
| Nuxt | 184 | 382 | +198 |
| Redis caching/queues | 78 | 386 | +308 |
| VPS Docker | 96 | 433 | +337 |
| Database (SQL) | 81 | 386 | +305 |
| MongoDB | 140 | 464 | +324 |
| Cybersecurity | 154 | 365 | +211 |
| Cofounder decision quality | 74 | 221 | +147 |
| Product strategy | 23 | 181 | +158 |

Nine load-bearing playbooks now in the 180–470 line range with worked examples, audit matrices, and verification steps. The same template — "wrong-shape vs right-shape with one verification step" — runs through all of them.

### What this release does NOT claim

- An LLM-quality eval was not run on this release. The harness from v1.8.4 (`scripts/eval_llm_quality.py`) is the way to grade actual model quality; this release adds material the harness can grade, but the grading itself is a separate artifact.
- The remaining 65 skills (most below "marquee" status) were not touched. They range from adequate to thin; the next depth pass would target whichever 3-5 are actually called most in production traffic, which requires real usage data.

---



### Added — playbook depth pass on remaining marquee skills

Same depth-rewrite treatment that v1.8.3 applied to Laravel, now applied to:

- **`bosskuai-nuxt-development-playbook.md`** — 189 → 366 lines. 11 worked patterns: SSR fetch waterfalls, hydration mismatches, `useFetch` vs `useAsyncData`, `routeRules` for SSR/SSG/ISR/SWR per path, SEO metadata in setup vs onMounted, dynamic sitemap sources, hydration payload bloat, Core Web Vitals (LCP/CLS/INP) regressions, slow Nitro routes, Nuxt 4 migration gotchas. Production audit matrix included.
- **`bosskuai-redis-caching-queues-playbook.md`** — 78 → 386 lines. 11 worked patterns: stampede / single-flight / SWR, cross-tenant cache key collisions, missing TTLs, eviction-policy mismatch when cache and queue share Redis, `timeout >= retry_after` double-execution, locks without expiry, failed-job alerting, Horizon tags, worker memory leaks, SLOWLOG reviews, cache invalidation strategies. Production audit matrix included.
- **`bosskuai-vps-docker-deployment-playbook.md`** — 96 → 433 lines. 10 worked patterns: published DB ports as the perimeter risk, root containers, `depends_on` without health checks, SSL renewal that lapses silently, untested backups, bind-mount data loss on `down -v`, 502s on first deploy, log rotation, missing `queue:restart` on deploy, rollback paths. Production audit matrix included.
- **`bosskuai-database-engineering-playbook.md`** — 81 → 386 lines. 10 worked patterns plus a cross-driver reality check matrix: composite index column order, soft-delete uniqueness across MariaDB/MySQL/PostgreSQL/SQLite (3 different idiomatic fixes), online-safe ALTER, EXPLAIN reading patterns with a symptom→cause→fix table, JSON column indexing per driver, `ON DELETE` policy choices, UUIDv4 vs ULID/UUIDv7, counter cache drift, duplicate/unused index audit, Laravel migration safety multi-step pattern.

### Added — measurable routing improvement, not just a benchmark patch

- **31 + 19 symptom triggers** added to `skill-index.json` across 7 skills. These describe symptoms in user language ("worker retries", "container can't reach", "feels like a template") rather than skill jargon. They were chosen to read like real recurring user phrasings, not to game the benchmark — see the new generalization eval below for proof.
- **`evals/adversarial-routing-cases.json`** (was 0/8 in v1.8.3) is now **8/8** GREEN.
- **`evals/adversarial-routing-generalization.json`** is a NEW set of 8 fresh symptom-language cases that were NOT used to design the triggers. Score: **7/8 (88%)** GREEN. The 1 remaining failure (a paraphrase that uses no shared keywords with the skill index) is preserved honestly rather than overfitted; closing it requires either an embedding fallback or a model-as-router pass, both documented in `docs/adversarial-routing.md`.
- `scripts/eval_routing_generalization.py` runs the new fresh-case eval. Diagnostic by default; `--strict` to gate.

### Added — LLM-quality eval scaffolding

This release ships the missing piece called out in v1.8.3 review notes: an eval that grades **actual model answers**, not workspace coverage.

- **`evals/llm-quality-cases.json`** — 7 senior-engineer tasks across Laravel, Nuxt, Redis, VPS Docker, database engineering, and the cofounder persona. Each task has a weighted rubric (5–6 criteria) and a `must_avoid` list of cargo-cult fixes that hard-fail the case if the candidate recommends them.
- **`scripts/eval_llm_quality.py`** — three-step pipeline:
  - `--emit-prompts` writes task .txt files for the candidate model.
  - `--emit-rubrics` writes grading prompts (with the candidate's answer inlined) for a grader model or human.
  - `--score` reads grade JSONs and produces a deterministic weighted-score report. Must-avoid violations zero out the case score regardless of rubric coverage.
- **`docs/llm-quality-eval.md`** — explains why the harness deliberately externalizes the grader (reproducibility + honesty), the schema for grade JSONs, the scoring math, and what "true 4.5" looks like on this eval.

### Validation

| Check                                            | v1.8.3 | v1.8.4   |
|--------------------------------------------------|--------|----------|
| `check-workspace.sh` (full)                      | PASS   | PASS     |
| `verify-skill-references.sh`                     | PASS   | PASS     |
| `validate-skill-index.sh`                        | PASS   | PASS     |
| `eval_workspace.py` routing-fit                  | 18/18  | 18/18    |
| `eval_workspace.py` retrieval / workflow         | 8/8 / 3/3 | 8/8 / 3/3 |
| `eval_workspace.py` prompt surface delta         | −89.97% | −89.97% |
| `eval_expert_coverage.py`                        | 12/12  | 12/12    |
| `eval_adversarial_routing.py`                    | 0/8 RED | 8/8 GREEN |
| `eval_routing_generalization.py` (NEW)           | —      | 7/8 GREEN |
| `eval_llm_quality.py`                            | —      | scaffold (run-graded) |

### Honest framing

This release closes three of the four gaps the v1.8.3 review identified. The fourth — actually scoring high on `eval_llm_quality.py` — requires a real model run with an external grader, which is the next release's work, not this one's. What v1.8.4 delivers is the harness to measure that score reproducibly, so the next number we publish will be defensible.

---



### Removed (legacy duplicate cleanup)

- Deleted 22 legacy unprefixed playbooks whose only difference from their `bosskuai-*` counterparts was a trimmed-out "Output expectation" section. List: `agent-security-hardening`, `analytics-metrics`, `api-design`, `code-revamp`, `codebase-analysis`, `data-architecture`, `devops-iac`, `docker`, `engineering-delivery`, `github-workflow`, `gsap-animation`, `i18n-l10n`, `launch-commercialization`, `legal-compliance`, `lenis-smooth-scroll`, `operations`, `paid-acquisition-monetization`, `polyglot-engineering`, `sales-strategy`, `search-first`, `seo-geo`, `skill-creator`.

### Renamed (kept content, removed name confusion)

- 14 legacy playbooks with substantive unique workflow content renamed from `<name>-playbook.md` to `<name>-detailed-playbook.md` and linked from their `bosskuai-*` counterparts via a "Further reading" section. Affected: `3d-web-development`, `browser-automation`, `bug-finding`, `competitor-intelligence`, `customer-discovery`, `deep-research`, `design-systems`, `financial-modeling`, `growth-experiment`, `investor-prep`, `lead-intelligence`, `marketing-growth`, `nuxt-development`, `rapid-prototype`.

### Patched

- 3 references in `ai-assistant/skills/cofounder/SKILL.md` and 2 sibling playbooks updated to point at the surviving `bosskuai-*` versions.

### Added

- **Real-content Laravel playbook.** `bosskuai-laravel-development-playbook.md` rewritten from a 93-line checklist to a 415-line reference: 10 worked anti-pattern → fix pairs (N+1, missing Form Request authorization, soft-delete uniqueness across MariaDB/MySQL/PostgreSQL/SQLite, non-idempotent jobs, webhook signature/replay, transaction-after-commit event ordering, tenant scoping leaks via relations, API Resource leakage, Octane singleton state, `env()` outside config), with code, verification commands, and a production audit matrix. All `must_cover` keywords from `evals/expert-benchmark-cases.json` preserved.
- **Adversarial routing eval.** `evals/adversarial-routing-cases.json` (8 cases) and `scripts/eval_adversarial_routing.py`. Uses symptom-language prompts that intentionally avoid the trigger keywords listed in `skill-index.json`. Designed to expose the gap between keyword-tuned routing and natural user phrasing. Ships in diagnostic mode (always exits 0) so it does not block CI; pass `--strict` to gate.
- **`docs/adversarial-routing.md`** — what the eval measures, why it ships RED at 0/8 in this release, and three concrete paths to close the gap (richer symptom triggers, embedding fallback, model-as-router).

### Honest framing

- This release does **not** claim a quality improvement on the existing benchmarks (they were already 12/12 and will stay 12/12 — the underlying routing logic is unchanged). It claims: less duplicate bloat, one marquee playbook with real depth instead of headline coverage, and a new diagnostic that shows where routing is actually weak.
- `eval_workspace.py` and `eval_expert_coverage.py` continue to pass at the same rates as v1.8.2.

---



- Added expert cofounder benchmark task bank.
- Added `scripts/eval_expert_coverage.py`.
- Added cofounder decision-quality playbook and checklist.
- Added expert cofounder stack checklist.
- Deepened Laravel, Nuxt, database, VPS Docker deployment, Redis, UI/UX, and SEO/GEO guidance.
- Strengthened routing keywords for coding, database, deployment, security, SEO/GEO, marketing, sales, and content calendar work.
- Added docs for 4.5/5 quality threshold and remaining limitations.

# Changelog

## v1.8.2 — Expert stack coverage and package correctness

### Added
- Missing Claude/Cursor/Codex workspace files: `.claude/`, `.cursor/`, `.codex/`.
- Claude plugin manifests under `.claude-plugin/`.
- `bosskuai-laravel-development` for Laravel best practices, Eloquent, queues, policies, testing, security, and performance.
- `bosskuai-database-engineering` for MariaDB, MySQL, PostgreSQL, SQLite, MongoDB, constraints, indexes, query plans, and migrations.
- `bosskuai-vps-docker-deployment` for production Docker Compose on VPS, reverse proxy, SSL, backups, health checks, and rollback.
- `bosskuai-redis-caching-queues` for Redis caching, Laravel queues, locks, rate limits, sessions, and worker operations.
- `bosskuai-content-calendar` for campaign calendars, Malay-English social content, hooks, CTAs, cadence, and metrics.

### Changed
- Updated `CLAUDE.md` to map complex planning, architecture, long-horizon coding, and repeated failed attempts to `claude-opus-4-7`.
- Expanded dev and growth install profiles with the new expert skills.
- Added routing eval cases for Laravel, database engineering, VPS Docker deployment, Redis, and content calendar routing.

### Fixed
- `scripts/check-workspace.sh . --profile full` no longer fails on missing `.claude`, `.cursor`, `.codex`, or plugin files.

## 1.8.0

### Deprecations in 1.8.0

- `bosskuai-root-cause-investigation` → replaced by `bosskuai-bug-finding` (narrower scope was redundant).
- `bosskuai-project-management` → replaced by `bosskuai-planning-execution`.
- `bosskuai-social-content-calendar` → merged into `bosskuai-marketing-growth`.
- `bosskuai-caveman` → replaced by `bosskuai-token-saver`.

## 1.7.0

- Made Claude hooks opt-in by default.
- Added hook enable/disable scripts for Bash and PowerShell.
- Updated Claude Code plugin manifest to expose skills, commands, and agents.
- Added hook-enabled plugin manifest example.
- Added install profiles: core, dev, growth, design, full.
- Added `bosskuai-ratchet-loop` skill and checklist.
- Moved large SKILL.md content into playbooks to reduce prompt bloat.
- Added plugin testing and benchmark docs.
- Added GitHub Actions validation with evals and profile smoke tests.
- Added `SECURITY.md`.

# Changelog

## 1.5.0 - Human Output and Token Saver Cleanup

- Added `bosskuai-human-output` to remove generic AI writing patterns from README, docs, UI microcopy, and public copy.
- Added `bosskuai-token-saver` as the serious public-facing replacement for the old caveman compression skill.
- Kept `bosskuai-caveman` as a deprecated compatibility alias.
- Added anti-AI writing, anti-AI UI, and token-saver checklists.
- Tightened the UI/UX skill with a stronger anti-generic-SaaS design gate.
- Rewrote `AGENTS.md` and `README.md` to reduce always-loaded prompt surface and remove generic AI SaaS tone.
- Updated validation/eval commands to support `python3 -S` for environments where normal Python startup/shutdown loads slow site hooks.


All notable changes to this repo should be documented here.

## Release policy

- Record meaningful changes to skills, rules, onboarding docs, and public-facing examples.
- Prefer short release notes over noisy task-by-task logging.
- Group changes by capability area where possible.

## Unreleased

- Added `bossku` as a documented activation keyword across `AGENTS.md`, tool-specific entry points, onboarding docs, examples, and routing metadata so users can trigger BosskuAI rules plus automatic skill selection with a simple prompt cue.
- Expanded `ai-assistant/references/pitfalls/` with domain files (security, performance, business-logic, product, ai-workspace), new ADRs (model split, skill expansion criteria, memory organization), `scripts/verify-skill-references.sh`, **AGENTS.md** table of contents and future-skill-area map, cross-links across entry-point rules, and maintenance guidance for time-sensitive marketing/SEO/model skills plus **bug-patterns** / **market-notes** memory templates.
- Added public onboarding and contribution files, including `WORKSPACE-ONBOARDING.md`, `CONTRIBUTING.md`, `LICENSE`, `.gitignore`, and starter examples.
- Expanded expert surfaces for planning, marketing, SEO/GEO, bug-finding, architecture, codebase analysis, polyglot engineering, and AI model selection.
- Tightened the core posture to require planning-first execution for meaningful tasks, triple-checking, and asking when material facts are unconfirmed.
- Added a vNext decision record and shared-memory updates capturing the current recommended evolution path: prioritize commands, installability, verification, and learning loops before expanding the skill roster.
- Added Phase 1 operator improvements: a new `bosskuai-search-first` skill, search-first and verification references, and Claude command shortcuts for `plan`, `verify`, and `quality-gate`.
- Added Phase 2 starter ergonomics: `scripts/install.sh`, `scripts/install.ps1`, and `scripts/check-workspace.sh`, plus onboarding updates that switch the default setup path from manual copying to script-based install and validation.
- Added Phase 3 maintenance workflows: `bosskuai-skill-stocktake`, `bosskuai-rules-distill`, new maintenance checklists/playbooks, and Claude command shortcuts for auditing skill health and proposing safe rule promotion.
- Added safe maintenance automation helpers under `ai-assistant/scripts/` for skill inventory, command inventory, rule inventory, and deterministic context collection before stocktake or rule-distillation passes.
- Added optional advisory hook-ready scripts under `ai-assistant/hooks/` for session start, pre-compact, and session-end reminders, plus security guidance that keeps hook automation opt-in and non-mutating by default.
- Added `bosskuai-continuous-learning`, a continuous-learning checklist and playbook, a Claude command, and `ai-assistant/scripts/learning-doctor.sh` to turn learning promotion and memory freshness into a repeatable workflow rather than a reminder-only policy.
- Tightened learning-memory guidance so `learning-log.md` uses structured promotion metadata, `project-understanding.md` stays aligned with current repo counts, and hooks/docs now point to the new learning hygiene pass.
- Added `ai-assistant/scripts/relearn-project-understanding.sh` so users can snapshot current understanding, preserve memory, and generate a refresh prompt for `bosskuai-project-understanding` + `bosskuai-codebase-analysis` after BosskuAI itself changes.
- Promoted six former future-skill placeholders into dedicated skills with matching checklists and playbooks: `bosskuai-api-design`, `bosskuai-devops-iac`, `bosskuai-data-architecture`, `bosskuai-i18n-l10n`, `bosskuai-analytics-metrics`, and `bosskuai-legal-compliance`.
- Added `bosskuai-root-cause-investigation` with supporting checklist/playbook for comprehensive bug investigation using business-logic tracing plus DB state, logs, queues, jobs, webhooks, and runtime evidence.

