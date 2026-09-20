# Copyright (c) 2026
"""Tests for bounded Context disclosure of exact-name function retrieval."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import (
    PythonFunctionDeclarationAnalysis,
    PythonFunctionDeclarationKind,
    PythonFunctionExactNameQuery,
    PythonFunctionExactNameRetrievalResult,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    derive_python_function_declarations,
    disclose_python_function_exact_name_retrieval,
    observe_repository_resource,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _analysis(tmp_path: Path, content: str) -> PythonFunctionDeclarationAnalysis:
    """Establish declaration knowledge through the production boundaries."""
    source = tmp_path / "module.py"
    source.write_text(content, encoding="utf-8", newline="")
    snapshot = observe_repository_resource(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        address=RepositoryResourceAddress("module.py"),
    )
    return derive_python_function_declarations(snapshot)


def _retrieve(
    analysis: PythonFunctionDeclarationAnalysis,
    name: str,
) -> PythonFunctionExactNameRetrievalResult:
    """Retrieve established declarations by exact name."""
    return retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=PythonFunctionExactNameQuery(name),
    )


def test_disclosure_selects_and_projects_all_matches_without_strengthening(
    tmp_path: Path,
) -> None:
    """Selection and representation preserve duplicate established knowledge."""
    analysis = _analysis(
        tmp_path,
        """def duplicate():
    pass

def other():
    pass

async def duplicate():
    pass
""",
    )
    retrieval = _retrieve(analysis, "duplicate")

    disclosure = disclose_python_function_exact_name_retrieval(retrieval)

    assert disclosure.retrieval is retrieval
    assert disclosure.selected_matches is retrieval.matches
    assert len(disclosure.items) == len(retrieval.matches)
    assert [item.declared_name for item in disclosure.items] == [
        "duplicate",
        "duplicate",
    ]
    assert [item.declaration_kind for item in disclosure.items] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
    ]
    assert [
        item.source_occurrence.source_range.start_line for item in disclosure.items
    ] == [1, 7]
    assert all(
        str(item.source_occurrence.resource_address) == "module.py"
        for item in disclosure.items
    )
    for item, match in zip(disclosure.items, retrieval.matches, strict=True):
        assert item.selected_match is match
        assert item.declared_name == match.knowledge.declared_name
        assert item.declaration_kind is match.knowledge.declaration_kind
        assert item.source_occurrence is match.knowledge.support
        assert item.proposition == match.knowledge.PROPOSITION
        assert not hasattr(item, "source_text")
        assert not hasattr(item, "runtime_exists")
        assert not hasattr(item, "callable")
        assert not hasattr(item, "confidence")
        assert not hasattr(item, "score")
    assert disclosure.SELECTION == "all-exact-name-matches-in-retrieval-order-v1"
    assert disclosure.items[0].REPRESENTATION == (
        "python-function-declaration-knowledge-projection-v1"
    )
    assert disclosure.identity == (
        disclose_python_function_exact_name_retrieval(retrieval).identity
    )
    assert not hasattr(disclosure, "model_request")
    assert not hasattr(disclosure, "ranking")


def test_successful_retrieval_zero_becomes_successful_zero_item_disclosure(
    tmp_path: Path,
) -> None:
    """Bounded zero remains a realized disclosure without an absence claim."""
    analysis = _analysis(tmp_path, "def available():\n    pass\n")
    retrieval = _retrieve(analysis, "missing")

    disclosure = disclose_python_function_exact_name_retrieval(retrieval)

    assert disclosure.retrieval is retrieval
    assert disclosure.selected_matches == ()
    assert disclosure.items == ()
    assert disclosure.identity
    assert not hasattr(disclosure, "repository_absence")
    assert not hasattr(disclosure, "failure")


def test_disclosure_does_not_acquire_parse_or_derive(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Context disclosure consumes only the completed retrieval result."""
    analysis = _analysis(tmp_path, "def target():\n    pass\n")
    retrieval = _retrieve(analysis, "target")

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "disclosure attempted acquisition, parsing, or derivation"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden)
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse", forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.derive_python_function_declarations",
        forbidden,
    )

    disclosure = disclose_python_function_exact_name_retrieval(retrieval)

    assert disclosure.items[0].selected_match is retrieval.matches[0]
