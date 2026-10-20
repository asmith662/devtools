# Copyright (c) 2026
"""Typed llama.cpp-specific request-settings extension seam."""

from dataclasses import dataclass, field

from devtools.models.interaction import ProviderRequestSettings


@dataclass(frozen=True, slots=True)
class LlamaCppRequestSettings(ProviderRequestSettings):
    """Supported llama.cpp template reasoning control; defaults stay unchanged."""

    provider: str = field(init=False, default="llama.cpp")
    reasoning_effort: str | None = None

    def __post_init__(self) -> None:
        """Reject unsupported template settings before dispatch."""
        super(LlamaCppRequestSettings, self).__post_init__()
        if self.reasoning_effort not in {None, "low", "medium", "xhigh"}:
            msg = "llama.cpp reasoning effort must be low, medium, xhigh or None."
            raise ValueError(msg)
