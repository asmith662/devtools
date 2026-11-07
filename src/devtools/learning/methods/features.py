# Copyright (c) 2026
"""Retained feature-recipe identity and the selected SQUARE implementation."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass

from devtools.learning.measurement.contracts import nonempty
from devtools.learning.representation.features import FeatureTable, FeatureValueKind


def _hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode(),
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class FeatureOperator:
    """Reviewed definition metadata; possession does not load or execute code."""

    name: str
    version: int
    order: int
    input_semantics: str
    output_semantics: str
    incompatible_with: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        for v in (self.name, self.input_semantics, self.output_semantics):
            nonempty(v)
        if type(self.version) is not int or self.version < 1:
            msg = "positive operator version required"
            raise ValueError(msg)
        if type(self.order) is not int or self.order < 0:
            msg = "nonnegative canonical order required"
            raise ValueError(msg)
        if type(self.incompatible_with) is not tuple or len(
            set(self.incompatible_with),
        ) != len(self.incompatible_with):
            msg = "immutable unique incompatibility identities required"
            raise ValueError(msg)
        for name in self.incompatible_with:
            nonempty(name)

    @property
    def identity(self) -> str:
        """Apply the explicit identity contract within this owner."""
        return f"{self.name}_v{self.version}"


ORIGINAL_CONTINUOUS = "original_prepared_continuous_coordinates_v1"
SQUARES = FeatureOperator(
    "append_squared_features",
    1,
    0,
    ORIGINAL_CONTINUOUS,
    "append original x_i*x_i in original index order",
)


@dataclass(frozen=True, slots=True)
class FeatureRecipe:
    """Canonical nonempty operator subset with an explicit originating catalog."""

    catalog_identity: str
    operators: tuple[FeatureOperator, ...]
    construction_rule: str = "nonempty-compatible-subsets-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.catalog_identity)
        if self.construction_rule != "nonempty-compatible-subsets-v1":
            msg = "unsupported construction rule"
            raise ValueError(msg)
        if type(self.operators) is not tuple or not self.operators:
            msg = "immutable nonempty recipe required"
            raise ValueError(msg)
        if any(not isinstance(o, FeatureOperator) for o in self.operators):
            msg = "typed operator definitions required"
            raise TypeError(msg)
        if len({o.identity for o in self.operators}) != len(self.operators):
            msg = "duplicate operator"
            raise ValueError(msg)
        if (
            tuple(sorted(self.operators, key=lambda o: (o.order, o.identity)))
            != self.operators
        ):
            msg = "noncanonical operator order"
            raise ValueError(msg)
        if any(o.input_semantics != ORIGINAL_CONTINUOUS for o in self.operators):
            msg = "incompatible original-coordinate inputs"
            raise ValueError(msg)
        if any(
            p.identity in o.incompatible_with
            for o in self.operators
            for p in self.operators
        ):
            msg = "incompatible operator subset"
            raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return _hash(asdict(self))

    @property
    def identity(self) -> str:
        """Apply the explicit identity contract within this owner."""
        return "feature-recipe-v1:" + self.content_identity


def transform_features(
    original: FeatureTable,
    recipe: FeatureRecipe,
    *,
    maximum_dimension: int,
) -> FeatureTable:
    """Append only reviewed maps of ORIGINAL coordinates; never recurse.

    Neither arbitrary callables nor unknown operator definitions are executable.
    Resource bounds are supplied by the caller's authorized experiment.
    """
    if not isinstance(original, FeatureTable) or not isinstance(recipe, FeatureRecipe):
        msg = "typed original features and recipe required"
        raise TypeError(msg)
    if type(maximum_dimension) is not int or maximum_dimension < 1:
        msg = "positive dimension budget required"
        raise ValueError(msg)
    if not original.feature_names or any(
        k is not FeatureValueKind.CONTINUOUS for k in original.feature_value_kinds
    ):
        msg = "nonempty original continuous schema required"
        raise ValueError(msg)
    names = list(original.feature_names)
    pairs: list[tuple[int, int]] = []
    for operator in recipe.operators:
        if operator == SQUARES:
            added = [(i, i) for i in range(len(original.feature_names))]
        else:
            msg = "operator has no approved executable implementation"
            raise ValueError(msg)
        pairs.extend(added)
        names.extend(
            (
                f"{operator.identity}[{i},{j}]:{original.feature_names[i]}*{original.feature_names[j]}"
                for i, j in added
            ),
        )
    if len(names) > maximum_dimension or len(set(names)) != len(names):
        msg = "expanded dimension/coordinate identities exceed compatibility"
        raise ValueError(msg)
    rows = tuple(
        tuple(row) + tuple((row[i] * row[j] for i, j in pairs)) for row in original.rows
    )
    if any(not math.isfinite(v) for row in rows for v in row):
        msg = "nonfinite transformed coordinate"
        raise ValueError(msg)
    return FeatureTable(tuple(names), rows, (FeatureValueKind.CONTINUOUS,) * len(names))
