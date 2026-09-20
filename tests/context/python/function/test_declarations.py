# Copyright (c) 2026
"""Tests for direct module-body Python function declaration knowledge."""

from __future__ import annotations

import platform
import sys
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionDeclarationKind,
    PythonFunctionDeclarationKnowledge,
    PythonFunctionSubject,
    PythonModuleParseError,
    PythonSourceOccurrence,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositorySnapshot,
    derive_python_function_declarations,
    observe_repository_resource,
    observe_repository_resources,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _repository() -> Repository:
    """Return one deterministic logical Repository."""
    return Repository(RepositoryId.parse(_REPOSITORY_ID))


def _snapshot(tmp_path: Path, content: str) -> RepositorySnapshot:
    """Observe one Python fixture through the production snapshot boundary."""
    source = tmp_path / "module.py"
    source.write_text(content, encoding="utf-8", newline="")
    return observe_repository_resource(
        repository=_repository(),
        root=ResolvedPath(tmp_path),
        address=RepositoryResourceAddress("module.py"),
    )


def _multi_snapshot(
    tmp_path: Path,
    *,
    first: str,
    second: str,
) -> RepositorySnapshot:
    """Observe two addressed Python fixtures into one identified snapshot."""
    (tmp_path / "a.py").write_text(first, encoding="utf-8", newline="")
    (tmp_path / "b.py").write_text(second, encoding="utf-8", newline="")
    return observe_repository_resources(
        repository=_repository(),
        root=ResolvedPath(tmp_path),
        addresses=(
            RepositoryResourceAddress("a.py"),
            RepositoryResourceAddress("b.py"),
        ),
    )


def test_derives_source_grounded_direct_function_declaration_knowledge(
    tmp_path: Path,
) -> None:
    """Direct sync and async declarations remain distinct; a method is excluded."""
    snapshot = _snapshot(
        tmp_path,
        """def duplicate():
    pass

async def duplicate():
    pass

class Holder:
    def duplicate(self):
        pass
""",
    )

    result = derive_python_function_declarations(snapshot)

    expected_declaration_count = len(PythonFunctionDeclarationKind)
    first_start_line = 1
    first_end_line = first_start_line + 1
    second_start_line = first_end_line + expected_declaration_count
    second_end_line = second_start_line + 1
    assert len(result.declarations) == expected_declaration_count
    first, second = result.declarations
    assert all(
        isinstance(declaration, PythonFunctionDeclarationKnowledge)
        for declaration in result.declarations
    )
    assert [declaration.declared_name for declaration in result.declarations] == [
        "duplicate",
        "duplicate",
    ]
    assert [declaration.declaration_kind for declaration in result.declarations] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
    ]
    assert first.support.source_range.start_line == first_start_line
    assert first.support.source_range.end_line == first_end_line
    assert second.support.source_range.start_line == second_start_line
    assert second.support.source_range.end_line == second_end_line
    assert first.support != second.support
    assert first.subject != second.subject
    assert first.subject.identity != second.subject.identity
    assert first.identity != second.identity
    assert first.declared_name == second.declared_name
    assert isinstance(first.support, PythonSourceOccurrence)
    assert isinstance(first.subject, PythonFunctionSubject)
    assert not isinstance(first.support, PythonFunctionSubject)
    assert first.support.snapshot_id == snapshot.id
    assert first.support.resource_address == snapshot.resource.address
    assert first.subject.snapshot_id == snapshot.id
    assert first.derivation_identity == result.derivation.identity
    assert first.PROPOSITION == result.derivation.definition.PROPOSITION
    assert result.coverage.derivation_identity == result.derivation.identity
    assert result.coverage.declaration_count == expected_declaration_count
    assert result.coverage.IS_EXHAUSTIVE is True
    assert result.coverage.SCOPE == (
        "direct-module-body-ast.FunctionDef-or-ast.AsyncFunctionDef"
    )


def test_derivation_is_reproducible_and_records_narrow_semantic_input(
    tmp_path: Path,
) -> None:
    """Equivalent realization retains definition, dependency, and result identity."""
    snapshot = _snapshot(tmp_path, "def function():\n    pass\n")

    first = derive_python_function_declarations(snapshot)
    second = derive_python_function_declarations(snapshot)

    assert first == second
    assert first.derivation.identity == second.derivation.identity
    assert first.declarations[0].identity == second.declarations[0].identity
    definition = first.derivation.definition
    assert definition.identity == second.derivation.definition.identity
    assert definition.analyzer_semantics_version == "2"
    assert definition.parser_implementation == sys.implementation.name
    assert definition.parser_runtime_version == platform.python_version()
    assert definition.grammar_feature_version == (3, 12)
    assert definition.TRAVERSAL_SEMANTICS == "direct-ast-module-body-only-v1"
    assert definition.NODE_VOCABULARY == (
        "ast.FunctionDef",
        "ast.AsyncFunctionDef",
    )
    upgraded_definition = replace(definition, analyzer_semantics_version="3")
    different_parser = replace(
        definition,
        parser_runtime_version=f"{definition.parser_runtime_version}-different",
    )
    assert upgraded_definition.identity != definition.identity
    assert different_parser.identity != definition.identity
    assert replace(first.derivation, definition=upgraded_definition).identity != (
        first.derivation.identity
    )
    dependency = first.derivation.dependency
    assert dependency.snapshot_id == snapshot.id
    assert dependency.repository_id == snapshot.repository_id
    assert dependency.resource == snapshot.resource
    assert first.declarations[0].subject.resource_dependency_identity == (
        dependency.identity
    )
    assert dependency.identity == second.derivation.dependency.identity
    assert not hasattr(dependency, "root")


def test_valid_module_with_no_direct_declarations_is_exhaustive_zero(
    tmp_path: Path,
) -> None:
    """A successful complete traversal can establish exhaustive zero."""
    snapshot = _snapshot(
        tmp_path,
        """VALUE = 1

class Holder:
    def method(self):
        pass

if VALUE:
    def conditional():
        pass
""",
    )

    result = derive_python_function_declarations(snapshot)

    assert result.declarations == ()
    assert result.coverage.declaration_count == 0
    assert result.coverage.IS_EXHAUSTIVE is True


def test_invalid_python_is_parse_failure_without_successful_coverage(
    tmp_path: Path,
) -> None:
    """Syntax failure is observably different from exhaustive zero."""
    snapshot = _snapshot(tmp_path, "def broken(:\n    pass\n")

    with pytest.raises(PythonModuleParseError) as captured:
        derive_python_function_declarations(snapshot)

    error = captured.value
    assert error.derivation.dependency.snapshot_id == snapshot.id
    assert error.derivation.definition.grammar_feature_version == (3, 12)
    assert error.parser_message
    assert error.line_number == 1
    assert error.parser_offset is not None
    assert "module.py" in str(error)
    assert not hasattr(error, "coverage")


def test_multiple_same_name_direct_declarations_have_distinct_subjects(
    tmp_path: Path,
) -> None:
    """Declared text is not subject identity or declaration-result identity."""
    snapshot = _snapshot(
        tmp_path,
        """def repeated():
    pass

def repeated():
    pass

def repeated():
    pass
""",
    )

    result = derive_python_function_declarations(snapshot)

    expected_names = [
        "repeated",
        "repeated",
        "repeated",
    ]
    expected_count = len(expected_names)
    assert [item.declared_name for item in result.declarations] == expected_names
    subject_identities = {item.subject.identity for item in result.declarations}
    assert len(subject_identities) == expected_count
    assert len({item.identity for item in result.declarations}) == expected_count
    assert result.coverage.declaration_count == expected_count


def test_surrounding_source_shift_changes_source_grounding(
    tmp_path: Path,
) -> None:
    """Snapshot-local grounding follows harmless line movement in new state."""
    first_snapshot = _snapshot(tmp_path, "def function():\n    pass\n")
    first = derive_python_function_declarations(first_snapshot)

    second_snapshot = _snapshot(
        tmp_path,
        "# harmless surrounding source\n\ndef function():\n    pass\n",
    )
    second = derive_python_function_declarations(second_snapshot)

    first_declaration = first.declarations[0]
    second_declaration = second.declarations[0]
    shifted_start_line = first_declaration.support.source_range.start_line + 2
    assert first_declaration.support.source_range.start_line == 1
    assert second_declaration.support.source_range.start_line == shifted_start_line
    assert first_declaration.support != second_declaration.support
    assert first_declaration.subject.identity != second_declaration.subject.identity
    assert first.derivation.definition == second.derivation.definition
    assert first.derivation.dependency != second.derivation.dependency


def test_source_range_uses_utf8_byte_columns(tmp_path: Path) -> None:
    """Non-ASCII syntax demonstrates the local stdlib AST column contract."""
    final_line = '    return "é"'
    snapshot = _snapshot(tmp_path, f"def café():\n{final_line}\n")

    declaration = derive_python_function_declarations(snapshot).declarations[0]
    source_range = declaration.support.source_range
    expected_end_line = source_range.start_line + 1

    assert declaration.declared_name == "café"
    assert source_range.start_line == 1
    assert source_range.start_column_utf8 == 0
    assert source_range.end_line == expected_end_line
    assert source_range.end_column_utf8 == len(final_line.encode("utf-8"))
    assert source_range.end_column_utf8 != len(final_line)


def test_explicitly_selected_multi_snapshot_resources_are_distinct_dependencies(
    tmp_path: Path,
) -> None:
    """Each derivation consumes only its selected observed resource occurrence."""
    snapshot = _multi_snapshot(
        tmp_path,
        first="def duplicate():\n    return 'a'\n\ndef only_a():\n    pass\n",
        second="async def duplicate():\n    return 'b'\n\ndef only_b():\n    pass\n",
    )
    first_address = RepositoryResourceAddress("a.py")
    second_address = RepositoryResourceAddress("b.py")

    first = derive_python_function_declarations(
        snapshot,
        resource_address=first_address,
    )
    second = derive_python_function_declarations(
        snapshot,
        resource_address=second_address,
    )

    assert [item.declared_name for item in first.declarations] == [
        "duplicate",
        "only_a",
    ]
    assert [item.declared_name for item in second.declarations] == [
        "duplicate",
        "only_b",
    ]
    assert first.derivation.dependency.resource is snapshot.resource_at(first_address)
    assert second.derivation.dependency.resource is snapshot.resource_at(second_address)
    assert {item.support.resource_address for item in first.declarations} == {
        first_address,
    }
    assert {item.support.resource_address for item in second.declarations} == {
        second_address,
    }
    first_duplicate = first.declarations[0]
    second_duplicate = second.declarations[0]
    assert first_duplicate.declared_name == second_duplicate.declared_name
    assert first_duplicate.subject.declaration_ordinal == (
        second_duplicate.subject.declaration_ordinal
    )
    assert first_duplicate.subject.identity != second_duplicate.subject.identity
    assert first_duplicate.identity != second_duplicate.identity
    assert first.derivation.identity != second.derivation.identity


def test_multi_snapshot_selection_rejects_an_unobserved_address(
    tmp_path: Path,
) -> None:
    """A derivation cannot consume source absent from its identified snapshot."""
    snapshot = _multi_snapshot(
        tmp_path,
        first="def first():\n    pass\n",
        second="def second():\n    pass\n",
    )

    with pytest.raises(ValueError, match="does not contain resource address"):
        derive_python_function_declarations(
            snapshot,
            resource_address=RepositoryResourceAddress("absent.py"),
        )
    with pytest.raises(ValueError, match="exactly one"):
        derive_python_function_declarations(snapshot)


def test_selected_multi_resource_zero_and_parse_failure_remain_distinct(
    tmp_path: Path,
) -> None:
    """Only the selected resource determines successful zero or parse failure."""
    snapshot = _multi_snapshot(
        tmp_path,
        first="VALUE = 1\n",
        second="def broken(:\n    pass\n",
    )
    first_address = RepositoryResourceAddress("a.py")
    second_address = RepositoryResourceAddress("b.py")

    exhaustive_zero = derive_python_function_declarations(
        snapshot,
        resource_address=first_address,
    )

    assert exhaustive_zero.declarations == ()
    assert exhaustive_zero.coverage.declaration_count == 0
    assert exhaustive_zero.coverage.IS_EXHAUSTIVE is True
    assert exhaustive_zero.derivation.dependency.resource.address == first_address
    with pytest.raises(PythonModuleParseError) as captured:
        derive_python_function_declarations(
            snapshot,
            resource_address=second_address,
        )
    assert captured.value.derivation.dependency.resource.address == second_address
    assert not hasattr(captured.value, "coverage")


def test_explicit_resource_derivation_performs_no_filesystem_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Derivation consumes only selected state already retained by the snapshot."""
    snapshot = _multi_snapshot(
        tmp_path,
        first="def selected():\n    pass\n",
        second="def unselected():\n    pass\n",
    )

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "derivation attempted repository acquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden_read)

    result = derive_python_function_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("a.py"),
    )

    assert [item.declared_name for item in result.declarations] == ["selected"]
