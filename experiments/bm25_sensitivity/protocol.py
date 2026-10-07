# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention

"""Pre-outcome parameter frame and deterministic multi-objective selection."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from statistics import median
from typing import Any

K1 = (0.6, 0.9, 1.2, 1.5, 1.8, 2.4)
B = (0.0, 0.25, 0.5, 0.75, 1.0)
FILENAME = (0.0, 0.1, 0.25, 0.5, 1.0, 2.0)
BASELINE = (1.2, 0.75, 0.25)
CASES = tuple(range(4, 10))
START = "b1f8413e30bfe870e80f01b08c2fcd81fc633aa6"
GRID = tuple(product(K1, B, FILENAME))


def key(config: tuple[float, float, float]) -> str:
    """Name exact experimental parameter values, without a new framework ID."""
    return "/".join(str(v) for v in config)


def distance(config: tuple[float, float, float]) -> Fraction:
    """Calculate ordinal-grid Manhattan distance only for equivalence ties."""
    return sum(
        (
            Fraction(abs(grid.index(v) - grid.index(base)), len(grid) - 1)
            for grid, v, base in zip((K1, B, FILENAME), config, BASELINE, strict=True)
        ),
        Fraction(),
    )


def select(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply the precommitted role rules with exact rational comparisons."""
    safe = [
        r
        for r in rows
        if r["reach_safe"]
        and tuple(r["parameters"]) != BASELINE
        and r["complete_for_selection"]
    ]
    if not safe:
        return {"roles": {}, "unique_challengers": []}

    def ratios(row: dict[str, Any], name: str) -> list[Fraction]:
        return [
            Fraction(*c["normalized_exact"][name])
            for c in row["cases"]
            if c.get("selection_eligible", True)
        ]

    def tie(row: dict[str, Any]) -> tuple[Fraction, tuple[float, ...]]:
        return distance(tuple(row["parameters"])), tuple(row["parameters"])

    completion = min(
        safe,
        key=lambda r: (
            median(ratios(r, "max_own")),
            max(ratios(r, "max_own")),
            median(ratios(r, "prefix_union")),
            *tie(r),
        ),
    )
    burden = min(
        safe,
        key=lambda r: (
            median(ratios(r, "prefix_union")),
            max(ratios(r, "prefix_union")),
            median(ratios(r, "max_own")),
            *tie(r),
        ),
    )

    def robust_key(row: dict[str, Any]) -> tuple[Any, ...]:
        worst = [
            max(a, b)
            for a, b in zip(
                ratios(row, "max_own"), ratios(row, "prefix_union"), strict=True
            )
        ]
        return max(worst), median(worst), median(ratios(row, "global")), *tie(row)

    robust = min(safe, key=robust_key)
    roles = {
        name: r["parameters"]
        for name, r in (
            ("completion", completion),
            ("burden", burden),
            ("robust", robust),
        )
    }
    return {
        "roles": roles,
        "unique_challengers": [
            list(c) for c in sorted({tuple(v) for v in roles.values()})
        ],
    }
