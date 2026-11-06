# Copyright (c) 2026
"""Explicit source declarations; numerical storage alone cannot establish a target."""

import math
from dataclasses import asdict, dataclass
from enum import Enum

from devtools.learning.identity import source_fingerprint as fingerprint
from devtools.learning.measurement.contracts import nonempty
from devtools.learning.regression.limits import (
    REGRESSION_V2,
    check_text,
    version_limits,
)
from devtools.learning.representation.features import FeatureTable
from devtools.learning.representation.observations import PopulationScope


class RegressionRole(Enum):
    """Retain the declared RegressionRole scientific values and invariants."""

    TRAINING = "training"
    DEVELOPMENT = "development"
    CONFIRMATION = "confirmation"

    @property
    def scope(self) -> PopulationScope:
        """Apply the explicit scope contract within this owner."""
        return {
            RegressionRole.TRAINING: PopulationScope.TRAINING,
            RegressionRole.DEVELOPMENT: PopulationScope.VALIDATION,
            RegressionRole.CONFIRMATION: PopulationScope.TEST,
        }[self]


@dataclass(frozen=True, slots=True)
class ContinuousTarget:
    """Caller-declared scalar quantity, never inferred from class encodings.

    None is an explicitly unknown source unit. No conversion is inferred. A false
    source declaration cannot be detected from a numerical vector alone.
    """

    identity: str
    quantity: str
    unit: str | None
    kind: str = "continuous_scalar"
    version: str = "continuous-target-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.identity)
        nonempty(self.quantity)
        if self.unit is not None:
            nonempty(self.unit)
        if (self.kind, self.version) != ("continuous_scalar", "continuous-target-v1"):
            msg = "explicit continuous scalar target declaration required"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class RegressionInput:
    """Identified label-free numeric rows, with exact ordered source units."""

    features: FeatureTable
    feature_units: tuple[str | None, ...]
    row_ids: tuple[str, ...]
    population_id: str
    source_identity: str
    role: RegressionRole
    version: str = "regression-input-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        limits = version_limits(self.version, "regression-input")
        if not isinstance(self.features, FeatureTable) or not isinstance(
            self.role,
            RegressionRole,
        ):
            msg = "typed regression features and original role required"
            raise TypeError(msg)
        if (
            type(self.row_ids) is not tuple
            or len(self.row_ids) != len(self.features.rows)
            or len(set(self.row_ids)) != len(self.row_ids)
            or (not 1 <= len(self.features.feature_names) <= limits.features)
            or (len(self.row_ids) > limits.population_rows)
            or (type(self.feature_units) is not tuple)
            or (len(self.feature_units) != len(self.features.feature_names))
        ):
            msg = "bounded immutable original row/schema correspondence"
            raise ValueError(msg)
        for value in (*self.row_ids, self.population_id, self.source_identity):
            nonempty(value)
        for unit in self.feature_units:
            if unit is not None:
                nonempty(unit)
        if limits is REGRESSION_V2:
            check_text(
                (
                    *self.row_ids,
                    self.population_id,
                    self.source_identity,
                    *self.features.feature_names,
                    *self.feature_units,
                ),
            )

    @property
    def schema_identity(self) -> str:
        """Apply the explicit schema identity contract within this owner."""
        return "regression-schema-v1:" + fingerprint(
            (
                self.features.feature_names,
                self.features.feature_value_kinds,
                self.feature_units,
            ),
        )

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return self.version + ":" + fingerprint(asdict(self))


@dataclass(frozen=True, slots=True)
class RegressionPopulation:
    """Original finite continuous observations aligned to identified feature rows."""

    inputs: RegressionInput
    target: ContinuousTarget
    values: tuple[float, ...]
    missing_policy: str = "reject_no_imputation"
    version: str = "regression-population-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if (
            type(self.inputs) is not RegressionInput
            or type(self.target) is not ContinuousTarget
        ):
            msg = "continuous regression source contracts required"
            raise TypeError(msg)
        if (
            self.version != self.inputs.version.replace("input", "population")
            or self.missing_policy != "reject_no_imputation"
            or type(self.values) is not tuple
            or (len(self.values) != len(self.inputs.row_ids))
            or any(type(v) is not float or not math.isfinite(v) for v in self.values)
        ):
            msg = "finite original float targets; no category/int coercion"
            raise ValueError(msg)
        if self.version == "regression-population-v2":
            check_text((self.target.identity, self.target.quantity, self.target.unit))

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return self.version + ":" + fingerprint(asdict(self))


class RegressionMethod(Enum):
    """Retain the declared RegressionMethod scientific values and invariants."""

    MEAN = "training_mean"
    RIDGE = "ridge"
    KNN = "knn"


@dataclass(frozen=True, slots=True)
class RegressionSpecification:
    """One bounded semantic menu; native details are retained by the Integration."""

    method: RegressionMethod
    version: str = "regression-specification-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.method, RegressionMethod):
            msg = "supported concrete regression method required"
            raise TypeError(msg)
        if self.version != "regression-specification-v1" and (
            not (
                self.method is RegressionMethod.KNN
                and self.version == "regression-specification-v2"
            )
        ):
            msg = "unsupported regression specification"
            raise ValueError(msg)

    @property
    def configuration(self) -> tuple[tuple[str, str | int | float | bool], ...]:
        """Apply the explicit configuration contract within this owner."""
        if self.method is RegressionMethod.MEAN:
            return (("training_mean", "fsum_divide_n"),)
        if self.method is RegressionMethod.RIDGE:
            return (("alpha", 1.0), ("fit_intercept", True), ("solver", "svd"))
        if self.version == "regression-specification-v2":
            return (
                ("n_neighbors", 5),
                ("weights", "uniform"),
                ("metric", "euclidean"),
                ("algorithm", "brute"),
                ("n_jobs", 1),
                ("boundary_tie_policy", "computed_distance_original_row_utf8_v1"),
                ("distance_evaluation", "cpython_math_dist_binary64_v1"),
                ("target_average", "fsum_selected_distance_id_order_divide_five"),
            )
        return (
            ("n_neighbors", 5),
            ("weights", "uniform"),
            ("metric", "euclidean"),
            ("algorithm", "brute"),
            ("n_jobs", 1),
            ("boundary_tie_policy", "refuse_1e-12_relative_absolute"),
        )

    @property
    def complexity(self) -> int:
        """Apply the explicit complexity contract within this owner."""
        return tuple(RegressionMethod).index(self.method)

    @property
    def identity(self) -> str:
        """Apply the explicit identity contract within this owner."""
        revision = self.version.rsplit("-", 1)[1]
        return (
            "regression-method-"
            + revision
            + ":"
            + fingerprint((asdict(self), self.configuration))
        )
