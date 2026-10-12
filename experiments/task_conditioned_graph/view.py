# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812
"""Reference-only resource projection, retaining native RI facts verbatim."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.python.references.declarations.model import (
    PythonDeclarationReferenceKnowledge,
)
from devtools.context.retrieval.graph.view import _check_declaration
from devtools.context.retrieval.structural import _check_address, _check_endpoint

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True)
class ReferenceEdge:
    """One directed pair, distinct occurrences, sqrt weight and normalized row."""

    source: RepositoryResourceAddress
    target: RepositoryResourceAddress
    references: tuple[PythonDeclarationReferenceKnowledge, ...]
    weight: float
    probability: float


@dataclass(frozen=True)
class ReferenceView:
    """Experiment ranking view over one retained native snapshot."""

    snapshot: RepositorySnapshot
    nodes: tuple[RepositoryResourceAddress, ...]
    edges: tuple[ReferenceEdge, ...]


def build_reference_view(
    snapshot: RepositorySnapshot,
    references: Sequence[PythonDeclarationReferenceKnowledge],
) -> ReferenceView:
    """Project positive resolved native References, including self references.

    No parsing, resolution, paths, reverse edges or other relation families.
    Distinct reference occurrences count once; conflicting facts for the same
    occurrence are rejected rather than converted to ambiguous fan-out.
    """
    nodes = tuple(sorted((r.address for r in snapshot.resources), key=str))
    grouped: dict[
        tuple[RepositoryResourceAddress, RepositoryResourceAddress],
        dict[str, PythonDeclarationReferenceKnowledge],
    ] = {}
    occurrences: dict[tuple[str, str], PythonDeclarationReferenceKnowledge] = {}
    for fact in references:
        if not isinstance(fact, PythonDeclarationReferenceKnowledge):
            raise TypeError("Only active resolved declaration Reference facts accepted")
        occurrence = fact.occurrence
        _check_address(snapshot, occurrence.snapshot_id, occurrence.resource_address)
        _check_declaration(snapshot, fact.target_declaration)
        _check_endpoint(
            snapshot, fact.target_declaration.support.snapshot_id, fact.target_resource
        )
        if (
            fact.target_resource.address
            != fact.target_declaration.support.resource_address
        ):
            raise ValueError("Reference target resource differs from definition owner")
        key = (str(occurrence.resource_address), repr(occurrence.source_range))
        if key in occurrences and occurrences[key] != fact:
            raise ValueError("One occurrence has conflicting native Reference facts")
        occurrences[key] = fact
        pair = (occurrence.resource_address, fact.target_resource.address)
        grouped.setdefault(pair, {})[fact.identity] = fact
    weights = {pair: math.sqrt(len(facts)) for pair, facts in grouped.items()}
    totals = {
        node: math.fsum(
            w for (source, _), w in sorted(weights.items(), key=str) if source == node
        )
        for node in nodes
    }
    edges = tuple(
        ReferenceEdge(
            source,
            target,
            tuple(facts[key] for key in sorted(facts)),
            weights[source, target],
            weights[source, target] / totals[source],
        )
        for (source, target), facts in sorted(
            grouped.items(), key=lambda x: tuple(map(str, x[0]))
        )
    )
    return ReferenceView(snapshot, nodes, edges)


def require_view(snapshot: RepositorySnapshot, view: ReferenceView) -> None:
    """Reconstruct structure/provenance and reject stale or tampered views."""
    if view.snapshot != snapshot or view != build_reference_view(
        snapshot, tuple(f for edge in view.edges for f in edge.references)
    ):
        raise ValueError("Reference view frame/provenance/weight mismatch")
