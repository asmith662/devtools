# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Source-grounded class and direct method declaration knowledge."""

from __future__ import annotations

import ast
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.python.classes import (
    PythonClassMethodAnalysisAggregate,
    PythonClassMethodParseError,
    PythonExcludedClassMethodSyntaxKind,
    analyze_python_class_method_resources,
    build_python_class_method_containment_view,
    derive_python_class_method_declarations,
)
from devtools.context.python.function import (
    PythonFunctionDeclarationKind,
    derive_python_function_declarations,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.python.classes.declarations import PythonClassMethodAnalysis
    from devtools.context.repository.snapshot import RepositorySnapshot


def _snapshot(tmp_path: Path, contents: dict[str, str]) -> RepositorySnapshot:
    for address, content in contents.items():
        target = tmp_path / address
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000051"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in contents),
        maximum_resource_bytes=4096,
    )


def test_direct_classes_methods_exclusions_and_existing_function_contract(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "module.py": (
                "def module_function():\n    pass\n\n"
                "@register\nclass A(Base, pkg.Other):\n"
                "    @staticmethod\n    def run(self):\n"
                "        def nested():\n            pass\n"
                "    @property\n    async def load(self):\n        pass\n"
                "    class Nested:\n        def hidden(self):\n            pass\n\n"
                "class B:\n    def run(self):\n        pass\n\n"
                "def outer():\n    class Local:\n        pass\n"
            ),
        },
    )
    analysis = derive_python_class_method_declarations(snapshot)
    assert [item.declared_name for item in analysis.classes] == ["A", "B"]
    assert [item.declared_name for item in analysis.methods] == [
        "run",
        "load",
        "run",
    ]
    assert [item.declaration_kind for item in analysis.methods] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
        PythonFunctionDeclarationKind.SYNCHRONOUS,
    ]
    assert analysis.classes[0].support.source_range.start_line == 5
    assert analysis.classes[0].support.source_range.start_column_utf8 == 0
    assert analysis.methods[0].support.source_range.start_line == 7
    assert analysis.methods[1].support.source_range.start_line == 11
    assert analysis.methods[0].support.resource_address == snapshot.resource.address
    assert analysis.methods[0].support.snapshot_id == snapshot.id
    assert [base.ordinal for base in analysis.classes[0].base_syntax] == [0, 1]
    assert [base.source_text for base in analysis.classes[0].base_syntax] == [
        "Base",
        "pkg.Other",
    ]
    assert [
        base.occurrence.source_range.start_line
        for base in analysis.classes[0].base_syntax
    ] == [5, 5]
    assert analysis.classes[1].base_syntax == ()
    assert analysis.methods[0].containing_class == analysis.classes[0]
    assert analysis.methods[2].containing_class == analysis.classes[1]
    assert analysis.classes[0].subject.identity != analysis.classes[1].subject.identity
    assert analysis.methods[0].subject.identity != analysis.methods[2].subject.identity
    assert analysis.methods[0].identity != analysis.methods[2].identity
    assert analysis.methods[0].subject.containing_class_subject_identity == (
        analysis.classes[0].subject.identity
    )
    assert analysis.coverage.class_count == 2
    assert analysis.coverage.method_count == 3
    assert analysis.coverage.module_body_function_count == 2
    assert analysis.coverage.excluded_class_count == 2
    assert analysis.coverage.excluded_function_count == 2
    assert [item.kind for item in analysis.excluded_syntax] == [
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS,
        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY,
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS,
        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY,
    ]
    assert analysis.coverage.IS_EXHAUSTIVE_FOR_SCOPE
    assert analysis.coverage.derivation_identity == analysis.derivation.identity
    assert analysis.derivation.dependency.resource == snapshot.resource
    assert analysis.derivation.dependency.repository_id == snapshot.repository_id
    assert analysis.derivation.dependency.snapshot_id == snapshot.id
    assert analysis.classes[0].derivation_identity == analysis.derivation.identity
    assert analysis.methods[0].derivation_identity == analysis.derivation.identity
    assert analysis == derive_python_class_method_declarations(snapshot)
    module_functions = derive_python_function_declarations(snapshot)
    assert [item.declared_name for item in module_functions.declarations] == [
        "module_function",
        "outer",
    ]
    assert all(item.declared_name != "run" for item in module_functions.declarations)
    assert not hasattr(analysis.methods[0], "runtime_descriptor")
    assert not hasattr(analysis.classes[0], "resolved_bases")


def test_multiple_resources_same_names_and_bidirectional_navigation(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "b.py": "class C:\n    def run(self):\n        pass\n",
            "a.py": (
                "class C:\n    def run(self):\n        pass\n\nclass Empty:\n    pass\n"
            ),
            "empty.py": "VALUE = 1\n",
        },
    )
    addresses = tuple(
        RepositoryResourceAddress(value) for value in ("a.py", "empty.py", "b.py")
    )
    aggregate = analyze_python_class_method_resources(
        snapshot,
        resource_addresses=addresses,
    )
    view = build_python_class_method_containment_view(snapshot, aggregate=aggregate)
    assert [item.declared_name for item in aggregate.classes] == ["C", "Empty", "C"]
    assert [item.declared_name for item in aggregate.methods] == ["run", "run"]
    assert len({item.subject.identity for item in aggregate.classes}) == 3
    assert len({item.subject.identity for item in aggregate.methods}) == 2
    assert view.module_body_classes_in(addresses[0]) == aggregate.analyses[0].classes
    assert view.module_body_classes_in(addresses[1]) == ()
    assert view.direct_methods_of(aggregate.classes[0]) == (aggregate.methods[0],)
    assert view.direct_methods_of(aggregate.classes[1]) == ()
    assert view.containing_class_of(aggregate.methods[1]) == aggregate.classes[2]
    assert view.occurrence_resource_of(aggregate.classes[0]) == snapshot.resource_at(
        addresses[0],
    )
    assert view.occurrence_resource_of(aggregate.methods[1]) == snapshot.resource_at(
        addresses[2],
    )
    assert view.snapshot_id == snapshot.id
    assert view.repository_id == snapshot.repository_id
    assert view.occurrence_resource_of(aggregate.methods[0]).content_identity == (
        snapshot.resource_at(addresses[0]).content_identity
    )
    assert not hasattr(view, "query")
    assert not hasattr(view, "rank")
    assert not hasattr(view, "score")
    (tmp_path / "a.py").unlink()
    assert (
        build_python_class_method_containment_view(snapshot, aggregate=aggregate)
        == view
    )
    assert view.module_body_classes_in(addresses[0]) == aggregate.analyses[0].classes


def test_unselected_and_wrong_snapshot_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": "class A:\n    def x(self):\n        pass\n",
            "b.py": "class B:\n    pass\n",
        },
    )
    a = RepositoryResourceAddress("a.py")
    b = RepositoryResourceAddress("b.py")
    aggregate = analyze_python_class_method_resources(snapshot, resource_addresses=(a,))
    view = build_python_class_method_containment_view(snapshot, aggregate=aggregate)
    other = derive_python_class_method_declarations(snapshot, resource_address=b)
    with pytest.raises(ValueError, match="not selected"):
        view.module_body_classes_in(b)
    with pytest.raises(ValueError, match="Class declaration does not belong"):
        view.direct_methods_of(other.classes[0])
    with pytest.raises(ValueError, match="Method declaration does not belong"):
        view.containing_class_of(replace(aggregate.methods[0], declared_name="other"))
    with pytest.raises(ValueError, match="Declaration does not belong"):
        view.occurrence_resource_of(other.classes[0])
    with pytest.raises(ValueError, match="at least one"):
        build_python_class_method_containment_view(
            snapshot,
            aggregate=PythonClassMethodAnalysisAggregate(()),
        )
    with pytest.raises(ValueError, match="repeats a resource"):
        build_python_class_method_containment_view(
            snapshot,
            aggregate=replace(aggregate, analyses=(aggregate.analyses[0],) * 2),
        )
    wrong_snapshot = _snapshot(tmp_path, {"a.py": "class A:\n    pass\n"})
    with pytest.raises(ValueError, match="another repository snapshot"):
        build_python_class_method_containment_view(wrong_snapshot, aggregate=aggregate)
    absent_snapshot = replace(snapshot, resources=(snapshot.resource_at(b),))
    with pytest.raises(ValueError, match="absent"):
        build_python_class_method_containment_view(absent_snapshot, aggregate=aggregate)
    changed_snapshot = _snapshot(
        tmp_path,
        {"a.py": "class Changed:\n    pass\n", "b.py": "class B:\n    pass\n"},
    )
    stale_snapshot = replace(changed_snapshot, id=snapshot.id)
    with pytest.raises(ValueError, match="stale observed resource"):
        build_python_class_method_containment_view(stale_snapshot, aggregate=aggregate)


def test_parse_failure_and_selection_guards(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"a.py": "class A:\n    pass\n", "bad.py": "class Bad(:\n"},
    )
    a = RepositoryResourceAddress("a.py")
    bad = RepositoryResourceAddress("bad.py")
    with pytest.raises(PythonClassMethodParseError) as captured:
        derive_python_class_method_declarations(snapshot, resource_address=bad)
    assert captured.value.derivation.dependency.snapshot_id == snapshot.id
    assert captured.value.parser_message
    assert captured.value.line_number == 1
    assert captured.value.parser_offset is not None
    assert not hasattr(captured.value, "coverage")
    with pytest.raises(ValueError, match="exactly one resource"):
        derive_python_class_method_declarations(snapshot)
    with pytest.raises(ValueError, match="at least one"):
        analyze_python_class_method_resources(snapshot, resource_addresses=())
    with pytest.raises(ValueError, match="distinct"):
        analyze_python_class_method_resources(snapshot, resource_addresses=(a, a))
    with pytest.raises(ValueError, match="does not contain"):
        analyze_python_class_method_resources(
            snapshot,
            resource_addresses=(a, RepositoryResourceAddress("missing.py")),
        )
    with pytest.raises(PythonClassMethodParseError):
        analyze_python_class_method_resources(snapshot, resource_addresses=(a, bad))


def test_missing_base_source_segment_rejects_incomplete_support(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot = _snapshot(tmp_path, {"a.py": "class A(Base):\n    pass\n"})
    monkeypatch.setattr(
        ast,
        "get_source_segment",
        lambda *_arguments: None,
    )
    with pytest.raises(ValueError, match="lacks exact observed source text"):
        derive_python_class_method_declarations(snapshot)


def test_containment_rejects_inconsistent_native_facts(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": (
                "class A(Base):\n    def run(self):\n        pass\n"
                "    class Nested:\n        pass\n"
            ),
        },
    )
    address = RepositoryResourceAddress("a.py")
    aggregate = analyze_python_class_method_resources(
        snapshot,
        resource_addresses=(address,),
    )
    analysis = aggregate.analyses[0]

    def reject(changed_analysis: PythonClassMethodAnalysis, message: str) -> None:
        changed = replace(aggregate, analyses=(changed_analysis,))
        with pytest.raises(ValueError, match=message):
            build_python_class_method_containment_view(
                snapshot,
                aggregate=changed,
            )

    for coverage in (
        replace(analysis.coverage, derivation_identity="other"),
        replace(analysis.coverage, class_count=0),
        replace(analysis.coverage, method_count=0),
        replace(analysis.coverage, excluded_class_count=0),
        replace(analysis.coverage, excluded_function_count=1),
    ):
        reject(replace(analysis, coverage=coverage), "coverage differs")

    declaration = analysis.classes[0]
    base = declaration.base_syntax[0]
    for changed_class in (
        replace(declaration, derivation_identity="other"),
        replace(
            declaration,
            subject=replace(declaration.subject, declaration_ordinal=1),
        ),
        replace(
            declaration,
            base_syntax=(
                replace(
                    base,
                    occurrence=replace(
                        base.occurrence,
                        snapshot_id=replace(snapshot.id, value="0" * 64),
                    ),
                ),
            ),
        ),
    ):
        reject(replace(analysis, classes=(changed_class,)), "Class declaration differs")

    method = analysis.methods[0]
    for changed_method in (
        replace(method, containing_class=replace(declaration, declared_name="Other")),
        replace(
            method,
            subject=replace(method.subject, containing_class_subject_identity="other"),
        ),
        replace(
            method,
            support=replace(
                method.support,
                resource_address=RepositoryResourceAddress("other.py"),
            ),
        ),
    ):
        reject(
            replace(analysis, methods=(changed_method,)),
            "Method declaration differs",
        )

    excluded = analysis.excluded_syntax[0]
    reject(
        replace(
            analysis,
            excluded_syntax=(
                replace(
                    excluded,
                    occurrence=replace(
                        excluded.occurrence,
                        resource_address=RepositoryResourceAddress("other.py"),
                    ),
                ),
            ),
        ),
        "Excluded syntax differs",
    )
