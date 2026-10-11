# Copyright (c) 2026
# ruff: noqa: S101, COM812, FBT003, ANN401 -- heterogeneous controlled dataclass mutation fixtures
"""Gold-independent controlled boundaries for the frozen R1.7 decision rule."""

from dataclasses import replace
from typing import Any

import pytest

from experiments.query_term_weighting.gates import Comparison, evaluate


def evidence() -> Comparison:
    """Supply exact meaningful and burden boundaries, no prospective outcomes."""
    return Comparison(
        True,
        True,
        True,
        ((100, 80), (10, 10)),
        ((10, 8), (20, 20)),
        (100, 90),
        (200, 190),
        (1000, 1000),
    )


@pytest.mark.parametrize(
    ("field", "value", "outcome"),
    [
        ("contract", False, "EXPERIMENTAL_CONTRACT_DEFECT"),
        ("application", False, "QUERY_TERM_WEIGHTING_DEFECT"),
        ("reach", False, "QUERY_TERM_WEIGHTING_DEFECT"),
        ("depths", ((100, 80), (10, 11)), "COMPLEMENTARY_QUERY_WEIGHTING_VALUE"),
        ("depths", ((100, 80), (10, 13)), "QUERY_TERM_WEIGHTING_HARMFUL"),
        ("depths", ((100, 80), (10, None)), "QUERY_TERM_WEIGHTING_HARMFUL"),
        ("required_ranks", ((10, 8), (20, 25)), "QUERY_TERM_WEIGHTING_HARMFUL"),
    ],
)
def test_precedence_and_bounded_regressions(
    field: str, value: Any, outcome: str
) -> None:
    """A favorable gain never suppresses an earlier defect or unsafe regression."""
    assert evaluate(replace(evidence(), **{field: value}))["outcome"] == outcome


def test_exact_meaningful_burden_and_regression_boundaries() -> None:
    """Integer cross-products have no rounded threshold decisions."""
    e = evidence()
    assert evaluate(e)["outcome"] == "QUERY_TERM_WEIGHTING_SUPPORTED"
    assert (
        evaluate(replace(e, depths=((100, 81),)))["outcome"]
        == "COMPLEMENTARY_QUERY_WEIGHTING_VALUE"
    )
    assert (
        evaluate(replace(e, unique_resources=(100, 91), occurrences=(200, 181)))[
            "outcome"
        ]
        == "COMPLEMENTARY_QUERY_WEIGHTING_VALUE"
    )
    assert (
        evaluate(replace(e, depths=((None, 1),)))["outcome"]
        == "QUERY_TERM_WEIGHTING_SUPPORTED"
    )
    assert (
        evaluate(replace(e, depths=((100, 80), (25, 30))))["outcome"]
        == "COMPLEMENTARY_QUERY_WEIGHTING_VALUE"
    )
    assert (
        evaluate(replace(e, depths=((100, 80), (30, 36))))["outcome"]
        == "QUERY_TERM_WEIGHTING_HARMFUL"
    )
    tied = replace(
        e,
        depths=((100, 100),),
        required_ranks=((10, 10),),
        unique_resources=(100, 100),
        occurrences=(200, 200),
    )
    assert evaluate(tied)["outcome"] == "NO_MATERIAL_VALUE"


@pytest.mark.parametrize("ranks", [((0, 1),), ((-1, 1),), ((True, 1),)])
def test_invalid_rank_metrics_rejected(ranks: tuple[tuple[int, int], ...]) -> None:
    """Future scientific evidence cannot encode zero/negative/floating ranks."""
    with pytest.raises(ValueError, match="Invalid exact integer"):
        evaluate(replace(evidence(), depths=ranks))
