"""Regression tests for the memory audit fixes: redaction shapes (A06/B17/B18) and sync only where notes exist (A12/A24).

Secret-looking samples are joined from pieces at run time so this file does not trip secret scanners.
"""
import tempfile
import time
import unittest
from pathlib import Path

from bossku.memory import remember, save_user_config, sync_project
from bossku.redact import redact

PEM_BODY = "\n".join(["MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj"] * 3)


def pem(label="PRIVATE KEY", body=PEM_BODY, end=True):
    tail = f"\n-----END {label}-----" if end else ""
    return f"-----BEGIN {label}-----\n{body}{tail}"


class RedactShapeTests(unittest.TestCase):
    """One row per shape. Each secret must be gone and the words around it must stay."""

    SECRETS = {
        "slack bot token": "xox" + "b-1234567890-1234567890123-AbCdEfGhIjKlMnOpQrStUvWx",
        "google api key": "AIza" + "SyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY",
        "stripe live key": "sk_" + "live_4eC39HqLyjWDarjtT1zdp7dc",
        "stripe restricted key": "rk_" + "test_4eC39HqLyjWDarjtT1zdp7dc",
        "gitlab token": "glpat" + "-xxxxxxxxxxxxxxxxxxxx",
        "hugging face token": "hf_" + "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
        "npm token": "npm_" + "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
        "jwt": "eyJ" + "hbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dBjftJeZ4CVPmB92K27uhbUJU1p1r",
        "aws secret in env style": "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "stripe env name": "STRIPE_SECRET_KEY=" + "sk_" + "live_abc123",
        "supabase env name": "SUPABASE_SERVICE_ROLE_KEY=abcDEF123456",
        "basic auth header": "Authorization: Basic " + "dXNlcjpwYXNzd29yZDEyMw==",
    }

    def test_each_shape_is_redacted_and_the_prose_around_it_stays(self):
        for name, secret in self.SECRETS.items():
            with self.subTest(name):
                out = redact(f"before the value {secret} after the value")
                self.assertNotIn(secret[-12:], out)
                self.assertNotIn(secret[len(secret) // 2:], out)
                self.assertIn("before the value", out)
                self.assertIn("[REDACTED]", out)

    def test_url_password_goes_and_scheme_and_host_stay(self):
        for url, kept in (("postgres://appuser:Sup3rPass@db.internal:5432/app", "postgres://"),
                          ("redis://:Sup3rPass@cache.internal:6379/0", "redis://"),
                          ("https://user:p%40ss@example.com/path", "https://")):
            with self.subTest(url):
                out = redact(f"connect with {url} now")
                self.assertNotIn("Sup3rPass", out)
                self.assertNotIn("p%40ss", out)
                self.assertIn(kept, out)
                self.assertRegex(out, r"@(db\.internal:5432/app|cache\.internal:6379/0|example\.com/path) now")

    def test_urls_without_a_password_are_unchanged(self):
        for text in ("see https://example.com:8443/docs?a=b for more",
                     "clone ssh://git@github.com:org/repo.git today",
                     "mail me at dev@example.com or http://host:80, thanks",
                     "https://example.com/users/name@home/profile"):
            with self.subTest(text):
                self.assertEqual(redact(text), text)

    def test_pem_block_is_removed_whole(self):
        for label in ("PRIVATE KEY", "RSA PRIVATE KEY", "EC PRIVATE KEY", "OPENSSH PRIVATE KEY",
                      "ENCRYPTED PRIVATE KEY", "PGP PRIVATE KEY BLOCK"):
            with self.subTest(label):
                out = redact(f"the key:\n{pem(label)}\nkeep this line")
                self.assertNotIn("MIIEvQIBADANBg", out)
                self.assertNotIn("END", out)
                self.assertTrue(out.startswith("the key:\n"))
                self.assertTrue(out.endswith("\nkeep this line"))

    def test_encrypted_pem_headers_with_hyphens_do_not_stop_the_match(self):
        body = "Proc-Type: 4,ENCRYPTED\nDEK-Info: AES-128-CBC,0123456789ABCDEF\n\n" + PEM_BODY
        out = redact(f"x\n{pem('RSA PRIVATE KEY', body)}\ny")
        self.assertNotIn("MIIEvQIBADANBg", out)
        self.assertNotIn("DEK-Info", out)

    def test_truncated_pem_loses_its_base64_lines_and_not_the_prose_after_it(self):
        out = redact(f"saved:\n{pem(end=False)}\n\nThen we rotated it and moved on.")
        self.assertNotIn("MIIEvQIBADANBg", out)
        self.assertTrue(out.endswith("Then we rotated it and moved on."))

    def test_bare_pem_header_still_redacts_and_keeps_following_prose(self):
        out = redact("-----BEGIN RSA PRIVATE KEY-----\nThis file holds the key, so keep it private.")
        self.assertNotIn("BEGIN", out)
        self.assertIn("This file holds the key, so keep it private.", out)

    def test_a_public_key_block_is_not_redacted(self):
        text = "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL\n-----END PUBLIC KEY-----"
        self.assertEqual(redact(text), text)

    def test_names_and_prose_that_look_close_are_unchanged(self):
        for text in ("set max_tokens=4096 for the long runs",
                     "the token budget is 4096 and the password policy is in the docs",
                     "Use Bearer authentication; the risk-assessment-framework task-queue stays",
                     "tokens_used = 5 and secret_santa notes",
                     "sk_live is the Stripe prefix and hf_ and npm_ are prefixes too",
                     "npm_config and hf_hub_download are names",
                     "a JWT looks like eyJ..eyJ..sig in docs",
                     "Authorization: Basic auth"):
            with self.subTest(text):
                self.assertEqual(redact(text), text)

    def test_token_label_prose_behaves_as_before(self):
        self.assertEqual(redact("token: see docs"), "[REDACTED] docs")   # unchanged by the new shapes

    def test_hostile_input_stays_fast(self):
        pieces = ["eyJ-" * 20000, "-----BEGIN PRIVATE KEY-----\n" * 3000, "a_" * 40000 + "=",
                  "xoxb-" * 16000, "://a:" * 15000, "eyJaaaaaaaaaa." * 6000]
        for piece in pieces:
            with self.subTest(piece[:20]):
                start = time.perf_counter()
                redact(piece)
                self.assertLess(time.perf_counter() - start, 3.0)


class SyncOnlyWhereNotesExistTests(unittest.TestCase):
    """Repo-mode sync must not create folders or state files in a project that has no notes (A12, A24)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.vault = self.home / "vault"
        self.vault.mkdir()
        save_user_config({"obsidian_vault": str(self.vault)}, self.home)

    def test_a_folder_with_no_notes_gets_nothing_written(self):
        stray = self.home / "stray"
        stray.mkdir()
        result = sync_project(stray, home=self.home)
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(list(stray.iterdir()), [])
        self.assertFalse((self.vault / "BosskuAI").exists())

    def test_an_empty_memory_folder_counts_as_no_notes(self):
        project = self.home / "empty"
        (project / ".bossku" / "memory").mkdir(parents=True)
        self.assertEqual(sync_project(project, home=self.home)["status"], "skipped")
        self.assertEqual(list((project / ".bossku" / "memory").iterdir()), [])
        self.assertFalse((self.vault / "BosskuAI").exists())

    def test_a_project_with_notes_still_syncs(self):
        project = self.home / "shop"
        saved = remember(project, "decision", "Keep it small.", home=self.home)
        self.assertEqual(saved["vault"]["status"], "ok")
        copy = self.vault / "BosskuAI" / "shop" / "decisions.md"
        self.assertIn("Keep it small.", copy.read_text(encoding="utf-8"))
        self.assertEqual(sync_project(project, home=self.home)["status"], "ok")
        self.assertTrue((project / ".bossku" / "memory" / "sync-state.json").is_file())


class VaultEditKeptByteForByteTests(unittest.TestCase):
    """A05 follow-up: a vault copy that is not valid UTF-8 must not crash the sync or lose bytes in the conflict copy."""

    def test_non_utf8_vault_edit_is_kept_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "repo"
            note = project / ".bossku" / "memory" / "decisions.md"
            note.parent.mkdir(parents=True)
            note.write_text("# Decisions\n\nFirst.\n", encoding="utf-8")
            vault = home / "vault"
            vault.mkdir()
            save_user_config({"obsidian_vault": str(vault)}, home)
            sync_project(project, home=home)
            copy = vault / "BosskuAI" / "repo" / "decisions.md"
            edited = b"# Decisions\n\ncaf\xe9 edit from an old editor\n"
            copy.write_bytes(edited)
            note.write_text("# Decisions\n\nSecond.\n", encoding="utf-8")
            result = sync_project(project, home=home)
            self.assertEqual(len(result["conflicts"]), 1)
            self.assertEqual(Path(result["conflicts"][0]).read_bytes(), edited)
            self.assertIn("Second.", copy.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
