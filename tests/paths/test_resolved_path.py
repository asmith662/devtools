# Copyright (c) 2026
"""Tests for :class:`devtools.paths.ResolvedPath`."""

from __future__ import annotations

import os
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from devtools.paths import ResolvedPath


def test_constructs_from_an_absolute_path(tmp_path: Path) -> None:
    """An absolute path is retained unchanged."""
    path = tmp_path / "example.txt"

    resolved_path = ResolvedPath(path)

    assert resolved_path.path == path


def test_rejects_a_relative_path() -> None:
    """A relative path violates the value object's invariant."""
    with pytest.raises(ValueError, match="requires an absolute path"):
        ResolvedPath(Path("relative.txt"))


def test_is_immutable(tmp_path: Path) -> None:
    """The stored path cannot be reassigned."""
    resolved_path = ResolvedPath(tmp_path)
    attribute = "path"

    with pytest.raises(FrozenInstanceError):
        setattr(resolved_path, attribute, tmp_path.parent)


def test_exposes_path_metadata_and_representations(tmp_path: Path) -> None:
    """Path metadata and string forms delegate to the stored path."""
    path = tmp_path / "directory" / "archive.tar.gz"
    resolved_path = ResolvedPath(path)

    assert resolved_path.path == path
    assert resolved_path.name == "archive.tar.gz"
    assert resolved_path.stem == "archive.tar"
    assert resolved_path.suffix == ".gz"
    assert resolved_path.suffixes == (".tar", ".gz")
    assert resolved_path.parts == path.parts
    assert resolved_path.as_posix() == path.as_posix()
    assert str(resolved_path) == str(path)
    assert os.fspath(resolved_path) == os.fspath(path)
    assert Path(resolved_path) == path


def test_equality_and_hashing_are_value_based(tmp_path: Path) -> None:
    """Frozen dataclass equality and hashing use the stored path."""
    path = tmp_path / "item"

    assert ResolvedPath(path) == ResolvedPath(path)
    assert hash(ResolvedPath(path)) == hash(ResolvedPath(path))


def test_root_path_and_suffixless_filename_edge_cases(tmp_path: Path) -> None:
    """Root paths and suffixless filenames preserve pathlib semantics."""
    root = Path(tmp_path.anchor)
    suffixless = ResolvedPath(tmp_path / "README")

    assert ResolvedPath(root).name == root.name
    assert ResolvedPath(root).parts == root.parts
    assert suffixless.name == "README"
    assert suffixless.stem == "README"
    assert suffixless.suffix == ""
    assert suffixless.suffixes == ()
