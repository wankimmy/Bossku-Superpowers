import heapq


def resolve_order(dependencies):
    """Return a valid build order for a dependency graph.

    `dependencies` maps each node name to the list of node names it depends on.
    """
    if not isinstance(dependencies, dict):
        raise TypeError("dependencies must be a dict")

    nodes = set(dependencies.keys())
    for deps in dependencies.values():
        nodes.update(deps)

    deps_of = {n: set(dependencies.get(n, [])) for n in nodes}
    dependents = {n: [] for n in nodes}
    indegree = {n: len(deps_of[n]) for n in nodes}
    for n, deps in deps_of.items():
        for d in deps:
            dependents[d].append(n)

    ready = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for dependent in dependents[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(order) != len(nodes):
        raise ValueError("dependency graph has a cycle")
    return order
