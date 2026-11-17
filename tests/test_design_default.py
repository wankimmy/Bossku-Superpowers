import json
import unittest
from pathlib import Path

from bossku.design import APP_REMINDER, NEUTRAL_REMINDER, PRODUCT_REMINDER, TASK_REMINDER, WEB_REMINDER, design_reminder
from bossku.hint import hook_output
from bossku.skills import select_skill_stack

ROOT = Path(__file__).resolve().parents[1]


class DesignReminderTests(unittest.TestCase):
    """The owner's decision (2026-11-17): classify the product first; the house rule is for showcase web only."""

    def test_a_showcase_site_gets_the_house_rule_and_a_jury_score(self):
        for prompt in ("build me a landing page for my coffee brand", "design a portfolio website",
                       "design an agency portfolio site", "redesign our homepage so it looks premium",
                       "bina laman web untuk syarikat saya"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), WEB_REMINDER)
        self.assertIn("bosskuai-taste", WEB_REMINDER)
        self.assertIn("jury", WEB_REMINDER)

    def test_a_storefront_is_task_first_with_native_scroll_and_no_theatre(self):
        for prompt in ("build a storefront for my bakery", "design the checkout page for our shop",
                       "create a pricing page for the product"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), TASK_REMINDER)
        self.assertIn("native scroll", TASK_REMINDER)
        self.assertIn("no intro loader", TASK_REMINDER)

    def test_product_ui_follows_the_design_system_with_no_jury_or_signature(self):
        for prompt in ("design an ERP dashboard for the finance team", "design a dashboard for tenant management",
                       "build an admin panel with a data table", "improve an existing SaaS dashboard",
                       "fix the layout of the HRMS leave form",
                       "build a CRM dashboard for a marketing agency",
                       "design an admin panel for our studio booking system",
                       "design the campaign analytics dashboard",
                       "design a HRMS leave form for a recruitment agency",
                       "improve the SaaS dashboard hero metrics",
                       "build a machine learning dashboard",
                       "design a learning management system admin dashboard",
                       "build a web app for invoicing",
                       # a sales pipeline is a CRM screen, not a CI pipeline
                       "design the CRM dashboard for our sales team, they need pipeline and tasks at a glance"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), PRODUCT_REMINDER)
        self.assertIn("design system", PRODUCT_REMINDER)
        self.assertIn("no jury", PRODUCT_REMINDER)
        self.assertNotIn("Awwwards", PRODUCT_REMINDER)

    def test_a_consumer_or_mobile_app_follows_platform_conventions(self):
        for prompt in ("build a mobile language-learning app", "create the settings screen for the app",
                       "design a habit tracker app in Expo", "build a mobile app in Android Studio"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), APP_REMINDER)
        self.assertIn("platform conventions", APP_REMINDER)
        self.assertIn("engagement", APP_REMINDER)

    def test_an_unclear_type_is_asked_to_pick_not_sent_to_the_showcase_rule(self):
        for prompt in ("improve the login page", "update the profile screen", "refactor the settings page",
                       "update the pricing page", "fix the design of the login screen",
                       "build the leave request screen"):
            with self.subTest(prompt=prompt):
                self.assertIn(design_reminder(prompt), (NEUTRAL_REMINDER, PRODUCT_REMINDER, TASK_REMINDER))
        for prompt in ("improve the login page", "update the profile screen", "fix the design of the login screen"):
            self.assertEqual(design_reminder(prompt), NEUTRAL_REMINDER)
        self.assertNotIn("jury", NEUTRAL_REMINDER)
        self.assertIn("assumed", NEUTRAL_REMINDER)

    def test_work_that_is_not_design_gets_no_style_line(self):
        for prompt in ("fix the bug on the settings page", "write a database migration for the users page",
                       "write tests for the dashboard", "fix the crash on the checkout page",
                       "write tests for the landing page",
                       "make sure the page loads", "deploy the website to production", "thanks!",
                       "explain how the router works", "create a users table in postgres",
                       "build an API endpoint for the dashboard", "update the docs",
                       "update the documentation for the CLI", "refactor the redux store",
                       "update the app dependencies", "make the app faster", "implement booking cancellation",
                       "refactor the checkout service", "update the README section on install",
                       "update the form validation logic", "create an app password for gmail",
                       "fix the build pipeline for the dashboard", "update the deployment pipeline for the web app",
                       "create a data pipeline for the analytics dashboard",
                       "Refactor the dashboard controller into services", "Improve error handling in the admin controller",
                       "Update the admin user role in the seeder", "Update the CRM webhook retry logic",
                       "Improve the SaaS billing retry logic", "Update the .env settings for staging",
                       "Update the panel of reviewers in CODEOWNERS", "Refactor the tables seeder",
                       "Build a CLI command to sync the ERP stock levels",
                       "build a queue worker for the CRM import", "build an export job for the HRMS payroll",
                       "bina queue worker untuk import data CRM", "improve the page load time",
                       "implement rate limiting for the admin login", "create a cron job that emails the analytics report",
                       "create a middleware to protect the admin routes", "create a form request for the invoice",
                       "Update the site config in nginx", "Refactor the page cache layer",
                       "update the components version in package.json"):
            with self.subTest(prompt=prompt):
                self.assertIsNone(design_reminder(prompt))

    def test_a_product_screen_that_names_a_showcase_noun_is_not_sent_to_the_showcase_rule(self):
        for prompt in ("Build an investment portfolio dashboard for our wealth app",
                       "Design the portfolio holdings table in the admin panel",
                       "Design the admin dashboard for our marketing site CMS",
                       "Design the landing page editor screen inside our SaaS admin",
                       "design the portfolio screen for our mobile investing app",
                       "build a portfolio tracker web app for crypto holdings", "design the portfolio page in our trading app",
                       "design the portfolio tab of the mobile banking app", "reka skrin portfolio untuk app pelaburan kami",
                       "create the project portfolio table for our ERP", "design the campaign page list in our CRM",
                       "design the landing page editor screen for our SaaS",
                       "design the settings form for the landing page builder SaaS",
                       "build the web design approval screen in our agency CRM",
                       "design a portfolio management system for fund managers",
                       "build the studio page booking form in our SaaS"):
            with self.subTest(prompt=prompt):
                self.assertEqual(design_reminder(prompt), NEUTRAL_REMINDER)
        self.assertEqual(design_reminder("build a landing page for our SaaS"), WEB_REMINDER)

    def test_the_prompt_hook_adds_the_line_and_skips_slash_commands(self):
        out = hook_output(json.dumps({"prompt": "design a portfolio website for a photographer", "cwd": "C:/proj"}))
        self.assertIn("showcase", out["hookSpecificOutput"]["additionalContext"])
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
