# Copyright (c) 2026
"""Deterministic evidence from categorical truth and predictions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.learning.representation.targets import (
    CategoryValue,
    category_identity,
    validate_category_values,
)

if TYPE_CHECKING:
    from collections.abc import Iterable


@dataclass(frozen=True, slots=True)
class ClassificationConfusionMatrix:
    """Immutable confusion counts in explicit category order.

    Rows represent actual categories and columns represent predicted
    categories. ``counts[i][j]`` is therefore the number of observations whose
    actual category is ``categories[i]`` and whose predicted category is
    ``categories[j]``.
    """

    categories: tuple[CategoryValue, ...]
    counts: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        """Validate immutable numerical correspondence."""
        categories = validate_category_values(self.categories)
        counts = tuple(tuple(row) for row in self.counts)
        if not categories:
            msg = "confusion matrix must contain at least one category"
            raise ValueError(msg)
        identities = tuple(category_identity(value) for value in categories)
        if len(set(identities)) != len(identities):
            msg = "confusion matrix categories must be unique"
            raise ValueError(msg)
        if len(counts) != len(categories) or any(
            len(row) != len(categories) for row in counts
        ):
            msg = "confusion matrix counts must be square by category"
            raise ValueError(msg)
        if any(type(count) is not int or count < 0 for row in counts for count in row):
            msg = "confusion counts must be non-negative integers"
            raise ValueError(msg)
        object.__setattr__(self, "categories", categories)
        object.__setattr__(self, "counts", counts)

    def count(
        self,
        actual_category: CategoryValue,
        predicted_category: CategoryValue,
    ) -> int:
        """Return the count for a typed actual/predicted category pair."""
        identities = tuple(category_identity(value) for value in self.categories)
        try:
            actual_index = identities.index(category_identity(actual_category))
            predicted_index = identities.index(category_identity(predicted_category))
        except ValueError as error:
            msg = "category is not represented in this confusion matrix"
            raise KeyError(
                msg,
            ) from error
        return self.counts[actual_index][predicted_index]


@dataclass(frozen=True, slots=True)
class PerCategoryEvaluation:
    """Counts and derived classification measures for one category."""

    category: CategoryValue
    support: int
    predicted_count: int
    true_positive_count: int

    def __post_init__(self) -> None:
        """Validate immutable numerical correspondence."""
        category = validate_category_values((self.category,))[0]
        counts = (self.support, self.predicted_count, self.true_positive_count)
        if any(type(count) is not int or count < 0 for count in counts):
            msg = "per-category counts must be non-negative integers"
            raise ValueError(msg)
        if self.true_positive_count > min(self.support, self.predicted_count):
            msg = "true positives cannot exceed support or predictions"
            raise ValueError(msg)
        object.__setattr__(self, "category", category)

    @property
    def precision(self) -> float | None:
        """True positives divided by predicted count, or None if absent."""
        if self.predicted_count == 0:
            return None
        return self.true_positive_count / self.predicted_count

    @property
    def recall(self) -> float | None:
        """True positives divided by actual support, or None if absent."""
        if self.support == 0:
            return None
        return self.true_positive_count / self.support

    @property
    def f1(self) -> float | None:
        """Harmonic precision/recall, undefined when its ratio is undefined.

        If both ratios are defined but are zero, their harmonic mean is also
        undefined and is represented as ``None`` rather than an invented zero.
        """
        precision = self.precision
        recall = self.recall
        if precision is None or recall is None or precision + recall == 0:
            return None
        return 2 * precision * recall / (precision + recall)


@dataclass(frozen=True, slots=True)
class ClassificationEvaluation:
    """Immutable, prediction-only classification evaluation evidence."""

    observation_count: int
    correct_count: int
    confusion_matrix: ClassificationConfusionMatrix
    per_category: tuple[PerCategoryEvaluation, ...]

    def __post_init__(self) -> None:
        """Validate immutable numerical correspondence."""
        if type(self.observation_count) is not int or self.observation_count < 1:
            msg = "observation_count must be a positive integer"
            raise ValueError(msg)
        if type(self.correct_count) is not int or not (
            0 <= self.correct_count <= self.observation_count
        ):
            msg = "correct_count must be within the evaluated population"
            raise ValueError(msg)
        if not isinstance(self.confusion_matrix, ClassificationConfusionMatrix):
            msg = "confusion_matrix must use ClassificationConfusionMatrix"
            raise TypeError(msg)

        per_category = tuple(self.per_category)
        categories = self.confusion_matrix.categories
        counts = self.confusion_matrix.counts
        if len(per_category) != len(categories) or any(
            not isinstance(item, PerCategoryEvaluation) for item in per_category
        ):
            msg = "one per-category result is required per matrix category"
            raise ValueError(msg)
        if tuple(category_identity(item.category) for item in per_category) != tuple(
            category_identity(category) for category in categories
        ):
            msg = "per-category results must follow matrix category order"
            raise ValueError(msg)
        if sum(sum(row) for row in counts) != self.observation_count:
            msg = "confusion counts must equal observation_count"
            raise ValueError(msg)
        if sum(counts[index][index] for index in range(len(categories))) != (
            self.correct_count
        ):
            msg = "diagonal confusion counts must equal correct_count"
            raise ValueError(msg)
        for index, result in enumerate(per_category):
            support = sum(counts[index])
            predicted_count = sum(row[index] for row in counts)
            true_positive_count = counts[index][index]
            if (result.support, result.predicted_count, result.true_positive_count) != (
                support,
                predicted_count,
                true_positive_count,
            ):
                msg = "per-category counts must agree with confusion matrix"
                raise ValueError(msg)
        object.__setattr__(self, "per_category", per_category)

    @property
    def categories(self) -> tuple[CategoryValue, ...]:
        """Return category order shared by the matrix and per-category evidence."""
        return self.confusion_matrix.categories

    @property
    def accuracy(self) -> float:
        """Return correct classifications divided by evaluated observations."""
        return self.correct_count / self.observation_count

    @property
    def macro_precision(self) -> float | None:
        """Mean category precision; undefined if any category precision is."""
        return _defined_macro(tuple(result.precision for result in self.per_category))

    @property
    def macro_recall(self) -> float | None:
        """Mean category recall; undefined if any category recall is."""
        return _defined_macro(tuple(result.recall for result in self.per_category))

    @property
    def macro_f1(self) -> float | None:
        """Mean category F1; undefined if any category F1 is."""
        return _defined_macro(tuple(result.f1 for result in self.per_category))


def evaluate_classification(
    truth: Iterable[CategoryValue],
    predictions: Iterable[CategoryValue],
) -> ClassificationEvaluation:
    """Evaluate already-produced categorical predictions against categorical truth.

    This operation consumes neither a classifier nor empirical features and
    performs no fitting. Its evidence is legitimately described as held-out
    only when upstream population-role handling authorized both input
    sequences as held-out observations.
    """
    actual = validate_category_values(tuple(truth))
    predicted = validate_category_values(tuple(predictions))
    if len(actual) != len(predicted):
        msg = "truth and prediction observation counts must match"
        raise ValueError(msg)
    if not actual:
        msg = "classification evaluation requires observations"
        raise ValueError(msg)

    category_by_identity = {
        category_identity(value): value for value in (*actual, *predicted)
    }
    categories = tuple(sorted(category_by_identity.values(), key=_category_sort_key))
    position_by_identity = {
        category_identity(value): index for index, value in enumerate(categories)
    }
    counts = [[0 for _ in categories] for _ in categories]
    correct_count = 0
    for actual_value, predicted_value in zip(actual, predicted, strict=True):
        actual_index = position_by_identity[category_identity(actual_value)]
        predicted_index = position_by_identity[category_identity(predicted_value)]
        counts[actual_index][predicted_index] += 1
        correct_count += actual_index == predicted_index

    immutable_counts = tuple(tuple(row) for row in counts)
    matrix = ClassificationConfusionMatrix(categories, immutable_counts)
    per_category = tuple(
        PerCategoryEvaluation(
            category=category,
            support=sum(immutable_counts[index]),
            predicted_count=sum(row[index] for row in immutable_counts),
            true_positive_count=immutable_counts[index][index],
        )
        for index, category in enumerate(categories)
    )
    return ClassificationEvaluation(
        observation_count=len(actual),
        correct_count=correct_count,
        confusion_matrix=matrix,
        per_category=per_category,
    )


def _category_sort_key(
    category: CategoryValue,
) -> tuple[int, str | int | float | bool]:
    """Sort by explicit scalar type family, then within-family value order."""
    if type(category) is str:
        return 0, category
    if type(category) is int:
        return 1, category
    if type(category) is float:
        return 2, category
    return 3, category


def _defined_macro(values: tuple[float | None, ...]) -> float | None:
    """Average all categories, leaving the aggregate undefined if any is."""
    if any(value is None for value in values):
        return None
    return sum(value for value in values if value is not None) / len(values)
