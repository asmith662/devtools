from occupancy import occupied_minutes

cases = [
    ([(1, 5), (3, 8)], (0, 10), 7),
    ([(1, 3), (5, 8)], (2, 6), 3),
    ([(2, 2), (8, 3)], (0, 10), 0),
    ([(0, 10)], (5, 5), 0),
]
for reservations, window, expected in cases:
    actual = occupied_minutes(reservations, window)
    assert actual == expected, (reservations, window, actual, expected)
print("4 focused checks passed")
