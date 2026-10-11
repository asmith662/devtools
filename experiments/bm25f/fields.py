# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812 -- bounded experiment validation
"""Read-only adaptation of canonical observations with exact native frame binding."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)

if TYPE_CHECKING:
    from devtools.context.repository.document import RepositoryTextDocumentCollection
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.filename import (
        RepositoryTextFilenameLexicalIndex,
    )
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )


@dataclass(frozen=True, slots=True)
class FieldState:
    """Retain canonical fields and native source frame."""

    collection: RepositoryTextDocumentCollection
    snapshot: RepositorySnapshot
    content: RepositoryTextLexicalInvertedIndex
    filename: RepositoryTextFilenameLexicalIndex
    observation_sha256: str


def validate_frame(
    collection: RepositoryTextDocumentCollection, snapshot: RepositorySnapshot
) -> None:
    """Reject foreign, stale, duplicate or reordered frame members."""
    repository = collection.corpus.definition.discovery.repository_id
    documents = collection.documents
    if (
        snapshot.repository_id != repository
        or any(d.repository_id != repository for d in documents)
        or tuple(d.resource for d in documents) != collection.corpus.resources
        or tuple(snapshot.resources) != collection.corpus.resources
        or tuple(d.resource.address for d in documents)
        != collection.corpus.definition.selected_addresses
        or len({d.id for d in documents}) != len(documents)
        or len({d.resource.address for d in documents}) != len(documents)
    ):
        raise ValueError("Foreign/stale/ambiguous field frame")


def build_fields(
    collection: RepositoryTextDocumentCollection, snapshot: RepositorySnapshot
) -> FieldState:
    """Build canonical fields only after execution authorization."""
    validate_frame(collection, snapshot)
    content = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=collection
            )
        )
    )
    filename = build_repository_text_filename_lexical_index(
        document_collection=collection
    )
    seal = hashlib.sha256(
        repr((collection, snapshot, content, filename)).encode()
    ).hexdigest()
    return FieldState(collection, snapshot, content, filename, seal)


def validate_state(state: FieldState) -> None:
    """Reject mutated field observations/statistics before scientific scoring."""
    validate_frame(state.collection, state.snapshot)
    seal = hashlib.sha256(
        repr((state.collection, state.snapshot, state.content, state.filename)).encode()
    ).hexdigest()
    if seal != state.observation_sha256:
        raise ValueError("Field observation/statistics tamper")
