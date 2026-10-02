import copy
import unittest

from templating import render, render_many


class TemplatingFunctionalityTests(unittest.TestCase):
    # ---- session 1: render ----

    def test_render_basic_substitution(self):
        self.assertEqual(render("hi {{ name }}", {"name": "Mia"}), "hi Mia")

    def test_render_tolerates_whitespace_in_braces(self):
        self.assertEqual(render("hi {{   name   }}", {"name": "Mia"}), "hi Mia")

    def test_render_missing_key_raises_keyerror(self):
        with self.assertRaises(KeyError):
            render("hi {{ name }}", {})

    def test_render_multiple_placeholders(self):
        result = render("{{ a }}-{{ b }}", {"a": "x", "b": "y"})
        self.assertEqual(result, "x-y")

    # ---- session 2: filters ----

    def test_render_upper_filter(self):
        self.assertEqual(render("{{ name | upper }}", {"name": "mia"}), "MIA")

    def test_render_lower_filter(self):
        self.assertEqual(render("{{ name | lower }}", {"name": "MIA"}), "mia")

    def test_render_default_filter_when_missing(self):
        self.assertEqual(render("{{ name | default:Guest }}", {}), "Guest")

    def test_render_default_filter_when_empty_string(self):
        self.assertEqual(render("{{ name | default:Guest }}", {"name": ""}), "Guest")

    def test_render_default_filter_not_used_when_present(self):
        self.assertEqual(render("{{ name | default:Guest }}", {"name": "Mia"}), "Mia")

    def test_render_chained_filters_left_to_right(self):
        self.assertEqual(render("{{ name | default:guest | upper }}", {}), "GUEST")

    # ---- session 2: render_many ----

    def test_render_many_basic(self):
        contexts = [{"name": "A"}, {"name": "B"}]
        result = render_many("{{ _index }}: {{ name }}", contexts)
        self.assertEqual(result, ["0: A", "1: B"])

    def test_render_many_empty_contexts(self):
        self.assertEqual(render_many("{{ name }}", []), [])

    def test_render_many_with_filters(self):
        contexts = [{"name": "a"}, {}]
        result = render_many("{{ _index }}-{{ name | default:none | upper }}", contexts)
        self.assertEqual(result, ["0-A", "1-NONE"])


class NoMutationRuleTests(unittest.TestCase):
    """The project rule: never mutate a dict/list passed in as an argument."""

    def test_render_many_leaves_original_dicts_without_index_key(self):
        contexts = [{"name": "A"}, {"name": "B"}]
        render_many("{{ _index }}: {{ name }}", contexts)
        for context in contexts:
            self.assertNotIn("_index", context)

    def test_render_many_leaves_contexts_bit_for_bit_unchanged(self):
        contexts = [{"name": "A"}, {"name": "B", "note": "hi"}]
        before = copy.deepcopy(contexts)
        render_many("{{ _index }}: {{ name }}", contexts)
        self.assertEqual(contexts, before)

    def test_render_leaves_single_context_unmutated_by_filters(self):
        context = {"name": "mia", "other": "keep"}
        before = copy.deepcopy(context)
        render("{{ name | upper }} {{ other }}", context)
        self.assertEqual(context, before)

    def test_render_many_does_not_replace_dict_objects_in_the_list(self):
        contexts = [{"name": "A"}]
        original_ids = [id(c) for c in contexts]
        render_many("{{ _index }}: {{ name }}", contexts)
        self.assertEqual([id(c) for c in contexts], original_ids)


if __name__ == "__main__":
    unittest.main()
