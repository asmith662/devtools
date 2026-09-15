# Copyright (c) 2026
"""Portable transient facts emitted at a completed model-interaction boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from devtools.core.identity import Identity

if TYPE_CHECKING:
    from devtools.core.time import Timestamp
    from devtools.models.interaction.models import InteractionSource, ModelRequest
    from devtools.models.interaction.response import ModelResponse


@dataclass(frozen=True, slots=True)
class ModelInteractionId:
    """Identify one invocation occurrence, independent of its request value."""

    value: Identity

    @classmethod
    def new(cls) -> ModelInteractionId:
        """Generate an identity for one provider invocation."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> ModelInteractionId:
        """Parse canonical UUID text."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return canonical UUID text."""
        return str(self.value)


@dataclass(frozen=True, slots=True)
class ModelInteractionObservation:
    """Carry completed interaction facts to an optional external observer.

    This is a transient composition seam, not Evidence and not a response
    metadata container.  Observability decides whether and how to retain it.
    """

    interaction_id: ModelInteractionId
    provider: str
    source: InteractionSource
    request: ModelRequest
    response: ModelResponse
    started_at: Timestamp
    completed_at: Timestamp
    provider_response_id: str | None = None
    provider_model: str | None = None

    def __post_init__(self) -> None:
        """Keep the occurrence interval and provider discriminator honest."""
        if not self.provider.strip():
            msg = "Model interaction observation provider cannot be blank."
            raise ValueError(msg)
        if self.completed_at.value < self.started_at.value:
            msg = "Model interaction observation cannot complete before it starts."
            raise ValueError(msg)


class ModelInteractionObserver(Protocol):
    """Receive one completed interaction without making observation mandatory."""

    def interaction_completed(self, observation: ModelInteractionObservation) -> None:
        """Observe one completed interaction occurrence."""
