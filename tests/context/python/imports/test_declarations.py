# Copyright (c) 2026
# ruff: noqa: D103, E501, PLR2004
"""Tests for direct Python import-declaration knowledge."""

from pathlib import Path

import pytest

from devtools.context.python.imports import (
    PythonImportParseError,
    derive_python_import_declarations,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath


def _snapshot(tmp_path: Path, text: str) -> object:
    (tmp_path / "module.py").write_text(text, encoding="utf-8", newline="")
    return observe_repository_resources(
        repository=Repository(RepositoryId.parse("00000000-0000-4000-8000-000000000017")),
        root=ResolvedPath(tmp_path),
        addresses=(RepositoryResourceAddress("module.py"),),
        maximum_resource_bytes=1024 * 1024,
    )


def test_import_forms_aliases_relative_levels_and_order(tmp_path: Path) -> None:
    text = "import foo\nimport foo.bar\nimport foo as alias\nimport one, two as local_two\nfrom source import item\nfrom source.pkg import member as local_member\nfrom source import a, b as local_b\nfrom . import relative\nfrom .pkg import entry\nfrom ..up import member\n"
    result = derive_python_import_declarations(_snapshot(tmp_path, text))  # type: ignore[arg-type]
    assert [(item.module, item.level, item.imported_name, item.local_alias) for item in result.declarations] == [("foo", 0, None, None), ("foo.bar", 0, None, None), ("foo", 0, None, "alias"), ("one", 0, None, None), ("two", 0, None, "local_two"), ("source", 0, "item", None), ("source.pkg", 0, "member", "local_member"), ("source", 0, "a", None), ("source", 0, "b", "local_b"), (None, 1, "relative", None), ("pkg", 1, "entry", None), ("up", 2, "member", None)]
    assert result.coverage.declaration_count == 12
    assert result.coverage.IS_EXHAUSTIVE is True


def test_zero_nested_parse_failure_and_occurrence(tmp_path: Path) -> None:
    result = derive_python_import_declarations(_snapshot(tmp_path, "if True:\n    import ignored\ndef f():\n    import ignored_again\n"))  # type: ignore[arg-type]
    assert result.declarations == ()
    assert result.coverage.declaration_count == 0
    with pytest.raises(PythonImportParseError):
        derive_python_import_declarations(_snapshot(tmp_path, "import ("))  # type: ignore[arg-type]
    grounded = derive_python_import_declarations(_snapshot(tmp_path, "import foo, bar\n"))  # type: ignore[arg-type]
    assert grounded.declarations[0].support == grounded.declarations[1].support
    assert grounded.declarations[0].support.resource_address.value == "module.py"


def test_explicit_address_and_multi_resource_requirement(tmp_path: Path) -> None:
    """Selection remains explicit when a snapshot has more than one resource."""
    (tmp_path / "a.py").write_text("import a\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("import b\n", encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000017"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=(RepositoryResourceAddress("a.py"), RepositoryResourceAddress("b.py")),
        maximum_resource_bytes=1024 * 1024,
    )
    with pytest.raises(ValueError, match="exactly one"):
        derive_python_import_declarations(snapshot)
    assert derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("b.py"),
    ).declarations[0].module == "b"
