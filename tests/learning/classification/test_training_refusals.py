# Copyright (c) 2026
"""Feature admission, typed target failures and imported neighbor vote guards."""

from __future__ import annotations

from importlib import import_module
from typing import Any, cast

import pytest

from devtools.learning.classification._validation import (
    inspect_training,
    validate_training,
)
from devtools.learning.classification.behavior import align_classification_features
from devtools.learning.classification.k_nearest_neighbors import (
    KNearestNeighborsWeighting,
)
from devtools.learning.integrations.sklearn.k_nearest_neighbors import (
    _SklearnKNearestNeighborsImplementation,
    construct_k_nearest_neighbors_classification,
)
from devtools.learning.methods.features import (
    SQUARES,
    FeatureRecipe,
    transform_features,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind


def _features() -> FeatureTable:
    return FeatureTable(("x",), ((1.0,), (2.0,)), (FeatureValueKind.CONTINUOUS,))


@pytest.mark.parametrize("targets", [(None, 0), (float("nan"), 1), (0, 0), (0,)])
def test_invalid_original_targets_fail_training_before_native_construction(
    targets: tuple[object, ...],
) -> None:
    """Invalid observations and class/row disagreement are concrete refusals."""
    with pytest.raises((TypeError, ValueError)):
        validate_training(_features(), cast("Any", targets), label="control")


def test_feature_and_neighbor_population_refusals() -> None:
    """Unknown types, empty coordinates and excessive neighbor counts cannot fit."""
    with pytest.raises(TypeError, match="FeatureTable"):
        validate_training(cast("Any", None), (0, 1), label="control")
    with pytest.raises(ValueError, match="population"):
        validate_training(_features(), (0, 1), label="control", neighbor_count=3)
    assert inspect_training(_features(), (0, 1), label="control").codes == (0, 1)
    with pytest.raises(TypeError, match="FeatureTable"):
        align_classification_features(
            cast("Any", None),
            ("x",),
            (FeatureValueKind.CONTINUOUS,),
        )
    with pytest.raises(TypeError, match="typed original"):
        transform_features(
            cast("Any", None),
            FeatureRecipe("control", (SQUARES,)),
            maximum_dimension=4,
        )
    with pytest.raises(TypeError, match="specification"):
        construct_k_nearest_neighbors_classification(
            cast("Any", None),
            _features(),
            (0, 1),
        )


class _ReportedNeighbors:
    """Return explicit distance reports without fitting another selected method."""

    def __init__(self, distances: tuple[float, ...]) -> None:
        self.distances = distances

    def kneighbors(self, *_args: object, **_kwargs: object) -> tuple[object, object]:
        """Retain actual NumPy row representation for the imported vote kernel."""
        np = import_module("numpy")
        return np.asarray([self.distances]), np.asarray([[0, 1]])


@pytest.mark.parametrize("distances", [(0.0, 1.0), (1.0, 2.0), (float("inf"), 1.0)])
def test_imported_weighted_vote_arithmetic_and_invalid_native_distance(
    distances: tuple[float, ...],
) -> None:
    """Qualify the retained kernel, without adding investigator menu entries."""
    model = _SklearnKNearestNeighborsImplementation(
        _ReportedNeighbors(distances),
        (0, 1),
        2,
        2,
        KNearestNeighborsWeighting.INVERSE_DISTANCE,
    )
    if float("inf") in distances:
        with pytest.raises(ValueError, match="non-finite"):
            model.predict(((1.0,),))
    else:
        assert model.predict(((1.0,),)) == (0,)
