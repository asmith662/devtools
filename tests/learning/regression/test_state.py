# Copyright (c) 2026
"""Genuine authored fits and adversarial retained-state/source correspondence."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

from devtools.learning.integrations.local.inspection import inspect_learning
from devtools.learning.integrations.local.regression.codec import state as decode_state
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.learning.regression.contracts import RegressionPopulation
from devtools.learning.regression.state import FittedRegression, validate_training_state
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture(scope="module")
def fitted_states(
    tmp_path_factory: pytest.TempPathFactory,
) -> Callable[[str], tuple[FittedRegression, RegressionPopulation]]:
    """Lazily fit each authored method once, under the active per-test collector."""
    root = tmp_path_factory.mktemp("states")
    cache: dict[str, tuple[FittedRegression, RegressionPopulation]] = {}

    def get(method: str) -> tuple[FittedRegression, RegressionPopulation]:
        if method not in cache:
            plan = authored_task("regression").plan(
                method,
                "online",
                "state-control-" + method,
            )
            grant = ExecutionAuthorization(
                plan.identity,
                (method,),
                EvidenceReference(
                    "learning_execution_grant-v1",
                    "state-control",
                    plan.identity,
                ),
            )
            reference = asyncio.run(
                ManagedLearningWorker.current().execute(plan, grant, root / method),
            )
            inspected = inspect_learning(reference, plan, grant)
            saved = json.loads(
                next(
                    (reference.root.value / "publication/generations").glob(
                        "*/result.json",
                    ),
                ).read_bytes(),
            )
            state = decode_state(saved["state"])
            assert inspected.state == state
            training, _ = plan.populations()
            assert isinstance(training, RegressionPopulation)
            cache[method] = state, training
        return cache[method]

    return get


@pytest.mark.parametrize("method", ["mean", "ridge", "knn-v2"])
def test_original_state_and_source_are_independently_valid(
    fitted_states: Callable[[str], tuple[FittedRegression, RegressionPopulation]],
    method: str,
) -> None:
    """Check actual retained fitted arithmetic and its source binding."""
    state, training = fitted_states(method)
    validate_training_state(state, training)
    predicted = state.predict(training.inputs)
    assert predicted.row_ids == training.inputs.row_ids
    assert predicted.target == training.target
    assert state.content_identity.startswith(state.version + ":")


@pytest.mark.parametrize(
    "changes,reason",
    [
        ({"state_id": "foreign"}, "identity"),
        ({"execution_id": "foreign"}, "identity"),
        ({"target": None}, "specification and target"),
        ({"specification": None}, "specification and target"),
        ({"intercept": float("nan")}, "finite"),
        ({"intercept": True}, "finite"),
        ({"coefficients": (float("inf"),)}, "finite"),
        ({"backend": (("python", ""),)}, "backend"),
        ({"backend": [["python", "x"]]}, "immutable"),
        ({"feature_names": ()}, "bounded"),
        ({"feature_names": ("x", "x")}, "bounded"),
        ({"feature_units": ()}, "bounded"),
        ({"feature_value_kinds": (FeatureValueKind.DISCRETE,) * 2}, "continuous"),
        ({"training_row_ids": ("duplicate",) * 8}, "bounded"),
        ({"training_population_id": ""}, "nonempty"),
        ({"feature_units": ("", None)}, "nonempty"),
        ({"preparation": "foreign"}, "mean state"),
        ({"coefficients": (0.0,)}, "mean state"),
        ({"neighbor_targets": (1.0,)}, "mean state"),
    ],
)
def test_invalid_mean_state_is_never_accepted(
    fitted_states: Callable[[str], tuple[FittedRegression, RegressionPopulation]],
    changes: dict[str, object],
    reason: str,
) -> None:
    """Reject wrong identities, nonfinite parameters and contradictory model shapes."""
    state, _ = fitted_states("mean")
    with pytest.raises((ValueError, TypeError), match=reason):
        cast("Callable[..., FittedRegression]", replace)(state, **changes)


@pytest.mark.parametrize("method", ["mean", "ridge", "knn-v2"])
def test_foreign_training_source_is_not_a_fitted_witness(
    fitted_states: Callable[[str], tuple[FittedRegression, RegressionPopulation]],
    method: str,
) -> None:
    """Preserve original rows, quantities and fitting identities at inspection."""
    state, training = fitted_states(method)
    changes = [
        replace(training, inputs=replace(training.inputs, source_identity="foreign")),
        replace(training, values=tuple(v + 1.0 for v in training.values)),
        replace(
            training,
            inputs=replace(
                training.inputs,
                row_ids=tuple(reversed(training.inputs.row_ids)),
            ),
        ),
        replace(training, target=replace(training.target, unit="foreign unit")),
    ]
    for foreign in changes:
        with pytest.raises(
            ValueError,
            match="original|training|target|source|correspondence",
        ):
            validate_training_state(state, foreign)


def test_distinct_fit_and_state_identities(
    fitted_states: Callable[[str], tuple[FittedRegression, RegressionPopulation]],
) -> None:
    """A fitted value identity cannot be its execution identity."""
    state, _ = fitted_states("mean")
    with pytest.raises(ValueError, match="separate state/fit"):
        replace(state, state_id=state.execution_id)
    assert replace(state, state_id=uuid4()).content_identity != state.content_identity


@pytest.mark.parametrize("method", ["ridge", "knn-v2"])
def test_preparation_belongs_to_the_original_training_population(
    fitted_states: Callable[[str], tuple[FittedRegression, RegressionPopulation]],
    method: str,
) -> None:
    """Refuse absent, foreign and mismatched preparation before prediction."""
    state, _ = fitted_states(method)
    assert state.preparation is not None
    for preparation in (
        None,
        replace(state.preparation, fitting_population_id="foreign"),
    ):
        with pytest.raises(ValueError, match="original-training preparation"):
            replace(state, preparation=preparation)


def test_neighbor_corpus_must_remain_complete(
    fitted_states: Callable[[str], tuple[FittedRegression, RegressionPopulation]],
) -> None:
    """Reject truncated, nonfinite or coefficient-composed neighbor states."""
    state, _ = fitted_states("knn-v2")
    assert state.neighbor_features is not None
    for changes in (
        {"neighbor_targets": None},
        {"neighbor_targets": (float("nan"),) * len(state.training_row_ids)},
        {"neighbor_features": None},
        {"coefficients": (1.0,)},
        {"intercept": 1.0},
        {
            "neighbor_features": FeatureTable(
                state.feature_names,
                state.neighbor_features.rows[:-1],
                state.feature_value_kinds,
            ),
        },
    ):
        with pytest.raises(ValueError, match="prepared neighbor corpus"):
            cast("Callable[..., FittedRegression]", replace)(state, **changes)
