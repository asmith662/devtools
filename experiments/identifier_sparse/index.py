# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter convention
"""Experiment-owned expanded-term statistics over native whole-resource documents."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

from experiments.identifier_sparse.analysis import iter_terms

if TYPE_CHECKING:
    from collections.abc import Iterable

    from devtools.context.repository.document import RepositoryTextDocumentCollection


@dataclass(frozen=True, slots=True)
class FieldIndex:
    """Retain immutable document lengths and term/document-frequency postings."""

    lengths: tuple[int, ...]
    postings: tuple[tuple[str, tuple[tuple[int, int], ...]], ...]
    average_length: float

    @property
    def vocabulary_size(self) -> int:
        """Count distinct field terms, not observations."""
        return len(self.postings)

    @property
    def posting_count(self) -> int:
        """Count distinct term/document pairs."""
        return sum(len(items) for _, items in self.postings)


def build_field(texts: Iterable[str], *, identifier: bool = True) -> FieldIndex:
    """Count all expanded observations, including repeated independent spans."""
    lengths = []
    postings: dict[str, list[tuple[int, int]]] = {}
    for position, text in enumerate(texts):
        counts = Counter(iter_terms(text, identifier=identifier))
        lengths.append(counts.total())
        for term, frequency in counts.items():
            postings.setdefault(term, []).append((position, frequency))
    return FieldIndex(
        tuple(lengths),
        tuple((term, tuple(items)) for term, items in postings.items()),
        sum(lengths) / len(lengths) if lengths else 0.0,
    )


@dataclass(frozen=True, slots=True)
class IdentifierIndex:
    """Keep the exact native corpus separate from experimental representation."""

    documents: RepositoryTextDocumentCollection
    content: FieldIndex


def build_index(documents: RepositoryTextDocumentCollection) -> IdentifierIndex:
    """Build R1 content state without mutating canonical analyses or identities."""
    return IdentifierIndex(
        documents, build_field(item.text for item in documents.documents)
    )
