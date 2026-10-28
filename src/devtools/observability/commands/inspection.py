# Copyright (c) 2026
"""Observe existing handles/results without another executor or raw-output store."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from typing import TYPE_CHECKING

from devtools.observability.commands.models import (
    CommandObservation,
    CommandOrigin,
    CommandPattern,
)
from devtools.resources.commands import CommandStarted

if TYPE_CHECKING:
    from devtools.resources.commands import CommandExecution, CommandResult


def completed_observation(
    result: CommandResult,
    *,
    origin: CommandOrigin,
    pattern: CommandPattern,
) -> CommandObservation:
    """Project a known local result, retaining no diagnostics or environment values."""
    return CommandObservation(
        origin,
        pattern,
        "framework-result",
        entered=True,
        outcome="succeeded" if result.succeeded else "failed",
        exit_code=result.exit_code,
        duration=result.duration,
        events_dropped=result.events_dropped,
        capture_incomplete=result.events_dropped > 0,
    )


class CommandInspector:
    """Consume one opt-in existing handle and preserve its exact result/failure.

    Lifecycle events can be dropped. A returned CommandResult establishes local
    completion even if its event was dropped. On error/cancellation, absence of
    CommandStarted is unknown entry, never proof the process did not execute.
    This claims the handle's sole event consumer; it is not global instrumentation.
    """

    def __init__(self, origin: CommandOrigin, pattern: CommandPattern) -> None:
        """Bind explicit capture policy and association before process observation."""
        self.observation = CommandObservation(origin, pattern, "framework-events")

    async def observe(self, execution: CommandExecution) -> CommandResult:
        """Drain value-free lifecycle facts, then await the same execution once."""

        async def drain() -> None:
            async for event in execution.events():
                if isinstance(event, CommandStarted):
                    self.observation = replace(self.observation, entered=True)

        reader = asyncio.create_task(drain())
        try:
            result = await execution
        except (Exception, asyncio.CancelledError) as error:
            # No diagnostic payload or exception message enters analytics.
            self.observation = replace(
                self.observation,
                outcome="cancelled"
                if isinstance(error, asyncio.CancelledError)
                else "unknown",
                events_dropped=execution.events_dropped,
            )
            raise
        finally:
            # Awaiting the original handle preserves its cancellation/child cleanup.
            # Our sole owned collector is settled on every exit path.
            # Managed Commands closes the event stream before its await finishes.
            # Drain it even for an already completed handle; cancelling an unstarted
            # reader would hide a previously claimed/failed capture boundary.
            settled = await asyncio.gather(reader, return_exceptions=True)
            self.observation = replace(
                self.observation,
                capture_incomplete=execution.events_dropped > 0
                or any(isinstance(x, BaseException) for x in settled),
            )
        self.observation = replace(
            completed_observation(
                result,
                origin=self.observation.origin,
                pattern=self.observation.pattern,
            ),
            source="framework-events",
            events_dropped=execution.events_dropped,
            capture_incomplete=self.observation.capture_incomplete,
        )
        return result
