# Copyright (c) 2026
"""Validated immutable definitions, bindings and observations shared by consumers.

The core never computes family metrics or imports their implementations. A
definition validates value meaning; context records known production conditions.
Neither validation nor a fingerprint proves experimental comparability.
"""

from __future__ import annotations

import hashlib
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timedelta
from enum import Enum
from math import isfinite
from typing import Protocol, cast
from uuid import UUID

from devtools.learning.representation.features import FeatureValueKind
from devtools.learning.representation.observations import (
    ColumnRole,
    MissingValuePolicy,
    PopulationScope,
)
from devtools.learning.representation.targets import (
    CategoryValue,
    validate_category_values,
)


def nonempty(value: str) -> None:
    """Apply the explicit nonempty contract within this owner."""
    if type(value) is not str or not value.strip():
        msg = "measurement text identities/reasons must be nonempty"
        raise ValueError(msg)


def digest(value: str | None) -> None:
    """Apply the explicit digest contract within this owner."""
    if value is not None and (
        type(value) is not str or not re.fullmatch("[0-9a-f]{64}", value)
    ):
        msg = "measurement digest must be canonical SHA-256 or unknown"
        raise ValueError(msg)


def utc(value: datetime) -> None:
    """Apply the explicit utc contract within this owner."""
    if not isinstance(value, datetime) or value.utcoffset() != timedelta(0):
        msg = "measurement timestamps must be timezone-aware UTC"
        raise ValueError(msg)


class _DataclassParameters(Protocol):
    frozen: bool


class _DataclassClass(Protocol):
    __dataclass_params__: _DataclassParameters


def _immutable(value: object) -> None:
    """Reject mutable containers without importing any family's value classes."""
    if type(value) in (str, int, float, bool, type(None)):
        return
    if isinstance(value, tuple):
        for member in value:
            _immutable(member)
        return
    if is_dataclass(value) and (not isinstance(value, type)):
        if not cast("_DataclassClass", type(value)).__dataclass_params__.frozen:
            msg = "measurement structures must be frozen values"
            raise TypeError(msg)
        for field in fields(value):
            _immutable(getattr(value, field.name))
        return
    msg = "measurement value must have immutable scalar/structured state"
    raise TypeError(msg)


class ValueShape(Enum):
    """Retain the declared ValueShape scientific values and invariants."""

    COUNT = "exact_count"
    REAL = "finite_real"
    LABELED_COUNT_MATRIX = "labeled_count_matrix"


class UnitMeaning(Enum):
    """Retain the declared UnitMeaning scientific values and invariants."""

    DIMENSIONLESS = "dimensionless"
    OBSERVATIONS = "observations"
    SOURCE_QUANTITY = "source_quantity"
    SECONDS = "seconds"
    BYTES = "bytes"


@dataclass(frozen=True, slots=True)
class OutputContract:
    """Definition-level quantity; a source unit is separately declared in a binding."""

    shape: ValueShape
    unit: UnitMeaning

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.shape, ValueShape) or not isinstance(
            self.unit,
            UnitMeaning,
        ):
            msg = "output requires typed shape and unit meaning"
            raise TypeError(msg)


type ParameterValue = str | int | float | bool | tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MetricParameter:
    """A copied, type-preserving semantic parameter, never backend kwargs."""

    name: str
    value: ParameterValue

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.name)
        if type(self.value) not in (str, int, float, bool, tuple):
            msg = "metric parameter requires a supported immutable scalar/tuple"
            raise TypeError(msg)
        if type(self.value) is float and (not isfinite(self.value)):
            msg = "metric parameter must be finite"
            raise ValueError(msg)
        if isinstance(self.value, tuple) and any(
            type(v) is not str for v in self.value
        ):
            msg = "parameter tuples contain only strings"
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class DefinitionIdentity:
    """Retain the declared DefinitionIdentity scientific values and invariants."""

    semantic_key: str
    version: int
    parameters_sha256: str

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.semantic_key)
        if type(self.version) is not int or self.version < 1:
            msg = "definition version must be a positive integer"
            raise ValueError(msg)
        digest(self.parameters_sha256)


class NonValueKind(Enum):
    """Retain the declared NonValueKind scientific values and invariants."""

    UNDEFINED = "undefined"
    NOT_APPLICABLE = "not_applicable"
    NOT_MEASURED = "not_measured"
    UNAVAILABLE = "unavailable"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class Measured[V]:
    """A value only becomes validated evidence when bound through a definition."""

    value: V


@dataclass(frozen=True, slots=True)
class NoValue:
    """Retain the declared NoValue scientific values and invariants."""

    kind: NonValueKind
    reason_code: str
    detail: str
    diagnostic_event_id: UUID | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.kind, NonValueKind):
            msg = "nonvalue kind must be explicit"
            raise TypeError(msg)
        nonempty(self.reason_code)
        nonempty(self.detail)
        if self.diagnostic_event_id is not None and (
            not isinstance(self.diagnostic_event_id, UUID)
        ):
            msg = "diagnostic reference must be a UUID or unknown"
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class PopulationBinding:
    """All cases in the referenced context, not an unspecified global population."""


@dataclass(frozen=True, slots=True)
class CategoryBinding:
    """Retain the declared CategoryBinding scientific values and invariants."""

    category: CategoryValue

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        validate_category_values((self.category,))


@dataclass(frozen=True, slots=True)
class FieldBinding:
    """Source declarations are preserved as declarations, including unknown units."""

    field: str
    declared_role: ColumnRole
    declared_value_kind: FeatureValueKind | None
    missingness: MissingValuePolicy
    source_unit: str | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.field)
        if not isinstance(self.declared_role, ColumnRole):
            msg = "field role must use the source declaration contract"
            raise TypeError(msg)
        if self.declared_value_kind is not None and (
            not isinstance(self.declared_value_kind, FeatureValueKind)
        ):
            msg = "field value kind must be declared or unknown"
            raise TypeError(msg)
        if not isinstance(self.missingness, MissingValuePolicy):
            msg = "source missingness policy must be explicit"
            raise TypeError(msg)
        if self.source_unit is not None:
            nonempty(self.source_unit)


@dataclass(frozen=True, slots=True)
class ScopedBinding:
    """Nonpopulation application identified by a recorded source event.

    Families extend this concrete binding with their scope/window requirements.
    The core does not interpret process counters or duration clocks.
    """

    scope_identity: str
    source_event_id: UUID
    execution_id: UUID
    activation_id: UUID

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.scope_identity)
        if not isinstance(self.source_event_id, UUID):
            msg = "scoped measurement requires a source event UUID"
            raise TypeError(msg)
        if not isinstance(self.execution_id, UUID) or not isinstance(
            self.activation_id,
            UUID,
        ):
            msg = "scoped binding requires execution and activation UUIDs"
            raise TypeError(msg)


type MeasurementBinding = (
    PopulationBinding | CategoryBinding | FieldBinding | ScopedBinding
)


@dataclass(frozen=True, slots=True)
class MeasurementBasis:
    """Exact basis counts; subset count does not identify its members."""

    population_count: int
    effective_count: int
    numerator: int | None = None
    denominator: int | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        for value in (
            self.population_count,
            self.effective_count,
            self.numerator,
            self.denominator,
        ):
            if value is not None and (type(value) is not int or value < 0):
                msg = "measurement basis requires exact nonnegative counts"
                raise ValueError(msg)
        if self.effective_count > self.population_count:
            msg = "effective subset exceeds containing population"
            raise ValueError(msg)
        if (self.numerator is None) != (self.denominator is None):
            msg = "ratio evidence requires numerator and denominator together"
            raise ValueError(msg)
        if self.denominator is not None and (
            self.denominator > self.population_count
            or (self.numerator is not None and self.numerator > self.denominator)
        ):
            msg = "ratio counts exceed containing population/denominator"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    """A named dependency/reference, with byte integrity when actually known."""

    relation: str
    identity: str
    sha256: str | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.relation)
        nonempty(self.identity)
        digest(self.sha256)


@dataclass(frozen=True, slots=True)
class MeasurementContext:
    """Shared scope and honest production provenance; export is a separate activity."""

    context_id: UUID
    subject: str
    population_id: str | None
    scope: PopulationScope | None
    observation_count: int | None
    source_identity: str | None = None
    membership_sha256: str | None = None
    representation_identity: str | None = None
    producing_execution_id: UUID | None = None
    activation_id: UUID | None = None
    measured_at: datetime | None = None
    implementation: str | None = None
    references: tuple[EvidenceReference, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.context_id, UUID):
            msg = "context identity must be UUID"
            raise TypeError(msg)
        nonempty(self.subject)
        if (self.population_id, self.scope, self.observation_count) != (
            None,
            None,
            None,
        ):
            if self.population_id is None:
                msg = "population identity is required for population context"
                raise ValueError(msg)
            nonempty(self.population_id)
            if not isinstance(self.scope, PopulationScope):
                msg = "population scope must be explicit"
                raise TypeError(msg)
            if type(self.observation_count) is not int or self.observation_count < 0:
                msg = "context population count must be nonnegative"
                raise ValueError(msg)
        elif self.membership_sha256 is not None:
            msg = "nonpopulation context cannot claim membership"
            raise ValueError(msg)
        for value in (
            self.source_identity,
            self.representation_identity,
            self.implementation,
        ):
            if value is not None:
                nonempty(value)
        for identity in (self.producing_execution_id, self.activation_id):
            if identity is not None and (not isinstance(identity, UUID)):
                msg = "production identities must be UUID or unknown"
                raise TypeError(msg)
        if self.activation_id is not None and self.producing_execution_id is None:
            msg = "activation requires its producing execution"
            raise ValueError(msg)
        if self.measured_at is not None:
            utc(self.measured_at)
        digest(self.membership_sha256)
        refs, limits = (tuple(self.references), tuple(self.limitations))
        if any(not isinstance(ref, EvidenceReference) for ref in refs):
            msg = "context references must be typed"
            raise TypeError(msg)
        if len({(ref.relation, ref.identity) for ref in refs}) != len(refs):
            msg = "duplicate context references"
            raise ValueError(msg)
        for value in limits:
            nonempty(value)
        object.__setattr__(self, "references", refs)
        object.__setattr__(self, "limitations", limits)


@dataclass(frozen=True, slots=True)
class MetricDefinition[V](ABC):
    """Shared meaning/validation base; family computation is deliberately separate."""

    @property
    @abstractmethod
    def semantic_key(self) -> str:
        """Apply the explicit semantic key contract within this owner."""
        ...

    @property
    @abstractmethod
    def version(self) -> int:
        """Apply the explicit version contract within this owner."""
        ...

    @property
    @abstractmethod
    def parameters(self) -> tuple[MetricParameter, ...]:
        """Apply the explicit parameters contract within this owner."""
        ...

    @property
    @abstractmethod
    def output(self) -> OutputContract:
        """Apply the explicit output contract within this owner."""
        ...

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        self.validate_definition()

    def validate_definition(self) -> None:
        """Apply the explicit validate definition contract within this owner."""
        nonempty(self.semantic_key)
        if type(self.version) is not int or self.version < 1:
            msg = "definition version must be positive"
            raise ValueError(msg)
        if not isinstance(self.output, OutputContract):
            msg = "definition output must use OutputContract"
            raise TypeError(msg)
        if type(self.parameters) is not tuple or any(
            not isinstance(p, MetricParameter) for p in self.parameters
        ):
            msg = "definition parameters must be immutable typed values"
            raise TypeError(msg)
        if len({p.name for p in self.parameters}) != len(self.parameters):
            msg = "definition parameter identities must be unique"
            raise ValueError(msg)

    @property
    def identity(self) -> DefinitionIdentity:
        """Apply the explicit identity contract within this owner."""
        data = [
            (p.name, type(p.value).__name__, p.value)
            for p in sorted(self.parameters, key=lambda p: p.name)
        ]
        data.append(
            ("output", "contract", (self.output.shape.value, self.output.unit.value)),
        )
        encoded = json.dumps(
            data,
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
        )
        return DefinitionIdentity(
            self.semantic_key,
            self.version,
            hashlib.sha256(encoded.encode()).hexdigest(),
        )

    @abstractmethod
    def validate_value(self, value: V) -> None:
        """Apply the explicit validate value contract within this owner."""
        ...

    @abstractmethod
    def validate_binding(
        self,
        binding: MeasurementBinding,
        basis: MeasurementBasis | None,
    ) -> None:
        """Apply the explicit validate binding contract within this owner."""
        ...

    def validate_result(
        self,
        result: Measured[V] | NoValue,
        binding: MeasurementBinding,
        basis: MeasurementBasis | None,
    ) -> None:
        """Apply the explicit validate result contract within this owner."""
        self.validate_definition()
        self.validate_binding(binding, basis)
        if isinstance(result, Measured):
            value = result.value
            _immutable(value)
            if self.output.shape is ValueShape.COUNT and (
                type(value) is not int or cast("int", value) < 0
            ):
                msg = "count output requires an exact nonnegative integer"
                raise ValueError(msg)
            if self.output.shape is ValueShape.REAL and (
                type(value) is not float or not isfinite(cast("float", value))
            ):
                msg = "real output requires a finite float"
                raise ValueError(msg)
            if self.output.shape is ValueShape.LABELED_COUNT_MATRIX and (
                not is_dataclass(value) or isinstance(value, type)
            ):
                msg = "matrix output requires an immutable labeled structure"
                raise TypeError(msg)
            self.validate_value(result.value)
        elif not isinstance(result, NoValue):
            msg = "observation requires a measured value or explicit nonvalue"
            raise TypeError(msg)

    def observe(
        self,
        result: Measured[V] | NoValue,
        *,
        context_id: UUID,
        key: str,
        binding: MeasurementBinding,
        basis: MeasurementBasis | None,
        collected_at: datetime,
    ) -> MetricObservation[V]:
        """Construct validated evidence, without performing a metric calculation."""
        return MetricObservation(
            self,
            context_id,
            key,
            binding,
            basis,
            result,
            collected_at,
        )


@dataclass(frozen=True, slots=True)
class MetricObservation[V]:
    """Retain the declared MetricObservation scientific values and invariants."""

    definition: MetricDefinition[V]
    context_id: UUID
    key: str
    binding: MeasurementBinding
    basis: MeasurementBasis | None
    result: Measured[V] | NoValue
    collected_at: datetime

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.definition, MetricDefinition):
            msg = "observation requires a metric definition"
            raise TypeError(msg)
        if not isinstance(self.context_id, UUID):
            msg = "observation context identity must be UUID"
            raise TypeError(msg)
        nonempty(self.key)
        if not isinstance(
            self.binding,
            (PopulationBinding, CategoryBinding, FieldBinding, ScopedBinding),
        ) or (
            self.basis is None
            if not isinstance(self.binding, ScopedBinding)
            else self.basis is not None
        ):
            msg = "observation requires typed binding and basis"
            raise TypeError(msg)
        if self.basis is not None and (not isinstance(self.basis, MeasurementBasis)):
            msg = "population basis must be typed"
            raise TypeError(msg)
        utc(self.collected_at)
        self.definition.validate_result(self.result, self.binding, self.basis)


@dataclass(frozen=True, slots=True)
class MeasurementBundle[V]:
    """Identified collection with shared contexts and unique local observation keys."""

    bundle_id: UUID
    collected_at: datetime
    contexts: tuple[MeasurementContext, ...]
    observations: tuple[MetricObservation[V], ...]
    adaptation_execution_id: UUID | None = None

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.bundle_id, UUID):
            msg = "bundle identity must be UUID"
            raise TypeError(msg)
        utc(self.collected_at)
        if self.adaptation_execution_id is not None and (
            not isinstance(self.adaptation_execution_id, UUID)
        ):
            msg = "adaptation occurrence must be UUID or unknown"
            raise TypeError(msg)
        contexts, observations = (tuple(self.contexts), tuple(self.observations))
        if not contexts or any(not isinstance(c, MeasurementContext) for c in contexts):
            msg = "bundle requires typed contexts"
            raise ValueError(msg)
        by_id = {c.context_id: c for c in contexts}
        if len(by_id) != len(contexts):
            msg = "context identities must be unique"
            raise ValueError(msg)
        keys: set[str] = set()
        for observation in observations:
            if not isinstance(observation, MetricObservation):
                msg = "bundle requires typed observations"
                raise TypeError(msg)
            if observation.key in keys:
                msg = "observation keys must be unique within bundle"
                raise ValueError(msg)
            keys.add(observation.key)
            if observation.context_id not in by_id:
                msg = "observation/context population identity mismatch"
                raise ValueError(msg)
            context = by_id[observation.context_id]
            if isinstance(observation.binding, ScopedBinding):
                if (
                    context.observation_count is not None
                    or observation.basis is not None
                ):
                    msg = "scoped measurement has no population denominator"
                    raise ValueError(msg)
                if (
                    observation.binding.execution_id != context.producing_execution_id
                    or observation.binding.activation_id != context.activation_id
                ):
                    msg = "scoped binding/context occurrence identity mismatch"
                    raise ValueError(msg)
            elif (
                observation.basis is None
                or context.observation_count is None
                or observation.basis.population_count != context.observation_count
            ):
                msg = "observation/context population identity mismatch"
                raise ValueError(msg)
            if observation.collected_at != self.collected_at:
                msg = "observation collection time must agree with bundle"
                raise ValueError(msg)
            measured_at = by_id[observation.context_id].measured_at
            if measured_at is not None and observation.collected_at < measured_at:
                msg = "collection cannot precede known measurement start"
                raise ValueError(msg)
        object.__setattr__(self, "contexts", contexts)
        object.__setattr__(self, "observations", observations)
