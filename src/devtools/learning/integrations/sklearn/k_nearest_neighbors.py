# mypy: disable-error-code="import-untyped"
# Copyright (c) 2026
"""scikit-learn Integration for k-nearest-neighbor classification."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TYPE_CHECKING

import numpy as np
from sklearn.neighbors import NearestNeighbors

from devtools.learning.classification._validation import validate_training
from devtools.learning.classification.behavior import _ClassificationImplementation
from devtools.learning.classification.k_nearest_neighbors import (
    FittedKNearestNeighborsClassification,
    KNearestNeighborsClassificationSpecification,
    KNearestNeighborsWeighting,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from devtools.learning.representation.features import FeatureTable
    from devtools.learning.representation.targets import CategoryValue


@dataclass(frozen=True, slots=True)
class _SklearnKNearestNeighborsImplementation(_ClassificationImplementation):
    """Retain backend neighbors and apply stable domain vote tie semantics."""

    neighbors: NearestNeighbors
    training_category_codes: tuple[int, ...]
    category_count: int
    neighbor_count: int
    weighting: KNearestNeighborsWeighting

    def predict(self, rows: tuple[tuple[float, ...], ...]) -> tuple[int, ...]:
        distances, indices = self.neighbors.kneighbors(
            np.asarray(rows, dtype=np.float64),
            n_neighbors=len(self.training_category_codes),
            return_distance=True,
        )
        predictions: list[int] = []
        for row_distances, row_indices in zip(distances, indices, strict=True):
            ordered_neighbors = sorted(
                (
                    (float(distance), int(index))
                    for distance, index in zip(row_distances, row_indices, strict=True)
                ),
                key=lambda neighbor: (neighbor[0], neighbor[1]),
            )[: self.neighbor_count]
            if any((not isfinite(distance) for distance, _ in ordered_neighbors)):
                msg = "kNN Integration returned a non-finite distance"
                raise ValueError(msg)
            zero_distance_neighbors = tuple(
                (index for distance, index in ordered_neighbors if distance == 0.0),
            )
            votes = [0.0] * self.category_count
            if self.weighting is KNearestNeighborsWeighting.UNIFORM:
                for _, index in ordered_neighbors:
                    votes[self.training_category_codes[index]] += 1.0
            elif zero_distance_neighbors:
                for index in zero_distance_neighbors:
                    votes[self.training_category_codes[index]] += 1.0
            else:
                for distance, index in ordered_neighbors:
                    votes[self.training_category_codes[index]] += 1.0 / distance
            predictions.append(
                max(range(self.category_count), key=lambda code: (votes[code], -code)),
            )
        return tuple(predictions)


def construct_k_nearest_neighbors_classification(
    specification: KNearestNeighborsClassificationSpecification,
    training_features: FeatureTable,
    training_targets: Iterable[CategoryValue],
) -> FittedKNearestNeighborsClassification:
    """Construct kNN state from one aligned, already-represented training set."""
    if not isinstance(specification, KNearestNeighborsClassificationSpecification):
        msg = "specification must use KNearestNeighborsClassificationSpecification"
        raise TypeError(msg)
    checked = validate_training(
        training_features,
        training_targets,
        label="kNN construction",
        neighbor_count=specification.neighbor_count,
    )
    targets = checked.targets
    categories = checked.categories
    encoded_targets = checked.codes
    neighbors = NearestNeighbors(
        n_neighbors=len(targets),
        algorithm="brute",
        metric=specification.distance.value,
        n_jobs=1,
    )
    neighbors.fit(np.asarray(training_features.rows, dtype=np.float64))
    implementation = _SklearnKNearestNeighborsImplementation(
        neighbors=neighbors,
        training_category_codes=tuple(encoded_targets),
        category_count=len(categories),
        neighbor_count=specification.neighbor_count,
        weighting=specification.weighting,
    )
    return FittedKNearestNeighborsClassification(
        specification=specification,
        feature_names=training_features.feature_names,
        feature_value_kinds=training_features.feature_value_kinds,
        categories=tuple(categories),
        _implementation=implementation,
    )
