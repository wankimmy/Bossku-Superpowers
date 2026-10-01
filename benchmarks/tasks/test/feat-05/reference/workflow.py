"""Tiny guarded state machine with a fired-transition history."""


class TransitionError(Exception):
    """No transition rule exists for (name, current state)."""


class GuardRejected(Exception):
    """Rule(s) exist, but every guard for them rejected this context."""


class StateMachine:
    def __init__(self, initial):
        self.current = initial
        self.history = []
        self._transitions = []  # list of (name, source, dest, guard), in add order

    def add_transition(self, name, source, dest, guard=None):
        self._transitions.append((name, source, dest, guard))

    def _candidates(self, name):
        return [t for t in self._transitions if t[0] == name and t[1] == self.current]

    def fire(self, name, context=None):
        context = {} if context is None else context
        candidates = self._candidates(name)
        if not candidates:
            raise TransitionError(f"no transition {name!r} from {self.current!r}")
        for _, _source, dest, guard in candidates:
            if guard is None or guard(context):
                self.history.append({"transition": name, "source": self.current, "dest": dest})
                self.current = dest
                return dest
        raise GuardRejected(f"every guard rejected {name!r} from {self.current!r}")

    def can_fire(self, name, context=None):
        context = {} if context is None else context
        candidates = self._candidates(name)
        return any(guard is None or guard(context) for _, _, _, guard in candidates)
