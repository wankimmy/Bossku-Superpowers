"""Groups: membership and inheritance ("extends") between groups."""


class Group:
    def __init__(self, name, members=None):
        self.name = name
        self.members = [] if members is None else members
        self.parents = []

    def extend(self, other):
        """This group inherits every rule granted/denied on `other`."""
        self.parents.append(other)

    def add_member(self, user):
        if user not in self.members:
            self.members.append(user)
