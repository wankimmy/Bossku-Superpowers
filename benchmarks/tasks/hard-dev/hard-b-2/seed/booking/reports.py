"""Simple utilization reporting for a room."""

from .rooms import DAY_MINUTES


def utilization_percent(room):
    """Percentage (0-100, rounded to 1 decimal place) of the day booked."""
    return round(room.booked_minutes() * 100 / DAY_MINUTES, 1)
