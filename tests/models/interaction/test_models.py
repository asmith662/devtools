# Copyright (c) 2026
"""Tests for values at the model-interaction boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelResponse,
    ModelTermination,
    ModelUsage,
    Prompt,
    validate_maximum_output_tokens,
    validate_thinking_enabled,
)

_INPUT_TOKENS = 8
_OUTPUT_TOKENS = 4
_PROVIDER_TOTAL_TOKENS = 99


@pytest.mark.parametrize("value", [1, 8])
def test_maximum_output_tokens_accepts_positive_integers(value: int) -> None:
    """A request-side output limit is optional but positive when supplied."""
    validate_maximum_output_tokens(value)


@pytest.mark.parametrize("value", [0, -1, True, False, "8", 8.0])
def test_maximum_output_tokens_rejects_nonpositive_or_noninteger_values(
    value: object,
) -> None:
    """The provider-neutral request constraint rejects invalid values locally."""
    with pytest.raises(ValueError, match="positive integer"):
        validate_maximum_output_tokens(value)  # type: ignore[arg-type]


def test_maximum_output_tokens_allows_absence() -> None:
    """Absent output limits preserve an unbounded provider request."""
    validate_maximum_output_tokens(None)


@pytest.mark.parametrize("value", [None, True, False])
def test_thinking_enabled_accepts_strict_optional_boolean(
    *, value: bool | None,
) -> None:
    """The thinking request control accepts only its typed values."""
    validate_thinking_enabled(value)


@pytest.mark.parametrize("value", [0, 1, "true", "false", 1.0, [], {}])
def test_thinking_enabled_rejects_non_boolean_values(*, value: object) -> None:
    """Integer and truthy values cannot bypass the request boundary."""
    with pytest.raises(TypeError, match="boolean"):
        validate_thinking_enabled(value)


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
    """A response has content, source, and optional provider facts."""
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
    assert response.usage is None
    assert response.termination is None
    assert response.reasoning_content is None
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


def test_model_usage_retains_reported_counts_without_deriving_a_total() -> None:
    """Usage keeps provider totals even when they differ from component counts."""
    usage = ModelUsage(
        input_tokens=_INPUT_TOKENS,
        output_tokens=_OUTPUT_TOKENS,
        total_tokens=_PROVIDER_TOTAL_TOKENS,
    )
    response = ModelResponse(
        content="reply",
        source=InteractionSource("llama.cpp"),
        usage=usage,
    )

    assert response.usage == usage
    assert response.usage.total_tokens == _PROVIDER_TOTAL_TOKENS


def test_model_response_retains_termination_separately_from_usage() -> None:
    """Termination remains an optional response fact independent of token accounting."""
    response = ModelResponse(
        content="reply",
        source=InteractionSource("llama.cpp"),
        usage=ModelUsage(output_tokens=_OUTPUT_TOKENS),
        termination=ModelTermination.OUTPUT_LIMIT,
    )

    assert response.termination is ModelTermination.OUTPUT_LIMIT
    assert response.usage == ModelUsage(output_tokens=_OUTPUT_TOKENS)


def test_model_response_retains_reasoning_separately_from_visible_content() -> None:
    """A provider's non-visible reasoning is not substituted for assistant content."""
    response = ModelResponse(
        content="",
        source=InteractionSource("llama.cpp"),
        reasoning_content="Thinking through the requested answer.",
    )

    assert response.content == ""
    assert response.reasoning_content == "Thinking through the requested answer."


def test_model_response_keeps_reasoning_usage_and_termination_independent() -> None:
    """Provider response facts coexist without cross-field assumptions."""
    response = ModelResponse(
        content="final",
        source=InteractionSource("llama.cpp"),
        reasoning_content="reasoning",
        usage=ModelUsage(input_tokens=_INPUT_TOKENS),
        termination=ModelTermination.NORMAL_STOP,
    )

    assert response.content == "final"
    assert response.reasoning_content == "reasoning"
    assert response.usage == ModelUsage(input_tokens=_INPUT_TOKENS)
    assert response.termination is ModelTermination.NORMAL_STOP


def test_model_termination_uses_provider_neutral_immutable_values() -> None:
    """Termination values describe semantics rather than provider response strings."""
    assert ModelTermination.NORMAL_STOP.value == "normal_stop"
    assert ModelTermination.OUTPUT_LIMIT.value == "output_limit"
    assert ModelTermination.TOOL_CALL.value == "tool_call"


def test_model_usage_allows_partial_provider_counts() -> None:
    """Providers can report one count without local estimation of the others."""
    usage = ModelUsage(input_tokens=_INPUT_TOKENS)

    assert usage.input_tokens == _INPUT_TOKENS
    assert usage.output_tokens is None
    assert usage.total_tokens is None


@pytest.mark.parametrize(
    "value",
    [-1, True, "8"],
)
def test_model_usage_rejects_invalid_provider_counts(value: object) -> None:
    """Reported token counts must be non-negative integers rather than estimates."""
    with pytest.raises((TypeError, ValueError), match="token"):
        ModelUsage(input_tokens=value)  # type: ignore[arg-type]


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
