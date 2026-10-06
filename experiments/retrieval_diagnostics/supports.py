# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- qualified native evidence projections
"""Retain native positive support identities without claiming relevance causes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.grounding.contract import (
    AnchorGrounding,
    GroundingResolver,
)
from devtools.context.repository.resource import RepositoryResourceOccurrence
from experiments.retrieval_diagnostics.models import LaneCapture, SupportReference

if TYPE_CHECKING:
    from devtools.context.localization.roles.models import ResourceRoleEvidence
    from devtools.context.retrieval.structural import (
        PythonDirectStructuralResourceCandidate,
    )


def structural(
    capture: LaneCapture, candidate: PythonDirectStructuralResourceCandidate
) -> tuple[SupportReference, ...]:
    """Attach existing direct RI supports from a snapshot-qualified candidate."""
    resource = next(
        (r for r in capture.resources if r.address == candidate.resource_address), None
    )
    if candidate.snapshot_id != capture.frame.snapshot or resource is None:
        raise ValueError("Structural support frame differs.")
    return tuple(
        SupportReference(
            capture.frame,
            resource,
            "STRUCTURAL",
            s.fact.identity,
            s.direction + ":" + s.seed_resource.value,
        )
        for s in candidate.supports
    )


def role(capture: LaneCapture, evidence: ResourceRoleEvidence) -> SupportReference:
    """Attach a native soft role identity; roles never become relevance labels."""
    if (
        evidence.repository_id != capture.frame.repository
        or evidence.snapshot_id != capture.frame.snapshot
        or evidence.resource not in capture.resources
    ):
        raise ValueError("Role support frame differs.")
    return SupportReference(
        capture.frame,
        evidence.resource,
        "ROLE",
        evidence.identity,
        evidence.role.value + ":" + evidence.derivation_identity,
    )


def exact_resource(
    capture: LaneCapture, grounding: AnchorGrounding
) -> tuple[SupportReference, ...]:
    """Attach exact resource lookup evidence; other symbolic resolvers stay native."""
    if (
        grounding.request.repository_id != capture.frame.repository
        or grounding.request.snapshot_id != capture.frame.snapshot
        or grounding.resolver is not GroundingResolver.SNAPSHOT_RESOURCE_AT
    ):
        raise ValueError("Exact resource support scope differs.")
    resources = tuple(
        c.referent
        for c in grounding.candidates
        if isinstance(c.referent, RepositoryResourceOccurrence)
    )
    if any(r not in capture.resources for r in resources):
        raise ValueError("Exact referent is outside capture.")
    return tuple(
        SupportReference(
            capture.frame,
            r,
            "EXACT",
            r.address.value + ":" + r.content_identity.value,
            grounding.resolver.value + ":" + grounding.disposition.value,
        )
        for r in resources
    )
