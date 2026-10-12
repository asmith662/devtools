# Copyright (c) 2026
"""Stable import identities for Case 0015 durable capture values only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.repository.document import RepositoryTextDocumentCollection
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.analysis import (
        RepositoryTextLexicalCollectionAnalysis,
    )
    from devtools.context.retrieval.lexical.filename import (
        RepositoryTextFilenameLexicalIndex,
    )


@dataclass(frozen=True, slots=True)
class PreparedFrame:
    """Native frame values with a stable durable type, not a new identity domain."""

    documents: RepositoryTextDocumentCollection
    snapshot: RepositorySnapshot
    SCHEMA: ClassVar[str] = "case-0015-prepared-frame-v2"


@dataclass(frozen=True, slots=True)
class PreparedFields:
    """Canonical field preparation with a stable durable type."""

    content: RepositoryTextLexicalCollectionAnalysis
    filename: RepositoryTextFilenameLexicalIndex
    SCHEMA: ClassVar[str] = "case-0015-prepared-fields-v2"
