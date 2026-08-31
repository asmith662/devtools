# Copyright (c) 2026
"""Tests for the experimental repository-file Tool adapter."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import (
    File,
    FileFormatError,
    FilesystemNotFoundError,
    MarkdownFile,
    NotAFileError,
)
from devtools.paths import ResolvedPath
from devtools.tools import Tool, ToolInputError, ToolRunner
from devtools.tools.filesystem import ReadRepositoryFileTool

if TYPE_CHECKING:
    from pathlib import Path


def _resolved(path: Path) -> ResolvedPath:
    """Create one normalized absolute path value for Tool input."""
    return ResolvedPath(path.resolve())


def test_read_repository_file_tool_is_typed_and_returns_rich_file(
    tmp_path: Path,
) -> None:
    """An admitted supported file remains its rich Filesystem model."""
    root = tmp_path / "repository"
    source = root / "notes.md"
    source.parent.mkdir()
    source.write_bytes(b"# Notes\nready\n")

    async def exercise() -> None:
        tool = ReadRepositoryFileTool(_resolved(root))
        typed_tool: Tool[ResolvedPath, File] = tool
        result: File = await ToolRunner().execute(typed_tool, _resolved(source))

        assert tool.name == "read_repository_file"
        assert tool.description
        assert isinstance(result, MarkdownFile)
        assert result.content == "# Notes\nready\n"

    asyncio.run(exercise())


def test_read_repository_file_tool_rejects_sibling_prefix_without_reading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A sibling path sharing a textual prefix remains outside the root."""
    root = tmp_path / "repository"
    candidate = tmp_path / "repository-other" / "notes.md"

    def read_must_not_run(_path: ResolvedPath) -> File:
        msg = "Filesystem execution should not begin for rejected input."
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.tools.filesystem.read", read_must_not_run)

    async def exercise() -> None:
        with pytest.raises(ToolInputError, match="outside"):
            await ToolRunner().execute(
                ReadRepositoryFileTool(_resolved(root)),
                _resolved(candidate),
            )

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("root_form", "candidate_form"),
    [
        ("unnormalized", "normalized"),
        ("normalized", "unnormalized"),
    ],
)
def test_read_repository_file_tool_normalizes_direct_resolved_path_inputs(
    tmp_path: Path,
    root_form: str,
    candidate_form: str,
) -> None:
    """Equivalent direct absolute values receive the same scope decision."""
    root = tmp_path / "repository"
    source = root / "notes.md"
    source.parent.mkdir()
    source.write_bytes(b"# Notes\n")
    root_value = root / "nested" / ".." if root_form == "unnormalized" else root
    candidate_value = (
        root / "nested" / ".." / source.name
        if candidate_form == "unnormalized"
        else source
    )

    async def exercise() -> None:
        result = await ToolRunner().execute(
            ReadRepositoryFileTool(ResolvedPath(root_value)),
            ResolvedPath(candidate_value),
        )

        assert isinstance(result, MarkdownFile)
        assert result.content == "# Notes\n"

    asyncio.run(exercise())


def test_read_repository_file_tool_rejects_direct_parent_escape(
    tmp_path: Path,
) -> None:
    """A direct absolute parent escape is rejected after normalization."""
    root = tmp_path / "repository"
    candidate = ResolvedPath(root / ".." / "other" / "notes.md")

    async def exercise() -> None:
        with pytest.raises(ToolInputError, match="outside"):
            await ToolRunner().execute(
                ReadRepositoryFileTool(ResolvedPath(root)),
                candidate,
            )

    asyncio.run(exercise())


def test_read_repository_file_tool_leaves_missing_paths_to_filesystem(
    tmp_path: Path,
) -> None:
    """An admitted missing path remains a Filesystem execution failure."""
    root = tmp_path / "repository"
    root.mkdir()

    async def exercise() -> None:
        with pytest.raises(FilesystemNotFoundError):
            await ToolRunner().execute(
                ReadRepositoryFileTool(_resolved(root)),
                _resolved(root / "missing.md"),
            )

    asyncio.run(exercise())


def test_read_repository_file_tool_leaves_directories_to_filesystem(
    tmp_path: Path,
) -> None:
    """An admitted in-root directory remains a Filesystem execution failure."""
    root = tmp_path / "repository"
    directory = root / "directory"
    directory.mkdir(parents=True)

    async def exercise() -> None:
        with pytest.raises(NotAFileError):
            await ToolRunner().execute(
                ReadRepositoryFileTool(_resolved(root)),
                _resolved(directory),
            )

    asyncio.run(exercise())


def test_read_repository_file_tool_admits_root_then_filesystem_rejects_directory(
    tmp_path: Path,
) -> None:
    """The configured root itself is in scope but normally is not a file."""
    root = tmp_path / "repository"
    root.mkdir()

    async def exercise() -> None:
        with pytest.raises(NotAFileError):
            await ToolRunner().execute(
                ReadRepositoryFileTool(_resolved(root)),
                _resolved(root),
            )

    asyncio.run(exercise())


def test_read_repository_file_tool_preserves_filesystem_format_errors(
    tmp_path: Path,
) -> None:
    """An admitted unsupported file remains a Filesystem format failure."""
    root = tmp_path / "repository"
    source = root / "notes.unknown"
    source.parent.mkdir()
    source.write_text("notes", encoding="utf-8")

    async def exercise() -> None:
        with pytest.raises(FileFormatError):
            await ToolRunner().execute(
                ReadRepositoryFileTool(_resolved(root)),
                _resolved(source),
            )

    asyncio.run(exercise())


def test_read_repository_file_tool_repeated_reads_are_independent(
    tmp_path: Path,
) -> None:
    """Repeated reads return independent domain values without Tool state."""
    root = tmp_path / "repository"
    source = root / "notes.md"
    source.parent.mkdir()
    source.write_text("# Notes\n", encoding="utf-8")

    async def exercise() -> None:
        runner = ToolRunner()
        tool = ReadRepositoryFileTool(_resolved(root))

        first = await runner.execute(tool, _resolved(source))
        second = await runner.execute(tool, _resolved(source))

        assert isinstance(first, MarkdownFile)
        assert isinstance(second, MarkdownFile)
        assert first == second

    asyncio.run(exercise())
