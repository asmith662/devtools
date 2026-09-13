# Copyright (c) 2026
"""Tests for the structural ModelInteraction protocol."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelInteraction,
    ModelResponse,
    Prompt,
)


@dataclass(frozen=True, slots=True)
class FakeInteraction:
    """Minimal structural model interaction implementation."""

    source: InteractionSource

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
    ) -> ModelResponse:
        """Return same-source output and preserve provider continuation."""
        return ModelResponse(
            content=f"Reply to: {prompt.content}",
            source=self.source,
            conversation=conversation,
        )


def test_model_interaction_is_structural_and_accepts_prompts() -> None:
    """A compatible provider is used solely through the model interaction protocol."""
    source = InteractionSource("fake")
    interaction: ModelInteraction = FakeInteraction(source)
    prompt = Prompt(content="Remember ALPHA-4821.", role="user")
    continuation = ConversationRef(source, "opaque-thread")

    async def send_twice() -> tuple[ModelResponse, ModelResponse]:
        return (
            await interaction.send(prompt),
            await interaction.send(prompt, conversation=continuation),
        )

    first, second = asyncio.run(send_twice())
    assert first.content == "Reply to: Remember ALPHA-4821."
    assert first.conversation is None
    assert second.conversation is continuation
