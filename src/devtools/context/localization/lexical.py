# Copyright (c) 2026
"""Acquire full-task and obligation-associated native lexical evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from devtools.context.retrieval.composition import require_lexical_result_snapshot
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25RetrievalResult,
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        LocalizationQueryIdentity,
    )
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )


@dataclass(frozen=True, slots=True)
class ObligationLexicalQuery:
    """Associate exact caller query text with one task obligation."""

    identity: LocalizationQueryIdentity
    obligation: LocalizationObligationIdentity
    text: str

    def __post_init__(self) -> None:
        """Require a query identity and obligation from the same task scope."""
        if self.identity.task != self.obligation.task:
            msg = "Obligation lexical query identities must share task scope."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ObligationLexicalEvidence:
    """Keep an obligation/query association beside the untouched native result."""

    request: ObligationLexicalQuery
    retrieval: RepositoryTextLexicalBm25RetrievalResult


@dataclass(frozen=True, slots=True)
class LocalizationLexicalAcquisitionRequest:
    """Bind task purpose, query lanes, corpus frame, and BM25 bound for one run."""

    task: LocalizationTaskInterpretation
    purpose: str
    full_task_query: str
    obligation_queries: tuple[ObligationLexicalQuery, ...]
    snapshot: RepositorySnapshot
    index: RepositoryTextLexicalInvertedIndex
    maximum_results: int
    settings: RepositoryTextLexicalBm25Settings = field(
        default_factory=RepositoryTextLexicalBm25Settings,
    )


@dataclass(frozen=True, slots=True)
class LocalizationLexicalAcquisition:
    """Retain one full-task lane and ordered obligation-specific native lanes."""

    task: LocalizationTaskInterpretation
    purpose: str
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    full_task_retrieval: RepositoryTextLexicalBm25RetrievalResult
    obligation_retrievals: tuple[ObligationLexicalEvidence, ...]


def acquire_localization_lexical_evidence(
    request: LocalizationLexicalAcquisitionRequest,
) -> LocalizationLexicalAcquisition:
    """Run existing BM25 independently for the global and explicit task lanes.

    The complete supplied task query is retained verbatim. Each obligation query
    is an independent retrieval over the same caller-authorized lexical index;
    this operation neither fuses lanes nor assesses obligation satisfaction.
    """
    if not request.purpose.strip():
        msg = "Localization lexical acquisition requires a task purpose."
        raise ValueError(msg)
    obligation_ids = {item.identity for item in request.task.obligations}
    query_ids: set[LocalizationQueryIdentity] = set()
    for query in request.obligation_queries:
        if query.identity.task != request.task.identity:
            msg = "Obligation lexical query has a foreign task identity."
            raise ValueError(msg)
        if query.obligation not in obligation_ids:
            msg = "Obligation lexical query references an unknown obligation."
            raise ValueError(msg)
        if query.identity in query_ids:
            msg = "Obligation lexical query identity is duplicated."
            raise ValueError(msg)
        query_ids.add(query.identity)

    global_result = _retrieve(
        query_text=request.full_task_query,
        index=request.index,
        maximum_results=request.maximum_results,
        settings=request.settings,
    )
    require_lexical_result_snapshot(request.snapshot, global_result)
    obligation_results = tuple(
        ObligationLexicalEvidence(
            request=query,
            retrieval=_retrieve(
                query_text=query.text,
                index=request.index,
                maximum_results=request.maximum_results,
                settings=request.settings,
            ),
        )
        for query in request.obligation_queries
    )
    return LocalizationLexicalAcquisition(
        task=request.task,
        purpose=request.purpose,
        repository_id=request.snapshot.repository_id,
        snapshot_id=request.snapshot.id,
        full_task_retrieval=global_result,
        obligation_retrievals=obligation_results,
    )


def _retrieve(
    *,
    query_text: str,
    index: RepositoryTextLexicalInvertedIndex,
    maximum_results: int,
    settings: RepositoryTextLexicalBm25Settings,
) -> RepositoryTextLexicalBm25RetrievalResult:
    """Execute canonical content-plus-filename BM25 without altering its result."""
    return retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=query_text),
        index=index,
        maximum_results=maximum_results,
        settings=settings,
    )
