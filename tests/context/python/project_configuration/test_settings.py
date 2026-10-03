# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Exercise bounded declarations independently of repository path conventions."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.project_configuration import (
    PythonConfigurationDeclarationAnalysis,
    PythonConfigurationSetting,
    analyze_python_project_configuration,
    resolve_python_project_configuration,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshotId

from .test_configuration import _resolve, _snapshot


def _analyze(tmp_path: Path, content: str) -> PythonConfigurationDeclarationAnalysis:
    snapshot = _snapshot(tmp_path, {"project.toml": content})
    return analyze_python_project_configuration(
        snapshot,
        address=RepositoryResourceAddress("project.toml"),
    )


def test_supported_build_project_and_tool_declarations(tmp_path: Path) -> None:
    analysis = _analyze(
        tmp_path,
        """
[build-system]
requires = ["builder>=1", "helper", "helper"]
build-backend = "builder.api"
backend-path = ["backend"]
[project]
name = "sample"
version = "1.2"
description = "description"
requires-python = ">=3.12"
dependencies = ["dependency>=2"]
dynamic = []
[project.scripts]
command = "sample:main"
[project.gui-scripts]
window = "sample:window"
[project.entry-points."example.group"]
plugin = "sample.plugin:factory"
[tool.mypy]
strict = true
[tool.ruff.lint]
select = ["ALL"]
[tool.coverage.run]
branch = true
[tool.coverage.report]
fail_under = 100
[tool.hatch.build.targets.wheel]
packages = []
[tool.unknown]
foo = "bar"
""",
    )
    settings = analysis.settings
    assert settings is not None
    values = {item.key: item.value for item in settings.declarations}
    assert values[("build-system", "requires")] == ("builder>=1", "helper", "helper")
    assert values[("build-system", "backend-path")] == ("backend",)
    assert values[("project", "scripts", "command")] == "sample:main"
    assert values[("project", "gui-scripts", "window")] == "sample:window"
    assert values[("project", "entry-points", "example.group", "plugin")] == (
        "sample.plugin:factory"
    )
    assert not any(item.unsupported_reason for item in settings.declarations)
    assert settings.recognized_tool_tables == (
        ("tool", "coverage", "run"),
        ("tool", "coverage", "report"),
        ("tool", "hatch", "build", "targets", "wheel"),
        ("tool", "mypy"),
        ("tool", "ruff"),
        ("tool", "ruff", "lint"),
    )
    assert len(values) == 12
    assert len({item.identity for item in settings.declarations}) == len(values)
    assert all(
        item.derivation_identity == analysis.derivation_identity
        for item in settings.declarations
    )
    assert tuple(values) == tuple(sorted(values))
    assert not hasattr(settings.declarations[0], "start_line")


def test_pytest_patterns_exclusions_and_opaque_arguments(tmp_path: Path) -> None:
    analysis = _analyze(
        tmp_path,
        """
[tool.pytest.ini_options]
testpaths = ["checks", "checks"]
python_files = ["check_*.py", "*_spec.py", "check_*.py"]
python_classes = "Check* Spec"
python_functions = ["check_*", "spec_*", ""]
norecursedirs = ["generated", "vendor*"]
addopts = "--ignore=checks/slow --ignore-glob='*_external.py'"
""",
    )
    assert analysis.settings is not None
    values = {item.key[-1]: item.value for item in analysis.settings.declarations}
    assert values == {
        "python_files": ("check_*.py", "*_spec.py", "check_*.py"),
        "python_classes": "Check* Spec",
        "python_functions": ("check_*", "spec_*", ""),
        "norecursedirs": ("generated", "vendor*"),
        "addopts": "--ignore=checks/slow --ignore-glob='*_external.py'",
    }
    assert [item.value for item in analysis.declarations] == ["checks", "checks"]
    assert len({item.identity for item in analysis.declarations}) == 2
    assert ("tool", "pytest", "ini_options") in (
        analysis.settings.recognized_tool_tables
    )
    assert not hasattr(analysis.settings, "tests")


@pytest.mark.parametrize("content", ["", "[tool.other]\nkey=1"])
def test_supported_absence_is_bounded_to_named_keys(
    tmp_path: Path,
    content: str,
) -> None:
    result = _analyze(tmp_path, content)
    assert result.settings is not None
    assert not result.settings.declarations
    assert len(result.settings.absent_keys) == 17
    assert not result.settings.recognized_tool_tables
    assert len(result.absent_selectors) == 6


@pytest.mark.parametrize("content", ["[project", "project.name='a'\nproject.name='b'"])
def test_malformed_toml_cannot_claim_setting_absence(
    tmp_path: Path,
    content: str,
) -> None:
    analysis = _analyze(tmp_path, content)
    assert analysis.parse_error == "malformed-toml"
    assert analysis.settings is None
    assert not analysis.absent_selectors


@pytest.mark.parametrize(
    ("assignment", "reason", "value"),
    [
        ('project.name = ["name"]', "unsupported-value-form", None),
        ('build-system.requires = "builder"', "expected-string-array", "builder"),
        ('project.dependencies = ["ok", 42]', "unsupported-value-form", None),
        ("tool.pytest.ini_options.python_files = 42", "unsupported-value-form", None),
        (
            "tool.pytest.ini_options.python_functions = [false]",
            "unsupported-value-form",
            None,
        ),
        (
            'tool.pytest.ini_options.norecursedirs = {path="vendor"}',
            "unsupported-value-form",
            None,
        ),
        ("project = 42", "non-table-parent", None),
        ('tool.pytest = "invalid"', "non-table-parent", None),
    ],
)
def test_unsupported_shapes_keep_source_and_do_not_claim_absence(
    tmp_path: Path,
    assignment: str,
    reason: str,
    value: str | None,
) -> None:
    analysis = _analyze(tmp_path, assignment)
    assert analysis.settings is not None
    assert analysis.resource.content == assignment
    matching = [
        item
        for item in analysis.settings.declarations
        if item.unsupported_reason == reason
    ]
    assert matching
    assert all(item.value == value for item in matching)
    assert all(item.key not in analysis.settings.absent_keys for item in matching)


def test_entrypoint_tables_invalid_shapes_reserved_groups_and_empty_tables(
    tmp_path: Path,
) -> None:
    analysis = _analyze(
        tmp_path,
        """
[project]
scripts = "invalid"
gui-scripts = {}
[project.entry-points]
broken = "invalid"
empty = {}
console_scripts = {command = "pkg:main"}
gui_scripts = {}
[project.entry-points.valid]
"a.b" = "pkg:main"
invalid = ["pkg:main"]
""",
    )
    assert analysis.settings is not None
    declarations = {item.key: item for item in analysis.settings.declarations}
    assert declarations[("project", "scripts")].unsupported_reason == "expected-table"
    assert declarations[("project", "gui-scripts")].value == ()
    assert declarations[("project", "entry-points", "empty")].value == ()
    assert declarations[("project", "entry-points", "broken")].unsupported_reason
    assert declarations[
        ("project", "entry-points", "console_scripts")
    ].unsupported_reason == ("reserved-entrypoint-group")
    assert declarations[("project", "entry-points", "gui_scripts")].unsupported_reason
    assert declarations[("project", "entry-points", "valid", "a.b")].value == "pkg:main"
    assert declarations[
        ("project", "entry-points", "valid", "invalid")
    ].unsupported_reason
    assert not analysis.declarations  # no duplicate unsupported entrypoint derivation


def test_dynamic_values_are_declarations_not_effective_metadata(tmp_path: Path) -> None:
    analysis = _analyze(
        tmp_path,
        """
[project]
version = "1.0"
dynamic = ["version", "description"]
""",
    )
    assert analysis.settings is not None
    declarations = {item.key: item for item in analysis.settings.declarations}
    assert declarations[("project", "version")].value == "1.0"
    assert (
        declarations[("project", "version")].unsupported_reason
        == "dynamic-project-field"
    )
    assert ("project", "description") in analysis.settings.absent_keys


def test_identity_binds_snapshot_repository_resource_shape_and_retained_content(
    tmp_path: Path,
) -> None:
    first = _analyze(tmp_path, 'project.name="sample"')
    assert first == _analyze(tmp_path, 'project.name="sample"')
    assert first.settings is not None
    setting = first.settings.declarations[0]
    assert setting.identity != replace(setting, value=("sample",)).identity
    assert setting.identity != replace(setting, key=("project.name",)).identity
    assert (
        setting.identity != replace(setting, unsupported_reason="unsupported").identity
    )
    # An invalid value remains distinguished by exact retained source dependency.
    assert _analyze(tmp_path, "project.name=42").derivation_identity != (
        _analyze(tmp_path, "project.name=43").derivation_identity
    )
    snapshot = _snapshot(tmp_path, {"project.toml": 'project.name="sample"'})
    (tmp_path / "project.toml").write_text("invalid [", encoding="utf-8")
    assert (
        analyze_python_project_configuration(
            snapshot,
            address=RepositoryResourceAddress("project.toml"),
        )
        == first
    )
    for changed in (
        replace(
            snapshot,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000048"),
        ),
        replace(snapshot, id=RepositorySnapshotId("0" * 64)),
        _snapshot(tmp_path, {"other.toml": 'project.name="sample"'}),
    ):
        result = analyze_python_project_configuration(
            changed,
            address=changed.resources[0].address,
        )
        assert result.settings is not None
        assert result.settings.declarations[0].identity != setting.identity


def test_dynamic_entrypoints_are_retained_without_effective_binding_claims(
    tmp_path: Path,
) -> None:
    result = _analyze(
        tmp_path,
        """
[project]
dynamic = ["scripts", "gui-scripts", "entry-points"]
gui-scripts = {}
[project.scripts]
command = "sample:main"
[project.entry-points.group]
plugin = "sample:plugin"
""",
    )
    assert result.settings is not None
    declarations = {item.key: item for item in result.settings.declarations}
    assert declarations[("project", "scripts", "command")].value == "sample:main"
    assert declarations[("project", "gui-scripts")].value == ()
    assert declarations[("project", "entry-points", "group", "plugin")].value == (
        "sample:plugin"
    )
    assert all(
        item.unsupported_reason == "dynamic-project-field"
        for key, item in declarations.items()
        if key != ("project", "dynamic")
    )


def test_resolution_rejects_forged_or_duplicate_setting_declarations(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(tmp_path, {"pyproject.toml": 'project.name="sample"'})
    result = _resolve(snapshot)
    settings = result.declarations.settings
    assert settings is not None
    for declarations in (
        (*settings.declarations, settings.declarations[0]),
        (replace(settings.declarations[0], value="forged"),),
    ):
        with pytest.raises(ValueError, match="Configuration declarations"):
            resolve_python_project_configuration(
                snapshot,
                replace(
                    result.declarations,
                    settings=replace(settings, declarations=declarations),
                ),
                universe=result.universe,
            )


def test_setting_identity_distinguishes_absent_value_and_empty_string() -> None:
    setting = PythonConfigurationSetting("derivation", ("project", "name"), "", None)
    assert setting.identity != replace(setting, value=None).identity


def test_table_order_does_not_change_setting_order(tmp_path: Path) -> None:
    first = _analyze(tmp_path, '[project.scripts]\nb="pkg:b"\na="pkg:a"')
    second = _analyze(tmp_path, '[project.scripts]\na="pkg:a"\nb="pkg:b"')
    assert first.settings is not None
    assert second.settings is not None
    assert [(item.key, item.value) for item in first.settings.declarations] == [
        (item.key, item.value) for item in second.settings.declarations
    ]
    assert first.derivation_identity != second.derivation_identity
