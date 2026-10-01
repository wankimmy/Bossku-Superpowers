import ast
import os
import unittest

import tickets
from tickets import Ticket, load_tickets, count_by_status, classify_priority


def _module_path():
    return os.path.abspath(tickets.__file__)


def _source_tree():
    with open(_module_path(), "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


def _annotation_nodes(tree):
    nodes = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            for arg in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs):
                if arg.annotation is not None:
                    nodes.append(arg.annotation)
            if args.vararg is not None and args.vararg.annotation is not None:
                nodes.append(args.vararg.annotation)
            if args.kwarg is not None and args.kwarg.annotation is not None:
                nodes.append(args.kwarg.annotation)
            if node.returns is not None:
                nodes.append(node.returns)
        elif isinstance(node, ast.AnnAssign):
            nodes.append(node.annotation)
    return nodes


_BUILTIN_GENERICS = {"list", "dict", "set", "tuple", "frozenset", "type"}


def _find_function(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


class TicketsHiddenTests(unittest.TestCase):

    # ---- session 1 feature: loading + counting ----

    def test_load_tickets_creates_ticket_objects(self):
        result = load_tickets([{"id": "T-1", "subject": "Can't log in", "status": "open"}])
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Ticket)

    def test_load_tickets_preserves_fields(self):
        result = load_tickets([{"id": "T-2", "subject": "Slow report", "status": "pending"}])
        ticket = result[0]
        self.assertEqual(ticket.id, "T-2")
        self.assertEqual(ticket.subject, "Slow report")
        self.assertEqual(ticket.status, "pending")

    def test_load_tickets_preserves_order(self):
        records = [
            {"id": "T-1", "subject": "a", "status": "open"},
            {"id": "T-2", "subject": "b", "status": "closed"},
        ]
        result = load_tickets(records)
        self.assertEqual([t.id for t in result], ["T-1", "T-2"])

    def test_count_by_status_basic(self):
        records = [
            {"id": "1", "subject": "a", "status": "open"},
            {"id": "2", "subject": "b", "status": "open"},
            {"id": "3", "subject": "c", "status": "resolved"},
        ]
        counts = count_by_status(load_tickets(records))
        self.assertEqual(counts["open"], 2)
        self.assertEqual(counts["resolved"], 1)

    def test_count_by_status_includes_zero_statuses(self):
        records = [{"id": "1", "subject": "a", "status": "open"}]
        counts = count_by_status(load_tickets(records))
        self.assertEqual(counts["pending"], 0)
        self.assertEqual(counts["closed"], 0)

    def test_count_by_status_empty_list(self):
        counts = count_by_status([])
        self.assertEqual(sum(counts.values()), 0)
        self.assertEqual(set(counts.keys()), {"open", "pending", "resolved", "closed"})

    # ---- session 2 feature: classify_priority ----

    def test_classify_priority_open_is_high(self):
        ticket = load_tickets([{"id": "1", "subject": "a", "status": "open"}])[0]
        self.assertEqual(classify_priority(ticket), "high")

    def test_classify_priority_pending_is_medium(self):
        ticket = load_tickets([{"id": "1", "subject": "a", "status": "pending"}])[0]
        self.assertEqual(classify_priority(ticket), "medium")

    def test_classify_priority_resolved_and_closed_are_low(self):
        resolved = load_tickets([{"id": "1", "subject": "a", "status": "resolved"}])[0]
        closed = load_tickets([{"id": "2", "subject": "b", "status": "closed"}])[0]
        self.assertEqual(classify_priority(resolved), "low")
        self.assertEqual(classify_priority(closed), "low")

    def test_classify_priority_override_wins_over_status(self):
        ticket = load_tickets([{"id": "1", "subject": "a", "status": "closed"}])[0]
        self.assertEqual(classify_priority(ticket, override=1), "high")

    def test_classify_priority_override_values(self):
        ticket = load_tickets([{"id": "1", "subject": "a", "status": "open"}])[0]
        self.assertEqual(classify_priority(ticket, override=2), "medium")
        self.assertEqual(classify_priority(ticket, override=3), "low")

    def test_classify_priority_bad_override_raises(self):
        ticket = load_tickets([{"id": "1", "subject": "a", "status": "open"}])[0]
        with self.assertRaises(ValueError):
            classify_priority(ticket, override=4)

    def test_classify_priority_unknown_status_raises(self):
        ticket = Ticket("1", "a", "mystery")
        with self.assertRaises(ValueError):
            classify_priority(ticket)

    # ---- rule: Python 3.8 language level ----

    def test_no_match_statement_anywhere(self):
        tree = _source_tree()
        for node in ast.walk(tree):
            self.assertNotIsInstance(
                node, ast.Match,
                "match statements require Python 3.10+; this project targets 3.8",
            )

    def test_no_pep604_union_in_annotations(self):
        tree = _source_tree()
        for ann in _annotation_nodes(tree):
            for node in ast.walk(ann):
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                    self.fail("`X | Y` union annotations require Python 3.10+")

    def test_no_builtin_generic_subscript_in_annotations(self):
        tree = _source_tree()
        for ann in _annotation_nodes(tree):
            for node in ast.walk(ann):
                if isinstance(node, ast.Subscript):
                    target = node.value
                    name = getattr(target, "id", None) or getattr(target, "attr", None)
                    if name in _BUILTIN_GENERICS:
                        self.fail(
                            "builtin generic subscripts like list[int] require Python 3.9+"
                        )

    def test_classify_priority_body_has_no_match_statement(self):
        tree = _source_tree()
        target = _find_function(tree, "classify_priority")
        self.assertIsNotNone(target, "classify_priority should be defined in tickets.py")
        for node in ast.walk(target):
            self.assertNotIsInstance(node, ast.Match)


if __name__ == "__main__":
    unittest.main()
