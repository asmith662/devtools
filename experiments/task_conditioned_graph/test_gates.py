# Copyright (c) 2026
# ruff: noqa: D103, S101, COM812, FBT001, FBT003
"""Outcome-independent synthetic integer gate boundaries and precedence."""

from dataclasses import replace

import pytest

from experiments.task_conditioned_graph.gates import (
    DecisionInputs,
    bounded,
    decide,
    meaningful_depth,
    meaningful_rank,
)


@pytest.mark.parametrize(
    ("a", "c", "expected"),
    [(None, 10, True), (10, 8, True), (10, 9, False), (0, 0, False), (10, None, False)],
)
def test_meaningful_depth(a: int | None, c: int | None, expected: bool) -> None:
    assert meaningful_depth(a, c) is expected


@pytest.mark.parametrize(
    ("a", "c", "expected"),
    [(10, 8, True), (5, 4, False), (10, 9, False), (None, 1, False)],
)
def test_meaningful_rank(a: int | None, c: int | None, expected: bool) -> None:
    assert meaningful_rank(a, c) is expected


def test_bounds_zero_and_absolute_limits() -> None:
    assert bounded(0, 0, 5)
    assert not bounded(0, 1, 5)
    assert bounded(25, 30, 5)
    assert not bounded(30, 36, 5)
    assert bounded(50, 60, 10)
    assert not bounded(60, 72, 10)
    assert not bounded(10, None, 10)


def test_precedence_hybrid_complementary_harm_and_no_value() -> None:
    inputs = DecisionInputs(
        ((20, 16), (0, 0)), ((20, 16),), (20, 30, 100), (18, 27, 100), True
    )
    assert decide(inputs)["outcome"] == "GRAPH_HYBRID_SUPPORTED"
    assert (
        decide(replace(inputs, c_burden=(20, 30, 100)))["outcome"]
        == "COMPLEMENTARY_GRAPH_VALUE"
    )
    assert (
        decide(replace(inputs, required_ranks=((2, 3),)))["outcome"] == "GRAPH_HARMFUL"
    )
    assert (
        decide(replace(inputs, required_ranks=((2, None),)))["outcome"]
        == "GRAPH_HARMFUL"
    )
    assert decide(replace(inputs, depths=((20, None),)))["outcome"] == "GRAPH_HARMFUL"
    assert (
        decide(replace(inputs, graph_contributed_gain=False))["outcome"]
        == "NO_MATERIAL_VALUE"
    )
    assert (
        decide(replace(inputs, ranking_defect=True))["outcome"]
        == "GRAPH_RANKING_DEFECT"
    )
    assert (
        decide(replace(inputs, contract_defect=True, ranking_defect=True))["outcome"]
        == "EXPERIMENTAL_CONTRACT_DEFECT"
    )
    assert (
        decide(replace(inputs, required_unit_reach_loss=True))["outcome"]
        == "GRAPH_HARMFUL"
    )


def test_reach_rescue_safe_materiality_without_burden_gain() -> None:
    inputs = DecisionInputs(
        ((10, 10),), ((None, 8), (5, 5)), (10, 10, 100), (11, 11, 110), True
    )
    assert decide(inputs)["safe_material_gain"] is True
    assert decide(inputs)["outcome"] == "GRAPH_HYBRID_SUPPORTED"
    assert (
        decide(replace(inputs, required_ranks=((None, 8), (5, 6))))["outcome"]
        == "COMPLEMENTARY_GRAPH_VALUE"
    )


@pytest.mark.parametrize("ranks", [((0, 1),), ((True, 1),), ((-1, 1),), ((1.5, 1),)])
def test_invalid_ranks(ranks: tuple[tuple[int | None, int | None], ...]) -> None:
    with pytest.raises(ValueError, match=r"integers|ranks"):
        decide(DecisionInputs((), ranks, (1, 1, 1), (1, 1, 1), False))
