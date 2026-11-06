# Copyright (c) 2026
"""Independent retained v2 kNN oracle; no selector, native fitting or I/O calls."""

import math

from devtools.learning.regression.state import FittedRegression, finite

_NEIGHBOR_COUNT = 5


def inspect_knn_query(
    state: FittedRegression,
    prepared_row: tuple[float, ...],
) -> tuple[tuple[str, ...], tuple[float, ...], float, bool]:
    """Independent hypot/difference arithmetic and target-blind ordered selection.

    Last flag qualifies original native parity outside the old ambiguity region;
    it does not change v2 ordering. Actual qualified runtime must agree on distance
    rounding. No across-platform portability is inferred.
    """
    if state.specification.version != "regression-specification-v2":
        msg = "explicit deterministic numerical specification required"
        raise ValueError(msg)
    corpus, targets = (state.neighbor_features, state.neighbor_targets)
    if not (corpus is not None):
        msg_0 = "Required numerical state invariant is absent."
        raise AssertionError(msg_0)
    if not (targets is not None):
        msg_0 = "Required numerical state invariant is absent."
        raise AssertionError(msg_0)
    ranking = []
    for index, original in enumerate(corpus.rows):
        differences = tuple(
            (float(a - b) for a, b in zip(prepared_row, original, strict=True)),
        )
        distance = finite(math.hypot(*differences))
        ranking.append((distance, state.training_row_ids[index].encode("utf-8"), index))
    ranking.sort(key=lambda item: (item[0], item[1]))
    selected = ranking[:5]
    ids = tuple((state.training_row_ids[i] for _, _, i in selected))
    distances = tuple((d for d, _, _ in selected))
    value = finite(math.fsum((targets[i] for _, _, i in selected)) / 5)
    separated = len(ranking) == _NEIGHBOR_COUNT or not math.isclose(
        ranking[4][0],
        ranking[5][0],
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    return (ids, distances, value, separated)
