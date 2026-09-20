# Copyright (c) 2026
"""Tests for resource selection from exact-name Python function retrieval."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import (
    PythonFunctionExactNameQuery,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    analyze_python_function_declaration_resources,
    assemble_python_function_context_model_request,
    disclose_python_function_exact_name_retrieval,
    materialize_python_function_disclosure_source,
    observe_repository_resources,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
    select_python_function_resources_from_exact_name_retrieval,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    import pytest

    from devtools.context import RepositorySnapshot

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"
_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024


def _observe(
    tmp_path: Path,
    resources: Mapping[str, str],
) -> RepositorySnapshot:
    """Observe an explicit fixture collection through the production boundary."""
    addresses = tuple(RepositoryResourceAddress(path) for path in resources)
    for path, content in resources.items():
        source = tmp_path.joinpath(*path.split("/"))
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(content, encoding="utf-8", newline="")
    return observe_repository_resources(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )


def test_selects_matching_resources_without_altering_context_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Selection exposes match resources while the original retrieval drives Context."""
    addresses = {
        name: RepositoryResourceAddress(name)
        for name in ("a.py", "b.py", "c.py", "d.py")
    }
    snapshot = _observe(
        tmp_path,
        {
            "a.py": "def helper():\n    return 'A'\n",
            "b.py": "def selected_function():\n    return 'B'\n",
            "c.py": "async def selected_function():\n    return 'C'\n",
            "d.py": "def selected_function():\n    return 'UNANALYZED'\n",
        },
    )

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "post-observation pipeline attempted filesystem acquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden_read)
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(addresses["a.py"], addresses["b.py"], addresses["c.py"]),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("selected_function"),
    )

    selection = select_python_function_resources_from_exact_name_retrieval(retrieval)

    assert selection.retrieval is retrieval
    assert selection.resource_addresses == (addresses["b.py"], addresses["c.py"])
    assert tuple(selected.snapshot_id for selected in selection.selected_resources) == (
        snapshot.id,
        snapshot.id,
    )
    assert (
        tuple(
            selected.supporting_matches[0] for selected in selection.selected_resources
        )
        == retrieval.matches
    )
    assert addresses["a.py"] not in selection.resource_addresses
    assert addresses["d.py"] not in selection.resource_addresses
    assert tuple(match.knowledge for match in retrieval.matches) == (
        aggregate.analyses[1].declarations[0],
        aggregate.analyses[2].declarations[0],
    )

    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Inspect selected_function.", "user")),
        context=rendered,
    )

    assert disclosure.retrieval is retrieval
    assert [item.source_text for item in materialized.items] == [
        "def selected_function():\n    return 'B'",
        "async def selected_function():\n    return 'C'",
    ]
    assert "Repository-relative resource: b.py" in rendered.text
    assert "Repository-relative resource: c.py" in rendered.text
    assert "Repository-relative resource: a.py" not in rendered.text
    assert "Repository-relative resource: d.py" not in rendered.text
    assert rendered.text in request.prompt.content
    assert not hasattr(disclosure, "resource_selection")


def test_first_match_order_and_all_support_survive_resource_deduplication(
    tmp_path: Path,
) -> None:
    """One resource is selected once while retaining every original match."""
    first_address = RepositoryResourceAddress("a.py")
    second_address = RepositoryResourceAddress("b.py")
    snapshot = _observe(
        tmp_path,
        {
            "a.py": (
                "def selected_function():\n    return 'A1'\n\n"
                "async def selected_function():\n    return 'A2'\n"
            ),
            "b.py": "def selected_function():\n    return 'B'\n",
        },
    )
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(second_address, first_address),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("selected_function"),
    )

    selection = select_python_function_resources_from_exact_name_retrieval(retrieval)

    assert selection.resource_addresses == (second_address, first_address)
    assert selection.selected_resources[0].supporting_matches == (retrieval.matches[0],)
    assert selection.selected_resources[1].supporting_matches == retrieval.matches[1:]
    assert (
        tuple(
            match.knowledge
            for match in selection.selected_resources[1].supporting_matches
        )
        == aggregate.analyses[1].declarations
    )


def test_zero_retrieval_produces_successful_zero_resource_selection(
    tmp_path: Path,
) -> None:
    """Retrieval zero projects to selection zero without an absence claim."""
    address = RepositoryResourceAddress("module.py")
    snapshot = _observe(tmp_path, {"module.py": "def available():\n    pass\n"})
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(address,),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("missing"),
    )

    selection = select_python_function_resources_from_exact_name_retrieval(retrieval)

    assert selection.retrieval is retrieval
    assert selection.selected_resources == ()
    assert selection.resource_addresses == ()
    assert not hasattr(selection, "repository_absence")
    assert not hasattr(selection, "confidence")
    assert not hasattr(selection, "score")


def test_selection_invokes_no_upstream_or_downstream_operation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Selection reads only the supplied immutable retrieval result."""
    address = RepositoryResourceAddress("module.py")
    snapshot = _observe(
        tmp_path,
        {"module.py": "def selected_function():\n    pass\n"},
    )
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(address,),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("selected_function"),
    )

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "resource selection attempted another pipeline operation"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden)
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse", forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.derive_python_function_declarations",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.retrieval.retrieve_python_functions_by_exact_name",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.disclosure.disclose_python_function_exact_name_retrieval",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.materialization.materialize_python_function_disclosure_source",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.rendering.render_materialized_python_function_context",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.request_assembly.assemble_python_function_context_model_request",
        forbidden,
    )

    selection = select_python_function_resources_from_exact_name_retrieval(retrieval)

    assert selection.selected_resources[0].supporting_matches == retrieval.matches
