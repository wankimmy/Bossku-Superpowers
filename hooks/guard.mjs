// BosskuAI destructive-command guard. PreToolUse on Bash | PowerShell.
//
// Denies the small set of commands that destroy uncommitted work, wipe data, or
// take down the runtime the agent is executing in, and tells the model to hand
// the command to the user with recovery steps instead of routing around it.
// Everything else is allowed (fail-open). Off switch: BOSSKU_GUARD=off.
//
// Manual test:
//   echo '{"tool_name":"Bash","tool_input":{"command":"git reset --hard"}}' | node hooks/guard.mjs
import os from "node:os";
import { emit, isMain, isOff, readStdinJson, segments, toPosix } from "./_lib.mjs";

// `git -C dir -c k=v --no-pager <verb>`: global options sit between git and the verb and hide it from RULES.
const GIT_GLOBAL = /\bgit((?:\s+(?:-C\s+(?:"[^"]*"|'[^']*'|\S+)|-c\s+(?:"[^"]*"|'[^']*'|\S+)|--no-pager|--git-dir(?:=|\s+)\S+|--work-tree(?:=|\s+)\S+|-P|--paginate))+)\s+/gi;

const TEMP_HINTS = [
  /(^|\/)tmp(\/|$)/i,
  /(^|\/)temp(\/|$)/i,
  /\$tmpdir/i,
  /scratchpad/i,
  /node_modules/i,
  /(^|\/)(dist|build|\.cache|\.next|\.nuxt|coverage)(\/|$)/i,
];

// `git restore` discards the working tree unless --staged/-S is the only target.
const restoreDiscards = (seg) =>
  /\bgit\s+restore\b/i.test(seg) && (!/\s(--staged|-S)(\s|$)/.test(seg) || /\s(--worktree|-W)(\s|$)/.test(seg));

// `git branch -D x`, `-d -f`, `-df`, `--delete --force`: delete + force in any order. Plain `-d` (merged only) is fine.
const branchForceDeletes = (seg) =>
  /\bgit\s+branch\b/i.test(seg) &&
  (/\s-[a-zA-Z]*D/.test(seg) ||
    (/\s(--delete|-[a-zA-Z]*d[a-zA-Z]*)(\s|$)/.test(seg) && /\s(--force|-[a-zA-Z]*f[a-zA-Z]*)(\s|$)/.test(seg)));

// `perm` is the matching `permissions.deny` string(s) in ~/.claude/settings.json (the second layer).
// judge() ignores it; tests/hooks.test.mjs checks each one is covered by its own rule.
export const RULES = [
  // git: uncommitted work and history
  // the flag can follow other arguments: `git reset -q --hard`, `git reset HEAD~1 --hard`
  { re: /\bgit\s+reset\b[^]*\s--(hard|merge)\b/i, why: "destroys uncommitted changes", perm: ["Bash(git reset --hard:*)"] },
  // --force-with-lease / --force-if-includes are the safe forms; -f in any short cluster, --force and a +refspec are not
  { re: /\bgit\s+push\b[^]*(\s--force(?![-\w])|\s-[a-zA-Z]*f[a-zA-Z]*\b|\s["']?\+\S)/i, why: "overwrites remote history (use --force-with-lease if the user wants it)", perm: ["Bash(git push -f:*)"] },
  { re: /\bgit\s+clean\b[^]*(\s-[a-zA-Z]*f|\s--force\b)/i, why: "permanently deletes untracked files", perm: ["Bash(git clean -f:*)"] },
  { re: /\bgit\s+checkout\s+(?:[^\s-]\S*\s+)?(?:--|\.\/?)(\s|$)/i, why: "discards working-tree changes" },
  { re: /\bgit\s+(checkout|switch)\b[^]*\s(-f|--force|--discard-changes)(\s|$)/i, why: "discards working-tree changes" },
  { re: { test: restoreDiscards }, why: "discards working-tree changes (git restore --staged is fine)" },
  { re: { test: branchForceDeletes }, why: "force-deletes a branch and its unmerged commits" },
  { re: /\bgit\s+stash\s+(drop|clear)\b/i, why: "destroys stashed work" },
  // runtime the agent may be executing inside
  { re: /\bdocker(-compose|\s+compose)\s+(down|stop|restart|rm|kill)\b/i, why: "stops or removes the running stack, possibly the one this session runs in", perm: ["Bash(docker compose down:*)", "Bash(docker-compose down:*)"] },
  { re: /\bdocker\s+(system|volume|container|image)\s+prune\b/i, why: "prunes Docker state", perm: ["Bash(docker system prune:*)"] },
  { re: /\bdocker\s+volume\s+rm\b/i, why: "deletes a Docker volume" },
  { re: /\bdocker\s+(stop|kill)\b/i, why: "stops a running container" },
  { re: /\bdocker\s+rm\s+(-[a-zA-Z]*f|--force)\b/i, why: "force-removes a container" },
  { re: /(^|\s)(shutdown|reboot|halt|poweroff)(\s|$)/i, why: "restarts or halts the host" },
  { re: /\bsystemctl\s+(stop|restart|disable|mask)\b/i, why: "stops or disables a system service" },
  { re: /\b(kill\s+-9|kill\s+-KILL|pkill|killall|taskkill)\b/i, why: "force-kills processes" },
  { re: /\bStop-(Process|Service|Computer)\b|\bRestart-(Computer|Service)\b/i, why: "stops processes or services" },
  // data
  { re: /\bartisan\s+(migrate:fresh|migrate:reset|db:wipe)\b/i, why: "wipes the project database", perm: ["Bash(php artisan migrate:fresh:*)", "Bash(php artisan db:wipe:*)"] },
  { re: /\bprisma\s+migrate\s+reset\b|\brails\s+db:(drop|reset)\b|\bdrizzle-kit\s+drop\b/i, why: "drops the project database" },
  { re: /\b(drop\s+(database|schema|table)|truncate\s+table)\b/i, why: "destructive SQL" },
  { re: /\bflushall\b|\bflushdb\b/i, why: "wipes Redis" },
  // disk
  { re: /\bmkfs(\.\w+)?\b|\bdd\s+[^]*\bof=\/dev\//i, why: "formats or overwrites a device" },
  { re: /\b(chmod|chown)\s+-[a-zA-Z]*R[a-zA-Z]*\s+[^]*\s\/(\s|$)/i, why: "recursive permission change on /" },
];

// Judged on the whole command line, not per segment: the pipe is the point.
const WHOLE_LINE_RULES = [
  { re: /\b(curl|wget|irm|iwr|Invoke-(WebRequest|RestMethod))\b[^]*\|\s*(sudo\s+)?(bash|sh|zsh|iex|Invoke-Expression|powershell|pwsh)\b/i, why: "pipes a remote script into a shell (supply-chain risk)" },
];

// In front of the verb: `sudo`, `env FOO=1`, `nohup`, `time`, an option, or the verb's own folder (/bin/rm).
const WRAP = "(?:(?:sudo|env|command|nohup|time|exec)\\s+|-\\S+\\s+|\\w+=\\S*\\s+)*(?:[\\w.:~-]*[\\\\/])*";
const RM_RE = new RegExp(`^${WRAP}(rm|Remove-Item|ri|rd|rmdir|del|erase)\\b(.*)$`, "i");
const FIND_RE = new RegExp(`^${WRAP}find\\s+(.*?)\\s-(?:delete|exec\\s+(?:\\S*[\\\\/])?rm)\\b`, "i");
// `bash -c '...'`, `pwsh -Command "..."`, `cmd /c ...`: the quoted body is a command line of its own.
const NESTED = new RegExp(`^${WRAP}(?:bash|sh|zsh|dash|ksh|powershell|pwsh|cmd)(?:\\.exe)?\\s(?:[^]*?\\s)?(?:-[a-z]*c|-command|\\/c)\\s+([^]*)$`, "i");
const unquote = (t) => t.replace(/["']/g, ""); // all quotes, so "$HOME"/x and '~'/x expand like "$HOME/x"

function rmTargets(seg) {
  // rm -r <targets>, Remove-Item -Recurse <targets>, rd /s /q <target>, del /s /q
  const m = seg.match(RM_RE);
  if (!m) return null;
  const verb = m[1].toLowerCase();
  const rest = m[2];
  // Remove-Item has no other parameter that starts with r, so -r, -rec and -Recurse all mean recursive.
  const psRecurse = /(^|\s)-r[a-z]*(\s|:|$)/i.test(rest);
  const recursive =
    (verb === "rm" && (/(^|\s)-[a-zA-Z]*r[a-zA-Z]*(\s|$)/i.test(rest) || /--recursive/.test(rest))) ||
    ((verb === "remove-item" || verb === "ri") && psRecurse) ||
    ((verb === "rd" || verb === "rmdir" || verb === "del" || verb === "erase") && (/\/s/i.test(rest) || psRecurse));
  if (!recursive) return null;
  return rest
    .split(/\s+/)
    .filter((t) => t && !t.startsWith("-") && !/^\/[sq]$/i.test(t))
    .map(unquote);
}

// find <paths> [tests] -delete | -exec rm: the paths are what gets wiped. `find . -name x -delete` stays inside the project.
function findTargets(seg) {
  const m = seg.match(FIND_RE);
  if (!m) return null;
  const words = m[1].split(/\s+/).filter(Boolean);
  const at = words.findIndex((t) => /^[-(!]/.test(t));
  const paths = at < 0 ? words : words.slice(0, at);
  return paths.filter((t) => !(at >= 0 && t === ".")).map(unquote);
}

const HOME = toPosix(os.homedir()).replace(/\/+$/, "");
// ~, $HOME, ${HOME}, $USERPROFILE, $env:USERPROFILE, $env:HOME, %USERPROFILE% at the start of a path
const HOME_TOKEN = /^(?:~|\$\{?(?:HOME|USERPROFILE)\}?|\$env:(?:USERPROFILE|HOME)|%USERPROFILE%)(?=\/|$)/i;
const under = (p, dir) => !!dir && p.toLowerCase().startsWith(dir.toLowerCase() + "/");
// A folder that is a protected root or a home itself: /etc, /usr, C:/Windows, /home, C:/Users, and one user's folder
// directly below the last three. Never a project, so "inside cwd" means nothing there.
const ROOT_DIR = /^(\/(bin|boot|dev|etc|lib|lib64|opt|proc|root|sbin|sys|usr|var)|[a-zA-Z]:\/(Windows|Program Files|ProgramData)|(\/(home|Users)|[a-zA-Z]:\/Users)(\/[^/]+)?)$/i;
const broad = (p) => p.length < 2 || /^[a-zA-Z]:$/.test(p) || p.toLowerCase() === HOME.toLowerCase() || ROOT_DIR.test(p);
const TMP = toPosix(os.tmpdir()).replace(/\/+$/, "");

function dangerousTarget(t, cwd) {
  let n = toPosix(t).replace(/\/+$/, "");
  if (n === "" || n === "/" || n === "~" || n === "." || n === ".." || n === "*" || n === "/*" || n === "~/*") return true;
  const c = toPosix(cwd).replace(/\/+$/, "");
  const viaHome = HOME_TOKEN.test(n);
  if (viaHome && HOME) n = n.replace(HOME_TOKEN, HOME);
  if (viaHome && (n === HOME || n === HOME + "/*")) return true;
  if (/^\$(HOME|USERPROFILE|APPDATA|LOCALAPPDATA)\/?$/i.test(n)) return true;
  if (/^[a-zA-Z]:\/?$/.test(n)) return true;
  if (/(^|\/)\.git$/.test(n)) return true;
  if (/^\.\.\//.test(n)) return true;
  // A `..` after the start can climb out of the project (or out of a temp dir), so an absolute path with one is never allowed.
  if ((viaHome || /^\/|^[a-zA-Z]:\//.test(n)) && /\/\.\.(\/|$)/.test(n)) return true;
  // A project path spelled with ~ or $HOME is the project, but only when cwd is strictly under home.
  if (viaHome && under(n, c) && under(c, HOME)) return false;
  const absolute = /^\//.test(n) || /^[a-zA-Z]:\//.test(n);
  // The project (and the OS temp folder) usually sit under /home, /Users or C:/Users, so they are allowed before
  // those roots are refused. Neither is allowed when it is a home or system folder itself (`cd ~ && rm -rf ~/x`).
  if (absolute && under(n, c) && !broad(c)) return false;
  if (absolute && under(n, TMP) && !broad(TMP)) return false;
  if (/^(\/(bin|boot|dev|etc|lib|lib64|opt|proc|root|sbin|sys|usr|var|home|Users))(\/|$)/i.test(n)) return true;
  if (/^[a-zA-Z]:\/(Windows|Program Files|Users)(\/|$)/i.test(n)) return true;
  if (absolute) {
    if (TEMP_HINTS.some((re) => re.test(n))) return false;
    if (under(n, c)) return false;
    return true; // absolute path outside the project and not a temp dir
  }
  return false;
}

export function judge(command, cwd) {
  const whole = String(command || "");
  for (const rule of WHOLE_LINE_RULES) {
    if (rule.re.test(whole)) return { rule: whole.trim().slice(0, 160), why: rule.why };
  }
  for (const seg of segments(command)) {
    const bare = seg.replace(GIT_GLOBAL, "git "); // RULES see the verb; rmTargets keeps the raw text
    for (const rule of RULES) {
      if (rule.re.test(bare)) return { rule: seg, why: rule.why };
    }
    const targets = rmTargets(seg) || findTargets(seg);
    if (targets) {
      const bad = targets.find((t) => dangerousTarget(t, cwd));
      if (bad) return { rule: seg, why: `recursive delete of ${JSON.stringify(bad)} (outside the project or a protected path)` };
    }
    const nested = seg.match(NESTED);
    if (nested) {
      const hit = judge(nested[1].replace(/^["']/, "").replace(/["']$/, ""), cwd);
      if (hit) return { rule: seg, why: hit.why };
    }
  }
  return null;
}

if (isMain(import.meta.url)) {
  try {
    if (isOff("BOSSKU_GUARD")) process.exit(0);
    const input = readStdinJson();
    const tool = input.tool_name || "";
    const ti = input.tool_input || {};
    const command = ti.command || "";
    if (!/^(Bash|PowerShell)$/.test(tool) || !command) process.exit(0);
    const hit = judge(command, input.cwd);
    if (!hit) process.exit(0);
    emit({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason:
          `BosskuAI guard denied: ${hit.rule}  (${hit.why}). ` +
          "Do not work around this. Give the user the exact command plus the recovery steps " +
          "(stash first, --force-with-lease, backup, dry run) and let them run it in their own terminal. " +
          "Off switch for a deliberate session: BOSSKU_GUARD=off.",
      },
    });
    process.exit(0);
  } catch {
    process.exit(0);
  }
}
