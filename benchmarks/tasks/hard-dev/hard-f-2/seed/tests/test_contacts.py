import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import main


class ContactCliTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_tmp_contacts.json"
        )
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        code = main(argv, stdout=out, stderr=err, db_path=self.db_path)
        return code, out.getvalue(), err.getvalue()

    def test_add_and_show(self):
        code, out, _ = self.run_cli([
            "add", "Ada Lovelace", "--email", "ada@example.com", "--company", "Acme",
        ])
        self.assertEqual(code, 0)
        contact = json.loads(out)
        self.assertEqual(contact["full_name"], "Ada Lovelace")
        self.assertEqual(contact["email"], "ada@example.com")
        self.assertEqual(contact["company"], "Acme")
        self.assertEqual(contact["tags"], [])

        code, out, _ = self.run_cli(["show", str(contact["id"])])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), contact)

    def test_add_with_tags_dedup(self):
        code, out, _ = self.run_cli([
            "add", "Grace Hopper", "--tag", "navy", "--tag", "navy", "--tag", "compiler",
        ])
        self.assertEqual(code, 0)
        contact = json.loads(out)
        self.assertEqual(contact["tags"], ["navy", "compiler"])

    def test_add_invalid_email_is_validation_error(self):
        code, out, err = self.run_cli(["add", "Bad Email", "--email", "not-an-email"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("validation", err)

    def test_tag_is_idempotent(self):
        _, out, _ = self.run_cli(["add", "Linus Torvalds"])
        cid = json.loads(out)["id"]
        code, out, _ = self.run_cli(["tag", str(cid), "kernel"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["tags"], ["kernel"])
        code, out, _ = self.run_cli(["tag", str(cid), "kernel"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["tags"], ["kernel"])

    def test_delete_then_show_not_found(self):
        _, out, _ = self.run_cli(["add", "Temp Contact"])
        cid = json.loads(out)["id"]
        code, _, _ = self.run_cli(["delete", str(cid)])
        self.assertEqual(code, 0)
        code, out, err = self.run_cli(["show", str(cid)])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("not_found", err)

    def test_list_returns_all_contacts_in_id_order(self):
        self.run_cli(["add", "First Person"])
        self.run_cli(["add", "Second Person"])
        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        contacts = json.loads(out)
        self.assertEqual([c["full_name"] for c in contacts], ["First Person", "Second Person"])

    def test_count(self):
        self.run_cli(["add", "A"])
        self.run_cli(["add", "B"])
        code, out, _ = self.run_cli(["count"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"count": 2})


if __name__ == "__main__":
    unittest.main()
