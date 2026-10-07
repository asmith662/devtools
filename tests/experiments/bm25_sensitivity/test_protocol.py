# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- frozen protocol fixture values
"""Grid/configuration identities and precommitted selection, without outcomes."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from experiments.bm25_sensitivity.protocol import BASELINE, GRID, distance, select
from experiments.retrieval_diagnostics.models import Configuration


def row(
    p: tuple[float, float, float], own: Fraction, union: Fraction
) -> dict[str, Any]:
    """Construct synthetic normalized effects, never historical grid outcomes."""
    return {
        "parameters": p,
        "reach_safe": True,
        "complete_for_selection": True,
        "cases": [
            {
                "normalized_exact": {
                    k: [v.numerator, v.denominator]
                    for k, v in (
                        ("max_own", own),
                        ("prefix_union", union),
                        ("global", Fraction(1)),
                    )
                }
            }
        ],
    }


def test_full_factorial_and_configuration_identity() -> None:
    """Every pre-outcome parameter triple is distinct and legal."""
    assert len(GRID) == len(set(GRID)) == 180
    assert BASELINE in GRID
    assert (
        len(
            {
                Configuration("sensitivity", "fixed-index", "canonical", *p).identity
                for p in GRID
            }
        )
        == 180
    )
    assert distance(BASELINE) == 0


def test_role_selection_is_multiobjective_and_deduplicated() -> None:
    """Completion, burden and minimax may select different safe points."""
    a = row((0.6, 0.0, 0.0), Fraction(1, 2), Fraction(9, 5))
    b = row((0.9, 0.25, 0.1), Fraction(8, 5), Fraction(3, 5))
    c = row((1.5, 0.5, 0.5), Fraction(11, 10), Fraction(11, 10))
    selected = select([a, b, c])
    assert selected["roles"] == {
        "completion": a["parameters"],
        "burden": b["parameters"],
        "robust": c["parameters"],
    }
    assert len(selected["unique_challengers"]) == 3
    assert len(select([a])["unique_challengers"]) == 1


def test_safety_completeness_distance_and_final_tie() -> None:
    """Unsafe/incomplete cannot win; equivalent points use distance then lex."""
    left = row((0.9, 0.75, 0.25), Fraction(1), Fraction(1))
    right = row((1.5, 0.75, 0.25), Fraction(1), Fraction(1))
    farther = row((2.4, 0.75, 0.25), Fraction(1), Fraction(1))
    unsafe = row((0.6, 0.0, 0.0), Fraction(1, 10), Fraction(1, 10))
    unsafe["reach_safe"] = False
    incomplete = row((0.6, 1.0, 0.0), Fraction(1, 10), Fraction(1, 10))
    incomplete["complete_for_selection"] = False
    assert select([right, farther, left, unsafe, incomplete])["unique_challengers"] == [
        list(left["parameters"])
    ]
    assert (
        select([row(BASELINE, Fraction(1), Fraction(1)), unsafe, incomplete])["roles"]
        == {}
    )
