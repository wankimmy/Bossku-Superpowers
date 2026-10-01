"""allocate.py - largest-remainder (Hamilton method) proportional
allocation. See README.md for the full specification.
"""

from fractions import Fraction


class AllocationError(ValueError):
    """Raised for a structurally valid but un-allocatable input."""


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int")


def _validate_total(total):
    _check_int(total, "total")
    if total < 0:
        raise AllocationError("total must be non-negative")


def _validate_weights(weights):
    if not isinstance(weights, (list, tuple)):
        raise TypeError("weights must be a list or tuple")
    if len(weights) == 0:
        raise AllocationError("weights must not be empty")
    for w in weights:
        _check_int(w, "each weight")
        if w < 0:
            raise AllocationError("weights must be non-negative")


def _largest_remainder(total, weights):
    n = len(weights)
    if total == 0:
        return [0] * n
    total_weight = sum(weights)
    if total_weight == 0:
        raise AllocationError("cannot allocate a positive total with all-zero weights")
    quotas = [Fraction(total * w, total_weight) for w in weights]
    bases = [q.numerator // q.denominator for q in quotas]
    leftover = total - sum(bases)
    order = sorted(range(n), key=lambda i: (-(quotas[i] - bases[i]), i))
    result = list(bases)
    for k in range(leftover):
        result[order[k]] += 1
    return result


def allocate(total, weights):
    _validate_total(total)
    _validate_weights(weights)
    return _largest_remainder(total, list(weights))


def allocate_with_minimums(total, weights, minimums=None):
    _validate_total(total)
    _validate_weights(weights)
    n = len(weights)
    if minimums is None:
        minimums = [0] * n
    else:
        if not isinstance(minimums, (list, tuple)):
            raise TypeError("minimums must be a list or tuple")
        if len(minimums) != n:
            raise AllocationError("minimums must be the same length as weights")
        for m in minimums:
            _check_int(m, "each minimum")
            if m < 0:
                raise AllocationError("minimums must be non-negative")
        minimums = list(minimums)
    base_sum = sum(minimums)
    if base_sum > total:
        raise AllocationError("minimums exceed total")
    remaining = total - base_sum
    extra = _largest_remainder(remaining, list(weights))
    return [minimums[i] + extra[i] for i in range(n)]
