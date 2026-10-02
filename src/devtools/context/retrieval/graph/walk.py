# Copyright (c) 2026
"""Shared deterministic stationary random walk arithmetic for Retrieval views."""

from __future__ import annotations

import math


def stationary_distribution(
    outgoing: list[list[tuple[int, float]]],
    seeds: list[float],
    *,
    damping: float,
    tolerance: float,
    maximum_iterations: int,
) -> tuple[list[float], int, bool]:
    """Iterate normalized rows with explicit restart and dangling distribution.

    Callers own graph validation and seed semantics. An empty graph yields an
    empty converged distribution. Operation order follows the supplied view.
    """
    if not seeds:
        return [], 0, True
    scores = seeds.copy()
    converged = False
    iterations = 0
    for _ in range(maximum_iterations):
        iterations += 1
        next_scores = [(1 - damping) * seed for seed in seeds]
        dangling = math.fsum(scores[i] for i, edges in enumerate(outgoing) if not edges)
        for i, seed in enumerate(seeds):
            next_scores[i] += damping * dangling * seed
        for i, edges in enumerate(outgoing):
            for target, probability in edges:
                next_scores[target] += damping * scores[i] * probability
        delta = math.fsum(abs(a - b) for a, b in zip(scores, next_scores, strict=True))
        scores = next_scores
        if delta <= tolerance:
            converged = True
            break
    mass = math.fsum(scores)
    return [score / mass for score in scores], iterations, converged
