# Copyright (c) 2026
"""Real retained prediction arithmetic and explicitly forged-state refusal controls."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.learning.regression.contracts import RegressionRole
from devtools.learning.regression.state import (
    FittedRegression,
    RegressionPredictions,
    validate_training_preparation,
    validate_training_state,
)
from devtools.learning.representation.features import FeatureTable
from devtools.learning.representation.observations import PopulationScope

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.learning.regression.contracts import (
        RegressionInput,
        RegressionPopulation,
    )

type Witnesses = Callable[[str], tuple[FittedRegression, RegressionPopulation]]


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("state_id", "foreign"),
        ("target", None),
        ("row_ids", []),
        ("row_ids", ("duplicate",) * 8),
        ("values", []),
        ("values", (float("nan"),) * 8),
        ("neighbor_row_ids", ()),
        ("neighbor_row_ids", []),
        ("neighbor_row_ids", ((),) * 8),
        ("neighbor_distances", ((-1.0,) * 5,) * 8),
    ],
)
def test_predicted_values_cannot_lose_source_or_neighbor_correspondence(
    fitted_states: Witnesses,
    field: str,
    bad: object,
) -> None:
    """Retain original row count, scalar types and five-neighbor witnesses."""
    state, training = fitted_states("knn-v2")
    prediction = state.predict(training.inputs)
    reconstruct = cast("Callable[..., RegressionPredictions]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(prediction, **{field: bad})
    assert prediction.content_identity.startswith("regression-predictions-v2:")


def test_prediction_neighbor_pair_and_capacity_are_explicit(
    fitted_states: Witnesses,
) -> None:
    """A complete payload cannot omit one witness half or exceed capacity."""
    state, training = fitted_states("knn-v2")
    prediction = state.predict(training.inputs)
    with pytest.raises(ValueError, match="remain paired"):
        replace(prediction, neighbor_distances=None)
    too_many = 2049
    with pytest.raises(ValueError, match="bounded complete prediction population"):
        replace(
            prediction,
            row_ids=tuple("q" + str(i) for i in range(too_many)),
            values=(0.0,) * too_many,
        )


def test_inference_refuses_wrong_types_units_and_unrepresentable_sums(
    fitted_states: Witnesses,
) -> None:
    """The retained predictor needs no labels, and errors never become finite output."""
    state, training = fitted_states("ridge")
    with pytest.raises(ValueError, match="typed original prediction"):
        state.predict(cast("RegressionInput", None))
    with pytest.raises(ValueError, match="ordered feature schema/units"):
        state.predict(replace(training.inputs, feature_units=("foreign", None)))
    assert state.preparation is not None
    row = tuple(
        m + s
        for m, s in zip(
            state.preparation.training_means,
            state.preparation.effective_scales,
            strict=True,
        )
    )
    query = replace(
        training.inputs,
        features=replace(training.inputs.features, rows=(row,)),
        row_ids=("overflow-query",),
        role=RegressionRole.DEVELOPMENT,
    )
    corrupt = replace(state, coefficients=(1e308,) * len(row), intercept=0.0)
    with pytest.raises(ValueError, match="unrepresentable regression prediction"):
        corrupt.predict(query)


@pytest.mark.parametrize("method", ["ridge", "knn-v2"])
def test_training_reinspection_recomputes_original_statistics_and_parameters(
    fitted_states: Witnesses,
    method: str,
) -> None:
    """A new hash cannot make forged preparation or fitted parameters original."""
    state, training = fitted_states(method)
    assert state.preparation is not None
    preparation = state.preparation
    with pytest.raises(ValueError, match="training-only preparation population/schema"):
        validate_training_preparation(
            replace(preparation, fitting_population_id="foreign"),
            training,
        )
    with pytest.raises(ValueError, match="standardization arithmetic"):
        validate_training_preparation(
            replace(
                preparation,
                training_means=tuple(m + 1 for m in preparation.training_means),
            ),
            training,
        )
    if method == "ridge":
        with pytest.raises(ValueError, match="normal-equation residual"):
            validate_training_state(
                replace(state, intercept=state.intercept + 1),
                training,
            )
        with pytest.raises(ValueError, match="not a neighbor model"):
            replace(state, neighbor_targets=(1.0,) * len(state.training_row_ids))
    else:
        assert state.neighbor_features is not None
        corrupt = replace(
            state.neighbor_features,
            rows=tuple(
                tuple(v + 1 for v in row) for row in state.neighbor_features.rows
            ),
        )
        with pytest.raises(ValueError, match="source-bound neighbor corpus"):
            validate_training_state(replace(state, neighbor_features=corrupt), training)
    assert preparation.fitting_scope is PopulationScope.TRAINING


def test_forged_declared_shape_cannot_start_excessive_prediction_work(
    fitted_states: Witnesses,
) -> None:
    """Refuse work on a forged large corpus before distance materialization.

    No fit or accepted source is claimed for the copied shape. Independent
    source validation also rejects it against the genuine original witness.
    """
    state, training = fitted_states("knn-v2")
    assert state.preparation is not None
    assert state.neighbor_features is not None
    assert state.neighbor_targets is not None
    count = 2048
    corpus = replace(
        state.neighbor_features,
        rows=tuple(
            state.neighbor_features.rows[i % len(state.training_row_ids)]
            for i in range(count)
        ),
    )
    forged = replace(
        state,
        training_row_ids=tuple("forged-" + str(i) for i in range(count)),
        preparation=replace(state.preparation, fitting_observation_count=count),
        neighbor_features=corpus,
        neighbor_targets=tuple(
            state.neighbor_targets[i % len(state.training_row_ids)]
            for i in range(count)
        ),
    )
    with pytest.raises(ValueError, match="original"):
        validate_training_state(forged, training)
    query = replace(
        training.inputs,
        row_ids=tuple("q" + str(i) for i in range(count)),
        features=replace(
            training.inputs.features,
            rows=(training.inputs.features.rows[0],) * count,
        ),
        role=RegressionRole.DEVELOPMENT,
    )
    with pytest.raises(ValueError, match="work bound exceeded before materialization"):
        forged.predict(query)


def test_oversized_neighbor_identity_payload_refuses_before_materialization(
    fitted_states: Witnesses,
) -> None:
    """Retained shape limits do not permit an oversized complete prediction payload."""
    state, training = fitted_states("knn-v2")
    forged = replace(
        state,
        training_row_ids=tuple(
            "x" * 3000 + str(i) for i in range(len(state.training_row_ids))
        ),
    )
    count = 128
    query = replace(
        training.inputs,
        row_ids=tuple("q" + str(i) for i in range(count)),
        features=FeatureTable(
            training.inputs.features.feature_names,
            (training.inputs.features.rows[0],) * count,
            training.inputs.features.feature_value_kinds,
        ),
        role=RegressionRole.DEVELOPMENT,
    )
    with pytest.raises(ValueError, match="bounded complete prediction payload"):
        forged.predict(query)
