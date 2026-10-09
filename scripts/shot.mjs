#!/usr/bin/env node
// BosskuAI visual verification: screenshot a URL at phone (390x844) and desktop
// (1440x900) so the model can Read the PNGs and look at what it built.
//
//   node scripts/shot.mjs <url> [outDir] [--wait <ms>] [--no-full]
//
// Uses the Playwright CLI (`npx --no playwright screenshot`). `--no` means npx never downloads a package on its
// own: if Playwright or its Chromium build is missing, it says so and prints the one-time install command for
// you to run.
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { isMain } from "../hooks/_lib.mjs";

// How to run npx without handing the URL to a shell. On Windows npx.cmd needs cmd.exe, which would run
// anything after an & in the URL, so call npm's npx-cli.js with node itself. Only when that file is
// missing do we fall back to cmd.exe, and then only for arguments with no shell metacharacters.
export function spawnPlan(cli, { platform = process.platform, execPath = process.execPath, exists = fs.existsSync } = {}) {
  if (platform !== "win32") return { cmd: "npx", args: cli, shell: false };
  const npxCli = path.join(path.dirname(execPath), "node_modules", "npm", "bin", "npx-cli.js");
  if (exists(npxCli)) return { cmd: execPath, args: [npxCli, ...cli], shell: false };
  const bad = cli.find((a) => /[&|<>^"%]/.test(a));
  if (bad) throw new Error(`unsafe argument for cmd.exe: ${bad}`);
  return { cmd: "npx.cmd", args: cli.map((a) => `"${a}"`), shell: true };
}

// The npx arguments for one screenshot. `--no`: npx must refuse to download a missing package, never fetch it unasked.
export function shotArgs({ size, wait, fullPage, url, out }) {
  const cli = ["--no", "playwright", "screenshot", `--viewport-size=${size}`, `--wait-for-timeout=${wait}`];
  if (fullPage) cli.push("--full-page");
  cli.push(url, out);
  return cli;
}

// What to tell the user when npx or Playwright failed, or null when the error is something else.
export function installHint(err) {
  if (/canceled due to missing packages|no YES option/i.test(err)) {
    return "Playwright is not installed in this project. One-time install (run it yourself):\n  npm i -D playwright && npx playwright install chromium";
  }
  if (/Executable doesn't exist|browserType\.launch|install/i.test(err)) {
    return "Playwright browsers are missing. One-time install:\n  npx playwright install chromium";
  }
  return null;
}

function main() {
  const args = process.argv.slice(2);
  const urlArg = args.find((a) => /^https?:\/\//.test(a)) || (args[0] && !args[0].startsWith("--") ? args[0] : null);
  let url = null;
  try {
    // a bare host:port gets http://; any other scheme (file:, javascript:) is refused
    const candidate = urlArg && (/^[a-z][a-z0-9+.-]*:\/\//i.test(urlArg) ? urlArg : `http://${urlArg}`);
    if (candidate && /^https?:$/.test(new URL(candidate).protocol)) url = candidate;
  } catch {
    /* usage below */
  }
  if (!url) {
    console.error("usage: node scripts/shot.mjs <url> [outDir] [--wait <ms>] [--no-full]");
    console.error("example: node scripts/shot.mjs http://localhost:3000");
    process.exit(1);
  }
  const waitIdx = args.indexOf("--wait");
  const wait = waitIdx >= 0 ? String(parseInt(args[waitIdx + 1], 10) || 1500) : "1500";
  const fullPage = !args.includes("--no-full");
  const explicitOut = args.filter((a, i) => !a.startsWith("--") && a !== urlArg && !(waitIdx >= 0 && i === waitIdx + 1))[0];
  const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const outDir = explicitOut || path.join(process.cwd(), ".bossku", "shots", stamp);
  fs.mkdirSync(outDir, { recursive: true });

  const viewports = [
    ["phone-390", "390,844"],
    ["desktop-1440", "1440,900"],
  ];
  const written = [];
  for (const [name, size] of viewports) {
    const out = path.join(outDir, `${name}.png`);
    const cli = shotArgs({ size, wait, fullPage, url, out });
    let plan;
    try {
      plan = spawnPlan(cli);
    } catch (err) {
      console.error(`screenshot not run: ${err.message}`);
      process.exit(2);
    }
    const r = spawnSync(plan.cmd, plan.args, { encoding: "utf8", timeout: 120000, shell: plan.shell });
    if (r.status !== 0 || !fs.existsSync(out)) {
      const err = (r.stderr || r.stdout || "").trim();
      console.error(`screenshot failed for ${name}: ${err.slice(0, 800)}`);
      const hint = installHint(err);
      if (hint) console.error(hint);
      process.exit(2);
    }
    written.push(out);
  }
  console.log(written.join("\n"));
  console.log(
    "\nNow Read both PNGs and check: hero fits the viewport, nothing overflows at 390, CTA visible, no placeholder blocks, spacing rhythm consistent, contrast readable.",
  );
}

if (isMain(import.meta.url)) main();
