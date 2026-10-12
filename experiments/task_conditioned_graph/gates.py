# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004
"""Prospective Graph-3 C-versus-A integer gates, independent of case outcomes."""

from __future__ import annotations

from dataclasses import dataclass


def meaningful_depth(a: int | None, c: int | None) -> bool:
    """Completion rescue or at least 20 percent nonzero-baseline improvement."""
    return c is not None and (a is None or (a > 0 and 5 * c <= 4 * a))


def meaningful_rank(a: int | None, c: int | None) -> bool:
    """Reach rescue is separate; finite rank gain requires two and 20 percent."""
    return a is not None and c is not None and a - c >= 2 and 5 * c <= 4 * a


def bounded(a: int | None, c: int | None, absolute: int) -> bool:
    """No baseline loss, 20 percent plus absolute bound; zero stays zero."""
    return a is None or (c is not None and 5 * c <= 6 * a and c - a <= absolute)


@dataclass(frozen=True)
class DecisionInputs:
    """Reviewed metrics only; graph contribution must have captured provenance."""

    depths: tuple[tuple[int | None, int | None], ...]
    required_ranks: tuple[tuple[int | None, int | None], ...]
    a_burden: tuple[int, int, int]  # unique, occurrences, distinct bytes
    c_burden: tuple[int, int, int]
    graph_contributed_gain: bool
    contract_defect: bool = False
    ranking_defect: bool = False
    required_unit_reach_loss: bool = False


def decide(values: DecisionInputs) -> dict[str, bool | str]:
    """Apply frozen precedence without costs, diagnostic map or top-K votes.

    Safe materiality = a graph-contributed REQUIRED-cell reach rescue (one cell
    minimum), with no selected depth or baseline-reached REQUIRED rank worsening.
    Strong burden = positive baseline, 10 percent unique or occurrence reduction,
    all three burden dimensions nonincreasing. B alone does not select outcome.
    """
    pairs = (*values.depths, *values.required_ranks)
    if any((n is not None and (type(n) is not int or n < 0)) for p in pairs for n in p):
        raise ValueError("Depths/ranks must be nonnegative integers or unreached")
    if any(n is not None and n == 0 for pair in values.required_ranks for n in pair):
        raise ValueError("Reached ranks start at one")
    if any(type(n) is not int or n < 0 for n in (*values.a_burden, *values.c_burden)):
        raise ValueError("Burden must be nonnegative")
    witness_gain = any(meaningful_depth(a, c) for a, c in values.depths)
    rank_gain = any(meaningful_rank(a, c) for a, c in values.required_ranks)
    rescue = any(a is None and c is not None for a, c in values.required_ranks)
    loss = values.required_unit_reach_loss or any(
        a is not None and c is None for a, c in values.required_ranks
    )
    completion_loss = any(a is not None and c is None for a, c in values.depths)
    bounds = all(bounded(a, c, 5) for a, c in values.depths) and all(
        bounded(a, c, 10) for a, c in values.required_ranks
    )
    safety = all(a is None or (c is not None and c <= a) for a, c in pairs)
    au, ao, ab = values.a_burden
    cu, co, cb = values.c_burden
    burden = (
        all(a is not None and c is not None for a, c in values.depths)
        and bool(values.depths)
        and au > 0
        and ao > 0
        and (10 * cu <= 9 * au or 10 * co <= 9 * ao)
        and cu <= au
        and co <= ao
        and cb <= ab
    )
    material = rescue and safety and not loss and values.graph_contributed_gain
    if values.contract_defect:
        outcome = "EXPERIMENTAL_CONTRACT_DEFECT"
    elif values.ranking_defect:
        outcome = "GRAPH_RANKING_DEFECT"
    elif loss or completion_loss or not bounds:
        outcome = "GRAPH_HARMFUL"
    elif (
        (witness_gain or rescue)
        and values.graph_contributed_gain
        and (burden or material)
    ):
        outcome = "GRAPH_HYBRID_SUPPORTED"
    elif values.graph_contributed_gain and (witness_gain or rank_gain or rescue):
        outcome = "COMPLEMENTARY_GRAPH_VALUE"
    else:
        outcome = "NO_MATERIAL_VALUE"
    return {
        "outcome": outcome,
        "witness_gain": witness_gain,
        "rank_gain": rank_gain,
        "required_reach_rescue": rescue,
        "required_reach_loss": loss,
        "completion_loss": completion_loss,
        "complementary_bounds": bounds,
        "strong_safety": safety,
        "strong_burden": burden,
        "safe_material_gain": material,
    }
