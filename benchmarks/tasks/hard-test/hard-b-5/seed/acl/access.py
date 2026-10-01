"""Resolve whether a user has a permission, given groups and rules."""

from .groups import Group


class AccessControl:
    def __init__(self):
        self._groups = {}
        self._allows = set()
        self._denies = set()
        self._cache = {}

    def add_group(self, name):
        if name in self._groups:
            raise ValueError(f"group {name!r} already exists")
        group = Group(name)
        self._groups[name] = group
        return group

    def group(self, name):
        return self._groups[name]

    def add_member(self, group_name, user):
        group = self._groups[group_name]
        group.add_member(user)

    def grant_user(self, user, permission):
        self._denies.discard((user, permission))
        self._allows.add((user, permission))
        self._cache.clear()

    def deny_user(self, user, permission):
        self._allows.discard((user, permission))
        self._denies.add((user, permission))
        self._cache.clear()

    def grant_group(self, group_name, permission):
        self._denies.discard((group_name, permission))
        self._allows.add((group_name, permission))
        self._cache.clear()

    def deny_group(self, group_name, permission):
        self._allows.discard((group_name, permission))
        self._denies.add((group_name, permission))
        self._cache.clear()

    def _user_groups(self, user):
        return [g for g in self._groups.values() if user in g.members]

    def _reachable_groups(self, user):
        """Every group the user belongs to, plus every group those
        extend (transitively), each visited at most once."""
        visited = []
        seen = set()
        stack = list(self._user_groups(user))
        while stack:
            group = stack.pop()
            if group.name in seen:
                continue
            seen.add(group.name)
            visited.append(group)
            stack.extend(group.parents)
        return visited

    def _group_verdict(self, user, permission):
        for group in self._reachable_groups(user):
            if (group.name, permission) in self._denies:
                return False
            if (group.name, permission) in self._allows:
                return True
        return None

    def can(self, user, permission):
        key = (user, permission)
        if key not in self._cache:
            if (user, permission) in self._denies:
                verdict = False
            elif (user, permission) in self._allows:
                verdict = True
            else:
                verdict = bool(self._group_verdict(user, permission))
            self._cache[key] = verdict
        return self._cache[key]
