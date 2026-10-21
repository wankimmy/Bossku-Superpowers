import json
import unittest
from pathlib import Path

from bossku.design import PRODUCT_REMINDER, WEB_REMINDER, design_reminder
from bossku.hint import hook_output
from bossku.skills import select_skill_stack

ROOT = Path(__file__).resolve().parents[1]


class DesignReminderTests(unittest.TestCase):
    def test_a_website_or_landing_request_gets_the_awwwards_house_rule(self):
        for prompt in ("build me a landing page for my coffee brand", "design a portfolio website",
                       "buatkan website untuk kedai kek saya", "bina laman web untuk syarikat saya",
                       "redesign our homepage so it looks premium"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), WEB_REMINDER)

    def test_a_dashboard_or_app_screen_gets_the_craft_bar_with_native_scroll(self):
        for prompt in ("design a dashboard for tenant management", "build an admin panel with a data table",
                       "create the settings screen for the app"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), PRODUCT_REMINDER)
        self.assertIn("native scroll", PRODUCT_REMINDER)

    def test_work_that_is_not_design_gets_no_style_line(self):
        for prompt in ("fix the crash on the checkout page", "write tests for the landing page",
                       "make sure the page loads", "deploy the website to production", "thanks!",
                       "explain how the router works", "create a users table in postgres",
                       "build an API endpoint for the dashboard"):
            with self.subTest(prompt=prompt):
                self.assertIsNone(design_reminder(prompt))

    def test_the_prompt_hook_adds_the_line_and_skips_slash_commands(self):
        out = hook_output(json.dumps({"prompt": "design a portfolio website for a photographer", "cwd": "C:/proj"}))
        self.assertIn("Awwwards", out["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(hook_output(json.dumps({"prompt": "/design a website", "cwd": "C:/proj"})), {})


class AwwwardsRoutingTests(unittest.TestCase):
    def primary(self, prompt):
        return select_skill_stack(prompt, ROOT, limit=3)["selected"][0]["skill_id"]

    def test_web_design_prompts_route_to_the_house_rule(self):
        for prompt in ("build me a landing page for my coffee brand", "design a portfolio website",
                       "buatkan website untuk kedai kek saya", "bina laman web untuk syarikat saya",
                       "make the homepage look premium like awwwards",
                       "redesign our marketing site so it stops looking generic"):
            with self.subTest(prompt=prompt):
                self.assertEqual(self.primary(prompt), "bosskuai-taste")

    def test_scoring_goes_to_jury_and_dashboards_to_design_to_code(self):
        self.assertEqual(self.primary("score my website like the awwwards jury"), "jury")
        self.assertEqual(self.primary("design a dashboard for tenant management"), "bosskuai-ui-ux-design-to-code")

    def test_a_named_direction_still_wins(self):
        self.assertEqual(self.primary("use hallmark for my landing page"), "hallmark")

    def test_the_two_awwwards_build_loops_never_load_together(self):
        ids = [row["skill_id"] for row in select_skill_stack(
            "use awwwards and awwwards-web-design for my studio site", ROOT, limit=5)["selected"]]
        self.assertLessEqual(len({"awwwards", "awwwards-web-design"} & set(ids)), 1)


if __name__ == "__main__":
    unittest.main()
