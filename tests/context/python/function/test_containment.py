# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Navigation over existing direct Python function declaration ownership."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.python.function import (
    PythonFunctionDeclarationAnalysisAggregate,
    PythonFunctionDeclarationKind,
    analyze_python_function_declaration_resources,
    build_python_function_declaration_containment_view,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationAnalysis,
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


def _snapshot(tmp_path: Path, contents: dict[str, str]) -> RepositorySnapshot:
    for address, content in contents.items():
        target = tmp_path / address
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000041"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in contents),
        maximum_resource_bytes=1024,
    )


def _aggregate(
    snapshot: RepositorySnapshot,
    *addresses: str,
) -> PythonFunctionDeclarationAnalysisAggregate:
    return analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=tuple(
            RepositoryResourceAddress(value) for value in addresses
        ),
    )


def _replace_first_analysis(
    aggregate: PythonFunctionDeclarationAnalysisAggregate,
    analysis: PythonFunctionDeclarationAnalysis,
) -> PythonFunctionDeclarationAnalysisAggregate:
    return replace(aggregate, analyses=(analysis, *aggregate.analyses[1:]))


def _replace_first_declaration(
    aggregate: PythonFunctionDeclarationAnalysisAggregate,
    declaration: PythonFunctionDeclarationKnowledge,
) -> PythonFunctionDeclarationAnalysisAggregate:
    analysis = aggregate.analyses[0]
    return _replace_first_analysis(
        aggregate,
        replace(analysis, declarations=(declaration, *analysis.declarations[1:])),
    )


def test_navigates_native_declarations_in_both_directions(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "b.py": "def other():\n    pass\n",
            "a.py": (
                "def first():\n    pass\n\n"
                "async def second():\n    pass\n\n"
                "class Holder:\n    def method(self):\n        pass\n\n"
                "def outer():\n    def nested():\n        pass\n"
            ),
            "empty.py": "class OnlyClass:\n    pass\n",
        },
    )
    aggregate = _aggregate(snapshot, "a.py", "empty.py", "b.py")
    view = build_python_function_declaration_containment_view(
        snapshot,
        aggregate=aggregate,
    )
    a = RepositoryResourceAddress("a.py")
    empty = RepositoryResourceAddress("empty.py")
    b = RepositoryResourceAddress("b.py")
    direct = view.direct_declarations_in(a)
    assert [item.declared_name for item in direct] == ["first", "second", "outer"]
    assert [item.declaration_kind for item in direct] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
        PythonFunctionDeclarationKind.SYNCHRONOUS,
    ]
    assert view.direct_declarations_in(empty) == ()
    assert [item.declared_name for item in view.direct_declarations_in(b)] == [
        "other",
    ]
    assert direct == aggregate.analyses[0].declarations
    assert view.containing_resource_of(direct[1]) == snapshot.resource_at(a)
    assert view.containing_resource_of(view.direct_declarations_in(b)[0]) == (
        snapshot.resource_at(b)
    )
    assert direct[1].support.source_range.start_line == 4
    assert direct[1].support.resource_address == a
    assert direct[1].support.snapshot_id == snapshot.id
    assert view.repository_id == snapshot.repository_id
    assert view.snapshot_id == snapshot.id
    assert view.containing_resource_of(direct[1]).content_identity == (
        snapshot.resource_at(a).content_identity
    )
    assert direct[1].derivation_identity == aggregate.analyses[0].derivation.identity
    assert aggregate.analyses[0].coverage.declaration_count == 3
    assert aggregate.analyses[1].coverage.declaration_count == 0
    assert aggregate.analyses[1].coverage.IS_EXHAUSTIVE
    assert not hasattr(view, "query")
    assert not hasattr(view, "score")
    assert not hasattr(view, "rank")
    # The view and existing derivation retain source; no working-tree reread.
    (tmp_path / "a.py").unlink()
    assert view.direct_declarations_in(a) == direct
    assert (
        build_python_function_declaration_containment_view(
            snapshot,
            aggregate=aggregate,
        )
        == view
    )


def test_unselected_resource_and_declaration_do_not_imply_absence(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"a.py": "def a():\n    pass\n", "b.py": "def b():\n    pass\n"},
    )
    aggregate = _aggregate(snapshot, "a.py")
    view = build_python_function_declaration_containment_view(
        snapshot,
        aggregate=aggregate,
    )
    with pytest.raises(ValueError, match="not selected"):
        view.direct_declarations_in(RepositoryResourceAddress("b.py"))
    other = _aggregate(snapshot, "b.py").declarations[0]
    with pytest.raises(ValueError, match="does not belong"):
        view.containing_resource_of(other)


def test_rejects_empty_duplicate_wrong_and_stale_analysis(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"a.py": "def a():\n    pass\n"})
    aggregate = _aggregate(snapshot, "a.py")
    analysis = aggregate.analyses[0]
    with pytest.raises(ValueError, match="at least one"):
        build_python_function_declaration_containment_view(
            snapshot,
            aggregate=PythonFunctionDeclarationAnalysisAggregate(()),
        )
    with pytest.raises(ValueError, match="repeats a selected resource"):
        build_python_function_declaration_containment_view(
            snapshot,
            aggregate=replace(aggregate, analyses=(analysis, analysis)),
        )
    dependency = analysis.derivation.dependency
    for changed_dependency in (
        replace(
            dependency,
            repository_id=RepositoryId.parse(
                "00000000-0000-4000-8000-000000000042",
            ),
        ),
        replace(dependency, snapshot_id=replace(snapshot.id, value="0" * 64)),
    ):
        changed = _replace_first_analysis(
            aggregate,
            replace(
                analysis,
                derivation=replace(analysis.derivation, dependency=changed_dependency),
            ),
        )
        with pytest.raises(ValueError, match="another repository snapshot"):
            build_python_function_declaration_containment_view(
                snapshot,
                aggregate=changed,
            )
    missing = replace(snapshot, resources=())
    with pytest.raises(ValueError, match="absent"):
        build_python_function_declaration_containment_view(
            missing,
            aggregate=aggregate,
        )
    changed_content = _snapshot(tmp_path, {"a.py": "def changed():\n    pass\n"})
    stale = replace(changed_content, id=snapshot.id)
    with pytest.raises(ValueError, match="stale observed resource"):
        build_python_function_declaration_containment_view(
            stale,
            aggregate=aggregate,
        )


def test_rejects_inconsistent_coverage_and_declaration_support(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"a.py": "def a():\n    pass\n"})
    aggregate = _aggregate(snapshot, "a.py")
    analysis = aggregate.analyses[0]
    for changed_coverage in (
        replace(analysis.coverage, derivation_identity="other"),
        replace(analysis.coverage, declaration_count=0),
    ):
        changed = _replace_first_analysis(
            aggregate,
            replace(analysis, coverage=changed_coverage),
        )
        with pytest.raises(ValueError, match="coverage differs"):
            build_python_function_declaration_containment_view(
                snapshot,
                aggregate=changed,
            )
    declaration = analysis.declarations[0]
    subject = declaration.subject
    support = declaration.support
    changed_declarations = (
        replace(declaration, derivation_identity="other"),
        replace(
            declaration,
            subject=replace(subject, snapshot_id=replace(snapshot.id, value="0" * 64)),
        ),
        replace(
            declaration,
            subject=replace(subject, resource_dependency_identity="other"),
        ),
        replace(
            declaration,
            subject=replace(subject, derivation_definition_identity="other"),
        ),
        replace(declaration, subject=replace(subject, declaration_ordinal=1)),
        replace(
            declaration,
            support=replace(support, snapshot_id=replace(snapshot.id, value="0" * 64)),
        ),
        replace(
            declaration,
            support=replace(
                support,
                resource_address=RepositoryResourceAddress("other.py"),
            ),
        ),
    )
    for changed_declaration in changed_declarations:
        changed = _replace_first_declaration(aggregate, changed_declaration)
        with pytest.raises(ValueError, match="differs from its resource"):
            build_python_function_declaration_containment_view(
                snapshot,
                aggregate=changed,
            )
