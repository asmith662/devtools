# Copyright (c) 2026
# ruff: noqa: D103
"""Codex-authored regressions for native dependency-group role evidence."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.localization.roles import (
    RepositoryRoleEvidenceInputs,
    RepositoryRoleKind,
    RoleSupportKind,
    derive_repository_role_evidence,
)
from devtools.context.python.project_configuration import (
    analyze_python_project_configuration,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from tests.context.localization.roles.helpers import configuration_targets, snapshot

_R = RepositoryRoleKind
_K = RoleSupportKind
_A = RepositoryResourceAddress


@pytest.mark.parametrize(
    "name",
    ["test", "pytest", "lint", "docs", "build", "Custom-Group"],
)
def test_names_do_not_infer_roles_and_native_source_is_preserved(
    tmp_path: Path,
    name: str,
) -> None:
    content = f'[dependency-groups]\n{name}=["pytest", "pytest", "raw string !"]'
    observed = snapshot(tmp_path, {"pyproject.toml": content, "unrelated.py": ""})
    analysis = analyze_python_project_configuration(
        observed,
        address=_A("pyproject.toml"),
    )
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(analysis,)),
    )
    assert {item.role for item in view.for_resource(_A("pyproject.toml"))} == {
        _R.PROJECT_CONFIGURATION,
    }
    supports = view.supports_for(_A("pyproject.toml"), _R.PROJECT_CONFIGURATION)
    native = [item for item in supports if item.kind is _K.PROJECT_DECLARATION]
    assert len(native) == 1
    assert analysis.settings is not None
    setting = analysis.settings.declarations[0]
    assert native[0].observation == ("dependency-groups", name)
    assert native[0].native_identities == (setting.identity,)
    assert native[0].source_address == analysis.resource.address
    assert view.inputs.configurations == (analysis,)
    assert view.evidence[0].resource == observed.resource_at(
        view.evidence[0].resource.address,
    )
    assert {item.role for item in view.for_resource(_A("unrelated.py"))} == {
        _R.PYTHON_CODE,
    }
    assert view.SEMANTICS == "positive-python-repository-role-support-v2"
    assert view == derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(analysis, analysis)),
    )


@pytest.mark.parametrize(
    ("content", "present"),
    [
        ("", False),
        ("[dependency-groups]", True),
        ("[dependency-groups]\nempty=[]", True),
    ],
)
def test_native_presence_is_distinct_from_absence_without_filename_hints(
    tmp_path: Path,
    content: str,
    *,
    present: bool,
) -> None:
    observed = snapshot(tmp_path, {"settings.toml": content})
    analysis = analyze_python_project_configuration(
        observed,
        address=_A("settings.toml"),
    )
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(analysis,)),
    )
    assert bool(view.evidence) is present
    assert analysis.settings is not None
    if present:
        assert {item.role for item in view.evidence} == {_R.PROJECT_CONFIGURATION}
        support = view.evidence[0].supports[0]
        assert support.kind is _K.PROJECT_DECLARATION
        assert support.native_identities == (
            analysis.settings.declarations[0].identity,
        )
        assert analysis.settings.declarations[0].value == ()
    else:
        assert ("dependency-groups",) in analysis.settings.absent_keys


@pytest.mark.parametrize(
    "content",
    [
        "dependency-groups=false",
        '[dependency-groups]\ninclude=[{include-group="base"}]',
        '[dependency-groups]\nmixed=["a", {include-group="base"}]',
        '[dependency-groups]\n"QA.Test"=[]\nqa_test=[]',
        "[dependency-groups]\ninvalid=42",
        "[dependency-groups",
    ],
)
def test_unsupported_groups_abstain_but_native_evidence_is_retained(
    tmp_path: Path,
    content: str,
) -> None:
    observed = snapshot(tmp_path, {"settings.toml": content})
    analysis = analyze_python_project_configuration(
        observed,
        address=_A("settings.toml"),
    )
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(analysis,)),
    )
    assert not view.evidence
    assert view.inputs.configurations == (analysis,)
    if analysis.settings is not None:
        assert analysis.settings.declarations
        assert all(item.unsupported_reason for item in analysis.settings.declarations)
    else:
        assert analysis.parse_error == "malformed-toml"


def test_mixed_siblings_preserve_independent_support_kinds(tmp_path: Path) -> None:
    content = """
[project]
name = "sample"
[dependency-groups]
test = []
unsupported = [{include-group="test"}]
[build-system]
requires = ["builder"]
[tool.ruff]
[tool.pytest.ini_options]
python_files = ["check_*.py"]
"""
    observed = snapshot(tmp_path, {"pyproject.toml": content})
    targets = configuration_targets(observed)
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configuration_targets=(targets,)),
    )
    assert {item.role for item in view.evidence} == {
        _R.PROJECT_CONFIGURATION,
        _R.BUILD_CONFIGURATION,
        _R.TOOL_CONFIGURATION,
        _R.TEST_CONFIGURATION,
    }
    assert targets.declarations.settings is not None
    settings = {item.key: item for item in targets.declarations.settings.declarations}
    group = settings[("dependency-groups", "test")]
    unsupported = settings[("dependency-groups", "unsupported")]
    supporting = [
        (item.role, support.kind)
        for item in view.evidence
        for support in item.supports
        if group.identity in support.native_identities
    ]
    assert supporting == [(_R.PROJECT_CONFIGURATION, _K.PROJECT_DECLARATION)]
    assert not any(
        unsupported.identity in support.native_identities
        for item in view.evidence
        for support in item.supports
    )
    assert view.inputs.configuration_targets == (targets,)
    assert _K.BUILD_DECLARATION in {
        support.kind for item in view.evidence for support in item.supports
    }
    assert _K.TOOL_TABLE in {
        support.kind for item in view.evidence for support in item.supports
    }
    assert _K.PYTEST_DECLARATION in {
        support.kind for item in view.evidence for support in item.supports
    }


def test_changed_or_forged_native_groups_are_rejected(tmp_path: Path) -> None:
    text = "[dependency-groups]\ntest=[]"
    observed = snapshot(tmp_path, {"pyproject.toml": text})
    analysis = analyze_python_project_configuration(
        observed,
        address=_A("pyproject.toml"),
    )
    assert analysis.settings is not None
    forged = replace(
        analysis,
        settings=replace(
            analysis.settings,
            declarations=(
                replace(analysis.settings.declarations[0], value=("invented",)),
            ),
        ),
    )
    with pytest.raises(ValueError, match="differs from the retained snapshot"):
        derive_repository_role_evidence(
            observed,
            inputs=RepositoryRoleEvidenceInputs(configurations=(forged,)),
        )
    changed = snapshot(
        tmp_path,
        {"pyproject.toml": text + "\n# changed retained bytes"},
    )
    with pytest.raises(ValueError, match="differs from the retained snapshot"):
        derive_repository_role_evidence(
            changed,
            inputs=RepositoryRoleEvidenceInputs(configurations=(analysis,)),
        )
    first = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(analysis,)),
    )
    fresh = analyze_python_project_configuration(changed, address=_A("pyproject.toml"))
    second = derive_repository_role_evidence(
        changed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(fresh,)),
    )
    assert first.derivation_identity != second.derivation_identity
