# Copyright (c) 2026
"""Identified numeric feature observations and their declared semantics."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import SupportsFloat


class FeatureValueKind(Enum):
    """Interpretation assigned to a feature independently of its numeric dtype."""

    CONTINUOUS = "continuous"
    DISCRETE = "discrete"


@dataclass(frozen=True, slots=True)
class FeatureTable:
    """Numeric feature observations with stable local identities and semantics.

    Rows are observations; ``feature_names`` and ``feature_value_kinds``
    describe each column in the same order. Numeric values are stored as
    finite floats. Feature names must be unique within a table.
    """

    feature_names: tuple[str, ...]
    rows: tuple[tuple[float, ...], ...]
    feature_value_kinds: tuple[FeatureValueKind, ...]

    def __post_init__(self) -> None:
        """Validate immutable numerical correspondence."""
        feature_names = tuple(self.feature_names)
        feature_value_kinds = tuple(self.feature_value_kinds)
        if any(not isinstance(name, str) or not name.strip() for name in feature_names):
            msg = "feature names must be non-empty strings"
            raise ValueError(msg)
        if len(set(feature_names)) != len(feature_names):
            msg = "feature identities must be unique"
            raise ValueError(msg)
        if len(feature_value_kinds) != len(feature_names):
            msg = "each feature must have one value kind"
            raise ValueError(msg)
        if any(not isinstance(kind, FeatureValueKind) for kind in feature_value_kinds):
            msg = "feature value kinds must use FeatureValueKind"
            raise TypeError(msg)

        rows = tuple(
            tuple(_finite_numeric_value(value) for value in row) for row in self.rows
        )
        if any(len(row) != len(feature_names) for row in rows):
            msg = "each observation must have one value per feature"
            raise ValueError(msg)

        object.__setattr__(self, "feature_names", feature_names)
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "feature_value_kinds", feature_value_kinds)

    @property
    def observation_count(self) -> int:
        """Number of rows represented by this table."""
        return len(self.rows)


def _finite_numeric_value(value: SupportsFloat) -> float:
    if isinstance(value, (bool, str, bytes, bytearray)):
        msg = "feature observations must be numeric values, not text or bool"
        raise TypeError(msg)
    try:
        numeric_value = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        msg = "feature observations must be numeric values"
        raise TypeError(msg) from error
    if not math.isfinite(numeric_value):
        msg = "feature observations must be finite"
        raise ValueError(msg)
    return numeric_value
