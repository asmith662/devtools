# Copyright (c) 2026
"""Whole-resource searchable representations of repository text corpus members."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from devtools.context.repository.resource import _validate_sha256

if TYPE_CHECKING:
    from devtools.context.repository.corpus import RepositoryTextCorpus
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import RepositoryResourceOccurrence


@dataclass(frozen=True, slots=True)
class RepositoryTextDocumentId:
    """Identify one repository text representation under local strategy semantics."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Repository text document identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositoryTextDocument:
    """Represent one corpus member as one whole-resource searchable document."""

    id: RepositoryTextDocumentId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    REPRESENTATION_SEMANTICS: ClassVar[str] = "whole-resource-exact-text-v1"

    @property
    def text(self) -> str:
        """Return the exact decoded text retained by the source occurrence."""
        return self.resource.content


@dataclass(frozen=True, slots=True)
class RepositoryTextDocumentCollection:
    """Retain one corpus and its ordered whole-resource document representation."""

    corpus: RepositoryTextCorpus
    documents: tuple[RepositoryTextDocument, ...]

    REPRESENTATION_SEMANTICS: ClassVar[str] = (
        RepositoryTextDocument.REPRESENTATION_SEMANTICS
    )


def represent_repository_text_corpus(
    *,
    corpus: RepositoryTextCorpus,
) -> RepositoryTextDocumentCollection:
    """Represent every corpus member once without tokenization or acquisition."""
    repository_id = corpus.definition.discovery.repository_id
    return RepositoryTextDocumentCollection(
        corpus=corpus,
        documents=tuple(
            RepositoryTextDocument(
                id=RepositoryTextDocumentId(
                    _semantic_digest(
                        RepositoryTextDocument.REPRESENTATION_SEMANTICS,
                        str(repository_id),
                        str(resource.address),
                        str(resource.content_identity),
                    ),
                ),
                repository_id=repository_id,
                resource=resource,
            )
            for resource in corpus.resources
        ),
    )


def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash unambiguous length-framed document identity inputs."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
