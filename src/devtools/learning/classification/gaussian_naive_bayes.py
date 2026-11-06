# Copyright (c) 2026

"""Domain semantics for Gaussian Naïve Bayes classification."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

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


@dataclass(frozen=True, slots=True)
class GaussianNaiveBayesClassificationSpecification:
    """Request Gaussian classification with an explicit variance-smoothing scale."""

    variance_smoothing: float = 1e-09

    def __post_init__(self) -> None:

        if isinstance(self.variance_smoothing, bool) or not isinstance(
            self.variance_smoothing,
            (int, float),
        ):
            msg = "variance_smoothing must be numeric"
            raise TypeError(msg)

        if (
            not math.isfinite(float(self.variance_smoothing))
            or self.variance_smoothing <= 0
        ):
            msg = "variance_smoothing must be finite and positive"
            raise ValueError(msg)

        object.__setattr__(self, "variance_smoothing", float(self.variance_smoothing))


@dataclass(frozen=True, slots=True)
class FittedGaussianNaiveBayesClassification(ClassificationBehavior):
    """Reusable Gaussian state for compatible continuous-feature observations."""

    specification: GaussianNaiveBayesClassificationSpecification

    feature_names: tuple[str, ...]

    feature_value_kinds: tuple[FeatureValueKind, ...]

    categories: tuple[CategoryValue, ...]

    _implementation: _ClassificationImplementation = field(repr=False)

    def __post_init__(self) -> None:

        names = tuple(self.feature_names)

        kinds = tuple(self.feature_value_kinds)

        categories = validate_category_values(self.categories)

        if not isinstance(
            self.specification,
            GaussianNaiveBayesClassificationSpecification,
        ):
            msg = "specification must use GaussianNaiveBayesClassificationSpecification"
            raise TypeError(
                msg,
            )

        if not names or any(
            not isinstance(name, str) or not name.strip() for name in names
        ):
            msg = "fitted feature identities must be non-empty"
            raise ValueError(msg)

        if len(set(names)) != len(names):
            msg = "fitted feature identities must be unique"
            raise ValueError(msg)

        if len(kinds) != len(names) or any(
            kind is not FeatureValueKind.CONTINUOUS for kind in kinds
        ):
            msg = "Gaussian Naïve Bayes requires continuous features"
            raise ValueError(msg)

        if len(categories) < 2:
            msg = "fitted classification state requires at least two classes"
            raise ValueError(
                msg,
            )

        if len({category_identity(category) for category in categories}) != len(
            categories,
        ):
            msg = "fitted classification categories must be unique"
            raise ValueError(msg)

        object.__setattr__(self, "feature_names", names)

        object.__setattr__(self, "feature_value_kinds", kinds)

        object.__setattr__(self, "categories", categories)

    def classify(self, features: FeatureTable) -> tuple[CategoryValue, ...]:
        """Classify compatible continuous features without labels or refitting."""
        aligned_rows = align_classification_features(
            features,
            self.feature_names,
            self.feature_value_kinds,
        )

        if not aligned_rows:
            return ()

        category_indices = self._implementation.predict(aligned_rows)

        if len(category_indices) != len(aligned_rows):
            msg = "classification implementation returned an invalid row count"
            raise ValueError(
                msg,
            )

        if any(
            type(index) is not int or not 0 <= index < len(self.categories)
            for index in category_indices
        ):
            msg = "classification implementation returned an invalid class"
            raise ValueError(msg)

        return tuple(self.categories[index] for index in category_indices)
