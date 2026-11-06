# Copyright (c) 2026
"""Domain semantics for Decision Tree classification."""

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


class DecisionTreeCriterion(Enum):
    """Impurity measure used to choose Decision Tree splits."""

    GINI = "gini"
    ENTROPY = "entropy"


@dataclass(frozen=True, slots=True)
class DecisionTreeClassificationSpecification:
    """Request Decision Tree construction with method-relevant constraints.

    The split criterion and maximum depth affect the learned classification
    behavior. Other first-slice backend settings remain fixed by the
    scikit-learn Integration rather than mirroring its full constructor API.
    """

    criterion: DecisionTreeCriterion = DecisionTreeCriterion.GINI
    maximum_depth: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.criterion, DecisionTreeCriterion):
            msg = "criterion must use DecisionTreeCriterion"
            raise TypeError(msg)
        if self.maximum_depth is not None and (
            type(self.maximum_depth) is not int or self.maximum_depth < 1
        ):
            msg = "maximum_depth must be a positive integer or None"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class FittedDecisionTreeClassification(ClassificationBehavior):
    """Reusable fitted classification state and its classification behavior.

    The state retains the expected feature identities and meanings, original
    categorical values in first-observed order, the construction request, and
    an opaque method-specific runtime implementation. It does not retain the
    supplied training feature or target observations.
    """

    specification: DecisionTreeClassificationSpecification
    feature_names: tuple[str, ...]
    feature_value_kinds: tuple[FeatureValueKind, ...]
    categories: tuple[CategoryValue, ...]
    _implementation: _ClassificationImplementation = field(repr=False)

    def __post_init__(self) -> None:
        feature_names = tuple(self.feature_names)
        feature_value_kinds = tuple(self.feature_value_kinds)
        categories = validate_category_values(self.categories)
        if not isinstance(self.specification, DecisionTreeClassificationSpecification):
            msg = "specification must use DecisionTreeClassificationSpecification"
            raise TypeError(msg)
        if not feature_names or any(
            not isinstance(name, str) or not name.strip() for name in feature_names
        ):
            msg = "fitted feature identities must be non-empty"
            raise ValueError(msg)
        if len(set(feature_names)) != len(feature_names):
            msg = "fitted feature identities must be unique"
            raise ValueError(msg)
        if len(feature_value_kinds) != len(feature_names):
            msg = "each fitted feature must have one value kind"
            raise ValueError(msg)
        if any(not isinstance(kind, FeatureValueKind) for kind in feature_value_kinds):
            msg = "fitted feature meanings must use FeatureValueKind"
            raise TypeError(msg)
        if len(categories) < 2:
            msg = "fitted classification state requires at least two classes"
            raise ValueError(msg)
        if len({category_identity(category) for category in categories}) != len(
            categories,
        ):
            msg = "fitted classification categories must be unique"
            raise ValueError(msg)
        object.__setattr__(self, "feature_names", feature_names)
        object.__setattr__(self, "feature_value_kinds", feature_value_kinds)
        object.__setattr__(self, "categories", categories)

    def classify(self, features: FeatureTable) -> tuple[CategoryValue, ...]:
        """Classify compatible observations without target values or refitting.

        Columns are aligned by fitted identity. Extra columns are ignored;
        missing selected columns and changed continuous/discrete meanings are
        rejected. Empty compatible populations produce no predictions.
        """
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
