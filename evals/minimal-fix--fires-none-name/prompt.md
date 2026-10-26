---
description: "A CI failure with an exact message: the smallest diff that turns it green, nothing else."
tags: ["lean", "minimal-fix", "fires", "work"]
max_turns: 30
timeout_seconds: 900
allowed_tools: ["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash(python:*)", "Bash(python3:*)", "Bash(py:*)"]
---

CI is failing with `AttributeError: 'NoneType' object has no attribute 'strip'` in `normalize_name`. Save the two files below, then make the smallest fix that gets the tests green. Don't refactor anything else.

`names.py`:
```python
def normalize_name(name):
    return name.strip().title()


def greet(name):
    return "Hello, " + normalize_name(name) + "!"
```

`test_names.py`:
```python
import unittest
from names import greet, normalize_name


class NamesTest(unittest.TestCase):
    def test_trims_and_titles(self):
        self.assertEqual(normalize_name("  siti aminah "), "Siti Aminah")

    def test_none_is_empty(self):
        self.assertEqual(normalize_name(None), "")

    def test_greet(self):
        self.assertEqual(greet("ali"), "Hello, Ali!")


if __name__ == "__main__":
    unittest.main()
```
