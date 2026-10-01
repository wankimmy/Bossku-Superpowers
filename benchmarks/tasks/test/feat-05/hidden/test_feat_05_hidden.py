import unittest

from workflow import StateMachine, TransitionError, GuardRejected


class ExceptionShapeTests(unittest.TestCase):
    def test_exceptions_are_independent(self):
        self.assertTrue(issubclass(TransitionError, Exception))
        self.assertTrue(issubclass(GuardRejected, Exception))
        self.assertFalse(issubclass(GuardRejected, TransitionError))
        self.assertFalse(issubclass(TransitionError, GuardRejected))


class StateMachineTests(unittest.TestCase):
    def test_initial_state_and_empty_history(self):
        sm = StateMachine("new")
        self.assertEqual(sm.current, "new")
        self.assertEqual(sm.history, [])

    def test_simple_successful_transition(self):
        sm = StateMachine("new")
        sm.add_transition("submit", "new", "pending")
        result = sm.fire("submit")
        self.assertEqual(result, "pending")
        self.assertEqual(sm.current, "pending")
        self.assertEqual(sm.history, [{"transition": "submit", "source": "new", "dest": "pending"}])

    def test_unregistered_name_raises_transition_error(self):
        sm = StateMachine("new")
        sm.add_transition("submit", "new", "pending")
        with self.assertRaises(TransitionError):
            sm.fire("nope")
        self.assertEqual(sm.current, "new")
        self.assertEqual(sm.history, [])

    def test_name_registered_from_different_source_raises_transition_error(self):
        sm = StateMachine("new")
        sm.add_transition("approve", "pending", "done")
        with self.assertRaises(TransitionError):
            sm.fire("approve")
        self.assertEqual(sm.current, "new")
        self.assertEqual(sm.history, [])

    def test_guard_false_raises_guard_rejected_and_state_unchanged(self):
        sm = StateMachine("new")
        sm.add_transition("submit", "new", "pending", guard=lambda ctx: False)
        with self.assertRaises(GuardRejected):
            sm.fire("submit")
        self.assertEqual(sm.current, "new")
        self.assertEqual(sm.history, [])

    def test_guard_receives_the_context_passed_to_fire(self):
        seen = []

        def guard(ctx):
            seen.append(ctx)
            return ctx.get("approved", False)

        sm = StateMachine("pending")
        sm.add_transition("approve", "pending", "done", guard=guard)
        sm.fire("approve", context={"approved": True})
        self.assertEqual(sm.current, "done")
        self.assertEqual(seen, [{"approved": True}])

    def test_default_context_is_empty_dict_when_omitted(self):
        sm = StateMachine("pending")
        sm.add_transition("approve", "pending", "done", guard=lambda ctx: ctx == {})
        sm.fire("approve")
        self.assertEqual(sm.current, "done")

    def test_first_passing_guard_among_candidates_wins_not_first_overall(self):
        sm = StateMachine("A")
        sm.add_transition("go", "A", "X", guard=lambda ctx: False)
        sm.add_transition("go", "A", "Y", guard=lambda ctx: True)
        sm.add_transition("go", "A", "Z", guard=lambda ctx: True)
        sm.fire("go")
        self.assertEqual(sm.current, "Y")

    def test_all_guards_rejecting_raises_guard_rejected_even_with_candidates(self):
        sm = StateMachine("A")
        sm.add_transition("go", "A", "X", guard=lambda ctx: False)
        sm.add_transition("go", "A", "Y", guard=lambda ctx: False)
        with self.assertRaises(GuardRejected):
            sm.fire("go")
        self.assertEqual(sm.current, "A")
        self.assertEqual(sm.history, [])

    def test_unguarded_fallback_used_only_when_earlier_guards_reject(self):
        sm = StateMachine("A")
        sm.add_transition("go", "A", "X", guard=lambda ctx: False)
        sm.add_transition("go", "A", "FALLBACK", guard=None)
        sm.fire("go")
        self.assertEqual(sm.current, "FALLBACK")

    def test_can_fire_matches_whether_fire_would_succeed(self):
        sm = StateMachine("A")
        sm.add_transition("go", "A", "B", guard=lambda ctx: ctx.get("ok"))
        self.assertFalse(sm.can_fire("go"))
        self.assertTrue(sm.can_fire("go", context={"ok": True}))
        self.assertFalse(sm.can_fire("missing"))
        self.assertEqual(sm.current, "A")
        self.assertEqual(sm.history, [])

    def test_can_fire_repeated_calls_never_mutate_state_or_history(self):
        sm = StateMachine("A")
        sm.add_transition("go", "A", "B")
        for _ in range(5):
            self.assertTrue(sm.can_fire("go"))
        self.assertEqual(sm.current, "A")
        self.assertEqual(sm.history, [])

    def test_sequential_multi_step_workflow_records_history_in_order(self):
        sm = StateMachine("new")
        sm.add_transition("submit", "new", "pending")
        sm.add_transition("approve", "pending", "done")
        sm.fire("submit")
        sm.fire("approve")
        self.assertEqual(sm.current, "done")
        self.assertEqual(sm.history, [
            {"transition": "submit", "source": "new", "dest": "pending"},
            {"transition": "approve", "source": "pending", "dest": "done"},
        ])

    def test_same_transition_name_from_different_sources_is_independent(self):
        sm1 = StateMachine("failed")
        sm1.add_transition("retry", "failed", "pending")
        sm1.add_transition("retry", "timeout", "pending")
        sm1.fire("retry")
        self.assertEqual(sm1.current, "pending")

        sm2 = StateMachine("timeout")
        sm2.add_transition("retry", "failed", "pending")
        sm2.add_transition("retry", "timeout", "pending")
        sm2.fire("retry")
        self.assertEqual(sm2.current, "pending")


if __name__ == "__main__":
    unittest.main()
