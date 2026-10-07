# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention
"""Expose independent-field combination weight only at the experiment boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Match,
    RepositoryTextLexicalBm25RetrievalResult,
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_content_bm25,
)
from devtools.context.retrieval.lexical.filename import (
    score_repository_text_filename_lexical_bm25,
)

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.filename import (
        RepositoryTextFilenameLexicalIndex,
    )
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )
    from experiments.retrieval_diagnostics.models import Configuration


def retrieve(
    index: RepositoryTextLexicalInvertedIndex,
    filename: RepositoryTextFilenameLexicalIndex,
    text: str,
    config: Configuration,
) -> RepositoryTextLexicalBm25RetrievalResult:
    """Reuse native content/filename scorers, preserving canonical combination/ties."""
    collection = index.corpus_statistics.collection_analysis.document_collection
    query = analyze_repository_text_lexical_query(text=text)
    settings = RepositoryTextLexicalBm25Settings(k1=config.k1, b=config.b)
    content = retrieve_repository_text_documents_by_content_bm25(
        query=query,
        index=index,
        maximum_results=max(1, len(collection.documents)),
        settings=settings,
    )
    names = score_repository_text_filename_lexical_bm25(
        query=query, index=filename, settings=settings
    )
    matches = {id(m.document_statistics.analysis.document): m for m in content.matches}
    statistics = {
        id(s.analysis.document): s for s in index.corpus_statistics.document_statistics
    }
    ranked = []
    for position, document in enumerate(collection.documents):
        match = matches.get(id(document))
        terms = names.get(id(document), ())
        content_score = match.content_score if match else 0.0
        filename_score = sum(t.contribution for t in terms)
        score = content_score + config.filename_weight * filename_score
        if score > 0:
            ranked.append(
                (
                    position,
                    RepositoryTextLexicalBm25Match(
                        document_statistics=statistics[id(document)],
                        score=score,
                        term_contributions=match.term_contributions if match else (),
                        content_score=content_score,
                        filename_score=filename_score,
                        filename_weight=config.filename_weight,
                        weighted_filename_score=config.filename_weight * filename_score,
                        filename_term_contributions=terms,
                    ),
                )
            )
    ranked.sort(key=lambda item: (-item[1].score, item[0]))
    return RepositoryTextLexicalBm25RetrievalResult(
        query=query,
        index=index,
        settings=settings,
        maximum_results=max(1, len(collection.documents)),
        matches=tuple(m for _, m in ranked),
        filename_index=filename,
    )
