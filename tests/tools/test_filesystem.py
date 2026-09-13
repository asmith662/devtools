# Copyright (c) 2026
"""Tests for the experimental repository-file Tool adapter."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest

from devtools.filesystem import (
    File,
    FileFormatError,
    FilesystemNotFoundError,
    FilesystemPermissionError,
    MarkdownFile,
    NotAFileError,
)
from devtools.paths import ResolvedPath
from devtools.tools import Tool, ToolInputError, ToolRunner, filesystem
from devtools.tools.filesystem import (
    ListRepositoryDirectoryTool,
    ReadRepositoryFileTool,
    RepositoryDirectoryEntry,
    RepositoryDirectoryEntryKind,
)

_TWO_ENTRIES = 2


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


def test_list_repository_directory_tool_returns_sorted_direct_entries(
    tmp_path: Path,
) -> None:
    """Listing is non-recursive and exposes only deterministic entry names and kinds."""
    root = tmp_path / "repository"
    facts = root / "facts"
    (facts / "nested").mkdir(parents=True)
    (facts / "nested" / "hidden.txt").write_text("hidden", encoding="utf-8")
    (facts / "zeta.txt").write_text("z", encoding="utf-8")
    (facts / "alpha.txt").write_text("a", encoding="utf-8")

    async def exercise() -> None:
        result = await ToolRunner().execute(
            ListRepositoryDirectoryTool(_resolved(root)),
            _resolved(facts),
        )

        assert result.truncated is False
        assert [(entry.name, entry.kind) for entry in result.entries] == [
            ("alpha.txt", RepositoryDirectoryEntryKind.FILE),
            ("nested", RepositoryDirectoryEntryKind.DIRECTORY),
            ("zeta.txt", RepositoryDirectoryEntryKind.FILE),
        ]
        assert all(entry.name != "hidden.txt" for entry in result.entries)

    asyncio.run(exercise())


def test_list_repository_directory_tool_bounds_and_marks_truncation(
    tmp_path: Path,
) -> None:
    """The Tool returns a deterministic bounded prefix and explicit truncation state."""
    root = tmp_path / "repository"
    facts = root / "facts"
    facts.mkdir(parents=True)
    for name in ("charlie.txt", "alpha.txt", "bravo.txt"):
        (facts / name).write_text(name, encoding="utf-8")

    async def exercise() -> None:
        result = await ToolRunner().execute(
            ListRepositoryDirectoryTool(_resolved(root), maximum_entries=_TWO_ENTRIES),
            _resolved(facts),
        )

        assert [entry.name for entry in result.entries] == ["alpha.txt", "bravo.txt"]
        assert len(result.entries) == _TWO_ENTRIES
        assert result.truncated is True

    asyncio.run(exercise())


def test_list_repository_directory_tool_reports_empty_directory_without_truncation(
    tmp_path: Path,
) -> None:
    """An empty direct listing is complete rather than a silently omitted result."""
    root = tmp_path / "repository"
    facts = root / "facts"
    facts.mkdir(parents=True)

    async def exercise() -> None:
        result = await ToolRunner().execute(
            ListRepositoryDirectoryTool(_resolved(root), maximum_entries=_TWO_ENTRIES),
            _resolved(facts),
        )

        assert result.entries == ()
        assert result.truncated is False

    asyncio.run(exercise())


def test_list_repository_directory_tool_exact_bound_is_not_truncated(
    tmp_path: Path,
) -> None:
    """Exactly the configured number of direct entries remains a complete listing."""
    root = tmp_path / "repository"
    facts = root / "facts"
    facts.mkdir(parents=True)
    for name in ("alpha.txt", "bravo.txt"):
        (facts / name).write_text(name, encoding="utf-8")

    async def exercise() -> None:
        result = await ToolRunner().execute(
            ListRepositoryDirectoryTool(_resolved(root), maximum_entries=_TWO_ENTRIES),
            _resolved(facts),
        )

        assert len(result.entries) == _TWO_ENTRIES
        assert result.truncated is False

    asyncio.run(exercise())


def test_list_repository_directory_tool_rejects_outside_root(tmp_path: Path) -> None:
    """A sibling directory remains outside the configured Tool scope."""
    root = tmp_path / "repository"
    sibling = tmp_path / "repository-other"
    sibling.mkdir()

    async def exercise() -> None:
        with pytest.raises(ToolInputError, match="outside"):
            await ToolRunner().execute(
                ListRepositoryDirectoryTool(_resolved(root)),
                _resolved(sibling),
            )

    asyncio.run(exercise())


def test_list_repository_directory_tool_preserves_missing_and_non_directory_errors(
    tmp_path: Path,
) -> None:
    """Admitted paths retain honest filesystem and standard directory failures."""
    root = tmp_path / "repository"
    root.mkdir()
    file = root / "file.txt"
    file.write_text("file", encoding="utf-8")

    async def exercise() -> None:
        tool = ListRepositoryDirectoryTool(_resolved(root))
        with pytest.raises(FilesystemNotFoundError):
            await ToolRunner().execute(tool, _resolved(root / "missing"))
        with pytest.raises(NotADirectoryError):
            await ToolRunner().execute(tool, _resolved(file))

    asyncio.run(exercise())


def test_list_repository_directory_tool_classifies_symlink_when_supported(
    tmp_path: Path,
) -> None:
    """A direct symlink is disclosed as a symlink without traversal."""
    root = tmp_path / "repository"
    facts = root / "facts"
    facts.mkdir(parents=True)
    target = root / "target.txt"
    target.write_text("target", encoding="utf-8")
    link = facts / "link.txt"
    try:
        link.symlink_to(target)
    except OSError as error:
        pytest.skip(f"Symlink creation is unavailable: {error}")

    async def exercise() -> None:
        result = await ToolRunner().execute(
            ListRepositoryDirectoryTool(_resolved(root)),
            _resolved(facts),
        )

        assert result.entries == (
            RepositoryDirectoryEntry("link.txt", RepositoryDirectoryEntryKind.SYMLINK),
        )

    asyncio.run(exercise())


def test_list_repository_directory_tool_requires_positive_bound(tmp_path: Path) -> None:
    """A zero entry bound cannot silently create an unusable Tool."""
    with pytest.raises(ValueError, match="positive"):
        ListRepositoryDirectoryTool(_resolved(tmp_path), maximum_entries=0)


def test_list_repository_directory_tool_exposes_local_tool_metadata(
    tmp_path: Path,
) -> None:
    """The concrete Tool keeps the normal provider-neutral Tool metadata shape."""
    tool = ListRepositoryDirectoryTool(_resolved(tmp_path))

    assert tool.name == "list_repository_directory"
    assert tool.description == (
        "List bounded direct entries inside one repository directory."
    )


def test_list_repository_directory_tool_converts_permission_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An admitted directory listing retains the Filesystem permission boundary."""
    root = tmp_path / "repository"
    facts = root / "facts"
    facts.mkdir(parents=True)

    def denied(_path: Path) -> object:
        msg = "denied"
        raise PermissionError(msg)

    monkeypatch.setattr(Path, "iterdir", denied)

    async def exercise() -> None:
        with pytest.raises(FilesystemPermissionError, match="Permission denied"):
            await ToolRunner().execute(
                ListRepositoryDirectoryTool(_resolved(root)),
                _resolved(facts),
            )

    asyncio.run(exercise())


@dataclass(frozen=True, slots=True)
class _OtherPath:
    """Model only the direct entry checks relevant to the private classifier."""

    name: str = "socket"

    def is_symlink(self) -> bool:
        return False

    def is_file(self) -> bool:
        return False

    def is_dir(self) -> bool:
        return False


def test_list_repository_directory_tool_classifies_other_direct_entry() -> None:
    """The explicit fallback avoids pretending unusual entries are ordinary files."""
    entry = filesystem._directory_entry(cast("Path", _OtherPath()))  # noqa: SLF001

    assert entry == RepositoryDirectoryEntry(
        "socket",
        RepositoryDirectoryEntryKind.OTHER,
    )
