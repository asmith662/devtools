# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Bounded direct-base knowledge from retained Python repository resources."""

from __future__ import annotations

import ast
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.python.classes import (
    PythonDirectBaseAnalysis,
    analyze_python_class_method_resources,
    derive_python_direct_bases,
)
from devtools.context.python.classes import (
    PythonDirectBaseOutcome as Outcome,
)
from devtools.context.python.classes import (
    PythonDirectBaseRoute as Route,
)
from devtools.context.python.classes.bases import _bindings
from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.repository.snapshot import RepositorySnapshot


def _snapshot(tmp_path: Path, contents: dict[str, str]) -> RepositorySnapshot:
    for name, content in contents.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000072"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in contents),
        maximum_resource_bytes=4096,
    )


def _derive(snapshot: RepositorySnapshot) -> PythonDirectBaseAnalysis:
    addresses = tuple(item.address for item in snapshot.resources)
    aggregate = analyze_python_class_method_resources(
        snapshot,
        resource_addresses=addresses,
    )
    interpretations = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=addresses,
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretations.interpretations,
    )
    return derive_python_direct_bases(
        snapshot,
        aggregate=aggregate,
        module_universe=universe,
    )


def test_local_order_multiple_bases_identity_navigation_and_no_transitive(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/a.py": (
                "class Root:\n    pass\n"
                "class Other:\n    pass\n"
                "class Child(Root, Missing, Other):\n    pass\n"
                "class Grandchild(Child):\n    pass\n"
            ),
        },
    )
    analysis = _derive(snapshot)
    root, other, child, grandchild = analysis.aggregate.classes
    assert [item.outcome for item in analysis.assessments] == [
        Outcome.RESOLVED,
        Outcome.UNRESOLVED_BINDING,
        Outcome.RESOLVED,
        Outcome.RESOLVED,
    ]
    assert [item.target for item in analysis.direct_bases_of(child)] == [root, other]
    assert [item.target for item in analysis.direct_bases_of(grandchild)] == [child]
    assert analysis.direct_bases_of(root) == ()
    assert [item.child for item in analysis.direct_subclasses_of(root)] == [child]
    assert [item.child for item in analysis.direct_subclasses_of(child)] == [grandchild]
    assert grandchild not in [
        item.child for item in analysis.direct_subclasses_of(root)
    ]
    first = analysis.assessments[0]
    assert first.route is Route.LOCAL_CLASS
    assert first.base.source_text == "Root"
    assert first.base.ordinal == 0
    assert first.base.occurrence.source_range.start_line == 5
    assert first.base.occurrence.source_range.start_column_utf8 == 12
    assert first.child_analysis.derivation.dependency.resource.content_identity == (
        snapshot.resource.content_identity
    )
    assert first.target_analysis == first.child_analysis
    assert first.target is not None
    assert first.child.subject.identity != first.target.subject.identity
    assert first.identity == _derive(snapshot).assessments[0].identity
    assert not hasattr(first, "rank")
    assert not hasattr(first, "relevance")
    with pytest.raises(ValueError, match="outside the analyzed"):
        analysis.direct_bases_of(replace(child, declared_name="Other"))
    with pytest.raises(ValueError, match="outside the analyzed"):
        analysis.direct_subclasses_of(replace(root, declared_name="Other"))


def test_imported_member_alias_and_qualified_module_forms(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "class Export:\n    pass\n",
            "src/pkg/base.py": "class Base:\n    pass\n",
            "src/use.py": (
                "from pkg.base import Base as Alias\n"
                "from pkg import Export\n"
                "import pkg.base as m\n"
                "import pkg.base\n"
                "class One(Alias):\n    pass\n"
                "class Two(Export):\n    pass\n"
                "class Three(m.Base):\n    pass\n"
                "class Four(pkg.base.Base):\n    pass\n"
            ),
        },
    )
    analysis = _derive(snapshot)
    assert [item.outcome for item in analysis.assessments] == [Outcome.RESOLVED] * 4
    assert [item.route for item in analysis.assessments] == [
        Route.IMPORTED_MEMBER,
        Route.IMPORTED_MEMBER,
        Route.IMPORTED_MODULE_ATTRIBUTE,
        Route.IMPORTED_MODULE_ATTRIBUTE,
    ]
    assert all(item.target is not None for item in analysis.assessments)
    assert [
        item.target.declared_name for item in analysis.assessments if item.target
    ] == [
        "Base",
        "Export",
        "Base",
        "Base",
    ]
    assert all(item.import_resolution is not None for item in analysis.assessments)
    assert all(item.import_declaration is not None for item in analysis.assessments)
    assert all(
        item.import_resolution.matches
        for item in analysis.assessments
        if item.import_resolution
    )
    assert analysis.assessments[0].target_analysis is not None
    assert analysis.assessments[0].target_analysis.derivation.dependency.resource == (
        snapshot.resource_at(RepositoryResourceAddress("src/pkg/base.py"))
    )
    base = analysis.assessments[0].target
    assert base is not None
    assert [
        item.child.declared_name for item in analysis.direct_subclasses_of(base)
    ] == [
        "One",
        "Three",
        "Four",
    ]


def test_unresolved_and_ambiguous_forms_are_not_discarded(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/base.py": (
                "class Base:\n    pass\n"
                "class Base:\n    pass\n"
                "def NotClass():\n    pass\n"
                "VALUE = 1\n"
            ),
            "src/use.py": (
                "from pkg.base import Base, NotClass, VALUE, Missing\n"
                "import pkg.base as m\n"
                "class X(Base, NotClass, VALUE, Missing, m.Unknown, "
                "factory().Base, m.Base, object, Base[int]):\n    pass\n"
            ),
        },
    )
    analysis = _derive(snapshot)
    assert [item.outcome for item in analysis.assessments] == [
        Outcome.AMBIGUOUS_TARGET,
        Outcome.TARGET_NOT_CLASS,
        Outcome.TARGET_NOT_CLASS,
        Outcome.UNRESOLVED_TARGET,
        Outcome.UNRESOLVED_TARGET,
        Outcome.UNSUPPORTED_EXPRESSION,
        Outcome.AMBIGUOUS_TARGET,
        Outcome.UNRESOLVED_BINDING,
        Outcome.UNSUPPORTED_EXPRESSION,
    ]
    assert analysis.direct_bases_of(analysis.aggregate.classes[2]) == ()


def test_shadowing_decorators_and_unsupported_qualification(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/m.py": (
                "class Base:\n    pass\n"
                "Base = external\n"
                "class A(Base):\n    pass\n"
                "@decorate\nclass Decorated:\n    pass\n"
                "class B(Decorated):\n    pass\n"
                "if flag:\n    class Conditional:\n        pass\n"
                "class C(Conditional):\n    pass\n"
                "class D(obj.Base):\n    pass\n"
            ),
            "src/pkg/base.py": "class Target:\n    pass\n",
            "src/q.py": (
                "import pkg.base as m\n"
                "class E(m.extra.Target):\n    pass\n"
                "from pkg.base import Target as Alias\n"
                "class F(Alias.member):\n    pass\n"
                "m.Target = replacement\n"
                "factory().Base = replacement\n"
                "class G(m.Target):\n    pass\n"
            ),
        },
    )
    analysis = _derive(snapshot)
    assert [item.outcome for item in analysis.assessments] == [
        Outcome.AMBIGUOUS_BINDING,
        Outcome.UNSUPPORTED_BINDING,
        Outcome.UNSUPPORTED_BINDING,
        Outcome.UNRESOLVED_BINDING,
        Outcome.UNSUPPORTED_BINDING,
        Outcome.UNSUPPORTED_BINDING,
        Outcome.AMBIGUOUS_BINDING,
    ]


def test_module_resolution_outcomes_and_snapshot_validation(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/a.py": (
                "from absent import Base\n"
                "from .missing import Other\n"
                "class X(Base, Other):\n    pass\n"
            ),
            "src/dup.py": "class Base:\n    pass\n",
        },
    )
    analysis = _derive(snapshot)
    assert [item.outcome for item in analysis.assessments] == [
        Outcome.UNRESOLVED_MODULE,
        Outcome.UNSUPPORTED_MODULE,
    ]
    wrong = _snapshot(tmp_path, {"src/a.py": "class X:\n    pass\n"})
    with pytest.raises(ValueError, match="another repository snapshot"):
        derive_python_direct_bases(
            wrong,
            aggregate=analysis.aggregate,
            module_universe=analysis.module_universe,
        )
    with pytest.raises(ValueError, match="module universe differs"):
        derive_python_direct_bases(
            snapshot,
            aggregate=analysis.aggregate,
            module_universe=replace(
                analysis.module_universe,
                interpretations=(
                    replace(
                        analysis.module_universe.interpretations[0],
                        snapshot_id=wrong.id,
                    ),
                ),
            ),
        )


def test_target_change_changes_identity_and_no_worktree_reread(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/base.py": "class Base:\n    pass\n",
            "src/use.py": "from base import Base\nclass Child(Base):\n    pass\n",
        },
    )
    first = _derive(snapshot).assessments[0]
    (tmp_path / "src/base.py").unlink()
    assert _derive(snapshot).assessments[0].identity == first.identity
    changed = _snapshot(
        tmp_path,
        {
            "src/base.py": "class Other:\n    pass\n",
            "src/use.py": "from base import Base\nclass Child(Base):\n    pass\n",
        },
    )
    second = _derive(changed).assessments[0]
    assert second.outcome is Outcome.UNRESOLVED_TARGET
    assert second.identity != first.identity


def test_same_names_in_distinct_modules_resolve_to_distinct_subjects(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/a.py": "class Base:\n    pass\n",
            "src/b.py": "class Base:\n    pass\n",
            "src/x.py": "from a import Base\nclass X(Base):\n    pass\n",
            "src/y.py": "from b import Base\nclass Y(Base):\n    pass\n",
        },
    )
    analysis = _derive(snapshot)
    assert [item.outcome for item in analysis.assessments] == [Outcome.RESOLVED] * 2
    assert all(item.target is not None for item in analysis.assessments)
    targets = [item.target for item in analysis.assessments if item.target]
    assert targets[0].subject.identity != targets[1].subject.identity


def test_wildcard_imports_and_selected_source_with_on_demand_target(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/target.py": "class Base:\n    pass\n",
            "src/source.py": (
                "from target import Base\nclass Child(Base):\n    pass\n"
            ),
            "src/wild.py": ("from target import *\nclass Child(Base):\n    pass\n"),
            "src/nested.py": (
                "if flag:\n    from target import *\nclass Child(Base):\n    pass\n"
            ),
            "src/target_wild.py": ("class Base:\n    pass\nfrom target import *\n"),
            "src/using_wild.py": (
                "from target_wild import Base\nclass Child(Base):\n    pass\n"
            ),
        },
    )
    all_results = _derive(snapshot)
    assert {
        item.child.support.resource_address.value: item.outcome
        for item in all_results.assessments
    } == {
        "src/source.py": Outcome.RESOLVED,
        "src/wild.py": Outcome.AMBIGUOUS_BINDING,
        "src/nested.py": Outcome.AMBIGUOUS_BINDING,
        "src/using_wild.py": Outcome.AMBIGUOUS_TARGET,
    }
    source = RepositoryResourceAddress("src/source.py")
    aggregate = analyze_python_class_method_resources(
        snapshot,
        resource_addresses=(source,),
    )
    selected = derive_python_direct_bases(
        snapshot,
        aggregate=aggregate,
        module_universe=all_results.module_universe,
    )
    assert selected.assessments[0].outcome is Outcome.RESOLVED
    assert selected.assessments[0].target_analysis is not None
    assert selected.assessments[
        0
    ].target_analysis.derivation.dependency.resource.address == (
        RepositoryResourceAddress("src/target.py")
    )


def test_ambiguous_module_interpretation_and_competing_nested_binding(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/base.py": "class Base:\n    pass\n",
            "src/a.py": (
                "if flag:\n    from base import Base\nclass Child(Base):\n    pass\n"
            ),
            "src/b.py": ("from base import Base\nclass Child(Base):\n    pass\n"),
        },
    )
    analysis = _derive(snapshot)
    assert analysis.assessments[0].outcome is Outcome.UNSUPPORTED_BINDING
    interpretation = next(
        item
        for item in analysis.module_universe.interpretations
        if item.dotted_name == "base"
    )
    duplicate = replace(
        interpretation,
        module_root=PythonModuleRoot("."),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=(*analysis.module_universe.interpretations, duplicate),
    )
    ambiguous = derive_python_direct_bases(
        snapshot,
        aggregate=analysis.aggregate,
        module_universe=universe,
    )
    assert ambiguous.assessments[1].outcome is Outcome.AMBIGUOUS_MODULE


def test_imported_base_absent_from_empty_observed_module(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/empty.py": "",
            "src/child.py": "from empty import Base\nclass Child(Base):\n    pass\n",
        },
    )
    analysis = _derive(snapshot)
    assert len(analysis.assessments) == 1
    assert analysis.assessments[0].target is None
    assert analysis.assessments[0].outcome is Outcome.UNRESOLVED_TARGET


def test_empty_complete_binding_frame_produces_no_base_support(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"src/empty.py": ""})
    aggregate = analyze_python_class_method_resources(
        snapshot,
        resource_addresses=(RepositoryResourceAddress("src/empty.py"),),
    )
    assert _bindings(ast.parse(""), aggregate.analyses[0], ()) == ()
