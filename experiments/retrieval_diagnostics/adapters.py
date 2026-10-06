# Copyright (c) 2026
# ruff: noqa: COM812, EM101, PLR0913, PLR0917, TRY003 -- explicit experimental capture boundaries
"""Project canonical/R1 native evidence or frozen JSON, not ranking behavior."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.context.retrieval.lexical.filename import (
    RepositoryTextFilenameLexicalDocumentStatistics,
    build_repository_text_filename_lexical_index,
)
from experiments.identifier_sparse.index import build_field
from experiments.identifier_sparse.retrieval import (
    FILENAME_WEIGHT,
    SETTINGS,
    IdentifierResult,
)
from experiments.retrieval_diagnostics.models import (
    Configuration,
    FieldStatistics,
    Frame,
    LaneCapture,
    RankedCapture,
    TermCapture,
)

if TYPE_CHECKING:
    from devtools.context.localization.identity import LocalizationObligationIdentity
    from devtools.context.repository.document import RepositoryTextDocumentCollection
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from devtools.context.retrieval.lexical.statistics import (
        RepositoryTextLexicalDocumentStatistics,
    )


def fields(
    collection: RepositoryTextDocumentCollection, config: Configuration
) -> tuple[FieldStatistics, ...]:
    """Replay missing field state using its existing owner, never run queries."""
    texts = tuple(d.text for d in collection.documents)
    filenames = tuple(
        PurePosixPath(d.resource.address.value).stem for d in collection.documents
    )
    if config.analyzer == "identifier":
        output = []
        for name, weight, source in (
            ("content", 1.0, texts),
            ("filename", config.filename_weight, filenames),
        ):
            native = build_field(source)
            output.append(
                FieldStatistics(
                    name,
                    weight,
                    source,
                    native.lengths,
                    native.average_length,
                    native.postings,
                )
            )
        return tuple(output)
    content = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=collection
        )
    )
    filename = build_repository_text_filename_lexical_index(
        document_collection=collection
    )
    return (
        _canonical_field(
            "content",
            1.0,
            texts,
            content.document_statistics,
            content.average_document_length,
        ),
        _canonical_field(
            "filename",
            config.filename_weight,
            filenames,
            filename.document_statistics,
            filename.average_document_length,
        ),
    )


def _canonical_field(
    name: str,
    weight: float,
    texts: tuple[str, ...],
    statistics: tuple[
        RepositoryTextLexicalDocumentStatistics
        | RepositoryTextFilenameLexicalDocumentStatistics,
        ...,
    ],
    average: float,
) -> FieldStatistics:
    """Project retained canonical statistics without inventing another index."""
    postings: dict[str, list[tuple[int, int]]] = {}
    for i, item in enumerate(statistics):
        for t in item.term_frequencies:
            postings.setdefault(t.normalized_term, []).append((i, t.frequency))
    return FieldStatistics(
        name,
        weight,
        texts,
        tuple(d.document_length for d in statistics),
        average,
        tuple((term, tuple(p)) for term, p in postings.items()),
    )


def from_rows(
    snapshot: RepositorySnapshot,
    collection: RepositoryTextDocumentCollection,
    lane: str,
    query: str,
    query_terms: tuple[str, ...],
    rows: list[dict[str, Any]],
    config: Configuration,
    field_state: tuple[FieldStatistics, ...],
    *,
    complete: bool,
    obligation: LocalizationObligationIdentity | None = None,
) -> LaneCapture:
    """Bind the established Case B projection to native frozen occurrences."""
    frame = Frame(snapshot.repository_id, snapshot.id, collection.corpus.id)
    resources = tuple(d.resource for d in collection.documents)
    for d in collection.documents:
        if (
            d.repository_id != snapshot.repository_id
            or d.resource != snapshot.resource_at(d.resource.address)
        ):
            raise ValueError("Document is outside snapshot.")
    mapping = {r.address.value: r for r in resources}
    projected = []
    for r in rows:
        if (
            r["address"] not in mapping
            or r["content_identity"] != mapping[r["address"]].content_identity.value
        ):
            raise ValueError("Captured content identity differs.")
        if "filename_weight" in r and r["filename_weight"] != config.filename_weight:
            raise ValueError("Captured filename weight differs.")
        terms = tuple(
            TermCapture(
                f,
                t["term"],
                t["tf"],
                t["df"],
                t["length"],
                t["average_length"],
                t["idf"],
                t["contribution"],
            )
            for f in ("content", "filename")
            for t in r[f + "_terms"]
        )
        projected.append(
            RankedCapture(mapping[r["address"]], r["rank"], r["score"], terms)
        )
    return LaneCapture(
        frame,
        lane,
        query,
        query_terms,
        config,
        resources,
        field_state,
        tuple(projected),
        complete,
        obligation,
    )


def canonical(
    snapshot: RepositorySnapshot,
    lane: str,
    result: RepositoryTextLexicalBm25RetrievalResult,
    *,
    treatment: str,
    index_identity: str,
    filename_weight: float,
    obligation: LocalizationObligationIdentity | None = None,
) -> LaneCapture:
    """Consume a native canonical result, retaining its captured field evidence."""
    config = Configuration(
        treatment,
        index_identity,
        "canonical",
        result.settings.k1,
        result.settings.b,
        filename_weight,
    )
    collection = result.index.corpus_statistics.collection_analysis.document_collection
    rows = []
    for rank, match in enumerate(result.matches, 1):
        resource = match.document_statistics.analysis.document.resource
        item: dict[str, Any] = {
            "address": resource.address.value,
            "content_identity": resource.content_identity.value,
            "score": match.score,
            "rank": rank,
            "filename_weight": match.filename_weight,
        }
        for name, terms in (
            ("content", match.term_contributions),
            ("filename", match.filename_term_contributions),
        ):
            item[name + "_terms"] = [
                {
                    "term": t.normalized_term,
                    "tf": t.term_frequency,
                    "df": t.document_frequency,
                    "length": t.document_length,
                    "average_length": t.average_document_length,
                    "idf": t.inverse_document_frequency,
                    "contribution": t.contribution,
                }
                for t in terms
            ]
        rows.append(item)
    content = result.index.corpus_statistics
    state: tuple[FieldStatistics, ...] = (
        _canonical_field(
            "content",
            1.0,
            tuple(d.text for d in collection.documents),
            content.document_statistics,
            content.average_document_length,
        ),
    )
    if result.filename_index is not None:
        filename = result.filename_index
        state += (
            _canonical_field(
                "filename",
                filename_weight,
                tuple(
                    PurePosixPath(d.resource.address.value).stem
                    for d in collection.documents
                ),
                filename.document_statistics,
                filename.average_document_length,
            ),
        )
    return from_rows(
        snapshot,
        collection,
        lane,
        result.query.text,
        result.query.normalized_terms,
        rows,
        config,
        state,
        complete=result.maximum_results >= len(collection.documents),
        obligation=obligation,
    )


def identifier(
    snapshot: RepositorySnapshot,
    lane: str,
    result: IdentifierResult,
    *,
    treatment: str,
    index_identity: str,
    obligation: LocalizationObligationIdentity | None = None,
) -> LaneCapture:
    """Consume native R1 evidence and retained indexes, with no recomputation."""
    config = Configuration(
        treatment,
        index_identity,
        "identifier",
        SETTINGS.k1,
        SETTINGS.b,
        FILENAME_WEIGHT,
    )
    collection = result.index.documents
    state = tuple(
        FieldStatistics(
            name, weight, texts, native.lengths, native.average_length, native.postings
        )
        for name, weight, texts, native in (
            (
                "content",
                1.0,
                tuple(d.text for d in collection.documents),
                result.index.content,
            ),
            (
                "filename",
                FILENAME_WEIGHT,
                tuple(
                    PurePosixPath(d.resource.address.value).stem
                    for d in collection.documents
                ),
                result.filename_index,
            ),
        )
    )
    rows = []
    for rank, match in enumerate(result.matches, 1):
        resource = match.document.resource
        item: dict[str, Any] = {
            "address": resource.address.value,
            "content_identity": resource.content_identity.value,
            "score": match.score,
            "rank": rank,
        }
        for name, terms in (
            ("content", match.content_evidence),
            ("filename", match.filename_evidence),
        ):
            item[name + "_terms"] = [
                {
                    "term": t.term,
                    "tf": t.frequency,
                    "df": t.document_frequency,
                    "length": t.document_length,
                    "average_length": t.average_length,
                    "idf": t.idf,
                    "contribution": t.contribution,
                }
                for t in terms
            ]
        rows.append(item)
    return from_rows(
        snapshot,
        collection,
        lane,
        result.query_text,
        result.query_terms,
        rows,
        config,
        state,
        complete=result.maximum_results >= len(collection.documents),
        obligation=obligation,
    )
