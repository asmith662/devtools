# Copyright (c) 2026
"""Independent finite expectations and invalid preflight controls."""

# ruff: noqa: D103, PLR2004 -- independent literal expectations
from __future__ import annotations

from dataclasses import replace
from typing import Literal, cast

import pytest

from devtools.evaluation.preflight import OracleComparison, check_oracle_expectations


def comparisons() -> tuple[OracleComparison, ...]:
    # Discrete unit-cell membership independently derives integer interval union.
    reservations = ((1, 3), (5, 8))
    occupied = sum(
        any(start <= t < end for start, end in reservations) for t in range(2, 6)
    )
    return (
        OracleComparison(
            "ordinary",
            "union",
            "normal",
            3,
            len({1, 2, 3}),
            "unit cells",
        ),
        OracleComparison(
            "clip",
            "union",
            "boundary",
            2,
            occupied,
            "unit-cell membership in [2,6)",
        ),
        OracleComparison("empty", "union", "empty", 0, len(set()), "empty cell set"),
    )


def test_consistent_and_original_wrong_literal() -> None:
    cases = comparisons()
    assert check_oracle_expectations(obligations=("union",), comparisons=cases) == ()
    wrong = (cases[0], replace(cases[1], expected=3), cases[2])
    assert check_oracle_expectations(obligations=("union",), comparisons=wrong) == (
        "clip: expected value disagrees with cross-check.",
    )
    assert cases[1].expected == 2


@pytest.mark.parametrize("obligations", [(), ("",), ("union", "union"), ("missing",)])
def test_invalid_or_uncovered_obligations(obligations: tuple[str, ...]) -> None:
    assert check_oracle_expectations(obligations=obligations, comparisons=comparisons())


def test_missing_categories_duplicate_names_and_undocumented_basis() -> None:
    case = replace(comparisons()[0], name="", derivation=" ")
    issues = check_oracle_expectations(obligations=("union",), comparisons=(case, case))
    assert any("names" in issue for issue in issues)
    assert any("empty-input" in issue for issue in issues)
    assert sum("undocumented" in issue for issue in issues) == 2
    assert check_oracle_expectations(obligations=("union",), comparisons=())
    assert any(
        "names" in issue
        for issue in check_oracle_expectations(
            obligations=("union",),
            comparisons=(case, *comparisons()[1:]),
        )
    )
    invalid = replace(
        comparisons()[0],
        category=cast('Literal["normal", "boundary", "empty"]', "unknown"),
    )
    assert check_oracle_expectations(
        obligations=("union",),
        comparisons=(*comparisons(), invalid),
    )


def test_comparison_failure_is_not_a_successful_cross_check() -> None:
    class BrokenEquality:
        __hash__ = object.__hash__

        def __eq__(self, other: object) -> bool:
            msg = "Invalid observation value"
            raise RuntimeError(msg)

    cases = (
        replace(comparisons()[0], independently_derived=BrokenEquality()),
        *comparisons()[1:],
    )
    with pytest.raises(RuntimeError, match="Invalid observation"):
        check_oracle_expectations(obligations=("union",), comparisons=cases)
