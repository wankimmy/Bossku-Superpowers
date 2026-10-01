import time
import unittest

from deps import resolve_order


def _is_valid_order(order, dependencies):
    position = {node: i for i, node in enumerate(order)}
    for node, deps in dependencies.items():
        for dep in deps:
            if position[dep] >= position[node]:
                return False
    return True


class CorrectnessTests(unittest.TestCase):
    def test_simple_chain(self):
        deps = {"b": ["a"], "c": ["a", "b"]}
        self.assertEqual(resolve_order(deps), ["a", "b", "c"])

    def test_independent_nodes_use_lexicographic_order(self):
        deps = {"c": [], "a": [], "b": []}
        self.assertEqual(resolve_order(deps), ["a", "b", "c"])

    def test_node_appearing_only_as_a_dependency_is_included(self):
        deps = {"b": ["a"]}
        self.assertEqual(resolve_order(deps), ["a", "b"])

    def test_diamond_dependency(self):
        deps = {"b": ["a"], "c": ["a"], "d": ["b", "c"]}
        self.assertEqual(resolve_order(deps), ["a", "b", "c", "d"])

    def test_tie_break_across_disconnected_components(self):
        deps = {"b1": ["a1"], "b2": ["a2"]}
        self.assertEqual(resolve_order(deps), ["a1", "a2", "b1", "b2"])

    def test_result_is_a_valid_order_for_a_bigger_graph(self):
        deps = {
            "build": ["compile", "link"],
            "compile": ["fetch"],
            "link": ["compile"],
            "fetch": [],
            "test": ["build"],
        }
        order = resolve_order(deps)
        self.assertEqual(sorted(order), sorted(set(deps) | {d for ds in deps.values() for d in ds}))
        self.assertTrue(_is_valid_order(order, deps))

    def test_two_node_cycle_raises(self):
        with self.assertRaises(ValueError):
            resolve_order({"a": ["b"], "b": ["a"]})

    def test_self_dependency_raises(self):
        with self.assertRaises(ValueError):
            resolve_order({"a": ["a"]})

    def test_longer_cycle_raises(self):
        with self.assertRaises(ValueError):
            resolve_order({"a": ["b"], "b": ["c"], "c": ["a"]})

    def test_type_error_on_non_dict(self):
        with self.assertRaises(TypeError):
            resolve_order(["a", "b"])

    def test_empty_graph(self):
        self.assertEqual(resolve_order({}), [])


class PerformanceTests(unittest.TestCase):
    def test_large_chain_is_fast_and_correct(self):
        n = 50000
        deps = {}
        for i in range(1, n):
            deps[f"n{i:06d}"] = [f"n{i - 1:06d}"]
        expected = [f"n{i:06d}" for i in range(n)]

        t0 = time.perf_counter()
        order = resolve_order(deps)
        elapsed = time.perf_counter() - t0

        self.assertEqual(order, expected)
        self.assertLess(elapsed, 8.0, f"resolve_order took too long: {elapsed:.2f}s")


if __name__ == "__main__":
    unittest.main()
