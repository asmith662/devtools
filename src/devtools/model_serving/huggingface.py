# Copyright (c) 2026
"""Pinned Hugging Face model references for provider launch."""

from __future__ import annotations

import re
from dataclasses import dataclass

_PINNED_REVISION = re.compile(r"^[0-9a-fA-F]{40}$")


@dataclass(frozen=True, slots=True)
class HuggingFaceModelRef:
    """Represent one exact Hugging Face model repository revision.

    vLLM's normal model-loading CLI consumes a repository plus revision; it
    does not consume an individual filename.  A future GGUF-oriented provider
    can pressure-test whether a distinct artifact-file value is warranted.

    :ivar repository: Hugging Face repository identifier.
    :ivar revision: Pinned commit revision to load.
    """

    repository: str
    revision: str

    def __post_init__(self) -> None:
        """Validate the local structural identity."""
        if not self.repository.strip():
            msg = "Hugging Face repository cannot be empty."
            raise ValueError(msg)

        if not self.revision.strip():
            msg = "Hugging Face revision cannot be empty."
            raise ValueError(msg)

        if _PINNED_REVISION.fullmatch(self.revision) is None:
            msg = "Hugging Face revision must be a pinned 40-character commit ID."
            raise ValueError(msg)
