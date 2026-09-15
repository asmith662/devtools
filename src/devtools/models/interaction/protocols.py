# Copyright (c) 2026
"""Structural protocols for model invocation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from devtools.models.interaction.models import InteractionSource, ModelRequest
    from devtools.models.interaction.response import ModelResponse


class ModelInteraction(Protocol):
    """Describe one asynchronous invocation of a selected model."""

    @property
    def source(self) -> InteractionSource:
        """Return the source represented by this model interaction."""

    async def send(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """Send one immutable semantic model request.

        Implementations must honor supplied request settings or reject them.
        """
