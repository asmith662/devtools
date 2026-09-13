# Copyright (c) 2026
"""Provider-local failures for llama.cpp interaction."""

from __future__ import annotations


class LlamaCppInteractionError(Exception):
    """Base error for the llama.cpp interaction adapter."""


class LlamaCppTransportError(LlamaCppInteractionError):
    """Represent a failure before a usable provider HTTP response exists."""

    def __init__(self) -> None:
        """Create the fixed transport-boundary failure."""
        super().__init__("Could not communicate with llama.cpp.")


class LlamaCppHttpError(LlamaCppInteractionError):
    """Represent a non-success HTTP response returned by llama.cpp."""

    def __init__(self, status: int, detail: str) -> None:
        """Create an HTTP failure with bounded provider diagnostic text."""
        super().__init__(f"llama.cpp returned HTTP {status}: {detail}")
        self.status = status


class LlamaCppResponseError(LlamaCppInteractionError):
    """Represent a malformed successful llama.cpp response."""
