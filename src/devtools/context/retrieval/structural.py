# Copyright (c) 2026
"""Direct, purpose-relative resource projection over established Python RI facts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Literal

from devtools.context.python.imports.relations import PythonResolvedModuleImportRelation
from devtools.context.python.modules.membership import PythonImmediatePackageMembership
from devtools.context.python.references.analysis import PythonFunctionReferenceKnowledge

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

type PythonDirectStructuralFact = (
    PythonResolvedModuleImportRelation
    | PythonFunctionReferenceKnowledge
    | PythonImmediatePackageMembership
)
type PythonDirectStructuralDirection = Literal[
    "import-to-target",
    "import-to-source",
    "reference-to-definition",
    "definition-to-reference",
    "child-to-package",
    "package-to-child",
]


@dataclass(frozen=True, slots=True)
class PythonDirectStructuralRetrievalRequest:
    """Carry one information purpose and caller-selected resource anchors."""

    purpose: str
    seed_resources: tuple[RepositoryResourceAddress, ...]

    def __post_init__(self) -> None:
        """Require an explicit purpose and a nonempty, distinct seed set."""
        if not self.purpose.strip():
            msg = "Direct structural retrieval requires a nonempty purpose."
            raise ValueError(msg)
        if not self.seed_resources or len(set(self.seed_resources)) != len(
            self.seed_resources,
        ):
            msg = "Direct structural retrieval requires distinct seed resources."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class PythonDirectStructuralResourceEvidence:
    """Retain one seed, direction, and exact RI fact supporting a resource."""

    seed_resource: RepositoryResourceAddress
    direction: PythonDirectStructuralDirection
    fact: PythonDirectStructuralFact

    MECHANISM: ClassVar[str] = "direct-python-ri-resource-projection-v1"


@dataclass(frozen=True, slots=True)
class PythonDirectStructuralResourceCandidate:
    """Group independent direct supports for one snapshot resource occurrence."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    supports: tuple[PythonDirectStructuralResourceEvidence, ...]


@dataclass(frozen=True, slots=True)
class PythonDirectStructuralRetrievalResult:
    """Retain the request, snapshot, and candidates in first-support order."""

    request: PythonDirectStructuralRetrievalRequest
    snapshot_id: RepositorySnapshotId
    candidates: tuple[PythonDirectStructuralResourceCandidate, ...]


def retrieve_python_direct_structural_resources(  # noqa: C901, PLR0912
    snapshot: RepositorySnapshot,
    *,
    request: PythonDirectStructuralRetrievalRequest,
    imports: Sequence[PythonResolvedModuleImportRelation] = (),
    references: Sequence[PythonFunctionReferenceKnowledge] = (),
    memberships: Sequence[PythonImmediatePackageMembership] = (),
) -> PythonDirectStructuralRetrievalResult:
    """Project supplied positive RI facts one relation away from each seed.

    Inputs are already-derived facts. Missing facts establish no negative claim;
    this operation neither derives relations nor selects or ranks candidates.
    """
    for seed in request.seed_resources:
        snapshot.resource_at(seed)

    pairs: list[
        tuple[
            RepositoryResourceAddress,
            RepositoryResourceAddress,
            PythonDirectStructuralDirection,
            PythonDirectStructuralDirection,
            PythonDirectStructuralFact,
        ]
    ] = []
    for import_fact in imports:
        if not isinstance(import_fact, PythonResolvedModuleImportRelation):
            msg = "Imports must contain resolved module import relations."
            raise TypeError(msg)
        _check_endpoint(
            snapshot, import_fact.source.snapshot_id, import_fact.source.resource,
        )
        _check_endpoint(
            snapshot, import_fact.target.snapshot_id, import_fact.target.resource,
        )
        pairs.append(
            (
                import_fact.source.resource.address,
                import_fact.target.resource.address,
                "import-to-target",
                "import-to-source",
                import_fact,
            ),
        )
    for reference_fact in references:
        if not isinstance(reference_fact, PythonFunctionReferenceKnowledge):
            msg = "References must contain qualified function reference knowledge."
            raise TypeError(msg)
        reference_source = reference_fact.occurrence
        definition = reference_fact.target_declaration.support
        _check_address(
            snapshot, reference_source.snapshot_id, reference_source.resource_address,
        )
        _check_address(snapshot, definition.snapshot_id, definition.resource_address)
        pairs.append(
            (
                reference_source.resource_address,
                definition.resource_address,
                "reference-to-definition",
                "definition-to-reference",
                reference_fact,
            ),
        )
    for membership_fact in memberships:
        if not isinstance(membership_fact, PythonImmediatePackageMembership):
            msg = "Memberships must contain immediate package membership facts."
            raise TypeError(msg)
        _check_endpoint(
            snapshot, membership_fact.child.snapshot_id, membership_fact.child.resource,
        )
        _check_endpoint(
            snapshot,
            membership_fact.package.snapshot_id,
            membership_fact.package.resource,
        )
        pairs.append(
            (
                membership_fact.child.resource.address,
                membership_fact.package.resource.address,
                "child-to-package",
                "package-to-child",
                membership_fact,
            ),
        )

    grouped: dict[
        RepositoryResourceAddress,
        list[PythonDirectStructuralResourceEvidence],
    ] = {}
    seen: set[
        tuple[RepositoryResourceAddress, PythonDirectStructuralDirection, str]
    ] = set()
    for seed in request.seed_resources:
        for source_address, target_address, forward, reverse, fact in pairs:
            if source_address == target_address:
                continue
            if seed == source_address:
                candidate, direction = target_address, forward
            elif seed == target_address:
                candidate, direction = source_address, reverse
            else:
                continue
            key = (seed, direction, fact.identity)
            if key not in seen:
                seen.add(key)
                grouped.setdefault(candidate, []).append(
                    PythonDirectStructuralResourceEvidence(seed, direction, fact),
                )
    return PythonDirectStructuralRetrievalResult(
        request=request,
        snapshot_id=snapshot.id,
        candidates=tuple(
            PythonDirectStructuralResourceCandidate(
                snapshot.id,
                address,
                tuple(supports),
            )
            for address, supports in grouped.items()
        ),
    )


def _check_endpoint(
    snapshot: RepositorySnapshot,
    snapshot_id: RepositorySnapshotId,
    resource: RepositoryResourceOccurrence,
) -> None:
    if snapshot_id != snapshot.id or snapshot.resource_at(resource.address) != resource:
        msg = "Structural fact endpoint does not belong to the supplied snapshot."
        raise ValueError(msg)


def _check_address(
    snapshot: RepositorySnapshot,
    snapshot_id: RepositorySnapshotId,
    address: RepositoryResourceAddress,
) -> None:
    if snapshot_id != snapshot.id:
        msg = "Structural fact endpoint does not belong to the supplied snapshot."
        raise ValueError(msg)
    snapshot.resource_at(address)
