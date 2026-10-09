# Copyright (c) 2026
# ruff: noqa: COM812 -- literal protocol prose or fixture assertions; formatter owns commas
"""Build isolated native frames without historical case defaults."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import put_text
from experiments.exact_hint_routing.routing import ExactFrame

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )


def make_frame(
    tmp_path: Path,
    source: str = "class Target:\n    def run(self): pass\ndef build(): pass\n",
    *,
    competing_source: str | None = None,
) -> tuple[ExactFrame, RepositoryTextLexicalInvertedIndex]:
    """Observe native facts from a finite temporary fixture only."""
    put_text(tmp_path / "src/pkg/native.py", source)
    put_text(tmp_path / "docs/notes.md", "noise target documentation\n")
    if competing_source is not None:
        put_text(tmp_path / "other/pkg/native.py", competing_source)
    repository = Repository(RepositoryId.parse("00000000-0000-0000-0000-000000000071"))
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=resolve_path(tmp_path),
        maximum_resource_count=20,
        maximum_traversal_entry_count=40,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(tmp_path),
        addresses=discovery.addresses,
        maximum_resource_bytes=4096,
    )
    addresses: tuple[RepositoryResourceAddress, ...] = (
        RepositoryResourceAddress("src/pkg/native.py"),
    )
    analysis = interpret_python_module_resources(
        snapshot, module_root=PythonModuleRoot("src"), resource_addresses=addresses
    )
    interpretations = analysis.interpretations
    if competing_source is not None:
        extra = RepositoryResourceAddress("other/pkg/native.py")
        interpretations += interpret_python_module_resources(
            snapshot, module_root=PythonModuleRoot("other"), resource_addresses=(extra,)
        ).interpretations
        addresses += (extra,)
    modules = define_python_module_interpretation_universe(
        repository_id=repository.id, interpretations=interpretations
    )
    frame = ExactFrame(repository.id, snapshot.id, snapshot, modules, addresses)
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery, selected_addresses=discovery.addresses
        ),
        snapshot=snapshot,
    )
    docs = represent_repository_text_corpus(corpus=corpus)
    index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=docs
            )
        )
    )
    return frame, index


@pytest.fixture
def native(tmp_path: Path) -> tuple[ExactFrame, RepositoryTextLexicalInvertedIndex]:
    """Supply a fresh controlled native frame."""
    return make_frame(tmp_path)
