// BosskuAI session context. SessionStart on startup | resume | clear | compact.
//
// Prints the compact harness contract so it reaches the model in every repo the
// plugin is enabled for, including ones with no CLAUDE.md / AGENTS.md adapter and
// after /compact wipes earlier context. Kept short on purpose: the full contract
// lives in AGENTS.md; this is the reminder, not the manual.
import fs from "node:fs";
import path from "node:path";
import { pluginRoot, readStdinJson } from "./_lib.mjs";

// `bossku init` writes .bossku/DESIGN.md with this status line until the designer contract fills it in.
const STUB = /^Status: STUB\b/m;

// The first real design file, so an unfilled stub never hides the project's own DESIGN.md or design/DESIGN.md.
// With only a stub, say so: { rel, stub: true }. Keep the file list equal to DESIGN_FILES in bossku/init_project.py.
function designFile(cwd) {
  let stub = null;
  for (const rel of [".bossku/DESIGN.md", "DESIGN.md", "design/DESIGN.md"]) {
    const p = path.join(cwd, rel);
    try {
      if (!fs.statSync(p).isFile()) continue;
      if (!STUB.test(fs.readFileSync(p, "utf8").slice(0, 2000))) return { rel, stub: false };
      stub = stub || rel;
    } catch {
      /* next */
    }
  }
  return stub ? { rel: stub, stub: true } : null;
}

try {
  const input = readStdinJson();
  const cwd = input.cwd || process.cwd();
  const root = pluginRoot(import.meta.url);
  const design = designFile(cwd);
  const memory = fs.existsSync(path.join(cwd, ".bossku", "memory"));
  const lines = [
    "[BosskuAI harness active]",
    "- Start every response with the [BOSSKUAI] indicator (Skill / Agent: orchestrator|planner|designer|executor|auditor|final-reviewer|clarification / Model Role / Memory Used).",
    "- Route to one primary skill first. Landing or marketing UI: bosskuai-taste; dashboards, app screens, and product UI: bosskuai-ui-ux-design-to-code. State a one-line Design Read, then build. Motion: animate (web) or animate-expo.",
    !design
      ? "- No DESIGN.md in this repo. For anything beyond a one-off page, have the designer contract write .bossku/DESIGN.md first."
      : design.stub
        ? `- ${design.rel} is still an unfilled stub. For anything beyond a one-off page, have the designer contract fill it in first.`
        : `- Design source of truth: ${design.rel}. Read it before any UI change; keep tokens, type, and components consistent with it.`,
    "- Ponytail: simplest thing that works. Never lazy about validation, security, accessibility, or data loss.",
    "- Gates enforced by hooks: destructive commands are denied (hand them to the user with recovery steps); slop is linted on write; a turn that edits source cannot end until a verification command ran, or you state exactly what is unverified.",
    `- UI edits: screenshot 390 and 1440 with node "${root}/scripts/shot.mjs" <url> and look at both before claiming done.`,
    memory
      ? "- Project memory: .bossku/memory (read when the task touches prior decisions; save with `bossku remember`)."
      : '- Save durable decisions with `bossku remember --project . --kind decision "..."`.',
    '- Off switch for the disciplines: "normal mode".',
  ];
  process.stdout.write(lines.join("\n") + "\n");
} catch {
  /* fail open */
}
process.exit(0);
