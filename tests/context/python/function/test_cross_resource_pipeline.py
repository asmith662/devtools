# Copyright (c) 2026
"""Tests for cross-resource Python function Context through request assembly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import (
    PythonFunctionExactNameQuery,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositorySnapshot,
    analyze_python_function_declaration_resources,
    assemble_python_function_context_model_request,
    disclose_python_function_exact_name_retrieval,
    materialize_python_function_disclosure_source,
    observe_repository_resources,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    import pytest

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _snapshot(
    tmp_path: Path,
    sources: Mapping[str, str],
) -> RepositorySnapshot:
    """Observe all explicitly supplied source fixtures into one snapshot."""
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
    )


def _forbid_reacquisition(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail if any post-observation stage attempts a filesystem read."""

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "cross-resource pipeline attempted filesystem reacquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden_read)


def test_cross_resource_match_reaches_request_without_reacquisition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only matching knowledge is resolved, rendered, and assembled."""
    selected_source = 'def selected_function():\n    return "TARGET"'
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": 'def helper():\n    return "A"\n',
            "b.py": f"{selected_source}\n",
            "unrelated.py": 'def selected_function():\n    return "UNSELECTED"\n',
        },
    )
    first_address = RepositoryResourceAddress("a.py")
    selected_address = RepositoryResourceAddress("b.py")
    _forbid_reacquisition(monkeypatch)

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(first_address, selected_address),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("selected_function"),
    )
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    task_request = ModelRequest(Prompt("Return the selected value.", "user"))
    request = assemble_python_function_context_model_request(
        task_request=task_request,
        context=rendered,
    )

    selected_knowledge = aggregate.analyses[1].declarations[0]
    assert [
        analysis.derivation.dependency.resource.address
        for analysis in aggregate.analyses
    ] == [first_address, selected_address]
    assert tuple(match.knowledge for match in retrieval.matches) == (
        selected_knowledge,
    )
    assert disclosure.selected_matches == retrieval.matches
    assert disclosure.items[0].selected_match is retrieval.matches[0]
    assert materialized.items[0].disclosure_item is disclosure.items[0]
    assert materialized.items[0].source_snapshot_id == snapshot.id
    assert materialized.items[0].source_content_identity == (
        snapshot.resource_at(selected_address).content_identity
    )
    assert materialized.items[0].source_text == selected_source
    assert "Repository-relative resource: b.py\n" in rendered.text
    assert selected_source in rendered.text
    assert "helper" not in rendered.text
    assert "UNSELECTED" not in rendered.text
    assert request.prompt.content.count(rendered.text) == 1
    assert rendered.text in request.prompt.content
    assert task_request.prompt.content in request.prompt.content


def test_duplicate_cross_resource_matches_survive_the_complete_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Same-name declarations retain source, identity, order, and correlation."""
    first_source = 'def selected_function():\n    return "A"'
    second_source = 'async def selected_function():\n    return "B"'
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": f"{first_source}\n",
            "b.py": f"{second_source}\n",
            "unrelated.py": "VALUE = 1\n",
        },
    )
    first_address = RepositoryResourceAddress("b.py")
    second_address = RepositoryResourceAddress("a.py")
    _forbid_reacquisition(monkeypatch)

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(first_address, second_address),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("selected_function"),
    )
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Compare selected functions.", "user")),
        context=rendered,
    )

    expected_knowledge = aggregate.declarations
    assert tuple(match.knowledge for match in retrieval.matches) == expected_knowledge
    assert disclosure.selected_matches == retrieval.matches
    assert (
        tuple(
            item.disclosure_item.selected_match.knowledge for item in materialized.items
        )
        == expected_knowledge
    )
    assert [item.source_text for item in materialized.items] == [
        second_source,
        first_source,
    ]
    assert [item.source_snapshot_id for item in materialized.items] == [
        snapshot.id,
        snapshot.id,
    ]
    assert [item.source_content_identity for item in materialized.items] == [
        snapshot.resource_at(first_address).content_identity,
        snapshot.resource_at(second_address).content_identity,
    ]
    assert len(
        {item.source_content_identity for item in materialized.items},
    ) == len(materialized.items)
    assert rendered.text.count("Declared name: selected_function\n") == len(
        materialized.items,
    )
    assert rendered.text.index(
        "Repository-relative resource: b.py\n",
    ) < rendered.text.index("Repository-relative resource: a.py\n")
    assert rendered.text.index(second_source) < rendered.text.index(first_source)
    assert request.prompt.content.count(rendered.text) == 1


def test_cross_resource_zero_remains_bounded_through_request_assembly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Zero matches require no resource resolution and make no absence claim."""
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": "def first():\n    pass\n",
            "b.py": "def second():\n    pass\n",
            "unrelated.py": "def missing():\n    pass\n",
        },
    )
    _forbid_reacquisition(monkeypatch)
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(
            RepositoryResourceAddress("a.py"),
            RepositoryResourceAddress("b.py"),
        ),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("missing"),
    )
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Investigate missing.", "user")),
        context=rendered,
    )

    assert retrieval.matches == ()
    assert disclosure.items == ()
    assert materialized.items == ()
    assert "Selected declarations: 0\n" in rendered.text
    assert "supplied exact-name retrieval result" in request.prompt.content
    lowered = request.prompt.content.lower()
    assert "does not exist" not in lowered
    assert "repository contains no" not in lowered
