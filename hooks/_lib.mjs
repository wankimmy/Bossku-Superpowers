// Shared helpers for BosskuAI plugin hooks. Every hook is fail-open: any internal
// error exits 0 so a hook bug can never wedge a session.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function readStdinJson() {
  try {
    const raw = fs.readFileSync(0, "utf8");
    return raw.trim() ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export function emit(obj) {
  process.stdout.write(JSON.stringify(obj));
}

export function isOff(name) {
  const v = process.env[name];
  return v === "off" || v === "0" || v === "false";
}

// Split a shell command line into segments on &&, ||, ;, | and a lone & (not the &
// of 2>&1, <& or &>) so each simple command is judged on its own (a safe
// `git status && git reset --hard` still contains a destructive segment).
export function segments(cmd) {
  return String(cmd)
    .replace(/\r?\n/g, " ; ")
    .split(/\s*(?:&&|\|\||;|\||(?<![<>&])&(?![>&]))\s*/)
    .map((s) => s.trim())
    .filter(Boolean);
}

export function toPosix(p) {
  return String(p || "").replace(/\\/g, "/");
}

export function ext(filePath) {
  const p = toPosix(filePath).toLowerCase();
  if (p.endsWith(".blade.php")) return "blade.php";
  const base = p.split("/").pop() || "";
  if (base === "dockerfile" || base === "makefile") return base;
  const i = base.lastIndexOf(".");
  return i >= 0 ? base.slice(i + 1) : "";
}

// True when this module is the script node was started with. realpath on both sides
// so a junction or symlink invocation still counts, and a look-alike name
// (probe-guard.mjs importing guard.mjs) does not.
export function isMain(importMetaUrl) {
  try {
    const argv1 = process.argv[1];
    if (!argv1) return false;
    const self = fileURLToPath(importMetaUrl);
    return argv1 === self || fs.realpathSync.native(argv1) === fs.realpathSync.native(self);
  } catch {
    return false;
  }
}

// Folder that holds hooks/ and scripts/: the plugin env var when the host sets it,
// else derived from the calling module so settings.json installs get a real path too.
export function pluginRoot(importMetaUrl) {
  const env = process.env.CLAUDE_PLUGIN_ROOT;
  return toPosix(env || path.resolve(path.dirname(fileURLToPath(importMetaUrl)), ".."));
}

// Every spelling of a path, lowercased with forward slashes: as given, and resolved through links and
// 8.3 short names (a TEMP folder is often C:\Users\ADMINI~1\..., a file path usually is not).
function spellings(p) {
  const abs = path.resolve(p);
  let real = abs;
  try {
    real = fs.realpathSync.native(abs);
  } catch {
    /* does not exist (any more): the plain spelling only */
  }
  return [...new Set([abs, real].map((s) => toPosix(s).replace(/\/+$/, "").toLowerCase()))];
}

function within(p, dir) {
  const dirs = spellings(dir);
  return spellings(p).some((a) => dirs.some((d) => a === d || a.startsWith(d + "/")));
}

// Files that are not part of any project: Claude Code's own config folder (workflow scripts, memory, plans)
// and the OS temp folder. The hooks give them no syntax check, no lint and no "unverified edit". Narrow on
// purpose: /add-dir folders and sibling repos still count, and so does a session that works inside one of
// those folders itself (cwd under the same root).
export function isScratch(file, cwd) {
  try {
    if (!file || !path.isAbsolute(file)) return false;
    const here = cwd && path.isAbsolute(cwd) ? cwd : "";
    return [path.join(os.homedir(), ".claude"), os.tmpdir()].some((root) => within(file, root) && !(here && within(here, root)));
  } catch {
    return false; // fail open: treat it as a normal file
  }
}
