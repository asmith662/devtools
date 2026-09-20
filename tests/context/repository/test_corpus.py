# Copyright (c) 2026
"""Tests for explicit discovery-grounded corpus membership intent."""

from pathlib import Path

import pytest

from devtools.context import (
    RepositoryId,
    RepositoryResourceAddress,
    RepositoryResourceDiscovery,
    define_repository_text_corpus,
)
from devtools.core.paths import ResolvedPath


def _discovery() -> RepositoryResourceDiscovery:
    return RepositoryResourceDiscovery(
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000001"),
        root=ResolvedPath(Path.cwd()),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
        examined_entry_count=8,
        addresses=tuple(
            RepositoryResourceAddress(value)
            for value in (
                ".gitignore", "README.md", "assets/image.bin", "config.json",
                "notes", "pyproject.toml", "src/example.py", "uv.lock",
            )
        ),
    )


def _empty_discovery() -> RepositoryResourceDiscovery:
    return RepositoryResourceDiscovery(
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000001"),
        root=ResolvedPath(Path.cwd()),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
        examined_entry_count=0,
        addresses=(),
    )


def test_membership_is_discovery_grounded_heterogeneous_and_canonical() -> None:
    """Membership preserves discovery correlation and heterogeneous addresses."""
    discovery = _discovery()
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("uv.lock"),
            RepositoryResourceAddress("assets/image.bin"),
            RepositoryResourceAddress("src/example.py"),
        ),
    )
    assert definition.discovery is discovery
    assert tuple(map(str, definition.selected_addresses)) == (
        "assets/image.bin", "src/example.py", "uv.lock",
    )
    assert tuple(map(str, definition.excluded_addresses)) == (
        ".gitignore",
        "README.md",
        "config.json",
        "notes",
        "pyproject.toml",
    )


def test_equivalent_selection_is_caller_order_independent() -> None:
    """Equivalent caller selections yield the same canonical immutable value."""
    discovery = _discovery()
    first = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("src/example.py"),
            RepositoryResourceAddress("README.md"),
        ),
    )
    second = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("README.md"),
            RepositoryResourceAddress("src/example.py"),
        ),
    )
    assert first == second
    assert tuple(map(str, first.selected_addresses)) == ("README.md", "src/example.py")


def test_empty_membership_retains_nonempty_discovery() -> None:
    """An empty selection means only that no discovered address was selected."""
    discovery = _discovery()
    empty = define_repository_text_corpus(discovery=discovery, selected_addresses=())
    assert empty.discovery is discovery
    assert empty.selected_addresses == ()
    assert empty.excluded_addresses == discovery.addresses


def test_empty_discovery_can_define_an_empty_membership() -> None:
    """An empty definition remains correlated with its completed empty discovery."""
    discovery = _empty_discovery()
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(),
    )
    assert definition.discovery is discovery
    assert definition.selected_addresses == ()
    assert definition.excluded_addresses == ()


def test_duplicate_or_undiscovered_selection_fails() -> None:
    """Membership accepts only distinct addresses from the supplied discovery."""
    discovery = _discovery()
    address = RepositoryResourceAddress("src/example.py")
    with pytest.raises(ValueError, match="distinct"):
        define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=(address, address),
        )
    with pytest.raises(ValueError, match="not discovered"):
        define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=(RepositoryResourceAddress("missing.py"),),
        )


def test_definition_construction_performs_no_acquisition_or_analysis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Membership construction does not rediscover, observe, parse, or classify."""
    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Definition construction must not perform work."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.repository.observation.observe_repository_resources",
        fail,
    )
    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)

    definition = define_repository_text_corpus(
        discovery=_discovery(),
        selected_addresses=(RepositoryResourceAddress("assets/image.bin"),),
    )

    assert tuple(map(str, definition.selected_addresses)) == ("assets/image.bin",)
