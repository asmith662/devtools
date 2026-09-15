# Copyright (c) 2026
"""Typed llama.cpp-specific request-settings extension seam."""

from dataclasses import dataclass, field

from devtools.models.interaction import ProviderRequestSettings


@dataclass(frozen=True, slots=True)
class LlamaCppRequestSettings(ProviderRequestSettings):
    """Reserve an immutable typed extension point for llama.cpp-only settings.

    The established output and thinking controls are portable `ModelSettings`,
    so this Phase 1 value intentionally carries no speculative provider field.
    """

    provider: str = field(init=False, default="llama.cpp")
