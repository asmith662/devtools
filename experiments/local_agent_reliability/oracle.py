"""Undisclosed independent union measure; no candidate implementation supplied."""
import importlib.util
import itertools
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("candidate", Path(sys.argv[1]) / "occupancy.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
literal = [
    ([(2, 10), (4, 6)], (0, 12), 8),
    ([(4, 6), (2, 10)], (3, 9), 6),
    ([(1, 3), (3, 7)], (0, 10), 6),
    ([(1.5, 3.5), (2.5, 5.0)], (2.0, 4.5), 2.5),
    ([(-5, 2), (-2, 4), (7, 1)], (-3, 3), 6),
    ([], (0, 2), 0),
    ([(0, 20)], (10, 1), 0),
]
for intervals, window, expected in literal:
    before = list(intervals)
    assert module.occupied_minutes(intervals, window) == expected
    assert intervals == before
count = 0
choices = [(-2, 3), (0, 1), (1, 4), (2, 2), (3, 1)]
for intervals in itertools.product(choices, repeat=3):
    expected = sum(any(a <= point < b for a, b in intervals) for point in range(-1, 4))
    assert module.occupied_minutes(intervals, (-1, 4)) == expected
    count += 1
print("7 literal and", count, "independent grid checks passed")
