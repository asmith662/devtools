# Copyright (c) 2026
"""Project exact Python declaration References to distinct referencing resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.association.references import (
    PythonReferenceResourceSupport,
    reference_seed,
    replay_reference_source,
)
from devtools.context.localization.generation.contract import (
    GenerationDisposition,
    MemberProjectionAttempt,
    ProjectedMemberTarget,
)

if TYPE_CHECKING:
    from devtools.context.localization.association.references import (
        PythonReferenceProjectionRequest,
    )
    from devtools.context.localization.generation.contract import GroundedMemberRecipe
    from devtools.context.repository.snapshot import RepositorySnapshot


def project_referencing_resources(
    snapshot: RepositorySnapshot,
    member: GroundedMemberRecipe,
    request: PythonReferenceProjectionRequest,
) -> MemberProjectionAttempt:
    """Enumerate a complete frozen frame or abstain before oversized native work."""
    seed = reference_seed(member.grounding)
    if seed is None:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.UNSUPPORTED_SOURCE,
            None,
            (),
            0,
            work_limit=request.work_limit,
        )
    if len(request.sources) > request.work_limit:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.WORK_BOUND_EXCEEDED,
            seed,
            (),
            0,
            complete=False,
            work_limit=request.work_limit,
            uncovered_frontier=tuple(
                item.analysis.derivation.dependency.resource for item in request.sources
            ),
        )
    targets: list[ProjectedMemberTarget] = []
    for source in request.sources:
        replay_reference_source(source, request, snapshot)
        facts = tuple(
            fact
            for fact in source.analysis.references
            if fact.target_subject == seed.subject and fact.target_declaration == seed
        )
        if facts:
            targets.append(
                ProjectedMemberTarget(
                    source.analysis.derivation.dependency.resource,
                    (
                        PythonReferenceResourceSupport(
                            member.grounding,
                            request,
                            source,
                            facts,
                        ),
                    ),
                ),
            )
    return MemberProjectionAttempt(
        member,
        GenerationDisposition.GENERATED,
        seed,
        tuple(targets),
        len(request.sources),
        work_limit=request.work_limit,
    )
