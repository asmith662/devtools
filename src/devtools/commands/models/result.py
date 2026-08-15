# Copyright (c) 2026
"""Command execution models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.commands import Command
    from devtools.time import Duration


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Represent the completed result of a command execution.

    A nonzero exit code is a valid command result and does not itself represent
    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`
    when interpreting the command's exit status.

    :ivar command: Command that was executed.
    :ivar exit_code: Process exit code.
    :ivar stdout: Retained leading bytes written to standard output.
    :ivar stderr: Retained leading bytes written to standard error.
    :ivar duration: Monotonic elapsed execution duration.
    :ivar stdout_truncated: Whether stdout exceeded the retained limit.
    :ivar stderr_truncated: Whether stderr exceeded the retained limit.
    :ivar events_dropped: Number of events omitted by bounded buffering.
    """

    command: Command
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: Duration
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    events_dropped: int = 0

    @property
    def succeeded(self) -> bool:
        """Return whether the command exited successfully.

        :returns: ``True`` when the exit code is zero.
        """
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        """Return whether the command exited unsuccessfully.

        :returns: ``True`` when the exit code is nonzero.
        """
        return not self.succeeded
