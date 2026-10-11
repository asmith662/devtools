# Copyright (c) 2026
# ruff: noqa: S101, COM812, FBT003, ANN401 -- heterogeneous controlled dataclass mutation fixtures
"""Gold-independent controlled boundaries for the frozen R2 decision rule."""

from dataclasses import replace
from typing import Any

import pytest

from experiments.bm25f.gates import Comparison, evaluate


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
        ("application", False, "BM25F_IMPLEMENTATION_DEFECT"),
        ("reach", False, "BM25F_IMPLEMENTATION_DEFECT"),
        ("depths", ((100, 80), (10, 11)), "COMPLEMENTARY_BM25F_VALUE"),
        ("depths", ((100, 80), (10, 13)), "BM25F_HARMFUL"),
        ("depths", ((100, 80), (10, None)), "BM25F_HARMFUL"),
        ("required_ranks", ((10, 8), (20, 25)), "BM25F_HARMFUL"),
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
    assert evaluate(e)["outcome"] == "TRUE_BM25F_SUPPORTED"
    assert (
        evaluate(replace(e, depths=((100, 81),)))["outcome"]
        == "COMPLEMENTARY_BM25F_VALUE"
    )
    assert (
        evaluate(replace(e, unique_resources=(100, 91), occurrences=(200, 181)))[
            "outcome"
        ]
        == "COMPLEMENTARY_BM25F_VALUE"
    )
    assert (
        evaluate(replace(e, depths=((None, 1),)))["outcome"] == "TRUE_BM25F_SUPPORTED"
    )
    assert (
        evaluate(replace(e, depths=((100, 80), (25, 30))))["outcome"]
        == "COMPLEMENTARY_BM25F_VALUE"
    )
    assert (
        evaluate(replace(e, depths=((100, 80), (30, 36))))["outcome"] == "BM25F_HARMFUL"
    )
    tied = replace(
        e,
        depths=((100, 100),),
        required_ranks=((10, 10),),
        unique_resources=(100, 100),
        occurrences=(200, 200),
    )
    assert evaluate(tied)["outcome"] == "NO_MATERIAL_VALUE"


@pytest.mark.parametrize("ranks", [((-1, 1),), ((True, 1),)])
def test_invalid_rank_metrics_rejected(ranks: tuple[tuple[int, int], ...]) -> None:
    """Future scientific evidence cannot encode zero/negative/floating ranks."""
    with pytest.raises(ValueError, match="Invalid exact integer"):
        evaluate(replace(evidence(), depths=ranks))


def test_zero_task_backed_depth_and_required_rank_boundary() -> None:
    """Complete zero-depth witnesses are valid and tied zeros are not meaningful."""
    e = replace(evidence(), depths=((0, 0),), required_ranks=((10, 10),))
    assert evaluate(e)["outcome"] == "NO_MATERIAL_VALUE"
    assert (
        evaluate(replace(e, depths=((None, 0),)))["outcome"] == "TRUE_BM25F_SUPPORTED"
    )
    with pytest.raises(ValueError, match="Invalid exact integer"):
        evaluate(replace(e, required_ranks=((0, 1),)))
    assert evaluate(replace(e, required_ranks=((10, 8),)))["required_rank_gain"]
    assert not evaluate(replace(e, required_ranks=((5, 4),)))["required_rank_gain"]
    assert evaluate(replace(e, required_ranks=((50, 60),), depths=((100, 80),)))[
        "bounded_regressions"
    ]
    assert not evaluate(replace(e, required_ranks=((55, 66),), depths=((100, 80),)))[
        "bounded_regressions"
    ]
