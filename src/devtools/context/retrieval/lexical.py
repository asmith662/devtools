# Copyright (c) 2026
"""Baseline heterogeneous lexical observations over repository text documents."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.repository.document import (
        RepositoryTextDocument,
        RepositoryTextDocumentCollection,
    )

_LEXICAL_SPAN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalObservation:
    """Record one normalized lexical span and its exact document-text evidence."""

    encounter_ordinal: int
    observed_text: str
    normalized_term: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalDocumentAnalysis:
    """Retain ordered baseline lexical observations for one exact document."""

    document: RepositoryTextDocument
    observations: tuple[RepositoryTextLexicalObservation, ...]

    ANALYSIS_SEMANTICS: ClassVar[str] = "unicode-word-span-casefold-v1"


@dataclass(frozen=True, slots=True)
class RepositoryTextLexicalCollectionAnalysis:
    """Retain independent lexical analyses in document-collection order."""

    document_collection: RepositoryTextDocumentCollection
    analyses: tuple[RepositoryTextLexicalDocumentAnalysis, ...]

    ANALYSIS_SEMANTICS: ClassVar[str] = (
        RepositoryTextLexicalDocumentAnalysis.ANALYSIS_SEMANTICS
    )


def analyze_repository_text_document(
    *,
    document: RepositoryTextDocument,
) -> RepositoryTextLexicalDocumentAnalysis:
    """Observe Unicode word spans in one document without retrieval or parsing."""
    return RepositoryTextLexicalDocumentAnalysis(
        document=document,
        observations=tuple(
            RepositoryTextLexicalObservation(
                encounter_ordinal=ordinal,
                observed_text=match.group(),
                normalized_term=match.group().casefold(),
                start=match.start(),
                end=match.end(),
            )
            for ordinal, match in enumerate(
                _LEXICAL_SPAN_PATTERN.finditer(document.text),
            )
        ),
    )


def analyze_repository_text_document_collection(
    *,
    document_collection: RepositoryTextDocumentCollection,
) -> RepositoryTextLexicalCollectionAnalysis:
    """Analyze each document independently while preserving collection order."""
    return RepositoryTextLexicalCollectionAnalysis(
        document_collection=document_collection,
        analyses=tuple(
            analyze_repository_text_document(document=document)
            for document in document_collection.documents
        ),
    )
