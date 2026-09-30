# Copyright (c) 2026
"""Snapshot-validated navigation over intrinsic function declaration ownership.

Each declaration's existing occurrence and derivation dependency already
establish its direct module-body resource. This view creates no new RI fact.
It does not interpret retrieval relevance or choose Context disclosure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationAnalysisAggregate,
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationContainmentView:
    """Navigate validated direct module-body declarations in either direction."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    aggregate: PythonFunctionDeclarationAnalysisAggregate

    def direct_declarations_in(
        self,
        resource_address: RepositoryResourceAddress,
    ) -> tuple[PythonFunctionDeclarationKnowledge, ...]:
        """Return direct declarations in source order for an analyzed resource.

        An unselected address is an error, not a declaration-free result.
        """
        for analysis in self.aggregate.analyses:
            if analysis.derivation.dependency.resource.address == resource_address:
                return analysis.declarations
        msg = "Resource was not selected for function declaration analysis."
        raise ValueError(msg)

    def containing_resource_of(
        self,
        declaration: PythonFunctionDeclarationKnowledge,
    ) -> RepositoryResourceOccurrence:
        """Return the exact observed resource owning a selected declaration."""
        for analysis in self.aggregate.analyses:
            if declaration in analysis.declarations:
                return analysis.derivation.dependency.resource
        msg = "Declaration does not belong to the selected analyses."
        raise ValueError(msg)


def build_python_function_declaration_containment_view(
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonFunctionDeclarationAnalysisAggregate,
) -> PythonFunctionDeclarationContainmentView:
    """Validate native analyses against retained state and expose navigation.

    This validation checks provenance consistency without reparsing source or
    introducing an independently identified ownership relationship.
    """
    if not aggregate.analyses:
        msg = "Containment requires at least one selected resource analysis."
        raise ValueError(msg)
    seen_addresses: set[RepositoryResourceAddress] = set()
    for analysis in aggregate.analyses:
        derivation = analysis.derivation
        dependency = derivation.dependency
        address = dependency.resource.address
        if address in seen_addresses:
            msg = "Containment repeats a selected resource analysis."
            raise ValueError(msg)
        seen_addresses.add(address)
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
        ):
            msg = "Declaration analysis belongs to another repository snapshot."
            raise ValueError(msg)
        try:
            observed = snapshot.resource_at(address)
        except ValueError as error:
            msg = "Analyzed resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if observed != dependency.resource:
            msg = "Declaration analysis uses stale observed resource content."
            raise ValueError(msg)
        if (
            analysis.coverage.derivation_identity != derivation.identity
            or analysis.coverage.declaration_count != len(analysis.declarations)
        ):
            msg = "Declaration coverage differs from its retained analysis."
            raise ValueError(msg)
        for ordinal, declaration in enumerate(analysis.declarations):
            if (
                declaration.derivation_identity != derivation.identity
                or declaration.subject.snapshot_id != snapshot.id
                or declaration.subject.resource_dependency_identity
                != dependency.identity
                or declaration.subject.derivation_definition_identity
                != derivation.definition.identity
                or declaration.subject.declaration_ordinal != ordinal
                or declaration.support.snapshot_id != snapshot.id
                or declaration.support.resource_address != address
            ):
                msg = "Declaration differs from its resource analysis or support."
                raise ValueError(msg)
    return PythonFunctionDeclarationContainmentView(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        aggregate=aggregate,
    )
