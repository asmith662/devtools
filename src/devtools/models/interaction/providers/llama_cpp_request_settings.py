# Copyright (c) 2026
"""Typed llama.cpp-specific request-settings extension seam."""

import math
from dataclasses import dataclass, field
from typing import Literal

from devtools.models.interaction import ProviderRequestSettings

_MAXIMUM_TOP_K = 1024


@dataclass(frozen=True, slots=True)
class LlamaCppRequestSettings(ProviderRequestSettings):
    """Supported llama.cpp template reasoning control; defaults stay unchanged."""

    provider: str = field(init=False, default="llama.cpp")
    reasoning_effort: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    min_p: float | None = None
    presence_penalty: float | None = None
    response_format: Literal["json_object"] | None = None

    def __post_init__(self) -> None:
        """Reject unsupported template settings before dispatch."""
        super(LlamaCppRequestSettings, self).__post_init__()
        if self.response_format not in (None, "json_object"):
            msg = "llama.cpp response format must be json_object or None."
            raise ValueError(msg)
        if self.reasoning_effort not in {None, "low", "medium", "xhigh"}:
            msg = "llama.cpp reasoning effort must be low, medium, xhigh or None."
            raise ValueError(msg)
        for value, lower, upper in (
            (self.temperature, 0, 2),
            (self.top_p, 0, 1),
            (self.min_p, 0, 1),
            (self.presence_penalty, -2, 2),
        ):
            if value is not None and (
                type(value) not in {int, float}
                or not math.isfinite(value)
                or not lower <= value <= upper
            ):
                msg = "llama.cpp sampling value is outside supported finite bounds."
                raise ValueError(msg)
        if self.top_k is not None and (
            type(self.top_k) is not int or not 0 <= self.top_k <= _MAXIMUM_TOP_K
        ):
            msg = "llama.cpp top_k must be an integer from 0 to 1024."
            raise ValueError(msg)
