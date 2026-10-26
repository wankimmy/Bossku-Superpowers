// BosskuAI destructive-command guard. PreToolUse on Bash | PowerShell.
//
// Denies the small set of commands that destroy uncommitted work, wipe data, or
// take down the runtime the agent is executing in, and tells the model to hand
// the command to the user with recovery steps instead of routing around it.
// Everything else is allowed (fail-open). Off switch: BOSSKU_GUARD=off.
//
// Manual test:
//   echo '{"tool_name":"Bash","tool_input":{"command":"git reset --hard"}}' | node hooks/guard.mjs
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
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

// Legitimate but consequential: the work leaves this machine, reaches users, or changes live infrastructure. AGENTS.md
// says push, merge and PRs wait for the user's go-ahead, so the host asks instead of refusing (a skill's
// `allowed-tools` cannot skip it). A deny rule above wins over these. Off switch for an approved autonomous loop:
// BOSSKU_GUARD_ASK=off.
//
// Ask rules read the command the shell runs, word by word (see commands() and parseCommand() below): the program at
// the start of each simple command and its subcommand words, with options and their values in between allowed
// (`kubectl -n prod delete`, `gh -R o/r pr merge`). Quoted text, a heredoc body or a `grep` pattern that mentions
// `git push` is not a push. `--dry-run` and `--help` never ask.
const WRITE_METHOD = /^(?:POST|PUT|PATCH|DELETE)$/i;
// REST endpoints where a write merges, moves a branch, cuts a release, starts a deploy or changes the repository's
// settings or branch protection.
const API_TARGET = /(?:^|\/)(?:merges?|git\/refs|releases|dispatches|deployments|protection)(?:[/?]|$)|\/repository\/(?:branches|tags)(?:[/?]|$)|^\/?repos\/[^/]+\/[^/?]+\/?$/i;
const GRAPHQL_WRITE = /\b(?:merge\w*|enable\w*AutoMerge|delete\w*|updateRefs?|createRef|archiveRepository|transferRepository|closePullRequest|createPullRequest)\s*\(/i;

// `gh api` / `glab api` calls that merge, move a ref, publish a release, dispatch a workflow or delete. Reading, and
// writes such as resolving a review thread or a comment, stay quiet.
function apiWrite(p) {
  let method = null;
  let fields = false;
  for (let k = 0; k < p.args.length; k++) {
    const w = p.args[k];
    const m = /^(?:-X|--method)(?:=?(.+))?$/.exec(w);
    if (m) method = m[1] !== undefined ? m[1] : p.args[k + 1] || "";
    else if (/^(?:-[fF]|--(?:raw-)?field|--input)(?:=|$)|^-[fF]\S/.test(w)) fields = true;
  }
  if (method !== null && /^DELETE$/i.test(method)) return true;
  const endpoint = p.seq.slice(1).find((w) => w.includes("/") || w.toLowerCase() === "graphql") || "";
  if (endpoint.toLowerCase() === "graphql") return /\bmutation\b/i.test(p.args.join(" ")) && GRAPHQL_WRITE.test(p.args.join(" "));
  const writes = method !== null ? WRITE_METHOD.test(method) : fields;   // gh and glab POST when fields are given
  return writes && API_TARGET.test(endpoint);
}

const vercelProd = (p) =>
  hasFlag(p, /^--prod$|^--target=production$/i) || (hasFlag(p, /^--target$/) && p.seq.some((w) => w.toLowerCase() === "production"));

export const ASK_RULES = [
  { tools: ["git"], paths: [["push"], ["subtree", "push"]], unless: (p) => hasFlag(p, /^-[a-zA-Z]*n[a-zA-Z]*$/), why: "pushes commits to a remote" },
  { tools: ["gh"], paths: [["pr", "create"], ["pr", "merge"]], why: "opens or merges a pull request" },
  { tools: ["glab"], paths: [["mr", "create"], ["mr", "merge"]], why: "opens or merges a merge request" },
  { tools: ["gh"], paths: [["repo", "delete"], ["repo", "archive"], ["repo", "rename"], ["release", "create"], ["release", "delete"], ["release", "upload"], ["workflow", "run"]], why: "changes a GitHub repository or release, or starts a workflow" },
  { tools: ["gh"], paths: [["repo", "create"]], when: (p) => hasFlag(p, /^--push$/), why: "creates a repository and pushes to it" },
  { tools: ["gh", "glab"], paths: [["api"]], when: apiWrite, why: "writes through the GitHub or GitLab API (a merge, a ref, a release, a dispatch or a delete)" },
  { tools: ["npm", "pnpm", "bun", "cargo", "poetry", "uv", "hatch", "flit"], paths: [["publish"]], why: "publishes a package" },
  { tools: ["yarn"], paths: [["publish"], ["npm", "publish"]], why: "publishes a package" },
  { tools: ["twine"], paths: [["upload"]], why: "publishes a package" },
  { tools: ["gem"], paths: [["push"]], why: "publishes a package" },
  { tools: ["npx", "bunx", "pnpx"], paths: [["semantic-release"], ["release-it"]], why: "publishes a release" },
  { tools: ["docker", "podman"], paths: [["push"], ["image", "push"], ["compose", "push"]], why: "publishes an image" },
  { tools: ["docker-compose"], paths: [["push"]], why: "publishes an image" },
  { tools: ["docker", "podman"], paths: [["build"], ["buildx", "build"], ["image", "build"]], when: (p) => hasFlag(p, /^--push$/), why: "publishes an image" },
  { tools: ["eas"], paths: [["submit"], ["update"]], why: "submits an app to a store or pushes an over-the-air update to users" },
  { tools: ["eas"], paths: [["build"]], when: (p) => hasFlag(p, /^--auto-submit/), why: "submits an app to a store" },
  { tools: ["fastlane"], paths: [["deliver"], ["supply"], ["pilot"]], why: "submits an app to a store" },
  { tools: ["vercel"], when: vercelProd, why: "deploys to production" },
  { tools: ["vercel"], paths: [["promote"]], why: "deploys to production" },
  { tools: ["netlify"], paths: [["deploy"]], when: (p) => hasFlag(p, /^--prod(?:=|$)/), why: "deploys to production" },
  { tools: ["firebase", "fly", "flyctl", "serverless", "sls"], paths: [["deploy"]], why: "deploys to production" },
  { tools: ["wrangler"], paths: [["deploy"], ["publish"], ["pages", "deploy"], ["pages", "publish"]], why: "deploys to production" },
  { tools: ["railway"], paths: [["up"]], why: "deploys to production" },
  { tools: ["terraform", "tofu"], paths: [["apply"], ["destroy"]], why: "changes or destroys live infrastructure" },
  { tools: ["pulumi"], paths: [["up"], ["destroy"]], why: "changes or destroys live infrastructure" },
  { tools: ["cdk"], paths: [["deploy"], ["destroy"]], why: "changes or destroys live infrastructure" },
  { tools: ["kubectl"], paths: [["delete"]], why: "deletes live infrastructure" },
  { tools: ["helm"], paths: [["uninstall"], ["delete"]], why: "removes a live release" },
  { tools: ["aws"], paths: [["s3", "rm"], ["s3", "rb"], [/^[\w-]+$/, /^(?:delete|terminate)-/i]], why: "deletes cloud resources" },
  { tools: ["gcloud", "az"], when: (p) => p.seq.some((w) => w.toLowerCase() === "delete"), why: "deletes cloud resources" },
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
  // Only what is inside the temp folder is scratch: on Linux it is /tmp itself, which matches the hints below.
  if (absolute && (n.toLowerCase() === TMP.toLowerCase() || /^\/(tmp|temp)$/i.test(n))) return true;
  if (/^(\/(bin|boot|dev|etc|lib|lib64|opt|proc|root|sbin|sys|usr|var|home|Users))(\/|$)/i.test(n)) return true;
  if (/^[a-zA-Z]:\/(Windows|Program Files|Users)(\/|$)/i.test(n)) return true;
  if (absolute) {
    if (TEMP_HINTS.some((re) => re.test(n))) return false;
    if (under(n, c)) return false;
    return true; // absolute path outside the project and not a temp dir
  }
  return false;
}

// Files that hold credentials. Example, sample and template copies of .env are meant to be committed, and so is
// dotenv-vault's encrypted .env.vault; `.env.d.ts` and `.env.mjs` are source code that reads env vars.
const ENV_NOT_SECRET = /\.(?:example|sample|template|dist|defaults?|vault|[cm]?[jt]sx?|py|rb|php|go|rs|sh|md)$/i;
// A credential whatever is inside.
const SECRET_NAME = /^(?:id_(?:rsa|dsa|ecdsa|ed25519)|[^/]+\.(?:p12|pfx|jks)|secrets\.json|credentials\.json|creds\.md|[._]netrc|\.pgpass)$/i;
// A credential only when the content says so: a public CA bundle or a Keynote .key is fine, a private key is not.
const SECRET_BY_CONTENT = [
  { name: /\.(?:pem|key)$/i, content: /PRIVATE KEY-----/, unreadable: true },
  // `_authToken=${NPM_TOKEN}` reads the token from the environment: that file is meant to be committed.
  { name: /^\.(?:npmrc|pypirc)$/i, content: /_auth(?:Token)?\s*=\s*(?!\$\{?\w)\S|^\s*password\s*[=:]\s*(?!\$\{?\w)\S/im, unreadable: false },
];

function readHead(file) {
  try {
    const fd = fs.openSync(file, "r");
    try {
      const buf = Buffer.alloc(64 * 1024);
      return buf.toString("latin1", 0, fs.readSync(fd, buf, 0, buf.length, 0));
    } finally {
      fs.closeSync(fd);
    }
  } catch {
    return null;
  }
}

// `read(file)` returns the file's text or null; by default the file is read from the current folder.
export function isSecretFile(file, read = readHead) {
  const posix = toPosix(file).replace(/\/+$/, "");
  const base = posix.split("/").pop() || "";
  if (/^\.env(?:\..+)?$/i.test(base)) return !ENV_NOT_SECRET.test(base);
  if (SECRET_NAME.test(base) || /(?:^|\/)\.aws\/credentials$/i.test(posix)) return true;
  if (/\.keystore$/i.test(base)) return base.toLowerCase() !== "debug.keystore"; // Android's shared debug key
  const rule = SECRET_BY_CONTENT.find((r) => r.name.test(base));
  if (!rule) return false;
  const text = read(file);
  return text === null ? rule.unreadable : rule.content.test(text);
}

// git's own answer as text, or null on any failure (no git, not a repo, timeout): every caller fails open on null.
// One budget per hook call keeps all lookups inside the 10 s hook timeout.
function budgetedGit(totalMs = 6000) {
  const end = Date.now() + totalMs;
  return (args, cwd) => {
    const left = end - Date.now();
    if (left < 250) return null;
    try {
      return execFileSync("git", args, {
        cwd, encoding: "utf8", timeout: Math.min(2500, left), maxBuffer: 256 * 1024 * 1024,
        stdio: ["ignore", "pipe", "ignore"], windowsHide: true,
      });
    } catch {
      return null;
    }
  };
}
const nulList = (text) => (text ? text.split("\0").filter(Boolean) : []);

const rawWords = (s) => String(s).match(/"[^"]*"|'[^']*'|\S+/g) || [];
const shellWords = (s) => rawWords(s).map(unquote);

// Git Bash spells C:\x as /c/x (Cygwin as /cygdrive/c/x); Node on Windows would read that as \c\x on this drive.
export function nativePath(p) {
  if (process.platform !== "win32") return p;
  const m = toPosix(p).match(/^(?:\/cygdrive)?\/([a-zA-Z])(?:\/(.*))?$/);
  return m ? `${m[1].toUpperCase()}:/${m[2] || ""}` : p;
}
const resolveDir = (base, p) => path.resolve(base, nativePath(HOME_TOKEN.test(p) && HOME ? p.replace(HOME_TOKEN, HOME) : p));

// `cd x`, `cd /d x`, `Set-Location -Path x`, `pushd x`: the folder, or null when it cannot be known (`cd "$(...)"`).
const CD_RE = /^(?:cd|chdir|pushd|Set-Location|sl)(?=\s|$)(.*)$/i;
function cdTarget(rest) {
  for (const raw of rawWords(rest)) {
    if (/^\d*[<>]|^&>/.test(raw)) break; // a redirection ends the arguments
    if (raw === "-") return null; // `cd -`: the previous folder
    if (/^(?:\/d|-(?:Path|LiteralPath|L|P|e|@)|--)$/i.test(raw)) continue;
    const word = unquote(raw);
    if (!HOME_TOKEN.test(word) && /[$`%]/.test(raw.startsWith("'") ? "" : raw)) return null;
    return word;
  }
  return "~";
}

// Where git would run for this segment: the folder from `cd` earlier on the line, then `git -C x`. `--git-dir` and
// `--work-tree` are passed through as they are. `base` is the folder ls-files paths are relative to: the work tree
// when the command runs outside it, else the folder git runs in.
function gitContext(seg, dir) {
  const m = seg.match(/\bgit((?:\s+(?:-C\s+(?:"[^"]*"|'[^']*'|\S+)|-c\s+(?:"[^"]*"|'[^']*'|\S+)|--no-pager|--git-dir(?:=|\s+)\S+|--work-tree(?:=|\s+)\S+|-P|--paginate))*)\s+(?:add|commit)\b/i);
  const pre = [];
  let workTree = null;
  if (m) {
    const words = shellWords(m[1]);
    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      const opt = /^--(git-dir|work-tree)(?:=(.*))?$/s.exec(w);
      if (w === "-C" && words[i + 1]) dir = resolveDir(dir, words[++i]);
      else if (opt && (opt[2] !== undefined || words[i + 1])) {
        const value = nativePath(opt[2] !== undefined ? opt[2] : words[++i]);
        pre.push(`--${opt[1]}=${value}`);
        if (opt[1] === "work-tree") workTree = path.resolve(dir, value);
      }
    }
  }
  const inside = workTree && (dir === workTree || dir.toLowerCase().startsWith(workTree.toLowerCase() + path.sep));
  return { dir, pre, base: workTree && !inside ? workTree : dir };
}

// `git add` and `git commit` that would put a credential file into history. Only files that become tracked count:
// a file the repo already tracks is not a new leak, and a fixture that is already committed stays editable.
const ADD_RE = new RegExp(`^${WRAP}git\\s+add(?![-\\w])(.*)$`, "i");
const COMMIT_RE = new RegExp(`^${WRAP}git\\s+commit(?![-\\w])(.*)$`, "i");

function secretCommit(bare, seg, dir, git) {
  const add = bare.match(ADD_RE);
  if (add) {
    const opts = [];
    const specs = [];
    let endOfOpts = false;
    for (const w of shellWords(add[1])) {
      if (!endOfOpts && w === "--") endOfOpts = true;
      else if (!endOfOpts && w.startsWith("-")) opts.push(w);
      else specs.push(w);
    }
    const has = (long, short) => opts.some((o) => o === long || (short && new RegExp(`^-[a-zA-Z]*${short}[a-zA-Z]*$`).test(o)));
    if (has("--dry-run", "n")) return null;
    // -u stages tracked files only; -p, -i and -e only edit hunks of tracked files.
    if (!has("--all", "A") && (has("--update", "u") || has("--patch", "p") || has("--interactive", "i") || has("--edit", "e"))) return null;
    const ctx = gitContext(seg, dir);
    const readHere = (f) => readHead(path.resolve(ctx.base, nativePath(f)));
    const named = specs.filter((s) => !/[*?[]/.test(s) && isSecretFile(s, readHere));
    if (named.length) {
      // ls-files prints paths relative to the folder it runs in, so compare in that form.
      const rel = (s) => toPosix(path.relative(ctx.dir, path.resolve(ctx.dir, nativePath(s))));
      const tracked = new Set(nulList(git([...ctx.pre, "ls-files", "-z", "--", ...named], ctx.dir)).map(toPosix));
      const fresh = named.filter((s) => !tracked.has(rel(s)));
      if (fresh.length) return { files: fresh, staged: false };
    }
    if (!specs.length && !has("--all", "A")) return null; // bare `git add` adds nothing
    const force = has("--force", "f");
    const list = [...ctx.pre, "ls-files", "--others", ...(force ? [] : ["--exclude-standard"]), "-z", "--", ...(specs.length ? specs : [":/"])];
    const hits = nulList(git(list, ctx.dir)).filter((f) => isSecretFile(f, readHere));
    return hits.length ? { files: hits, staged: false } : null;
  }
  const commit = bare.match(COMMIT_RE);
  if (commit && !rawWords(commit[1]).includes("--dry-run")) {
    const ctx = gitContext(seg, dir);
    // diff --name-only prints paths from the repo root, and `:path` reads that path from the index.
    const readStaged = (f) => git([...ctx.pre, "cat-file", "-p", `:${f}`], ctx.dir);
    const added = nulList(git([...ctx.pre, "diff", "--cached", "--name-only", "--diff-filter=A", "-z"], ctx.dir));
    const hits = added.filter((f) => isSecretFile(f, readStaged));
    return hits.length ? { files: hits, staged: true } : null;
  }
  return null;
}

// After `cd <to>`: the new folder, or null (unknown) when `to` cannot be known or is relative to an unknown folder.
function moveTo(here, to) {
  if (to === null) return null;
  const expanded = HOME_TOKEN.test(to) && HOME ? to.replace(HOME_TOKEN, HOME) : to;
  if (here === null && !path.isAbsolute(nativePath(expanded))) return null;
  return resolveDir(here || process.cwd(), to);
}

// `cwd` is the project, used to judge deletes. `dir` is where the commands run after a `cd` on the line, used only
// for git lookups; null means unknown, and then git add/commit are not looked up (fail-open). `git` runs git (a
// parameter so tests can stand in for it).
export function judge(command, cwd, git = budgetedGit(), dir = cwd) {
  const whole = String(command || "");
  for (const rule of WHOLE_LINE_RULES) {
    if (rule.re.test(whole)) return { rule: whole.trim().slice(0, 160), why: rule.why };
  }
  let here = dir === null ? null : dir || cwd || process.cwd();
  for (const seg of segments(command)) {
    const cd = seg.match(CD_RE);
    if (cd) here = moveTo(here, cdTarget(cd[1]));
    const bare = seg.replace(GIT_GLOBAL, "git "); // RULES see the verb; rmTargets keeps the raw text
    for (const rule of RULES) {
      if (rule.re.test(bare)) return { rule: seg, why: rule.why };
    }
    const secrets = here === null ? null : secretCommit(bare, seg, here, git);
    if (secrets) {
      const { files, staged } = secrets;
      const shown = files.slice(0, 3).join(", ") + (files.length > 3 ? ` (+${files.length - 3} more)` : "");
      const fix = staged ? "unstage with `git rm --cached <file>` and add it to .gitignore" : "add it to .gitignore";
      return { rule: seg, why: `would commit credential file(s) ${shown}; ${fix}, or let the user run it if the file holds no secret` };
    }
    const targets = rmTargets(seg) || findTargets(seg);
    if (targets) {
      const bad = targets.find((t) => dangerousTarget(t, cwd));
      if (bad) return { rule: seg, why: `recursive delete of ${JSON.stringify(bad)} (outside the project or a protected path)` };
    }
    const nested = seg.match(NESTED);
    if (nested) {
      const body = nested[1].replace(/^["']/, "").replace(/["']$/, "");
      const hit = judge(body, cwd, git, here);
      if (hit) return { rule: seg, why: hit.why };
      // `bash -c "cd sub && git add ."` is split at the && above, so its cd carries into the segments after it, but
      // only while the body's quote is still open: `bash -c "cd x" && git add .` runs the git add where it started.
      const quote = /^["']/.exec(nested[1]);
      const innerCd = quote && !nested[1].includes(quote[0], 1) && body.match(CD_RE);
      if (innerCd) here = moveTo(here, cdTarget(innerCd[1]));
    }
  }
  return null;
}

// The simple commands of a command line, each as its words. Splits at unquoted ; & && || | ( ) { } and line breaks; a
// quoted string is one word without its quotes. Heredoc bodies are input, not commands, so they are dropped; `$(...)`
// and backtick bodies run even inside double quotes, so they come back as commands of their own. One pass, so a long
// line costs linear time.
const HEREDOC = /(<<-?[ \t]*(["']?)([\w.-]+)\2)([^\n]*)\n([^]*?)\n[ \t]*\3[ \t]*\r?(?=\n|$)/g;
// Characters a backslash escapes outside quotes. Before anything else (`C:\tools\git.exe`) it is a Windows path separator.
const ESCAPABLE = new Set([..."\"'\\$`;&|()<>{} \t"]);
// Where each `(` closes, found in one pass, so unbalanced input stays linear.
function closers(text) {
  const close = new Map();
  const open = [];
  for (let i = 0; i < text.length; i++) {
    if (text[i] === "(") open.push(i);
    else if (text[i] === ")" && open.length) close.set(open.pop(), i);
  }
  return close;
}
export function commands(line, depth = 0) {
  const nested = [];
  const raw = String(line);
  // A heredoc fed to a shell (`bash <<EOF`, `ssh host <<EOF`) is a script after all. Past 64 heredoc starts the
  // bodies are left in place: slower to read wrongly than to search for terminators that are not there.
  const heredocs = (raw.match(/<</g) || []).length;
  const text = heredocs > 64 ? raw : raw.replace(HEREDOC, (match, head, q, tag, rest, body, offset, all) => {
    const before = all.slice(all.lastIndexOf("\n", offset) + 1, offset).split(/[\s;&|(]+/).filter(Boolean);
    const program = programName(before.find((w) => !PREFIX_WORDS.has(w.toLowerCase()) && !/^[A-Za-z_]\w*=/.test(w)) || "");
    if (SHELLS.has(program) || program === "ssh") nested.push(body);
    return head + rest;
  });
  const out = [];
  const close = closers(text);
  let words = [];
  let word = "";
  let inWord = false;
  let quote = null;
  const endWord = () => {
    if (inWord) words.push(word);
    word = "";
    inWord = false;
  };
  const endCommand = () => {
    endWord();
    if (words.length) out.push(words);
    words = [];
  };
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quote === "'") {
      if (c === "'") quote = null;
      else word += c;
      continue;
    }
    if (c === "$" && text[i + 1] === "(") {
      const end = close.get(i + 1) ?? -1;
      if (end > 0) {
        nested.push(text.slice(i + 2, end));
        word += text.slice(i, end + 1);
        inWord = true;
        i = end;
        continue;
      }
    }
    if (c === "`") {
      const end = text.indexOf("`", i + 1);
      if (end > 0) {
        nested.push(text.slice(i + 1, end));
        word += text.slice(i, end + 1);
        inWord = true;
        i = end;
        continue;
      }
    }
    if (quote === '"') {
      if (c === '"') quote = null;
      else if (c === "\\" && /["\\$`]/.test(text[i + 1] || "")) word += text[++i];
      else word += c;
      continue;
    }
    if (c === "'" || c === '"') {
      quote = c;
      inWord = true;
    } else if (c === "\\" && ESCAPABLE.has(text[i + 1])) {
      word += text[++i];
      inWord = true;
    } else if (c === "\n" || c === ";" || c === "(" || c === ")" || c === "{" || c === "}" || c === "|") {
      endCommand();
    } else if (c === "&") {
      if (text[i + 1] === ">" || text[i - 1] === ">" || text[i - 1] === "<") {
        word += c; // &> >& <& are redirections
        inWord = true;
      } else endCommand();
    } else if (/\s/.test(c)) {
      endWord();
    } else {
      word += c;
      inWord = true;
    }
  }
  endCommand();
  if (depth < 3) for (const body of nested) out.push(...commands(body, depth + 1));
  return out;
}

// Words that can stand before the program: `sudo`, `env A=1`, `nohup`, `time`, shell keywords after a `;`.
const PREFIX_WORDS = new Set(["sudo", "doas", "env", "nohup", "exec", "command", "builtin", "time", "nice", "then", "do", "else", "elif", "if", "while", "until", "!"]);
const programName = (w) => toPosix(w).split("/").pop().replace(/\.(?:exe|cmd|bat)$/i, "").toLowerCase();

// One simple command as { tool, args, seq, value }: the program (no folder, no .exe or .cmd), the words after it, and
// its subcommand words with options left out. `value[i]` marks a word right after an option written without `=`:
// it may be that option's value, so a subcommand may also start after it (`kubectl -n prod delete`).
function parseCommand(words) {
  let i = 0;
  let prefixed = false;
  for (; i < words.length; i++) {
    const w = words[i];
    if (PREFIX_WORDS.has(w.toLowerCase())) prefixed = true;
    else if (!/^[A-Za-z_]\w*=/.test(w) && !(prefixed && w.startsWith("-"))) break;
  }
  if (i >= words.length) return null;
  const args = words.slice(i + 1);
  const seq = [];
  const value = [];
  let afterOption = false;
  for (const w of args) {
    if (w.length > 1 && w.startsWith("-")) {
      afterOption = !w.includes("=");
      continue;
    }
    seq.push(w);
    value.push(afterOption);
    afterOption = false;
  }
  return { tool: programName(words[i]), words: words.slice(i), args, seq, value };
}
function hasFlag(p, re) {
  return p.args.some((w) => w.length > 1 && w.startsWith("-") && re.test(w));
}
function hasPath(p, path) {
  const starts = [0];
  for (let k = 0; k < p.seq.length && p.value[k]; k++) starts.push(k + 1);
  return starts.some((s) =>
    path.every((m, j) => {
      const w = p.seq[s + j];
      return w !== undefined && (typeof m === "string" ? w.toLowerCase() === m : m.test(w));
    }));
}

const SHELLS = new Set(["bash", "sh", "zsh", "dash", "ksh", "powershell", "pwsh"]);
// The command line inside `bash -c '...'`, `pwsh -Command "..."`, `cmd /c ...`, `eval ...`, `find -exec ... ;`,
// `xargs ...`, `timeout 10 ...` or `watch ...`, or null.
function innerLine(p) {
  if (SHELLS.has(p.tool)) {
    const at = p.args.findIndex((w) => /^-[a-z]*c$|^-command$|^<<<$/i.test(w));   // also a here-string: bash <<< '...'
    return at >= 0 && p.args[at + 1] !== undefined ? p.args[at + 1] : null;
  }
  if (p.tool === "cmd") {
    const at = p.args.findIndex((w) => /^\/[ck]$/i.test(w));
    return at >= 0 ? p.args.slice(at + 1).join(" ") : null;
  }
  if (p.tool === "find") {
    // find ... -exec cmd {} ;  (also -execdir, -ok, -okdir)
    const at = p.args.findIndex((w) => /^-(?:exec|execdir|ok|okdir)$/.test(w));
    if (at < 0) return null;
    const end = p.args.findIndex((w, k) => k > at && (w === ";" || w === "+"));
    return p.args.slice(at + 1, end < 0 ? undefined : end).join(" ");
  }
  if (["xargs", "timeout", "watch"].includes(p.tool)) {
    // the command starts at the first word that is not an option or its value; timeout's first word is the duration
    const skip = p.tool === "timeout" ? 1 : 0;
    let k = 0;
    while (k < p.seq.length && p.value[k]) k++;
    const first = p.seq[k + skip];
    return first === undefined ? null : p.args.slice(p.args.indexOf(first, p.args.indexOf(p.seq[k]))).join(" ");
  }
  return p.tool === "eval" && p.args.length ? p.args.join(" ") : null;
}

// The first command that should wait for the user's go-ahead (ASK_RULES), looking inside `bash -c` bodies too, or
// null. Call it only after judge() found nothing to deny.
export function askFor(command, depth = 0) {
  for (const words of commands(command)) {
    const p = parseCommand(words);
    if (!p) continue;
    if (!hasFlag(p, /^--(?:dry-run|help)(?:=|$)/i)) {
      for (const rule of ASK_RULES) {
        if (!rule.tools.includes(p.tool)) continue;
        if (rule.paths && !rule.paths.some((path) => hasPath(p, path))) continue;
        if ((rule.when && !rule.when(p)) || (rule.unless && rule.unless(p))) continue;
        return { rule: p.words.join(" ").slice(0, 200), why: rule.why };
      }
    }
    const inner = depth < 3 ? innerLine(p) : null;
    if (inner) {
      const hit = askFor(inner, depth + 1);
      if (hit) return { rule: p.words.join(" ").slice(0, 200), why: hit.why };
    }
  }
  return null;
}

export const DENY_ADVICE =
  "Do not work around this. Give the user the exact command plus the recovery steps " +
  "(stash first, --force-with-lease, backup, dry run) and let them run it in their own terminal. " +
  "Off switch for a deliberate session: BOSSKU_GUARD=off.";
export const ASK_ADVICE =
  "Push, merge, publish and deploy wait for the user's go-ahead. Approve to run it. If no one can answer this " +
  "prompt, stop and give the user the exact command instead of working around it. " +
  "Off switch for an approved autonomous loop: BOSSKU_GUARD_ASK=off.";

// What the guard decides for one shell command: { decision: "deny" | "ask", rule, why, reason } or null. Every host
// adapter (Claude Code, Codex, Cursor, OpenCode) calls this, so the rules stay in one place.
export function decide(command, cwd) {
  if (!command || isOff("BOSSKU_GUARD")) return null;
  const hit = judge(command, cwd);
  if (hit) return { decision: "deny", ...hit, reason: `BosskuAI guard denied: ${hit.rule}  (${hit.why}). ${DENY_ADVICE}` };
  if (isOff("BOSSKU_GUARD_ASK")) return null;
  const ask = askFor(command);
  if (ask) return { decision: "ask", ...ask, reason: `BosskuAI guard: ${ask.rule}  (${ask.why}). ${ASK_ADVICE}` };
  return null;
}

// Codex and OpenCode 1 cannot ask from a hook (an "ask" fails open in Codex), so an ask rule refuses there and says how
// to go ahead.
export const CODEX_ASK_ADVICE =
  "Push, merge, publish and deploy wait for the user's go-ahead, and this tool cannot ask from a hook, so this was " +
  "refused. Give the user the exact command to run, or, for an approved autonomous loop, they can set " +
  "BOSSKU_GUARD_ASK=off.";

// The text for a host that can only refuse: a deny keeps its reason, an ask says it was refused for want of a prompt.
export function refusal(verdict) {
  return verdict.decision === "ask" ? `BosskuAI guard: ${verdict.rule}  (${verdict.why}). ${CODEX_ASK_ADVICE}` : verdict.reason;
}

// The hook's reply for one host, or null to stay silent. `host` comes from `--host <name>` on the command line:
// claude (PreToolUse, the default), codex (PreToolUse, Bash matcher), cursor (beforeShellExecution).
export function reply(host, input) {
  if (host === "cursor") {
    // Cursor blocks on an empty or invalid reply, so every path answers.
    const verdict = decide(String(input.command || ""), input.cwd);
    if (!verdict) return { permission: "allow" };
    return { permission: verdict.decision, user_message: verdict.reason, agent_message: verdict.reason };
  }
  const tool = input.tool_name || "";
  const command = (input.tool_input || {}).command || "";
  if (!/^(Bash|PowerShell)$/.test(tool) || typeof command !== "string" || !command) return null;
  const verdict = decide(command, input.cwd);
  if (!verdict) return null;
  const codexAsk = host === "codex" && verdict.decision === "ask";
  return {
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: codexAsk ? "deny" : verdict.decision,
      permissionDecisionReason: codexAsk ? refusal(verdict) : verdict.reason,
    },
  };
}

if (isMain(import.meta.url)) {
  const at = process.argv.indexOf("--host");
  const host = at > 0 ? String(process.argv[at + 1] || "").toLowerCase() : "claude";
  try {
    const out = reply(host, readStdinJson());
    if (out) emit(out);
  } catch {
    if (host === "cursor") emit({ permission: "allow" });   // fail open, but with a reply Cursor accepts
  }
  process.exit(0);
}
