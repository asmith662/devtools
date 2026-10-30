# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, D103, INP001, S101, PT011, PT018
# Dynamic experimental assertions; not an installable or maintained API.
"""Public diagnostics for delegated representation, not host integration."""

from __future__ import annotations

import json

import pytest

from devtools.agents.coding import navigation
from devtools.context import Repository, RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from devtools.tools.errors import ToolInputError
from devtools.tools.source import SourceScope


def scope_at(root, files):
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        write(TextFile(resolve_path(root / path), text))
    return SourceScope.observe(
        root=resolve_path(root),
        repository=Repository.new(),
        addresses=tuple(RepositoryResourceAddress(p) for p in files),
    )


def implementation():
    value = getattr(navigation, "complete_inventory", None)
    assert callable(value), "Complete authorized inventory representation is missing"
    return value


def test_complete_metadata(tmp_path):
    scope = scope_at(tmp_path, {"z.py": "secret-source\n", "read me.txt": "\u00e9\n"})
    (tmp_path / "outside.txt").write_bytes(b"outside-private")
    value = implementation()(scope, (RepositoryResourceAddress("z.py"),), 4096)
    assert value["repository_id"] == str(scope.snapshot.repository_id)
    assert value["snapshot_id"] == str(scope.snapshot.id)
    assert value["source_acquired"] is False
    assert value["complete_inventory"] is True
    assert [r["address"] for r in value["resources"]] == ["read me.txt", "z.py"]
    assert [r["editable"] for r in value["resources"]] == [False, True]
    assert [r["byte_size"] for r in value["resources"]] == [3, 14]
    for row, resource in zip(value["resources"], scope.snapshot.resources, strict=True):
        assert row["content_identity"] == str(resource.content_identity)
    wire = json.dumps(value, ensure_ascii=False)
    assert all(
        x not in wire
        for x in ("secret-source", "outside.txt", "outside-private", str(tmp_path))
    )


def test_empty_scope(tmp_path):
    scope = scope_at(tmp_path, {})
    value = implementation()(scope, (), 4096)
    assert value["resources"] == [] and value["complete_inventory"] is True
    assert value["snapshot_id"] == str(scope.snapshot.id)


def test_budget_and_foreign_editability(tmp_path):
    scope = scope_at(tmp_path, {"a.py": ""})
    fn = implementation()
    value = fn(scope, (), 4096)
    size = len(json.dumps(value, ensure_ascii=False).encode("utf-8"))
    assert fn(scope, (), size) == value
    with pytest.raises(ValueError, match="budget"):
        fn(scope, (), size - 1)
    with pytest.raises(ValueError):
        fn(scope, (RepositoryResourceAddress("outside.py"),), 4096)
    for invalid in (0, -1, True, 3.5):
        with pytest.raises(ValueError):
            fn(scope, (), invalid)


def test_stale_scope_refused(tmp_path):
    scope = scope_at(tmp_path, {"a.py": "old"})
    fn = implementation()
    write(TextFile(resolve_path(tmp_path / "a.py"), "new"))
    with pytest.raises(ToolInputError, match="no longer current"):
        fn(scope, (), 4096)
