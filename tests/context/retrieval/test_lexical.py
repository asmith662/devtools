# Copyright (c) 2026
"""Tests for baseline heterogeneous repository text lexical analysis."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.context import (
    ContentIdentity,
    RepositoryId,
    RepositoryResourceAddress,
    RepositoryResourceDiscovery,
    RepositoryResourceOccurrence,
    RepositoryTextCorpus,
    RepositoryTextCorpusId,
    RepositoryTextDocument,
    RepositoryTextDocumentCollection,
    RepositoryTextDocumentId,
    analyze_repository_text_document,
    analyze_repository_text_document_collection,
    define_repository_text_corpus,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    import pytest

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("utf-8"))
    return digest.hexdigest()


def _document(address: str, text: str) -> RepositoryTextDocument:
    repository_id = RepositoryId.parse(_REPOSITORY_ID)
    resource_address = RepositoryResourceAddress(address)
    occurrence = RepositoryResourceOccurrence(
        address=resource_address,
        content_identity=ContentIdentity(_digest(text)),
        content=text,
        encoding="utf-8",
        byte_size=len(text.encode("utf-8")),
    )
    return RepositoryTextDocument(
        id=RepositoryTextDocumentId(_digest(str(repository_id), address, text)),
        repository_id=repository_id,
        resource=occurrence,
    )


def _collection(
    documents: tuple[RepositoryTextDocument, ...],
) -> RepositoryTextDocumentCollection:
    repository_id = RepositoryId.parse(_REPOSITORY_ID)
    ordered_documents = tuple(
        sorted(documents, key=lambda document: document.resource.address.value),
    )
    addresses = tuple(document.resource.address for document in ordered_documents)
    definition = define_repository_text_corpus(
        discovery=RepositoryResourceDiscovery(
            repository_id=repository_id,
            root=ResolvedPath(Path.cwd()),
            maximum_resource_count=20,
            maximum_traversal_entry_count=20,
            examined_entry_count=len(addresses),
            addresses=addresses,
        ),
        selected_addresses=addresses,
    )
    corpus = RepositoryTextCorpus(
        id=RepositoryTextCorpusId(
            _digest("corpus", *(str(address) for address in addresses)),
        ),
        definition=definition,
        resources=tuple(document.resource for document in ordered_documents),
    )
    return RepositoryTextDocumentCollection(
        corpus=corpus,
        documents=ordered_documents,
    )


def test_heterogeneous_documents_use_one_baseline_lexical_mechanism() -> None:
    """Source, Markdown, TOML, YAML, and prose share one lexical analyzer."""
    documents = (
        _document("src/example.py", "def load_repository(): return repository_id"),
        _document("README.md", "# Repository Architecture\nThe repository corpus."),
        _document("pyproject.toml", "[tool.pytest.ini_options]\naddopts = '-q'"),
        _document("config/settings.yaml", "repository:\n  maximum_bytes: 1024"),
        _document("docs/design.md", "Retrieval should preserve exact evidence."),
    )

    result = analyze_repository_text_document_collection(
        document_collection=_collection(documents),
    )

    assert result.analyses[0].document is result.document_collection.documents[0]
    assert result.document_collection.documents == tuple(
        sorted(documents, key=lambda document: document.resource.address.value),
    )
    assert [
        tuple(observation.normalized_term for observation in analysis.observations)
        for analysis in result.analyses
    ] == [
        ("repository", "architecture", "the", "repository", "corpus"),
        ("repository", "maximum_bytes", "1024"),
        ("retrieval", "should", "preserve", "exact", "evidence"),
        ("tool", "pytest", "ini_options", "addopts", "q"),
        ("def", "load_repository", "return", "repository_id"),
    ]


def test_observations_preserve_order_repetition_casefolding_and_exact_spans() -> None:
    """Baseline observations preserve native text evidence and encounter order."""
    document = _document(
        "README.md",
        "Alpha alpha alpha RepositoryTextDocument repository_text_document "
        "pyproject.toml foo.bar foo-bar version2 Stra\u00dfe",
    )

    analysis = analyze_repository_text_document(document=document)

    assert tuple(
        observation.observed_text for observation in analysis.observations
    ) == (
        "Alpha",
        "alpha",
        "alpha",
        "RepositoryTextDocument",
        "repository_text_document",
        "pyproject",
        "toml",
        "foo",
        "bar",
        "foo",
        "bar",
        "version2",
        "Stra\u00dfe",
    )
    assert tuple(
        observation.normalized_term for observation in analysis.observations
    ) == (
        "alpha",
        "alpha",
        "alpha",
        "repositorytextdocument",
        "repository_text_document",
        "pyproject",
        "toml",
        "foo",
        "bar",
        "foo",
        "bar",
        "version2",
        "strasse",
    )
    assert [
        observation.encounter_ordinal for observation in analysis.observations
    ] == list(range(len(analysis.observations)))
    assert all(
        document.text[observation.start : observation.end]
        == observation.observed_text
        for observation in analysis.observations
    )


def test_document_analysis_is_deterministic_and_independent_of_other_documents(
) -> None:
    """One document's analysis does not depend on collection or corpus neighbors."""
    unchanged = _document("common.txt", "Common alpha")
    first = analyze_repository_text_document(document=unchanged)
    second = analyze_repository_text_document(document=unchanged)
    first_collection = analyze_repository_text_document_collection(
        document_collection=_collection((unchanged, _document("other.txt", "first"))),
    )
    second_collection = analyze_repository_text_document_collection(
        document_collection=_collection((unchanged, _document("other.txt", "changed"))),
    )

    assert first == second
    assert first_collection.analyses[0] == second_collection.analyses[0]
    assert first_collection != second_collection


def test_empty_document_and_empty_collection_are_successful_zero_results() -> None:
    """No recognized spans and no documents are both valid bounded outcomes."""
    empty_document = _document("empty.txt", "--- !!!")
    empty_analysis = analyze_repository_text_document(document=empty_document)
    empty_collection = analyze_repository_text_document_collection(
        document_collection=_collection(()),
    )

    assert empty_analysis.document is empty_document
    assert empty_analysis.observations == ()
    assert empty_collection.analyses == ()


def test_analysis_performs_no_acquisition_parsing_or_retrieval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lexical analysis consumes only document text and never crosses its boundary."""
    document = _document("README.md", "Repository text")

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Lexical analysis must not perform unrelated work."
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.candidates.tokenize.generate_tokens",
        fail,
    )
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)
    monkeypatch.setattr(
        "devtools.context.python.function.retrieval.retrieve_python_functions_by_exact_name",
        fail,
    )

    analysis = analyze_repository_text_document(document=document)

    assert tuple(
        observation.normalized_term for observation in analysis.observations
    ) == (
        "repository",
        "text",
    )


def test_analysis_exposes_no_statistics_or_retrieval_state() -> None:
    """Baseline analysis records observations, not statistics, queries, or ranks."""
    analysis = analyze_repository_text_document(
        document=_document("README.md", "repository repository"),
    )

    assert all(
        not hasattr(analysis, attribute)
        for attribute in (
            "score",
            "rank",
            "query",
            "relevance",
            "term_frequency",
            "document_frequency",
            "idf",
            "bm25",
            "embedding",
        )
    )
