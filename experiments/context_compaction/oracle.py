"""Frozen held-out literal cases; never disclosed to either model."""

import importlib.util
import sys
from pathlib import Path


def grade(root):
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("candidate", root / "reducer.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    def e(s, i, d, status="accepted"):
        return dict(stream=s, id=i, delta=d, status=status)
    cases = [
        ([e("λ", "x", 0), e("λ", "x", 99)], {"λ": 0}),
        ([e("a", "x", -3), e("a", "y", 7)], {"a": 4}),
        ([e("a", "x", 9, "pending"), e("b", "x", 2), e("a", "x", 4)], {"b": 2, "a": 4}),
        ([e("a", "x", 2), e("b", "x", 4), e("a", "x", 8), e("b", "y", -1)], {"a": 2, "b": 3}),
        ([e("a", "x", 5, "rejected")], {}),
    ]
    observed = [module.totals(events) for events, _ in cases]
    assert observed == [expected for _, expected in cases], observed
    return observed


if __name__ == "__main__":
    print(grade(Path(sys.argv[1]).resolve()))
