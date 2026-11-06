# Copyright (c) 2026
"""Actual retained kNN arithmetic against explicitly authored native-report faults.

The witness comes from one genuine contained fit. Altered native reports and
corrupted in-memory copies are controls, not new native measurements or studies.
"""

from __future__ import annotations

import copy
import math
from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.learning.integrations.sklearn.regression import parity
from devtools.learning.integrations.sklearn.regression.parity import (
    inspect_native_query,
    zero_residual_bound,
)
from devtools.learning.regression.state import FittedRegression
from devtools.learning.regression.verification import inspect_knn_query

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.learning.regression.contracts import RegressionPopulation

type Witnesses = Callable[[str], tuple[FittedRegression, RegressionPopulation]]


def _row(state: FittedRegression) -> tuple[float, ...]:
    assert state.neighbor_features is not None
    return state.neighbor_features.rows[0]


def test_authored_report_keeps_ordinary_parity_and_exact_zero_envelope(
    fitted_states: Witnesses,
) -> None:
    """Classify distance cancellation only for bit-identical original vectors."""
    state, _ = fitted_states("knn-v2")
    row = _row(state)
    ids, distances, value, separated = inspect_knn_query(state, row)
    assert separated
    assert inspect_native_query(state, row, ids, distances, value) == (
        "ORDINARY_PARITY",
    ) * len(ids)
    bound = zero_residual_bound(row)
    altered = (bound / 2, *distances[1:])
    assert (
        inspect_native_query(state, row, ids, altered, value)[0]
        == "IDENTICAL_VECTOR_CANCELLATION"
    )
    with pytest.raises(ValueError, match="unsupported native distance"):
        inspect_native_query(state, row, ids, (bound * 2, *distances[1:]), value)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("native_ids", ("foreign",)),
        ("native_ids", ("r0",) * 5),
        ("native_ids", tuple("foreign-" + str(i) for i in range(5))),
        ("native_distances", (0.0,)),
        ("native_distances", (float("nan"),) * 5),
        ("native_distances", (-1.0,) * 5),
        ("native_value", float("nan")),
    ],
)
def test_invalid_native_evidence_never_qualifies(
    fitted_states: Witnesses,
    field: str,
    bad: object,
) -> None:
    """Native metadata cannot invent row membership or finite predictions."""
    state, _ = fitted_states("knn-v2")
    row = _row(state)
    ids, distances, value, _ = inspect_knn_query(state, row)
    report: dict[str, object] = {
        "native_ids": ids,
        "native_distances": distances,
        "native_value": value,
    }
    report[field] = bad
    inspect = cast("Callable[..., tuple[str, ...]]", inspect_native_query)
    with pytest.raises(ValueError, match="invalid original native"):
        inspect(state, row, **report)


def test_separated_native_report_requires_original_membership_and_values(
    fitted_states: Witnesses,
) -> None:
    """A genuine retained witness rejects reported replacements and changed means."""
    state, _ = fitted_states("knn-v2")
    row = _row(state)
    ids, distances, value, separated = inspect_knn_query(state, row)
    assert separated
    assert state.training_row_ids[-1] not in ids
    foreign_members = (*ids[:-1], state.training_row_ids[-1])
    with pytest.raises(ValueError, match="neighbor identities disagree"):
        inspect_native_query(state, row, foreign_members, distances, value)
    with pytest.raises(ValueError, match="predictions disagree"):
        inspect_native_query(state, row, ids, distances, value + 1)
    unqualified = replace(state, backend=(("sklearn", "unqualified"),))
    with pytest.raises(ValueError, match="unqualified native kernel"):
        inspect_native_query(unqualified, row, ids, distances, value)


def test_boundary_tie_is_diagnostic_and_does_not_replace_retained_truth(
    fitted_states: Witnesses,
) -> None:
    """Allow native tie alternatives only within the original distance boundary."""
    state, _ = fitted_states("knn-v2")
    assert state.neighbor_features is not None
    assert state.neighbor_targets is not None
    row = (0.0,) * len(state.feature_names)
    ids, distances, value, separated = inspect_knn_query(state, row)
    assert not separated
    corpus = dict(
        zip(state.training_row_ids, state.neighbor_features.rows, strict=True),
    )
    targets = dict(zip(state.training_row_ids, state.neighbor_targets, strict=True))
    ranked = {i: math.dist(row, r) for i, r in corpus.items()}
    alternative = next(
        i
        for i, distance in ranked.items()
        if i not in ids and math.isclose(distance, distances[-1])
    )
    replaced = next(i for i in ids if math.isclose(ranked[i], distances[-1]))
    native_ids = tuple(alternative if i == replaced else i for i in ids)
    native_distances = tuple(ranked[i] for i in native_ids)
    native_value = math.fsum(targets[i] for i in native_ids) / 5
    assert native_value != value
    assert (
        inspect_native_query(state, row, native_ids, native_distances, native_value)[0]
        == "NATIVE_BOUNDARY_DIAGNOSTIC"
    )
    with pytest.raises(ValueError, match="target averaging differs"):
        inspect_native_query(state, row, native_ids, native_distances, native_value + 1)
    outside = next(i for i in corpus if ranked[i] > distances[-1])
    wrong_ids = (*ids[:-1], outside)
    wrong_distances = tuple(ranked[i] for i in wrong_ids)
    wrong_value = math.fsum(targets[i] for i in wrong_ids) / 5
    with pytest.raises(ValueError, match="boundary neighbor rank"):
        inspect_native_query(state, row, wrong_ids, wrong_distances, wrong_value)


@pytest.mark.parametrize("row", [(), (0.0,) * 17, (float("inf"),), (1e308,)])
def test_unqualified_cancellation_envelopes_refuse(row: tuple[float, ...]) -> None:
    """The rounding envelope is finite and bounded, rather than a relaxed tolerance."""
    with pytest.raises(ValueError, match=r"bounded finite|bound overflow"):
        zero_residual_bound(row)


@pytest.mark.parametrize("field", ["neighbor_features", "neighbor_targets"])
def test_corrupt_corpus_cannot_pass_even_with_a_faulty_oracle_reply(
    fitted_states: Witnesses,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
) -> None:
    """Inject memory corruption and an oracle fault; both guards still refuse."""
    state, _ = fitted_states("knn-v2")
    row = _row(state)
    report = inspect_knn_query(state, row)
    broken = copy.copy(state)
    assert broken is not state
    object.__setattr__(broken, field, None)
    with pytest.raises(AssertionError, match="state invariant"):
        inspect_knn_query(broken, row)
    monkeypatch.setattr(parity, "inspect_knn_query", lambda *_args: report)
    with pytest.raises(AssertionError, match="state invariant"):
        inspect_native_query(broken, row, report[0], report[1], report[2])
