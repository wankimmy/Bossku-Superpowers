"""The skill list Claude Code shows the model is capped by skillListingBudgetFraction x the context window.

`bossku doctor` estimates the list and warns; `install` / `update` --fit-skill-list raises the setting (opt-in).
Facts and links are in bossku/skill_listing.py. Every test uses a temporary home; none touches the real one.
"""

import contextlib
import io
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku import __version__
from bossku.cli import main
from bossku.doctor import format_doctor_success, skill_listing_lines
from bossku.paths import user_config_dir
from bossku.skill_listing import (
    BUDGET_KEY, ENTRY_OVERHEAD, MAX_DESC_KEY, UNSEEN_CHARS, budget_chars, estimate, fit_settings, fraction_that_fits,
)

ROOT = Path(__file__).resolve().parents[1]


def write_skill(folder: Path, name: str, description: str, *, when: str | None = None, hidden: bool = False,
                dirname: str | None = None) -> None:
    lines = ["---", f"name: {name}", f"description: {description}"]
    if when is not None:
        lines.append(f"when_to_use: {when}")
    if hidden:
        lines.append("disable-model-invocation: true")
    skill = folder / (dirname or name)
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text("\n".join([*lines, "---", "", "Body that never counts.", ""]), encoding="utf-8")


def entry(name: str, description_chars: int) -> int:
    return len(name) + ENTRY_OVERHEAD + description_chars


class HomeCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.skills = self.home / ".claude" / "skills"
        self.settings_path = self.home / ".claude" / "settings.json"

    def tearDown(self):
        self.tmp.cleanup()

    def add_many(self, count: int, size: int, prefix: str = "own") -> None:
        for number in range(count):
            write_skill(self.skills, f"{prefix}{number:02d}", "d" * size)

    def add_listing_of(self, count: int, chars: int) -> None:
        """`count` skills whose list entries add up to exactly `chars` (the names are 4 characters long)."""
        size, extra = divmod(chars - count * (4 + ENTRY_OVERHEAD), count)
        for number in range(count):
            write_skill(self.skills, f"s{number:03d}", "d" * (size + (1 if number < extra else 0)))

    def write_settings(self, data: dict) -> None:
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def settings(self) -> dict:
        return json.loads(self.settings_path.read_text(encoding="utf-8"))


class SizeEstimateTests(HomeCase):
    def test_counts_name_description_and_when_to_use_per_skill_and_skips_the_hidden_ones(self):
        write_skill(self.skills, "alpha", "a" * 100)
        write_skill(self.skills, "beta", "b" * 50, when="w" * 30, dirname="beta-folder")   # the name field wins
        write_skill(self.skills, "secret", "s" * 400, hidden=True)
        found = estimate(self.home)
        # description + one space + when_to_use for beta
        self.assertEqual(found["skills"], 2)
        self.assertEqual(found["chars"], entry("alpha", 100) + entry("beta", 50 + 1 + 30))
        self.assertEqual(found["tokens"], found["chars"] // 3)

    def test_one_entry_is_cut_at_1536_characters_by_default_and_at_the_configured_cap(self):
        write_skill(self.skills, "long", "x" * 3000)
        self.assertEqual(estimate(self.home)["chars"], entry("long", 1536))
        self.write_settings({MAX_DESC_KEY: 200})
        found = estimate(self.home)
        self.assertEqual((found["chars"], found["max_desc_chars"]), (entry("long", 200), 200))

    def test_a_project_skill_is_counted_with_doctor_project_and_replaces_a_same_named_user_skill(self):
        write_skill(self.skills, "alpha", "a" * 100)
        project = self.home / "proj"
        write_skill(project / ".claude" / "skills", "alpha", "p" * 10)
        write_skill(project / ".claude" / "skills", "gamma", "g" * 20)
        self.assertEqual(estimate(self.home)["chars"], entry("alpha", 100))
        self.assertEqual(estimate(self.home, project)["chars"], entry("alpha", 10) + entry("gamma", 20))

    def test_with_a_project_its_settings_files_override_the_user_file_local_first(self):
        """Both keys are scope "Any file"; project local beats project beats user (the docs linked in skill_listing)."""
        write_skill(self.skills, "alpha", "a" * 3000)
        project = self.home / "proj"
        (project / ".claude").mkdir(parents=True)

        def save(name, data):
            (project / ".claude" / name).write_text(json.dumps(data), encoding="utf-8")

        self.write_settings({BUDGET_KEY: 0.02, MAX_DESC_KEY: 500})
        found = estimate(self.home, project)                        # no project file sets either key yet
        self.assertEqual((found["fraction"], found["max_desc_chars"], found["fraction_file"]), (0.02, 500, "~/.claude/settings.json"))
        save("settings.json", {BUDGET_KEY: 0.05, MAX_DESC_KEY: 800})
        found = estimate(self.home, project)
        self.assertEqual((found["fraction"], found["max_desc_chars"]), (0.05, 800))
        self.assertEqual(found["fraction_file"], "the project's .claude/settings.json")
        self.assertFalse(found["fraction_is_default"])
        save("settings.local.json", {BUDGET_KEY: 0.07})
        found = estimate(self.home, project)
        self.assertEqual((found["fraction"], found["max_desc_chars"]), (0.07, 800))   # the cap still comes from the next file
        self.assertEqual(found["fraction_file"], "the project's .claude/settings.local.json")
        save("settings.local.json", {BUDGET_KEY: "lots"})                           # a bad value falls through to the next file
        self.assertEqual(estimate(self.home, project)["fraction"], 0.05)
        found = estimate(self.home)                                                 # without --project only the user file counts
        self.assertEqual((found["fraction"], found["max_desc_chars"]), (0.02, 500))

    def test_no_skills_or_a_broken_settings_file_gives_the_defaults_and_no_doctor_lines(self):
        self.assertEqual(skill_listing_lines(self.home), [])
        self.settings_path.parent.mkdir(parents=True)
        self.settings_path.write_text("{ not json", encoding="utf-8")
        write_skill(self.skills, "alpha", "a" * 10)
        found = estimate(self.home)
        self.assertEqual((found["fraction"], found["fraction_is_default"]), (0.01, True))
        self.assertEqual(found["max_desc_chars"], 1536)

    def test_a_wrongly_typed_setting_is_ignored(self):
        write_skill(self.skills, "alpha", "a" * 10)
        for bad in ("0.5", True, 0, -1, None):
            self.write_settings({BUDGET_KEY: bad, MAX_DESC_KEY: bad})
            with self.subTest(bad=bad):
                found = estimate(self.home)
                self.assertEqual((found["fraction"], found["max_desc_chars"]), (0.01, 1536))

    def test_out_of_range_values_are_ignored(self):
        """The settings reference: the fraction is above 0 and at most 1, the cap is a positive whole number."""
        write_skill(self.skills, "alpha", "a" * 10)
        for bad in (1.5, 2):
            self.write_settings({BUDGET_KEY: bad})
            with self.subTest(fraction=bad):
                self.assertEqual(estimate(self.home)["fraction"], 0.01)
                self.assertEqual(fit_settings(self.home)["status"], "skipped_invalid_value")
        for bad in (0.5, 1.5, 0):
            self.write_settings({MAX_DESC_KEY: bad})
            with self.subTest(cap=bad):
                self.assertEqual(estimate(self.home)["max_desc_chars"], 1536)

    def test_the_measured_machine_needs_0_035_not_0_03(self):
        """Claude Code 2.1.293 logged 98,037 characters for 267 skills where the 238 SKILL.md files estimate to
        81,157. Sizing from the files alone is one step short; the headroom for what bossku cannot see closes it."""
        self.add_listing_of(238, 81_157)
        found = estimate(self.home)
        self.assertEqual((found["skills"], found["chars"]), (238, 81_157))
        self.assertEqual(found["chars"] + UNSEEN_CHARS, 98_037)
        self.assertEqual(fraction_that_fits(found["chars"]), 0.03)       # the files alone: 90,000 characters
        self.assertEqual(found["fit_fraction"], 0.035)                   # what cleared the warning on Opus
        self.write_settings({BUDGET_KEY: 0.03})
        self.assertFalse(estimate(self.home)["models"]["1M"]["fits"])
        self.assertIn("Claude Code would cut about 25 descriptions", "\n".join(skill_listing_lines(self.home)))
        self.write_settings({BUDGET_KEY: 0.035})
        self.assertTrue(estimate(self.home)["models"]["1M"]["fits"])

    def test_the_headroom_counts_for_the_1M_check_only(self):
        self.add_listing_of(10, 5_900)                    # 200K budget at 0.01 is 6,000: the files alone fit
        found = estimate(self.home)
        self.assertTrue(found["models"]["200K"]["fits"])
        self.assertTrue(found["models"]["1M"]["fits"])    # 5,900 + 16,880 is still under 30,000
        self.assertEqual(found["fit_fraction"], 0.01)
        self.assertEqual(found["whole_tokens"], (5_900 + UNSEEN_CHARS) // 3)


class FractionMathsTests(unittest.TestCase):
    def test_budget_is_fraction_times_context_times_three_characters(self):
        self.assertEqual(budget_chars(0.01, 1_000_000), 30_000)        # measured on claude-opus-5-5
        self.assertEqual(budget_chars(0.01, 200_000), 6_000)           # measured on claude-sonnet-5-5 and haiku
        self.assertEqual(budget_chars(0.035, 1_000_000), 105_000)
        self.assertEqual(budget_chars(0.035, 200_000), 21_000)

    def test_the_fit_is_rounded_up_to_the_next_0_005(self):
        cases = {0: 0.005, 1: 0.005, 15_000: 0.005, 15_001: 0.01, 30_000: 0.01, 30_001: 0.015,
                 98_037: 0.035, 105_000: 0.035, 105_001: 0.04}
        for chars, expected in cases.items():
            with self.subTest(chars=chars):
                self.assertEqual(fraction_that_fits(chars), expected)
                self.assertLessEqual(chars, budget_chars(expected, 1_000_000))   # it really holds the list

    def test_no_smaller_step_would_hold_the_list(self):
        for chars in (15_001, 40_400, 98_037):
            smaller = round(fraction_that_fits(chars) - 0.005, 3)
            self.assertGreater(chars, budget_chars(smaller, 1_000_000))


class DoctorMessageTests(HomeCase):
    def test_a_small_list_fits_both_model_sizes(self):
        self.add_many(5, 100)
        lines = skill_listing_lines(self.home)
        text = "\n".join(lines)
        self.assertTrue(lines[0].startswith("  skill listing: about"))
        self.assertNotIn("warning", text)
        self.assertIn("1M-context model: limit 30,000 characters, every description fits", text)
        self.assertIn("200K-context model: limit 6,000 characters, every description fits", text)
        self.assertIn("(the default)", text)
        # the fraction is always named: 550 characters + the headroom for Claude Code's own skills is 0.01
        self.assertIn("A 1M-context model needs skillListingBudgetFraction 0.01: this list plus room for Claude Code's "
                      "own skills (16,880 characters, measured on one machine)", text)
        self.assertEqual(skill_listing_lines(self.home, only_warning=True), [])

    def test_a_list_that_fits_a_1M_model_but_not_a_200K_model_warns_and_counts_the_cuts(self):
        self.add_many(20, 500)                       # 20 x 510 = 10,200 characters
        text = "\n".join(skill_listing_lines(self.home))
        self.assertIn("warning: skill listing: about 10,200 characters", text)
        self.assertIn("1M-context model: limit 30,000 characters, every description fits", text)
        # (10,200 - 6,000) / 500 characters per description = 8.4, so 9
        self.assertIn("200K-context model: limit 6,000 characters, Claude Code would cut about 9 descriptions", text)
        self.assertNotIn("set skillListingBudgetFraction", text)       # a 1M model needs no fix
        self.assertIn("200K-context model needs a fraction 5 times higher", text)

    def test_a_list_too_big_for_both_names_the_fraction_that_fits_a_1M_model(self):
        self.add_many(40, 1000)                      # 40 x 1,010 = 40,400 characters, 57,280 with the headroom
        text = "\n".join(skill_listing_lines(self.home))
        self.assertIn("1M-context model: limit 30,000 characters, Claude Code would cut about 28 descriptions", text)
        self.assertIn("200K-context model: limit 6,000 characters, Claude Code would cut about 35 descriptions", text)
        self.assertIn("set skillListingBudgetFraction to 0.02 in ~/.claude/settings.json", text)   # 57,280 / 3,000,000 = 0.0191
        self.assertIn("A 1M-context model needs skillListingBudgetFraction 0.02:", text)
        self.assertIn("`bossku update --fit-skill-list`", text)
        self.assertNotIn("not this project's skills", text)            # no --project, so nothing to explain
        self.assertIn("costs context: the whole list is sent every session, about 19,093 tokens", text)   # 57,280 / 3
        self.assertIn("No skill is shortened or removed", text)
        self.assertIn("plugins and Claude Code's own bundled skills also count, so the real list can be larger", text)

    def test_with_a_project_the_advice_says_the_flag_sizes_from_the_user_skills_only(self):
        project = self.home / "proj"
        write_skill(project / ".claude" / "skills", "extra", "e" * 100)
        self.add_many(40, 1000)
        text = "\n".join(skill_listing_lines(self.home, project))
        self.assertIn("for 41 skills in ~/.claude/skills and the project's .claude/skills", text)
        self.assertIn("run `bossku update --fit-skill-list` (it sizes from ~/.claude/skills only, not this project's "
                      "skills). That costs context", text)

    def test_a_fraction_set_in_the_project_is_named_and_the_advice_points_at_that_file(self):
        project = self.home / "proj"
        (project / ".claude").mkdir(parents=True)
        (project / ".claude" / "settings.json").write_text(json.dumps({BUDGET_KEY: 0.015}), encoding="utf-8")
        self.add_many(40, 1000)
        self.write_settings({BUDGET_KEY: 0.2})                     # the user file is generous, but the project file wins
        text = "\n".join(skill_listing_lines(self.home, project))
        self.assertIn("skillListingBudgetFraction is 0.015 (from the project's .claude/settings.json)", text)
        self.assertIn("1M-context model: limit 45,000 characters, Claude Code would cut about", text)
        self.assertIn("set skillListingBudgetFraction to 0.02 in the project's .claude/settings.json (`--fit-skill-list` "
                      "only writes ~/.claude/settings.json, and the project file wins over it)", text)
        self.assertNotIn("or run `bossku update", text)
        plain = "\n".join(skill_listing_lines(self.home))          # without --project the user's 0.2 is the answer
        self.assertIn("skillListingBudgetFraction is 0.2", plain)
        self.assertNotIn("from the project", plain)

    def test_the_saved_fraction_is_used_and_shown(self):
        self.add_many(40, 1000)
        self.write_settings({BUDGET_KEY: 0.02})
        text = "\n".join(skill_listing_lines(self.home))
        self.assertIn("skillListingBudgetFraction is 0.02", text)
        self.assertNotIn("(the default)", text)
        self.assertIn("1M-context model: limit 60,000 characters, every description fits", text)
        self.assertIn("200K-context model: limit 12,000 characters, Claude Code would cut about", text)
        self.assertIn("A 1M-context model needs skillListingBudgetFraction 0.02:", text)   # shown even when it fits
        self.assertNotIn("set skillListingBudgetFraction", text)

    def test_doctor_prints_the_line_but_a_warning_does_not_make_it_fail(self):
        self.add_many(40, 1000)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["--home", str(self.home), "--root", str(ROOT), "install", "--profile", "core"])
        self.assertEqual(code, 0)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["--home", str(self.home), "--root", str(ROOT), "doctor"])
        self.assertEqual(code, 0, out.getvalue())
        self.assertIn("warning: skill listing", out.getvalue())
        lines = format_doctor_success(ROOT, self.home, version=__version__)
        self.assertTrue(any(line.startswith("  warning: skill listing") for line in lines))


class FitTests(HomeCase):
    """--fit-skill-list on install and update."""

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["--home", str(self.home), "--root", str(ROOT), *argv])
        return code, out.getvalue()

    def install(self, *argv) -> dict:
        code, out = self.run_cli("install", "--profile", "core", *argv)
        self.assertEqual(code, 0, out)
        return json.loads(out)

    def config(self) -> dict:
        return json.loads((user_config_dir(self.home) / "config.json").read_text(encoding="utf-8"))

    def backups(self) -> list:
        return sorted(self.settings_path.parent.glob("settings.json.bak-*"))

    def setUp(self):
        super().setUp()
        self.add_many(45, 1000)
        self.write_settings({"model": "opus[1m]", "env": {"A": "1"}, "permissions": {"allow": ["Bash(ls)"]}})

    def test_a_plain_install_does_not_touch_the_setting_or_the_config(self):
        result = self.install()
        self.assertNotIn(BUDGET_KEY, self.settings())
        self.assertNotIn("skill_listing", result)
        self.assertNotIn("fit_skill_list", self.config())

    def test_the_flag_sets_the_fraction_that_fits_a_1M_model_and_keeps_every_other_key(self):
        result = self.install("--fit-skill-list")
        found = estimate(self.home)
        saved = self.settings()
        self.assertGreater(saved[BUDGET_KEY], 0.01)
        self.assertEqual(saved[BUDGET_KEY], found["fit_fraction"])
        self.assertTrue(found["models"]["1M"]["fits"])
        self.assertEqual(saved["model"], "opus[1m]")
        self.assertEqual(saved["env"], {"A": "1"})
        self.assertIn("Bash(ls)", saved["permissions"]["allow"])
        self.assertIn("hooks", saved)                                   # the hooks install wrote are still there
        self.assertEqual(result["skill_listing"]["status"], "set")
        self.assertIsNone(result["skill_listing"]["was"])
        self.assertIs(self.config()["fit_skill_list"], True)
        self.assertFalse(self.settings_path.with_name("settings.json.tmp").exists())

    def test_a_change_keeps_exactly_one_copy_of_the_old_file(self):
        for old in self.backups():                                      # install_hooks makes its own on a first install
            old.unlink()
        before = self.settings_path.read_text(encoding="utf-8")
        self.assertEqual(fit_settings(self.home)["status"], "set")
        copies = self.backups()
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].read_text(encoding="utf-8"), before)
        self.assertEqual(fit_settings(self.home)["status"], "already_fits")   # nothing changed, so no second copy
        self.assertEqual(self.backups(), copies)

    def test_a_failed_swap_is_reported_and_leaves_the_file_and_no_temp_file(self):
        before = self.settings_path.read_bytes()
        with mock.patch("bossku.hooks.os.replace", side_effect=PermissionError("settings.json is locked")):
            result = fit_settings(self.home)
        self.assertEqual(result["status"], "failed")
        self.assertIn("settings.json is locked", result["error"])
        self.assertEqual(self.settings_path.read_bytes(), before)
        self.assertFalse(self.settings_path.with_name("settings.json.tmp").exists())

    def test_a_read_only_settings_file_fails_cleanly_and_the_next_run_works(self):
        """A file the user made read-only stays as it is on every OS (POSIX would otherwise swap a new file in), the
        error names it, no backup is left behind, and no .tmp blocks the next run."""
        tmp = self.settings_path.with_name("settings.json.tmp")
        before = self.settings_path.read_bytes()
        backups = set(self.settings_path.parent.glob("settings.json.bak*"))
        os.chmod(self.settings_path, stat.S_IREAD)
        try:
            result = fit_settings(self.home)
            self.assertEqual(result["status"], "failed")
            self.assertIn("settings.json", result["error"])
            self.assertIn("read-only", result["error"])
            self.assertFalse(tmp.exists())
            self.assertEqual(set(self.settings_path.parent.glob("settings.json.bak*")), backups)
            self.assertEqual(self.settings_path.read_bytes(), before)
        finally:
            os.chmod(self.settings_path, stat.S_IWRITE)
        self.assertEqual(fit_settings(self.home)["status"], "set")
        self.assertFalse(tmp.exists())

    def test_a_stale_read_only_temp_file_does_not_block_the_next_run(self):
        tmp = self.settings_path.with_name("settings.json.tmp")
        tmp.write_text("left over from a crash", encoding="utf-8")
        os.chmod(tmp, stat.S_IREAD)
        try:
            self.assertEqual(fit_settings(self.home)["status"], "set")
        finally:
            if tmp.exists():
                os.chmod(tmp, stat.S_IWRITE)
        self.assertFalse(tmp.exists())
        self.assertGreater(self.settings()[BUDGET_KEY], 0.01)

    def test_a_failed_backup_is_reported_and_leaves_the_file(self):
        before = self.settings_path.read_bytes()
        with mock.patch("bossku.skill_listing._backup", side_effect=OSError("disk full")):
            result = fit_settings(self.home)
        self.assertEqual((result["status"], result["error"]), ("failed", "disk full"))
        self.assertEqual(self.settings_path.read_bytes(), before)

    def test_a_lower_saved_value_is_raised(self):
        self.write_settings({BUDGET_KEY: 0.012, "model": "opus[1m]"})
        result = self.install("--fit-skill-list")
        self.assertEqual(result["skill_listing"]["status"], "set")
        self.assertEqual(result["skill_listing"]["was"], 0.012)
        self.assertEqual(self.settings()[BUDGET_KEY], estimate(self.home)["fit_fraction"])

    def test_a_higher_saved_value_is_never_lowered(self):
        self.write_settings({BUDGET_KEY: 0.2, "model": "opus[1m]"})
        result = self.install("--fit-skill-list")
        self.assertEqual(result["skill_listing"]["status"], "already_fits")
        self.assertEqual(self.settings()[BUDGET_KEY], 0.2)

    def test_a_list_that_already_fits_the_default_writes_nothing(self):
        for child in self.skills.glob("own*"):
            (child / "SKILL.md").unlink()
        self.assertEqual(fit_settings(self.home)["status"], "skipped_no_skills")
        write_skill(self.skills, "tiny", "t" * 20)
        before = self.settings_path.read_bytes()
        self.assertEqual(fit_settings(self.home)["status"], "already_fits")
        self.assertEqual(self.settings_path.read_bytes(), before)
        self.assertNotIn(BUDGET_KEY, self.settings())

    def test_running_it_again_changes_nothing(self):
        self.install("--fit-skill-list")
        first, backups = self.settings_path.read_bytes(), self.backups()
        again = self.install("--fit-skill-list")
        self.assertEqual(again["skill_listing"]["status"], "already_fits")
        self.assertEqual(self.settings_path.read_bytes(), first)
        self.assertEqual(self.backups(), backups)

    def test_update_honours_the_saved_choice(self):
        self.install("--fit-skill-list")
        fitted = self.settings()[BUDGET_KEY]
        saved = self.settings()
        del saved[BUDGET_KEY]
        self.write_settings(saved)
        code, out = self.run_cli("update")                              # no flag: the saved choice runs again
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(out)["skill_listing"]["status"], "set")
        self.assertEqual(self.settings()[BUDGET_KEY], fitted)

    def test_update_takes_the_flag_too(self):
        self.install()
        code, out = self.run_cli("update", "--fit-skill-list")
        self.assertEqual(code, 0, out)
        self.assertEqual(self.settings()[BUDGET_KEY], estimate(self.home)["fit_fraction"])
        self.assertIs(self.config()["fit_skill_list"], True)

    def test_no_fit_skill_list_leaves_the_users_value_alone_and_is_remembered(self):
        self.install("--fit-skill-list")
        fitted = self.settings()[BUDGET_KEY]
        result = self.install("--no-fit-skill-list")
        self.assertNotIn("skill_listing", result)
        self.assertIs(self.config()["fit_skill_list"], False)
        self.assertEqual(self.settings()[BUDGET_KEY], fitted)           # not removed, not lowered
        saved = self.settings()
        del saved[BUDGET_KEY]
        self.write_settings(saved)
        self.run_cli("update")                                           # the saved "no" is kept
        self.assertNotIn(BUDGET_KEY, self.settings())
        self.install()
        self.assertNotIn(BUDGET_KEY, self.settings())

    def test_an_unreadable_or_odd_settings_file_is_left_alone(self):
        self.settings_path.write_text("{ not json", encoding="utf-8")
        self.assertEqual(fit_settings(self.home)["status"], "skipped_invalid_json")
        self.assertEqual(self.settings_path.read_text(encoding="utf-8"), "{ not json")
        self.write_settings({BUDGET_KEY: "lots"})
        self.assertEqual(fit_settings(self.home)["status"], "skipped_invalid_value")
        self.assertEqual(self.settings(), {BUDGET_KEY: "lots"})
        empty = self.home / "other"
        self.assertEqual(fit_settings(empty)["status"], "skipped_not_found")
        self.assertFalse(empty.exists())

    def test_a_missing_settings_file_is_created_with_only_the_key(self):
        self.settings_path.unlink()
        self.assertEqual(fit_settings(self.home)["status"], "set")
        self.assertEqual(self.settings(), {BUDGET_KEY: estimate(self.home)["fit_fraction"]})

    def test_the_install_summary_says_what_was_set(self):
        from bossku.cli import _fit_summary

        self.assertIn("set to 0.02", _fit_summary({"status": "set", "fraction": 0.02, "was": None}))
        self.assertIn("was 0.012", _fit_summary({"status": "set", "fraction": 0.02, "was": 0.012}))
        self.assertIn("already enough", _fit_summary({"status": "already_fits", "fraction": 0.2, "needed": 0.02}))
        self.assertIn("not changed (skipped_invalid_json)", _fit_summary({"status": "skipped_invalid_json"}))
        self.assertIn("not changed (failed: locked)", _fit_summary({"status": "failed", "error": "locked"}))


if __name__ == "__main__":
    unittest.main()
