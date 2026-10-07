# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention

"""Alternative-aware obligation metrics without converting rank into satisfaction."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from experiments.bm25_sensitivity.cases import Case
    from experiments.retrieval_diagnostics.mechanics import Mechanics


def completion(
    choices: tuple[tuple[str, tuple[str, ...]], ...], ranks: dict[str, int]
) -> int | None:
    """Require every member of one accepted alternative, never mix alternatives."""
    valid = [
        (max(ranks[p] for p in members), identity)
        for identity, members in choices
        if all(p in ranks for p in members)
    ]
    return min(valid)[0] if valid else None


def measure(case: Case, engines: dict[str, Mechanics]) -> dict[str, Any]:
    """Retain absolute metrics, sufficient alternatives and exact reach sets."""
    global_rows = engines["global"].capture.rows
    global_rank = {r.resource.address.value: r.rank for r in global_rows}
    required = {
        j.resource.address.value
        for js in case.judgments.values()
        for j in js
        if j.label == "REQUIRED"
    }
    own_reached: set[tuple[str, str]] = set()
    reachable_units: set[tuple[str, str]] = set()
    depths = {}
    composition: Counter[str] = Counter()
    union: set[str] = set()
    occurrences = 0
    top: dict[str, Counter[str]] = {str(k): Counter() for k in (5, 10, 20)}
    top_n = {str(k): 0 for k in (5, 10, 20)}
    global_depths = []
    for ob, js in case.judgments.items():
        ranks = {p: r.rank for p, r in engines[ob].rows.items()}
        labels = {j.resource.address.value: j.label for j in js}
        for j in js:
            if j.label == "REQUIRED" and j.resource.address.value in ranks:
                own_reached.add((ob, j.resource.address.value))
                reachable_units.update((ob, u) for u in j.units)
        depths[ob] = completion(case.alternatives[ob], ranks)
        global_depths.append(completion(case.alternatives[ob], global_rank))
        prefix = (
            engines[ob].capture.rows[: depths[ob]] if depths[ob] is not None else ()
        )
        occurrences += len(prefix)
        union.update(r.resource.address.value for r in prefix)
        composition.update(labels[r.resource.address.value] for r in prefix)
        for k in (5, 10, 20):
            rows = engines[ob].capture.rows[:k]
            top[str(k)].update(labels[r.resource.address.value] for r in rows)
            top_n[str(k)] += len(rows)
    lower = min(len(u) for u in case.sufficient_unions)
    complete = all(d is not None for d in depths.values())
    required_units = {
        (ob, u)
        for ob, js in case.judgments.items()
        for j in js
        if j.label == "REQUIRED"
        for u in j.units
    }
    return {
        "case": case.number,
        "resource_count": len(case.documents.documents),
        "obligations": len(case.judgments),
        "required_resource_reach": sorted(required & global_rank.keys()),
        "required_resource_total": len(required),
        "required_cells_reached": sorted(own_reached),
        "required_cells_total": sum(
            j.label == "REQUIRED" for js in case.judgments.values() for j in js
        ),
        "required_unit_judgments_reached": sorted(reachable_units),
        "required_unit_judgments_total": len(required_units),
        "distinct_units_reached": sorted({u for _, u in reachable_units}),
        "distinct_units_total": len({u for _, u in required_units}),
        "global": max(d for d in global_depths if d is not None)
        if all(d is not None for d in global_depths)
        else None,
        "own_depths": depths,
        "max_own": max(d for d in depths.values() if d is not None)
        if complete
        else None,
        "maximum_completable_own": max(
            (d for d in depths.values() if d is not None), default=None
        ),
        "prefix_occurrences": occurrences if complete else None,
        "prefix_union": len(union) if complete else None,
        "complete_prefix_composition": dict(sorted(composition.items()))
        if complete
        else None,
        "known_complete_obligation_prefix_occurrences": occurrences,
        "known_complete_obligation_prefix_union": len(union),
        "minimum_sufficient_union": lower,
        "maximum_sufficient_union": max(len(u) for u in case.sufficient_unions),
        "excess": len(union) - lower if complete else None,
        "top_k": {
            k: {"labels": dict(sorted(v.items())), "denominator": top_n[k]}
            for k, v in top.items()
        },
    }


def normalize(current: dict[str, Any], baseline: dict[str, Any]) -> None:
    """Keep exact rational ratios and set-based required-loss partitions."""
    ratios = {}
    for k in ("global", "max_own", "prefix_union", "prefix_occurrences"):
        x, y = current[k], baseline[k]
        ratios[k] = (
            [Fraction(x, y).numerator, Fraction(x, y).denominator]
            if x is not None and y is not None and y
            else None
        )
    current["normalized_exact"] = ratios
    current["normalized"] = {
        k: v[0] / v[1] if v is not None else None for k, v in ratios.items()
    }
    current["required_losses"] = {
        k: sorted(set(map(tuple, baseline[k])) - set(map(tuple, current[k])))
        if k != "required_resource_reach"
        else sorted(set(baseline[k]) - set(current[k]))
        for k in (
            "required_resource_reach",
            "required_cells_reached",
            "required_unit_judgments_reached",
        )
    }
    current["reach_safe"] = not any(current["required_losses"].values())
