# Copyright (c) 2026
"""Tests for exact source materialization of Python function disclosure."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionExactNameContextDisclosure,
    PythonFunctionExactNameQuery,
    PythonFunctionSourceMaterializationError,
    PythonSourceRange,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositorySnapshot,
    derive_python_function_declarations,
    disclose_python_function_exact_name_retrieval,
    materialize_python_function_disclosure_source,
    observe_repository_resource,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _snapshot(
    tmp_path: Path,
    content: str,
    *,
    address: str = "module.py",
) -> RepositorySnapshot:
    """Observe exact UTF-8 fixture bytes into identified repository state."""
    source = tmp_path.joinpath(*address.split("/"))
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(content.encode("utf-8"))
    return observe_repository_resource(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        address=RepositoryResourceAddress(address),
    )


def _disclosure(
    snapshot: RepositorySnapshot,
    name: str,
) -> PythonFunctionExactNameContextDisclosure:
    """Produce a disclosure through the implemented preceding layers."""
    analysis = derive_python_function_declarations(snapshot)
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=PythonFunctionExactNameQuery(name),
    )
    return disclose_python_function_exact_name_retrieval(retrieval)


def test_materializes_duplicate_sync_and_async_exact_multiline_source(
    tmp_path: Path,
) -> None:
    """Materialization preserves CRLF, non-ASCII text, order, and correlation."""
    snapshot = _snapshot(
        tmp_path,
        '# préface\r\ndef duplicate():\r\n    return "café"\r\n\r\n'
        'async def duplicate():\r\n    return "naïve"\r\n',
    )
    disclosure = _disclosure(snapshot, "duplicate")

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )

    assert materialized.disclosure is disclosure
    assert [item.source_text for item in materialized.items] == [
        'def duplicate():\r\n    return "café"',
        'async def duplicate():\r\n    return "naïve"',
    ]
    knowledge_identities = {
        item.disclosure_item.selected_match.knowledge.identity
        for item in materialized.items
    }
    assert len(knowledge_identities) == len(materialized.items)
    for materialized_item, disclosure_item in zip(
        materialized.items,
        disclosure.items,
        strict=True,
    ):
        assert materialized_item.disclosure_item is disclosure_item
        assert materialized_item.source_snapshot_id == snapshot.id
        assert (
            materialized_item.source_content_identity
            == snapshot.resource.content_identity
        )
    repeated = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    assert repeated == materialized
    assert repeated.identity == materialized.identity
    assert not hasattr(materialized, "model_request")
    assert not hasattr(materialized, "summary")
    assert not hasattr(materialized, "confidence")
    assert not hasattr(materialized, "ranking")


def test_materializes_single_line_using_utf8_byte_columns(tmp_path: Path) -> None:
    """UTF-8 byte columns extract non-ASCII single-line syntax exactly."""
    expected = 'def café(): return "olé"'
    snapshot = _snapshot(tmp_path, f"# naïve\n{expected}\n")
    disclosure = _disclosure(snapshot, "café")

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )

    source_range = disclosure.items[0].source_occurrence.source_range
    assert source_range.end_column_utf8 == len(expected.encode("utf-8"))
    assert source_range.end_column_utf8 != len(expected)
    assert materialized.items[0].source_text == expected


def test_rejects_mismatched_snapshot_and_resource_state(tmp_path: Path) -> None:
    """Coordinates cannot be applied to another snapshot or addressed resource."""
    snapshot = _snapshot(tmp_path, "def target():\n    return 1\n")
    disclosure = _disclosure(snapshot, "target")
    changed_snapshot = _snapshot(tmp_path, "def target():\n    return 2\n")

    with pytest.raises(PythonFunctionSourceMaterializationError, match="snapshot"):
        materialize_python_function_disclosure_source(
            disclosure=disclosure,
            snapshot=changed_snapshot,
        )

    mismatched_resource = replace(
        snapshot.resource,
        address=RepositoryResourceAddress("other.py"),
    )
    mismatched_address_snapshot = replace(snapshot, resource=mismatched_resource)
    with pytest.raises(PythonFunctionSourceMaterializationError, match="resource"):
        materialize_python_function_disclosure_source(
            disclosure=disclosure,
            snapshot=mismatched_address_snapshot,
        )


@pytest.mark.parametrize(
    ("source_range", "match"),
    [
        (PythonSourceRange(1, 30, 1, 29), "ends before"),
        (PythonSourceRange(1, 0, 2, 0), "line is outside"),
        (PythonSourceRange(1, 0, 1, 100), "column is outside"),
        (PythonSourceRange(1, 8, 1, 26), "UTF-8 character boundaries"),
    ],
)
def test_rejects_source_ranges_that_cannot_be_faithfully_applied(
    tmp_path: Path,
    source_range: PythonSourceRange,
    match: str,
) -> None:
    """Malformed coordinates fail instead of producing misleading source."""
    snapshot = _snapshot(tmp_path, 'def café(): return "olé"\n')
    disclosure = _disclosure(snapshot, "café")
    disclosure_item = disclosure.items[0]
    invalid_occurrence = replace(
        disclosure_item.source_occurrence,
        source_range=source_range,
    )
    invalid_item = replace(
        disclosure_item,
        source_occurrence=invalid_occurrence,
    )
    invalid_disclosure = replace(disclosure, items=(invalid_item,))

    with pytest.raises(PythonFunctionSourceMaterializationError, match=match):
        materialize_python_function_disclosure_source(
            disclosure=invalid_disclosure,
            snapshot=snapshot,
        )


def test_zero_disclosure_materializes_without_resolving_snapshot_source(
    tmp_path: Path,
) -> None:
    """Zero selection needs no occurrence resolution or source extraction."""
    snapshot = _snapshot(tmp_path, "def available():\n    pass\n")
    disclosure = _disclosure(snapshot, "missing")
    unrelated_snapshot = _snapshot(
        tmp_path,
        "VALUE = 1\n",
        address="unrelated.py",
    )

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=unrelated_snapshot,
    )

    assert materialized.disclosure is disclosure
    assert materialized.items == ()
    assert materialized.identity


def test_materialization_does_not_reacquire_parse_derive_or_retrieve(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Materialization consumes only disclosure and explicit snapshot values."""
    snapshot = _snapshot(tmp_path, "def target():\n    pass\n")
    disclosure = _disclosure(snapshot, "target")

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "materialization attempted an upstream operation"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.read", forbidden)
    monkeypatch.setattr("devtools.context.python_declarations.ast.parse", forbidden)
    monkeypatch.setattr(
        "devtools.context.python_declarations.derive_python_function_declarations",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python_function_retrieval.retrieve_python_functions_by_exact_name",
        forbidden,
    )

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )

    assert materialized.items[0].disclosure_item is disclosure.items[0]
