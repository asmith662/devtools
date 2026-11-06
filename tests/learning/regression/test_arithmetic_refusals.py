# Copyright (c) 2026
"""Exact arithmetic failures and defensive guards on corrupted retained copies."""

from __future__ import annotations

import copy
import math
from dataclasses import asdict, replace
from typing import TYPE_CHECKING

import pytest

from devtools.learning.integrations.local.classification.codec import (
    document,
    preparation,
)
from devtools.learning.integrations.local.regression.codec import predictions, state
from devtools.learning.regression.contracts import RegressionSpecification
from devtools.learning.regression.state import (
    FittedRegression,
    deterministic_neighbors,
    finite,
    neighbors,
    training_mean,
    validate_training_state,
)
from devtools.learning.regression.verification import inspect_knn_query

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.learning.regression.contracts import RegressionPopulation

type Witnesses = Callable[[str], tuple[FittedRegression, RegressionPopulation]]


@pytest.mark.parametrize("values", [(), (float("inf"),), (1e308, 1e308)])
def test_unrepresentable_training_mean_is_not_a_fitted_result(
    values: tuple[float, ...],
) -> None:
    """The original sum is bounded before division; no compensated policy change."""
    with pytest.raises(ValueError, match=r"finite nonempty|training mean"):
        training_mean(values)


def test_nonfinite_distance_and_ambiguous_legacy_boundary_refuse() -> None:
    """Legacy five-neighbor ambiguity cannot silently use the v2 tie contract."""
    with pytest.raises(ValueError, match="not finitely"):
        finite(float("inf"))
    with pytest.raises(ValueError, match="bounded retained"):
        neighbors(((0.0,),), (0.0,))
    with pytest.raises(ValueError, match="ambiguous"):
        neighbors(((0.0,),) * 6, (0.0,))
    with pytest.raises(ValueError, match="complete identified"):
        deterministic_neighbors(((0.0,),) * 5, (0.0,), ("duplicate",) * 5)


@pytest.mark.parametrize("deterministic", [False, True])
def test_math_backend_overflow_remains_explicit(
    monkeypatch: pytest.MonkeyPatch,
    *,
    deterministic: bool,
) -> None:
    """Simulated library overflow verifies custody, not a native numerical outcome."""

    def fail(*_: object) -> float:
        message = "simulated math.dist failure"
        raise OverflowError(message)

    monkeypatch.setattr(math, "dist", fail)
    corpus = tuple((float(i),) for i in range(5))

    def compute() -> None:
        if deterministic:
            deterministic_neighbors(corpus, (0.0,), tuple(str(i) for i in range(5)))
        else:
            neighbors(corpus, (0.0,))

    with pytest.raises(ValueError, match=r"Euclidean distance|distance/identity"):
        compute()


@pytest.mark.parametrize("field", ["neighbor_features", "neighbor_targets"])
def test_in_memory_corruption_never_becomes_label_free_predictions(
    fitted_states: Witnesses,
    field: str,
) -> None:
    """Only the copied object is corrupted; genuine witness and ledger are retained."""
    original, training = fitted_states("knn-v2")
    damaged = copy.copy(original)
    object.__setattr__(damaged, field, None)
    with pytest.raises(AssertionError, match="invariant is absent"):
        damaged.predict(training.inputs)
    with pytest.raises(ValueError, match="source-bound neighbor corpus"):
        validate_training_state(damaged, training)
    object.__setattr__(damaged, "preparation", None)
    with pytest.raises(AssertionError, match="invariant is absent"):
        validate_training_state(damaged, training)


def test_wrong_capacity_and_legacy_specification_cannot_enter_v2_inspection(
    fitted_states: Witnesses,
) -> None:
    """Specification and capacity remain separately versioned correspondence."""
    original, _ = fitted_states("knn-v2")
    with pytest.raises(ValueError, match="capacity-v2 state"):
        replace(original, version="fitted-regression-v1")
    damaged = copy.copy(original)
    object.__setattr__(
        damaged,
        "specification",
        RegressionSpecification(original.specification.method),
    )
    with pytest.raises(ValueError, match="deterministic numerical"):
        inspect_knn_query(damaged, (0.0,) * len(original.feature_names))


def test_regression_and_preparation_codecs_preserve_original_meaning(
    fitted_states: Witnesses,
) -> None:
    """Round-trip real predictions; refuse extra schema, coercion and payload excess."""
    original, training = fitted_states("knn-v2")
    raw = document(asdict(original))
    predicted = original.predict(training.inputs)
    assert predictions(document(asdict(predicted))) == predicted
    for bound in (0, True, 1 << 30):
        with pytest.raises(ValueError, match="explicit bounded"):
            state(raw, maximum_bytes=bound)
    with pytest.raises(ValueError, match="bounded serialized"):
        state(raw, maximum_bytes=1)
    with pytest.raises(ValueError, match="schema fields"):
        state(dict(raw, invented=True))
    changed = dict(raw, intercept=0)
    with pytest.raises(TypeError, match="binary64"):
        state(changed)
    assert original.preparation is not None
    prepared = document(asdict(original.preparation))
    with pytest.raises(ValueError, match="standardization meaning"):
        preparation(dict(prepared, invented=True))
