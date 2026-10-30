# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, D103, INP001, S101, PLR2004
# Dynamic experimental assertions; not an installable or maintained API.
"""Independent acceptance. Not in the worker's authorized source surface."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest

from devtools.context import RepositoryResourceAddress
from devtools.tools.errors import ToolInputError
from devtools.tools.source import SourceScope
from experiments.delegated_b0035.focused import implementation, scope_at


def test_many_complete_resources_and_utf8(tmp_path):
    files = {f"dir/{i:02}.txt": "\U0001f600\r\n" * i for i in range(19)}
    scope = scope_at(tmp_path, files)
    editable = tuple(
        RepositoryResourceAddress(p) for p in files if int(p[4:6]) % 2 == 0
    )
    result = implementation()(scope, editable + editable, 20000)
    assert len(result["resources"]) == 19
    for i, row in enumerate(result["resources"]):
        assert row["address"] == f"dir/{i:02}.txt"
        assert row["byte_size"] == 6 * i
        assert row["editable"] is (i % 2 == 0)
        assert set(row) == {"address", "content_identity", "byte_size", "editable"}
    assert set(result) == {
        "repository_id",
        "snapshot_id",
        "source_acquired",
        "complete_inventory",
        "resources",
    }
    with pytest.raises(ValueError, match="budget"):
        implementation()(scope, editable, 500)


def test_updated_observation_changes_identity(tmp_path):
    first = scope_at(tmp_path, {"a.py": "one"})
    old = implementation()(first, (), 4096)
    second = scope_at(tmp_path, {"a.py": "two\U0001f600"})
    new = implementation()(second, (), 4096)
    assert new["snapshot_id"] != old["snapshot_id"]
    assert (
        new["resources"][0]["content_identity"]
        != old["resources"][0]["content_identity"]
    )
    assert new["resources"][0]["byte_size"] == 7
    assert json.dumps(old) != json.dumps(new)


def test_canonical_order_not_input_order(tmp_path):
    scope = scope_at(tmp_path, {"z": "z", "a": "a"})
    # Same genuine observation, alternative occurrence order; no source acquisition.
    unordered = SourceScope(
        scope.root,
        replace(scope.snapshot, resources=tuple(reversed(scope.snapshot.resources))),
    )
    # Currentness rejects manufactured noncanonical snapshots; do not bypass it.
    with pytest.raises(ToolInputError):
        implementation()(unordered, (), 4096)
