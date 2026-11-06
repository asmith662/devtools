# Copyright (c) 2026
from __future__ import annotations

from dataclasses import dataclass

from devtools.learning.measurement.contracts import EvidenceReference, nonempty

BINARY_OBJECTIVE = "supervised-binary-classification-v1"
KNN7 = "knn7_euclidean_uniform_v1"
METRICS = ("classification.macro_f1:v1", "classification.accuracy:v1")


@dataclass(frozen=True, slots=True)
class ExecutionAuthorization:
    """An explicit caller grant bound to one immutable plan and exact subset."""

    plan_identity: str
    candidate_ids: tuple[str, ...]
    authority: EvidenceReference

    def __post_init__(self) -> None:
        if not isinstance(self.authority, EvidenceReference):
            msg = "explicit caller authority reference required"
            raise TypeError(msg)
        if (
            type(self.candidate_ids) is not tuple
            or not self.candidate_ids
            or tuple(sorted(set(self.candidate_ids))) != self.candidate_ids
        ):
            msg = "unique canonical explicitly authorized candidate set required"
            raise ValueError(msg)
        nonempty(self.plan_identity)
