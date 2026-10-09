// BosskuAI post-edit checks. PostToolUse on Write | Edit | MultiEdit | NotebookEdit.
//
// 1. Syntax check the file that was just written when a cheap authoritative
//    checker exists (JSON parse, `node --check`, `php -l`, `python -m py_compile`).
//    A syntax error is reported back to the model with exit 2 so it is fixed now,
//    not discovered three edits later.
// 2. Anti-slop lint on UI and copy files. Hard tells (Jane Doe, Acme, Lorem ipsum,
//    99.99%) come back as exit 2; soft tells (em-dash, filler verbs, purple
//    gradients, glass everywhere, Inter-by-default, placeholder image hosts, text
//    logo walls) come back as additionalContext warnings.
//
// Files under ~/.claude (workflow scripts, memory) and the OS temp folder get neither check.
//
// Off switches: BOSSKU_POST_EDIT=off (all), BOSSKU_SLOP_LINT=off (lint only).
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { emit, ext, isMain, isOff, isScratch, readStdinJson, toPosix } from "./_lib.mjs";

const MAX_BYTES = 512 * 1024;
const UI_EXT = new Set(["html", "htm", "tsx", "jsx", "vue", "svelte", "astro", "mdx", "blade.php"]);
const COPY_EXT = new Set(["md"]);
const SKIP_PATH = /(^|\/)(node_modules|vendor|\.git|dist|build|\.next|\.nuxt|coverage|skills|agents|docs|references|memory|\.claude|\.bossku|ai-skills)(\/|$)/i;
const SKIP_NAME = /^(SKILL|CLAUDE|AGENTS|CHANGELOG|LICENSE|CONTRIBUTING|SECURITY)\.md$/i;

const HARD = [
  { re: /\bJane Doe\b|\bJohn Doe\b/g, tell: "placeholder person (Jane/John Doe)" },
  { re: /\bAcme\b/g, tell: "placeholder company (Acme)" },
  { re: /\bLorem ipsum\b/gi, tell: "Lorem ipsum filler" },
  { re: /\b99\.99%|\b100%\s+(uptime|satisfaction|secure|guaranteed)\b/gi, tell: "fake-perfect number" },
];
// `copy: true` rules also run on copy files (.md); the rest are UI-only.
const SOFT = [
  { re: /—/g, tell: "em-dash (use `-`)", copy: true },
  { re: /\b(elevate|seamless(?:ly)?|unleash|next-gen|supercharge|effortless(?:ly)?|revolutioni[sz]e|empower(?:ing)?|cutting-edge|game-chang(?:er|ing)|unlock your|take .{0,20} to the next level)\b/gi, tell: "filler verb / marketing slop", copy: true },
  { re: /\b99\.9%/g, tell: "99.9% uptime: needs a real source", copy: true },
  { re: /\b(?:from|to|via)-(?:purple|violet|fuchsia|indigo)-\d{3}\b/g, tell: "AI-purple gradient stop" },
  { re: /backdrop-blur/g, tell: "glassmorphism", min: 3 },
  { re: /(?:family=Inter\b|font-family:\s*['"]?Inter\b|fontFamily:\s*['"]Inter)/g, tell: "Inter by default (is it a deliberate choice?)" },
  { re: /via\.placeholder\.com|placehold\.(?:co|it)|placekitten\.com|dummyimage\.com/g, tell: "placeholder image host (use generated images or picsum seeds)" },
  { re: /<span[^>]*>\s*(?:Acme|Globex|Initech|Umbrella|Hooli|Stark|Wayne|Vandelay)\s*<\/span>/gi, tell: "text-only logo wall (use real SVG marks)" },
];

const PY_SYNTAX = [
  "import sys",
  "try:",
  " compile(open(sys.argv[1], 'rb').read(), sys.argv[1], 'exec')",
  "except SyntaxError as e:",
  " print('SyntaxError: %s (%s, line %s)' % (e.msg, sys.argv[1], e.lineno))",
  " sys.exit(1)",
].join("\n");

// Flow only (types are not valid JS). JSX is not matched here: it shows up as node's own "Unexpected token '<'".
const FLOW_ONLY = /@flow\b|^\s*(?:import|export)\s+type\b/m;
// A lone `<` only: merge-conflict markers fail with `'<<'` and must stay a syntax error.
const JSX_TOKEN = /SyntaxError: Unexpected token (?:'<'|<(?![<=]))/;

// First `bin` on PATH, never one in the current folder. Windows `where` (and an empty or "." PATH entry) looks there
// first, and hooks run in the project, so a php.exe planted in a repo would run on every .php edit.
export function which(bin) {
  const win = process.platform === "win32";
  const norm = (p) => {
    let r = path.resolve(p);
    try {
      r = fs.realpathSync.native(r);
    } catch {
      /* missing folder: the plain spelling */
    }
    return win ? r.toLowerCase() : r;
  };
  const here = norm(process.cwd());
  const exts = win ? (process.env.PATHEXT || ".COM;.EXE;.BAT;.CMD").split(";").filter(Boolean) : [""];
  const names = win && exts.some((x) => bin.toLowerCase().endsWith(x.toLowerCase())) ? [bin] : exts.map((x) => bin + x);
  for (const raw of (process.env.PATH || "").split(path.delimiter)) {
    const dir = raw.replace(/^"|"$/g, "");
    if (!dir || norm(dir) === here) continue;
    for (const name of names) {
      const full = path.join(dir, name);
      try {
        if (!fs.statSync(full).isFile()) continue;
        if (!win) fs.accessSync(full, fs.constants.X_OK);
        return full;
      } catch {
        /* next */
      }
    }
  }
  return null;
}

export function syntaxCheck(file, e) {
  const posix = toPosix(file);
  const base = posix.split("/").pop() || "";
  try {
    if (e === "json") {
      if (/^(tsconfig|jsconfig).*\.json$/i.test(base) || /\/\.vscode\//.test(posix) || /\/\.devcontainer\//.test(posix)) return null;
      JSON.parse(fs.readFileSync(file, "utf8").replace(/^﻿/, ""));
      return null;
    }
    if (e === "js" || e === "mjs" || e === "cjs") {
      // node --check passes a .js with import/export without parsing it unless the package is type: module,
      // so check a temp .mjs copy of such files. Flow and JSX in a .js are valid for the bundler but not for
      // node: Flow files keep the plain check, and a .js that fails on its first "<" is JSX, so it passes
      // (fails open; a real error before the first tag is still reported).
      const src = e === "js" ? fs.readFileSync(file, "utf8") : "";
      const esm = /^\s*(?:import|export)\s*[\w{*"'$]/m.test(src) && !FLOW_ONLY.test(src);
      const dir = esm ? fs.mkdtempSync(path.join(os.tmpdir(), "bossku-esm-")) : null;
      const target = esm ? path.join(dir, "check.mjs") : file;
      try {
        if (esm) fs.copyFileSync(file, target);
        const r = spawnSync(process.execPath, ["--check", target], { encoding: "utf8", timeout: 10000 });
        if (r.status === 0) return null;
        const msg = (r.stderr || r.stdout || "node --check failed").trim().split(target).join(file);
        return e === "js" && JSX_TOKEN.test(msg) ? null : msg;
      } finally {
        if (dir) fs.rmSync(dir, { recursive: true, force: true });
      }
    }
    if (e === "php") {
      const php = which("php");
      if (!php) return null;
      const r = spawnSync(php, ["-l", file], { encoding: "utf8", timeout: 10000 });
      return r.status === 0 ? null : (r.stdout || r.stderr || "php -l failed").trim();
    }
    if (e === "py") {
      // Exit 0 = valid, exit 1 with our SyntaxError line = invalid; anything else (missing binary, Windows Store
      // stub, broken interpreter) means try the next candidate. compile() writes no __pycache__ into the project.
      for (const py of [process.env.BOSSKU_PYTHON, "python3", "python", "py"].filter(Boolean)) {
        const r = spawnSync(py, ["-c", PY_SYNTAX, file], { encoding: "utf8", timeout: 10000 });
        if (r.error) continue;
        if (r.status === 0) return null;
        if (r.status === 1 && /^SyntaxError:/m.test(r.stdout)) return r.stdout.trim();
      }
      return null;
    }
  } catch (err) {
    return e === "json" ? `invalid JSON: ${err.message}` : null;
  }
  return null;
}

export function slopLint(file, e) {
  const posix = toPosix(file);
  const base = posix.split("/").pop() || "";
  if (SKIP_PATH.test(posix) || SKIP_NAME.test(base)) return { hard: [], soft: [] };
  const isUi = UI_EXT.has(e);
  const isCopy = COPY_EXT.has(e);
  if (!isUi && !isCopy) return { hard: [], soft: [] };
  const text = fs.readFileSync(file, "utf8");
  const hard = [];
  const soft = [];
  for (const rule of HARD) {
    const m = text.match(rule.re);
    if (m) hard.push(`${rule.tell} x${m.length}`);
  }
  for (const rule of SOFT) {
    if (isCopy && !rule.copy) continue; // copy files: prose tells only
    const m = text.match(rule.re);
    if (!m || m.length < (rule.min || 1)) continue;
    const sample = rule.tell.startsWith("filler")
      ? ` (${[...new Set(m.map((s) => s.toLowerCase()))].slice(0, 4).join(", ")})`
      : "";
    soft.push(`${rule.tell} x${m.length}${sample}`);
  }
  return { hard, soft };
}

if (isMain(import.meta.url)) {
  try {
    if (isOff("BOSSKU_POST_EDIT")) process.exit(0);
    const input = readStdinJson();
    const file = (input.tool_input && (input.tool_input.file_path || input.tool_input.notebook_path)) || "";
    if (!file || !fs.existsSync(file)) process.exit(0);
    if (isScratch(file, input.cwd)) process.exit(0); // ~/.claude (workflow scripts, memory) and the OS temp folder are not source
    const stat = fs.statSync(file);
    if (!stat.isFile() || stat.size > MAX_BYTES) process.exit(0);
    const e = ext(file);
    const short = toPosix(file).split("/").slice(-3).join("/");

    const syntax = syntaxCheck(file, e);
    if (syntax) {
      process.stderr.write(`BosskuAI post-edit: syntax error in ${short}. Fix it before doing anything else.\n${syntax.slice(0, 1200)}\n`);
      process.exit(2);
    }

    if (isOff("BOSSKU_SLOP_LINT")) process.exit(0);
    const { hard, soft } = slopLint(file, e);
    if (hard.length) {
      process.stderr.write(
        `BosskuAI anti-slop: ${short} contains banned placeholders: ${hard.join("; ")}. ` +
          "Replace with real names, real copy, and real numbers (or an honest range). " +
          (soft.length ? `Also: ${soft.join("; ")}. ` : "") +
          "Off switch: BOSSKU_SLOP_LINT=off.\n",
      );
      process.exit(2);
    }
    if (soft.length) {
      emit({
        hookSpecificOutput: {
          hookEventName: "PostToolUse",
          additionalContext: `BosskuAI anti-slop (${short}): ${soft.join("; ")}. Fix these unless each one is a deliberate, stated choice.`,
        },
      });
    }
    process.exit(0);
  } catch {
    process.exit(0);
  }
}
