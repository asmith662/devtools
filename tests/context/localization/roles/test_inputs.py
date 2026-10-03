# Copyright (c) 2026
# ruff: noqa: D103
"""Reject forged or stale native inputs while preserving explicit input scopes."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.localization.roles import (
    RepositoryRoleEvidenceInputs,
    derive_repository_role_evidence,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import RepositorySnapshotId
from tests.context.localization.roles.helpers import configuration_targets, snapshot


@pytest.mark.parametrize(
    "family",
    ["modules", "memberships", "mirrors", "configurations", "configuration_targets"],
)
def test_changed_snapshot_and_repository_reject_each_native_input(
    tmp_path: Path,
    family: str,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "pyproject.toml": '[tool.pytest.ini_options]\ntestpaths = ["tests"]',
            "src/devtools/__init__.py": "",
            "src/devtools/a.py": "",
            "tests/test_a.py": "",
        },
    )
    modules = interpret_python_module_resources(
        observed,
        module_root=PythonModuleRoot("src"),
        resource_addresses=tuple(item.address for item in observed.resources),
    )
    targets = configuration_targets(observed)
    all_inputs = RepositoryRoleEvidenceInputs(
        modules=(modules,),
        memberships=(
            derive_python_immediate_package_memberships(
                observed,
                interpretation_analysis=modules,
            ),
        ),
        mirrors=(derive_python_mirrored_path_correspondences(observed),),
        configurations=(targets.declarations,),
        configuration_targets=(targets,),
    )
    inputs = RepositoryRoleEvidenceInputs(**{family: getattr(all_inputs, family)})
    for changed in (
        replace(
            observed,
            id=RepositorySnapshotId("f" * 64),
        ),
        replace(
            observed,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000077"),
        ),
    ):
        with pytest.raises(ValueError, match=r"snapshot|repository|retained"):
            derive_repository_role_evidence(changed, inputs=inputs)
        original = derive_repository_role_evidence(observed, inputs=inputs)
        fresh = derive_repository_role_evidence(changed)
        assert original.derivation_identity != fresh.derivation_identity
        assert original.evidence[0].identity != fresh.evidence[0].identity


def test_corrupted_native_analyses_rejected_before_support_is_published(
    tmp_path: Path,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "pyproject.toml": '[tool.pytest.ini_options]\ntestpaths = ["tests"]',
            "src/devtools/__init__.py": "",
            "src/devtools/a.py": "",
            "tests/test_a.py": "",
        },
    )
    modules = interpret_python_module_resources(
        observed,
        module_root=PythonModuleRoot("src"),
        resource_addresses=tuple(item.address for item in observed.resources),
    )
    memberships = derive_python_immediate_package_memberships(
        observed,
        interpretation_analysis=modules,
    )
    mirror = derive_python_mirrored_path_correspondences(observed)
    targets = configuration_targets(observed)
    cases = (
        RepositoryRoleEvidenceInputs(
            modules=(
                replace(
                    modules,
                    interpretations=(
                        replace(modules.interpretations[0], dotted_name="invented"),
                        *modules.interpretations[1:],
                    ),
                ),
            ),
        ),
        RepositoryRoleEvidenceInputs(
            memberships=(replace(memberships, memberships=()),),
        ),
        RepositoryRoleEvidenceInputs(mirrors=(replace(mirror, correspondences=()),)),
        RepositoryRoleEvidenceInputs(
            configurations=(replace(targets.declarations, declarations=()),),
        ),
        RepositoryRoleEvidenceInputs(
            configuration_targets=(replace(targets, facts=()),),
        ),
    )
    for inputs in cases:
        with pytest.raises(ValueError, match=r"differs|differ"):
            derive_repository_role_evidence(observed, inputs=inputs)
