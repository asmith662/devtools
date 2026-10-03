# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Exercise configuration syntax, frames, provenance and competing readings."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.project_configuration import (
    PythonConfigurationFrame,
    PythonConfigurationResolutionAnalysis,
    PythonConfigurationSelector,
    PythonConfigurationStatus,
    analyze_python_project_configuration,
    resolve_python_project_configuration,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.core.paths import ResolvedPath

_ROOT = PythonModuleRoot(".")
_FRAME = PythonConfigurationFrame(_ROOT, _ROOT)
_S = PythonConfigurationStatus


def _snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000047"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _resolve(
    snapshot: RepositorySnapshot,
    *,
    config: str = "pyproject.toml",
    roots: tuple[PythonModuleRoot, ...] = (_ROOT,),
    frame: PythonConfigurationFrame = _FRAME,
) -> PythonConfigurationResolutionAnalysis:
    declarations = analyze_python_project_configuration(
        snapshot,
        address=RepositoryResourceAddress(config),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=tuple(
            module
            for root in roots
            for module in interpret_python_module_resources(
                snapshot,
                module_root=root,
                resource_addresses=tuple(item.address for item in snapshot.resources),
            ).interpretations
        ),
    )
    return resolve_python_project_configuration(
        snapshot,
        declarations,
        universe=universe,
        frame=frame,
    )


def test_actual_project_selectors_retained_content_and_coverage(tmp_path: Path) -> None:
    project = Path("pyproject.toml").read_text(encoding="utf-8")
    snapshot = _snapshot(
        tmp_path,
        {
            "pyproject.toml": project,
            "README.md": "project readme",
            "src/devtools/__init__.py": "",
            "src/devtools/a.py": "",
            "tests/test_a.py": "",
            "experiments/example.py": "",
            "testsmith/test_a.py": "distractor",
        },
    )
    (tmp_path / "pyproject.toml").write_text("broken [", encoding="utf-8")
    result = _resolve(snapshot, roots=(PythonModuleRoot("src"),))
    assert len(result.assessments) == 8
    assert all(item.status == _S.RESOLVED for item in result.assessments)
    assert not result.declarations.absent_selectors
    assert result.declarations.parse_error is None
    assert {item.declaration.selector for item in result.facts} == set(
        PythonConfigurationSelector,
    )
    assert all(
        item.configuration
        == snapshot.resource_at(RepositoryResourceAddress("pyproject.toml"))
        for item in result.facts
    )
    assert not any(
        item.target.address.value.startswith("testsmith/") for item in result.facts
    )
    coverage = next(
        item
        for item in result.assessments
        if item.declaration.selector == PythonConfigurationSelector.COVERAGE_SOURCE
    )
    assert [item.status for item in coverage.alternatives] == [
        _S.MISSING_IN_FRAME,
        _S.RESOLVED,
    ]
    assert result.facts[-1].requested == "src"
    assert len({item.identity for item in result.facts}) == len(result.facts)
    assert result == _resolve(snapshot, roots=(PythonModuleRoot("src"),))


def test_separate_nested_config_and_command_frames_and_duplicates(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "nested/pyproject.toml": """[project]
readme = "README.md"
[tool.hatch.build.targets.wheel]
packages = ["pkg", "pkg"]
[tool.pytest.ini_options]
testpaths = ["tests"]
[tool.mypy]
files = ["file.py", ".", "missing"]
mypy_path = ["src"]
""",
            "nested/README.md": "",
            "nested/pkg/a.py": "",
            "nested/pkg/b.py": "",
            "nested/src/a.py": "",
            "command/file.py": "",
            "command/src/a.py": "",
            "testroot/tests/test_a.py": "",
        },
    )
    result = _resolve(
        snapshot,
        config="nested/pyproject.toml",
        frame=PythonConfigurationFrame(
            PythonModuleRoot("command"),
            PythonModuleRoot("testroot"),
        ),
    )
    assert [item.status for item in result.assessments] == [
        _S.RESOLVED,
        _S.RESOLVED,
        _S.RESOLVED,
        _S.RESOLVED,
        _S.RESOLVED,
        _S.RESOLVED,
        _S.MISSING_IN_FRAME,
        _S.RESOLVED,
    ]
    packages = [
        item
        for item in result.assessments
        if item.declaration.selector == PythonConfigurationSelector.HATCH_PACKAGES
    ]
    assert [item.declaration.item_ordinal for item in packages] == [0, 1]
    assert packages[0].declaration.identity != packages[1].declaration.identity
    assert len(packages[0].alternatives[0].resources) == 2
    assert result.facts[0].target.address.value == "nested/README.md"
    assert result.facts[-1].target.address.value == "command/src/a.py"
    missing_frames = _resolve(
        snapshot,
        config="nested/pyproject.toml",
        frame=PythonConfigurationFrame(),
    )
    assert all(item.status == _S.UNSUPPORTED for item in missing_frames.assessments[3:])
    changed = _resolve(snapshot, config="nested/pyproject.toml", frame=_FRAME)
    assert result.derivation_identity != changed.derivation_identity


@pytest.mark.parametrize(
    "value",
    [
        "*.py",
        "$ROOT/src",
        "~/src",
        "{src}",
        "a?",
        "a[b]",
        "/src",
        "C:/src",
        "../src",
        "./src",
        "",
        "a//b",
        "a\\b",
        "a\nb",
        "a\tb",
        "a\x00b",
        "a\x7fb",
    ],
)
def test_unsupported_literals(tmp_path: Path, value: str) -> None:
    # JSON string escaping is compatible for these TOML basic-string fixtures.
    snapshot = _snapshot(
        tmp_path,
        {"pyproject.toml": "[tool.mypy]\nfiles = [" + json.dumps(value) + "]"},
    )
    result = _resolve(snapshot)
    assert result.assessments[0].status == _S.UNSUPPORTED
    assert result.assessments[0].alternatives[0].reason
    assert not result.facts


@pytest.mark.parametrize("content", ["[project", '[project]\nreadme="a"\nreadme="b"'])
def test_invalid_toml_never_publishes_declarations_or_facts(
    tmp_path: Path,
    content: str,
) -> None:
    result = _resolve(_snapshot(tmp_path, {"pyproject.toml": content}))
    assert result.declarations.parse_error == "malformed-toml"
    assert not result.declarations.declarations
    assert not result.declarations.absent_selectors
    assert not result.assessments
    assert not result.facts


@pytest.mark.parametrize(
    "content",
    [
        '[project]\nreadme={file="README.md", "content-type"="text/markdown"}',
        "[project]\nreadme=42",
        '[tool.mypy]\nfiles="src"',
        '[tool.mypy]\nfiles=[42, false, {path="src"}]',
        '[project]\ndynamic=["readme"]',
        '[project]\nreadme="README.md"\ndynamic=["readme"]',
    ],
)
def test_unsupported_selector_forms_and_dynamic_readme(
    tmp_path: Path,
    content: str,
) -> None:
    result = _resolve(_snapshot(tmp_path, {"pyproject.toml": content, "README.md": ""}))
    assert result.assessments
    assert all(item.status == _S.UNSUPPORTED for item in result.assessments)
    assert not result.facts
    assert all(item.declaration.identity for item in result.assessments)


def test_empty_arrays_absent_keys_and_non_table_nodes(tmp_path: Path) -> None:
    result = _resolve(
        _snapshot(
            tmp_path,
            {"pyproject.toml": "[tool.mypy]\nfiles=[]\n[project]\ndynamic=[]"},
        ),
    )
    assert not result.assessments
    assert (
        PythonConfigurationSelector.MYPY_FILES
        not in result.declarations.absent_selectors
    )
    assert len(result.declarations.absent_selectors) == 5
    assert (
        len(
            _resolve(
                _snapshot(tmp_path, {"pyproject.toml": "tool=42"}),
            ).declarations.absent_selectors,
        )
        == 6
    )


@pytest.mark.parametrize(
    ("targets", "roots", "expected"),
    [
        ({"pkg/__init__.py": "", "pkg/a.py": ""}, (_ROOT,), _S.AMBIGUOUS),
        (
            {"src/pkg/__init__.py": "", "other/pkg.py": ""},
            (PythonModuleRoot("src"), PythonModuleRoot("other")),
            _S.AMBIGUOUS,
        ),
        ({"pkg": "", "pkg/a.txt": ""}, (_ROOT,), _S.AMBIGUOUS),
        ({"pkg/a.txt": "", "pkg/b.txt": ""}, (_ROOT,), _S.RESOLVED),
        ({}, (_ROOT,), _S.MISSING_IN_FRAME),
    ],
)
def test_coverage_competing_routes_roots_and_many_members(
    tmp_path: Path,
    targets: dict[str, str],
    roots: tuple[PythonModuleRoot, ...],
    expected: PythonConfigurationStatus,
) -> None:
    # Exact-resource/prefix collision is a representable retained state; it
    # cannot be acquired from one physical filesystem tree.
    collision = "pkg" in targets and "pkg/a.txt" in targets
    resources = {key: value for key, value in targets.items() if key != "pkg"}
    snapshot = _snapshot(
        tmp_path,
        {"pyproject.toml": '[tool.coverage.run]\nsource=["pkg"]', **resources},
    )
    if collision:
        occurrence = replace(
            snapshot.resources[-1],
            address=RepositoryResourceAddress("pkg"),
        )
        snapshot = replace(snapshot, resources=(*snapshot.resources, occurrence))
    result = _resolve(snapshot, roots=roots)
    assert result.assessments[0].status == expected
    assert bool(result.facts) == (expected == _S.RESOLVED)
    if expected == _S.AMBIGUOUS:
        assert not result.facts


def test_coverage_path_only_and_module_without_path_frame(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "pyproject.toml": '[tool.coverage.run]\nsource=["src/pkg", "pkg"]',
            "src/pkg/__init__.py": "",
        },
    )
    result = _resolve(snapshot, roots=(PythonModuleRoot("src"),))
    assert all(item.status == _S.RESOLVED for item in result.assessments)
    assert result.facts[1].module is not None
    assert result.facts[1].identity
    unsupported = _resolve(
        snapshot,
        roots=(PythonModuleRoot("src"),),
        frame=PythonConfigurationFrame(),
    )
    assert all(item.status == _S.UNSUPPORTED for item in unsupported.assessments)


@pytest.mark.parametrize(
    "mutation",
    [
        "repository",
        "snapshot",
        "occurrence",
        "declaration",
        "derivation",
        "module-repository",
        "module-snapshot",
        "module-content",
        "universe",
        "absolute-cwd",
        "absolute-pytest",
    ],
)
def test_reject_foreign_or_stale_dependencies(  # noqa: C901
    tmp_path: Path,
    mutation: str,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "pyproject.toml": '[project]\nreadme="README.md"',
            "README.md": "",
            "pkg.py": "",
        },
    )
    result = _resolve(snapshot)
    declarations, universe, frame = result.declarations, result.universe, result.frame
    foreign = RepositoryId.parse("00000000-0000-4000-8000-000000000048")
    wrong_id = RepositorySnapshotId("0" * 64)
    if mutation == "repository":
        declarations = replace(declarations, repository_id=foreign)
    elif mutation == "snapshot":
        declarations = replace(declarations, snapshot_id=wrong_id)
    elif mutation == "occurrence":
        declarations = replace(
            declarations,
            resource=replace(declarations.resource, content="changed"),
        )
    elif mutation == "declaration":
        declarations = replace(
            declarations,
            declarations=(replace(declarations.declarations[0], value=None),),
        )
    elif mutation == "derivation":
        declarations = replace(declarations, derivation_identity="invalid")
    elif mutation == "universe":
        universe = replace(universe, repository_id=foreign)
    elif mutation == "absolute-cwd":
        frame = PythonConfigurationFrame(PythonModuleRoot("C:/absolute"))
    elif mutation == "absolute-pytest":
        frame = PythonConfigurationFrame(pytest_root=PythonModuleRoot("C:/absolute"))
    else:
        module = universe.interpretations[0]
        if mutation == "module-repository":
            module = replace(module, repository_id=foreign)
        elif mutation == "module-snapshot":
            module = replace(module, snapshot_id=wrong_id)
        else:
            module = replace(
                module,
                resource=replace(module.resource, content="changed"),
            )
        universe = replace(universe, interpretations=(module,))
    with pytest.raises(ValueError, match=r"Configuration|Repository resource"):
        resolve_python_project_configuration(
            snapshot,
            declarations,
            universe=universe,
            frame=frame,
        )


def test_default_frame_missing_address_and_dependency_changes(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"pyproject.toml": '[tool.mypy]\nfiles=["src"]', "src/a.py": ""},
    )
    result = _resolve(snapshot)
    assert (
        resolve_python_project_configuration(
            snapshot,
            result.declarations,
            universe=result.universe,
        )
        .assessments[0]
        .status
        == _S.UNSUPPORTED
    )
    with pytest.raises(ValueError, match="does not contain"):
        analyze_python_project_configuration(
            snapshot,
            address=RepositoryResourceAddress("absent.toml"),
        )
    changed = _resolve(
        _snapshot(
            tmp_path,
            {"pyproject.toml": '[tool.mypy]\nfiles=["src"]', "src/a.py": "changed"},
        ),
    )
    assert result.derivation_identity != changed.derivation_identity
    assert result.facts[0].identity != changed.facts[0].identity
    assert (
        result.declarations.declarations[0].identity
        != changed.declarations.declarations[0].identity
    )


def test_dynamic_readme_preserves_static_syntax_and_ordinals(tmp_path: Path) -> None:
    result = _resolve(
        _snapshot(
            tmp_path,
            {
                "pyproject.toml": (
                    '[project]\nreadme="README.md"\n'
                    'dynamic=["version", "readme", "readme"]'
                ),
                "README.md": "",
            },
        ),
    )
    assert [item.declaration.value for item in result.assessments] == [
        "README.md",
        "readme",
        "readme",
    ]
    assert [item.declaration.item_ordinal for item in result.assessments] == [
        None,
        1,
        2,
    ]
    assert len({item.declaration.identity for item in result.assessments}) == 3
    assert all(item.status == _S.UNSUPPORTED for item in result.assessments)
    assert not result.facts


def test_readme_missing_exact_target_never_selects_prefix(tmp_path: Path) -> None:
    result = _resolve(
        _snapshot(
            tmp_path,
            {
                "pyproject.toml": '[project]\nreadme="docs"',
                "docs/readme.md": "",
            },
        ),
    )
    assert result.assessments[0].status == _S.MISSING_IN_FRAME
    assert (
        result.assessments[0].alternatives[0].route
        == "configuration-relative-exact-resource"
    )
    assert not result.facts


def test_frame_order_does_not_change_derivation_or_fact_order(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "pyproject.toml": (
                '[tool.coverage.run]\nsource=["pkg"]\n[tool.mypy]\nfiles=["src"]'
            ),
            "src/pkg.py": "",
            "src/other.py": "",
        },
    )
    result = _resolve(snapshot, roots=(PythonModuleRoot("src"),))
    reordered = _resolve(
        replace(snapshot, resources=tuple(reversed(snapshot.resources))),
        roots=(PythonModuleRoot("src"),),
    )
    assert result.derivation_identity == reordered.derivation_identity
    assert result.assessments == reordered.assessments
    assert result.facts == reordered.facts
