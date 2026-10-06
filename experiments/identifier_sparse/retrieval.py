# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention
"""Independent content/filename BM25 using canonical production arithmetic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Settings
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)
from experiments.identifier_sparse.analysis import ANALYZER_SEMANTICS, query_terms
from experiments.identifier_sparse.index import FieldIndex, IdentifierIndex, build_field

if TYPE_CHECKING:
    from devtools.context.repository.document import RepositoryTextDocument

SETTINGS = RepositoryTextLexicalBm25Settings(k1=1.2, b=0.75)
FILENAME_WEIGHT = 0.25


@dataclass(frozen=True, slots=True)
class TermEvidence:
    """Explain exact field statistics and the reused BM25 arithmetic result."""

    term: str
    frequency: int
    document_frequency: int
    document_length: int
    average_length: float
    idf: float
    contribution: float


@dataclass(frozen=True, slots=True)
class IdentifierMatch:
    """Keep native resource identity and separate field evidence, without fusion."""

    document: RepositoryTextDocument
    score: float
    content_score: float
    filename_score: float
    content_evidence: tuple[TermEvidence, ...]
    filename_evidence: tuple[TermEvidence, ...]


@dataclass(frozen=True, slots=True)
class IdentifierResult:
    """Retain R1 representation identity, unchanged query text and corpus lineage."""

    query_text: str
    query_terms: tuple[str, ...]
    index: IdentifierIndex
    filename_index: FieldIndex
    maximum_results: int
    matches: tuple[IdentifierMatch, ...]
    analyzer: str = ANALYZER_SEMANTICS


def _score(
    field: FieldIndex, terms: tuple[str, ...]
) -> dict[int, tuple[TermEvidence, ...]]:
    evidence: dict[int, list[TermEvidence]] = {}
    postings = dict(field.postings)
    for term in terms:
        items = postings.get(term, ())
        if not items:
            continue
        idf = calculate_bm25_inverse_document_frequency(
            document_count=len(field.lengths),
            document_frequency=len(items),
        )
        for position, frequency in items:
            contribution = calculate_bm25_term_contribution(
                term_frequency=frequency,
                inverse_document_frequency=idf,
                document_length=field.lengths[position],
                average_document_length=field.average_length,
                settings=SETTINGS,
            )
            evidence.setdefault(position, []).append(
                TermEvidence(
                    term,
                    frequency,
                    len(items),
                    field.lengths[position],
                    field.average_length,
                    idf,
                    contribution,
                )
            )
    return {position: tuple(items) for position, items in evidence.items()}


def retrieve(
    index: IdentifierIndex, query: str, *, maximum_results: int
) -> IdentifierResult:
    """Change only lexical analysis; preserve whole units, weights and tie order."""
    if maximum_results <= 0:
        msg = "Maximum result count must be positive."
        raise ValueError(msg)
    terms = query_terms(query)
    # Match canonical lifecycle: filename statistics are built per retrieval.
    filename = build_field(
        PurePosixPath(item.resource.address.value).stem
        for item in index.documents.documents
    )
    content_scores = _score(index.content, terms)
    filename_scores = _score(filename, terms)
    matches = []
    for position, document in enumerate(index.documents.documents):
        content_evidence = content_scores.get(position, ())
        filename_evidence = filename_scores.get(position, ())
        content = sum(item.contribution for item in content_evidence)
        name = sum(item.contribution for item in filename_evidence)
        score = content + FILENAME_WEIGHT * name
        if score > 0:
            matches.append(
                IdentifierMatch(
                    document,
                    score,
                    content,
                    name,
                    content_evidence,
                    filename_evidence,
                )
            )
    # Stable sorting preserves exact collection order at equal score.
    matches.sort(key=lambda item: -item.score)
    return IdentifierResult(
        query, terms, index, filename, maximum_results, tuple(matches[:maximum_results])
    )
