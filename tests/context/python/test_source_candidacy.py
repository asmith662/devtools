# Copyright (c) 2026
"""Tests for Python-source address candidacy from repository discovery."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import (
    PythonFunctionExactNameQuery,
    PythonSourceAddressCandidateSelection,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositoryResourceDiscovery,
    analyze_python_function_declaration_resources,
    assemble_python_function_context_model_request,
    disclose_python_function_exact_name_retrieval,
    discover_repository_resource_addresses,
    materialize_python_function_disclosure_source,
    observe_repository_resources,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
    select_python_function_analysis_candidates,
    select_python_function_resources_from_exact_name_retrieval,
    select_python_source_address_candidates,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"
_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024
_DISCOVERED_COUNT = 7
_PYTHON_ADDRESS_CANDIDATE_COUNT = 4
_ANALYSIS_CANDIDATE_COUNT = 3


def _repository() -> Repository:
    """Return one stable logical repository for deterministic fixtures."""
    return Repository(RepositoryId.parse(_REPOSITORY_ID))


def _discover(tmp_path: Path) -> RepositoryResourceDiscovery:
    """Discover all regular-file fixture addresses under one explicit root."""
    return discover_repository_resource_addresses(
        repository=_repository(),
        root=ResolvedPath(tmp_path),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
    )


def test_exact_dot_py_candidacy_preserves_discovery_order_and_address_values(
    tmp_path: Path,
) -> None:
    """Only exact lowercase suffix matches become address candidates."""
    for name in (
        "module.py",
        "upper.PY",
        "stub.pyi",
        "window.pyw",
        "script",
        "archive.py.zip",
    ):
        (tmp_path / name).write_text("content", encoding="utf-8")
    discovery = _discover(tmp_path)

    result = select_python_source_address_candidates(discovery)

    assert isinstance(result, PythonSourceAddressCandidateSelection)
    assert result.discovery is discovery
    assert result.addresses == (RepositoryResourceAddress("module.py"),)
    assert result.candidates[0].address is discovery.addresses[1]
    evidence = result.candidates[0].evidence
    assert evidence.matched_suffix == ".py"
    assert evidence.MECHANISM == "exact-case-sensitive-dot-py-address-suffix-v1"
    assert evidence.NATIVE_OBSERVATION == "repository-address-ends-with-dot-py"
    assert not hasattr(evidence, "score")
    assert not hasattr(evidence, "confidence")


def test_discovery_candidates_compose_through_the_function_context_pipeline(
    tmp_path: Path,
) -> None:
    """Seven discovered files narrow deterministically to one disclosed resource."""
    sources = {
        "declaration.py": "def selected_function():\n    return 'TARGET'\n",
        "call.py": "value = selected_function()\n",
        "method.py": (
            "class Holder:\n    def selected_function(self):\n        return 'METHOD'\n"
        ),
        "unrelated.py": "def helper():\n    return 'OTHER'\n",
        "notes.txt": "selected_function\n",
        "README.md": "# Fixture\n",
    }
    for name, content in sources.items():
        (tmp_path / name).write_text(content, encoding="utf-8", newline="")
    (tmp_path / "binary.dat").write_bytes(b"\xff\xfe\x00")

    discovery = _discover(tmp_path)
    python_sources = select_python_source_address_candidates(discovery)
    snapshot = observe_repository_resources(
        repository=_repository(),
        root=ResolvedPath(tmp_path),
        addresses=python_sources.addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )
    query = PythonFunctionExactNameQuery("selected_function")
    analysis_candidates = select_python_function_analysis_candidates(
        snapshot,
        query=query,
        resource_addresses=python_sources.addresses,
    )
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=analysis_candidates.candidate_resource_addresses,
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=query,
    )
    selected_resources = select_python_function_resources_from_exact_name_retrieval(
        retrieval,
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

    assert len(discovery.addresses) == _DISCOVERED_COUNT
    assert len(python_sources.addresses) == _PYTHON_ADDRESS_CANDIDATE_COUNT
    assert len(snapshot.resources) == _PYTHON_ADDRESS_CANDIDATE_COUNT
    assert analysis_candidates.candidate_resource_addresses == (
        RepositoryResourceAddress("call.py"),
        RepositoryResourceAddress("declaration.py"),
        RepositoryResourceAddress("method.py"),
    )
    assert len(analysis_candidates.candidates) == _ANALYSIS_CANDIDATE_COUNT
    assert len(aggregate.analyses) == _ANALYSIS_CANDIDATE_COUNT
    assert len(retrieval.matches) == 1
    assert selected_resources.resource_addresses == (
        RepositoryResourceAddress("declaration.py"),
    )
    assert len(disclosure.items) == 1
    assert len(materialized.items) == 1
    assert materialized.items[0].source_text == (
        "def selected_function():\n    return 'TARGET'"
    )
    assert "Repository-relative resource: declaration.py" in rendered.text
    assert "Repository-relative resource: call.py" not in rendered.text
    assert "Repository-relative resource: method.py" not in rendered.text
    assert request.prompt.content.count(rendered.text) == 1


def test_candidate_zero_is_successful_and_bounded_to_discovered_addresses(
    tmp_path: Path,
) -> None:
    """No suffix match yields bounded candidate zero, not repository absence."""
    (tmp_path / "README.md").write_text("# No candidates\n", encoding="utf-8")
    (tmp_path / "module.PY").write_text("value = 1\n", encoding="utf-8")
    discovery = _discover(tmp_path)

    result = select_python_source_address_candidates(discovery)

    assert result.discovery is discovery
    assert result.candidates == ()
    assert result.addresses == ()
    assert not hasattr(result, "repository_absence")
    assert not hasattr(result, "content_identity")


def test_candidate_projection_performs_no_filesystem_or_pipeline_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Address candidacy consumes only the supplied completed discovery value."""
    (tmp_path / "module.py").write_text("value = 1\n", encoding="utf-8")
    discovery = _discover(tmp_path)

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "address candidacy attempted filesystem or downstream work"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.discovery.os.scandir", forbidden)
    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden)
    monkeypatch.setattr(
        "devtools.context.repository.observation.observe_repository_resources",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.candidates.tokenize.generate_tokens",
        forbidden,
    )
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

    result = select_python_source_address_candidates(discovery)

    assert result.addresses == (discovery.addresses[0],)
    assert result.addresses[0] is discovery.addresses[0]
