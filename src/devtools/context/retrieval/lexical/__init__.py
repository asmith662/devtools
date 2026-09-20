# Copyright (c) 2026
"""Public facade for bounded lexical analysis and content indexing."""

from devtools.context.retrieval.lexical.analysis import (
    RepositoryTextLexicalCollectionAnalysis,
    RepositoryTextLexicalDocumentAnalysis,
    RepositoryTextLexicalObservation,
    analyze_repository_text_document,
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.index import (
    RepositoryTextLexicalInvertedIndex,
    RepositoryTextLexicalPosting,
    RepositoryTextLexicalTermPostings,
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    RepositoryTextLexicalCorpusStatistics,
    RepositoryTextLexicalDocumentFrequency,
    RepositoryTextLexicalDocumentStatistics,
    RepositoryTextLexicalTermFrequency,
    calculate_repository_text_lexical_corpus_statistics,
)

__all__ = [
    "RepositoryTextLexicalCollectionAnalysis",
    "RepositoryTextLexicalCorpusStatistics",
    "RepositoryTextLexicalDocumentAnalysis",
    "RepositoryTextLexicalDocumentFrequency",
    "RepositoryTextLexicalDocumentStatistics",
    "RepositoryTextLexicalInvertedIndex",
    "RepositoryTextLexicalObservation",
    "RepositoryTextLexicalPosting",
    "RepositoryTextLexicalTermFrequency",
    "RepositoryTextLexicalTermPostings",
    "analyze_repository_text_document",
    "analyze_repository_text_document_collection",
    "build_repository_text_lexical_inverted_index",
    "calculate_repository_text_lexical_corpus_statistics",
]
