# Copyright (c) 2026
"""Tests for public path parsing, resolution, and location helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools.core.paths import (
    PathParsingError,
    PathResolutionError,
    ResolvedPath,
    get_downloads_dir,
    get_home_dir,
    get_temp_dir,
    parse_dot_path,
    parse_path,
    resolve_dot_path,
    resolve_path,
)


def test_parse_path_accepts_path_and_string_representations(tmp_path: Path) -> None:
    """Filesystem path parsing preserves supported representations."""
    path = tmp_path / "report.txt"

    assert parse_path(path) is path
    assert parse_path(str(path)) == path


def test_parse_path_rejects_empty_strings() -> None:
    """Blank filesystem path strings are not valid representations."""
    with pytest.raises(PathParsingError, match="cannot be empty"):
        parse_path("   ")


def test_parse_dot_path_converts_components_and_optional_suffix() -> None:
    """Dot paths convert mechanically to relative filesystem paths."""
    assert parse_dot_path("devtools.core.paths.models") == Path(
        "devtools",
        "core",
        "paths",
        "models",
    )
    assert parse_dot_path("devtools.core.paths.models", suffix="py") == Path(
        "devtools",
        "core",
        "paths",
        "models.py",
    )
    assert parse_dot_path("devtools.core.paths.models", suffix=".py") == Path(
        "devtools",
        "core",
        "paths",
        "models.py",
    )


@pytest.mark.parametrize("value", ["", "  ", "one..two", ".one", "one."])
def test_parse_dot_path_rejects_empty_components(value: str) -> None:
    """Empty dot paths and components are rejected."""
    with pytest.raises(PathParsingError):
        parse_dot_path(value)


def test_parse_dot_path_rejects_an_empty_suffix() -> None:
    """An explicitly supplied suffix must contain characters."""
    with pytest.raises(PathParsingError, match="Suffix cannot be empty"):
        parse_dot_path("devtools.core.paths", suffix="")


def test_parse_dot_path_normalizes_invalid_suffix_errors() -> None:
    """Invalid suffix application remains a path-domain parsing failure."""
    with pytest.raises(PathParsingError, match="Invalid dot-path suffix") as raised:
        parse_dot_path("devtools.core.paths", suffix="/bad")

    assert isinstance(raised.value.__cause__, ValueError)


def test_resolve_path_normalizes_absolute_paths_without_existing_target(
    tmp_path: Path,
) -> None:
    """Absolute paths are normalized even when their targets do not exist."""
    candidate = tmp_path / "missing" / ".." / "result.txt"

    resolved_path = resolve_path(candidate)

    assert resolved_path == ResolvedPath((tmp_path / "result.txt").resolve())


def test_resolve_path_uses_an_explicit_absolute_base(tmp_path: Path) -> None:
    """Relative paths resolve from the supplied absolute base directory."""
    resolved_path = resolve_path(
        Path("nested") / "." / "item" / ".." / "result.txt",
        base_directory=tmp_path,
    )

    assert resolved_path.value == (tmp_path / "nested" / "result.txt").resolve()


def test_resolve_path_requires_a_base_for_relative_inputs() -> None:
    """Relative filesystem paths cannot depend on the process directory."""
    with pytest.raises(PathResolutionError, match="explicit base directory"):
        resolve_path("relative.txt")


def test_resolve_path_rejects_relative_bases() -> None:
    """A base directory must itself be absolute."""
    with pytest.raises(PathResolutionError, match="must be absolute"):
        resolve_path("relative.txt", base_directory=Path("relative-base"))


def test_resolve_dot_path_parses_suffix_and_resolves_from_base(tmp_path: Path) -> None:
    """Dot-path resolution composes public parsing and resolution behavior."""
    resolved_path = resolve_dot_path(
        "package.module",
        base_directory=tmp_path,
        suffix="py",
    )

    assert resolved_path.value == (tmp_path / "package" / "module.py").resolve()


def test_resolve_dot_path_propagates_public_parse_and_base_errors() -> None:
    """Invalid dot paths and bases retain their documented error types."""
    with pytest.raises(PathParsingError):
        resolve_dot_path("invalid..dot", base_directory=Path.cwd())

    with pytest.raises(PathResolutionError, match="must be absolute"):
        resolve_dot_path("package.module", base_directory=Path("relative-base"))


def test_known_directory_helpers_return_conventional_absolute_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Known-directory helpers use their documented portable conventions."""
    home_directory = tmp_path / "home"
    temp_directory = tmp_path / "temporary"

    monkeypatch.setattr(Path, "home", lambda: home_directory)
    monkeypatch.setattr(
        "devtools.core.paths.resolution.tempfile.gettempdir",
        lambda: str(temp_directory),
    )

    assert get_home_dir() == ResolvedPath(home_directory.resolve())
    assert get_temp_dir() == ResolvedPath(temp_directory.resolve())
    assert get_downloads_dir() == ResolvedPath((home_directory / "Downloads").resolve())
