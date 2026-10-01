"""Merge overlapping/touching numeric ranges, with a configurable boundary rule."""


def merge(ranges, inclusive=True):
    items = []
    for idx, (start, end, label) in enumerate(ranges):
        if start > end:
            raise ValueError(f"start must be <= end, got start={start!r} end={end!r}")
        if start == end and not inclusive:
            continue
        items.append((start, end, label, idx))

    items.sort(key=lambda item: item[0])

    def touches(cluster_end, next_start):
        return next_start <= cluster_end if inclusive else next_start < cluster_end

    result = []
    cluster = []
    cluster_end = None
    for item in items:
        if cluster and touches(cluster_end, item[0]):
            cluster.append(item)
            cluster_end = max(cluster_end, item[1])
        else:
            if cluster:
                result.append(_finalize(cluster))
            cluster = [item]
            cluster_end = item[1]
    if cluster:
        result.append(_finalize(cluster))
    return result


def _finalize(cluster):
    start = min(item[0] for item in cluster)
    end = max(item[1] for item in cluster)
    best = min(cluster, key=lambda item: (item[0], -item[1], item[3]))
    return (start, end, best[2])
