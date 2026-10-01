# Copyright (c) 2026
# ruff: noqa: COM812
"""Forward resource dependency view projected from qualified production RI.

This is retrieval structure for a ranking purpose, not repository relationship
truth. Graph-1/Graph-2 enumerated reachable paths; this view carries weighted
transitions for query-conditioned diffusion and never enumerates paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.imports.relations import PythonResolvedModuleImportRelation
from devtools.context.python.references.analysis import PythonFunctionReferenceKnowledge
from devtools.context.python.references.declarations.model import (
    PythonDeclarationReferenceKnowledge,
)
from devtools.context.retrieval.structural import _check_address, _check_endpoint

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

type PythonGraphFact = (
    PythonResolvedModuleImportRelation
    | PythonFunctionReferenceKnowledge
    | PythonDeclarationReferenceKnowledge
)


@dataclass(frozen=True, slots=True)
class PythonGraphEdgeContribution:
    """One distinct RI fact supporting a forward dependency transition."""

    kind: str
    fact: PythonGraphFact
    weight: float


@dataclass(frozen=True, slots=True)
class PythonResourceGraphEdge:
    """Aggregate independently supported source-to-target dependencies."""

    source: RepositoryResourceAddress
    target: RepositoryResourceAddress
    contributions: tuple[PythonGraphEdgeContribution, ...]
    weight: float
    transition_probability: float


@dataclass(frozen=True, slots=True)
class PythonResourceGraphView:
    """Snapshot-bound resource nodes and forward RI transitions for retrieval."""

    snapshot_id: RepositorySnapshotId
    resources: tuple[RepositoryResourceAddress, ...]
    edges: tuple[PythonResourceGraphEdge, ...]

    PROJECTION: ClassVar[str] = (
        "python-forward-import-reference-resource-view-equal-fact-v1"
    )


def build_python_resource_graph_view(
    snapshot: RepositorySnapshot,
    *,
    imports: Sequence[PythonResolvedModuleImportRelation] = (),
    references: Sequence[
        PythonDeclarationReferenceKnowledge | PythonFunctionReferenceKnowledge
    ] = (),
) -> PythonResourceGraphView:
    """Project forward Import and Reference/Call facts, excluding self edges.

    Call is one tagged Reference, counted once. Package containment and reverse
    dependencies remain available to direct retrieval, but are not diffusion
    transitions: neither asserts that a sibling or dependent is query relevant.
    Equal weight per distinct fact is an untuned baseline; outgoing normalization
    bounds high-degree sources. Missing fact families imply no negative knowledge.
    """
    grouped: dict[
        tuple[RepositoryResourceAddress, RepositoryResourceAddress],
        dict[str, PythonGraphEdgeContribution],
    ] = {}
    for fact in imports:
        if not isinstance(fact, PythonResolvedModuleImportRelation):
            msg = "Imports must contain resolved module import relations."
            raise TypeError(msg)
        _check_endpoint(snapshot, fact.source.snapshot_id, fact.source.resource)
        _check_endpoint(snapshot, fact.target.snapshot_id, fact.target.resource)
        _add(
            grouped,
            fact.source.resource.address,
            fact.target.resource.address,
            PythonGraphEdgeContribution("import", fact, 1.0),
        )
    for reference_fact in references:
        if not isinstance(
            reference_fact,
            PythonDeclarationReferenceKnowledge | PythonFunctionReferenceKnowledge,
        ):
            msg = "References must contain supported declaration reference knowledge."
            raise TypeError(msg)
        reference_source = reference_fact.occurrence
        target = reference_fact.target_declaration.support
        _check_address(
            snapshot, reference_source.snapshot_id, reference_source.resource_address
        )
        _check_address(snapshot, target.snapshot_id, target.resource_address)
        if isinstance(reference_fact, PythonDeclarationReferenceKnowledge):
            _check_endpoint(
                snapshot,
                target.snapshot_id,
                reference_fact.target_resource,
            )
        _add(
            grouped,
            reference_source.resource_address,
            target.resource_address,
            PythonGraphEdgeContribution(
                "direct-call" if reference_fact.direct_call else "reference",
                reference_fact,
                1.0,
            ),
        )

    totals: dict[RepositoryResourceAddress, float] = {}
    for (source, _target), contributions in grouped.items():
        totals[source] = totals.get(source, 0.0) + sum(
            item.weight for item in contributions.values()
        )
    edges = tuple(
        PythonResourceGraphEdge(
            source=source,
            target=target,
            contributions=tuple(
                sorted(
                    contributions.values(),
                    key=lambda item: (item.kind, item.fact.identity),
                )
            ),
            weight=sum(item.weight for item in contributions.values()),
            transition_probability=sum(item.weight for item in contributions.values())
            / totals[source],
        )
        for (source, target), contributions in sorted(
            grouped.items(),
            key=lambda item: (str(item[0][0]), str(item[0][1])),
        )
    )
    return PythonResourceGraphView(
        snapshot_id=snapshot.id,
        resources=tuple(sorted((item.address for item in snapshot.resources), key=str)),
        edges=edges,
    )


def _add(
    grouped: dict[
        tuple[RepositoryResourceAddress, RepositoryResourceAddress],
        dict[str, PythonGraphEdgeContribution],
    ],
    source: RepositoryResourceAddress,
    target: RepositoryResourceAddress,
    contribution: PythonGraphEdgeContribution,
) -> None:
    if source != target:
        grouped.setdefault((source, target), {})[contribution.fact.identity] = (
            contribution
        )
