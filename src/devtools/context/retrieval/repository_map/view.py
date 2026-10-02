# Copyright (c) 2026
"""Dependency-only structural view and declaration metadata for repository maps."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
)
from devtools.context.retrieval.graph.pagerank import require_graph_view_snapshot
from devtools.context.retrieval.graph.view import (
    PythonGraphEdge,
    PythonGraphNodeKind,
    PythonGraphProjection,
    _check_declaration,
    _declaration_node,
)

if TYPE_CHECKING:
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.graph.view import (
        PythonGraphDeclaration,
        PythonGraphEdgeContribution,
        PythonGraphNode,
        PythonGraphView,
    )


@dataclass(frozen=True, slots=True)
class RepositoryMapSymbol:
    """Existing RI subject, exact support, and legitimate lexical parent name."""

    node: PythonGraphNode
    declaration: PythonGraphDeclaration
    qualified_name: str


@dataclass(frozen=True, slots=True)
class RepositoryMapView:
    """Retain canonical typed RI projection alongside importance transitions."""

    core: PythonGraphView
    dependencies: PythonGraphView
    symbols: tuple[RepositoryMapSymbol, ...]


def build_repository_map_view(
    snapshot: RepositorySnapshot,
    *,
    core: PythonGraphView,
) -> RepositoryMapView:
    """Remove outward containment flow, retaining owner return and dependencies.

    Import, Reference, direct-base, and containment-return families each receive
    equal row capacity when active. Unique native supports divide their family's
    capacity. Membership and path correspondence are navigation, not importance.
    """
    require_graph_view_snapshot(snapshot, core)
    if core.projection is not PythonGraphProjection.TYPED_CORE:
        msg = "Repository map requires a canonical typed core projection."
        raise ValueError(msg)
    declarations = {
        contribution.fact.subject.identity: contribution.fact
        for edge in core.edges
        for contribution in edge.contributions
        if contribution.family == "containment"
        and isinstance(
            contribution.fact,
            PythonFunctionDeclarationKnowledge
            | PythonClassDeclarationKnowledge
            | PythonMethodDeclarationKnowledge,
        )
    }
    symbols = []
    for declaration in declarations.values():
        _check_declaration(snapshot, declaration)
        node = _declaration_node(declaration)
        name = declaration.declared_name
        if isinstance(declaration, PythonMethodDeclarationKnowledge):
            name = f"{declaration.containing_class.declared_name}.{name}"
        symbols.append(RepositoryMapSymbol(node, declaration, name))
    expected = {node for node in core.nodes if node.kind.value != "resource"}
    if {item.node for item in symbols} != expected:
        msg = "Repository map declarations differ from typed graph subjects."
        raise ValueError(msg)
    resources = {
        node.resource_address: node
        for node in core.nodes
        if node.kind is PythonGraphNodeKind.RESOURCE
    }
    grouped: dict[
        tuple[PythonGraphNode, PythonGraphNode],
        list[PythonGraphEdgeContribution],
    ] = {}
    for edge in core.edges:
        for item in edge.contributions:
            if item.family == "containment":
                continue
            source = (
                resources[edge.source.resource_address]
                if item.family in {"reference", "direct-base"}
                else edge.source
            )
            grouped.setdefault((source, edge.target), []).append(item)
    positions = {node: index for index, node in enumerate(core.nodes)}
    edges = tuple(
        PythonGraphEdge(source, target, tuple(items), 1.0, 1.0)
        for (source, target), items in sorted(
            grouped.items(),
            key=lambda row: (positions[row[0][0]], positions[row[0][1]]),
        )
    )
    counts = Counter(
        (edge.source, item.family) for edge in edges for item in edge.contributions
    )
    families: dict[PythonGraphNode, set[str]] = {}
    for source, family in counts:
        families.setdefault(source, set()).add(family)
    normalized = []
    for edge in edges:
        contributions = tuple(
            replace(
                item,
                weight=1
                / (len(families[edge.source]) * counts[edge.source, item.family]),
            )
            for item in edge.contributions
        )
        weight = sum(item.weight for item in contributions)
        normalized.append(
            replace(
                edge,
                contributions=contributions,
                weight=weight,
                transition_probability=weight,
            ),
        )
    return RepositoryMapView(
        core,
        replace(core, edges=tuple(normalized)),
        tuple(sorted(symbols, key=lambda item: item.node.identity)),
    )
