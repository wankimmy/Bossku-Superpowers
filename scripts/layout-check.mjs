#!/usr/bin/env node
// BosskuAI layout check: open a page at several widths in Playwright and report layout defects a screenshot
// can hide: sideways scroll, overflow hidden used to cover it, text wider than its box, cut-off text,
// overlapping controls and tiny tap targets. Run it beside scripts/shot.mjs, after you build a page.
//
//   node scripts/layout-check.mjs <url> [--widths 320,375,390,768,1024,1440,1920] [--height 900] [--wait <ms>] [--json]
//
// Exit 0: no error. Exit 1: at least one finding of kind "error". Exit 2: the check could not run.
// Playwright is resolved from the project you run this in (the current directory), not from this repo.
// Nothing is downloaded or installed: if Playwright or its browser is missing, it prints the install command.
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { isMain } from "../hooks/_lib.mjs";
import { installHint } from "./shot.mjs";

export const DEFAULT_WIDTHS = [320, 375, 390, 768, 1024, 1440, 1920];
const MAX_ITEMS = 10;

// Parse the command line. Returns { url, widths, height, wait, json } or { error }.
export function parseArgs(argv) {
  const opts = { url: null, widths: DEFAULT_WIDTHS, height: 900, wait: 500, json: false };
  const num = (v, lo, hi) => (/^\d+$/.test(v ?? "") && +v >= lo && +v <= hi ? +v : null);
  let urlArg = null;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") opts.json = true;
    else if (a === "--widths") {
      const parts = (argv[++i] ?? "").split(",").map((s) => num(s.trim(), 200, 5000));
      if (!parts.length || parts.includes(null)) return { error: "--widths needs a comma list of numbers from 200 to 5000" };
      opts.widths = parts;
    } else if (a === "--height") {
      opts.height = num(argv[++i], 200, 5000);
      if (!opts.height) return { error: "--height needs a number from 200 to 5000" };
    } else if (a === "--wait") {
      opts.wait = num(argv[++i], 0, 60000);
      if (opts.wait === null) return { error: "--wait needs milliseconds from 0 to 60000" };
    } else if (a.startsWith("--")) return { error: `unknown option ${a}` };
    else if (urlArg === null) urlArg = a;
    else return { error: `unexpected argument ${a}` };
  }
  if (!urlArg) return { error: "missing <url>" };
  try {
    // a bare host:port gets http://; any other scheme (file:, javascript:) is refused
    const candidate = /^[a-z][a-z0-9+.-]*:\/\//i.test(urlArg) ? urlArg : `http://${urlArg}`;
    const u = new URL(candidate);
    if (!/^https?:$/.test(u.protocol)) return { error: `only http and https URLs are allowed, got ${u.protocol}` };
    opts.url = u.href;
  } catch {
    return { error: `not a valid URL: ${urlArg}` };
  }
  return opts;
}

// Runs inside the page (Playwright serialises it, so it must use nothing from this file).
// Returns plain data: no DOM nodes.
export function collectGeometry() {
  const de = document.documentElement;
  const SCROLLERS = /^(auto|scroll)$/;
  const CUT = /^(hidden|clip)$/;
  const INTERACTIVE = 'a[href],button,input:not([type="hidden"]),select,textarea,[role="button"],[tabindex]:not([tabindex="-1"])';
  const sel = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += `#${el.id}`;
    else if (typeof el.className === "string" && el.className.trim()) s += "." + el.className.trim().split(/\s+/).slice(0, 2).join(".");
    return s.replace(/[^\w#.:-]/g, "?").slice(0, 60);
  };
  const rendered = (el, cs, r) => {
    if (cs.display === "none" || cs.visibility === "hidden" || cs.visibility === "collapse") return false;
    if (r.width <= 0 || r.height <= 0) return false;
    // visually hidden text (the sr-only pattern): a 1px box that clips its content is not on screen
    if (r.width <= 1 && r.height <= 1 && (CUT.test(cs.overflowX) || (cs.clip && cs.clip !== "auto") || (cs.clipPath && cs.clipPath !== "none"))) return false;
    if (el.closest('[aria-hidden="true"]')) return false;
    if (el.closest("details:not([open])") && !el.closest("summary")) return false;
    return true;
  };
  const ids = new Map();
  const ancestorId = (el) => {
    for (let p = el.parentElement; p; p = p.parentElement) if (ids.has(p)) return ids.get(p);
    return -1;
  };
  const elements = [];
  const all = document.body.querySelectorAll("*");
  const CAP = 5000;
  for (const el of all) {
    if (elements.length >= CAP) break;
    if (/^(script|style|link|meta|head|title|noscript|template|br|svg|path)$/i.test(el.tagName)) continue;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (!rendered(el, cs, r)) continue;
    // a display: contents parent has no box: measure against the first ancestor that has one
    let parent = el.parentElement;
    while (parent && parent !== document.body && getComputedStyle(parent).display === "contents") parent = parent.parentElement;
    const pcs = parent && getComputedStyle(parent);
    const pr = parent && parent.getBoundingClientRect();
    let fixed = false;
    for (let p = el; p; p = p.parentElement) if (getComputedStyle(p).position === "fixed") { fixed = true; break; }
    let inScroller = false;
    for (let p = parent; p && p !== document.body && p !== de; p = p.parentElement) {
      const c = getComputedStyle(p);
      if (SCROLLERS.test(c.overflowX) || CUT.test(c.overflowX)) { inScroller = true; break; }
    }
    const px = (v) => parseFloat(v) || 0;
    const ownText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    const own = (el.textContent || "").replace(/\s+/g, " ").trim();
    // an inline link sits in a sentence: the parent has text of its own outside any link
    let outside = "";
    if (el.tagName === "A" && cs.display === "inline" && parent) for (const n of parent.childNodes) if (n.nodeType === 3 || (n.nodeType === 1 && n.tagName !== "A")) outside += n.textContent;
    const inlineLink = outside.replace(/\s+/g, " ").trim().length > 3;
    ids.set(el, elements.length);
    elements.push({
      id: elements.length,
      parent: ancestorId(el),
      tag: el.tagName.toLowerCase(),
      sel: sel(el),
      rect: { l: r.left + scrollX, t: r.top + scrollY, r: r.right + scrollX, b: r.bottom + scrollY },
      pc: pr && {
        l: pr.left + scrollX + px(pcs.borderLeftWidth) + px(pcs.paddingLeft),
        r: pr.right + scrollX - px(pcs.borderRightWidth) - px(pcs.paddingRight),
      },
      pScrolls: !!pcs && SCROLLERS.test(pcs.overflowX),
      pInline: !!pcs && pcs.display === "inline",
      fixed,
      positioned: cs.position === "fixed" || cs.position === "absolute",
      inScroller,
      interactive: el.matches(INTERACTIVE),
      inlineLink,
      hasText: own.length > 0,
      ownText,
      leaf: el.children.length === 0,
      display: cs.display,
      overflowX: cs.overflowX,
      overflowY: cs.overflowY,
      scrollW: el.scrollWidth,
      scrollH: el.scrollHeight,
      clientW: el.clientWidth,
      clientH: el.clientHeight,
      ellipsis: cs.textOverflow === "ellipsis",
      clamp: !!cs.webkitLineClamp && cs.webkitLineClamp !== "none",
    });
  }
  return {
    viewport: { width: de.clientWidth },
    docWidth: de.scrollWidth,
    htmlOverflowX: getComputedStyle(de).overflowX,
    bodyOverflowX: getComputedStyle(document.body).overflowX,
    elements,
    truncated: all.length > CAP && elements.length >= CAP,
    total: all.length,
    measured: elements.length,
  };
}

const r1 = (n) => Math.round(n * 10) / 10;

// Judge one page's geometry (the output of collectGeometry). Pure: no browser needed.
// Returns { width, errors, warnings, infos, findings, more } where findings hold at most 10 items per check.
export function judgeLayout(geom, width = Number(geom.viewport.width) || 0) {
  const vw = Number(geom.viewport.width) || 0;
  const els = (geom.elements || []).map((e) => ({ ...e, sel: String(e.sel ?? "").replace(/[^\w#.:-]/g, "?").slice(0, 60) }));
  const all = [];
  const add = (check, kind, selector, message, extra = {}) => all.push({ check, kind, selector, message, ...extra });

  const past = els
    .filter((e) => !e.inScroller && !e.fixed && e.rect.r > vw + 1)
    .map((e) => ({ e, over: r1(e.rect.r - vw) }))
    .sort((a, b) => b.over - a.over);
  const widest = Math.max(geom.docWidth || 0, ...past.map((p) => Math.ceil(p.e.rect.r)));
  const wider = widest > vw + 1;
  if (wider) {
    add("page_overflow_x", "error", "html", `page is ${r1(widest - vw)}px wider than the ${vw}px viewport`, { overshoot: r1(widest - vw) });
    for (const { e, over } of past) add("page_overflow_x", "error", e.sel, `right edge passes the viewport by ${over}px`, { overshoot: over });
  }
  const cutX = (v) => v === "hidden" || v === "clip";
  if (wider && (cutX(geom.htmlOverflowX) || cutX(geom.bodyOverflowX))) {
    const who = cutX(geom.htmlOverflowX) ? "html" : "body";
    add("hidden_overflow_x", "error", who, `${who} has overflow-x ${cutX(geom.htmlOverflowX) ? geom.htmlOverflowX : geom.bodyOverflowX} while content is ${r1(widest - vw)}px wider: hiding the overflow is the defect, fix the wide element`);
  }

  const byId = new Map(els.map((e) => [e.id, e]));
  const BOXES = new Set(["input", "button", "img", "select", "textarea", "video"]);
  for (const e of els) {
    if (e.positioned || e.pScrolls || e.pInline || !e.pc) continue;
    const box = BOXES.has(e.tag) || e.ownText;
    if (box && (e.rect.r > e.pc.r + 1 || e.rect.l < e.pc.l - 1)) {
      const over = r1(Math.max(e.rect.r - e.pc.r, e.pc.l - e.rect.l));
      add("element_overflow", "error", e.sel, `box passes its container by ${over}px`, { overshoot: over });
    } else if (e.ownText && e.leaf && e.overflowX === "visible" && e.display !== "inline" && e.scrollW > e.clientW + 1) {
      add("element_overflow", "error", e.sel, `text is ${e.scrollW - e.clientW}px wider than its own box`, { overshoot: e.scrollW - e.clientW });
    }
  }

  for (const e of els) {
    if (/^(html|body|input|textarea|select)$/.test(e.tag) || !e.ownText) continue;
    const cut = (e.overflowX === "hidden" || e.overflowX === "clip") || (e.overflowY === "hidden" || e.overflowY === "clip");
    if (!cut) continue;
    const dx = e.scrollW - e.clientW;
    const dy = e.scrollH - e.clientH;
    if (!((e.overflowX === "hidden" || e.overflowX === "clip") && dx > 1) && !((e.overflowY === "hidden" || e.overflowY === "clip") && dy > 1)) continue;
    if (e.ellipsis || e.clamp) add("clipped_text", "info", e.sel, "text is cut on purpose (ellipsis or line clamp)");
    else add("clipped_text", "error", e.sel, `text is cut off (${Math.max(dx, dy)}px hidden) with no ellipsis and no line clamp`);
  }

  const isAncestor = (a, b) => {
    for (let p = byId.get(b)?.parent; p !== undefined && p >= 0; p = byId.get(p)?.parent) if (p === a) return true;
    return false;
  };
  const inter = els.filter((e) => e.interactive);
  for (let i = 0; i < inter.length; i++) {
    for (let j = i + 1; j < inter.length; j++) {
      const a = inter[i];
      const b = inter[j];
      const w = Math.min(a.rect.r, b.rect.r) - Math.max(a.rect.l, b.rect.l);
      const h = Math.min(a.rect.b, b.rect.b) - Math.max(a.rect.t, b.rect.t);
      if (w <= 0 || h <= 0 || w * h <= 4) continue;
      if (a.fixed !== b.fixed) continue; // a fixed bar over the page content is a layout choice, not a clash
      if (isAncestor(a.id, b.id) || isAncestor(b.id, a.id)) continue;
      add("overlap", "error", `${a.sel} / ${b.sel}`, `interactive boxes overlap by ${r1(w * h)} square px`);
    }
  }

  for (const e of inter) {
    if (e.inlineLink) continue;
    const w = e.rect.r - e.rect.l;
    const h = e.rect.b - e.rect.t;
    if (w < 24 || h < 24) add("small_target", "warning", e.sel, `target is ${r1(w)}x${r1(h)}px, under 24x24 (WCAG 2.5.8)`);
  }

  if (geom.truncated) add("coverage", "warning", "page", `only the first ${Number(geom.measured) || 0} of ${Number(geom.total) || 0} elements were checked, so this width is not clean`);

  const out = { width, errors: 0, warnings: 0, infos: 0, findings: [], more: {} };
  const seen = {};
  for (const f of all) {
    out[f.kind === "error" ? "errors" : f.kind === "warning" ? "warnings" : "infos"]++;
    seen[f.check] = (seen[f.check] || 0) + 1;
    if (seen[f.check] <= MAX_ITEMS) out.findings.push(f);
    else out.more[f.check] = (out.more[f.check] || 0) + 1;
  }
  return out;
}

// 0 when no width has an error, else 1. Warnings and infos never fail the check.
export function exitCode(results) {
  return results.some((r) => r.errors > 0) ? 1 : 0;
}

export const FOOTER = "A clean result is not proof the page looks right. Still look at screenshots (node scripts/shot.mjs <url>).";

export function formatPlain(results) {
  const lines = [];
  for (const r of results) {
    const counts = {};
    for (const f of r.findings) counts[f.check] = (counts[f.check] || 0) + 1;
    for (const [k, n] of Object.entries(r.more)) counts[k] += n;
    const summary = Object.entries(counts).map(([k, n]) => `${k} ${n}`).join(", ");
    lines.push(`${r.width}px: ${summary || "clean"}`);
    for (const f of r.findings) lines.push(`  [${f.kind}] ${f.check}: ${f.selector}: ${f.message}`);
    for (const [k, n] of Object.entries(r.more)) lines.push(`  ... and ${n} more ${k}`);
  }
  lines.push("", FOOTER);
  return lines.join("\n");
}

const MISSING_PW = "Playwright is not installed in this project. One-time install (run it yourself):\n  npm i -D playwright && npx playwright install chromium";

// Load Playwright from the project in `cwd`. `resolve` is injectable for tests.
export async function loadPlaywright({ cwd = process.cwd(), resolve = (id, from) => createRequire(path.join(from, "noop.js")).resolve(id) } = {}) {
  const file = resolve("playwright", cwd);
  return import(pathToFileURL(file).href);
}

// Whole run, no process.exit and no printing: returns { code, stdout, stderr }.
// A page-thrown message is untrusted: one line, no control or line-separator characters, bounded.
const oneLine = (err) => String(err?.message || err).split("\n")[0].replace(/[\x00-\x1f\x7f-\x9f\u2028\u2029]/g, " ").slice(0, 300);

export async function run(argv, deps = {}) {
  const opts = parseArgs(argv);
  if (opts.error) return { code: 2, stdout: "", stderr: `layout check not run: ${opts.error}\nusage: node scripts/layout-check.mjs <url> [--widths 320,375,...] [--height 900] [--wait <ms>] [--json]` };
  let pw;
  try {
    pw = await (deps.loadPlaywright || loadPlaywright)();
  } catch {
    return { code: 2, stdout: "", stderr: `layout check not run: Playwright cannot be resolved from ${process.cwd()}\n${MISSING_PW}` };
  }
  const chromium = (pw.chromium || pw.default?.chromium);
  let browser;
  try {
    browser = await chromium.launch();
  } catch (err) {
    const msg = String(err?.message || err);
    return { code: 2, stdout: "", stderr: `layout check not run: browser did not start: ${msg.split("\n")[0]}\n${installHint(msg) || "One-time install:\n  npx playwright install chromium"}` };
  }
  const results = [];
  try {
    for (const width of opts.widths) {
      const ctx = await browser.newContext({ viewport: { width, height: opts.height } });
      const page = await ctx.newPage();
      try {
        const resp = await page.goto(opts.url, { waitUntil: "load", timeout: 30000 });
        if (!resp || resp.status() >= 400) throw new Error(`HTTP ${resp ? resp.status() : "no response"}`);
      } catch (err) {
        return { code: 2, stdout: "", stderr: `layout check not run: page failed to load at ${width}px: ${oneLine(err)}` };
      }
      if (opts.wait) await page.waitForTimeout(opts.wait);
      const geom = await page.evaluate(collectGeometry);
      if (!geom.elements?.length) return { code: 2, stdout: "", stderr: `layout check not run: no elements were measured at ${width}px (empty page?)` };
      results.push(judgeLayout(geom, width));
      await ctx.close();
    }
  } catch (err) {
    return { code: 2, stdout: "", stderr: `layout check not run: ${oneLine(err)}` };
  } finally {
    await browser.close().catch(() => {});
  }
  const stdout = opts.json ? JSON.stringify({ url: opts.url, results, note: FOOTER }, null, 2) : formatPlain(results);
  return { code: exitCode(results), stdout, stderr: "" };
}

async function main() {
  const r = await run(process.argv.slice(2));
  if (r.stdout) console.log(r.stdout);
  if (r.stderr) console.error(r.stderr);
  process.exitCode = r.code;
}

if (isMain(import.meta.url)) main();
