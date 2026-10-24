# Copyright (c) 2026
# ruff: noqa: D103, PT011 -- contract fixes exception types, not diagnostic wording
"""Exact bounded resource differences; no filesystem or rename inference."""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from devtools.context import (
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositorySnapshot,
    RepositorySnapshotDelta,
    compare_repository_snapshots,
    observe_repository_resources,
)
from devtools.context.repository import RepositorySnapshotDelta as LocalDelta
from devtools.context.repository import compare_repository_snapshots as local_compare
from devtools.core.paths import resolve_path


def _snapshot(root: Path, resources: dict[str, str]) -> RepositorySnapshot:
    root.mkdir(parents=True, exist_ok=True)
    for name, text in resources.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000022"),
        ),
        root=resolve_path(root),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=65536,
    )


def _names(addresses: tuple[RepositoryResourceAddress, ...]) -> tuple[str, ...]:
    return tuple(address.value for address in addresses)


def test_public_result_and_actual_observed_resource_partitions(tmp_path: Path) -> None:
    before = _snapshot(
        tmp_path / "before",
        {"old.py": "shared", "edit.py": "old", "keep.py": "same"},
    )
    after = _snapshot(
        tmp_path / "after",
        {"new.py": "shared", "edit.py": "new", "keep.py": "same"},
    )
    delta = compare_repository_snapshots(before, after)
    assert isinstance(delta, RepositorySnapshotDelta)
    assert delta.before is before
    assert delta.after is after
    assert _names(delta.added) == ("new.py",)
    assert _names(delta.removed) == ("old.py",)
    assert _names(delta.modified) == ("edit.py",)
    assert _names(delta.unchanged) == ("keep.py",)
    reverse = compare_repository_snapshots(after, before)
    assert reverse.added == delta.removed
    assert reverse.removed == delta.added
    assert reverse.modified == delta.modified
    # Later changes to physical fixtures do not rewrite the retained observations.
    (tmp_path / "before/edit.py").write_text("later", encoding="utf-8")
    (tmp_path / "after/edit.py").unlink()
    assert delta == compare_repository_snapshots(before, after)
    with pytest.raises((FrozenInstanceError, AttributeError)):
        setattr(delta, "added", ())  # noqa: B010 -- exercise frozen result at runtime


def test_empty_and_unchanged_snapshots(tmp_path: Path) -> None:
    empty = _snapshot(tmp_path / "empty", {})
    sample = _snapshot(tmp_path / "sample", {"z.py": "Z", "a.py": "A"})
    assert not compare_repository_snapshots(empty, empty).unchanged
    assert _names(compare_repository_snapshots(empty, sample).added) == ("a.py", "z.py")
    assert _names(compare_repository_snapshots(sample, empty).removed) == (
        "a.py",
        "z.py",
    )
    same = compare_repository_snapshots(sample, sample)
    assert not same.added
    assert not same.removed
    assert not same.modified
    assert _names(same.unchanged) == ("a.py", "z.py")


def test_exact_case_unicode_and_order(tmp_path: Path) -> None:
    before = _snapshot(
        tmp_path / "before",
        {"Case.py": "x", "café.py": "old", "shared.py": "s"},
    )
    after = _snapshot(
        tmp_path / "after",
        {"case.py": "x", "café.py": "new", "shared.py": "s"},
    )
    result = compare_repository_snapshots(before, after)
    assert _names(result.added) == ("case.py",)
    assert _names(result.removed) == ("Case.py",)
    assert _names(result.modified) == ("café.py",)
    shuffled = compare_repository_snapshots(
        replace(before, resources=tuple(reversed(before.resources))),
        replace(after, resources=tuple(reversed(after.resources))),
    )
    assert (
        shuffled.added,
        shuffled.removed,
        shuffled.modified,
        shuffled.unchanged,
    ) == (
        result.added,
        result.removed,
        result.modified,
        result.unchanged,
    )


def test_complete_occurrence_equality_even_when_ids_are_equal(tmp_path: Path) -> None:
    before = _snapshot(tmp_path, {"a.py": "text"})
    resource = before.resource
    after = replace(before, resources=(replace(resource, encoding="different"),))
    assert after.id == before.id
    result = compare_repository_snapshots(before, after)
    assert _names(result.modified) == ("a.py",)
    assert not result.unchanged


@pytest.mark.parametrize("side", ["before", "after"])
def test_duplicate_addresses_refuse_ambiguous_inputs(tmp_path: Path, side: str) -> None:
    original = _snapshot(tmp_path, {"a.py": "text"})
    repeated = replace(original, resources=(original.resource, original.resource))
    with pytest.raises(ValueError):
        compare_repository_snapshots(
            repeated if side == "before" else original,
            repeated if side == "after" else original,
        )


def test_mismatched_repository_and_public_reexports(tmp_path: Path) -> None:
    assert LocalDelta is RepositorySnapshotDelta
    assert local_compare is compare_repository_snapshots
    before = _snapshot(tmp_path, {"a.py": "text"})
    after = replace(
        before,
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000023"),
    )
    with pytest.raises(ValueError):
        compare_repository_snapshots(before, after)
