import unittest
from pathlib import Path

from bossku.skills import audit_skills, list_skill_ids, load_library_only, load_vendored, parse_skill_md, skill_folder

ROOT = Path(__file__).resolve().parents[1]
MAX_DESCRIPTION_CHARS = 300   # the length `bossku skills audit` flags


def first_party_descriptions() -> dict[str, str]:
    """Descriptions of the skills this repo owns; vendored packs keep their upstream wording."""
    vendored = load_vendored(ROOT)
    return {
        sid: parse_skill_md(skill_folder(sid, ROOT) / "SKILL.md").description
        for sid in list_skill_ids(ROOT) if sid not in vendored
    }


class FirstPartyDescriptionTests(unittest.TestCase):
    def test_every_first_party_description_starts_with_use_when(self):
        missing = [sid for sid, text in first_party_descriptions().items() if not text.startswith("Use when ")]
        self.assertEqual(missing, [])

    def test_the_audit_counts_none_without_use_when(self):
        self.assertEqual(audit_skills(ROOT)["custom_descriptions_without_use_when"], [])

    def test_every_first_party_description_stays_under_the_length_cap(self):
        # Library-only skills are never listed, so a long description costs no session anything.
        library_only = load_library_only(ROOT)
        long = {sid: len(text) for sid, text in first_party_descriptions().items()
                if len(text) > MAX_DESCRIPTION_CHARS and sid not in library_only}
        self.assertEqual(long, {})

