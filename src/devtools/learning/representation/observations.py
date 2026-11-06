# Copyright (c) 2026
"""Caller-owned scalar observations, separate from prepared learning features."""

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum
from math import isnan

from devtools.learning.representation.features import FeatureValueKind
from devtools.learning.representation.targets import CategoryValue

type ObservationValue = CategoryValue | None


class ColumnRole(Enum):
    """Declarations are caller claims, never inferred from storage or field names."""

    UNKNOWN = "unknown"
    NUMERIC_FEATURE = "numeric_feature"
    CATEGORICAL_FEATURE = "categorical_feature"
    TARGET = "target"
    IDENTIFIER = "identifier"
    METADATA = "metadata"


class PopulationScope(Enum):
    FULL_DESCRIPTIVE = "full_descriptive"
    DESCRIPTIVE_SUBSET = "descriptive_subset"
    TRAINING = "training"
    VALIDATION = "validation"
    TEST = "test"


@dataclass(frozen=True, slots=True)
class MissingValuePolicy:
    """None is missing; other source tokens require an explicit interpretation.

    NaN is missing by default, but remains an observed nonfinite number. Infinity
    is invalid numerical evidence, not automatically missing. Sentinels may be
    identified yet retained, as in the existing Adult '?' category policy.
    Strings are never stripped or coerced by the shared observation contract.
    """

    source_sentinels: tuple[str, ...] = ()
    sentinels_are_missing: bool = False
    empty_strings_are_missing: bool = False
    whitespace_only_strings_are_missing: bool = False
    nan_is_missing: bool = True

    def __post_init__(self) -> None:
        if isinstance(self.source_sentinels, (str, bytes)):
            msg = "source_sentinels must be a sequence of string tokens"
            raise TypeError(msg)
        sentinels = tuple(self.source_sentinels)
        if any(type(value) is not str for value in sentinels):
            msg = "source sentinels must be strings"
            raise TypeError(msg)
        if len(set(sentinels)) != len(sentinels):
            msg = "source sentinels must be unique"
            raise ValueError(msg)
        for flag in (
            self.sentinels_are_missing,
            self.empty_strings_are_missing,
            self.whitespace_only_strings_are_missing,
            self.nan_is_missing,
        ):
            if type(flag) is not bool:
                msg = "missingness flags must be booleans"
                raise TypeError(msg)
        object.__setattr__(self, "source_sentinels", sentinels)

    def is_missing(self, value: ObservationValue) -> bool:
        if value is None:
            return True
        if type(value) is float:
            return self.nan_is_missing and isnan(value)
        if type(value) is str:
            return (
                (self.sentinels_are_missing and value in self.source_sentinels)
                or (self.empty_strings_are_missing and value == "")
                or (self.whitespace_only_strings_are_missing and (not value.strip()))
            )
        return False


@dataclass(frozen=True, slots=True)
class ScalarColumn:
    """A copied scalar column permitting source missingness and mixed types.

    Only builtin strings, integers, floats, booleans and None are supported.
    Containers and native backend objects fail at this boundary, rather than
    being implicitly stringified. Nonfinite floats are accepted for diagnosis.
    """

    name: str
    values: tuple[ObservationValue, ...]
    declared_role: ColumnRole = ColumnRole.UNKNOWN
    declared_value_kind: FeatureValueKind | None = None
    missingness: MissingValuePolicy = MissingValuePolicy()

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name.strip():
            msg = "column identity must be a nonempty string"
            raise ValueError(msg)
        if isinstance(self.values, (str, bytes)):
            msg = "values must be a sequence of scalar observations"
            raise TypeError(msg)
        values = tuple(self.values)
        if any(
            type(value) not in (str, int, float, bool, type(None)) for value in values
        ):
            msg = "tabular observations support builtin scalar observations only"
            raise TypeError(msg)
        if not isinstance(self.declared_role, ColumnRole):
            msg = "declared_role must use ColumnRole"
            raise TypeError(msg)
        if self.declared_value_kind is not None and (
            not isinstance(self.declared_value_kind, FeatureValueKind)
        ):
            msg = "declared_value_kind must use FeatureValueKind"
            raise TypeError(msg)
        if not isinstance(self.missingness, MissingValuePolicy):
            msg = "missingness must use MissingValuePolicy"
            raise TypeError(msg)
        object.__setattr__(self, "values", values)


@dataclass(frozen=True, slots=True)
class TabularObservations:
    """One explicitly identified aligned population, not a universal dataset.

    Source identity and roles are supplied by the caller. Consumers separately
    fingerprint actual observations and policies. Empty populations are valid
    descriptive subjects; zero-column inputs are not. Bounds limit this first
    exact, in-memory slice, not process memory or arbitrary ingestion.
    """

    population_id: str
    scope: PopulationScope
    columns: tuple[ScalarColumn, ...]
    source_identity: str | None = None

    def __post_init__(self) -> None:
        if type(self.population_id) is not str or not self.population_id.strip():
            msg = "population_id must be a nonempty caller identity"
            raise ValueError(msg)
        if not isinstance(self.scope, PopulationScope):
            msg = "scope must use PopulationScope"
            raise TypeError(msg)
        if self.source_identity is not None and (
            type(self.source_identity) is not str or not self.source_identity.strip()
        ):
            msg = "source_identity must be a nonempty string when supplied"
            raise ValueError(msg)
        columns = tuple(self.columns)
        if not 1 <= len(columns) <= 128:
            msg = "tabular observations require 1..128 columns"
            raise ValueError(msg)
        if any(not isinstance(column, ScalarColumn) for column in columns):
            msg = "columns must use ScalarColumn"
            raise TypeError(msg)
        if len({column.name for column in columns}) != len(columns):
            msg = "column identities must be unique"
            raise ValueError(msg)
        count = len(columns[0].values)
        if any(len(column.values) != count for column in columns):
            msg = "columns must preserve aligned observation counts"
            raise ValueError(msg)
        if count > 100000 or count * len(columns) > 1000000:
            msg = "tabular observation bounds are 100000 observations / 1000000 cells"
            raise ValueError(msg)
        object.__setattr__(self, "columns", columns)

    @property
    def observation_count(self) -> int:
        return len(self.columns[0].values)


def observation_fingerprint(subject: TabularObservations) -> str:
    """Type-aware, ordered identity; NaN/inf remain diagnostic tokens, not JSON NaN."""
    digest = hashlib.sha256()

    def append(value: object) -> None:
        digest.update(
            (json.dumps(value, sort_keys=True, ensure_ascii=True) + "\n").encode(),
        )

    append({"schema_version": 1, "scope": subject.scope.value})
    for column in subject.columns:
        append(
            {
                "name": column.name,
                "declared_role": column.declared_role.value,
                "declared_value_kind": column.declared_value_kind.value
                if column.declared_value_kind is not None
                else None,
                "missingness": asdict(column.missingness),
            },
        )
        for value in column.values:
            append(
                (type(value).__name__, value.hex() if type(value) is float else value),
            )
    return digest.hexdigest()
