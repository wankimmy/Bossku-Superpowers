from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from bossku import __version__
from bossku.doctor import format_doctor_success, gather_doctor_issues
from bossku.hooks import install_hooks, run_sync_hook, uninstall_hooks
from bossku.brief import memory_brief, session_output
from bossku.gate import gate_output
from bossku.hint import hook_output
from bossku.init_project import init_project
from bossku.install import install_user, uninstall_user, update_user
from bossku.memory import load_user_config, memory_directory, memory_project_root, remember, sync_project
from bossku.index import load_index, write_index
from bossku.skills import (
    audit_skills,
    locate_skill,
    overdue_packs,
    pack_stocktake,
    rank_skills,
    select_skill_stack,
    _profile_skills,
)
from bossku.validate import validate_repo

def _utf8_output() -> None:
    """Skills contain arrows, dashes and quotes; a Windows pipe defaults to cp1252 and `skills show` would crash."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass   # not a real text stream (a test capture, a closed pipe): leave it alone


def main(argv: list[str] | None = None) -> int:
    _utf8_output()
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--root", type=Path, default=None, help="BosskuAI repo root")
    parent.add_argument("--home", type=Path, default=None, help="Override home for tests")
    # Subcommands accept the same flags, but an unset flag must not overwrite one given before the
    # subcommand (`bossku --home X remember ...` used to fall back to the real home).
    child = argparse.ArgumentParser(add_help=False)
    child.add_argument("--root", type=Path, default=argparse.SUPPRESS, help="BosskuAI repo root")
    child.add_argument("--home", type=Path, default=argparse.SUPPRESS, help="Override home for tests")

    parser = argparse.ArgumentParser(prog="bossku", description="Bossku Superpower toolkit CLI (formerly BosskuAI)", parents=[parent])
    sub = parser.add_subparsers(dest="command", required=True)

    p_install = sub.add_parser("install", help="Install skills to user-level agent dirs", parents=[child])
    p_install.add_argument("--profile", choices=["lean", "core", "full"], default="lean",
                           help="lean (default) lists ~25 skills with short descriptions and keeps the rest "
                                "reachable through bossku skills show; core is the minimal set; full lists everything")
    p_install.add_argument("--vault", type=str, default=None, help="Obsidian vault path")
    p_install.add_argument("--memory-storage", choices=["repo", "obsidian"], default=None,
                           help="primary memory storage (obsidian keeps memory outside repos)")

    p_init = sub.add_parser("init", help="Initialize project adapter", parents=[child])
    p_init.add_argument("project", type=Path)
    p_init.add_argument("--portable", action="store_true")
    p_init.add_argument("--profile", choices=["lean", "core", "full"], default="core")

    sub.add_parser("update", help="Refresh user-level skills from repo", parents=[child])
    p_doctor = sub.add_parser("doctor", help="Check install health", parents=[child])
    p_doctor.add_argument(
        "--project",
        type=Path,
        default=None,
        help="Also verify project AGENTS.md + CLAUDE.md adapters",
    )

    p_remember = sub.add_parser("remember", help="Save curated memory", parents=[child])
    p_remember.add_argument("--kind", required=True, choices=["decision", "plan", "learning", "project"])
    p_remember.add_argument("--project", type=Path, default=Path("."), help="project root (default: current directory)")
    p_remember.add_argument("note")

    p_memory_path = sub.add_parser("memory-path", help="Resolve canonical project memory directory", parents=[child])
    p_memory_path.add_argument("--project", type=Path, default=Path("."))

    p_brief = sub.add_parser("memory-brief", help="Print the newest project notes in one short block", parents=[child])
    p_brief.add_argument("--project", type=Path, default=Path("."))
    p_brief.add_argument("--limit", type=int, default=1000, help="character budget for the brief")
    sub.add_parser("session-brief", help="Internal: SessionStart hook that puts the project notes in context",
                   parents=[child])
    p_sync = sub.add_parser("sync", help="Export project memory to Obsidian", parents=[child])
    p_sync.add_argument("--project", type=Path, default=Path("."), help="project root (default: current directory)")

    p_sync_hook = sub.add_parser(
        "sync-hook",
        help="Internal: run from agent auto-sync hooks; reads project cwd from stdin JSON",
        parents=[child],
    )
    p_sync_hook.add_argument("--project", type=Path, default=None)

    p_hooks = sub.add_parser(
        "hooks", help="Manage denser Obsidian auto-sync hooks (Claude Code, Cursor, Codex, OpenCode)", parents=[child]
    )
    p_hooks_sub = p_hooks.add_subparsers(dest="hooks_cmd", required=True)
    p_hooks_install = p_hooks_sub.add_parser("install", parents=[child])
    p_hooks_install.add_argument(
        "--tools", type=str, default=None, help="comma-separated subset: claude_code,cursor,codex,opencode"
    )
    p_hooks_uninstall = p_hooks_sub.add_parser("uninstall", parents=[child])
    p_hooks_uninstall.add_argument("--tools", type=str, default=None)

    p_vault = sub.add_parser("vault", help="Mirror agent memory and rules into the Obsidian vault, and tidy it", parents=[child])
    p_vault_sub = p_vault.add_subparsers(dest="vault_cmd", required=True)
    p_vault_sync = p_vault_sub.add_parser("sync", help="Mirror auto-memory, rules and legacy notes now", parents=[child])
    p_vault_sync.add_argument("--project", type=Path, default=Path("."), help="project folder (default: here)")
    p_vault_tidy = p_vault_sub.add_parser("tidy", help="Show what a clean-up would do; --apply does it (zip backup first, nothing deleted)",
                                          parents=[child])
    p_vault_tidy.add_argument("--apply", action="store_true")

    p_tools = sub.add_parser("tools", help="See which optional tools are installed, and install the safe ones on request",
                             parents=[child])
    p_tools_sub = p_tools.add_subparsers(dest="tools_cmd", required=True)
    p_tools_list = p_tools_sub.add_parser("list", help="Every known tool with its status", parents=[child])
    p_tools_list.add_argument("--json", dest="as_json", action="store_true")
    p_tools_list.add_argument("--project", type=Path, default=None, help="project folder for per-project tools (default: here)")
    p_tools_install = p_tools_sub.add_parser(
        "install", help="Show the install plan for a tool; run it only with --yes", parents=[child])
    p_tools_install.add_argument("tool", help="tool id, see `bossku tools list`")
    p_tools_install.add_argument("--yes", action="store_true", help="run the plan (pip and npm tools only)")
    p_tools_install.add_argument("--project", type=Path, default=None, help="project folder for per-project tools (default: here)")

    p_find = sub.add_parser("skills", help="Skill utilities", parents=[child])
    p_find_sub = p_find.add_subparsers(dest="skills_cmd", required=True)
    p_find_cmd = p_find_sub.add_parser("find", parents=[child])
    p_find_cmd.add_argument("task")
    p_find_cmd.add_argument("--limit", type=int, default=5, help="shortlist size")
    p_find_cmd.add_argument("--profile", choices=["lean", "core", "full"], default=None,
                            help="limit automatic selection to an installed skill profile")
    p_show = p_find_sub.add_parser("show", help="Print a skill's SKILL.md (works for library skills the host does not list)",
                                   parents=[child])
    p_show.add_argument("skill_id")
    p_show.add_argument("--max-chars", type=int, default=16000,
                        help="cap the output; the header names the full file path (0 = no cap)")
    p_find_sub.add_parser("index", help="Rebuild skills/skill-index.json", parents=[child])
    p_stock = p_find_sub.add_parser(
        "stocktake", help="Age vendored packs against the review window", parents=[child]
    )
    p_stock.add_argument("--strict", action="store_true", help="exit 1 when a pack is overdue")
    p_stock.add_argument("--json", action="store_true", dest="as_json")
    p_audit = p_find_sub.add_parser(
        "audit", help="Measure skill context size and integrity", parents=[child]
    )
    p_audit.add_argument("--json", action="store_true", dest="as_json")

    sub.add_parser("verify-gate", help="Internal: Stop hook that sends the agent back to run its code once",
                   parents=[child])
    sub.add_parser("skill-hint", help="Internal: UserPromptSubmit hook that suggests skills for the prompt on stdin",
                   parents=[child])
    sub.add_parser("validate", help="Validate repository layout", parents=[child])
    p_uninstall = sub.add_parser("uninstall", help="Remove user-level BosskuAI skills", parents=[child])
    p_uninstall.add_argument("--purge", action="store_true")

    args = parser.parse_args(argv)
    root = args.root
    home = args.home

    try:
        if args.command == "install":
            result = install_user(root=root, home=home, profile=args.profile, vault=args.vault,
                                  memory_storage=args.memory_storage)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "init":
            result = init_project(args.project, root=root, home=home, portable=args.portable, profile=args.profile)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "update":
            result = update_user(root=root, home=home)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "doctor":
            return _doctor(root, home, getattr(args, "project", None))
        if args.command == "remember":
            result = remember(args.project, args.kind, args.note, home=home)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "memory-path":
            print(json.dumps({"memory_dir": str(memory_directory(args.project, home=home)),
                              "project_root": str(memory_project_root(args.project, home=home))}, indent=2))
            return 0
        if args.command == "memory-brief":
            brief = memory_brief(args.project, home=home, limit=args.limit)
            print(brief if brief else "No project notes yet.")
            return 0
        if args.command == "session-brief":
            payload = session_output("" if sys.stdin.isatty() else sys.stdin.read(), home=home)
            if payload:
                print(json.dumps(payload))
            return 0
        if args.command == "sync":
            result = sync_project(args.project, home=home)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "sync-hook":
            result = run_sync_hook(project=args.project, home=home)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "hooks":
            tools = tuple(args.tools.split(",")) if args.tools else None
            if args.hooks_cmd == "install":
                result = install_hooks(home=home, tools=tools)
            else:
                result = uninstall_hooks(home=home, tools=tools)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "vault":
            return _vault(args, home)
        if args.command == "tools":
            return _tools(args, home)
        if args.command == "skills":
            if args.skills_cmd == "find":
                profile = args.profile or load_user_config(home).get("profile", "full")
                matches = rank_skills(args.task, root, limit=max(args.limit, 1))
                # The lean profile lists a few skills but keeps the whole library one `show` away.
                available = None if profile == "lean" else set(_profile_skills(profile, root))
                selection = select_skill_stack(args.task, root, limit=max(args.limit, 1), available=available)
                for row in selection["selected"]:
                    kind, path = locate_skill(row["skill_id"], root, home)
                    row["access"] = kind
                    row["path"] = str(path) if path else None
                    row["load_with"] = (f"bossku skills show {row['skill_id']}" if kind in {"library", "repo"}
                                        else "Skill tool, or read the path")
                stack = [(row["skill_id"], row["score"]) for row in selection["selected"]]
                sid = selection["primary"]
                score = stack[0][1] if stack else 0.0
                user_only = sorted(
                    {row["skill_id"] for row in selection["deferred"]
                     if row["reason"].startswith("requires user invocation")}
                )
                extra = (
                    {
                        "user_invoked": user_only,
                        "user_invoked_note": "Slash commands only: ask the user to run /<id>; "
                        "never load these through the Skill tool.",
                    }
                    if user_only
                    else {}
                )
                print(
                    json.dumps(
                        {
                            "skill_id": sid,
                            "score": score,
                            # Lexical matching is a fallback, not an oracle: say so when the
                            # top hit is weak or barely beats the next one, and read the
                            # shortlist instead of trusting skill_id.
                            "confident": selection["confident"],
                            "matches": [
                                {"skill_id": s, "score": round(v, 3)} for s, v in matches
                            ],
                            "recommended_stack": [
                                {"skill_id": s, "score": round(v, 3)} for s, v in stack
                            ],
                            "selection": selection,
                            "profile": profile,
                            "stack_note": (
                                "Selected primary and complements, with overlap and inventory checks. "
                                "Read selection reasons and descriptions; matches are search candidates."
                            ),
                            **extra,
                        },
                        indent=2,
                    )
                )
            elif args.skills_cmd == "show":
                kind, path = locate_skill(args.skill_id, root, home)
                if path is None:
                    print(f"error: no skill named {args.skill_id}", file=sys.stderr)
                    return 2
                body = path.read_text(encoding="utf-8")
                cap = args.max_chars
                clipped = bool(cap) and len(body) > cap
                print(f"# skill: {args.skill_id} ({kind}) path: {path}")
                print(body[:cap] if clipped else body)
                if clipped:
                    print(f"\n[output cut at {cap} of {len(body)} chars; read {path} for the rest]")
                return 0
            elif args.skills_cmd == "index":
                dest = write_index(root)
                print(json.dumps({"index": str(dest)}, indent=2))
            elif args.skills_cmd == "stocktake":
                return _stocktake(root, strict=args.strict, as_json=args.as_json)
            elif args.skills_cmd == "audit":
                return _skill_audit(root, as_json=args.as_json)
            return 0
        if args.command in ("verify-gate", "skill-hint"):
            # Hooks never fail the user's session: exit code 2 would block the prompt or the stop, so any error is silent.
            try:
                text = _hook_stdin()
                result = (gate_output(text) if args.command == "verify-gate"
                          else hook_output(text, root=root, home=home))
                if result:
                    print(json.dumps(result))
            except Exception:  # noqa: BLE001
                pass
            return 0
        if args.command == "validate":
            errors = validate_repo(root)
            if errors:
                for err in errors:
                    print(err, file=sys.stderr)
                return 1
            print("validate: ok")
            # A pack going stale is a prompt to review, not a broken repo: warn, stay green.
            stale = overdue_packs(root)
            if stale:
                print(
                    f"warning: {len(stale)} vendored pack(s) due for review "
                    f"({', '.join(stale)}); run `bossku skills stocktake`"
                )
            return 0
        if args.command == "uninstall":
            result = uninstall_user(root=root, home=home, purge=args.purge)
            print(json.dumps(result, indent=2))
            return 0
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


def _vault(args, home) -> int:
    from collections import Counter

    from bossku import vault

    if args.vault_cmd == "sync":
        print(json.dumps(vault.sync(args.project, home=home, force=True), indent=2))
        return 0
    plan = vault.plan_tidy(home=home)
    if not plan:
        print("Nothing to tidy (or no vault is configured).")
        return 0
    counts = Counter(step["action"] for step in plan)
    for step in plan:
        print(f"{step['action']:20s} {step['source']}" + (f"\n{'':20s} -> {step['target']}" if step["target"] else "") + f"\n{'':20s}    ({step['why']})")
    print("\n" + ", ".join(f"{n} {a}" for a, n in sorted(counts.items())))
    if not args.apply:
        print("Nothing was changed. Run again with --apply: a zip backup is made first and no note is deleted.")
        return 0
    result = vault.apply_tidy(plan, home=home)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "ok" else 1


def _tools(args, home=None) -> int:
    from bossku import tools

    project = getattr(args, "project", None)
    if args.tools_cmd == "list":
        rows = tools.status_table(project, home)
        if getattr(args, "as_json", False):
            print(json.dumps(rows, indent=2))
            return 0
        print(f"{'tool':20s} {'status':10s} {'how':12s} what it is for")
        for row in rows:
            print(f"{row['id']:20s} {'installed' if row['installed'] else 'missing':10s} {row['kind']:12s} {row['purpose']}")
        print("\nNothing is installed unless you run `bossku tools install <tool> --yes`.")
        return 0
    tool = tools.BY_ID.get(args.tool)
    if tool is None:
        print(f"unknown tool {args.tool!r}; known: {', '.join(tools.BY_ID)}", file=sys.stderr)
        return 2
    info = tools.describe(tool, project, home)
    print(f"{tool.title}: {'already installed' if info['installed'] else 'not installed'}. {tool.purpose}.")
    if tool.note:
        print(f"Note: {tool.note}")
    print("Plan:" if info["automatic"] else "Install by hand:")
    for step in info["install"]:
        print(f"  {step}")
    if not args.yes:
        print("\nNothing was run. Add --yes to run the plan." if info["automatic"] else "")
        return 0
    result = tools.run_install(tool, project=project)
    print(result["message"])
    return 0 if result["ok"] else 1


def _hook_stdin() -> str:
    """The hook payload as UTF-8 text: a Windows pipe would otherwise decode it with the console code page."""
    if sys.stdin.isatty():
        return ""
    raw = getattr(sys.stdin, "buffer", None)
    return raw.read().decode("utf-8", errors="replace") if raw is not None else sys.stdin.read()


def _stocktake(root: Path | None, *, strict: bool = False, as_json: bool = False) -> int:
    rows = pack_stocktake(root)
    if as_json:
        print(json.dumps(rows, indent=2))
    else:
        print(f"{'PACK':<20}{'SKILLS':>7}{'LAST SYNCED':>14}{'AGE':>7}  STATUS")
        for r in rows:
            age = "never" if r["age_days"] is None else f"{r['age_days']}d"
            status = "OVERDUE" if r["overdue"] else "ok"
            print(f"{r['pack']:<20}{r['skills']:>7}{r['last_synced'] or '-':>14}{age:>7}  {status}")
        overdue = [r for r in rows if r["overdue"]]
        window = rows[0]["review_days"] if rows else 0
        print()
        if overdue:
            print(f"{len(overdue)} pack(s) past the {window}-day review window:")
            for r in overdue:
                print(f"  {r['pack']}: re-vendor from {r['upstream'] or 'upstream'}, "
                      f"then update last_synced in skills/vendored.json")
        else:
            print(f"all {len(rows)} packs within the {window}-day review window.")
        print("note: dates are recorded syncs, not a live upstream check.")
    return 1 if strict and any(r["overdue"] for r in rows) else 0


def _skill_audit(root: Path | None, *, as_json: bool = False) -> int:
    report = audit_skills(root)
    if as_json:
        print(json.dumps(report, indent=2))
        return 0
    print(
        f"skills: {report['skill_count']} "
        f"({report['custom_count']} custom, {report['vendored_count']} vendored)"
    )
    print(
        f"always-loaded descriptions: {report['description_chars']} chars "
        f"(~{report['approx_description_tokens']} tokens)"
    )
    print(
        f"custom descriptions: {report['custom_description_chars']} chars "
        f"(~{report['approx_custom_description_tokens']} tokens)"
    )
    print(f"descriptions over 300 chars: {len(report['descriptions_over_300_chars'])}")
    print(f"skill bodies over 500 words: {len(report['bodies_over_500_words'])}")
    print(f"broken relative links: {len(report['broken_relative_links'])}")
    if report["broken_relative_links_by_pack"]:
        detail = ", ".join(
            f"{pack}={count}"
            for pack, count in report["broken_relative_links_by_pack"].items()
        )
        print(f"broken relative links by pack: {detail}")
    print(f"custom broken relative links: {len(report['custom_broken_relative_links'])}")
    return 0


def _doctor(root: Path | None, home: Path | None, project: Path | None = None) -> int:
    issues = gather_doctor_issues(root, home, project=project)
    if issues:
        print("doctor: issues found")
        for item in issues:
            print(f"  - {item}")
        return 1
    for line in format_doctor_success(root, home, version=__version__, project=project):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
