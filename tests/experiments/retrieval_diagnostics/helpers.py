# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention

"""Native toy captures through actual rankers, never a mock scoring oracle."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
    retrieve_repository_text_documents_by_content_bm25,
)
from experiments.codex_dogfood.case_0009.freeze import canonical_index
from experiments.identifier_sparse.index import build_index
from experiments.identifier_sparse.retrieval import retrieve
from experiments.retrieval_diagnostics import adapters
from experiments.retrieval_diagnostics.models import Judgment
from tests.context.retrieval.lexical._helpers import _collection, _document

if TYPE_CHECKING:
    from experiments.retrieval_diagnostics.models import Label, LaneCapture

OBLIGATION = LocalizationObligationIdentity(
    LocalizationTaskIdentity("diagnostic-fixture"), "need"
)


def capture(
    documents: tuple[tuple[str, str], ...],
    query: str = "plain",
    *,
    expanded: bool = False,
    limit: int = 100,
    content_only: bool = False,
) -> LaneCapture:
    """Capture native evidence for exact snapshot/corpus identities."""
    collection = _collection(
        tuple(_document(address, text) for address, text in documents)
    )
    snapshot = RepositorySnapshot(
        RepositorySnapshotId("a" * 64),
        collection.documents[0].repository_id,
        tuple(d.resource for d in collection.documents),
    )
    if expanded:
        result = retrieve(build_index(collection), query, maximum_results=limit)
        return adapters.identifier(
            snapshot,
            "query",
            result,
            treatment="B",
            index_identity="fixture-index-B",
            obligation=OBLIGATION,
        )
    ranker = (
        retrieve_repository_text_documents_by_content_bm25
        if content_only
        else retrieve_repository_text_documents_by_bm25
    )
    native = ranker(
        query=analyze_repository_text_lexical_query(text=query),
        index=canonical_index(collection),
        maximum_results=limit,
    )
    return adapters.canonical(
        snapshot,
        "query",
        native,
        treatment="A",
        index_identity="fixture-index-A",
        filename_weight=0.0 if content_only else 0.25,
        obligation=OBLIGATION,
    )


def judged(value: LaneCapture, labels: tuple[Label, ...]) -> tuple[Judgment, ...]:
    """Attach independent toy obligation labels in corpus order."""
    return tuple(
        Judgment(
            value.frame, r, OBLIGATION, label, ("unit",) if label == "REQUIRED" else ()
        )
        for r, label in zip(value.resources, labels, strict=True)
    )
