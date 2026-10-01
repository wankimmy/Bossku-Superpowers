"""Build a human-readable report of feature flag state."""

import flags


def build_report():
    """Return a report of every flag that has ever been explicitly enabled
    or disabled, sorted alphabetically, one per line as "name: ON"/"name: OFF".
    If nothing has ever been set, return "no flags configured"."""
    current = flags.all_flags()
    if not current:
        return "no flags configured"
    lines = [
        f"{name}: {'ON' if state else 'OFF'}" for name, state in sorted(current.items())
    ]
    return "\n".join(lines)
