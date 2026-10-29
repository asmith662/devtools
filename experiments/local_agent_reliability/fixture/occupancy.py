"""Occupied-time accounting for one room."""


def occupied_minutes(reservations, window):
    """Return occupied duration within the observation window."""
    lower, upper = window
    total = 0
    for start, end in reservations:
        start, end = max(start, lower), min(end, upper)
        if end > start:
            total += end - start
    return total
