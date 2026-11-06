# mypy: disable-error-code="import-untyped"
# Copyright (c) 2026
"""Opt-in dense binary64 kernel qualification; retained v2 mathematics is truth."""

import math

from devtools.learning.regression.state import FittedRegression
from devtools.learning.regression.verification import inspect_knn_query

_KERNEL_DIMENSION_LIMIT = 16
_NEIGHBOR_COUNT = 5

STRICT = "native-regression-parity-v1"
IDENTICAL = "native-knn-identical-vector-parity-v2"


def zero_residual_bound(row: tuple[float, ...]) -> float:
    """Squared-norm/DOT/GEMM roundoff envelope, only for identical vectors."""
    if not 1 <= len(row) <= _KERNEL_DIMENSION_LIMIT or any(
        not math.isfinite(v) for v in row
    ):
        msg = "bounded finite binary64 coordinates required"
        raise ValueError(msg)
    u = 2.0 ** (-53)
    n = len(row) + 2
    squared_bound = 8 * (n * u / (1 - n * u)) * math.fsum(v * v for v in row)
    if not math.isfinite(squared_bound):
        msg = "native cancellation bound overflow"
        raise ValueError(msg)
    return math.sqrt(squared_bound)


def inspect_native_query(
    state: FittedRegression,
    row: tuple[float, ...],
    native_ids: tuple[str, ...],
    native_distances: tuple[float, ...],
    native_value: float,
) -> tuple[str, ...]:
    """Reconstruct exact membership/arithmetic; classify native zeros narrowly."""
    if dict(state.backend).get("sklearn") != "1.9.1":
        msg = "unqualified native kernel version"
        raise ValueError(msg)
    ids, distances, value, separated = inspect_knn_query(state, row)
    if (
        len(native_ids) != _NEIGHBOR_COUNT
        or len(set(native_ids)) != _NEIGHBOR_COUNT
        or len(native_distances) != _NEIGHBOR_COUNT
        or any(not math.isfinite(d) or d < 0 for d in native_distances)
        or (not math.isfinite(native_value))
        or (not set(native_ids) <= set(state.training_row_ids))
    ):
        msg = "invalid original native neighbor evidence"
        raise ValueError(msg)
    if separated and set(native_ids) != set(ids):
        msg = "native and retained neighbor identities disagree"
        raise ValueError(msg)
    if separated and (
        not math.isclose(native_value, value, rel_tol=1e-10, abs_tol=1e-12)
    ):
        msg = "native and retained predictions disagree"
        raise ValueError(msg)
    actual = dict(zip(native_ids, native_distances, strict=True))
    if not (state.neighbor_features is not None):
        msg_0 = "Required numerical state invariant is absent."
        raise AssertionError(msg_0)
    corpus = dict(
        zip(state.training_row_ids, state.neighbor_features.rows, strict=True),
    )
    if not (state.neighbor_targets is not None):
        msg_0 = "Required numerical state invariant is absent."
        raise AssertionError(msg_0)
    targets = dict(zip(state.training_row_ids, state.neighbor_targets, strict=True))
    if not math.isclose(
        native_value,
        math.fsum(targets[i] for i in native_ids) / 5,
        rel_tol=1e-10,
        abs_tol=1e-12,
    ):
        msg = "native target averaging differs"
        raise ValueError(msg)
    if not separated:
        cutoff = distances[-1]
        ranked = {
            i: math.hypot(*(a - b for a, b in zip(row, r, strict=True)))
            for i, r in corpus.items()
        }
        required = {
            i
            for i, d in ranked.items()
            if d < cutoff
            and (not math.isclose(d, cutoff, rel_tol=1e-12, abs_tol=1e-12))
        }
        allowed = {
            i
            for i, d in ranked.items()
            if d <= cutoff or math.isclose(d, cutoff, rel_tol=1e-12, abs_tol=1e-12)
        }
        if not required <= set(native_ids) <= allowed:
            msg = "native boundary neighbor rank differs"
            raise ValueError(msg)
    classifications = [] if separated else ["NATIVE_BOUNDARY_DIAGNOSTIC"]
    for identity in native_ids:
        distance = math.hypot(
            *(a - b for a, b in zip(row, corpus[identity], strict=True)),
        )
        observed = actual[identity]
        if math.isclose(observed, distance, rel_tol=1e-10, abs_tol=1e-12):
            classifications.append("ORDINARY_PARITY")
            continue
        identical = all(
            (a.hex() == b.hex() for a, b in zip(row, corpus[identity], strict=True)),
        )
        if (
            distance != 0.0
            or not identical
            or math.hypot(*(a - b for a, b in zip(row, corpus[identity], strict=True)))
            != 0.0
            or (observed > zero_residual_bound(row))
        ):
            msg = "unsupported native distance discrepancy"
            raise ValueError(msg)
        classifications.append("IDENTICAL_VECTOR_CANCELLATION")
    return tuple(classifications)
