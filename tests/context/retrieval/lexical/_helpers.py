# Copyright (c) 2026
"""Shared builders for lexical retrieval tests."""

from __future__ import annotations

import hashlib
from pathlib import Path

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
    define_repository_text_corpus,
)
from devtools.core.paths import ResolvedPath

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _digest(*values: str) -> str:
    """Return the deterministic test digest used by document/corpus fixtures."""
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("utf-8"))
    return digest.hexdigest()


def _document(address: str, text: str) -> RepositoryTextDocument:
    """Build a repository text document with exact observed text."""
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
    """Build the stable caller-selected corpus/document collection for tests."""
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
