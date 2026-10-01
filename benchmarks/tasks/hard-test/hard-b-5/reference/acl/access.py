"""Resolve whether a user has a permission, given groups and rules."""

from .groups import Group


def _key(value):
    return value.strip().lower()


class AccessControl:
    def __init__(self):
        self._groups = {}
        self._allows = set()
        self._denies = set()
        self._cache = {}

    def add_group(self, name):
        key = _key(name)
        if key in self._groups:
            raise ValueError(f"group {name!r} already exists")
        group = Group(name)
        self._groups[key] = group
        return group

    def group(self, name):
        return self._groups[_key(name)]

    def add_member(self, group_name, user):
        group = self._groups[_key(group_name)]
        group.add_member(_key(user))
        self._cache.clear()

    def grant_user(self, user, permission):
        key = (_key(user), _key(permission))
        self._denies.discard(key)
        self._allows.add(key)
        self._cache.clear()

    def deny_user(self, user, permission):
        key = (_key(user), _key(permission))
        self._allows.discard(key)
        self._denies.add(key)
        self._cache.clear()

    def grant_group(self, group_name, permission):
        key = (_key(group_name), _key(permission))
        self._denies.discard(key)
        self._allows.add(key)
        self._cache.clear()

    def deny_group(self, group_name, permission):
        key = (_key(group_name), _key(permission))
        self._allows.discard(key)
        self._denies.add(key)
        self._cache.clear()

    def _user_groups(self, user):
        key = _key(user)
        return [g for g in self._groups.values() if key in g.members]

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
        reachable = self._reachable_groups(user)
        permission_key = _key(permission)
        if any((_key(g.name), permission_key) in self._denies for g in reachable):
            return False
        if any((_key(g.name), permission_key) in self._allows for g in reachable):
            return True
        return None

    def can(self, user, permission):
        key = (_key(user), _key(permission))
        if key not in self._cache:
            if key in self._denies:
                verdict = False
            elif key in self._allows:
                verdict = True
            else:
                verdict = bool(self._group_verdict(user, permission))
            self._cache[key] = verdict
        return self._cache[key]
