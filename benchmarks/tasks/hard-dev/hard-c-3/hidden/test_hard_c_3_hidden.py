import io
import unittest
from contextlib import redirect_stdout

import cli
import flags
import gating
import reporting
from flags import FeatureFlags


class FeatureFlagsBasicTests(unittest.TestCase):
    def test_enable_then_is_enabled(self):
        reg = FeatureFlags()
        reg.enable("beta")
        self.assertTrue(reg.is_enabled("beta"))

    def test_unset_flag_is_false(self):
        reg = FeatureFlags()
        self.assertFalse(reg.is_enabled("nope"))

    def test_disable_registers_entry_even_if_never_enabled(self):
        reg = FeatureFlags()
        reg.disable("new_flag")
        self.assertEqual(reg.all_flags(), {"new_flag": False})

    def test_never_touched_flag_absent_from_all_flags(self):
        reg = FeatureFlags()
        reg.enable("a")
        self.assertNotIn("b", reg.all_flags())
        self.assertFalse(reg.is_enabled("b"))

    def test_all_flags_returns_copy(self):
        reg = FeatureFlags()
        reg.enable("a")
        snapshot = reg.all_flags()
        snapshot["a"] = False
        snapshot["b"] = True
        self.assertTrue(reg.is_enabled("a"))
        self.assertFalse(reg.is_enabled("b"))

    def test_independent_instances_do_not_share_state(self):
        reg1 = FeatureFlags()
        reg2 = FeatureFlags()
        reg1.enable("only_in_one")
        self.assertFalse(reg2.is_enabled("only_in_one"))
        self.assertNotIn("only_in_one", reg2.all_flags())

    def test_enable_rejects_non_string_name(self):
        reg = FeatureFlags()
        with self.assertRaises(TypeError):
            reg.enable(123)

    def test_is_enabled_rejects_non_string_name(self):
        reg = FeatureFlags()
        with self.assertRaises(TypeError):
            reg.is_enabled(123)


class DefaultRegistryTests(unittest.TestCase):
    def test_module_level_enable_visible_on_default_registry(self):
        flags.enable("hc3_dr_enable_1")
        self.assertTrue(flags.default_registry.is_enabled("hc3_dr_enable_1"))

    def test_default_registry_mutation_visible_via_module_functions(self):
        flags.default_registry.enable("hc3_dr_match_2")
        self.assertTrue(flags.is_enabled("hc3_dr_match_2"))


class GatingTests(unittest.TestCase):
    def test_run_if_enabled_calls_function_on_default_registry(self):
        flags.enable("hc3_run_enabled_3")
        calls = []
        ok, result = gating.run_if_enabled(
            "hc3_run_enabled_3", lambda: calls.append(1) or "done"
        )
        self.assertTrue(ok)
        self.assertEqual(result, "done")
        self.assertEqual(calls, [1])

    def test_run_if_enabled_skips_function_when_disabled(self):
        calls = []
        ok, result = gating.run_if_enabled(
            "hc3_run_disabled_4_never_set", lambda: calls.append(1)
        )
        self.assertFalse(ok)
        self.assertIsNone(result)
        self.assertEqual(calls, [])

    def test_run_if_enabled_explicit_registry_independent_of_global(self):
        custom = FeatureFlags()
        custom.enable("hc3_independent_5")
        calls = []
        ok, _ = gating.run_if_enabled(
            "hc3_independent_5", lambda: calls.append(1), registry=custom
        )
        self.assertTrue(ok)
        self.assertEqual(calls, [1])
        # The global registry was never told about this flag.
        self.assertFalse(flags.is_enabled("hc3_independent_5"))
        ok2, _ = gating.run_if_enabled("hc3_independent_5", lambda: calls.append(2))
        self.assertFalse(ok2)
        self.assertEqual(calls, [1])

    def test_run_if_enabled_passes_args_and_kwargs(self):
        custom = FeatureFlags()
        custom.enable("hc3_args_6")
        ok, result = gating.run_if_enabled(
            "hc3_args_6", lambda a, b, c=0: a + b + c, 1, 2, registry=custom, c=3
        )
        self.assertTrue(ok)
        self.assertEqual(result, 6)


class ReportingTests(unittest.TestCase):
    def test_build_report_empty_custom_registry(self):
        reg = FeatureFlags()
        self.assertEqual(reporting.build_report(reg), "no flags configured")

    def test_build_report_sorted_and_formatted(self):
        reg = FeatureFlags()
        reg.enable("zeta")
        reg.disable("alpha")
        reg.enable("mid")
        self.assertEqual(
            reporting.build_report(reg), "alpha: OFF\nmid: ON\nzeta: ON"
        )

    def test_build_report_uses_global_when_no_registry_passed(self):
        flags.enable("hc3_report_global_7")
        self.assertIn("hc3_report_global_7: ON", reporting.build_report())


class CliTests(unittest.TestCase):
    def test_cli_list_fresh_registry_no_flags(self):
        reg = FeatureFlags()
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main(["list"], registry=reg)
        self.assertEqual(buf.getvalue().strip(), "no flags configured")

    def test_cli_enable_then_list_isolated_registry(self):
        reg = FeatureFlags()
        with redirect_stdout(io.StringIO()):
            cli.main(["enable", "beta"], registry=reg)
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main(["list"], registry=reg)
        self.assertEqual(buf.getvalue().strip(), "beta: ON")

    def test_cli_unknown_command(self):
        reg = FeatureFlags()
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main(["frobnicate"], registry=reg)
        self.assertEqual(buf.getvalue().strip(), "unknown command: frobnicate")

    def test_cli_default_registry_used_when_omitted(self):
        with redirect_stdout(io.StringIO()):
            cli.main(["enable", "hc3_cli_default_8"])
        self.assertTrue(flags.default_registry.is_enabled("hc3_cli_default_8"))

    def test_cli_disable_isolated_registry_does_not_touch_global(self):
        reg = FeatureFlags()
        with redirect_stdout(io.StringIO()):
            cli.main(["disable", "hc3_cli_isolated_9"], registry=reg)
        self.assertNotIn("hc3_cli_isolated_9", flags.all_flags())
        self.assertEqual(reg.all_flags(), {"hc3_cli_isolated_9": False})


if __name__ == "__main__":
    unittest.main()
