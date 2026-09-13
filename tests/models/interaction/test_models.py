# Copyright (c) 2026
"""Tests for values at the model-interaction boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelResponse,
    Prompt,
)


def test_prompt_is_an_immutable_model_input_without_conversation_identity() -> None:
    """A prompt contains only the text and role needed by current providers."""
    prompt = Prompt(content="Remember ALPHA-4821.", role="user")
    assert prompt.content == "Remember ALPHA-4821."
    assert prompt.role == "user"
    with pytest.raises(FrozenInstanceError):
        prompt.content = "other"  # type: ignore[misc]


def test_interaction_source_rejects_blank_or_padded_values() -> None:
    """Provider source identity is a small validated model-boundary value."""
    assert str(InteractionSource("llama.cpp")) == "llama.cpp"
    for value in ("", "  ", " llama.cpp", "llama.cpp "):
        with pytest.raises(ValueError, match="source"):
            InteractionSource(value)


def test_response_carries_model_output_not_a_conversation_message() -> None:
    """A response has content, source, and optional provider continuation only."""
    source = InteractionSource("llama.cpp")
    continuation = ConversationRef(source, "opaque-thread")
    response = ModelResponse(
        content="A final response",
        source=source,
        conversation=continuation,
    )
    assert response.content == "A final response"
    assert response.source is source
    assert response.conversation is continuation
    assert not hasattr(response, "id")
    with pytest.raises(FrozenInstanceError):
        response.content = "other"  # type: ignore[misc]


def test_response_rejects_continuation_from_another_source() -> None:
    """A provider continuation cannot be attributed to a different provider."""
    with pytest.raises(ValueError, match="must match"):
        ModelResponse(
            content="reply",
            source=InteractionSource("llama.cpp"),
            conversation=ConversationRef(InteractionSource("other"), "thread"),
        )


def test_conversation_ref_is_opaque_and_immutable() -> None:
    """The model boundary retains provider-owned continuation without parsing it."""
    source = InteractionSource("llama.cpp")
    reference = ConversationRef(source, "opaque-token:ALPHA/42")
    assert reference == ConversationRef(InteractionSource("llama.cpp"), reference.value)
    with pytest.raises(FrozenInstanceError):
        reference.value = "other"  # type: ignore[misc]


@pytest.mark.parametrize("value", ["", " ", " thread", "thread "])
def test_conversation_ref_rejects_blank_or_padded_values(value: str) -> None:
    """Opaque provider continuations still have minimum text validation."""
    with pytest.raises(ValueError, match="reference"):
        ConversationRef(InteractionSource("llama.cpp"), value)
