# Copyright (c) 2026
"""Provider-local failures for llama.cpp/Qwen interaction."""

from __future__ import annotations


class QwenError(Exception):
    """Base error for the experimental Qwen provider adapter."""


class QwenTransportError(QwenError):
    """Represent a failure before a usable provider HTTP response exists."""

    def __init__(self) -> None:
        """Create the fixed transport-boundary failure."""
        super().__init__("Could not communicate with llama.cpp.")


class QwenHttpError(QwenError):
    """Represent a non-success HTTP response returned by llama.cpp."""

    def __init__(self, status: int, detail: str) -> None:
        """Create an HTTP failure with bounded provider diagnostic text."""
        super().__init__(f"llama.cpp returned HTTP {status}: {detail}")
        self.status = status


class QwenResponseError(QwenError):
    """Represent a malformed successful llama.cpp response."""
