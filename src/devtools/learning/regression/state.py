# Copyright (c) 2026
"""Immutable retained regression arithmetic; no native object or fitting import."""

import math
from collections.abc import Callable
from dataclasses import asdict, dataclass
from uuid import UUID

from devtools.learning.classification.linear import _hash
from devtools.learning.measurement.contracts import nonempty
from devtools.learning.regression.contracts import (
    ContinuousTarget,
    RegressionInput,
    RegressionMethod,
    RegressionPopulation,
    RegressionRole,
    RegressionSpecification,
)
from devtools.learning.regression.limits import (
    REGRESSION_V1,
    REGRESSION_V2,
    check_text,
    prediction_byte_bound,
    version_limits,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.observations import PopulationScope
from devtools.learning.representation.standardization import (
    FittedFeatureStandardization,
    _fingerprint,
)

_NEIGHBOR_COUNT = 5
_BACKEND_PAIR_SIZE = 2


def finite(value: float) -> float:
    """Apply the explicit finite contract within this owner."""
    if not math.isfinite(value):
        msg = "regression arithmetic is not finitely representable"
        raise ValueError(msg)
    return value


def training_mean(values: tuple[float, ...]) -> float:
    """Apply the explicit training mean contract within this owner."""
    if not values or any(type(v) is not float or not math.isfinite(v) for v in values):
        msg = "finite nonempty original continuous targets required"
        raise ValueError(msg)
    try:
        return finite(math.fsum(values) / len(values))
    except OverflowError as error:
        msg = "unrepresentable training mean"
        raise ValueError(msg) from error


def neighbors(
    training: tuple[tuple[float, ...], ...],
    row: tuple[float, ...],
    *,
    version: str = "fitted-regression-v1",
) -> tuple[tuple[int, ...], tuple[float, ...]]:
    """Inspect the selected set under the declared deterministic tie contract."""
    limits = version_limits(version, "fitted-regression")
    if (
        not _NEIGHBOR_COUNT <= len(training) <= limits.training_rows
        or len(training) * len(row) > limits.training_cells
    ):
        msg = "bounded retained five-neighbor corpus required"
        raise ValueError(msg)
    try:
        distances = tuple(finite(math.dist(row, other)) for other in training)
    except OverflowError as error:
        msg = "unrepresentable Euclidean distance"
        raise ValueError(msg) from error
    order = sorted(range(len(distances)), key=lambda i: (distances[i], i))
    if len(order) > _NEIGHBOR_COUNT and math.isclose(
        distances[order[4]],
        distances[order[5]],
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        msg = "unsupported ambiguous kth-neighbor distance boundary"
        raise ValueError(msg)
    selected = tuple(sorted(order[:5]))
    return (selected, tuple(distances[i] for i in selected))


def deterministic_neighbors(
    training: tuple[tuple[float, ...], ...],
    row: tuple[float, ...],
    row_ids: tuple[str, ...],
) -> tuple[tuple[int, ...], tuple[float, ...]]:
    """V2: exact computed math.dist order, then original UTF-8 identity.

    No isclose buckets or targets. Historical neighbors() remains unchanged.
    Qualification is for the recorded CPython binary64 implementation.
    """
    limits = REGRESSION_V2
    if (
        type(training) is not tuple
        or type(row) is not tuple
        or type(row_ids) is not tuple
        or (not _NEIGHBOR_COUNT <= len(training) <= limits.training_rows)
        or (len(row_ids) != len(training))
        or (len(set(row_ids)) != len(row_ids))
        or (not 1 <= len(row) <= limits.features)
        or (len(training) * len(row) > limits.training_cells)
        or any(type(i) is not str or not i for i in row_ids)
        or any(type(r) is not tuple or len(r) != len(row) for r in training)
        or any(
            type(v) not in (float, int) or not math.isfinite(v)
            for r in (*training, row)
            for v in r
        )
    ):
        msg = "finite complete identified deterministic kNN corpus required"
        raise ValueError(msg)
    check_text(row_ids)
    try:
        keys = tuple(i.encode("utf-8") for i in row_ids)
        distances = tuple(finite(math.dist(row, other)) for other in training)
    except (OverflowError, UnicodeError) as error:
        msg = "unrepresentable deterministic distance/identity"
        raise ValueError(msg) from error
    selected = tuple(
        sorted(range(len(training)), key=lambda i: (distances[i], keys[i]))[:5],
    )
    return (selected, tuple(distances[i] for i in selected))


@dataclass(frozen=True, slots=True)
class RegressionPredictions:
    """Retain the declared RegressionPredictions scientific values and invariants."""

    state_id: UUID
    method_identity: str
    input_identity: str
    population_id: str
    row_ids: tuple[str, ...]
    target: ContinuousTarget
    values: tuple[float, ...]
    neighbor_row_ids: tuple[tuple[str, ...], ...] | None = None
    neighbor_distances: tuple[tuple[float, ...], ...] | None = None
    version: str = "regression-predictions-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        limits = version_limits(self.version, "regression-predictions")
        if (
            not isinstance(self.state_id, UUID)
            or type(self.target) is not ContinuousTarget
            or type(self.row_ids) is not tuple
            or (type(self.values) is not tuple)
            or (len(self.row_ids) != len(self.values))
            or (len(set(self.row_ids)) != len(self.row_ids))
            or any(type(v) is not float or not math.isfinite(v) for v in self.values)
        ):
            msg = "exact finite identified regression predictions required"
            raise ValueError(msg)
        if limits is REGRESSION_V2 and len(self.row_ids) > limits.prediction_rows:
            msg = "bounded complete prediction population required"
            raise ValueError(msg)
        for v in (
            self.method_identity,
            self.input_identity,
            self.population_id,
            *self.row_ids,
        ):
            nonempty(v)
        if (self.neighbor_row_ids is None) != (self.neighbor_distances is None):
            msg = "neighbor membership and distances remain paired"
            raise ValueError(msg)
        if self.neighbor_row_ids is not None:
            if not (self.neighbor_distances is not None):
                msg_0 = "Required numerical state invariant is absent."
                raise AssertionError(msg_0)
            if (
                type(self.neighbor_row_ids) is not tuple
                or type(self.neighbor_distances) is not tuple
            ):
                msg = "immutable identified neighbor results required"
                raise ValueError(msg)
            if len(self.neighbor_row_ids) != len(self.row_ids) or len(
                self.neighbor_distances,
            ) != len(self.row_ids):
                msg = "complete query-neighbor correspondence"
                raise ValueError(msg)
            for ids, distances in zip(
                self.neighbor_row_ids,
                self.neighbor_distances,
                strict=True,
            ):
                if (
                    type(ids) is not tuple
                    or type(distances) is not tuple
                    or any(type(v) is not str or not v for v in ids)
                    or (len(ids) != _NEIGHBOR_COUNT)
                    or (len(set(ids)) != _NEIGHBOR_COUNT)
                    or (len(distances) != _NEIGHBOR_COUNT)
                    or any(
                        type(v) is not float or not math.isfinite(v) or v < 0
                        for v in distances
                    )
                ):
                    msg = "five original neighbors and finite distances"
                    raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return self.version + ":" + _hash(asdict(self))


@dataclass(frozen=True, slots=True)
class FittedRegression:
    """Three concrete regression states, not a universal fitted-model interface."""

    specification: RegressionSpecification
    target: ContinuousTarget
    feature_names: tuple[str, ...]
    feature_value_kinds: tuple[FeatureValueKind, ...]
    feature_units: tuple[str | None, ...]
    training_population_id: str
    training_row_ids: tuple[str, ...]
    training_identity: str
    preparation: FittedFeatureStandardization | None
    coefficients: tuple[float, ...]
    intercept: float
    neighbor_features: FeatureTable | None
    neighbor_targets: tuple[float, ...] | None
    execution_id: UUID
    state_id: UUID
    backend: tuple[tuple[str, str], ...]
    version: str = "fitted-regression-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        limits = version_limits(self.version, "fitted-regression")
        if (
            self.specification.version == "regression-specification-v2"
            and self.version != "fitted-regression-v2"
        ):
            msg = "deterministic numerical specification requires capacity-v2 state"
            raise ValueError(msg)
        if (
            type(self.specification) is not RegressionSpecification
            or type(self.target) is not ContinuousTarget
        ):
            msg = "concrete regression specification and target required"
            raise TypeError(msg)
        if not isinstance(self.execution_id, UUID) or not isinstance(
            self.state_id,
            UUID,
        ):
            msg = "original state and fitting occurrence identity required"
            raise ValueError(msg)
        if any(
            type(v) is not float or not math.isfinite(v)
            for v in (*self.coefficients, self.intercept)
        ):
            msg = "finite retained regression parameters required"
            raise ValueError(msg)
        if any(
            type(v) is not tuple
            for v in (
                self.feature_names,
                self.feature_value_kinds,
                self.feature_units,
                self.training_row_ids,
                self.coefficients,
                self.backend,
            )
        ):
            msg = "immutable source-bound regression state required"
            raise ValueError(msg)
        if self.state_id == self.execution_id or any(
            type(pair) is not tuple
            or len(pair) != _BACKEND_PAIR_SIZE
            or any(type(v) is not str or not v for v in pair)
            for pair in self.backend
        ):
            msg = "separate state/fit identities and immutable backend versions"
            raise ValueError(msg)
        if (
            not 1 <= len(self.feature_names) <= limits.features
            or len(self.feature_names) != len(self.feature_units)
            or len(self.feature_names) != len(self.feature_value_kinds)
            or (len(set(self.feature_names)) != len(self.feature_names))
            or (not 1 <= len(self.training_row_ids) <= limits.training_rows)
            or (len(set(self.training_row_ids)) != len(self.training_row_ids))
        ):
            msg = "original bounded fitted schema/population required"
            raise ValueError(msg)
        if any(k is not FeatureValueKind.CONTINUOUS for k in self.feature_value_kinds):
            msg = "continuous numerical features required"
            raise ValueError(msg)
        for v in (
            *self.feature_names,
            *self.training_row_ids,
            self.training_population_id,
            self.training_identity,
        ):
            nonempty(v)
        for unit in self.feature_units:
            if unit is not None:
                nonempty(unit)
        if limits is REGRESSION_V2:
            check_text(
                (
                    *self.feature_names,
                    *self.training_row_ids,
                    self.training_population_id,
                    self.training_identity,
                    *self.feature_units,
                    self.target.identity,
                    self.target.quantity,
                    self.target.unit,
                    *(x for pair in self.backend for x in pair),
                ),
            )
        method = self.specification.method
        if method is RegressionMethod.MEAN:
            if (
                self.preparation is not None
                or self.coefficients
                or self.neighbor_features is not None
                or (self.neighbor_targets is not None)
            ):
                msg = "mean state has only its original training mean"
                raise ValueError(msg)
        else:
            p = self.preparation
            if (
                p is None
                or p.fitting_population_id != self.training_population_id
                or p.fitting_scope is not PopulationScope.TRAINING
                or (p.feature_names != self.feature_names)
                or (p.fitting_observation_count != len(self.training_row_ids))
            ):
                msg = "proper original-training preparation required"
                raise ValueError(msg)
            if method is RegressionMethod.RIDGE:
                if (
                    len(self.coefficients) != len(self.feature_names)
                    or self.neighbor_features is not None
                    or self.neighbor_targets is not None
                ):
                    msg = "Ridge retains coefficients/intercept, not a neighbor model"
                    raise ValueError(msg)
            elif (
                self.coefficients
                or self.intercept != 0.0
                or self.neighbor_features is None
                or (self.neighbor_targets is None)
                or (type(self.neighbor_targets) is not tuple)
                or (len(self.neighbor_targets) != len(self.training_row_ids))
                or (
                    self.neighbor_features.observation_count
                    != len(self.training_row_ids)
                )
                or (self.neighbor_features.feature_names != self.feature_names)
                or (
                    self.neighbor_features.feature_value_kinds
                    != self.feature_value_kinds
                )
                or (len(self.training_row_ids) < _NEIGHBOR_COUNT)
                or any(
                    type(v) is not float or not math.isfinite(v)
                    for v in self.neighbor_targets
                )
            ):
                msg = "actual original prepared neighbor corpus required"
                raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return self.version + ":" + _hash(asdict(self))

    def predict(self, inputs: RegressionInput) -> RegressionPredictions:
        """Label-free retained arithmetic, preserving row order and source units."""
        if type(inputs) is not RegressionInput:
            msg = "typed original prediction population required"
            raise ValueError(msg)
        larger = (
            self.version == "fitted-regression-v2"
            or inputs.version == "regression-input-v2"
        )
        limits = REGRESSION_V2 if larger else REGRESSION_V1
        return self._predict_ranges(
            inputs,
            ((0, len(inputs.row_ids)),),
            larger=larger,
            work_limit=limits.distance_operations,
        )

    def _predict_ranges(
        self,
        inputs: RegressionInput,
        ranges: tuple[tuple[int, int], ...],
        *,
        larger: bool,
        work_limit: int,
        progress: Callable[[int, int], None] | None = None,
    ) -> RegressionPredictions:
        """One shared arithmetic kernel; ranges never create population identities."""
        if type(inputs) is not RegressionInput or (
            inputs.features.feature_names,
            inputs.features.feature_value_kinds,
            inputs.feature_units,
        ) != (self.feature_names, self.feature_value_kinds, self.feature_units):
            msg = "exact original ordered feature schema/units required"
            raise ValueError(msg)
        limits = REGRESSION_V2 if larger else REGRESSION_V1
        work = (
            len(inputs.row_ids) * len(self.training_row_ids) * len(self.feature_names)
            if not larger or self.specification.method is RegressionMethod.KNN
            else 0
        )
        if (
            len(inputs.row_ids) > limits.prediction_rows
            or type(work_limit) is not int
            or (not 1 <= work_limit <= limits.distance_operations)
            or (work > work_limit)
        ):
            msg = "prediction work bound exceeded before materialization"
            raise ValueError(msg)
        if (
            larger
            and prediction_byte_bound(
                inputs.row_ids,
                self.training_row_ids,
                (
                    inputs.population_id,
                    self.target.identity,
                    self.target.quantity,
                    self.target.unit,
                ),
                neighbors=self.specification.method is RegressionMethod.KNN,
            )
            > REGRESSION_V2.prediction_bytes
        ):
            msg = "bounded complete prediction payload required"
            raise ValueError(msg)
        values = []
        members = []
        distances = []
        try:
            for start, stop in ranges:
                original = FeatureTable(
                    inputs.features.feature_names,
                    inputs.features.rows[start:stop],
                    inputs.features.feature_value_kinds,
                )
                table = (
                    original
                    if self.preparation is None
                    else self.preparation.transform(original).features
                )
                for row in table.rows:
                    if self.specification.method is RegressionMethod.MEAN:
                        value = self.intercept
                    elif self.specification.method is RegressionMethod.RIDGE:
                        value = finite(
                            math.fsum(
                                (
                                    a * b
                                    for a, b in zip(self.coefficients, row, strict=True)
                                ),
                            )
                            + self.intercept,
                        )
                    else:
                        if not (self.neighbor_features is not None):
                            msg_0 = "Required numerical state invariant is absent."
                            raise AssertionError(msg_0)
                        if not (self.neighbor_targets is not None):
                            msg_0 = "Required numerical state invariant is absent."
                            raise AssertionError(msg_0)
                        if self.specification.version == "regression-specification-v2":
                            indices, ds = deterministic_neighbors(
                                self.neighbor_features.rows,
                                row,
                                self.training_row_ids,
                            )
                        else:
                            indices, ds = neighbors(
                                self.neighbor_features.rows,
                                row,
                                version="fitted-regression-v2"
                                if larger
                                else self.version,
                            )
                        value = finite(
                            math.fsum(self.neighbor_targets[i] for i in indices) / 5,
                        )
                        members.append(tuple(self.training_row_ids[i] for i in indices))
                        distances.append(ds)
                    values.append(value)
                if progress is not None:
                    progress(stop, len(inputs.row_ids))
        except OverflowError as error:
            msg = "unrepresentable regression prediction"
            raise ValueError(msg) from error
        knn = self.specification.method is RegressionMethod.KNN
        return RegressionPredictions(
            self.state_id,
            self.specification.identity,
            inputs.content_identity,
            inputs.population_id,
            inputs.row_ids,
            self.target,
            tuple(values),
            tuple(members) if knn else None,
            tuple(distances) if knn else None,
            inputs.version.replace("input", "predictions"),
        )


def validate_training_preparation(
    p: FittedFeatureStandardization,
    training: RegressionPopulation,
) -> FeatureTable:
    """Replay original fitting-only statistics even when a later native fit failed."""
    from statistics import mean, pstdev

    t = training.inputs
    if (
        t.role is not RegressionRole.TRAINING
        or p.feature_names != t.features.feature_names
        or p.feature_value_kinds != t.features.feature_value_kinds
        or (p.fitting_population_id != t.population_id)
        or (p.fitting_observation_count != len(t.row_ids))
        or (p.fitting_scope is not PopulationScope.TRAINING)
    ):
        msg = "original training-only preparation population/schema"
        raise ValueError(msg)
    means = tuple(
        float(mean(tuple(r[j] for r in t.features.rows)))
        for j in range(len(p.feature_names))
    )
    deviations = tuple(
        float(pstdev(tuple(r[j] for r in t.features.rows)))
        for j in range(len(p.feature_names))
    )
    if (
        p.training_means != means
        or p.training_standard_deviations != deviations
        or p.fitting_input_sha256 != _fingerprint(t.features)
        or (p.source_identity != t.source_identity)
    ):
        msg = "original training-only standardization arithmetic"
        raise ValueError(msg)
    return p.transform(t.features).features


def validate_training_state(
    state: FittedRegression,
    training: RegressionPopulation,
) -> None:
    """Check source, training-only preparation, means/corpus and Ridge residuals.

    These are retained arithmetic conditions, not optimizer reproduction.
    """
    t = training.inputs
    if (
        t.role is not RegressionRole.TRAINING
        or state.version != t.version.replace("regression-input", "fitted-regression")
        or (
            state.training_identity,
            state.training_population_id,
            state.training_row_ids,
            state.target,
            state.feature_names,
            state.feature_value_kinds,
            state.feature_units,
        )
        != (
            training.content_identity,
            t.population_id,
            t.row_ids,
            training.target,
            t.features.feature_names,
            t.features.feature_value_kinds,
            t.feature_units,
        )
    ):
        msg = "original fitting population/schema/target correspondence"
        raise ValueError(msg)
    if state.specification.method is RegressionMethod.MEAN:
        if state.intercept != training_mean(training.values):
            msg = "original training mean arithmetic"
            raise ValueError(msg)
        return
    p = state.preparation
    if not (p is not None):
        msg_0 = "Required numerical state invariant is absent."
        raise AssertionError(msg_0)
    x = validate_training_preparation(p, training)
    if state.specification.method is RegressionMethod.KNN:
        if state.neighbor_features != x or state.neighbor_targets != training.values:
            msg = "original source-bound neighbor corpus"
            raise ValueError(msg)
        return
    residuals = tuple(
        (
            y
            - (
                math.fsum((c * v for c, v in zip(state.coefficients, row, strict=True)))
                + state.intercept
            )
            for row, y in zip(x.rows, training.values, strict=True)
        ),
    )
    scale = max(
        1.0,
        math.fsum(abs(y) for y in training.values),
        *(
            math.fsum(
                (
                    abs(row[j] * y)
                    for row, y in zip(x.rows, training.values, strict=True)
                ),
            )
            for j in range(len(state.coefficients))
        ),
    )
    errors = (
        abs(math.fsum(residuals)),
        *(
            abs(
                math.fsum(
                    (row[j] * r for row, r in zip(x.rows, residuals, strict=True)),
                )
                - state.coefficients[j],
            )
            for j in range(len(state.coefficients))
        ),
    )
    if any(not math.isfinite(v) or v > 1e-08 * scale for v in errors):
        msg = "retained Ridge intercept/regularized normal-equation residual"
        raise ValueError(msg)
