# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Bounded declaration references over exact retained source occurrences."""

from __future__ import annotations

import ast
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
)
from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.modules.declarations import (
    PythonModuleDeclarationLookupOutcome,
    lookup_python_module_declaration,
)
from devtools.context.python.modules.interpretation import (
    PythonModuleInterpretationUniverse,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import (
    PythonDeclarationReferenceAnalysis,
    PythonDeclarationReferenceKnowledge,
    derive_python_declaration_references,
)
from devtools.context.python.references import (
    PythonDeclarationReferenceOutcome as Outcome,
)
from devtools.context.python.references import (
    PythonDeclarationReferenceRoute as Route,
)
from devtools.context.python.references.declarations.bindings import _Binding
from devtools.context.python.references.declarations.resolution import _resolve
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
            RepositoryId.parse("00000000-0000-4000-8000-000000000073"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in contents),
        maximum_resource_bytes=4096,
    )


def _universe(snapshot: RepositorySnapshot) -> PythonModuleInterpretationUniverse:
    interpretation = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=tuple(item.address for item in snapshot.resources),
    )
    return define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretation.interpretations,
    )


def _analysis(
    snapshot: RepositorySnapshot,
    address: str,
) -> PythonDeclarationReferenceAnalysis:
    return derive_python_declaration_references(
        snapshot,
        resource_address=RepositoryResourceAddress(address),
        module_universe=_universe(snapshot),
        source_interpretations=tuple(
            item
            for item in _universe(snapshot).interpretations
            if item.resource.address == RepositoryResourceAddress(address)
        ),
    )


def _fact(
    analysis: PythonDeclarationReferenceAnalysis,
    text: str,
) -> PythonDeclarationReferenceKnowledge:
    matches = [
        item.reference
        for item in analysis.assessments
        if item.source_text == text and item.reference is not None
    ]
    assert len(matches) == 1
    return matches[0]


def _outcome(
    analysis: PythonDeclarationReferenceAnalysis,
    text: str,
) -> Outcome:
    matches = [
        item.outcome for item in analysis.assessments if item.source_text == text
    ]
    assert len(matches) == 1
    return matches[0]


def test_module_qualified_function_and_class_references(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "# package\n",
            "src/pkg/api.py": (
                "def helper():\n    pass\nclass Service:\n    pass\nVALUE = 1\n"
            ),
            "src/use.py": (
                "import pkg.api\nimport pkg.api as m\n"
                "pkg.api.helper()\nm.helper()\nm.Service()\n"
                "m.VALUE\nm.Unknown\nobj.attribute\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    first = _fact(analysis, "pkg.api.helper")
    second = _fact(analysis, "m.helper")
    third = _fact(analysis, "m.Service")
    assert first.route is Route.MODULE_QUALIFIED
    assert second.route is Route.MODULE_QUALIFIED
    assert isinstance(first.target_declaration, PythonFunctionDeclarationKnowledge)
    assert isinstance(third.target_declaration, PythonClassDeclarationKnowledge)
    assert first.direct_call
    assert second.direct_call
    assert third.direct_call
    assert first.occurrence.source_range.start_line == 3
    assert first.occurrence.source_range.start_column_utf8 == 0
    assert first.occurrence.source_range.end_column_utf8 == len("pkg.api.helper")
    assert first.target_resource == snapshot.resource_at(
        RepositoryResourceAddress("src/pkg/api.py"),
    )
    assert first.import_declaration is not None
    assert first.module_resolution is not None
    assert first.direct_member_resolution is not None
    assert (
        first.identity
        == _fact(_analysis(snapshot, "src/use.py"), "pkg.api.helper").identity
    )
    assert _outcome(analysis, "m.VALUE") is Outcome.TARGET_NOT_DECLARATION
    assert _outcome(analysis, "m.Unknown") is Outcome.MEMBER_UNRESOLVED
    assert _outcome(analysis, "obj.attribute") is Outcome.UNSUPPORTED_RECEIVER
    assert analysis.coverage.reference_count == len(analysis.references) == 3


def test_direct_imported_classes_aliases_and_names(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/base.py": "class Base:\n    pass\n",
            "src/use.py": (
                "from base import Base\nfrom base import Base as Alias\n"
                "Base()\nAlias()\nBase\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    assert [item.route for item in analysis.references] == [Route.IMPORTED_MEMBER] * 3
    assert isinstance(
        _fact(analysis, "Alias").target_declaration,
        PythonClassDeclarationKnowledge,
    )
    assert [item.direct_call for item in analysis.references] == [True, True, False]
    assert len({item.target_subject.identity for item in analysis.references}) == 1
    assert analysis.coverage.IS_EXHAUSTIVE is False


def test_one_facade_function_preserves_existing_positive_route(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/pkg/__init__.py": "from .impl import helper as exported\n",
            "src/pkg/impl.py": "def helper():\n    pass\n",
            "src/use.py": "from pkg import exported as local\nlocal()\n",
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    reference = _fact(analysis, "local")
    assert reference.route is Route.ONE_FACADE
    assert reference.direct_call
    assert reference.imported_member_resolution is not None
    assert reference.target_resource.address == RepositoryResourceAddress(
        "src/pkg/impl.py",
    )


def test_same_module_functions_classes_and_class_qualified_methods(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/local.py": (
                "def helper():\n    pass\n"
                "class Service:\n"
                "    def run(self):\n        pass\n"
                "    async def load(self):\n        pass\n"
                "def caller():\n"
                "    helper()\n    Service()\n"
                "    Service.run()\n    Service.load\n"
                "    self.run()\n    cls.load()\n    obj.run()\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/local.py")
    assert _fact(analysis, "helper").route is Route.SAME_MODULE
    assert _fact(analysis, "Service").route is Route.SAME_MODULE
    run = _fact(analysis, "Service.run")
    load = _fact(analysis, "Service.load")
    assert run.route is Route.CLASS_QUALIFIED_METHOD
    assert isinstance(run.target_declaration, PythonMethodDeclarationKnowledge)
    assert isinstance(load.target_declaration, PythonMethodDeclarationKnowledge)
    assert run.containing_class is not None
    assert run.target_declaration.containing_class == run.containing_class
    assert run.direct_call
    assert not load.direct_call
    assert _outcome(analysis, "self.run") is Outcome.UNSUPPORTED_RECEIVER
    assert _outcome(analysis, "cls.load") is Outcome.UNSUPPORTED_RECEIVER
    assert _outcome(analysis, "obj.run") is Outcome.UNSUPPORTED_RECEIVER


def test_imported_and_module_qualified_class_methods(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/base.py": ("class Service:\n    def run(self):\n        pass\n"),
            "src/use.py": (
                "from base import Service as S\nimport base as m\n"
                "S.run()\nm.Service.run()\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    assert [item.route for item in analysis.references] == [
        Route.CLASS_QUALIFIED_METHOD,
        Route.CLASS_QUALIFIED_METHOD,
    ]
    assert all(
        item.target_resource.address == RepositoryResourceAddress("src/base.py")
        for item in analysis.references
    )
    assert all(item.direct_call for item in analysis.references)


def test_decorated_and_rebound_methods_do_not_claim_declaration_binding(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/use.py": (
                "class Service:\n"
                "    @property\n    def decorated(self):\n        return 1\n"
                "    def rebound(self):\n        pass\n"
                "    rebound = replacement\n"
                "Service.decorated\nService.rebound\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    assert _outcome(analysis, "Service.decorated") is Outcome.METHOD_UNRESOLVED
    assert _outcome(analysis, "Service.rebound") is Outcome.AMBIGUOUS_BINDING


def test_shadowing_rebinding_ambiguity_and_unsupported(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/base.py": "def helper():\n    pass\n",
            "src/use.py": (
                "from base import helper\nhelper = replacement\n"
                "def caller():\n    helper()\n"
                "class Later:\n    pass\n"
                "def local():\n    Later()\n    value = 1\n"
                "factory().method()\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    assert _outcome(analysis, "helper") is Outcome.AMBIGUOUS_BINDING
    assert _outcome(analysis, "factory().method") is Outcome.UNSUPPORTED_EXPRESSION
    assert _fact(analysis, "Later").route is Route.SAME_MODULE
    changed = _snapshot(
        tmp_path,
        {
            "src/base.py": "def changed():\n    pass\n",
            "src/use.py": "from base import helper\nhelper()\n",
        },
    )
    assert _outcome(_analysis(changed, "src/use.py"), "helper") is (
        Outcome.MEMBER_UNRESOLVED
    )


def test_wrong_snapshot_and_retained_content(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/base.py": "class Base:\n    pass\n",
            "src/use.py": "from base import Base\nBase()\n",
        },
    )
    universe = _universe(snapshot)
    address = RepositoryResourceAddress("src/use.py")
    analysis = _analysis(snapshot, "src/use.py")
    (tmp_path / "src/base.py").unlink()
    assert _fact(_analysis(snapshot, "src/use.py"), "Base").identity == (
        _fact(analysis, "Base").identity
    )
    wrong = _snapshot(tmp_path, {"src/use.py": "class X:\n    pass\n"})
    with pytest.raises(ValueError, match="module universe differs"):
        derive_python_declaration_references(
            wrong,
            resource_address=address,
            module_universe=universe,
        )
    with pytest.raises(ValueError, match="source interpretation differs"):
        derive_python_declaration_references(
            snapshot,
            resource_address=address,
            module_universe=universe,
            source_interpretations=(
                replace(universe.interpretations[0], snapshot_id=wrong.id),
            ),
        )


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("def target():\n    pass\n", PythonModuleDeclarationLookupOutcome.RESOLVED),
        ("class target:\n    pass\n", PythonModuleDeclarationLookupOutcome.RESOLVED),
        ("other = 1\n", PythonModuleDeclarationLookupOutcome.UNRESOLVED),
        ("target = 1\n", PythonModuleDeclarationLookupOutcome.NOT_DECLARATION),
        (
            "def target():\n    pass\ntarget = 1\n",
            PythonModuleDeclarationLookupOutcome.AMBIGUOUS,
        ),
        ("from other import *\n", PythonModuleDeclarationLookupOutcome.AMBIGUOUS),
        ("exec('target = 1')\n", PythonModuleDeclarationLookupOutcome.AMBIGUOUS),
        (
            "@decorate\ndef target():\n    pass\n",
            PythonModuleDeclarationLookupOutcome.NOT_DECLARATION,
        ),
        (
            "if condition:\n    def target():\n        pass\n",
            PythonModuleDeclarationLookupOutcome.NOT_DECLARATION,
        ),
        ("import unrelated\n", PythonModuleDeclarationLookupOutcome.UNRESOLVED),
        (
            "if condition:\n    from other import target\n",
            PythonModuleDeclarationLookupOutcome.NOT_DECLARATION,
        ),
        (
            "if condition:\n    from other import *\n",
            PythonModuleDeclarationLookupOutcome.AMBIGUOUS,
        ),
        (
            "if condition:\n    def unrelated():\n        pass\n",
            PythonModuleDeclarationLookupOutcome.UNRESOLVED,
        ),
        (
            "if condition:\n    from other import unrelated\n",
            PythonModuleDeclarationLookupOutcome.UNRESOLVED,
        ),
    ],
)
def test_direct_module_lookup_bounded_outcomes(
    tmp_path: Path,
    source: str,
    expected: PythonModuleDeclarationLookupOutcome,
) -> None:
    snapshot = _snapshot(tmp_path, {"src/use.py": source})
    module = _universe(snapshot).interpretations[0]
    lookup = lookup_python_module_declaration(
        snapshot,
        module=module,
        declared_name="target",
    )
    assert lookup.outcome is expected
    assert (lookup.target is not None) == (
        expected is PythonModuleDeclarationLookupOutcome.RESOLVED
    )
    assert (
        lookup.identity
        == lookup_python_module_declaration(
            snapshot,
            module=module,
            declared_name="target",
        ).identity
    )


def test_direct_module_lookup_rejects_stale_and_invalid_input(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"src/use.py": "def target():\n    pass\n"})
    module = _universe(snapshot).interpretations[0]
    with pytest.raises(ValueError, match="identifier"):
        lookup_python_module_declaration(
            snapshot,
            module=module,
            declared_name="bad.name",
        )
    newer = _snapshot(tmp_path / "newer", {"src/use.py": "class target:\n    pass\n"})
    with pytest.raises(ValueError, match="snapshot"):
        lookup_python_module_declaration(newer, module=module, declared_name="target")


def test_reference_scope_and_binding_assessments(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/target.py": "def helper():\n    pass\n",
            "src/use.py": (
                "from target import helper\n"
                "helper()\n"
                "def caller(helper, *args, **kwargs):\n"
                "    helper()\n"
                "    [helper() for x in args]\n"
                "class C:\n"
                "    helper()\n"
                "def later():\n"
                "    local()\n"
                "    def local():\n        pass\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    outcomes = [a.outcome for a in analysis.assessments if a.source_text == "helper"]
    assert Outcome.RESOLVED in outcomes
    assert Outcome.SHADOWED_BINDING in outcomes
    assert Outcome.UNSUPPORTED_SCOPE in outcomes
    assert _outcome(analysis, "local") is Outcome.SHADOWED_BINDING


@pytest.mark.parametrize(
    ("source", "text", "expected"),
    [
        ("helper()\ndef helper():\n    pass\n", "helper", Outcome.UNRESOLVED_BINDING),
        ("helper = other\nhelper()\n", "helper", Outcome.SHADOWED_BINDING),
        (
            "def helper():\n    pass\nhelper.attribute\n",
            "helper.attribute",
            Outcome.UNSUPPORTED_RECEIVER,
        ),
        (
            "from absent import helper\nhelper()\n",
            "helper",
            Outcome.MODULE_UNRESOLVED,
        ),
        (
            "from target import helper\nhelper.attribute.deep\n",
            "helper.attribute.deep",
            Outcome.UNSUPPORTED_RECEIVER,
        ),
        (
            "from target import helper\nhelper.attribute\n",
            "helper.attribute",
            Outcome.UNSUPPORTED_RECEIVER,
        ),
        (
            "import target as alias\nalias\n",
            "alias",
            Outcome.UNSUPPORTED_RECEIVER,
        ),
        (
            "import target as alias\nalias.helper.attribute\n",
            "alias.helper.attribute",
            Outcome.UNSUPPORTED_RECEIVER,
        ),
        (
            "import target as alias\nalias.helper.attribute.deep\n",
            "alias.helper.attribute.deep",
            Outcome.UNSUPPORTED_RECEIVER,
        ),
        (
            "from target import helper\nexec('pass')\nhelper()\n",
            "helper",
            Outcome.AMBIGUOUS_BINDING,
        ),
    ],
)
def test_unresolved_reference_routes(
    tmp_path: Path,
    source: str,
    text: str,
    expected: Outcome,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"src/use.py": source, "src/target.py": "def helper():\n    pass\n"},
    )
    assert _outcome(_analysis(snapshot, "src/use.py"), text) is expected


def test_method_binding_outcomes(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/use.py": (
                "class Service:\n"
                "    def run(self):\n        pass\n"
                "    import other as missing\n"
                "Service.absent\nService.missing\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    assert _outcome(analysis, "Service.absent") is Outcome.METHOD_UNRESOLVED
    assert _outcome(analysis, "Service.missing") is Outcome.METHOD_UNRESOLVED


def test_missing_retained_source_segment_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"src/use.py": "def helper():\n    pass\nhelper()\n"},
    )
    monkeypatch.setattr(
        "devtools.context.python.references.declarations.analysis.ast.get_source_segment",
        lambda _content, _node: None,
    )
    with pytest.raises(ValueError, match="exact source text"):
        _analysis(snapshot, "src/use.py")


def test_incomplete_internal_binding_support_never_establishes_reference(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(tmp_path, {"src/use.py": "foo\n"})
    address = RepositoryResourceAddress("src/use.py")
    tree = ast.parse("foo\n")
    node = tree.body[0]
    assert isinstance(node, ast.Expr)
    assert isinstance(node.value, ast.Name)
    imports = derive_python_import_declarations(snapshot, resource_address=address)
    for kind, expected in (
        ("function", Outcome.TARGET_NOT_DECLARATION),
        ("imported-member", Outcome.UNSUPPORTED_RECEIVER),
    ):
        result = _resolve(
            snapshot,
            node.value,
            {},
            (_Binding("foo", kind, 1),),
            False,  # noqa: FBT003
            imports,
            _universe(snapshot),
            (),
            (),
            (),
        )
        assert result.outcome is expected


@pytest.mark.parametrize(
    "syntax",
    ["class Target: pass", "def Target(): pass", "async def Target(): pass"],
)
def test_decorated_imported_and_module_members_remain_unsupported(
    tmp_path: Path,
    syntax: str,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "src/native.py": "@decorator\n" + syntax + "\n",
            "src/use.py": (
                "from native import Target\nimport native as m\nTarget\nm.Target\n"
            ),
        },
    )
    analysis = _analysis(snapshot, "src/use.py")
    assert _outcome(analysis, "Target") is Outcome.TARGET_NOT_DECLARATION
    assert _outcome(analysis, "m.Target") is Outcome.TARGET_NOT_DECLARATION
    assert not analysis.references
