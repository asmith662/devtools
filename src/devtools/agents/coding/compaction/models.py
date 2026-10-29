# Copyright (c) 2026
"""Host authority and transient accounting for optional working-state summaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.core.time import Duration
    from devtools.models.interaction import (
        InteractionSource,
        ModelInteraction,
        ModelRequest,
        ModelResponse,
        ModelSettings,
        ModelUsage,
        PromptMessage,
        ProviderRequestSettings,
    )

    from .adaptive import AdaptiveCompaction


@dataclass(frozen=True, slots=True)
class SummarySelection:
    """Separately authorize outbound disclosure and replacement of original indices."""

    disclose: frozenset[int]
    replace: frozenset[int]

    def __post_init__(self) -> None:
        """Require an immutable subset; history bounds are checked later."""
        if (
            not isinstance(self.disclose, frozenset)
            or not isinstance(self.replace, frozenset)
            or not self.replace <= self.disclose
            or any(type(i) is not int or i < 0 for i in self.disclose)
        ):
            msg = "Invalid summary disclosure selection."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class SummaryCompaction:
    """Explicit auxiliary-model envelope, independent of acting-model budgets.

    Selection is trusted host policy over ORIGINAL messages. It grants outbound
    disclosure to this interaction, not execution authority. Provider reasoning
    is never disclosed. Entry needs an explicit host request or opt-in adaptive
    policy; configuration without either still makes no auxiliary request.
    """

    interaction: ModelInteraction
    select: Callable[[tuple[PromptMessage, ...]], SummarySelection]
    maximum_calls: int
    input_bytes: int
    output_bytes: int
    settings: ModelSettings
    timeout: Duration
    recent_exchanges: int = 1
    input_tokens: int | None = None
    measure_input: Callable[[ModelRequest], Awaitable[int]] | None = None
    retain_payloads: bool = False
    adaptive: AdaptiveCompaction | None = None
    provider_settings: ProviderRequestSettings | None = None
    allow_json_fence: bool = False

    def __post_init__(self) -> None:
        """Require explicit finite bounds; never invent a tokenizer or capacity."""
        bounds = (
            self.maximum_calls,
            self.input_bytes,
            self.output_bytes,
            self.recent_exchanges,
            self.settings.maximum_output_tokens,
        )
        if (
            any(type(v) is not int or v <= 0 for v in bounds)
            or type(self.allow_json_fence) is not bool
            or self.timeout.total_seconds <= 0
            or (self.input_tokens is None) != (self.measure_input is None)
            or (
                self.input_tokens is not None
                and (type(self.input_tokens) is not int or self.input_tokens <= 0)
            )
        ):
            msg = "Invalid bounded summary configuration."
            raise ValueError(msg)


@dataclass(slots=True)
class SummaryAttempt:
    """Qualified strategy facts, never a Tool receipt or candidate acceptance.

    Original exceptions stay available locally; callers must not export their
    messages as privacy-safe analytics. Raw auxiliary payloads are opt-in.
    """

    status: str = "requested"
    entered: bool = False
    response_received: bool = False
    validated: bool = False
    adopted: bool = False
    normalized_json_fence: bool = False
    input_indices: tuple[int, ...] = ()
    replaced_indices: tuple[int, ...] = ()
    partial_coverage: bool = True
    input_bytes: int | None = None
    measured_input_tokens: int | None = None
    request_digest: str | None = None
    response_digest: str | None = None
    original_bytes: int | None = None
    resulting_bytes: int | None = None
    usage: ModelUsage | None = None
    source: InteractionSource | None = None
    request: ModelRequest | None = None
    response: ModelResponse | None = None
    error: BaseException | None = None
