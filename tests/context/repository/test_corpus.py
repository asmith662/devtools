# Copyright (c) 2026
"""Tests for explicit discovery-grounded corpus membership intent."""

from __future__ import annotations

import pytest
from pathlib import Path

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
        ".gitignore", "README.md", "config.json", "notes", "pyproject.toml",
    )


def test_empty_membership_and_invalid_selection() -> None:
    """Empty membership is valid while duplicate or undiscovered input is not."""
    discovery = _discovery()
    empty = define_repository_text_corpus(discovery=discovery, selected_addresses=())
    assert empty.selected_addresses == ()
    assert empty.excluded_addresses == discovery.addresses
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
