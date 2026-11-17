// BosskuAI stop gate. Stop hook.
//
// "Verification before completion", made mechanical: if source files were edited
// this turn and no verification command (test, lint, typecheck, build, smoke
// check) ran after the last edit, the turn may not end. The model is sent back to
// run the pass signal, or to state explicitly what is unverified and why.
//
// Never fires twice in a row (stop_hook_active), never blocks doc-only turns,
// and accepts an explicit "not verified / could not run" statement in the final
// message as the honest way out. Edits under ~/.claude and the OS temp folder are
// not source edits (isScratch). Off switch: BOSSKU_STOP_GATE=off.
//
// Security gate (a must rule, see bossku/security.py): a turn that changed code, a
// dependency manifest or infra/CI/agent config must end with a `Security gate:`
// verdict line. Same once-per-turn rule. Off switch: BOSSKU_SECURITY_GATE=off.
//
// Review gate: a turn that edited source files must end with a `Review: CLEAN | FIXED <n> | OPEN <n>` line from a
// self-review of its own diff. It checks that the line is there, not that the review was good. All asks go out in
// one block, so a turn costs at most one extra round. Off switch: BOSSKU_REVIEW_GATE=off.
import fs from "node:fs";
import { ext, isMain, isOff, isScratch, pluginRoot, readStdinJson, toPosix } from "./_lib.mjs";

const EDIT_TOOLS = new Set(["Write", "Edit", "MultiEdit", "NotebookEdit"]);
const RUN_TOOLS = new Set(["Bash", "PowerShell"]);
const CODE_EXT = new Set([
  "js", "jsx", "ts", "tsx", "mjs", "cjs", "vue", "svelte", "astro", "py", "php", "blade.php", "rb", "go", "rs",
  "java", "kt", "swift", "cs", "sql", "css", "scss", "sass", "less", "html", "sh", "ps1", "dockerfile", "makefile",
]);
const UI_EXT = new Set(["vue", "tsx", "jsx", "svelte", "astro", "html", "blade.php", "css", "scss", "sass", "less"]);
// Stylesheets carry no trust boundary; every other code file gets the security pass.
const STYLE_EXT = new Set(["css", "scss", "sass", "less"]);
// Same lists as MANIFESTS and INFRA in bossku/security.py.
const MANIFESTS = new Set([
  "package.json", "package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock",
  "requirements.txt", "pyproject.toml", "poetry.lock", "pipfile", "pipfile.lock", "uv.lock",
  "composer.json", "composer.lock", "go.mod", "go.sum", "cargo.toml", "cargo.lock", "gemfile", "gemfile.lock",
  "pom.xml", "build.gradle", "build.gradle.kts", "packages.lock.json", "pubspec.lock",
]);
const INFRA =
  /(?:^|\/)(?:dockerfile[^/]*|docker-compose[^/]*\.ya?ml|compose\.ya?ml|[^/]+\.tf|[^/]+\.tfvars|\.gitlab-ci\.yml|\.github\/workflows\/[^/]+\.ya?ml|\.mcp\.json|nginx[^/]*\.conf|serverless\.ya?ml|vercel\.json|netlify\.toml)$/i;
// A line of its own, with the same prefixes as REVIEW_RE: "Done. Security gate: PASS" mid-sentence is not a verdict.
const VERDICT_RE = /^[\s>*_-]*security gate:/im;
// A line of its own that starts with the verdict, as in `Review: FIXED 2` or `**Review:** CLEAN`. Prose such as
// "Code review: clean-up later" and the bare `CLEAN | FIXED <n>` template do not count.
const REVIEW_RE = /^[\s>*_-]*review:[*_]*\s*(?:clean(?![\w-])(?!\s*\|)|fixed\s+\d+|open\s+\d+)/im;

const baseName = (f) => (toPosix(f).split("/").pop() || "").toLowerCase();

export function isSecurityRelevant(file) {
  const e = ext(file);
  return (CODE_EXT.has(e) && !STYLE_EXT.has(e)) || MANIFESTS.has(baseName(file)) || INFRA.test(toPosix(file));
}

// One regex per family, kept as literals so escapes cannot be mangled by a shell.
const VERIFY_PATTERNS = [
  /\b(pytest|unittest|vitest|jest|mocha|ava|phpunit|pest|artisan\s+test|composer\s+test)\b/i,
  /\b(npm|pnpm|yarn|bun)\s+(run\s+)?(test|lint|typecheck|type-check|check|build|e2e|ci)\b/i,
  /\bnpx\s+(tsc|eslint|vitest|jest|playwright|biome|prettier\s+--check|vue-tsc|nuxi\s+typecheck|astro\s+check|svelte-check)\b/i,
  /\b(tsc|eslint|biome\s+(check|lint)|ruff|mypy|pyright|flake8|pylint|black\s+--check|pint|phpstan|psalm|golangci-lint|clippy|rubocop|swiftlint)\b/i,
  /\bgo\s+(test|vet|build)\b|\bcargo\s+(test|check|clippy|build)\b|\bdotnet\s+(test|build)\b|\b(gradlew?|mvn)\s+(test|check|verify)\b/i,
  /\bmake\s+(test|check|lint|build)\b|\bnode\s+(--test|--check)\b|\bdeno\s+(test|lint|check)\b|\bphp\s+-l\b/i,
  /\bbossku\s+validate\b|\bpython3?(\.exe)?"?\s+-m\s+(bossku\s+validate|unittest|pytest|py_compile)\b/i,
  /\bplaywright\s+(test|screenshot)\b|shot\.mjs|\bcurl\b[^|]{0,2000}(localhost|127\.0\.0\.1|:\d{4})|\bgit\s+diff\s+--check\b/i,
];
// Running the code is the check the gate asks for, same rule as bossku/gate.py RUNS_CODE: a script, `-c`, or a heredoc
// fed to an interpreter, or a shell script. Version and help flags and pip installs run nothing of the project's.
const RUNS_CODE = [
  /(?:^|[\s(`])(?:python3?|py|node|deno|bun|ruby|php|perl|Rscript)(?:\.exe)?"?\s+(?!--version\b|-V\b|-v\b|-h\b|--help\b|-m\s+(?:pip|venv|ensurepip)\b)\S/i,
  /(?:^|[\s(`])(?:bash|sh|zsh)\s+[^\s|;&]+\.sh\b/i,
  // A ./script.sh or ./script.py only as the command word (`chmod +x ./run.sh` and `git add ./check.py` run nothing).
  /^\s*(?:(?:then|do|else|elif|if|while|until|!|\{|sudo|time|env|exec|nohup|command)\s+)*(?:\w+=\S*\s+)*(?:timeout\s+\S+\s+)?\.\/[\w./-]+\.(?:sh|py)\b/i,
  // A path-qualified or quoted interpreter, only as the command word (`git add src/python docs` runs nothing).
  /^\s*(?:\w+=\S*\s+)*(?:timeout\s+\S+\s+)?(?:"[^"]*[\\/]|'[^']*[\\/]|[^\s=]*[\\/])(?:python3?|py|node|deno|bun|ruby|php|perl|Rscript)(?:\.exe)?["']?\s+(?!--version\b|-V\b|-v\b|-h\b|--help\b|-m\s+(?:pip|venv|ensurepip)\b)\S/i,
];
// A segment that starts with one of these only reads (same list as bossku/gate.py READS_ONLY).
const READS_ONLY = /^\s*(?:(?:sudo|command)\s+)?(?:\S*[\\/])?(?:(?:git\s+grep|grep|egrep|rg|cat|echo|printf|head|tail|less|more|type|findstr|ls|dir|wc|stat|which|where|gc|gci|sls|write-output|write-host|get-content|get-childitem|select-string)(?:\.exe)?(?![\w.-])|sed\s+-n\b)/i;
// An error result that says the command never ran (denied by the auto-mode classifier, a permission rule, a hook or the
// user, or aborted or interrupted first) is not a failed check. Same list as NOT_RUN in bossku/gate.py; any other error
// text stays a failure.
const NOT_RUN_RE =
  /^\s*(?:<error>)?(?:Permission (?:for this (?:action|command) (?:was|has been) denied|to use )|The user doesn't want to proceed with this tool use|Command was aborted before completion|\[Request interrupted by user|\[Tool call interrupted: |PreToolUse:\S+ hook error: [^\n]{0,60}? denied|The server-side auto mode classifier gave no verdict|<tool_use_error>Blocked: |This agent is isolated in the worktree)/;
// Masks the secret shapes of bossku/redact.py redact_command that show up in a command: NAME=value for a secret-looking
// name, --password/--token style flags, and well-known token prefixes.
// A value is a whole quoted string (an unclosed one runs to the end) or a bare word.
// A quote followed by a space, a separator or the end is a closing quote (`grep -q "API_KEY=" f`), not a value.
const VALUE = String.raw`(?:"(?![\s;|&)]|$)[^"]*"?|'(?![\s;|&)]|$)[^']*'?|[^\s"']\S*)`;
const SECRET_FLAG = new RegExp(String.raw`((?<![\w-])-{1,2}[\w-]*(?:password|passwd|pass|token|secret|api[-_]?key|access[-_]?key|auth|credentials?)(?:=|\s+))(?!-)${VALUE}`, "gi");
const SECRET_ENV = new RegExp(String.raw`(\b[\w-]*(?:secret|passw(?:or)?d|pass|pwd|token|credentials?|api[_-]?key|_key)\s*=\s*)${VALUE}`, "gi");
const SECRET_TOKEN =
  /\b(?:sk-[\w-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_\w{20,}|AKIA[0-9A-Z]{16}\b|xox[abposr]-[\w-]{10,}|(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{10,}|glpat-[\w-]{20,}|hf_[A-Za-z0-9]{30,}|npm_[A-Za-z0-9]{36}\b|AIza[\w-]{35})|(?<![\w-])eyJ[\w-]{8,}\.[\w-]{8,}\.[\w-]{8,}/g;
// The other shapes of redact_command and redact, in the same order: a value after a program's own flag (curl -u,
// gh secret set --body, docker login -p, mysql -pVALUE), NAME: value pairs and JSON, Bearer and Basic headers,
// a PEM key, and user:password in a URL.
const SECRET_SHAPES = [
  [new RegExp(String.raw`(\bsecrets?\s+set\b[^\n|;&]*?\s(?:--body|-b)(?:=|\s+))${VALUE}`, "gi"), "$1[REDACTED]"],
  [new RegExp(String.raw`(\bcurl\b[^\n|;&]*?\s(?:-[a-zA-Z]*u|--user(?![\w-]))(?:=|\s*))${VALUE}`, "gi"), "$1[REDACTED]"],
  [new RegExp(String.raw`(\b(?:docker|podman|nerdctl)\s+login\b[^\n|;&]*?\s-p(?:=|\s*))${VALUE}`, "gi"), "$1[REDACTED]"],
  // The command name is case-insensitive, the flag is not (-P is the port), as in bossku/redact.py.
  [new RegExp(String.raw`(\b(?:${["mysql", "mysqldump", "mysqladmin", "mariadb", "mariadb-dump"].map((w) => w.replace(/[a-z]/g, (c) => `[${c}${c.toUpperCase()}]`)).join("|")})\b[^\n|;&]*?\s-p)(?=\S)${VALUE}`, "g"), "$1[REDACTED]"],
  [new RegExp(String.raw`(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*${VALUE}`, "gi"), "[REDACTED]"],
  [/["'](api[_-]?key|secret|token|password)["']\s*:\s*["'][^"']+["']/gi, "[REDACTED]"],
  [/\bBearer\s+(?=[A-Za-z0-9._~+/=-]*\d)[A-Za-z0-9._~+/=-]{8,}/gi, "[REDACTED]"],
  [/-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----(?:(?:[^-]|-(?!--)){0,16384}?-----END (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----|(?:\s+[A-Za-z0-9+/=]{20,}){1,200})?/g, "[REDACTED]"],
  [/\bAuthorization:\s*Basic\s+[A-Za-z0-9+/]{8,}={0,2}/gi, "[REDACTED]"],
  [/(?<=:\/\/)[^\s/:@]*:[^\s/@]+(?=@)/g, "[REDACTED]"],
];
const maskSecrets = (cmd) =>
  SECRET_SHAPES.reduce((s, [re, to]) => s.replace(re, to), cmd.replace(SECRET_FLAG, "$1[REDACTED]").replace(SECRET_ENV, "$1[REDACTED]").replace(SECRET_TOKEN, "[REDACTED]"));
const UNVERIFIED_RE = /\b(not verified|unverified|could ?n[o']t (run|verify|be run)|did ?n[o']t run|no tests? (ran|were run|exist)|untested|nothing to run|cannot be verified here)\b/i;

// The simple commands of a shell command (same walk as bossku/gate.py _command_segments): a newline, ; & | and
// parentheses end a command only outside quotes, a backslash escapes the next character outside single quotes (in a
// PowerShell command a backtick does, and a backslash is plain), `$(...)` inside double quotes is a command of its own,
// a # at the start of a word outside quotes starts a comment, and heredoc body lines are skipped.
function segments(command, powershell = false) {
  const text = String(command || "");
  const esc = powershell ? "`" : "\\";
  const out = [];
  const stack = [];
  const pending = [];
  let lines = null; // trimmed line -> start offsets, built once on the first heredoc
  let escaped = false; // the last character of `cur` was escaped, so an escaped space does not end a word
  let cur = "";
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    const top = stack[stack.length - 1] || "";
    if (ch === esc && top !== "'") {
      // A line continuation after a word break leaves the next line at a word start, so its # is a comment.
      const atWordStart = cur === "" || (/\s$/.test(cur) && !escaped);
      cur += text.slice(i, i + 2);
      escaped = !(text[i + 1] === "\n" && atWordStart);
      i += 2;
      continue;
    }
    if (top === "'") {
      if (ch === "'") stack.pop();
    } else if (top === '"') {
      if (ch === '"') stack.pop();
      else if (text.startsWith("$(", i)) {
        out.push(cur);
        cur = "";
        i += 2;
        stack.push("$(");
        continue;
      }
    } else if (ch === "#" && (cur === "" || (/\s$/.test(cur) && !escaped))) {
      const nl = text.indexOf("\n", i);
      i = nl < 0 ? text.length : nl;
      continue;
    } else if (ch === '"' || ch === "'") {
      stack.push(ch);
    } else if (ch === ")" && top === "$(") {
      stack.pop();
      out.push(cur);
      cur = "";
      i++;
      continue;
    } else if (text.startsWith("<<", i) && !text.startsWith("<<<", i)) {
      const m = /^<<-?\s*(['"]?)([\w.-]+)\1/.exec(text.slice(i));
      if (m) pending.push(m[2]);
    } else if (";&|()\n".includes(ch)) {
      out.push(cur);
      cur = "";
      i++;
      if (ch === "\n" && pending.length) {
        const delim = pending.shift();
        if (!lines) {
          lines = new Map();
          for (let pos = 0; pos <= text.length; ) {
            const nl = text.indexOf("\n", pos);
            const end = nl < 0 ? text.length : nl;
            const key = text.slice(pos, end).trim();
            if (lines.has(key)) lines.get(key).push(pos);
            else lines.set(key, [pos]);
            pos = end + 1;
          }
        }
        // The first delimiter line from here on; none found means it was no heredoc (`$((1<<2))`), so nothing is skipped.
        const starts = lines.get(delim) || [];
        let lo = 0;
        for (let hi = starts.length; lo < hi; ) {
          const mid = (lo + hi) >> 1;
          if (starts[mid] < i) lo = mid + 1;
          else hi = mid;
        }
        if (lo < starts.length) {
          const nl = text.indexOf("\n", starts[lo]);
          i = nl < 0 ? text.length : nl + 1;
        }
      }
      continue;
    }
    escaped = false;
    cur += ch;
    i++;
  }
  out.push(cur);
  return out;
}

function isVerification(command, powershell = false) {
  return segments(command, powershell).some((seg) => !READS_ONLY.test(seg) && (VERIFY_PATTERNS.some((re) => re.test(seg)) || RUNS_CODE.some((re) => re.test(seg))));
}

// User-role lines the app writes that no person typed (same list as bossku/gate.py).
const NOT_TYPED = ["<ci-monitor-event>", "<task-notification>", "<agent-message", "<local-command", "<system-reminder>"];
// The gate's own block message comes back as an isMeta user line; it keeps restarting the window so the gate fires once per turn.
const OWN_BLOCK = "BosskuAI stop gate: ";

function resultText(b) {
  const c = b.content;
  const t = typeof c === "string" ? c : Array.isArray(c) ? c.map((x) => (x && typeof x.text === "string" ? x.text : "")).join("\n") : "";
  return t.slice(0, 500);
}

function textOf(entry) {
  const c = entry.message && entry.message.content;
  if (typeof c === "string") return c;
  return Array.isArray(c) ? c.map((b) => (b && b.type === "text" && typeof b.text === "string" ? b.text : "")).join("\n") : "";
}

function humanPrompt(entry) {
  if (entry.type !== "user" || entry.isSidechain) return false;
  if (entry.isMeta) return textOf(entry).includes(OWN_BLOCK);
  if (entry.isCompactSummary || (entry.origin && typeof entry.origin === "object" && entry.origin.kind && entry.origin.kind !== "human")) return false;
  const c = entry.message && entry.message.content;
  if (typeof c === "string") return !NOT_TYPED.some((t) => c.trimStart().startsWith(t));
  if (Array.isArray(c)) {
    return c.some((b) => b && b.type === "text") && !c.some((b) => b && b.type === "tool_result") && !NOT_TYPED.some((t) => textOf(entry).trimStart().startsWith(t));
  }
  return false;
}

// Read only the end of the transcript: grow the window until it holds a human prompt (the gate ignores
// everything before the last one), or fall back to the whole file. `chunk` is a parameter so tests can force growth.
export function tailLines(file, chunk = 256 * 1024) {
  const fd = fs.openSync(file, "r");
  try {
    const size = fs.fstatSync(fd).size;
    for (let n = chunk; ; n *= 4) {
      const len = Math.min(n, size);
      const buf = Buffer.alloc(len);
      fs.readSync(fd, buf, 0, len, size - len);
      let lines = buf.toString("utf8").split("\n");
      if (len < size) lines = lines.slice(1); // the first line may be cut in half
      lines = lines.filter(Boolean);
      if (len >= size || lines.some(isPromptLine)) return lines;
    }
  } finally {
    fs.closeSync(fd);
  }
}

function isPromptLine(line) {
  if (!line.includes('"type":"user"')) return false; // cheap pre-filter; a miss only grows the window, never changes the verdict
  try {
    return humanPrompt(JSON.parse(line));
  } catch {
    return false;
  }
}

// `cwd` is the session's working directory: edits under ~/.claude or the OS temp folder are not source edits
// (see isScratch) unless the session itself works inside that folder.
export function analyze(lines, cwd) {
  const entries = [];
  for (const line of lines) {
    try {
      entries.push(JSON.parse(line));
    } catch {
      /* skip */
    }
  }
  let start = 0;
  for (let i = 0; i < entries.length; i++) if (humanPrompt(entries[i])) start = i;
  const edits = [];
  const secEdits = [];
  const scratch = new Map(); // isScratch resolves real paths; a turn edits the same few files again and again
  const isScratchOnce = (f) => (scratch.has(f) ? scratch.get(f) : scratch.set(f, isScratch(f, cwd)).get(f));
  const failed = new Map(); // tool_use id -> "failed" (an error), "skipped" (an error that says it never ran) or "ok"
  let checks = []; // {id, command} of the verification commands after the last edit
  for (let i = start; i < entries.length; i++) {
    const e = entries[i];
    const c = e.message && e.message.content;
    if (!Array.isArray(c)) continue;
    if (e.type === "user") {
      for (const b of c) {
        if (b && b.type === "tool_result" && b.tool_use_id) failed.set(String(b.tool_use_id), b.is_error !== true ? "ok" : NOT_RUN_RE.test(resultText(b)) ? "skipped" : "failed");
      }
      continue;
    }
    if (e.type !== "assistant") continue;
    for (const b of c) {
      if (!b || b.type !== "tool_use") continue;
      const inp = b.input || {};
      if (EDIT_TOOLS.has(b.name)) {
        const f = inp.file_path || inp.notebook_path || "";
        if (!f || isScratchOnce(f)) continue;
        if (CODE_EXT.has(ext(f))) {
          edits.push(f);
          checks = [];
        }
        if (isSecurityRelevant(f)) secEdits.push(f);
      } else if (RUN_TOOLS.has(b.name) && isVerification(inp.command, b.name === "PowerShell")) {
        checks.push({ id: String(b.id || ""), command: inp.command });
      }
    }
  }
  const ui = edits.filter((f) => UI_EXT.has(ext(f)));
  // A check with no result in the transcript counts as passed, so an unknown shape can never trap a session.
  // A denied or aborted check did not run: the last one that did decides.
  const ran = checks.filter((k) => failed.get(k.id) !== "skipped");
  const lastVerify = ran.length ? ran[ran.length - 1] : null;
  const checkFailed = edits.length > 0 && lastVerify !== null && failed.get(lastVerify.id) === "failed";
  const unverifiedAfterEdit = edits.length > 0 && (lastVerify === null || checkFailed);
  // Capped before masking so a huge command stays cheap; only the first 200 characters are ever shown.
  const failedCommand = checkFailed ? maskSecrets(String(lastVerify.command).replace(/\s+/g, " ").trim().slice(0, 2000)).slice(0, 200) : "";
  return { edits, ui, unverifiedAfterEdit, failedCommand, secEdits };
}

function shortList(files) {
  const names = [...new Set(files)].map((f) => toPosix(f).split("/").slice(-2).join("/"));
  return [names.length, names.slice(0, 5).join(", ") + (names.length > 5 ? ` (+${names.length - 5} more)` : "")];
}

if (isMain(import.meta.url)) {
  try {
    if (isOff("BOSSKU_STOP_GATE")) process.exit(0);
    const input = readStdinJson();
    if (input.stop_hook_active) process.exit(0);
    const path = input.transcript_path;
    if (!path || !fs.existsSync(path)) process.exit(0);
    const last = String(input.last_assistant_message || "");
    const { edits, ui, unverifiedAfterEdit, failedCommand, secEdits } = analyze(tailLines(path), input.cwd);
    const verify = unverifiedAfterEdit && !UNVERIFIED_RE.test(last);
    const security = secEdits.length > 0 && !VERDICT_RE.test(last) && !isOff("BOSSKU_SECURITY_GATE");
    const review = edits.length > 0 && !REVIEW_RE.test(last) && !isOff("BOSSKU_REVIEW_GATE");
    if (!verify && !security && !review) process.exit(0);
    const parts = [];
    if (verify) {
      const [n, shown] = shortList(edits);
      let msg =
        `BosskuAI stop gate: ${n} source file(s) changed this turn (${shown}) but ` +
        (failedCommand
          ? `the last check failed: \`${failedCommand}\` errored after the last edit. Read its error and fix the cause. `
          : "no verification command ran after the last edit. ") +
        "Run the pass signal now (focused test, lint, typecheck, build, or a curl/smoke check), read its real output, and only then finish. " +
        "If nothing can be run, say exactly what is not verified and why.";
      if (ui.length) {
        msg +=
          " UI files changed: capture screenshots at 390 and 1440 " +
          `(node "${pluginRoot(import.meta.url)}/scripts/shot.mjs" <url>) and look at both before claiming the UI is done.`;
      }
      parts.push(msg);
    }
    if (security) {
      // Starts with OWN_BLOCK so the block message restarts the window, as the verification one does.
      const [n, shown] = shortList(secEdits);
      const deps = secEdits.some((f) => MANIFESTS.has(baseName(f)));
      parts.push(
        `${OWN_BLOCK}security gate (must rule): ${n} file(s) changed this turn (${shown}) and the reply has no security verdict. ` +
          "Load bosskuai-security-gate and run its pass on this change: each layer it touches, deep pass for auth, payments, tenant data, secrets, uploads, public endpoints, infra/CI or agent tools. " +
          (deps ? "A dependency file changed: check the changed packages against live feeds (OSV.dev, GitHub Advisories, CISA KEV) now. " : "") +
          "Then end the reply with `Security gate: PASS | BLOCK | PROVISIONAL`, listing only High and Critical findings.",
      );
    }
    if (review) {
      // Same OWN_BLOCK start, so a review-only block also restarts the window.
      const [n, shown] = shortList(edits);
      parts.push(
        `${OWN_BLOCK}review gate: ${n} source file(s) changed this turn (${shown}) and the reply has no review line. ` +
          "Review your own diff with bosskuai-rigorous-code-review (correctness, risk, missing tests, does it meet the goal), " +
          "fix what you find and run the check again, then end the reply with `Review: CLEAN | FIXED <n> | OPEN <n>`. " +
          "Save a lesson worth reusing with `bossku remember --kind learning`.",
      );
    }
    process.stderr.write(parts.join("\n") + "\n");
    process.exit(2);
  } catch {
    process.exit(0);
  }
}
