# Copyright (c) 2026
"""Tests for the structural ModelInteraction protocol."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from inspect import signature

from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelInteraction,
    ModelRequest,
    ModelResponse,
    Prompt,
)


@dataclass(frozen=True, slots=True)
class FakeInteraction:
    """Minimal structural model interaction implementation."""

    source: InteractionSource

    async def send(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """Return same-source output and preserve provider continuation."""
        return ModelResponse(
            content=f"Reply to: {request.prompt.content}",
            source=self.source,
            conversation=request.conversation,
        )


def test_model_interaction_is_structural_and_accepts_prompts() -> None:
    """A compatible provider is used solely through the model interaction protocol."""
    source = InteractionSource("fake")
    interaction: ModelInteraction = FakeInteraction(source)
    prompt = Prompt(content="Remember ALPHA-4821.", role="user")
    continuation = ConversationRef(source, "opaque-thread")

    async def send_twice() -> tuple[ModelResponse, ModelResponse]:
        return (
            await interaction.send(ModelRequest(prompt)),
            await interaction.send(ModelRequest(prompt, conversation=continuation)),
        )

    first, second = asyncio.run(send_twice())
    assert first.content == "Reply to: Remember ALPHA-4821."
    assert first.conversation is None
    assert second.conversation is continuation


def test_model_interaction_exposes_one_request_parameter_without_legacy_controls() -> (
    None
):
    """The reusable protocol has no competing keyword request surface."""
    assert tuple(signature(ModelInteraction.send).parameters) == ("self", "request")
