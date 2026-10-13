# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- bounded experiment-only evidence projection
"""Annotate unchanged native lexical matches with direct forward References.

No query scoring, RI derivation, candidate acquisition or ranking implementation.
Inputs must come from authenticated capture construction. Native structural
support values are reused; this is not a universal CandidateEvidence schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.python.references import PythonDeclarationReferenceKnowledge
from devtools.context.retrieval.composition import require_lexical_result_snapshot
from devtools.context.retrieval.graph.view import _check_declaration
from devtools.context.retrieval.structural import (
    PythonDirectStructuralResourceEvidence,
    _check_address,
    _check_endpoint,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        LocalizationQueryIdentity,
    )
    from devtools.context.repository.document import RepositoryTextDocumentId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )


@dataclass(frozen=True, slots=True)
class SupportingSource:
    """One stronger native A candidate and all distinct forward occurrences."""

    resource: RepositoryResourceOccurrence
    document_id: RepositoryTextDocumentId
    a_rank: int
    supports: tuple[PythonDirectStructuralResourceEvidence, ...]


@dataclass(frozen=True, slots=True)
class TargetAnnotation:
    """Inspect direct support and an unexecuted one-position comparison."""

    resource: RepositoryResourceOccurrence
    document_id: RepositoryTextDocumentId
    a_rank: int
    sources: tuple[SupportingSource, ...]
    predecessor: RepositoryResourceOccurrence
    predecessor_document_id: RepositoryTextDocumentId

    @property
    def distinct_source_count(self) -> int:
        """Count sources without interpreting count as relevance."""
        return len(self.sources)

    @property
    def occurrence_count(self) -> int:
        """Count distinct authenticated native occurrences, never duplicate input."""
        return sum(len(s.supports) for s in self.sources)

    @property
    def best_source_rank(self) -> int:
        """Expose the strongest source's original lexical rank."""
        return min(s.a_rank for s in self.sources)


@dataclass(frozen=True, slots=True)
class AnnotatedLexicalSurface:
    """An obligation-relative evidence annotation, with A retained verbatim."""

    obligation: LocalizationObligationIdentity
    query: LocalizationQueryIdentity
    purpose: str
    snapshot: RepositorySnapshot
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    annotations: tuple[TargetAnnotation, ...]


@dataclass(frozen=True, slots=True)
class PreparedReferences:
    """Snapshot-owned, query-independent native identities authenticated once.

    This invocation-local preparation is never persisted as reusable trust. Future
    capture proof binds its input facts and construction implementation. Cached
    identities avoid recursively hashing RI universes during warm annotation.
    """

    snapshot: RepositorySnapshot
    facts: tuple[PythonDeclarationReferenceKnowledge, ...]

    @property
    def self_reference_count(self) -> int:
        """Expose a descriptive count that cannot affect support eligibility."""
        return sum(
            f.occurrence.resource_address == f.target_resource.address
            for f in self.facts
        )


def prepare_references(
    snapshot: RepositorySnapshot,
    references: Sequence[PythonDeclarationReferenceKnowledge],
) -> PreparedReferences:
    """Check exact native type/frame/occurrence conflicts, not rederive RI truth."""
    unique: dict[str, PythonDeclarationReferenceKnowledge] = {}
    occurrences: dict[tuple[str, str], PythonDeclarationReferenceKnowledge] = {}
    for fact in references:
        if not isinstance(fact, PythonDeclarationReferenceKnowledge):
            raise TypeError("Only positive native declaration References are eligible")
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
            raise ValueError("Reference target differs from declaration owner")
        key = (str(occurrence.resource_address), repr(occurrence.source_range))
        if key in occurrences and occurrences[key] != fact:
            raise ValueError("Conflicting native facts for one occurrence")
        identity = fact.identity
        if identity in unique and unique[identity] != fact:
            raise ValueError("Conflicting native fact identity")
        unique[identity] = fact
        occurrences[key] = fact
    return PreparedReferences(snapshot, tuple(unique[key] for key in sorted(unique)))


def annotate(
    prepared: PreparedReferences,
    *,
    obligation: LocalizationObligationIdentity,
    query: LocalizationQueryIdentity,
    purpose: str,
    lexical_result: RepositoryTextLexicalBm25RetrievalResult,
) -> AnnotatedLexicalSurface:
    """Keep A exactly; allow only same-lane stronger-source -> target evidence."""
    if not purpose.strip() or query.task != obligation.task:
        raise ValueError("Obligation/query/purpose scope differs")
    snapshot = prepared.snapshot
    require_lexical_result_snapshot(snapshot, lexical_result)
    statistics = {
        id(s) for s in lexical_result.index.corpus_statistics.document_statistics
    }
    if any(id(m.document_statistics) not in statistics for m in lexical_result.matches):
        raise ValueError("Lexical match is foreign to the retained index")
    documents = tuple(
        m.document_statistics.analysis.document for m in lexical_result.matches
    )
    positions = {d.resource.address: rank for rank, d in enumerate(documents, 1)}
    if len(positions) != len(documents):
        raise ValueError("Duplicate lexical candidate")
    grouped: dict[
        RepositoryResourceAddress,
        dict[RepositoryResourceAddress, list[PythonDeclarationReferenceKnowledge]],
    ] = {}
    for fact in prepared.facts:
        source, target = fact.occurrence.resource_address, fact.target_resource.address
        if (
            source not in positions
            or target not in positions
            or positions[source] >= positions[target]
        ):
            continue
        grouped.setdefault(target, {}).setdefault(source, []).append(fact)
    annotations = []
    for document in documents:
        target = document.resource.address
        if target not in grouped:
            continue
        rank = positions[target]
        sources = tuple(
            SupportingSource(
                documents[positions[source] - 1].resource,
                documents[positions[source] - 1].id,
                positions[source],
                tuple(
                    PythonDirectStructuralResourceEvidence(
                        source, "reference-to-definition", fact
                    )
                    for fact in facts
                ),
            )
            for source, facts in sorted(
                grouped[target].items(), key=lambda x: (positions[x[0]], str(x[0]))
            )
        )
        predecessor = documents[rank - 2]
        annotations.append(
            TargetAnnotation(
                document.resource,
                document.id,
                rank,
                sources,
                predecessor.resource,
                predecessor.id,
            )
        )
    return AnnotatedLexicalSurface(
        obligation, query, purpose, snapshot, lexical_result, tuple(annotations)
    )
