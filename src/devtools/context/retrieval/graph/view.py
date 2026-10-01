# Copyright (c) 2026
"""Purpose-specific typed Retrieval graph projected from production RI facts.

This view is ranking structure, not a repository-truth graph. Each edge keeps
the exact native fact and the direction chosen by Retrieval. Graph-1/Graph-2
enumerated neighborhoods; this view supports query-conditioned diffusion.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from enum import Enum
from typing import TYPE_CHECKING

from devtools.context.python.classes.bases import (
    PythonDirectBaseAssessment,
    PythonDirectBaseOutcome,
)
from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    PythonModuleResourceDependency,
    PythonSourceRange,
)
from devtools.context.python.imports.relations import PythonResolvedModuleImportRelation
from devtools.context.python.mirrored_paths import PythonMirroredPathCorrespondence
from devtools.context.python.modules.membership import PythonImmediatePackageMembership
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
    | PythonFunctionDeclarationKnowledge
    | PythonClassDeclarationKnowledge
    | PythonMethodDeclarationKnowledge
    | PythonDirectBaseAssessment
    | PythonImmediatePackageMembership
    | PythonMirroredPathCorrespondence
)
type PythonGraphDeclaration = (
    PythonFunctionDeclarationKnowledge
    | PythonClassDeclarationKnowledge
    | PythonMethodDeclarationKnowledge
)
type PythonGraphReference = (
    PythonFunctionReferenceKnowledge | PythonDeclarationReferenceKnowledge
)


class PythonGraphProjection(Enum):
    """Prospectively fixed Retrieval projections over the same RI substrate."""

    RESOURCE_FORWARD = "resource-forward-v1"
    TYPED_CORE = "typed-core-v1"
    TYPED_NAVIGATION = "typed-navigation-v1"


class PythonGraphNodeKind(Enum):
    """Distinguish observed resource and supported declaration endpoints."""

    RESOURCE = "resource"
    FUNCTION = "module-function"
    CLASS = "module-class"
    METHOD = "direct-method"


@dataclass(frozen=True, slots=True)
class PythonGraphNode:
    """One graph endpoint anchored to an observed resource or RI subject."""

    kind: PythonGraphNodeKind
    identity: str
    resource_address: RepositoryResourceAddress


@dataclass(frozen=True, slots=True)
class PythonGraphEdgeContribution:
    """One native fact supporting one explicitly directed Retrieval transition."""

    family: str
    direction: str
    kind: str
    fact: PythonGraphFact
    weight: float = 1.0


@dataclass(frozen=True, slots=True)
class PythonGraphEdge:
    """Aggregate distinct supports between two typed graph endpoints."""

    source: PythonGraphNode
    target: PythonGraphNode
    contributions: tuple[PythonGraphEdgeContribution, ...]
    weight: float
    transition_probability: float


@dataclass(frozen=True, slots=True)
class PythonGraphView:
    """Snapshot-bound typed nodes, projected transitions, and resource universe."""

    snapshot_id: RepositorySnapshotId
    projection: PythonGraphProjection
    resources: tuple[RepositoryResourceAddress, ...]
    nodes: tuple[PythonGraphNode, ...]
    edges: tuple[PythonGraphEdge, ...]


def build_python_resource_graph_view(
    snapshot: RepositorySnapshot,
    *,
    imports: Sequence[PythonResolvedModuleImportRelation] = (),
    references: Sequence[PythonGraphReference] = (),
) -> PythonGraphView:
    """Reproduce the frozen forward file graph through the canonical builder."""
    return build_python_graph_view(
        snapshot,
        projection=PythonGraphProjection.RESOURCE_FORWARD,
        imports=imports,
        references=references,
    )


def build_python_graph_view(  # noqa: C901, PLR0912, PLR0913, PLR0915
    snapshot: RepositorySnapshot,
    *,
    projection: PythonGraphProjection,
    imports: Sequence[PythonResolvedModuleImportRelation] = (),
    references: Sequence[PythonGraphReference] = (),
    functions: Sequence[PythonFunctionDeclarationKnowledge] = (),
    classes: Sequence[PythonClassDeclarationKnowledge] = (),
    methods: Sequence[PythonMethodDeclarationKnowledge] = (),
    direct_bases: Sequence[PythonDirectBaseAssessment] = (),
    memberships: Sequence[PythonImmediatePackageMembership] = (),
    mirrored_paths: Sequence[PythonMirroredPathCorrespondence] = (),
) -> PythonGraphView:
    """Project specified RI facts without deriving new repository truth.

    The core view follows Imports and resolved References, exposes direct
    lexical containment in both navigation directions, and follows direct
    resolved bases. The navigation variant additionally projects immediate
    package membership and weak mirrored-path correspondence in both directions.
    Every source row is normalized; typed rows first balance active families.
    """
    resource_addresses = tuple(
        sorted((item.address for item in snapshot.resources), key=str),
    )
    resource_nodes = {
        address: PythonGraphNode(
            PythonGraphNodeKind.RESOURCE,
            f"resource:{snapshot.id}:{address}",
            address,
        )
        for address in resource_addresses
    }
    typed = projection is not PythonGraphProjection.RESOURCE_FORWARD
    if not typed and (
        functions or classes or methods or direct_bases or memberships or mirrored_paths
    ):
        msg = "Resource-only projection accepts only Imports and References."
        raise ValueError(msg)
    if projection is PythonGraphProjection.TYPED_CORE and (
        memberships or mirrored_paths
    ):
        msg = "Core projection excludes package and mirrored-path navigation."
        raise ValueError(msg)

    declaration_nodes: dict[str, PythonGraphNode] = {}
    declarations: list[PythonGraphDeclaration] = []
    supplied_declarations: tuple[PythonGraphDeclaration, ...] = (
        *functions,
        *classes,
        *methods,
    )
    for declaration in supplied_declarations:
        _check_declaration(snapshot, declaration)
        node = _declaration_node(declaration)
        if node.identity in declaration_nodes:
            msg = "Graph declaration inputs repeat a structural subject."
            raise ValueError(msg)
        declaration_nodes[node.identity] = node
        declarations.append(declaration)
    class_subjects = {item.subject.identity: item for item in classes}
    for method in methods:
        if (
            class_subjects.get(method.containing_class.subject.identity)
            != method.containing_class
        ):
            msg = "Method's direct containing class is absent from graph inputs."
            raise ValueError(msg)

    grouped: dict[
        tuple[PythonGraphNode, PythonGraphNode],
        dict[str, PythonGraphEdgeContribution],
    ] = {}
    for import_fact in imports:
        if not isinstance(import_fact, PythonResolvedModuleImportRelation):
            msg = "Imports must contain resolved module import relations."
            raise TypeError(msg)
        _check_endpoint(
            snapshot,
            import_fact.source.snapshot_id,
            import_fact.source.resource,
        )
        _check_endpoint(
            snapshot,
            import_fact.target.snapshot_id,
            import_fact.target.resource,
        )
        _add(
            grouped,
            resource_nodes[import_fact.source.resource.address],
            resource_nodes[import_fact.target.resource.address],
            PythonGraphEdgeContribution("import", "forward", "import", import_fact),
        )
    for reference_fact in references:
        if not isinstance(
            reference_fact,
            PythonDeclarationReferenceKnowledge | PythonFunctionReferenceKnowledge,
        ):
            msg = "References must contain supported declaration Reference facts."
            raise TypeError(msg)
        source_occurrence = reference_fact.occurrence
        target_occurrence = reference_fact.target_declaration.support
        _check_address(
            snapshot,
            source_occurrence.snapshot_id,
            source_occurrence.resource_address,
        )
        _check_address(
            snapshot,
            target_occurrence.snapshot_id,
            target_occurrence.resource_address,
        )
        if isinstance(reference_fact, PythonDeclarationReferenceKnowledge):
            _check_endpoint(
                snapshot,
                target_occurrence.snapshot_id,
                reference_fact.target_resource,
            )
        source_node = resource_nodes[source_occurrence.resource_address]
        target_node = resource_nodes[target_occurrence.resource_address]
        if typed:
            target_node = _require_declaration_node(
                declaration_nodes,
                reference_fact.target_declaration,
            )
            source_node = (
                _source_declaration_node(
                    source_occurrence.resource_address,
                    source_occurrence.source_range,
                    declarations,
                    declaration_nodes,
                )
                or source_node
            )
        _add(
            grouped,
            source_node,
            target_node,
            PythonGraphEdgeContribution(
                "reference",
                "source-to-target",
                "direct-call" if reference_fact.direct_call else "reference",
                reference_fact,
            ),
        )
    if typed:
        for declaration in declarations:
            child = _require_declaration_node(declaration_nodes, declaration)
            if isinstance(declaration, PythonMethodDeclarationKnowledge):
                parent = _require_declaration_node(
                    declaration_nodes,
                    declaration.containing_class,
                )
                forward, reverse = "class-to-method", "method-to-class"
            else:
                parent = resource_nodes[declaration.support.resource_address]
                forward, reverse = "resource-to-declaration", "declaration-to-resource"
            _add(
                grouped,
                parent,
                child,
                PythonGraphEdgeContribution(
                    "containment",
                    forward,
                    forward,
                    declaration,
                ),
            )
            _add(
                grouped,
                child,
                parent,
                PythonGraphEdgeContribution(
                    "containment-return",
                    reverse,
                    reverse,
                    declaration,
                ),
            )
        for base_fact in direct_bases:
            if not isinstance(base_fact, PythonDirectBaseAssessment):
                msg = "Direct bases must contain bounded base assessments."
                raise TypeError(msg)
            if (
                base_fact.outcome is not PythonDirectBaseOutcome.RESOLVED
                or base_fact.target is None
            ):
                msg = "Graph direct-base inputs must be positive resolved facts."
                raise ValueError(msg)
            _check_address(
                snapshot,
                base_fact.base.occurrence.snapshot_id,
                base_fact.base.occurrence.resource_address,
            )
            child = _require_declaration_node(declaration_nodes, base_fact.child)
            parent = _require_declaration_node(declaration_nodes, base_fact.target)
            _add(
                grouped,
                child,
                parent,
                PythonGraphEdgeContribution(
                    "direct-base",
                    "child-to-base",
                    "direct-base",
                    base_fact,
                ),
            )
        if projection is PythonGraphProjection.TYPED_NAVIGATION:
            for membership_fact in memberships:
                if not isinstance(membership_fact, PythonImmediatePackageMembership):
                    msg = "Memberships must contain qualified immediate package facts."
                    raise TypeError(msg)
                _check_endpoint(
                    snapshot,
                    membership_fact.child.snapshot_id,
                    membership_fact.child.resource,
                )
                _check_endpoint(
                    snapshot,
                    membership_fact.package.snapshot_id,
                    membership_fact.package.resource,
                )
                package = resource_nodes[membership_fact.package.resource.address]
                child = resource_nodes[membership_fact.child.resource.address]
                for source_node, target_node, direction in (
                    (package, child, "package-to-child"),
                    (child, package, "child-to-package"),
                ):
                    _add(
                        grouped,
                        source_node,
                        target_node,
                        PythonGraphEdgeContribution(
                            "package-membership",
                            direction,
                            direction,
                            membership_fact,
                        ),
                    )
            for mirrored_fact in mirrored_paths:
                if not isinstance(mirrored_fact, PythonMirroredPathCorrespondence):
                    msg = "Mirrored paths must contain exact correspondence facts."
                    raise TypeError(msg)
                if (
                    mirrored_fact.repository_id != snapshot.repository_id
                    or mirrored_fact.snapshot_id != snapshot.id
                ):
                    msg = "Mirrored-path fact belongs to another snapshot."
                    raise ValueError(msg)
                _check_endpoint(
                    snapshot,
                    mirrored_fact.snapshot_id,
                    mirrored_fact.source,
                )
                _check_endpoint(snapshot, mirrored_fact.snapshot_id, mirrored_fact.test)
                source_node = resource_nodes[mirrored_fact.source.address]
                test_node = resource_nodes[mirrored_fact.test.address]
                for origin, destination, direction in (
                    (source_node, test_node, "source-to-mirrored-test"),
                    (test_node, source_node, "test-to-mirrored-source"),
                ):
                    _add(
                        grouped,
                        origin,
                        destination,
                        PythonGraphEdgeContribution(
                            "mirrored-path",
                            direction,
                            direction,
                            mirrored_fact,
                        ),
                    )

    nodes = tuple(resource_nodes[address] for address in resource_addresses) + tuple(
        sorted(
            declaration_nodes.values(),
            key=lambda node: (
                node.kind.value,
                str(node.resource_address),
                node.identity,
            ),
        ),
    )
    position = {node: index for index, node in enumerate(nodes)}
    totals = Counter[PythonGraphNode]()
    family_counts = Counter[tuple[PythonGraphNode, str]]()
    active_families: dict[PythonGraphNode, set[str]] = {}
    for (source, _), grouped_contributions in grouped.items():
        totals[source] += len(grouped_contributions)
        for contribution in grouped_contributions.values():
            family_counts[(source, contribution.family)] += 1
            active_families.setdefault(source, set()).add(contribution.family)
    edges: list[PythonGraphEdge] = []
    for (source, target), raw in sorted(
        grouped.items(),
        key=lambda row: (position[row[0][0]], position[row[0][1]]),
    ):
        edge_contributions = tuple(
            sorted(
                raw.values(),
                key=lambda item: (item.kind, item.direction, item.fact.identity),
            ),
        )
        if typed:
            edge_contributions = tuple(
                replace(
                    item,
                    weight=1
                    / (
                        len(active_families[source])
                        * family_counts[(source, item.family)]
                    ),
                )
                for item in edge_contributions
            )
        weight = sum(item.weight for item in edge_contributions)
        edges.append(
            PythonGraphEdge(
                source,
                target,
                edge_contributions,
                weight,
                weight if typed else weight / totals[source],
            ),
        )
    return PythonGraphView(
        snapshot.id,
        projection,
        resource_addresses,
        nodes,
        tuple(edges),
    )


def _check_declaration(
    snapshot: RepositorySnapshot,
    declaration: PythonGraphDeclaration,
) -> None:
    support = declaration.support
    _check_address(snapshot, support.snapshot_id, support.resource_address)
    resource = snapshot.resource_at(support.resource_address)
    dependency = PythonModuleResourceDependency(
        snapshot.id,
        snapshot.repository_id,
        resource,
    )
    if (
        declaration.subject.snapshot_id != snapshot.id
        or declaration.subject.resource_dependency_identity != dependency.identity
    ):
        msg = "Graph declaration differs from retained snapshot content."
        raise ValueError(msg)


def _declaration_node(declaration: PythonGraphDeclaration) -> PythonGraphNode:
    kind = (
        PythonGraphNodeKind.FUNCTION
        if isinstance(declaration, PythonFunctionDeclarationKnowledge)
        else PythonGraphNodeKind.CLASS
        if isinstance(declaration, PythonClassDeclarationKnowledge)
        else PythonGraphNodeKind.METHOD
    )
    return PythonGraphNode(
        kind,
        f"{kind.value}:{declaration.subject.identity}",
        declaration.support.resource_address,
    )


def _require_declaration_node(
    nodes: dict[str, PythonGraphNode],
    declaration: PythonGraphDeclaration,
) -> PythonGraphNode:
    node = nodes.get(_declaration_node(declaration).identity)
    if node is None:
        msg = "Graph Reference or relation target is absent from declaration inputs."
        raise ValueError(msg)
    return node


def _source_declaration_node(
    resource: RepositoryResourceAddress,
    span: PythonSourceRange,
    declarations: list[PythonGraphDeclaration],
    nodes: dict[str, PythonGraphNode],
) -> PythonGraphNode | None:
    candidates = (
        item
        for item in declarations
        if item.support.resource_address == resource
        and _contains(item.support.source_range, span)
    )
    nearest = min(
        candidates,
        key=lambda item: (
            item.support.source_range.end_line - item.support.source_range.start_line,
            item.support.source_range.end_column_utf8
            - item.support.source_range.start_column_utf8,
            item.subject.identity,
        ),
        default=None,
    )
    return nodes[_declaration_node(nearest).identity] if nearest is not None else None


def _contains(outer: PythonSourceRange, inner: PythonSourceRange) -> bool:
    return (outer.start_line, outer.start_column_utf8) <= (
        inner.start_line,
        inner.start_column_utf8,
    ) and (inner.end_line, inner.end_column_utf8) <= (
        outer.end_line,
        outer.end_column_utf8,
    )


def _add(
    grouped: dict[
        tuple[PythonGraphNode, PythonGraphNode],
        dict[str, PythonGraphEdgeContribution],
    ],
    source: PythonGraphNode,
    target: PythonGraphNode,
    contribution: PythonGraphEdgeContribution,
) -> None:
    if source != target:
        key = (
            f"{contribution.family}:{contribution.direction}:"
            f"{contribution.fact.identity}"
        )
        grouped.setdefault((source, target), {})[key] = contribution
