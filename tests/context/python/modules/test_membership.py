# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Tests for qualified immediate observed Python package membership."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.modules import (
    PythonImmediatePackageMembershipStatus,
    PythonModuleInterpretationAnalysis,
    PythonModuleKind,
    PythonModuleRoot,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath


def _snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000030"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _interpret(
    snapshot: RepositorySnapshot,
    root: str = ".",
) -> PythonModuleInterpretationAnalysis:
    return interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot(root),
        resource_addresses=tuple(item.address for item in snapshot.resources),
    )


def test_immediate_membership_and_both_directional_queries(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "pkg/__init__.py": "# package\n",
            "pkg/a.py": "",
            "pkg/b.py": "",
            "pkg/nested/__init__.py": "",
            "pkg/nested/child.py": "",
        },
    )
    interpretation = _interpret(snapshot)
    result = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=interpretation,
    )
    by_name = {item.dotted_name: item for item in interpretation.interpretations}
    parent = by_name["pkg"]
    assert parent.kind is PythonModuleKind.PACKAGE
    assert result.immediate_package_of(by_name["pkg.a"]) is not None
    assert {item.child.dotted_name for item in result.immediate_members_of(parent)} == {
        "pkg.a",
        "pkg.b",
        "pkg.nested",
    }
    nested_membership = result.immediate_package_of(by_name["pkg.nested.child"])
    assert nested_membership is not None
    assert nested_membership.package == by_name["pkg.nested"]
    assert all(
        item.package != parent
        for item in result.immediate_members_of(by_name["pkg.nested"])
    )
    assert all(item.child.snapshot_id == snapshot.id for item in result.memberships)
    assert all(item.package.snapshot_id == snapshot.id for item in result.memberships)
    assert all(
        item.child.resource == snapshot.resource_at(item.child.resource.address)
        for item in result.memberships
    )
    assert all(
        item.package.resource == snapshot.resource_at(item.package.resource.address)
        for item in result.memberships
    )
    assert len({item.identity for item in result.memberships}) == 4
    assert result == derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=interpretation,
    )
    assert result.coverage.established_count == 4
    assert result.coverage.assessment_count == 5


def test_missing_non_package_and_excluded_are_distinct(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "lonely/child.py": "",
            "ordinary.py": "",
            "ordinary/child.py": "",
            "notes.txt": "",
        },
    )
    result = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=_interpret(snapshot),
    )
    states = {item.child.dotted_name: item.status for item in result.assessments}
    assert (
        states["lonely.child"]
        is PythonImmediatePackageMembershipStatus.MISSING_OBSERVED_PACKAGE
    )
    assert (
        states["ordinary.child"]
        is PythonImmediatePackageMembershipStatus.PARENT_NOT_PACKAGE
    )
    assert (
        states["ordinary"] is PythonImmediatePackageMembershipStatus.NO_PARENT_COMPONENT
    )
    assert not result.memberships
    assert result.coverage.excluded_count == 1
    assert str(result.exclusions[0].resource.address) == "notes.txt"
    assert result.coverage.IS_EXHAUSTIVE_FOR_SELECTION


def test_explicit_root_is_necessary_for_parent_match(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "",
            "src/pkg/child.py": "",
        },
    )
    relative = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=_interpret(snapshot, "src"),
    )
    rooted = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=_interpret(snapshot, "."),
    )
    assert relative.memberships[0].child.dotted_name == "pkg.child"
    assert rooted.memberships[0].child.dotted_name == "src.pkg.child"
    assert rooted.memberships[0].package.dotted_name == "src.pkg"
    assert relative.memberships[0].child.module_root == PythonModuleRoot("src")
    assert rooted.memberships[0].child.module_root == PythonModuleRoot(".")
    assert relative.memberships[0].identity != rooted.memberships[0].identity


def test_ordinary_name_collision_does_not_replace_unique_package(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "pkg.py": "",
            "pkg/__init__.py": "",
            "pkg/child.py": "",
        },
    )
    result = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=_interpret(snapshot),
    )
    child = next(
        item for item in result.assessments if item.child.dotted_name == "pkg.child"
    )
    assert child.status is PythonImmediatePackageMembershipStatus.ESTABLISHED
    assert len(child.observed_name_matches) == 2
    assert child.membership is not None
    assert child.membership.package.kind is PythonModuleKind.PACKAGE


def test_ambiguous_package_candidates_establish_no_membership(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "pkg/__init__.py": "",
            "other/__init__.py": "",
            "pkg/child.py": "",
        },
    )
    analysis = _interpret(snapshot)
    # The current path interpreter cannot produce this collision from one
    # root; preserve defined behavior if a supplied interpretation set does.
    other = next(
        item for item in analysis.interpretations if item.dotted_name == "other"
    )
    competing = replace(other, dotted_name="pkg")
    supplied = replace(
        analysis,
        interpretations=(*analysis.interpretations, competing),
    )
    result = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=supplied,
    )
    child = next(
        item for item in result.assessments if item.child.dotted_name == "pkg.child"
    )
    assert child.status is PythonImmediatePackageMembershipStatus.AMBIGUOUS_PACKAGE
    assert len(child.observed_name_matches) == 2
    assert child.membership is None


def test_snapshot_or_root_mismatch_is_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"pkg/__init__.py": "", "pkg/child.py": ""})
    analysis = _interpret(snapshot)
    newer = _snapshot(tmp_path, {"pkg/__init__.py": "# changed\n", "pkg/child.py": ""})
    with pytest.raises(ValueError, match="snapshot"):
        derive_python_immediate_package_memberships(
            newer,
            interpretation_analysis=analysis,
        )
    wrong_root = replace(analysis, module_root=PythonModuleRoot("pkg"))
    with pytest.raises(ValueError, match="root"):
        derive_python_immediate_package_memberships(
            snapshot,
            interpretation_analysis=wrong_root,
        )
