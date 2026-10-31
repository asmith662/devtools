# Copyright (c) 2026
# ruff: noqa: E501 -- finite operational receipts and formatter compatibility
"""Assess information availability through Localization and exact Context evidence."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from devtools.context import RepositoryResourceAddress
from devtools.context.localization import (
    Disposition,
    LocalizationAssessment,
    LocalizationEvidenceReference,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    RequirementStatus,
    SatisfactionCriterion,
    SupportedWitness,
    TaskProvenance,
    WitnessSet,
    assess_localization_readiness,
)

if TYPE_CHECKING:
    from devtools.context.planning.source import SourceRangeDisclosureOption
    from devtools.context.repository.snapshot import RepositorySnapshot


def assess(
    task: dict[str, Any],
    identity: str,
    snapshot: RepositorySnapshot,
    available: tuple[SourceRangeDisclosureOption, ...],
) -> dict[str, Any]:
    """Judge only the explicitly approved whole-current-resource criterion.

    This says information is available, never that the behavioral repair is right.
    Each new candidate snapshot receives a new assessment with its exact evidence.
    """
    task_id = LocalizationTaskIdentity(identity)
    provenance = TaskProvenance(identity, explanation="Host-approved native packet")
    obligations, assessments = [], []
    for row in task["obligations"]:
        resource = snapshot.resource_at(RepositoryResourceAddress(row["path"]))
        obligation = LocalizationObligation(
            LocalizationObligationIdentity(task_id, row["name"]),
            row["predicate"],
            (),
            provenance,
            RequirementStatus.MANDATORY,
            SatisfactionCriterion(
                row["criterion"],
                "Exact current whole-resource text available for inspection",
            ),
            (WitnessSet((resource,)),),
        )
        supports = tuple(
            LocalizationEvidenceReference(
                o.identity,
                snapshot.repository_id,
                snapshot.id,
            )
            for o in available
            if o.snapshot_id == snapshot.id
            and o.unit.resource == resource
            and o.span == (0, len(resource.content))
            and not o.truncated
        )
        obligations.append(obligation)
        assessments.append(
            LocalizationAssessment(
                obligation.identity,
                snapshot.repository_id,
                snapshot.id,
                Disposition.RESOLVED if supports else Disposition.OPEN,
                supported_witnesses=(SupportedWitness(resource, supports),)
                if supports
                else (),
            ),
        )
    interpreted = LocalizationTaskInterpretation(
        task_id,
        provenance,
        (),
        tuple(obligations),
    )
    result = assess_localization_readiness(
        task=interpreted,
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        assessments=assessments,
    )
    return {
        "snapshot": str(snapshot.id),
        "repository": str(snapshot.repository_id),
        "ready": result.is_ready,
        "unresolved": [o.value for o in result.unresolved_mandatory],
        "evidence": [o.identity for o in available],
        "scope": "Information availability only; supplied frame is not claimed exhaustive",
    }
