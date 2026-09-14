# Copyright (c) 2026
"""Structural protocols for model invocation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from devtools.models.interaction.models import ConversationRef, InteractionSource
    from devtools.models.interaction.prompt import Prompt
    from devtools.models.interaction.response import ModelResponse


class ModelInteraction(Protocol):
    """Describe one asynchronous invocation of a selected model."""

    @property
    def source(self) -> InteractionSource:
        """Return the source represented by this model interaction."""

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
        maximum_output_tokens: int | None = None,
        thinking_enabled: bool | None = None,
    ) -> ModelResponse:
        """Send one prompt with an optional requested output-token limit.

        Implementations must honor supplied request controls or reject them
        explicitly.
        """
