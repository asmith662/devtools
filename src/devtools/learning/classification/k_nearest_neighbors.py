# Copyright (c) 2026
"""Domain semantics for k-nearest-neighbor classification."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from devtools.learning.classification.behavior import (
    ClassificationBehavior,
    _ClassificationImplementation,
    align_classification_features,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.targets import (
    CategoryValue,
    category_identity,
    validate_category_values,
)


class KNearestNeighborsDistance(Enum):
    """Distance geometry used to rank training observations."""

    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"


class KNearestNeighborsWeighting(Enum):
    """Contribution each of the selected neighbors makes to class voting."""

    UNIFORM = "uniform"
    INVERSE_DISTANCE = "inverse_distance"


@dataclass(frozen=True, slots=True)
class KNearestNeighborsClassificationSpecification:
    """Request kNN using explicit neighbor count, distance, and voting semantics."""

    neighbor_count: int
    distance: KNearestNeighborsDistance
    weighting: KNearestNeighborsWeighting

    def __post_init__(self) -> None:
        if type(self.neighbor_count) is not int or self.neighbor_count < 1:
            msg = "neighbor_count must be a positive integer"
            raise ValueError(msg)
        if not isinstance(self.distance, KNearestNeighborsDistance):
            msg = "distance must use KNearestNeighborsDistance"
            raise TypeError(msg)
        if not isinstance(self.weighting, KNearestNeighborsWeighting):
            msg = "weighting must use KNearestNeighborsWeighting"
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class FittedKNearestNeighborsClassification(ClassificationBehavior):
    """Reusable kNN state that classifies compatible numeric feature tables.

    The state retains its method specification, expected feature contract,
    category identity/order, and private Integration-owned neighbor state. The
    Integration retains the training observations because instance-based
    classification requires them at prediction time.
    """

    specification: KNearestNeighborsClassificationSpecification
    feature_names: tuple[str, ...]
    feature_value_kinds: tuple[FeatureValueKind, ...]
    categories: tuple[CategoryValue, ...]
    _implementation: _ClassificationImplementation = field(repr=False)

    def __post_init__(self) -> None:
        names = tuple(self.feature_names)
        kinds = tuple(self.feature_value_kinds)
        categories = validate_category_values(self.categories)
        if not isinstance(
            self.specification, KNearestNeighborsClassificationSpecification,
        ):
            msg = "specification must use KNearestNeighborsClassificationSpecification"
            raise TypeError(msg)
        if not names or any(
            not isinstance(name, str) or not name.strip() for name in names
        ):
            msg = "fitted feature identities must be non-empty"
            raise ValueError(msg)
        if len(set(names)) != len(names):
            msg = "fitted feature identities must be unique"
            raise ValueError(msg)
        if len(kinds) != len(names) or any(
            not isinstance(kind, FeatureValueKind) for kind in kinds
        ):
            msg = "each fitted feature must have one valid value kind"
            raise ValueError(msg)
        if len(categories) < 2:
            msg = "fitted classification state requires at least two classes"
            raise ValueError(msg)
        identities = tuple(category_identity(category) for category in categories)
        if len(set(identities)) != len(categories):
            msg = "fitted classification categories must be unique"
            raise ValueError(msg)
        object.__setattr__(self, "feature_names", names)
        object.__setattr__(self, "feature_value_kinds", kinds)
        object.__setattr__(self, "categories", categories)

    def classify(self, features: FeatureTable) -> tuple[CategoryValue, ...]:
        """Classify features only, aligning them without refitting or labels."""
        aligned_rows = align_classification_features(
            features, self.feature_names, self.feature_value_kinds,
        )
        if not aligned_rows:
            return ()
        category_indices = self._implementation.predict(aligned_rows)
        if len(category_indices) != len(aligned_rows):
            msg = "classification implementation returned an invalid row count"
            raise ValueError(msg)
        if any(
            type(index) is not int or not 0 <= index < len(self.categories)
            for index in category_indices
        ):
            msg = "classification implementation returned an invalid class"
            raise ValueError(msg)
        return tuple(self.categories[index] for index in category_indices)
