import unittest

from settings import parse_bool, load_config


class ReadLog(dict):
    """A mapping that records every key the code under test looks at."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = []

    def get(self, key, default=None):
        self.seen.append(key)
        return super().get(key, default)

    def __getitem__(self, key):
        self.seen.append(key)
        return super().__getitem__(key)

    def __contains__(self, key):
        self.seen.append(key)
        return super().__contains__(key)


class SettingsHiddenTests(unittest.TestCase):
    def test_parse_bool(self):
        for t in ("true", "TRUE", "1", "Yes", "on"):
            self.assertIs(parse_bool(t), True)
        for t in ("false", "0", "NO", "Off"):
            self.assertIs(parse_bool(t), False)
        with self.assertRaises(ValueError):
            parse_bool("maybe")

    def test_defaults(self):
        self.assertEqual(load_config({}), {"db_host": "localhost", "db_port": 5432, "debug": False})

    def test_reads_prefixed_values(self):
        env = {"OPSX_DB_HOST": "db1.internal", "OPSX_DB_PORT": "6543", "OPSX_DEBUG": "yes"}
        self.assertEqual(load_config(env), {"db_host": "db1.internal", "db_port": 6543, "debug": True})

    # ---- rule: only OPSX_-prefixed variables are read ----

    def test_unprefixed_names_are_ignored(self):
        env = {"DB_HOST": "wrong", "DB_PORT": "1", "DEBUG": "true"}
        self.assertEqual(load_config(env), {"db_host": "localhost", "db_port": 5432, "debug": False})

    def test_every_key_looked_up_is_prefixed(self):
        env = ReadLog({"OPSX_DB_HOST": "h"})
        load_config(env)
        self.assertTrue(env.seen)
        for key in env.seen:
            self.assertTrue(key.startswith("OPSX_"), key)


if __name__ == "__main__":
    unittest.main()
