# Copyright (c) 2026
"""Identified immutable binary linear prediction, independent of fitting backend.

The supplied numerical schema can be generated or ordinary. Preparation and
feature construction remain separately identified dependencies, not native model
objects owned by this classifier. A logit is not a calibrated success probability.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from uuid import UUID, uuid4

from devtools.learning.measurement.contracts import EvidenceReference, digest, nonempty
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.standardization import _fingerprint
from devtools.learning.requirements.evidence import validate_references


def _hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
            default=str,
        ).encode(),
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class BinaryLinearTraining:
    """Explicit aligned binary fitting population; missing labels cannot fit."""

    features: FeatureTable
    targets: tuple[int, ...]
    row_ids: tuple[str, ...]
    population_id: str
    target_identity: str
    references: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if not isinstance(self.features, FeatureTable):
            msg = "FeatureTable required"
            raise TypeError(msg)
        if (
            not self.features.feature_names
            or not self.features.rows
            or any(
                k is not FeatureValueKind.CONTINUOUS
                for k in self.features.feature_value_kinds
            )
        ):
            msg = "finite nonempty continuous training required"
            raise ValueError(msg)
        if (
            type(self.targets) is not tuple
            or any(type(v) is not int or v not in (0, 1) for v in self.targets)
            or set(self.targets) != {0, 1}
        ):
            msg = "both original integer categories 0/1 required"
            raise ValueError(msg)
        if (
            type(self.row_ids) is not tuple
            or len(set(self.row_ids)) != len(self.row_ids)
            or len(self.row_ids) != len(self.targets)
            or (len(self.targets) != self.features.observation_count)
        ):
            msg = "unique aligned immutable fitting rows required"
            raise ValueError(msg)
        for text in (*self.row_ids, self.population_id, self.target_identity):
            nonempty(text)
        validate_references(self.references)
        if not self.references:
            msg = "actual training source references required"
            raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return _hash(
            {
                "input_sha256": _fingerprint(self.features),
                "targets": self.targets,
                "row_ids": self.row_ids,
                "population_id": self.population_id,
                "target_identity": self.target_identity,
                "references": [asdict(r) for r in self.references],
            },
        )


@dataclass(frozen=True, slots=True)
class FittedBinaryLinearClassifier:
    """Retained binary logit; strict positive selects 1, exact zero selects 0."""

    feature_names: tuple[str, ...]
    target_identity: str
    coefficients: tuple[float, ...]
    intercept: float
    training_population_id: str
    training_input_sha256: str
    fitting_execution_id: UUID
    configuration: tuple[tuple[str, str], ...]
    backend_observations: tuple[tuple[str, str], ...]
    references: tuple[EvidenceReference, ...]
    state_id: UUID = field(default_factory=uuid4)
    algorithm: str = field(default="binary-logistic-linear-v1", init=False)
    categories: tuple[int, int] = field(default=(0, 1), init=False)
    threshold: str = field(default="logit>0;exact_zero_negative", init=False)

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if (
            type(self.feature_names) is not tuple
            or not self.feature_names
            or len(set(self.feature_names)) != len(self.feature_names)
        ):
            msg = "unique ordered immutable feature schema required"
            raise ValueError(msg)
        for text in (
            *self.feature_names,
            self.target_identity,
            self.training_population_id,
        ):
            nonempty(text)
        if (
            type(self.coefficients) is not tuple
            or len(self.coefficients) != len(self.feature_names)
            or any(
                type(v) is not float or not math.isfinite(v)
                for v in (*self.coefficients, self.intercept)
            )
        ):
            msg = "one finite binary64 coefficient per coordinate required"
            raise ValueError(msg)
        digest(self.training_input_sha256)
        if self.training_input_sha256 is None:
            msg = "original training fingerprint required"
            raise ValueError(msg)
        if (
            not isinstance(self.state_id, UUID)
            or not isinstance(self.fitting_execution_id, UUID)
            or self.state_id == self.fitting_execution_id
        ):
            msg = "distinct model and fitting occurrence identities required"
            raise ValueError(msg)
        for pairs in (self.configuration, self.backend_observations):
            if (
                type(pairs) is not tuple
                or not pairs
                or any(type(p) is not tuple or len(p) != 2 for p in pairs)
                or (len({p[0] for p in pairs}) != len(pairs))
            ):
                msg = "immutable unique observed key/value pairs required"
                raise ValueError(msg)
            for pair in pairs:
                for value in pair:
                    nonempty(value)
        validate_references(self.references)
        if not self.references:
            msg = "fitting dependencies required"
            raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return _hash(asdict(self))

    def logits(self, features: FeatureTable) -> tuple[float, ...]:
        """Apply the explicit logits contract within this owner."""
        if features.feature_names != self.feature_names or any(
            k is not FeatureValueKind.CONTINUOUS for k in features.feature_value_kinds
        ):
            msg = "incompatible ordered continuous prediction schema"
            raise ValueError(msg)
        scores = tuple(
            math.fsum(
                (
                    self.intercept,
                    *(w * x for w, x in zip(self.coefficients, row, strict=True)),
                ),
            )
            for row in features.rows
        )
        if any(not math.isfinite(v) for v in scores):
            msg = "nonfinite retained logit"
            raise ValueError(msg)
        return scores

    def classify(self, features: FeatureTable) -> tuple[int, ...]:
        """Apply the explicit classify contract within this owner."""
        return tuple(int(value > 0.0) for value in self.logits(features))
