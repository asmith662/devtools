# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Production exact observed Python mirrored-path knowledge."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.python import derive_python_mirrored_path_correspondences
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.repository.snapshot import RepositorySnapshot


def _snapshot(tmp_path: Path, contents: dict[str, str]) -> RepositorySnapshot:
    for address, content in contents.items():
        target = tmp_path / address
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000031"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in contents),
        maximum_resource_bytes=1024,
    )


def test_exact_nested_pairs_roles_and_observed_support(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "tests/pkg/test_z.py": "# test z\n",
            "src/devtools/pkg/z.py": "# source z\n",
            "src/devtools/a.py": "# source a\n",
            "tests/test_a.py": "# test a\n",
            "src/devtools/pkg/deep/thing.py": "# source thing\n",
            "tests/pkg/deep/test_thing.py": "# test thing\n",
        },
    )
    result = derive_python_mirrored_path_correspondences(snapshot)
    assert [
        (str(item.source.address), str(item.test.address))
        for item in result.correspondences
    ] == [
        ("src/devtools/a.py", "tests/test_a.py"),
        ("src/devtools/pkg/deep/thing.py", "tests/pkg/deep/test_thing.py"),
        ("src/devtools/pkg/z.py", "tests/pkg/test_z.py"),
    ]
    assert all(
        item.repository_id == snapshot.repository_id for item in result.correspondences
    )
    assert all(item.snapshot_id == snapshot.id for item in result.correspondences)
    assert all(
        item.source == snapshot.resource_at(item.source.address)
        and item.test == snapshot.resource_at(item.test.address)
        for item in result.correspondences
    )
    assert len({item.identity for item in result.correspondences}) == 3
    assert result.coverage.correspondence_count == 3
    assert result.coverage.unmatched_source_resources == 0
    assert result.coverage.unmatched_named_test_resources == 0
    assert result.coverage.derivation_identity == result.derivation.identity
    assert result == derive_python_mirrored_path_correspondences(snapshot)
    assert not hasattr(result.correspondences[0], "tests")
    assert not hasattr(result.correspondences[0], "coverage")
    assert not hasattr(result.correspondences[0], "relevance")


def test_unmatched_near_matches_and_initializer_exclusions(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/devtools/pkg/thing.py": "",
            "tests/other/test_thing.py": "",
            "tests/pkg/thing.py": "",
            "tests/pkg/test_Thing.py": "",
            "src/devtools/pkg/orphan.py": "",
            "tests/pkg/test_orphan.py.bak": "",
            "tests/pkg/test_missing.py": "",
            "src/other/pkg/missing.py": "",
            "src/devtools/pkg/__init__.py": "",
            "tests/pkg/test___init__.py": "",
            "tests/pkg/__init__.py": "",
            "src/devtools/pkg/other.txt": "",
            "tests/pkg/test_other.txt": "",
        },
    )
    result = derive_python_mirrored_path_correspondences(snapshot)
    assert result.correspondences == ()
    assert result.coverage.source_resources_examined == 3
    assert result.coverage.test_resources_examined == 6
    assert result.coverage.excluded_initializers == 2
    assert result.coverage.eligible_source_resources == 2
    assert result.coverage.eligible_named_test_resources == 3
    assert result.coverage.unmatched_source_resources == 2
    assert result.coverage.unmatched_named_test_resources == 3
    assert result.coverage.IS_EXHAUSTIVE_FOR_SELECTION
    assert result.coverage.SCOPE == "explicit-observed-snapshot-resource-set"


def test_snapshot_identity_and_content_are_derivation_dependencies(
    tmp_path: Path,
) -> None:
    addresses = {
        "src/devtools/a.py": "source",
        "tests/test_a.py": "test",
    }
    first_snapshot = _snapshot(tmp_path, addresses)
    first = derive_python_mirrored_path_correspondences(first_snapshot)
    second_snapshot = _snapshot(tmp_path, {**addresses, "tests/test_a.py": "changed"})
    second = derive_python_mirrored_path_correspondences(second_snapshot)
    assert first_snapshot.id != second_snapshot.id
    assert first.derivation.identity != second.derivation.identity
    assert first.correspondences[0].identity != second.correspondences[0].identity
    assert first.correspondences[0].test != second.correspondences[0].test
    absent_snapshot = _snapshot(tmp_path, {"src/devtools/a.py": "source"})
    absent = derive_python_mirrored_path_correspondences(absent_snapshot)
    assert absent.correspondences == ()
    assert absent.coverage.unmatched_source_resources == 1
    test_only_snapshot = _snapshot(tmp_path, {"tests/test_a.py": "test"})
    test_only = derive_python_mirrored_path_correspondences(test_only_snapshot)
    assert test_only.correspondences == ()
    assert test_only.coverage.unmatched_named_test_resources == 1
    # A source and test observed in separate snapshots are never joined.
    assert absent.derivation.snapshot_id != test_only.derivation.snapshot_id
    # A retained snapshot is sufficient even after the working tree changes.
    (tmp_path / "src/devtools/a.py").unlink()
    (tmp_path / "tests/test_a.py").unlink()
    assert derive_python_mirrored_path_correspondences(first_snapshot) == first


def test_input_order_and_unrelated_observed_resources_affect_derivation(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"tests/test_a.py": "test", "src/devtools/a.py": "source"},
    )
    first = derive_python_mirrored_path_correspondences(snapshot)
    reversed_snapshot = replace(snapshot, resources=tuple(reversed(snapshot.resources)))
    assert derive_python_mirrored_path_correspondences(reversed_snapshot) == first
    extended = _snapshot(
        tmp_path,
        {
            "tests/test_a.py": "test",
            "src/devtools/a.py": "source",
            "README.md": "other",
        },
    )
    assert (
        derive_python_mirrored_path_correspondences(extended).derivation.identity
        != first.derivation.identity
    )


def test_duplicate_address_is_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"src/devtools/a.py": "source"})
    duplicate = replace(
        snapshot,
        resources=(*snapshot.resources, snapshot.resources[0]),
    )
    with pytest.raises(ValueError, match="repeats a resource address"):
        derive_python_mirrored_path_correspondences(duplicate)
