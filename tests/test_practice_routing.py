import unittest
from pathlib import Path

from bossku.skills import find_skill, recommend_skill_stack


ROOT = Path(__file__).resolve().parents[1]


class PracticeRoutingTests(unittest.TestCase):
    def test_actual_product_checks_route_to_product_verification(self):
        for prompt in (
            "verify the signup flow in the running app",
            "run a cli smoke check in a temporary home",
            "write a launch and verification recipe for the actual user journey",
        ):
            with self.subTest(prompt=prompt):
                self.assertEqual(find_skill(prompt, ROOT)[0], "bosskuai-product-verification")

    def test_hindsight_operations_route_to_the_optional_integration(self):
        for prompt in (
            "connect Hindsight memory to this project",
            "Hindsight recall and reflect in a project memory bank",
            "use Hindsight retain for approved curated notes",
        ):
            with self.subTest(prompt=prompt):
                self.assertEqual(find_skill(prompt, ROOT)[0], "bosskuai-hindsight-memory")

    def test_new_skills_do_not_hijack_local_memory_or_test_authoring(self):
        for prompt, expected in (
            ("bossku remember this decision and sync memory to obsidian", "bosskuai-permanent-memory-orchestration"),
            ("write pytest fixtures for the parser module", "python-testing"),
        ):
            with self.subTest(prompt=prompt):
                self.assertEqual(find_skill(prompt, ROOT)[0], expected)
                stack = recommend_skill_stack(prompt, ROOT)
                self.assertNotIn("bosskuai-hindsight-memory", [sid for sid, _ in stack])
                self.assertNotIn("bosskuai-product-verification", [sid for sid, _ in stack])
