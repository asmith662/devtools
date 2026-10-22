# Copyright (c) 2026
# ruff: noqa: D103
"""Codex-authored public RI regressions for source-declared dependency groups."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.project_configuration import (
    analyze_python_project_configuration,
    resolve_python_project_configuration,
)
from devtools.context.repository.resource import RepositoryResourceAddress

from .test_configuration import _resolve, _snapshot


def test_ordered_raw_strings_and_empty_groups(tmp_path: Path) -> None:
    text = """
[dependency-groups]
"Docs.Build" = ["sphinx>=2", "coverage[toml]", "sphinx>=2"]
QA = ["package @ https://example.org/p.whl", "not a validated spec !", ""]
empty = []
a = ["a"]
42 = ["numeric-name"]
"""
    snapshot = _snapshot(tmp_path, {"pyproject.toml": text})
    result = _resolve(snapshot)
    analysis = result.declarations
    assert analysis.settings is not None
    items = analysis.settings.declarations
    assert [(item.key, item.value, item.unsupported_reason) for item in items] == [
        (("dependency-groups", "42"), ("numeric-name",), None),
        (
            ("dependency-groups", "Docs.Build"),
            ("sphinx>=2", "coverage[toml]", "sphinx>=2"),
            None,
        ),
        (
            ("dependency-groups", "QA"),
            ("package @ https://example.org/p.whl", "not a validated spec !", ""),
            None,
        ),
        (("dependency-groups", "a"), ("a",), None),
        (("dependency-groups", "empty"), (), None),
    ]
    assert analysis.resource == snapshot.resource_at(
        RepositoryResourceAddress("pyproject.toml"),
    )
    assert all(
        item.derivation_identity == analysis.derivation_identity for item in items
    )
    assert len({item.identity for item in items}) == len(items)
    assert not result.facts
    assert not result.assessments
    assert "dependency-group" in analysis.SCOPE
    assert analysis.SCOPE.endswith("v3")
    assert result == _resolve(snapshot)


@pytest.mark.parametrize(
    "literal",
    [
        '"x"',
        "42",
        "true",
        '["x", false]',
        '[{include-group="base"}]',
        '["x", {include-group="base"}]',
        '[{unknown="value"}]',
        '[["x"]]',
        '{x="y"}',
    ],
)
def test_unsupported_groups_retain_whole_group_and_valid_sibling(
    tmp_path: Path,
    literal: str,
) -> None:
    analysis = _resolve(
        _snapshot(
            tmp_path,
            {"pyproject.toml": f"[dependency-groups]\nbase=[]\nbad={literal}"},
        ),
    ).declarations
    assert analysis.settings is not None
    items = {item.key: item for item in analysis.settings.declarations}
    bad = items[("dependency-groups", "bad")]
    assert bad.value is None
    assert bad.unsupported_reason
    assert items[("dependency-groups", "base")].value == ()
    assert items[("dependency-groups", "base")].unsupported_reason is None
    assert ("dependency-groups",) not in analysis.settings.absent_keys


@pytest.mark.parametrize("name", ["", "-x", "x-", "bad name", "é", "x\\n", "."])
def test_invalid_names_are_qualified_without_dropping_original_key(
    tmp_path: Path,
    name: str,
) -> None:
    analysis = _resolve(
        _snapshot(
            tmp_path,
            {"pyproject.toml": f"[dependency-groups]\n{json.dumps(name)}=[]\ngood=[]"},
        ),
    ).declarations
    assert analysis.settings is not None
    bad, good = [
        next(item for item in analysis.settings.declarations if item.key[-1] == key)
        for key in (name, "good")
    ]
    assert bad.value is None
    assert bad.unsupported_reason
    assert good.value == ()
    assert good.unsupported_reason is None


def test_collisions_are_all_unsupported_and_original_names_preserved(
    tmp_path: Path,
) -> None:
    analysis = _resolve(
        _snapshot(
            tmp_path,
            {
                "pyproject.toml": (
                    '[dependency-groups]\n"QA.Test"=["a"]\nqa_test=["b"]\n'
                    '"qa--test"=[]\nsibling=[]'
                ),
            },
        ),
    ).declarations
    assert analysis.settings is not None
    groups = {item.key[-1]: item for item in analysis.settings.declarations}
    assert set(groups) == {"QA.Test", "qa_test", "qa--test", "sibling"}
    for name in ("QA.Test", "qa_test", "qa--test"):
        assert groups[name].value is None
        assert groups[name].unsupported_reason
    assert groups["sibling"].value == ()
    assert groups["sibling"].unsupported_reason is None


@pytest.mark.parametrize(
    ("text", "state"),
    [
        ("", "absent"),
        ("[dependency-groups]", "empty"),
        ("dependency-groups=false", "unsupported"),
        ("dependency-groups=[]", "unsupported"),
    ],
)
def test_absence_empty_table_and_unsupported_parent(
    tmp_path: Path,
    text: str,
    state: str,
) -> None:
    analysis = _resolve(_snapshot(tmp_path, {"pyproject.toml": text})).declarations
    assert analysis.settings is not None
    settings = analysis.settings
    if state == "absent":
        assert ("dependency-groups",) in settings.absent_keys
        assert not settings.declarations
    else:
        assert ("dependency-groups",) not in settings.absent_keys
        assert len(settings.declarations) == 1
        item = settings.declarations[0]
        assert item.key == ("dependency-groups",)
        if state == "empty":
            assert item.value == ()
            assert item.unsupported_reason is None
        else:
            assert item.value is None
            assert item.unsupported_reason


@pytest.mark.parametrize(
    "text",
    ["[dependency-groups", "[dependency-groups]\nx=[]\nx=[]"],
)
def test_malformed_input_cannot_claim_absence(tmp_path: Path, text: str) -> None:
    analysis = _resolve(_snapshot(tmp_path, {"pyproject.toml": text})).declarations
    assert analysis.settings is None
    assert analysis.parse_error == "malformed-toml"
    assert not analysis.absent_selectors
    assert not analysis.declarations


def test_dependency_settings_are_authenticated_by_resolution(tmp_path: Path) -> None:
    text = (
        'project.name="sample"\nproject.dynamic=["readme"]\n'
        '[dependency-groups]\ntest=["pytest"]\n'
        "[tool.pytest.ini_options]\ntestpaths=[]"
    )
    snapshot = _snapshot(tmp_path, {"pyproject.toml": text})
    result = _resolve(snapshot)
    analysis = result.declarations
    assert analysis.settings is not None
    settings = analysis.settings
    assert any(
        item.unsupported_reason == "dynamic-readme" for item in analysis.declarations
    )
    assert ("tool", "pytest", "ini_options") in settings.recognized_tool_tables
    changed = _resolve(
        _snapshot(tmp_path, {"pyproject.toml": text + "\n# identity"}),
    ).declarations
    assert changed.derivation_identity != analysis.derivation_identity
    assert changed.settings is not None
    assert (
        changed.settings.declarations[0].identity != settings.declarations[0].identity
    )
    first, *rest = settings.declarations
    with pytest.raises(ValueError, match="Configuration declarations"):
        resolve_python_project_configuration(
            snapshot,
            replace(
                analysis,
                settings=replace(
                    settings,
                    declarations=(replace(first, value=("forged",)), *rest),
                ),
            ),
            universe=result.universe,
            frame=result.frame,
        )
    assert analysis == analyze_python_project_configuration(
        snapshot,
        address=RepositoryResourceAddress("pyproject.toml"),
    )
