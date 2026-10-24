# Copyright (c) 2026
# ruff: noqa: COM812 -- explicit malformed invocation fixtures
"""Native invocation message admission, provider serialization and capture."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.context.planning.rendering import (
    assemble_context_disclosure_model_request,
)
from devtools.context.python.function.qualified_reference import (
    assemble_python_qualified_reference_model_request,
)
from devtools.context.python.function.request_assembly import (
    assemble_python_function_context_model_request,
)
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.models.interaction.providers import llama_cpp

if TYPE_CHECKING:
    from collections.abc import Callable

CALL = ModelToolCall("read_source", '{"path":"demo.py"}', "native-1")


def native_prompt() -> Prompt:
    """Return one exact correlated native exchange, including assistant content."""
    return Prompt(
        "",
        "messages",
        (
            PromptMessage("user", "Inspect the source"),
            PromptMessage("assistant", "I will inspect it.", (CALL,)),
            PromptMessage("tool", "captured source result", tool_call_id="native-1"),
        ),
    )


@pytest.mark.parametrize(
    "values",
    [
        {"role": "unknown", "content": "x"},
        {"role": "user", "content": 1},
        {"role": "user", "content": "x", "tool_calls": (CALL,)},
        {"role": "user", "content": "x", "tool_calls": []},
        {"role": "assistant", "content": "x", "tool_calls": ("bad",)},
        {"role": "tool", "content": "x"},
        {"role": "tool", "content": "x", "tool_call_id": " "},
        {"role": "tool", "content": "x", "tool_call_id": 1},
        {"role": "user", "content": "x", "tool_call_id": "unexpected"},
    ],
)
def test_malformed_message_refuses(values: dict[str, Any]) -> None:
    """Roles, argument representation and result IDs cannot be inferred."""
    with pytest.raises((TypeError, ValueError)):
        PromptMessage(**values)


@pytest.mark.parametrize(
    ("content", "role", "messages"),
    [
        ("", "messages", ()),
        ("x", "messages", (PromptMessage("user", "x"),)),
        ("", "user", (PromptMessage("user", "x"),)),
        ("", "messages", []),
        ("", "messages", ("bad",)),
        ("", "messages", (PromptMessage("tool", "x", tool_call_id="absent"),)),
        ("", "messages", (PromptMessage("assistant", "", (CALL,)),)),
        (
            "",
            "messages",
            (PromptMessage("assistant", "", (CALL,)), PromptMessage("user", "x")),
        ),
        ("", "messages", (PromptMessage("assistant", "", (CALL, CALL)),)),
        (
            "",
            "messages",
            (PromptMessage("assistant", "", (ModelToolCall("read_source", "{}"),)),),
        ),
    ],
)
def test_incomplete_or_dual_prompt_refuses(
    content: str, role: str, messages: object
) -> None:
    """The adapter never receives orphaned calls/results or two input forms."""
    with pytest.raises((TypeError, ValueError)):
        Prompt(content, role, cast("tuple[PromptMessage, ...]", messages))


def test_resolved_provider_id_can_recur_in_a_later_exchange() -> None:
    """Opaque provider IDs are scoped to each completed exchange, not invented."""
    prompt = native_prompt()
    messages = (*prompt.messages, *prompt.messages[1:])
    assert Prompt("", "messages", messages).messages == messages


def test_native_provider_serializes_messages_without_flattening(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise send() and normalized response using the real provider serializer."""
    payloads = []

    async def post(_endpoint: object, payload: dict[str, object]) -> dict[str, object]:
        payloads.append(payload)
        return {
            "choices": [
                {
                    "message": {"role": "assistant", "content": "Done"},
                    "finish_reason": "stop",
                }
            ]
        }

    monkeypatch.setattr(llama_cpp, "_post_chat_completion", post)
    interaction = llama_cpp.LlamaCppInteraction(
        endpoint="http://127.0.0.1:8080",
        model="fixture",
        source=InteractionSource("fixture"),
    )
    response = asyncio.run(interaction.send(ModelRequest(native_prompt())))
    assert response.content == "Done"
    messages = payloads[0]["messages"]
    assert isinstance(messages, list)
    assert [m["role"] for m in messages] == ["user", "assistant", "tool"]
    assert messages[1]["content"] == "I will inspect it."
    assert messages[1]["tool_calls"][0]["id"] == messages[2]["tool_call_id"]
    assert json.loads(messages[1]["tool_calls"][0]["function"]["arguments"]) == {
        "path": "demo.py"
    }


@pytest.mark.parametrize(
    "assemble",
    [
        assemble_context_disclosure_model_request,
        assemble_python_function_context_model_request,
        assemble_python_qualified_reference_model_request,
    ],
)
def test_text_assemblers_do_not_silently_discard_structured_history(
    assemble: Callable[..., ModelRequest],
) -> None:
    """Unsupported text-only assembly fails explicitly before touching Context."""
    with pytest.raises(ValueError, match="structured message"):
        assemble(task_request=ModelRequest(native_prompt()), context=None)
