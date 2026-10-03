# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Keep configuration presence and bounded matching separate from collection."""

from pathlib import Path

import pytest

from devtools.context.localization.roles import (
    RepositoryRoleEvidenceInputs,
    RepositoryRoleKind,
    RoleSupportKind,
    derive_repository_role_evidence,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from tests.context.localization.roles.helpers import configuration_targets, snapshot

_R = RepositoryRoleKind
_K = RoleSupportKind
_A = RepositoryResourceAddress


def test_supported_metadata_tables_and_targets_have_distinct_native_bases(
    tmp_path: Path,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "pyproject.toml": """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
[project]
name = "synthetic"
readme = "guide.txt"
[project.scripts]
run = "pkg:main"
[tool.pytest.ini_options]
testpaths = ["specs", "specs"]
python_files = ["check_*.py", "*_spec.py", "check_*.py"]
python_classes = ["Example*"]
python_functions = ["check_*"]
norecursedirs = ["generated"]
addopts = "--ignore=specs/check_ignored.py"
[tool.ruff.lint]
[tool.mypy]
files = ["pkg"]
[tool.coverage.run]
source = ["pkg"]
[tool.hatch.build.targets.wheel]
packages = ["pkg"]
""",
            "specs/check_one.py": "",
            "specs/another_spec.py": "",
            "specs/helper.py": "",
            "specs/check_ignored.py": "",
            "specs/check_one.txt": "",
            "outside/check_one.py": "",
            "pkg/__init__.py": "",
            "guide.txt": "",
        },
    )
    targets = configuration_targets(observed)
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(
            configuration_targets=(targets, targets),
            configurations=(targets.declarations,),
        ),
    )
    roles = {item.role for item in view.for_resource(_A("pyproject.toml"))}
    assert roles == {
        _R.PROJECT_CONFIGURATION,
        _R.BUILD_CONFIGURATION,
        _R.TEST_CONFIGURATION,
        _R.TOOL_CONFIGURATION,
    }
    assert (
        len(view.inputs.configurations) == len(view.inputs.configuration_targets) == 1
    )
    assert {
        _K.BUILD_DECLARATION,
        _K.PROJECT_DECLARATION,
        _K.PYTEST_DECLARATION,
        _K.TOOL_DECLARATION,
        _K.TOOL_TABLE,
    } <= {
        item.kind
        for item in view.supports_for(_A("pyproject.toml"), _R.PROJECT_CONFIGURATION)
    }
    match = view.supports_for(_A("specs/check_one.py"), _R.TEST)
    assert {_K.PYTEST_TESTPATH_TARGET, _K.PYTEST_BASENAME_GLOB} == {
        item.kind for item in match
    }
    assert len([item for item in match if item.kind is _K.PYTEST_BASENAME_GLOB]) == 4
    assert all(
        item.source_address == _A("pyproject.toml") and item.native_identities
        for item in match
    )
    assert any(
        item.kind is _K.PYTEST_BASENAME_GLOB
        for item in view.supports_for(_A("specs/another_spec.py"), _R.TEST)
    )
    assert {
        item.kind for item in view.supports_for(_A("specs/helper.py"), _R.TEST)
    } == {_K.PYTEST_TESTPATH_TARGET}
    assert {
        item.kind for item in view.supports_for(_A("specs/check_one.txt"), _R.TEST)
    } == {_K.PYTEST_TESTPATH_TARGET}
    assert any(
        item.kind is _K.PYTEST_BASENAME_GLOB
        for item in view.supports_for(_A("specs/check_ignored.py"), _R.TEST)
    )
    assert not view.supports_for(_A("outside/check_one.py"), _R.TEST)
    assert not view.supports_for(_A("pkg/__init__.py"), _R.TEST)
    assert (
        view.supports_for(_A("guide.txt"), _R.DOCUMENTATION)[0].kind is _K.README_TARGET
    )
    assert not view.limitations
    assert view == derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configuration_targets=(targets,)),
    )


@pytest.mark.parametrize(
    "config",
    ["", "broken [", "[project]\nname = 1\nreadme = 2", "[tool]\npytest = 2"],
)
def test_absent_malformed_and_unsupported_declarations_abstain(
    tmp_path: Path,
    config: str,
) -> None:
    observed = snapshot(tmp_path, {"pyproject.toml": config, "outside.py": ""})
    targets = configuration_targets(observed)
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(targets.declarations,)),
    )
    assert {item.role for item in view.for_resource(_A("pyproject.toml"))} == {
        _R.PROJECT_CONFIGURATION,
    }
    assert (
        view.supports_for(_A("pyproject.toml"), _R.PROJECT_CONFIGURATION)[0].kind
        is _K.PYPROJECT_NAME_CONVENTION
    )
    assert not view.supports_for(_A("outside.py"), _R.TEST)
    assert not view.inputs.configuration_targets


@pytest.mark.parametrize(
    ("value", "reason"),
    [
        ('"check_*.py *_spec.py"', "scalar-pattern-syntax-not-interpreted"),
        ("[1]", "unsupported-value-form"),
        ('["check_*.py"]', "no-supplied-testpaths-targets"),
    ],
)
def test_pattern_forms_and_missing_target_scope_remain_explicit(
    tmp_path: Path,
    value: str,
    reason: str,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "pyproject.toml": f"[tool.pytest.ini_options]\npython_files = {value}",
            "check_one.py": "",
        },
    )
    targets = configuration_targets(observed)
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configurations=(targets.declarations,)),
    )
    assert view.limitations[0].reason == reason
    assert not view.supports_for(_A("check_one.py"), _R.TEST)
    assert {
        item.kind
        for item in view.supports_for(_A("pyproject.toml"), _R.TEST_CONFIGURATION)
    } >= {_K.TOOL_TABLE}


def test_globs_are_bounded_case_sensitive_observations_and_conventions_survive(
    tmp_path: Path,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "pyproject.toml": """[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = [
"", "dir/*.py", "dir\\\\*.py", "bad\\u0001*.py", "bad\\u007f*.py", "check_[ab]?.py"
]
""",
            "tests/check_a1.py": "",
            "tests/CHECK_a1.py": "",
            "tests/other.py": "",
            "tests/check_b2.txt": "",
            "outside/check_a1.py": "",
        },
    )
    targets = configuration_targets(observed)
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configuration_targets=(targets,)),
    )
    assert len(view.limitations) == 5
    assert all(
        item.reason == "outside-basename-pattern-scope" for item in view.limitations
    )
    kinds = {item.kind for item in view.supports_for(_A("tests/check_a1.py"), _R.TEST)}
    assert kinds == {
        _K.TEST_DIRECTORY_CONVENTION,
        _K.PYTEST_TESTPATH_TARGET,
        _K.PYTEST_BASENAME_GLOB,
    }
    assert _K.PYTEST_BASENAME_GLOB not in {
        item.kind for item in view.supports_for(_A("tests/CHECK_a1.py"), _R.TEST)
    }
    assert not view.supports_for(_A("outside/check_a1.py"), _R.TEST)
    assert len(view.resources) == len(observed.resources)


def test_nested_configuration_uses_native_tool_root_and_retained_content(
    tmp_path: Path,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "nested/pyproject.toml": """[tool.pytest.ini_options]
testpaths = ["specs"]
python_files = ["check_*.py"]""",
            "nested/specs/check_one.py": "",
            "specs/check_one.py": "",
        },
    )
    targets = configuration_targets(observed, "nested/pyproject.toml", "nested")
    (tmp_path / "nested/pyproject.toml").write_text("broken [", encoding="utf-8")
    view = derive_repository_role_evidence(
        observed,
        inputs=RepositoryRoleEvidenceInputs(configuration_targets=(targets,)),
    )
    assert view.supports_for(_A("nested/specs/check_one.py"), _R.TEST)
    assert not view.supports_for(_A("specs/check_one.py"), _R.TEST)
