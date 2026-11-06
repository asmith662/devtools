# Copyright (c) 2026
"""Immutable binary L2 squared-hinge state with backend-free margin inference.

The separate logistic classifier retains its original objective/logit meaning.
Coefficients do not imply a universal model type or calibrated probability.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from uuid import UUID, uuid4

from devtools.learning.measurement.contracts import EvidenceReference, digest, nonempty
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
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
class FittedMarginClassifier:
    """Retained squared-hinge margin; strict positive selects 1, zero selects 0."""

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
    algorithm: str = field(default="binary-l2-squared-hinge-linear-v1", init=False)
    categories: tuple[int, int] = field(default=(0, 1), init=False)
    threshold: str = field(default="margin>0;exact_zero_negative", init=False)
    objective: str = field(
        default="0.5*(||w||^2+(b/intercept_scaling)^2)+C*sum(max(0,1-y_signed*margin)^2)",
        init=False,
    )
    score_meaning: str = field(
        default="signed_linear_margin;not_logit_or_probability",
        init=False,
    )

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
        observed = dict(self.configuration)
        if observed.get("penalty") != "l2" or observed.get("loss") != "squared_hinge":
            msg = "configuration contradicts the retained margin objective"
            raise ValueError(msg)
        validate_references(self.references)
        if not self.references:
            msg = "fitting dependencies required"
            raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return _hash(asdict(self))

    def margins(self, features: FeatureTable) -> tuple[float, ...]:
        """Apply the explicit margins contract within this owner."""
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
            msg = "nonfinite retained margin"
            raise ValueError(msg)
        return scores

    def classify(self, features: FeatureTable) -> tuple[int, ...]:
        """Apply the explicit classify contract within this owner."""
        return tuple(int(value > 0.0) for value in self.margins(features))
