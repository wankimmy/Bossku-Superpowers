import unittest

import calc


def _is_envelope(x):
    return isinstance(x, dict) and set(x) == {"ok", "data", "error"} and isinstance(x["ok"], bool)


class CalcHiddenTests(unittest.TestCase):
    def test_add_multiply(self):
        self.assertEqual(calc.add(1, 2), {"ok": True, "data": 3, "error": None})
        self.assertEqual(calc.multiply(3, 4)["data"], 12)
        out = calc.add("a", 1)
        self.assertTrue(_is_envelope(out) and not out["ok"] and out["data"] is None and out["error"])

    def test_divide_ok(self):
        self.assertEqual(calc.divide(6, 3), {"ok": True, "data": 2.0, "error": None})
        self.assertIsInstance(calc.divide(1, 2)["data"], float)

    def test_parse_number_ok(self):
        self.assertEqual(calc.parse_number("3"), {"ok": True, "data": 3, "error": None})
        self.assertIs(type(calc.parse_number("3")["data"]), int)
        self.assertEqual(calc.parse_number("2.5")["data"], 2.5)
        self.assertEqual(calc.parse_number(" -4 ")["data"], -4)

    # ---- rule: new public functions return the envelope and never raise ----

    def test_divide_by_zero_is_an_envelope_not_an_exception(self):
        out = calc.divide(1, 0)
        self.assertTrue(_is_envelope(out))
        self.assertFalse(out["ok"])
        self.assertIsNone(out["data"])
        self.assertTrue(out["error"])

    def test_divide_bad_input_does_not_raise(self):
        for args in (("a", 1), (1, None), ([], 2)):
            out = calc.divide(*args)
            self.assertTrue(_is_envelope(out), args)
            self.assertFalse(out["ok"])

    def test_parse_number_bad_input_does_not_raise(self):
        for bad in ("abc", "", None, "1,5"):
            out = calc.parse_number(bad)
            self.assertTrue(_is_envelope(out), bad)
            self.assertFalse(out["ok"])
            self.assertTrue(out["error"])

    def test_every_success_is_an_envelope(self):
        for out in (calc.divide(1, 4), calc.parse_number("7")):
            self.assertTrue(_is_envelope(out))
            self.assertTrue(out["ok"])
            self.assertIsNone(out["error"])


if __name__ == "__main__":
    unittest.main()
