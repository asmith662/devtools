# Copyright (c) 2026
"""Immutable population-standard-deviation scaling of selected continuous features.

Statistics use stdlib mean/pstdev on represented binary64 observations. Actual
constant coordinates retain zero deviation and use a unit denominator. Later
application aligns identities, never learns, and never scales extra indicators.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from fractions import Fraction
from statistics import mean, pstdev
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from devtools.learning.evidence.context import ExecutionContext, ExecutionRecorder
from devtools.learning.evidence.events import (
    Admitted,
    ExecutionEvent,
    Fact,
    FailureCategory,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.observations import PopulationScope

if TYPE_CHECKING:
    from collections.abc import Callable

MAX_OBSERVATIONS = 100000
MAX_FEATURES = 128
MAX_CELLS = 1000000


@dataclass(frozen=True, slots=True)
class FeatureStandardizationSpecification:
    """Select continuous coordinates under fixed population n/unit-constant policy."""

    feature_names: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if isinstance(self.feature_names, (str, bytes)):
            msg = "feature_names must be a sequence of identities"
            raise TypeError(msg)
        names = tuple(self.feature_names)
        if not 1 <= len(names) <= MAX_FEATURES or any(
            type(n) is not str or not n.strip() for n in names
        ):
            msg = "standardization requires 1..128 nonempty feature identities"
            raise ValueError(msg)
        if len(set(names)) != len(names):
            msg = "duplicate selected feature identity"
            raise ValueError(msg)
        object.__setattr__(self, "feature_names", names)


def _identity(value: str | None, *, required: bool = False) -> None:
    if value is None and (not required):
        return
    if type(value) is not str or not value.strip():
        msg = "population/source/representation identity must be nonempty"
        raise ValueError(msg)


def _selected(features: FeatureTable, names: tuple[str, ...]) -> FeatureTable:
    if not isinstance(features, FeatureTable):
        msg = "features must use FeatureTable"
        raise TypeError(msg)
    if (
        features.observation_count > MAX_OBSERVATIONS
        or features.observation_count * len(names) > MAX_CELLS
    ):
        msg = "standardization bounds: 100000 observations / 1000000 selected cells"
        raise ValueError(msg)
    positions = {n: i for i, n in enumerate(features.feature_names)}
    if any(n not in positions for n in names):
        msg = "missing required standardization coordinate"
        raise ValueError(msg)
    if any(
        features.feature_value_kinds[positions[n]] is not FeatureValueKind.CONTINUOUS
        for n in names
    ):
        msg = "standardization requires continuous quantitative coordinates"
        raise ValueError(msg)
    return FeatureTable(
        names,
        tuple(tuple(r[positions[n]] for n in names) for r in features.rows),
        (FeatureValueKind.CONTINUOUS,) * len(names),
    )


def _fingerprint(features: FeatureTable) -> str:
    digest = hashlib.sha256()
    digest.update(
        json.dumps(
            [features.feature_names, [k.value for k in features.feature_value_kinds]],
            separators=(",", ":"),
        ).encode(),
    )
    for row in features.rows:
        digest.update(
            (json.dumps([v.hex() for v in row], separators=(",", ":")) + "\n").encode(),
        )
    return digest.hexdigest()


def _z(value: float, center: float, scale: float) -> float:
    difference = value - center
    try:
        result = (
            difference / scale
            if math.isfinite(difference)
            else float((Fraction(value) - Fraction(center)) / Fraction(scale))
        )
    except (OverflowError, ZeroDivisionError) as error:
        msg = "standardized value is not finitely representable"
        raise ValueError(msg) from error
    if not math.isfinite(result) or (value != center and result == 0):
        msg = "standardized value overflows or underflows representation"
        raise ValueError(msg)
    return result


@dataclass(frozen=True, slots=True)
class StandardizationTransformationResult:
    """A fixed-state application with occurrence and selected-input evidence."""

    features: FeatureTable
    execution_id: UUID
    fitted_state_id: UUID
    construction_execution_id: UUID
    input_sha256: str
    population_id: str | None
    scope: PopulationScope | None
    source_identity: str | None
    representation_identity: str | None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.features, FeatureTable) or any(
            not isinstance(i, UUID)
            for i in (
                self.execution_id,
                self.fitted_state_id,
                self.construction_execution_id,
            )
        ):
            msg = "application requires typed features and occurrence/state identities"
            raise TypeError(msg)
        _digest(self.input_sha256)
        for value in (
            self.population_id,
            self.source_identity,
            self.representation_identity,
        ):
            _identity(value)
        if self.scope is not None and (not isinstance(self.scope, PopulationScope)):
            msg = "scope must use PopulationScope or remain unknown"
            raise TypeError(msg)


def _digest(value: str) -> None:
    if (
        type(value) is not str
        or len(value) != 64
        or any(c not in "0123456789abcdef" for c in value)
    ):
        msg = "selected-input evidence requires SHA-256"
        raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class FittedFeatureStandardization:
    """Retain training statistics and emit compatible rows in selected fitted order."""

    specification: FeatureStandardizationSpecification
    feature_value_kinds: tuple[FeatureValueKind, ...]
    training_means: tuple[float, ...]
    training_standard_deviations: tuple[float, ...]
    effective_scales: tuple[float, ...]
    constant_coordinates: tuple[bool, ...]
    fitting_population_id: str
    fitting_scope: PopulationScope
    fitting_observation_count: int
    fitting_input_sha256: str
    construction_execution_id: UUID
    source_identity: str | None = None
    representation_identity: str | None = None
    state_id: UUID = field(default_factory=uuid4)
    variance_convention: str = field(default="population_n", init=False)
    constant_policy: str = field(
        default="actual_zero_std_effective_unit_scale",
        init=False,
    )

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.specification, FeatureStandardizationSpecification):
            msg = "state requires FeatureStandardizationSpecification"
            raise TypeError(msg)
        n = len(self.specification.feature_names)
        for values in (
            self.feature_value_kinds,
            self.training_means,
            self.training_standard_deviations,
            self.effective_scales,
            self.constant_coordinates,
        ):
            if type(values) is not tuple or len(values) != n:
                msg = "one immutable statistic/kind per selected coordinate"
                raise ValueError(msg)
        if any(k is not FeatureValueKind.CONTINUOUS for k in self.feature_value_kinds):
            msg = "fitted coordinates must remain continuous"
            raise ValueError(msg)
        for center, deviation, scale, constant in zip(
            self.training_means,
            self.training_standard_deviations,
            self.effective_scales,
            self.constant_coordinates,
            strict=True,
        ):
            if (
                any(
                    type(v) is not float or not math.isfinite(v)
                    for v in (center, deviation, scale)
                )
                or type(constant) is not bool
            ):
                msg = "statistics require finite floats and typed constant facts"
                raise ValueError(msg)
            if (
                deviation < 0
                or constant != (deviation == 0)
                or scale != (1.0 if constant else deviation)
            ):
                msg = "actual deviation/constant/effective scale conflict"
                raise ValueError(msg)
        if (
            type(self.fitting_observation_count) is not int
            or not 1 <= self.fitting_observation_count <= MAX_OBSERVATIONS
            or self.fitting_observation_count * n > MAX_CELLS
        ):
            msg = "invalid fitting population/coordinate counts"
            raise ValueError(msg)
        _identity(self.fitting_population_id, required=True)
        for value in (self.source_identity, self.representation_identity):
            _identity(value)
        _digest(self.fitting_input_sha256)
        if not isinstance(
            self.fitting_scope,
            PopulationScope,
        ) or self.fitting_scope in (PopulationScope.VALIDATION, PopulationScope.TEST):
            msg = "evaluation populations cannot fit standardization"
            raise ValueError(msg)
        if (
            not isinstance(self.construction_execution_id, UUID)
            or not isinstance(self.state_id, UUID)
            or self.state_id == self.construction_execution_id
        ):
            msg = "fitted-state and construction occurrence identities differ"
            raise ValueError(msg)

    @property
    def feature_names(self) -> tuple[str, ...]:
        """Apply the explicit feature names contract within this owner."""
        return self.specification.feature_names

    def transform(
        self,
        features: FeatureTable,
        *,
        population_id: str | None = None,
        scope: PopulationScope | None = None,
        source_identity: str | None = None,
        representation_identity: str | None = None,
        recorder: ExecutionRecorder | None = None,
        observer: Callable[[ExecutionEvent], None] | None = None,
        parent: ExecutionContext | None = None,
    ) -> StandardizationTransformationResult:
        """Apply fixed statistics and retain later provenance or explicit unknowns."""

        def apply(
            execution: ExecutionContext | None,
        ) -> StandardizationTransformationResult:
            for identity in (population_id, source_identity, representation_identity):
                _identity(identity)
            if scope is not None and (not isinstance(scope, PopulationScope)):
                msg = "scope must use PopulationScope or remain unknown"
                raise TypeError(msg)
            if execution is not None:
                execution.stage(
                    "alignment",
                    "Validate fixed continuous feature identities",
                    FailureCategory.COMPATIBILITY,
                )
            selected = _selected(features, self.feature_names)
            if execution is not None:
                execution.stage(
                    "standardization",
                    "Center with fixed training mean and effective denominator",
                    FailureCategory.NUMERICAL,
                )
            output = FeatureTable(
                self.feature_names,
                tuple(
                    tuple(
                        (
                            _z(v, m, s)
                            for v, m, s in zip(
                                r,
                                self.training_means,
                                self.effective_scales,
                                strict=True,
                            )
                        ),
                    )
                    for r in selected.rows
                ),
                self.feature_value_kinds,
            )
            return StandardizationTransformationResult(
                output,
                execution.execution_id if execution else uuid4(),
                self.state_id,
                self.construction_execution_id,
                _fingerprint(selected),
                population_id,
                scope,
                source_identity,
                representation_identity,
            )

        if recorder is None:
            if observer is not None or parent is not None:
                msg = "observer/parent requires explicit recorder"
                raise ValueError(msg)
            return apply(None)
        with ExecutionContext(
            recorder,
            Admitted(
                "representation.standardization.transform",
                (
                    Fact("fitted_state_id", str(self.state_id)),
                    Fact(
                        "construction_execution_id",
                        str(self.construction_execution_id),
                    ),
                ),
            ),
            parent=parent,
            observer=observer,
        ) as execution:
            result = apply(execution)
            execution.completed(
                (
                    Fact("input_sha256", result.input_sha256),
                    Fact("population_id", population_id),
                    Fact("scope", scope.value if scope else None),
                    Fact("observation_count", result.features.observation_count),
                    Fact("coordinate_count", len(self.feature_names)),
                ),
            )
            return result


def fit_feature_standardization(
    specification: FeatureStandardizationSpecification,
    training_features: FeatureTable,
    *,
    population_id: str,
    scope: PopulationScope = PopulationScope.TRAINING,
    source_identity: str | None = None,
    representation_identity: str | None = None,
    recorder: ExecutionRecorder | None = None,
    observer: Callable[[ExecutionEvent], None] | None = None,
    parent: ExecutionContext | None = None,
) -> FittedFeatureStandardization:
    """Fit selected population mean/deviation; validation/test fitting is forbidden.

    mean/pstdev use exact binary-rational accumulation in the supported CPython
    stdlib, followed by binary64 rounding. No unstable floating E[x*x]-E[x]^2.
    Positive deviations rounding to zero and nonfinite statistics are rejected;
    variance itself need not be representable because actual deviations are retained.
    """

    def fit(execution: ExecutionContext | None) -> FittedFeatureStandardization:
        if execution is not None:
            execution.stage(
                "input_validation",
                "Validate selected coordinates and fitting scope",
                FailureCategory.INPUT,
            )
        if not isinstance(specification, FeatureStandardizationSpecification):
            msg = "specification must use FeatureStandardizationSpecification"
            raise TypeError(msg)
        _identity(population_id, required=True)
        _identity(source_identity)
        _identity(representation_identity)
        if not isinstance(scope, PopulationScope) or scope in (
            PopulationScope.VALIDATION,
            PopulationScope.TEST,
        ):
            msg = "evaluation populations cannot fit standardization"
            raise ValueError(msg)
        selected = _selected(training_features, specification.feature_names)
        if selected.observation_count == 0:
            msg = "fitting requires a nonempty population"
            raise ValueError(msg)
        if execution is not None:
            execution.stage(
                "population_statistics",
                "Fit population n mean/deviation; qualify exact constants",
                FailureCategory.NUMERICAL,
            )
        centers, deviations, constants = ([], [], [])
        for index in range(len(specification.feature_names)):
            values = tuple(r[index] for r in selected.rows)
            constant = min(values) == max(values)
            try:
                center, deviation = (float(mean(values)), float(pstdev(values)))
            except (OverflowError, ValueError) as error:
                msg = "fitted statistics are not finitely representable"
                raise ValueError(msg) from error
            if (
                not math.isfinite(center)
                or not math.isfinite(deviation)
                or (not constant and deviation == 0)
            ):
                msg = "fitted deviation overflows or underflows representation"
                raise ValueError(msg)
            centers.append(center)
            deviations.append(deviation)
            constants.append(constant)
        return FittedFeatureStandardization(
            specification,
            selected.feature_value_kinds,
            tuple(centers),
            tuple(deviations),
            tuple(
                (1.0 if c else s for c, s in zip(constants, deviations, strict=True)),
            ),
            tuple(constants),
            population_id,
            scope,
            selected.observation_count,
            _fingerprint(selected),
            execution.execution_id if execution else uuid4(),
            source_identity,
            representation_identity,
        )

    if recorder is None:
        if observer is not None or parent is not None:
            msg = "observer/parent requires explicit recorder"
            raise ValueError(msg)
        return fit(None)
    with ExecutionContext(
        recorder,
        Admitted(
            "representation.standardization.fit",
            (
                Fact("population_id", population_id),
                Fact(
                    "scope",
                    scope.value if isinstance(scope, PopulationScope) else None,
                ),
                Fact("source_identity", source_identity),
                Fact("representation_identity", representation_identity),
                Fact(
                    "selected_features",
                    json.dumps(specification.feature_names)
                    if isinstance(specification, FeatureStandardizationSpecification)
                    else None,
                ),
                Fact("implementation", "stdlib.population_standardization.v1"),
                Fact("variance_convention", "population_n"),
                Fact("constant_policy", "actual_zero_std_effective_unit_scale"),
            ),
        ),
        parent=parent,
        observer=observer,
    ) as execution:
        state = fit(execution)
        execution.completed(
            (
                Fact("fitted_state_id", str(state.state_id)),
                Fact("fitting_input_sha256", state.fitting_input_sha256),
                Fact("fitting_observation_count", state.fitting_observation_count),
                Fact("coordinate_count", len(state.feature_names)),
                Fact("means", json.dumps(state.training_means)),
                Fact(
                    "standard_deviations",
                    json.dumps(state.training_standard_deviations),
                ),
                Fact("effective_scales", json.dumps(state.effective_scales)),
                Fact("constant_coordinates", json.dumps(state.constant_coordinates)),
            ),
        )
        return state
