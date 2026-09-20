# Copyright (c) 2026
"""Tests for explicit multi-resource Python declaration analysis composition."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionDeclarationAnalysisAggregate,
    PythonFunctionExactNameQuery,
    PythonModuleParseError,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositorySnapshot,
    analyze_python_function_declaration_resources,
    observe_repository_resources,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"
_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024


def _snapshot(
    tmp_path: Path,
    sources: Mapping[str, str],
) -> RepositorySnapshot:
    """Observe an explicit addressed source collection for aggregation tests."""
    addresses: list[RepositoryResourceAddress] = []
    for value, content in sources.items():
        address = RepositoryResourceAddress(value)
        path = tmp_path.joinpath(*address.parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="")
        addresses.append(address)
    return observe_repository_resources(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )


def test_aggregates_independent_analyses_for_caller_ordered_resources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Selected resources retain derivations while combined knowledge is retrievable."""
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": "def duplicate():\n    return 'a'\n\ndef only_a():\n    pass\n",
            "b.py": "async def duplicate():\n    return 'b'\n",
            "unselected.py": "def broken(:\n    pass\n",
        },
    )
    first_address = RepositoryResourceAddress("b.py")
    second_address = RepositoryResourceAddress("a.py")

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "aggregation attempted repository acquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden_read)

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(first_address, second_address),
    )
    repeated = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(first_address, second_address),
    )

    assert isinstance(aggregate, PythonFunctionDeclarationAnalysisAggregate)
    assert aggregate == repeated
    assert [
        analysis.derivation.dependency.resource.address
        for analysis in aggregate.analyses
    ] == [first_address, second_address]
    assert aggregate.analyses[0].derivation.dependency.resource is (
        snapshot.resource_at(first_address)
    )
    assert aggregate.analyses[1].derivation.dependency.resource is (
        snapshot.resource_at(second_address)
    )
    assert [item.declared_name for item in aggregate.declarations] == [
        "duplicate",
        "duplicate",
        "only_a",
    ]
    expected_knowledge = (
        aggregate.analyses[0].declarations[0],
        *aggregate.analyses[1].declarations,
    )
    assert all(
        declaration is expected
        for declaration, expected in zip(
            aggregate.declarations,
            expected_knowledge,
            strict=True,
        )
    )
    assert all(
        item.support.resource_address != RepositoryResourceAddress("unselected.py")
        for item in aggregate.declarations
    )
    first_duplicate, second_duplicate = aggregate.declarations[:2]
    assert first_duplicate.subject.identity != second_duplicate.subject.identity
    assert first_duplicate.identity != second_duplicate.identity
    assert not hasattr(aggregate, "derivation")
    assert not hasattr(aggregate, "coverage")

    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("duplicate"),
    )

    assert tuple(match.knowledge for match in retrieval.matches) == (
        first_duplicate,
        second_duplicate,
    )


def test_aggregate_preserves_per_resource_zero_coverage(
    tmp_path: Path,
) -> None:
    """A zero analysis remains visible beside another resource's declarations."""
    snapshot = _snapshot(
        tmp_path,
        {
            "zero.py": "VALUE = 1\n",
            "positive.py": "def available():\n    pass\n",
        },
    )
    zero_address = RepositoryResourceAddress("zero.py")
    positive_address = RepositoryResourceAddress("positive.py")

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(zero_address, positive_address),
    )

    zero, positive = aggregate.analyses
    assert zero.coverage.IS_EXHAUSTIVE is True
    assert zero.coverage.declaration_count == 0
    assert zero.declarations == ()
    assert positive.coverage.declaration_count == 1
    assert aggregate.declarations == positive.declarations


def test_all_selected_exhaustive_zero_produces_empty_combined_knowledge(
    tmp_path: Path,
) -> None:
    """Combined zero preserves each bounded coverage without claiming absence."""
    snapshot = _snapshot(
        tmp_path,
        {
            "first.py": "VALUE = 1\n",
            "second.py": "class Holder:\n    def method(self):\n        pass\n",
        },
    )

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(
            RepositoryResourceAddress("first.py"),
            RepositoryResourceAddress("second.py"),
        ),
    )

    assert len(aggregate.analyses) == len(snapshot.resources)
    assert all(analysis.coverage.IS_EXHAUSTIVE for analysis in aggregate.analyses)
    assert all(
        analysis.coverage.declaration_count == 0 for analysis in aggregate.analyses
    )
    assert aggregate.declarations == ()


def test_invalid_aggregate_selections_fail_before_parsing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty, duplicate, and absent selections publish no aggregate analyses."""
    snapshot = _snapshot(tmp_path, {"available.py": "def available():\n    pass\n"})
    available = RepositoryResourceAddress("available.py")

    def forbidden_parse(*_args: object, **_kwargs: object) -> None:
        msg = "invalid selection attempted parsing"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse",
        forbidden_parse,
    )
    with pytest.raises(ValueError, match="at least one"):
        analyze_python_function_declaration_resources(
            snapshot,
            resource_addresses=(),
        )
    with pytest.raises(ValueError, match="distinct"):
        analyze_python_function_declaration_resources(
            snapshot,
            resource_addresses=(available, available),
        )
    with pytest.raises(ValueError, match="does not contain resource address"):
        analyze_python_function_declaration_resources(
            snapshot,
            resource_addresses=(RepositoryResourceAddress("absent.py"),),
        )


def test_selected_parse_failure_returns_no_successful_aggregate(
    tmp_path: Path,
) -> None:
    """One failed required analysis prevents successful aggregate publication."""
    snapshot = _snapshot(
        tmp_path,
        {
            "valid.py": "def available():\n    pass\n",
            "invalid.py": "def broken(:\n    pass\n",
        },
    )

    with pytest.raises(PythonModuleParseError) as captured:
        analyze_python_function_declaration_resources(
            snapshot,
            resource_addresses=(
                RepositoryResourceAddress("valid.py"),
                RepositoryResourceAddress("invalid.py"),
            ),
        )

    assert captured.value.derivation.dependency.resource.address == (
        RepositoryResourceAddress("invalid.py")
    )
    assert not hasattr(captured.value, "aggregate")
