# Copyright (c) 2026
"""Authored source/RI fixtures shared by independent framework tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.retrieval import build_source_search_index
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from devtools.tools.source import SourceScope

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.source import SourceSearchIndex

TEXT = "# \u03c0 prefix\r\ndef value():\r\n    return 7\r\n# tail\r\n"


def source_fixture(
    root: Path,
    text: str = TEXT,
) -> tuple[SourceScope, SourceSearchIndex]:
    """Observe and index one actual file using only canonical public substrates."""
    path = resolve_path(root / "module.py")
    write(TextFile(path, text), overwrite=False)
    address = RepositoryResourceAddress("module.py")
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=Repository.new(),
        addresses=(address,),
    )
    discovery = discover_repository_resource_addresses(
        repository=Repository(scope.snapshot.repository_id),
        root=scope.root,
        maximum_resource_count=4,
        maximum_traversal_entry_count=16,
        requested_addresses=(address,),
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=(address,),
        ),
        snapshot=scope.snapshot,
    )
    return scope, build_source_search_index(
        scope.snapshot,
        corpus=corpus,
        window_lines=2,
        overlap_lines=0,
    )
