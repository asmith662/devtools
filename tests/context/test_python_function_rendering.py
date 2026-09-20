# Copyright (c) 2026
"""Tests for deterministic rendering of materialized Python function Context."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.context import (
    MaterializedPythonFunctionContext,
    PythonFunctionExactNameQuery,
    RenderedPythonFunctionContext,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    derive_python_function_declarations,
    disclose_python_function_exact_name_retrieval,
    materialize_python_function_disclosure_source,
    observe_repository_resource,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _materialized_context(
    tmp_path: Path,
    content: str,
    *,
    name: str,
) -> MaterializedPythonFunctionContext:
    """Exercise every implemented layer before model-facing rendering."""
    source = tmp_path / "module.py"
    source.write_bytes(content.encode("utf-8"))
    snapshot = observe_repository_resource(
        repository=Repository(RepositoryId.parse(_REPOSITORY_ID)),
        root=ResolvedPath(tmp_path),
        address=RepositoryResourceAddress("module.py"),
    )
    analysis = derive_python_function_declarations(snapshot)
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=PythonFunctionExactNameQuery(name),
    )
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    return materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )


def test_renders_ordered_duplicate_sync_and_async_context_exactly(
    tmp_path: Path,
) -> None:
    """The full path renders metadata and unchanged CRLF/non-ASCII source."""
    first_source = (
        'def duplicate():\r\n    return "caf\u00e9 --- exact source ends ---"'
    )
    second_source = 'async def duplicate():\r\n    return "na\u00efve"'
    context = _materialized_context(
        tmp_path,
        f"# pr\u00e9face\r\n{first_source}\r\n\r\n{second_source}\r\n",
        name="duplicate",
    )

    rendered = render_materialized_python_function_context(context)
    expected_match_count = len(context.items)

    assert isinstance(rendered, RenderedPythonFunctionContext)
    assert rendered.materialized_context is context
    assert rendered.FORMAT == "python-function-context-text-v1"
    assert "Exact declared-name purpose: duplicate\n" in rendered.text
    assert "Selected declarations: 2\n" in rendered.text
    assert rendered.text.count("Declared name: duplicate\n") == expected_match_count
    assert "Declaration kind: function-def\n" in rendered.text
    assert "Declaration kind: async-function-def\n" in rendered.text
    assert (
        rendered.text.count("Repository-relative resource: module.py\n")
        == expected_match_count
    )
    assert "Source location: 2:0-3:" in rendered.text
    assert "Source location: 5:0-6:" in rendered.text
    assert context.items[0].disclosure_item.proposition in rendered.text
    assert first_source in rendered.text
    assert second_source in rendered.text
    assert first_source.replace("\r\n", "\n") not in rendered.text
    assert second_source.replace("\r\n", "\n") not in rendered.text
    assert rendered.text.index(first_source) < rendered.text.index(second_source)
    for item in context.items:
        expected_length = len(item.source_text.encode("utf-8"))
        assert f"Exact source UTF-8 byte length: {expected_length}\n" in rendered.text
    assert render_materialized_python_function_context(context) == rendered


def test_zero_context_renders_bounded_success_without_absence_claim(
    tmp_path: Path,
) -> None:
    """Successful zero stays scoped to the supplied retrieval result."""
    context = _materialized_context(
        tmp_path,
        "def available():\n    pass\n",
        name="missing",
    )

    rendered = render_materialized_python_function_context(context)

    assert rendered.materialized_context is context
    assert rendered.text == (
        "Python function Context\n"
        "Exact declared-name purpose: missing\n"
        "Selection: all exact-name matches in retrieval order\n"
        "Selected declarations: 0\n"
        "Bounded meaning: each item is established only as a direct module-body "
        "Python source occurrence that syntactically declares a snapshot-local "
        "function subject.\n"
        "No declarations were selected from the supplied exact-name retrieval "
        "result.\n"
    )
    lowered = rendered.text.lower()
    assert "does not exist" not in lowered
    assert "repository contains no" not in lowered
    assert "failed" not in lowered


def test_rendering_consumes_only_materialized_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rendering invokes no acquisition, analysis, selection, or materialization."""
    context = _materialized_context(
        tmp_path,
        "def target():\n    return 1\n",
        name="target",
    )

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "rendering attempted an upstream operation"
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

    rendered = render_materialized_python_function_context(context)

    assert rendered.materialized_context is context
    assert context.items[0].source_text in rendered.text
    lowered = rendered.text.lower()
    for excluded in (
        "confidence",
        "score",
        "ranking",
        "runtime binding",
        "callable",
        "importable",
        "unique function",
    ):
        assert excluded not in lowered
    assert not hasattr(rendered, "model_request")
    assert not hasattr(rendered, "messages")
    assert not hasattr(rendered, "agent")
    assert not hasattr(rendered, "runtime")
