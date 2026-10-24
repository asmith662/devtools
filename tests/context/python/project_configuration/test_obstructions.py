# Copyright (c) 2026
# ruff: noqa: D103
"""Codex regressions for present non-table parents, not fabricated absence."""

from pathlib import Path

import pytest

from devtools.context.python.project_configuration import (
    PythonConfigurationSelector,
    PythonConfigurationStatus,
)
from tests.context.python.project_configuration.test_configuration import (
    _resolve,
    _snapshot,
)

_K = PythonConfigurationSelector
_S = PythonConfigurationStatus
_PARENTS = tuple(
    sorted(
        {
            tuple(selector.value.split(".")[:length])
            for selector in _K
            for length in range(1, len(selector.value.split(".")))
        },
    ),
)


@pytest.mark.parametrize("key", _PARENTS)
@pytest.mark.parametrize("value", ["7", "false", '"opaque"', "[1, 2]"])
def test_each_non_table_parent_retains_full_selector_provenance(
    tmp_path: Path,
    key: tuple[str, ...],
    value: str,
) -> None:
    snapshot = _snapshot(tmp_path, {"pyproject.toml": f"{'.'.join(key)} = {value}\n"})
    result = _resolve(snapshot)
    expected = {
        selector
        for selector in _K
        if selector.value.split(".")[: len(key)] == list(key)
    }
    assert result.declarations.parse_error is None
    assert {item.declaration.selector for item in result.assessments} == expected
    assert set(result.declarations.absent_selectors) == set(_K) - expected
    assert not result.facts
    for assessment in result.assessments:
        declaration = assessment.declaration
        assert declaration.selector is not None
        assert declaration.key == tuple(declaration.selector.value.split("."))
        assert declaration.item_ordinal is None
        assert declaration.value is None
        assert declaration.unsupported_reason == "non-table-parent"
        assert (
            declaration.derivation_identity == result.declarations.derivation_identity
        )
        assert assessment.status == _S.UNSUPPORTED
        assert assessment.reason == "non-table-parent"
        assert not assessment.alternatives
    assert len({item.declaration.identity for item in result.assessments}) == len(
        expected,
    )
    assert result == _resolve(snapshot)


def test_valid_adjacent_branches_still_resolve(tmp_path: Path) -> None:
    result = _resolve(
        _snapshot(
            tmp_path,
            {
                "pyproject.toml": (
                    '[project]\nreadme = "README.md"\n'
                    '[tool]\nhatch = false\ncoverage = "opaque"\n'
                    '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'
                    '[tool.mypy]\nfiles = ["src"]\nmypy_path = []\n'
                ),
                "README.md": "readme",
                "tests/test_example.py": "",
                "src/example.py": "",
            },
        ),
    )
    statuses = {item.declaration.selector: item.status for item in result.assessments}
    assert statuses == {
        _K.README: _S.RESOLVED,
        _K.HATCH_PACKAGES: _S.UNSUPPORTED,
        _K.PYTEST_TESTPATHS: _S.RESOLVED,
        _K.COVERAGE_SOURCE: _S.UNSUPPORTED,
        _K.MYPY_FILES: _S.RESOLVED,
    }
    assert {item.declaration.selector for item in result.facts} == {
        _K.README,
        _K.PYTEST_TESTPATHS,
        _K.MYPY_FILES,
    }
    assert not result.declarations.absent_selectors


@pytest.mark.parametrize(
    "text",
    ["", "[tool]\n", "[tool.pytest]\n", "[tool.other]\nx=false\n"],
)
def test_genuine_absence_is_not_an_obstruction(tmp_path: Path, text: str) -> None:
    result = _resolve(_snapshot(tmp_path, {"pyproject.toml": text}))
    assert set(result.declarations.absent_selectors) == set(_K)
    assert not result.assessments
    assert not result.facts


@pytest.mark.parametrize(
    ("value", "reason"),
    [
        ("42", "unsupported-value-form"),
        ('"tests"', "expected-array"),
        ("{}", "unsupported-value-form"),
    ],
)
def test_present_unsupported_leaf_retains_existing_reason(
    tmp_path: Path,
    value: str,
    reason: str,
) -> None:
    result = _resolve(
        _snapshot(
            tmp_path,
            {"pyproject.toml": f"tool.pytest.ini_options.testpaths = {value}\n"},
        ),
    )
    assert len(result.assessments) == 1
    assessment = result.assessments[0]
    assert assessment.declaration.key == ("tool", "pytest", "ini_options", "testpaths")
    assert assessment.status == _S.UNSUPPORTED
    assert assessment.reason == reason
    assert _K.PYTEST_TESTPATHS not in result.declarations.absent_selectors
    assert not result.facts


def test_empty_array_and_dynamic_readme_survive_adjacent_obstruction(
    tmp_path: Path,
) -> None:
    result = _resolve(
        _snapshot(
            tmp_path,
            {
                "pyproject.toml": (
                    '[project]\nreadme = "README.md"\ndynamic = ["version", "readme"]\n'
                    "[tool]\nhatch = false\n[tool.pytest.ini_options]\ntestpaths = []\n"
                ),
                "README.md": "readme",
            },
        ),
    )
    assert _K.PYTEST_TESTPATHS not in result.declarations.absent_selectors
    assert [
        (item.declaration.key, item.declaration.item_ordinal, item.reason)
        for item in result.assessments
    ] == [
        (("project", "readme"), None, "dynamic-readme"),
        (
            ("tool", "hatch", "build", "targets", "wheel", "packages"),
            None,
            "non-table-parent",
        ),
        (("project", "dynamic"), 1, "dynamic-readme"),
    ]
    assert all(item.status == _S.UNSUPPORTED for item in result.assessments)
    assert not result.facts


@pytest.mark.parametrize("text", ["[tool\n", "tool=false\ntool=false\n"])
def test_malformed_toml_never_claims_absence_or_obstructions(
    tmp_path: Path,
    text: str,
) -> None:
    result = _resolve(_snapshot(tmp_path, {"pyproject.toml": text}))
    assert result.declarations.parse_error == "malformed-toml"
    assert not result.declarations.absent_selectors
    assert not result.declarations.declarations
    assert not result.assessments
    assert not result.facts


def test_obstruction_identity_tracks_exact_retained_configuration(
    tmp_path: Path,
) -> None:
    old_snapshot = _snapshot(tmp_path, {"pyproject.toml": "tool=false\n"})
    old = _resolve(old_snapshot)
    changed = _resolve(_snapshot(tmp_path, {"pyproject.toml": "tool=7\n"}))
    assert (
        old.declarations.derivation_identity != changed.declarations.derivation_identity
    )
    assert old.derivation_identity != changed.derivation_identity
    assert {item.declaration.identity for item in old.assessments}.isdisjoint(
        item.declaration.identity for item in changed.assessments
    )
    # Later filesystem changes cannot rewrite the old retained observation.
    assert old == _resolve(old_snapshot)
