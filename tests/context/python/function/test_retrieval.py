# Copyright (c) 2026
"""Tests for exact-name retrieval over Python declaration knowledge."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionDeclarationAnalysis,
    PythonFunctionDeclarationKind,
    PythonFunctionExactNameQuery,
    PythonFunctionExactNameRelevanceEvidence,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    derive_python_function_declarations,
    observe_repository_resource,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _declarations(
    tmp_path: Path,
    content: str,
) -> PythonFunctionDeclarationAnalysis:
    """Establish declaration knowledge through the production boundaries."""
    source = tmp_path / "module.py"
    source.write_text(content, encoding="utf-8", newline="")
    snapshot = observe_repository_resource(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        address=RepositoryResourceAddress("module.py"),
        maximum_resource_bytes=16 * 1024 * 1024,
    )
    return derive_python_function_declarations(snapshot)


def test_exact_name_retrieval_preserves_knowledge_evidence_and_order(
    tmp_path: Path,
) -> None:
    """Exact matches remain distinct and retain their established knowledge."""
    analysis = _declarations(
        tmp_path,
        """def duplicate():
    pass

def other():
    pass

async def duplicate():
    pass

def duplicate():
    pass
""",
    )
    query = PythonFunctionExactNameQuery("duplicate")

    result = retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=query,
    )

    expected_knowledge = (
        analysis.declarations[0],
        analysis.declarations[2],
        analysis.declarations[3],
    )
    assert result.query is query
    assert len(result.matches) == len(expected_knowledge)
    assert tuple(match.knowledge for match in result.matches) == expected_knowledge
    assert all(
        match.knowledge is expected
        for match, expected in zip(result.matches, expected_knowledge, strict=True)
    )
    assert [match.knowledge.declaration_kind for match in result.matches] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
        PythonFunctionDeclarationKind.SYNCHRONOUS,
    ]
    assert len({match.knowledge.identity for match in result.matches}) == len(
        expected_knowledge,
    )
    assert all(
        isinstance(match, PythonFunctionExactNameRelevanceEvidence)
        for match in result.matches
    )
    evidence = result.matches[0]
    assert evidence.query is query
    assert evidence.MECHANISM == "python-function-declared-name-exact-equality-v1"
    assert evidence.NATIVE_OBSERVATION == "exact-declared-name-match"
    assert not hasattr(evidence, "confidence")
    assert not hasattr(evidence, "score")
    assert not hasattr(evidence, "ranking_influence")


def test_nonmatching_names_are_excluded_and_input_order_is_preserved(
    tmp_path: Path,
) -> None:
    """The operation performs literal equality filtering without ranking."""
    analysis = _declarations(
        tmp_path,
        """def target():
    pass

def target_extra():
    pass

def TARGET():
    pass

def target():
    pass
""",
    )
    supplied = tuple(reversed(analysis.declarations))

    result = retrieve_python_functions_by_exact_name(
        declarations=supplied,
        query=PythonFunctionExactNameQuery("target"),
    )

    assert tuple(match.knowledge for match in result.matches) == (
        supplied[0],
        supplied[3],
    )
    assert all(match.knowledge.declared_name == "target" for match in result.matches)


def test_successful_zero_is_distinct_from_invalid_empty_query(tmp_path: Path) -> None:
    """No supplied match succeeds, while an empty retrieval purpose is invalid."""
    analysis = _declarations(tmp_path, "def available():\n    pass\n")
    query = PythonFunctionExactNameQuery("missing")

    result = retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=query,
    )

    assert result.query is query
    assert result.matches == ()
    with pytest.raises(ValueError, match="cannot be empty"):
        PythonFunctionExactNameQuery("")


def test_retrieval_does_not_read_or_parse_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Retrieval consumes established knowledge after acquisition and parsing."""
    analysis = _declarations(tmp_path, "def target():\n    pass\n")

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "retrieval attempted repository acquisition or Python parsing"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden)
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse", forbidden,
    )

    result = retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=PythonFunctionExactNameQuery("target"),
    )

    assert result.matches[0].knowledge is analysis.declarations[0]
