# Copyright (c) 2026
"""Live command execution handles."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Generator

    from devtools.commands.events import CommandEvent
    from devtools.commands.models import CommandResult

type ExecutionRunner = Callable[
    ["CommandExecution"],
    Coroutine[Any, Any, CommandResult],
]


class CommandExecution:
    """Represent one live command execution.

    A command execution is awaitable. Awaiting it returns the final
    :class:`~devtools.commands.models.CommandResult`.

    Events emitted while the command runs may be consumed through
    :meth:`events`.

    The underlying command is executed exactly once regardless of how many
    times the execution is awaited.
    """

    def __init__(
        self,
        runner: ExecutionRunner,
        *,
        max_pending_events: int,
    ) -> None:
        """Create and start a command execution.

        :param runner: Coroutine responsible for executing the command.
        """
        self._event_queue: asyncio.Queue[CommandEvent] = asyncio.Queue(
            maxsize=max_pending_events,
        )
        self._event_available = asyncio.Event()
        self._events_closed = False
        self._events_claimed = False
        self._events_dropped = 0
        self._task: asyncio.Task[CommandResult] = asyncio.create_task(runner(self))

    def __await__(
        self,
    ) -> Generator[Any, None, CommandResult]:
        """Await completion of the command execution.

        :returns: Final command result.
        """
        return self._task.__await__()

    @property
    def is_running(self) -> bool:
        """Return whether execution is still in progress.

        :returns: ``True`` while the execution has not completed.
        """
        return not self._task.done()

    @property
    def is_complete(self) -> bool:
        """Return whether execution has completed.

        :returns: ``True`` once execution has completed.
        """
        return self._task.done()

    @property
    def events_dropped(self) -> int:
        """Return the number of events omitted by bounded buffering.

        :returns: Number of output events dropped before observation.
        """
        return self._events_dropped

    async def events(self) -> AsyncIterator[CommandEvent]:
        """Yield structured events emitted by the execution.

        Only one consumer may iterate the event stream for a given execution.

        :yields: Command execution events.
        :raises RuntimeError: If the event stream has already been claimed.
        """
        if self._events_claimed:
            msg = "Command execution events may only be consumed once."
            raise RuntimeError(msg)

        self._events_claimed = True

        while True:
            try:
                event = self._event_queue.get_nowait()
            except asyncio.QueueEmpty:
                if self._events_closed:
                    return

                await self._event_available.wait()
                self._event_available.clear()
                continue

            yield event

    def _emit(self, event: CommandEvent) -> None:
        """Emit an execution event.

        :param event: Event to emit.
        """
        try:
            self._event_queue.put_nowait(event)
        except asyncio.QueueFull:
            self._events_dropped += 1
            return

        self._event_available.set()

    def _close_events(self) -> None:
        """Close the execution event stream."""
        self._events_closed = True
        self._event_available.set()
