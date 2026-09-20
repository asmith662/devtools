# Copyright (c) 2026
"""Tests for whole-resource repository text document representation."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositoryResourceDiscovery,
    RepositoryTextDocumentId,
    define_repository_text_corpus,
    observe_repository_resources,
    realize_repository_text_corpus,
    represent_repository_text_corpus,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from devtools.context.repository.corpus import RepositoryTextCorpus

_MAXIMUM_RESOURCE_BYTES = 1024


def _repository(value: str = "00000000-0000-4000-8000-000000000001") -> Repository:
    return Repository(RepositoryId.parse(value))


def _corpus(
    *,
    tmp_path: Path,
    repository: Repository,
    contents: dict[str, str],
    selected_addresses: tuple[str, ...],
) -> RepositoryTextCorpus:
    for address, text in contents.items():
        path = tmp_path / Path(address)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")
    addresses = tuple(
        RepositoryResourceAddress(address) for address in sorted(contents)
    )
    discovery = RepositoryResourceDiscovery(
        repository_id=repository.id,
        root=ResolvedPath(tmp_path),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
        examined_entry_count=len(addresses),
        addresses=addresses,
    )
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=tuple(
            RepositoryResourceAddress(address) for address in selected_addresses
        ),
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )
    return realize_repository_text_corpus(definition=definition, snapshot=snapshot)


def test_represents_heterogeneous_corpus_members_as_exact_whole_resources(
    tmp_path: Path,
) -> None:
    """All selected UTF-8 resources use the same whole-resource representation."""
    corpus = _corpus(
        tmp_path=tmp_path,
        repository=_repository(),
        contents={
            "README.md": "# Caf\u00e9\r\n",
            "config/settings.yaml": "enabled: true\n",
            "docs/design.md": "# Design\n",
            "pyproject.toml": "[project]\n",
            "src/example.py": "VALUE = 1\n",
        },
        selected_addresses=(
            "src/example.py",
            "README.md",
            "pyproject.toml",
            "config/settings.yaml",
            "docs/design.md",
        ),
    )

    collection = represent_repository_text_corpus(corpus=corpus)

    assert collection.corpus is corpus
    assert [str(document.resource.address) for document in collection.documents] == [
        "README.md",
        "config/settings.yaml",
        "docs/design.md",
        "pyproject.toml",
        "src/example.py",
    ]
    assert [document.text for document in collection.documents] == [
        "# Caf\u00e9\r\n",
        "enabled: true\n",
        "# Design\n",
        "[project]\n",
        "VALUE = 1\n",
    ]
    assert all(
        document.resource is resource
        for document, resource in zip(
            collection.documents,
            corpus.resources,
            strict=True,
        )
    )
    assert all(
        document.repository_id == corpus.definition.discovery.repository_id
        for document in collection.documents
    )


def test_equivalent_representation_is_deterministic(tmp_path: Path) -> None:
    """Representing the same corpus repeatedly preserves document identities."""
    corpus = _corpus(
        tmp_path=tmp_path,
        repository=_repository(),
        contents={"README.md": "readme\n"},
        selected_addresses=("README.md",),
    )

    first = represent_repository_text_corpus(corpus=corpus)
    second = represent_repository_text_corpus(corpus=corpus)

    assert first == second
    assert str(first.documents[0].id) == first.documents[0].id.value


def test_selected_content_and_address_change_document_identity(tmp_path: Path) -> None:
    """Document identity depends on its represented address and content identity."""
    repository = _repository()
    first = represent_repository_text_corpus(
        corpus=_corpus(
            tmp_path=tmp_path / "first",
            repository=repository,
            contents={"alpha.txt": "same\n"},
            selected_addresses=("alpha.txt",),
        ),
    )
    different_address = represent_repository_text_corpus(
        corpus=_corpus(
            tmp_path=tmp_path / "second",
            repository=repository,
            contents={"beta.txt": "same\n"},
            selected_addresses=("beta.txt",),
        ),
    )
    changed_content = represent_repository_text_corpus(
        corpus=_corpus(
            tmp_path=tmp_path / "third",
            repository=repository,
            contents={"alpha.txt": "changed\n"},
            selected_addresses=("alpha.txt",),
        ),
    )

    assert first.documents[0].id != different_address.documents[0].id
    assert first.documents[0].id != changed_content.documents[0].id


def test_other_member_changes_collection_but_not_an_unchanged_document(
    tmp_path: Path,
) -> None:
    """A document does not inherit unrelated corpus-member identity inputs."""
    repository = _repository()
    first_corpus = _corpus(
        tmp_path=tmp_path / "first",
        repository=repository,
        contents={"common.txt": "common\n", "other.txt": "first\n"},
        selected_addresses=("common.txt", "other.txt"),
    )
    second_corpus = _corpus(
        tmp_path=tmp_path / "second",
        repository=repository,
        contents={"common.txt": "common\n", "other.txt": "second\n"},
        selected_addresses=("common.txt", "other.txt"),
    )
    membership_changed_corpus = _corpus(
        tmp_path=tmp_path / "third",
        repository=repository,
        contents={"common.txt": "common\n", "other.txt": "second\n"},
        selected_addresses=("common.txt",),
    )

    first = represent_repository_text_corpus(corpus=first_corpus)
    second = represent_repository_text_corpus(corpus=second_corpus)
    membership_changed = represent_repository_text_corpus(
        corpus=membership_changed_corpus,
    )

    assert first != second
    assert first.documents[0].id == second.documents[0].id
    assert first != membership_changed
    assert first.documents[0].id == membership_changed.documents[0].id


def test_empty_corpus_represents_without_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty corpus yields an empty document collection without further work."""
    repository = _repository()
    definition = define_repository_text_corpus(
        discovery=RepositoryResourceDiscovery(
            repository_id=repository.id,
            root=ResolvedPath(Path.cwd()),
            maximum_resource_count=20,
            maximum_traversal_entry_count=20,
            examined_entry_count=0,
            addresses=(),
        ),
        selected_addresses=(),
    )
    corpus = realize_repository_text_corpus(definition=definition)

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Document representation must not perform work."
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)
    monkeypatch.setattr(
        "devtools.context.python.function.retrieval.retrieve_python_functions_by_exact_name",
        fail,
    )

    collection = represent_repository_text_corpus(corpus=corpus)

    assert collection.corpus is corpus
    assert collection.documents == ()


def test_document_representation_exposes_no_lexical_or_ranking_state(
    tmp_path: Path,
) -> None:
    """Whole-resource representation has no token, score, or embedding semantics."""
    document = represent_repository_text_corpus(
        corpus=_corpus(
            tmp_path=tmp_path,
            repository=_repository(),
            contents={"README.md": "readme\n"},
            selected_addresses=("README.md",),
        ),
    ).documents[0]

    assert all(
        not hasattr(document, attribute)
        for attribute in (
            "tokens",
            "term_frequencies",
            "score",
            "rank",
            "bm25",
            "embedding",
            "normalized_text",
        )
    )


def test_document_identity_rejects_noncanonical_value() -> None:
    """Document identities use the existing lowercase SHA-256 validation contract."""
    with pytest.raises(ValueError, match="64-character"):
        RepositoryTextDocumentId("not-a-digest")
