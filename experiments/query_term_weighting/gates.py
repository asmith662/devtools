# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004 -- literal prospectively frozen integer thresholds
"""Prospective integer decision rule; C is primary, B is diagnostic only."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Comparison:
    """Accept independently validated future gold-dependent comparison metrics."""

    contract: bool
    application: bool
    reach: bool
    depths: tuple[tuple[int | None, int | None], ...]
    required_ranks: tuple[tuple[int | None, int | None], ...]
    unique_resources: tuple[int, int]
    occurrences: tuple[int, int]
    utf8_bytes: tuple[int, int]


def evaluate(evidence: Comparison) -> dict[str, object]:
    """Apply frozen precedence and exact cross-products, never choose a winning arm."""
    numeric = (*evidence.unique_resources, *evidence.occurrences, *evidence.utf8_bytes)
    ranks = (*evidence.depths, *evidence.required_ranks)
    if any(
        type(v) is not bool
        for v in (evidence.contract, evidence.application, evidence.reach)
    ):
        raise ValueError("Invalid boolean contract evidence")
    if any(type(v) is not int or v < 0 for v in numeric) or any(
        type(v) is not int or v <= 0 for pair in ranks for v in pair if v is not None
    ):
        raise ValueError("Invalid exact integer metric")
    if not evidence.depths or not evidence.required_ranks:
        raise ValueError("Empty mandatory gold evidence")
    meaningful = tuple(
        i
        for i, (a, t) in enumerate(evidence.depths)
        if t is not None and (a is None or 5 * t <= 4 * a)
    )
    rank_gain = any(
        a is not None and t is not None and a - t >= 2 and 5 * t <= 4 * a
        for a, t in evidence.required_ranks
    )
    completion_safe = all(a is None or t is not None for a, t in evidence.depths)
    depth_safe = all(
        a is None or (t is not None and t <= a) for a, t in evidence.depths
    )
    rank_safe = all(
        a is None or (t is not None and t <= a) for a, t in evidence.required_ranks
    )
    bounded = (
        completion_safe
        and all(
            a is None or (t is not None and 5 * t <= 6 * a and t - a <= 5)
            for a, t in evidence.depths
        )
        and all(
            a is None or (t is not None and 5 * t <= 6 * a and t - a <= 10)
            for a, t in evidence.required_ranks
        )
    )
    burden = any(
        a > 0 and 10 * t <= 9 * a
        for a, t in (evidence.unique_resources, evidence.occurrences)
    )
    burden_safe = all(
        t <= a
        for a, t in (
            evidence.unique_resources,
            evidence.occurrences,
            evidence.utf8_bytes,
        )
    )
    if not evidence.contract:
        outcome = "EXPERIMENTAL_CONTRACT_DEFECT"
    elif not evidence.application or not evidence.reach:
        outcome = "QUERY_TERM_WEIGHTING_DEFECT"
    elif meaningful and depth_safe and rank_safe and burden and burden_safe:
        outcome = "QUERY_TERM_WEIGHTING_SUPPORTED"
    elif (meaningful or rank_gain) and bounded:
        outcome = "COMPLEMENTARY_QUERY_WEIGHTING_VALUE"
    elif not bounded:
        outcome = "QUERY_TERM_WEIGHTING_HARMFUL"
    else:
        outcome = "NO_MATERIAL_VALUE"
    return {
        "outcome": outcome,
        "meaningful_obligation_indices": meaningful,
        "required_rank_gain": rank_gain,
        "completion_safe": completion_safe,
        "depth_safe": depth_safe,
        "required_rank_safe": rank_safe,
        "bounded_regressions": bounded,
        "ten_percent_burden_gain": burden,
        "burden_safe": burden_safe,
    }
