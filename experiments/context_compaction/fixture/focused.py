"""Visible fixed acceptance examples, not a reference implementation."""

from reducer import totals


def event(stream, identity, delta, status="accepted"):
    return dict(stream=stream, id=identity, delta=delta, status=status)


cases = [
    ([], {}),
    ([event("a", "x", 3), event("a", "x", 99)], {"a": 3}),
    ([event("a", "x", 3), event("b", "x", 7)], {"a": 3, "b": 7}),
    ([event("a", "x", 99, "rejected"), event("a", "x", 4)], {"a": 4}),
]
for index, (events, expected) in enumerate(cases):
    actual = totals(events)
    print(index, actual, expected, flush=True)
    assert actual == expected, (index, actual, expected)
print("FOCUSED:4 passed")
