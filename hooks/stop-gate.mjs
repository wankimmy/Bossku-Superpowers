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
import fs from "node:fs";
import { ext, isMain, isOff, isScratch, pluginRoot, readStdinJson, toPosix } from "./_lib.mjs";

const EDIT_TOOLS = new Set(["Write", "Edit", "MultiEdit", "NotebookEdit"]);
const RUN_TOOLS = new Set(["Bash", "PowerShell"]);
const CODE_EXT = new Set([
  "js", "jsx", "ts", "tsx", "mjs", "cjs", "vue", "svelte", "astro", "py", "php", "blade.php", "rb", "go", "rs",
  "java", "kt", "swift", "cs", "sql", "css", "scss", "sass", "less", "html", "sh", "ps1", "dockerfile", "makefile",
]);
const UI_EXT = new Set(["vue", "tsx", "jsx", "svelte", "astro", "html", "blade.php", "css", "scss", "sass", "less"]);

// One regex per family, kept as literals so escapes cannot be mangled by a shell.
const VERIFY_PATTERNS = [
  /\b(pytest|unittest|vitest|jest|mocha|ava|phpunit|pest|artisan\s+test|composer\s+test)\b/i,
  /\b(npm|pnpm|yarn|bun)\s+(run\s+)?(test|lint|typecheck|type-check|check|build|e2e|ci)\b/i,
  /\bnpx\s+(tsc|eslint|vitest|jest|playwright|biome|prettier\s+--check|vue-tsc|nuxi\s+typecheck|astro\s+check|svelte-check)\b/i,
  /\b(tsc|eslint|biome\s+(check|lint)|ruff|mypy|pyright|flake8|pylint|black\s+--check|pint|phpstan|psalm|golangci-lint|clippy|rubocop|swiftlint)\b/i,
  /\bgo\s+(test|vet|build)\b|\bcargo\s+(test|check|clippy|build)\b|\bdotnet\s+(test|build)\b|\b(gradlew?|mvn)\s+(test|check|verify)\b/i,
  /\bmake\s+(test|check|lint|build)\b|\bnode\s+(--test|--check)\b|\bdeno\s+(test|lint|check)\b|\bphp\s+-l\b/i,
  /\bbossku\s+validate\b|\bpython3?(\.exe)?"?\s+-m\s+(bossku\s+validate|unittest|pytest|py_compile)\b/i,
  /\bplaywright\s+(test|screenshot)\b|shot\.mjs|\bcurl\b[^|]*(localhost|127\.0\.0\.1|:\d{4})|\bgit\s+diff\s+--check\b/i,
];
const UNVERIFIED_RE = /\b(not verified|unverified|could ?n[o']t (run|verify|be run)|did ?n[o']t run|no tests? (ran|were run|exist)|untested|nothing to run|cannot be verified here)\b/i;

function isVerification(command) {
  const c = String(command || "");
  return VERIFY_PATTERNS.some((re) => re.test(c));
}

// User-role lines the app writes that no person typed (same list as bossku/gate.py).
const NOT_TYPED = ["<ci-monitor-event>", "<task-notification>", "<local-command", "<system-reminder>"];
// The gate's own block message comes back as an isMeta user line; it keeps restarting the window so the gate fires once per turn.
const OWN_BLOCK = "BosskuAI stop gate: ";

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
  const scratch = new Map(); // isScratch resolves real paths; a turn edits the same few files again and again
  const isScratchOnce = (f) => (scratch.has(f) ? scratch.get(f) : scratch.set(f, isScratch(f, cwd)).get(f));
  let lastEdit = -1;
  let lastVerify = -1;
  for (let i = start; i < entries.length; i++) {
    const e = entries[i];
    if (e.type !== "assistant") continue;
    const c = e.message && e.message.content;
    if (!Array.isArray(c)) continue;
    for (const b of c) {
      if (!b || b.type !== "tool_use") continue;
      const inp = b.input || {};
      if (EDIT_TOOLS.has(b.name)) {
        const f = inp.file_path || inp.notebook_path || "";
        if (CODE_EXT.has(ext(f)) && !isScratchOnce(f)) {
          edits.push(f);
          lastEdit = i;
        }
      } else if (RUN_TOOLS.has(b.name) && isVerification(inp.command)) {
        lastVerify = i;
      }
    }
  }
  const ui = edits.filter((f) => UI_EXT.has(ext(f)));
  const unverifiedAfterEdit = edits.length > 0 && lastVerify < lastEdit;
  return { edits, ui, unverifiedAfterEdit };
}

if (isMain(import.meta.url)) {
  try {
    if (isOff("BOSSKU_STOP_GATE")) process.exit(0);
    const input = readStdinJson();
    if (input.stop_hook_active) process.exit(0);
    const path = input.transcript_path;
    if (!path || !fs.existsSync(path)) process.exit(0);
    const last = String(input.last_assistant_message || "");
    if (UNVERIFIED_RE.test(last)) process.exit(0);
    const { edits, ui, unverifiedAfterEdit } = analyze(tailLines(path), input.cwd);
    if (!unverifiedAfterEdit) process.exit(0);
    const files = [...new Set(edits)].map((f) => toPosix(f).split("/").slice(-2).join("/"));
    const shown = files.slice(0, 5).join(", ") + (files.length > 5 ? ` (+${files.length - 5} more)` : "");
    let msg =
      `BosskuAI stop gate: ${files.length} source file(s) changed this turn (${shown}) but no verification command ran after the last edit. ` +
      "Run the pass signal now (focused test, lint, typecheck, build, or a curl/smoke check), read its real output, and only then finish. " +
      "If nothing can be run, say exactly what is not verified and why.";
    if (ui.length) {
      msg +=
        " UI files changed: capture screenshots at 390 and 1440 " +
        `(node "${pluginRoot(import.meta.url)}/scripts/shot.mjs" <url>) and look at both before claiming the UI is done.`;
    }
    process.stderr.write(msg + "\n");
    process.exit(2);
  } catch {
    process.exit(0);
  }
}
