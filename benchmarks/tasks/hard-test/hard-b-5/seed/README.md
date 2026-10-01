# Access Control

Resolves whether a user can perform a permission, through direct rules
and group membership (with group inheritance).

Run tests: `python -m unittest discover -s tests`

## Groups

- `AccessControl.add_group(name)` creates and returns a `Group`. Raises
  `ValueError` if the (normalized) name already exists.
- `AccessControl.group(name)` looks it up; raises `KeyError` if it
  doesn't exist.
- `AccessControl.add_member(group_name, user)` adds `user` (any
  hashable id, typically a string) to that group. Adding the same user
  twice is a no-op. Raises `KeyError` if the group doesn't exist. A
  brand-new `Group` always starts with no members of its own - a
  member list is never shared between `Group` instances.
- `Group.extend(other_group)` makes this group inherit every rule
  granted or denied on `other_group` (see "Resolution order" below).
  Inheritance is transitive: if C extends B and B extends A, C
  inherits both B's and A's rules. If the hierarchy ever contains a
  cycle, resolution simply never visits the same group twice - it does
  not raise and does not loop forever.
- User ids, group names, and permission strings are all matched
  **case-insensitively**, ignoring leading/trailing whitespace,
  everywhere one is accepted.

## Rules

- `grant_user(user, permission)` / `deny_user(user, permission)`: a
  direct rule on one specific user.
- `grant_group(group_name, permission)` / `deny_group(group_name,
  permission)`: a rule on a group, inherited by every user in that
  group and in every group that (transitively) extends it. These do
  **not** require the group to already exist - a group's rules can be
  set up before or after the `Group` itself.
- Granting/denying the same subject+permission again simply replaces
  the previous verdict for that exact subject.

## Resolution order

`can(user, permission)` resolves in this order:

1. If `user` has a direct `deny_user` for `permission` -> **deny**.
2. Else if `user` has a direct `grant_user` for `permission` -> **allow**.
3. Else, collect every group reachable from `user` (their direct
   groups, plus everything those extend, transitively). If **any**
   reachable group has been `deny_group`'d for `permission` -> **deny**
   - no matter how far away that group is in the hierarchy, a deny
   anywhere always beats an allow anywhere. Else if any reachable
   group has been `grant_group`'d for `permission` -> **allow**.
4. Otherwise (nothing matched anywhere) -> **deny** (the default).

`can()` returns a plain `bool` (`True` for allow, `False` for deny).

## Caching

`can()`'s result is cached per `(user, permission)` pair for speed.
The very next call after **any** relevant change - `grant_user`,
`deny_user`, `grant_group`, `deny_group`, or `add_member` - must
already reflect that change. There is never a stale cached answer.
