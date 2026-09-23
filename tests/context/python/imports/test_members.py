# Copyright (c) 2026
# ruff: noqa: D103
"""Tests for one-facade imported-member function resolution."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.imports import (
    PythonFacadeCompetingBindingKind,
    PythonImportedMemberResolution,
    PythonImportedMemberResolutionOutcome,
    PythonImportedMemberUnsupportedReason,
    derive_python_import_declarations,
    resolve_python_imported_member,
)
from devtools.context.python.modules import (
    PythonModuleInterpretation,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath


def _snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000025"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(item) for item in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _interpret(
    snapshot: RepositorySnapshot,
    addresses: tuple[str, ...],
    *,
    root: str = ".",
) -> tuple[PythonModuleInterpretation, ...]:
    return interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot(root),
        resource_addresses=tuple(RepositoryResourceAddress(item) for item in addresses),
    ).interpretations


def _resolve(
    snapshot: RepositorySnapshot,
    *,
    interpretations: tuple[PythonModuleInterpretation, ...] | None = None,
    source_address: str = "consumer.py",
) -> PythonImportedMemberResolution:
    source = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress(source_address),
    )
    values = interpretations or _interpret(
        snapshot,
        tuple(item.address.value for item in snapshot.resources),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=values,
    )
    return resolve_python_imported_member(
        snapshot,
        source,
        source.declarations[0],
        module_universe=universe,
    )


@pytest.mark.parametrize(
    "target",
    ["def f():\n    pass\n", "async def f():\n    pass\n"],
)
def test_resolves_direct_sync_and_async_function(
    tmp_path: Path,
    target: str,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import f\n",
            "package/impl.py": target,
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.RESOLVED
    assert result.target_declaration is result.target_declarations[0]
    assert result.target_declaration.declared_name == "f"


@pytest.mark.parametrize(
    ("source", "reason"),
    [
        (
            "import package\n",
            PythonImportedMemberUnsupportedReason.SOURCE_NOT_IMPORTED_MEMBER,
        ),
        (
            "from package import *\n",
            PythonImportedMemberUnsupportedReason.SOURCE_STAR_IMPORT,
        ),
    ],
)
def test_source_must_be_a_named_imported_member(
    tmp_path: Path,
    source: str,
    reason: PythonImportedMemberUnsupportedReason,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"consumer.py": source, "package/__init__.py": ""},
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
    assert result.unsupported_reason is reason
    assert result.target_declaration is None


def test_source_module_resolution_states_are_preserved(tmp_path: Path) -> None:
    unresolved_snapshot = _snapshot(
        tmp_path,
        {"consumer.py": "from package import f\n"},
    )
    unresolved = _resolve(unresolved_snapshot)
    assert unresolved.outcome is (
        PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE
    )
    assert unresolved.target_declaration is None

    ambiguous_snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package.py": "",
            "package/__init__.py": "",
        },
    )
    ambiguous = _resolve(ambiguous_snapshot)
    assert ambiguous.outcome is PythonImportedMemberResolutionOutcome.AMBIGUOUS
    assert ambiguous.target_declaration is None

    relative_snapshot = _snapshot(
        tmp_path,
        {
            "package/consumer.py": "from .facade import f\n",
            "package/facade.py": "",
        },
    )
    unsupported = _resolve(relative_snapshot, source_address="package/consumer.py")
    assert unsupported.outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
    assert unsupported.unsupported_reason is (
        PythonImportedMemberUnsupportedReason.SOURCE_MODULE_RESOLUTION
    )


def test_source_alias_preserves_imported_identity_and_local_name(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f as renamed\n",
            "package/__init__.py": "from .impl import f\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.RESOLVED
    assert result.source_declaration.imported_name == "f"
    assert result.source_declaration.local_alias == "renamed"


def test_facade_alias_uses_public_binding_and_private_target_name(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import public_f\n",
            "package/__init__.py": "from .impl import f as public_f\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.RESOLVED
    assert result.facade_bindings[0].imported_name == "f"
    assert result.facade_bindings[0].local_alias == "public_f"
    assert result.target_declaration is not None
    assert result.target_declaration.declared_name == "f"


def test_unrelated_direct_facade_bindings_do_not_compete(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": (
                "import os\n"
                "def other():\n    pass\n"
                "class Other:\n    pass\n"
                "holder.value = object()\n"
                "from .impl import f\n"
            ),
            "package/impl.py": "def f():\n    pass\n",
        },
    )

    assert _resolve(snapshot).outcome is PythonImportedMemberResolutionOutcome.RESOLVED


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("VALUE = 1\n", PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE),
        (
            "class f:\n    pass\n",
            PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE,
        ),
        (
            "def outer():\n    def f():\n        pass\n",
            PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE,
        ),
        (
            "class Holder:\n    def f(self):\n        pass\n",
            PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE,
        ),
        (
            "def f():\n    pass\ndef f():\n    pass\n",
            PythonImportedMemberResolutionOutcome.AMBIGUOUS,
        ),
    ],
)
def test_only_one_direct_function_is_an_eligible_target(
    tmp_path: Path,
    target: str,
    expected: PythonImportedMemberResolutionOutcome,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import f\n",
            "package/impl.py": target,
        },
    )
    assert _resolve(snapshot).outcome is expected


def test_unresolved_target_module_retains_facade_resolution(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .missing import f\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is (
        PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE
    )
    assert result.facade_module_resolution is not None
    assert result.facade_module_resolution.requested_module == "package.missing"
    assert result.target is None


def test_absent_and_duplicate_facade_bindings_are_distinct_states(
    tmp_path: Path,
) -> None:
    absent = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import other\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    absent_result = _resolve(absent)
    assert absent_result.outcome is (
        PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE
    )
    assert absent_result.facade_bindings == ()

    duplicate = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": (
                "from .first import f\nfrom .second import f\n"
            ),
            "package/first.py": "def f():\n    pass\n",
            "package/second.py": "def f():\n    pass\n",
        },
    )
    duplicate_result = _resolve(duplicate)
    assert duplicate_result.outcome is PythonImportedMemberResolutionOutcome.AMBIGUOUS
    expected_binding_count = 2
    assert len(duplicate_result.facade_bindings) == expected_binding_count


def test_unsupported_facade_relative_resolution_is_preserved(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from ..impl import f\n",
            "impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
    assert result.unsupported_reason is (
        PythonImportedMemberUnsupportedReason.FACADE_MODULE_RESOLUTION
    )


def test_ambiguous_target_module_interpretation_is_not_selected(
    tmp_path: Path,
) -> None:
    resources = {
        "consumer.py": "from package import f\n",
        "package/__init__.py": "from .impl import f\n",
        "package/impl.py": "def f():\n    pass\n",
        "alternate/package/impl.py": "def f():\n    pass\n",
    }
    snapshot = _snapshot(tmp_path, resources)
    standard = _interpret(snapshot, tuple(resources))
    alternate = _interpret(snapshot, ("alternate/package/impl.py",), root="alternate")
    result = _resolve(snapshot, interpretations=(*standard, *alternate))

    assert result.outcome is PythonImportedMemberResolutionOutcome.AMBIGUOUS
    assert result.facade_module_resolution is not None
    expected_match_count = 2
    assert len(result.facade_module_resolution.matches) == expected_match_count
    assert result.target is None


@pytest.mark.parametrize(
    ("facade", "kind"),
    [
        (
            "from .impl import f\ndef f():\n    pass\n",
            PythonFacadeCompetingBindingKind.FUNCTION,
        ),
        (
            "def f():\n    pass\nfrom .impl import f\n",
            PythonFacadeCompetingBindingKind.FUNCTION,
        ),
        (
            "from .impl import f\nf = object()\n",
            PythonFacadeCompetingBindingKind.ASSIGNMENT,
        ),
        (
            "from .impl import f\nimport other as f\n",
            PythonFacadeCompetingBindingKind.IMPORT,
        ),
        (
            "from .impl import f\nclass f:\n    pass\n",
            PythonFacadeCompetingBindingKind.CLASS,
        ),
        (
            "from .impl import f\nf, other = object(), object()\n",
            PythonFacadeCompetingBindingKind.ASSIGNMENT,
        ),
    ],
)
def test_competing_direct_facade_binding_is_unsupported(
    tmp_path: Path,
    facade: str,
    kind: PythonFacadeCompetingBindingKind,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": facade,
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
    assert result.unsupported_reason is (
        PythonImportedMemberUnsupportedReason.COMPETING_FACADE_BINDING
    )
    assert result.competing_facade_bindings[0].kind is kind


@pytest.mark.parametrize(
    "facade",
    [
        "if enabled:\n    from .impl import f\n",
        "try:\n    from .impl import f\nexcept ImportError:\n    pass\n",
    ],
)
def test_nested_facade_import_is_unsupported(tmp_path: Path, facade: str) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": facade,
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
    assert result.unsupported_reason is (
        PythonImportedMemberUnsupportedReason.NESTED_FACADE_IMPORT
    )


def test_star_facade_import_is_unsupported(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import *\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)
    assert result.outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
    assert result.unsupported_reason is (
        PythonImportedMemberUnsupportedReason.FACADE_STAR_IMPORT
    )


def test_two_facade_chain_does_not_recurse(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .api import f\n",
            "package/api.py": "from .impl import f\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.outcome is (
        PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE
    )
    assert result.target is not None
    assert result.target.resource.address.value == "package/api.py"
    assert result.target_declarations == ()


@pytest.mark.parametrize("all_value", ['["f"]', "[]"])
def test_dunder_all_does_not_change_direct_binding_semantics(
    tmp_path: Path,
    all_value: str,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": (
                f"__all__ = {all_value}\nfrom .impl import f\n"
            ),
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    assert _resolve(snapshot).outcome is PythonImportedMemberResolutionOutcome.RESOLVED


def test_resolved_provenance_retains_exact_source_facade_and_target(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import f\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    result = _resolve(snapshot)

    assert result.source_declaration.support.resource_address.value == "consumer.py"
    assert result.source_module_resolution is not None
    assert result.source_module_resolution.matches[0] is result.facade
    assert result.facade_bindings[0].support.resource_address.value == (
        "package/__init__.py"
    )
    assert result.facade_module_resolution is not None
    assert result.facade_module_resolution.matches[0] is result.target
    assert result.target is not None
    assert result.target.resource.address.value == "package/impl.py"
    assert result.target_declaration is not None
    assert result.target_declaration.support.resource_address.value == "package/impl.py"
    assert result.target_declaration.subject.snapshot_id == snapshot.id


def test_result_identity_is_independent_of_universe_input_order(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import f\n",
            "package/impl.py": "def f():\n    pass\n",
            "unrelated.py": "",
        },
    )
    interpretations = _interpret(
        snapshot,
        tuple(item.address.value for item in snapshot.resources),
    )
    first = _resolve(snapshot, interpretations=interpretations)
    second = _resolve(snapshot, interpretations=tuple(reversed(interpretations)))

    assert first.outcome is second.outcome
    assert first.identity == second.identity


def test_inputs_must_share_one_repository_snapshot(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import f\n",
            "package/__init__.py": "from .impl import f\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("consumer.py"),
    )
    interpretations = _interpret(
        snapshot,
        tuple(item.address.value for item in snapshot.resources),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretations,
    )

    with pytest.raises(ValueError, match="does not belong"):
        resolve_python_imported_member(
            snapshot,
            analysis,
            replace(analysis.declarations[0], declaration_ordinal=99),
            module_universe=universe,
        )

    changed = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import changed\n",
            "package/__init__.py": "",
        },
    )
    with pytest.raises(ValueError, match="analysis does not match"):
        resolve_python_imported_member(
            changed,
            analysis,
            analysis.declarations[0],
            module_universe=define_python_module_interpretation_universe(
                repository_id=changed.repository_id,
                interpretations=(),
            ),
        )

    other_repository = RepositoryId.parse("00000000-0000-4000-8000-000000000026")
    with pytest.raises(ValueError, match="universe does not match"):
        resolve_python_imported_member(
            snapshot,
            analysis,
            analysis.declarations[0],
            module_universe=replace(universe, repository_id=other_repository),
        )

    changed_interpretations = _interpret(
        changed,
        tuple(item.address.value for item in changed.resources),
    )
    with pytest.raises(ValueError, match="another snapshot"):
        resolve_python_imported_member(
            snapshot,
            analysis,
            analysis.declarations[0],
            module_universe=define_python_module_interpretation_universe(
                repository_id=snapshot.repository_id,
                interpretations=changed_interpretations,
            ),
        )

    with pytest.raises(ValueError, match="source interpretation"):
        resolve_python_imported_member(
            snapshot,
            analysis,
            analysis.declarations[0],
            module_universe=universe,
            source_interpretations=(changed_interpretations[0],),
        )
