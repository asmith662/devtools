# Copyright (c) 2026
"""Project one exact source module's direct static imports to dependency resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.association.imports import (
    PythonImportDependencyResourceSupport,
    import_dependency_modules,
    replay_import_dependency_source,
)
from devtools.context.localization.generation.contract import (
    GenerationDisposition,
    MemberProjectionAttempt,
    ProjectedMemberTarget,
)

if TYPE_CHECKING:
    from devtools.context.localization.association.imports import (
        PythonImportDependencyProjectionRequest,
    )
    from devtools.context.localization.generation.contract import GroundedMemberRecipe
    from devtools.context.python.imports.relations import (
        PythonResolvedModuleImportRelation,
    )
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshot


def project_direct_import_dependencies(
    snapshot: RepositorySnapshot,
    member: GroundedMemberRecipe,
    request: PythonImportDependencyProjectionRequest,
) -> MemberProjectionAttempt:
    """Replay one exhaustive source analysis, or retain its uncovered frontier."""
    seed = member.grounding.candidates[0].referent
    modules = import_dependency_modules(member.grounding, request)
    if len(modules) != 1:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.AMBIGUOUS_SOURCE
            if modules
            else GenerationDisposition.UNSUPPORTED_SOURCE,
            seed,
            (),
            0,
            work_limit=request.work_limit,
        )
    source = next((item for item in request.sources if item.module == modules[0]), None)
    if source is None:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.UNSUPPORTED_SOURCE,
            seed,
            (),
            0,
            work_limit=request.work_limit,
            failure_reason="No native import analysis supplied for the source module.",
        )
    if request.work_limit < 1:
        return MemberProjectionAttempt(
            member,
            GenerationDisposition.WORK_BOUND_EXCEEDED,
            seed,
            (),
            0,
            complete=False,
            work_limit=request.work_limit,
            uncovered_frontier=(source.module.resource,),
        )
    relations = replay_import_dependency_source(source, request, snapshot)
    grouped: dict[
        RepositoryResourceOccurrence,
        list[PythonResolvedModuleImportRelation],
    ] = {}
    for relation in relations:
        grouped.setdefault(relation.target.resource, []).append(relation)
    return MemberProjectionAttempt(
        member,
        GenerationDisposition.GENERATED,
        seed,
        tuple(
            ProjectedMemberTarget(
                target,
                (
                    PythonImportDependencyResourceSupport(
                        member.grounding,
                        request,
                        source,
                        tuple(facts),
                    ),
                ),
            )
            for target, facts in grouped.items()
        ),
        1,
        work_limit=request.work_limit,
    )
