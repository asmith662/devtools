# Copyright (c) 2026
"""Tests for bounded Python function Context model-request assembly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.agents.conversation import Conversation
from devtools.context import (
    PythonFunctionExactNameQuery,
    RenderedPythonFunctionContext,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    assemble_python_function_context_model_request,
    derive_python_function_declarations,
    disclose_python_function_exact_name_retrieval,
    materialize_python_function_disclosure_source,
    observe_repository_resource,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelRequest,
    ModelSettings,
    ModelToolDefinition,
    Prompt,
    ProviderRequestSettings,
)

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _rendered_context(
    tmp_path: Path,
    content: str,
    *,
    name: str,
) -> RenderedPythonFunctionContext:
    """Exercise the real deterministic pipeline through Context rendering."""
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
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    return render_materialized_python_function_context(materialized)


def test_assembles_real_context_after_distinct_unchanged_task(
    tmp_path: Path,
) -> None:
    """Assembly preserves task, Context, role, and every other request semantic."""
    rendered = _rendered_context(
        tmp_path,
        'def target():\r\n    return "caf\u00e9"\r\n',
        name="target",
    )
    task_text = "Fix target without changing behavior.\r\nKeep its public name."
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider_settings = ProviderRequestSettings("test-model")
    tools = (
        ModelToolDefinition(
            name="inspect",
            description="Inspect one value.",
            input_schema_json='{"type":"object"}',
        ),
    )
    task_request = ModelRequest(
        prompt=Prompt(content=task_text, role="user"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider_settings,
        tools=tools,
    )

    request = assemble_python_function_context_model_request(
        task_request=task_request,
        context=rendered,
    )

    assert isinstance(request, ModelRequest)
    assert request is not task_request
    assert request.prompt.role == task_request.prompt.role
    assert request.settings is settings
    assert request.conversation is continuation
    assert request.provider_settings is provider_settings
    assert request.tools is tools
    assert task_request.prompt.content == task_text
    assert task_text in request.prompt.content
    assert rendered.text in request.prompt.content
    assert request.prompt.content.index(task_text) < request.prompt.content.index(
        rendered.text,
    )
    assert (
        f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n"
        in request.prompt.content
    )
    assert (
        "Supporting repository Context UTF-8 byte length: "
        f"{len(rendered.text.encode('utf-8'))}\n"
    ) in request.prompt.content
    assert request.prompt.content.count('def target():\r\n    return "caf\u00e9"') == 1
    assert (
        assemble_python_function_context_model_request(
            task_request=task_request,
            context=rendered,
        )
        == request
    )
    assert not hasattr(request, "rendered_context")


def test_assembles_zero_context_without_repository_absence_claim(
    tmp_path: Path,
) -> None:
    """A bounded zero remains the unchanged supporting Context representation."""
    rendered = _rendered_context(
        tmp_path,
        "def available():\n    pass\n",
        name="missing",
    )

    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Investigate missing.", "user")),
        context=rendered,
    )

    assert rendered.text in request.prompt.content
    assert "Selected declarations: 0\n" in request.prompt.content
    assert "supplied exact-name retrieval result" in request.prompt.content
    lowered = request.prompt.content.lower()
    assert "does not exist" not in lowered
    assert "repository contains no" not in lowered
    assert "failed" not in lowered


def test_assembly_invokes_no_upstream_execution_or_conversation_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Assembly is a pure request-value construction over completed Context."""
    rendered = _rendered_context(
        tmp_path,
        "def target():\n    pass\n",
        name="target",
    )
    conversation = Conversation.new()

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "request assembly attempted upstream or execution work"
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
    monkeypatch.setattr("devtools.execution.Runtime.send", forbidden)
    monkeypatch.setattr("devtools.agents.conversation.Conversation.add", forbidden)

    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Complete the task.", "user")),
        context=rendered,
    )

    assert isinstance(request, ModelRequest)
    assert rendered.text in request.prompt.content
    assert tuple(conversation.history) == ()
    assert not hasattr(request, "response")
    assert not hasattr(request, "interaction")
    assert not hasattr(request, "runtime")
