# Copyright (c) 2026
"""Tests for pre-analysis Python function resource candidate selection."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionAnalysisCandidateSelection,
    PythonFunctionCandidateTokenizationError,
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
    select_python_function_analysis_candidates,
    select_python_function_resources_from_exact_name_retrieval,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"
_EXPECTED_ELIGIBLE_RESOURCE_COUNT = 6
_EXPECTED_CANDIDATE_RESOURCE_COUNT = 3


def _observe(
    tmp_path: Path,
    resources: Mapping[str, str],
) -> RepositorySnapshot:
    """Observe an explicit source collection for candidate-selection tests."""
    addresses = tuple(RepositoryResourceAddress(value) for value in resources)
    for value, content in resources.items():
        source = tmp_path.joinpath(*value.split("/"))
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(content, encoding="utf-8", newline="")
    return observe_repository_resources(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        addresses=addresses,
    )


def test_name_token_candidates_feed_verified_context_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cheap candidates narrow six eligible resources to one verified Context item."""
    source_by_address = {
        "declaration.py": "def selected_function():\n    return 'TARGET'\n",
        "call.py": "value = selected_function()\n",
        "string_only.py": "value = 'selected_function'\n",
        "comment_only.py": "# selected_function\nVALUE = 1\n",
        "method.py": (
            "class Holder:\n"
            "    def selected_function(self):\n"
            "        return 'METHOD'\n"
        ),
        "unrelated.py": "def helper():\n    return 'OTHER'\n",
    }
    snapshot = _observe(tmp_path, source_by_address)
    eligible_addresses = tuple(
        RepositoryResourceAddress(value) for value in source_by_address
    )
    query = PythonFunctionExactNameQuery("selected_function")

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "post-observation pipeline attempted filesystem acquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.read", forbidden_read)
    candidates = select_python_function_analysis_candidates(
        snapshot,
        query=query,
        resource_addresses=eligible_addresses,
    )

    assert isinstance(candidates, PythonFunctionAnalysisCandidateSelection)
    assert candidates.snapshot_id == snapshot.id
    assert candidates.query is query
    assert candidates.eligible_resource_addresses == eligible_addresses
    assert candidates.candidate_resource_addresses == (
        RepositoryResourceAddress("declaration.py"),
        RepositoryResourceAddress("call.py"),
        RepositoryResourceAddress("method.py"),
    )
    assert all(
        candidate.resource is snapshot.resource_at(candidate.resource.address)
        for candidate in candidates.candidates
    )

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=candidates.candidate_resource_addresses,
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=query,
    )
    verified_resources = (
        select_python_function_resources_from_exact_name_retrieval(retrieval)
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

    assert len(snapshot.resources) == _EXPECTED_ELIGIBLE_RESOURCE_COUNT
    assert len(candidates.eligible_resources) == _EXPECTED_ELIGIBLE_RESOURCE_COUNT
    assert len(candidates.candidates) == _EXPECTED_CANDIDATE_RESOURCE_COUNT
    assert len(aggregate.analyses) == _EXPECTED_CANDIDATE_RESOURCE_COUNT
    assert len(retrieval.matches) == 1
    assert verified_resources.resource_addresses == (
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
    assert rendered.text in request.prompt.content


def test_duplicate_name_tokens_select_each_resource_once_in_eligible_order(
    tmp_path: Path,
) -> None:
    """All token observations survive without duplicating candidate resources."""
    first_address = RepositoryResourceAddress("a.py")
    second_address = RepositoryResourceAddress("b.py")
    snapshot = _observe(
        tmp_path,
        {
            "a.py": (
                "selected_function = 1\n"
                "value = selected_function\n"
            ),
            "b.py": "selected_function()\n",
        },
    )
    query = PythonFunctionExactNameQuery("selected_function")

    result = select_python_function_analysis_candidates(
        snapshot,
        query=query,
        resource_addresses=(second_address, first_address),
    )

    expected_candidate_addresses = (second_address, first_address)
    assert result.candidate_resource_addresses == expected_candidate_addresses
    assert len(result.candidates) == len(expected_candidate_addresses)
    assert len(result.candidates[0].supporting_matches) == 1
    assert tuple(
        match.token_string
        for match in result.candidates[1].supporting_matches
    ) == (query.declared_name, query.declared_name)
    assert [
        match.token_index for match in result.candidates[1].supporting_matches
    ] == sorted(
        match.token_index for match in result.candidates[1].supporting_matches
    )
    assert all(
        match.token_string == query.declared_name
        for candidate in result.candidates
        for match in candidate.supporting_matches
    )
    evidence = result.candidates[0].supporting_matches[0]
    assert evidence.MECHANISM == "stdlib-generate-tokens-name-exact-equality-v1"
    assert evidence.NATIVE_OBSERVATION == "exact-python-name-token-match"
    assert not hasattr(evidence, "score")
    assert not hasattr(evidence, "confidence")


def test_candidate_zero_is_successful_and_bounded_to_eligible_resources(
    tmp_path: Path,
) -> None:
    """No exact NAME token yields bounded candidate zero, not repository absence."""
    address = RepositoryResourceAddress("module.py")
    snapshot = _observe(
        tmp_path,
        {"module.py": "value = 'selected_function'\n# selected_function\n"},
    )

    result = select_python_function_analysis_candidates(
        snapshot,
        query=PythonFunctionExactNameQuery("selected_function"),
        resource_addresses=(address,),
    )

    assert result.eligible_resource_addresses == (address,)
    assert result.candidates == ()
    assert result.candidate_resource_addresses == ()
    assert not hasattr(result, "repository_absence")
    assert not hasattr(result, "declaration_coverage")


def test_invalid_eligible_resources_fail_before_tokenization(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty, duplicate, and absent eligibility publish no candidate result."""
    address = RepositoryResourceAddress("module.py")
    snapshot = _observe(tmp_path, {"module.py": "selected_function()\n"})

    def forbidden_tokenization(*_args: object, **_kwargs: object) -> None:
        msg = "invalid eligibility attempted tokenization"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.python_function_candidates.tokenize.generate_tokens",
        forbidden_tokenization,
    )
    query = PythonFunctionExactNameQuery("selected_function")
    with pytest.raises(ValueError, match="at least one"):
        select_python_function_analysis_candidates(
            snapshot,
            query=query,
            resource_addresses=(),
        )
    with pytest.raises(ValueError, match="distinct"):
        select_python_function_analysis_candidates(
            snapshot,
            query=query,
            resource_addresses=(address, address),
        )
    with pytest.raises(ValueError, match="does not contain resource address"):
        select_python_function_analysis_candidates(
            snapshot,
            query=query,
            resource_addresses=(
                address,
                RepositoryResourceAddress("absent.py"),
            ),
        )


def test_tokenization_failure_is_distinct_from_candidate_zero(tmp_path: Path) -> None:
    """A required resource tokenizer failure publishes no successful selection."""
    address = RepositoryResourceAddress("broken.py")
    snapshot = _observe(tmp_path, {"broken.py": "value = (\n"})

    with pytest.raises(PythonFunctionCandidateTokenizationError) as captured:
        select_python_function_analysis_candidates(
            snapshot,
            query=PythonFunctionExactNameQuery("value"),
            resource_addresses=(address,),
        )

    error = captured.value
    assert error.snapshot_id == snapshot.id
    assert error.resource_address == address
    assert "multi-line statement" in error.tokenizer_message
    assert "broken.py" in str(error)
    assert not hasattr(error, "candidates")


def test_candidate_selection_invokes_no_other_pipeline_operation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The selector consumes retained source without acquisition or AST analysis."""
    address = RepositoryResourceAddress("module.py")
    snapshot = _observe(tmp_path, {"module.py": "selected_function()\n"})

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "candidate selection attempted another pipeline operation"
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
    monkeypatch.setattr(
        "devtools.context.python_function_disclosure.disclose_python_function_exact_name_retrieval",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python_function_materialization.materialize_python_function_disclosure_source",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python_function_rendering.render_materialized_python_function_context",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python_function_request_assembly.assemble_python_function_context_model_request",
        forbidden,
    )

    result = select_python_function_analysis_candidates(
        snapshot,
        query=PythonFunctionExactNameQuery("selected_function"),
        resource_addresses=(address,),
    )

    assert result.candidate_resource_addresses == (address,)
