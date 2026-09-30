# Copyright (c) 2026
"""Snapshot-bound inventory of native lexical and direct structural retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from devtools.context.retrieval.structural import (
        PythonDirectStructuralResourceEvidence,
        PythonDirectStructuralRetrievalResult,
    )


@dataclass(frozen=True, slots=True)
class LexicalStructuralResourceEntry:
    """Correlate native supports for one resource in one explicit snapshot."""

    snapshot_id: RepositorySnapshotId
    resource: RepositoryResourceOccurrence
    lexical_rank: int | None
    lexical_match: RepositoryTextLexicalBm25Match | None
    structural_supports: tuple[PythonDirectStructuralResourceEvidence, ...]


@dataclass(frozen=True, slots=True)
class LexicalStructuralResourceInventory:
    """Retain a purpose and both native retrieval results without selection."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    structural_result: PythonDirectStructuralRetrievalResult
    resources: tuple[LexicalStructuralResourceEntry, ...]

    COMPOSITION_SEMANTICS: ClassVar[str] = (
        "snapshot-bound-lexical-direct-structural-resource-inventory-v1"
    )


def compose_lexical_structural_resource_evidence(  # noqa: C901
    snapshot: RepositorySnapshot,
    *,
    purpose: str,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
    structural_result: PythonDirectStructuralRetrievalResult,
) -> LexicalStructuralResourceInventory:
    """Correlate native matches and supports under one caller-owned invocation.

    Address order is a neutral inventory order, not a relevance ranking. The
    lexical query remains mechanism input and need not equal the purpose.
    """
    if not purpose.strip():
        msg = "Resource evidence composition requires a nonempty purpose."
        raise ValueError(msg)
    if structural_result.snapshot_id != snapshot.id or (
        structural_result.request.purpose != purpose
    ):
        msg = "Structural retrieval differs from the composition snapshot or purpose."
        raise ValueError(msg)

    require_lexical_result_snapshot(snapshot, lexical_result)

    statistics = lexical_result.index.corpus_statistics.document_statistics

    lexical_by_address: dict[
        RepositoryResourceAddress,
        tuple[int, RepositoryTextLexicalBm25Match],
    ] = {}
    for rank, match in enumerate(lexical_result.matches, start=1):
        if not any(match.document_statistics is item for item in statistics):
            msg = "Lexical match is absent from its retrieval index."
            raise ValueError(msg)
        address = match.document_statistics.analysis.document.resource.address
        previous = lexical_by_address.get(address)
        if previous is not None and previous[1] != match:
            msg = "Lexical retrieval has conflicting matches for one resource."
            raise ValueError(msg)
        if previous is None:
            lexical_by_address[address] = (rank, match)

    structural_by_address: dict[
        RepositoryResourceAddress,
        list[PythonDirectStructuralResourceEvidence],
    ] = {}
    structural_seen: dict[
        RepositoryResourceAddress,
        set[tuple[RepositoryResourceAddress, str, str]],
    ] = {}
    for candidate in structural_result.candidates:
        if candidate.snapshot_id != snapshot.id:
            msg = "Structural candidate belongs to another snapshot."
            raise ValueError(msg)
        snapshot.resource_at(candidate.resource_address)
        for support in candidate.supports:
            key = (support.seed_resource, support.direction, support.fact.identity)
            seen = structural_seen.setdefault(candidate.resource_address, set())
            if key not in seen:
                seen.add(key)
                structural_by_address.setdefault(candidate.resource_address, []).append(
                    support,
                )

    addresses = sorted(
        lexical_by_address.keys() | structural_by_address.keys(),
        key=str,
    )
    resources: list[LexicalStructuralResourceEntry] = []
    for address in addresses:
        lexical = lexical_by_address.get(address)
        resources.append(
            LexicalStructuralResourceEntry(
                snapshot_id=snapshot.id,
                resource=snapshot.resource_at(address),
                lexical_rank=lexical[0] if lexical is not None else None,
                lexical_match=lexical[1] if lexical is not None else None,
                structural_supports=tuple(structural_by_address.get(address, ())),
            ),
        )
    return LexicalStructuralResourceInventory(
        snapshot_id=snapshot.id,
        purpose=purpose,
        lexical_result=lexical_result,
        structural_result=structural_result,
        resources=tuple(resources),
    )


def require_lexical_result_snapshot(
    snapshot: RepositorySnapshot,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
) -> None:
    """Validate the entire retained lexical corpus against one snapshot."""
    collection = (
        lexical_result.index.corpus_statistics.collection_analysis.document_collection
    )
    if collection.corpus.definition.discovery.repository_id != snapshot.repository_id:
        msg = "Lexical corpus belongs to another repository."
        raise ValueError(msg)
    if collection.corpus.resources != tuple(
        document.resource for document in collection.documents
    ):
        msg = "Lexical documents differ from their observed corpus."
        raise ValueError(msg)
    for document in collection.documents:
        if document.repository_id != snapshot.repository_id:
            msg = "Lexical document belongs to another repository."
            raise ValueError(msg)
        _require_snapshot_resource(snapshot, document.resource)

    statistics = lexical_result.index.corpus_statistics.document_statistics
    if tuple(item.analysis.document for item in statistics) != collection.documents:
        msg = "Lexical index statistics differ from its document collection."
        raise ValueError(msg)


def _require_snapshot_resource(
    snapshot: RepositorySnapshot,
    resource: RepositoryResourceOccurrence,
) -> None:
    try:
        current = snapshot.resource_at(resource.address)
    except ValueError as error:
        msg = "Lexical corpus resource is absent from the supplied snapshot."
        raise ValueError(msg) from error
    if current != resource:
        msg = "Lexical corpus resource differs from the supplied snapshot."
        raise ValueError(msg)
