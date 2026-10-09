# Security Policy

Bossku Superpower is a local workspace layer. It can influence how AI coding tools read, write, and reason about a project, so treat configuration changes as code changes.

## Report a Vulnerability

Open a private security advisory or contact the maintainer through GitHub.

## Safety Notes

- Review the hook commands `bossku install` writes (see Hooks below).
- Do not store secrets in project memory (`.bossku/memory/` or your Obsidian vault).
- Do not paste production credentials into skill files, memory files, or examples.
- Treat MCP/tool integrations as privileged. Keep them least-privilege.
- Validate generated code with tests, review, and security checks.

## Hooks

`bossku install` turns hooks on by default; they are not opt-in. Each one is a short command added to the agent's own config: Claude Code (`~/.claude/settings.json`), Cursor (`~/.cursor/hooks.json`), Codex (`~/.codex/hooks.json`) and OpenCode (`~/.config/opencode/plugins/bossku-sync.js`). For Codex it also sets `[features] hooks = true` in `~/.codex/config.toml` unless you set it to `false`; a file that is not valid TOML is left as it is. Open those files to see exactly what runs.

Remove them with `bossku hooks uninstall` (`--tools` picks a subset). The Claude Code stop gate is the Node `hooks/stop-gate.mjs` on a default install, switched off with `BOSSKU_STOP_GATE=off`; `BOSSKU_VERIFY_GATE=0` switches off the Python verify gate, which is the Stop hook only after `bossku install --no-harness`.

Other things `bossku install` writes for Claude Code, all removable the same way or with `--no-harness` / `--no-agents`:

- **Node hooks** in `~/.claude/settings.json`: a `PreToolUse` guard that reads each shell command to refuse destructive ones, a `PostToolUse` check that reads the file the agent just wrote, a `SessionStart` reminder, and a `Stop` gate that reads the end of the session transcript. Each command runs a script from your checkout of this repo (`hooks/`) and ends in `--bossku-harness`. Switches are in [`hooks/README.md`](hooks/README.md).
- **`permissions.deny` entries** in the same file (`git reset --hard`, `git clean -f`, `git push -f`, `migrate:fresh`, `db:wipe`, `docker compose down`, `docker-compose down`, `docker system prune`), kept next to your own entries. `bossku hooks uninstall` removes only ours. They hold even if the guard is off.
- **Subagent contracts** copied from `agents/` to `~/.claude/agents` (six files).

Reading another tool's session data: the Claude Code `SessionStart` and `UserPromptSubmit` hooks look for a Codex task that stopped on its usage limit in the same folder. They read `~/.codex/state_*.sqlite` and the last 2 MB of that thread's rollout file, read-only. They show Claude one line at session start, and after you say "continue" a brief of at most 2,000 characters (your request, the plan, file names, the last three commands and Codex's last message) with common secret shapes blanked out (a pattern list, not a guarantee). The brief stays in the chat and is never saved to the vault or the notes. The only file written is `~/.bosskuai/resume-state.json` (thread ids and times). Set `BOSSKU_RESUME=off` to stop both hooks from opening Codex's files; `bossku resume` still works when you run it yourself.
