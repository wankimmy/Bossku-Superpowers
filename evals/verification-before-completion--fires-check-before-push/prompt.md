---
description: "Casual 'double check before I push': show evidence and its limits instead of a bare 'looks good'."
tags: ["lean", "verification-before-completion", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

ok i think my slug helper is done, just double check before i push ya. save these:

`slug.py`:
```python
import re
import unicodedata


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "item"
```

`test_slug.py`:
```python
import unittest
from slug import slugify


class SlugTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Nasi Lemak Special!"), "nasi-lemak-special")

    def test_accents(self):
        self.assertEqual(slugify("Café Délice"), "cafe-delice")

    def test_symbols_only(self):
        self.assertEqual(slugify("!!!"), "item")


if __name__ == "__main__":
    unittest.main()
```
