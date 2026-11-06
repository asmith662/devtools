# Copyright (c) 2026
"""Exact finite learning plans over caller-admitted data; no model authority."""

from __future__ import annotations

import json
from dataclasses import dataclass

from devtools.learning.classification.linear import BinaryLinearTraining, _hash
from devtools.learning.integrations.local._codec import (
    array,
    decode_references,
    integer,
)
from devtools.learning.integrations.local._codec import nonempty_text as text
from devtools.learning.integrations.local._codec import retained_object as obj
from devtools.learning.integrations.local.regression.codec import population
from devtools.learning.integrations.local.tables import _table
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.regression.contracts import RegressionPopulation, RegressionRole
from devtools.learning.representation.features import FeatureTable

METHODS = {
    "classification": ("knn7", "square-logistic", "square-margin"),
    "regression": ("mean", "ridge", "knn-v2"),
}
MAX_REQUEST_BYTES = 4 << 20
MAX_PUBLICATION_BYTES = 32 << 20
LEDGER_BYTES = 4 << 20


def canonical(value: object) -> str:
    """Preserve canonical finite JSON without executable/object decoding."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


@dataclass(frozen=True, slots=True)
class BinaryProblem:
    """Original typed binary training and disjoint held-out membership."""

    training: BinaryLinearTraining
    features: FeatureTable
    targets: tuple[int, ...]
    row_ids: tuple[str, ...]
    population_id: str
    source_identity: str


def binary_problem(value: object) -> BinaryProblem:
    """Decode the prepared binary problem with exact original scalar types."""
    d = obj(value)
    if set(d) != {
        "identity",
        "source_identity",
        "training",
        "evaluation_features",
        "evaluation_targets",
        "evaluation_row_ids",
        "evaluation_population_id",
    }:
        msg = "unsupported binary problem fields"
        raise ValueError(msg)
    t = obj(d["training"])
    if set(t) != {
        "features",
        "targets",
        "row_ids",
        "population_id",
        "target_identity",
        "references",
    }:
        msg = "unsupported binary training fields"
        raise ValueError(msg)
    training = BinaryLinearTraining(
        _table(t["features"]),
        tuple(integer(v) for v in array(t["targets"])),
        tuple(text(v) for v in array(t["row_ids"])),
        text(t["population_id"]),
        text(t["target_identity"]),
        decode_references(t["references"]),
    )
    result = BinaryProblem(
        training,
        _table(d["evaluation_features"]),
        tuple(integer(v) for v in array(d["evaluation_targets"])),
        tuple(text(v) for v in array(d["evaluation_row_ids"])),
        text(d["evaluation_population_id"]),
        text(d["source_identity"]),
    )
    if (
        result.features.feature_names != training.features.feature_names
        or result.features.feature_value_kinds != training.features.feature_value_kinds
    ):
        msg = "exact original binary feature schema required"
        raise ValueError(msg)
    if (
        not result.targets
        or len(result.targets) != len(result.row_ids)
        or len(result.targets) != len(result.features.rows)
        or any(v not in (0, 1) for v in result.targets)
        or len(set(result.row_ids)) != len(result.row_ids)
        or set(result.row_ids) & set(training.row_ids)
        or result.population_id == training.population_id
    ):
        msg = "aligned disjoint held-out binary population required"
        raise ValueError(msg)
    return result


@dataclass(frozen=True, slots=True)
class LearningPlan:
    """A source/role/metric/method-bound proposal, without fitting authority."""

    task_identity: str
    family: str
    method: str
    metric: str
    phase: str
    problem_json: str
    source_json: str
    invocation_identity: str

    def __post_init__(self) -> None:
        """Refuse unsupported meanings and bounds before process/backend entry."""
        for value in (self.task_identity, self.invocation_identity):
            text(value)
        if (
            self.family not in METHODS
            or self.method not in METHODS[self.family]
            or self.phase not in ("online", "final")
        ):
            msg = "unsupported learning family, method or role"
            raise ValueError(msg)
        metrics = (
            ("classification.macro_f1:v1", "classification.macro_f1:v2")
            if self.family == "classification"
            else ("regression.mae:v1",)
        )
        if self.metric not in metrics:
            msg = "incompatible family metric"
            raise ValueError(msg)
        if (
            len(self.problem_json.encode()) + len(self.source_json.encode())
            > MAX_REQUEST_BYTES
        ):
            msg = "learning request exceeds its frozen input bound"
            raise ValueError(msg)
        if (
            len(self.problem_json.encode()) + len(self.source_json.encode())
        ) * 24 + 65536 > 16 << 20:
            msg = "source-bound retained-state envelope exceeds the supported codec"
            raise ValueError(
                msg,
            )
        source = obj(json.loads(self.source_json))
        text(source["source_identity"])
        canonical(source)
        training, held = self.populations()
        if self.family == "classification":
            p = binary_problem(json.loads(self.problem_json))
            if p.source_identity != source["source_identity"]:
                msg = "foreign binary source"
                raise ValueError(msg)
        else:
            if not isinstance(training, RegressionPopulation) or not isinstance(
                held,
                RegressionPopulation,
            ):
                msg = "typed quantitative populations required"
                raise TypeError(msg)
            role = (
                RegressionRole.DEVELOPMENT
                if self.phase == "online"
                else RegressionRole.CONFIRMATION
            )
            if (
                training.inputs.role is not RegressionRole.TRAINING
                or held.inputs.role is not role
                or training.inputs.schema_identity != held.inputs.schema_identity
                or training.target != held.target
                or training.inputs.source_identity != held.inputs.source_identity
                or training.inputs.source_identity != source["source_identity"]
                or set(training.inputs.row_ids) & set(held.inputs.row_ids)
                or training.inputs.population_id == held.inputs.population_id
            ):
                msg = "source/schema/unit/target/role correspondence refused"
                raise ValueError(
                    msg,
                )
        features = (
            training.features
            if isinstance(training, BinaryLinearTraining)
            else training.inputs.features
        )
        held_features = (
            held.features if isinstance(held, BinaryProblem) else held.inputs.features
        )
        if (
            not features.rows
            or len(features.rows) > 10000
            or len(held_features.rows) > 10000
            or len(features.feature_names) > 128
            or len(features.rows) * len(features.feature_names) > 1_000_000
        ):
            msg = "learning population/cell bounds exceeded"
            raise ValueError(msg)
        if self.method == "knn7" and len(features.rows) < 7:
            msg = "seven original training rows required"
            raise ValueError(msg)
        if (
            self.method in {"knn7", "knn-v2"}
            and len(features.rows)
            * len(held_features.rows)
            * len(features.feature_names)
            > 5_000_000
        ):
            msg = "bounded independent neighbor inspection work required"
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Bind every declared scientific input and host invocation."""
        return _hash(self.document())

    def document(self) -> dict[str, str]:
        """Return an explicit closed, non-executable wire representation."""
        return {k: getattr(self, k) for k in self.__dataclass_fields__}

    def populations(
        self,
    ) -> (
        tuple[BinaryLinearTraining, BinaryProblem]
        | tuple[RegressionPopulation, RegressionPopulation]
    ):
        """Decode original typed populations without fitting or source acquisition."""
        d = obj(json.loads(self.problem_json))
        if self.family == "classification":
            p = binary_problem(d)
            return p.training, p
        if set(d) != {"training", "evaluation"}:
            msg = "unsupported regression problem fields"
            raise ValueError(msg)
        return population(d["training"]), population(d["evaluation"])


def validate_authorization(plan: LearningPlan, grant: ExecutionAuthorization) -> None:
    """Require the trusted caller's exact plan and singleton method authority."""
    if (
        grant.plan_identity != plan.identity
        or grant.candidate_ids != (plan.method,)
        or grant.authority.relation != "learning_execution_grant-v1"
        or grant.authority.sha256 != plan.identity
    ):
        msg = "exact caller-issued learning grant required"
        raise ValueError(msg)
