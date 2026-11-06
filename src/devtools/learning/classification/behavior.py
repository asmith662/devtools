# Copyright (c) 2026
"""Method-neutral classification behavior shared by fitted classifiers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from devtools.learning.representation.features import FeatureTable, FeatureValueKind

if TYPE_CHECKING:
    from devtools.learning.representation.targets import CategoryValue


class ClassificationBehavior(Protocol):
    """Common feature-only behavior exposed by fitted classifiers."""

    def classify(self, features: FeatureTable) -> tuple[CategoryValue, ...]:
        """Classify compatible observations without target values or refitting."""


class _ClassificationImplementation(Protocol):
    """Narrow runtime contract implemented by backend-owned fitted state."""

    def predict(self, rows: tuple[tuple[float, ...], ...]) -> tuple[int, ...]:
        """Return encoded category indices for rows in fitted feature order."""


def align_classification_features(
    features: FeatureTable,
    expected_names: tuple[str, ...],
    expected_kinds: tuple[FeatureValueKind, ...],
) -> tuple[tuple[float, ...], ...]:
    """Validate and align inputs under the common fitted feature contract."""
    if not isinstance(features, FeatureTable):
        msg = "features must use FeatureTable"
        raise TypeError(msg)
    positions = {name: index for index, name in enumerate(features.feature_names)}
    missing = tuple(name for name in expected_names if name not in positions)
    if missing:
        msg = f"classification input is missing features: {missing!r}"
        raise ValueError(msg)
    fitted_positions: list[int] = []
    for name, expected_kind in zip(expected_names, expected_kinds, strict=True):
        position = positions[name]
        if features.feature_value_kinds[position] is not expected_kind:
            msg = f"feature {name!r} has a representation-semantic mismatch"
            raise ValueError(msg)
        fitted_positions.append(position)
    return tuple(
        tuple(row[position] for position in fitted_positions) for row in features.rows
    )
