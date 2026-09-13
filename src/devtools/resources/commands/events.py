# Copyright (c) 2026
"""Structured command execution events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.core.time import Duration
    from devtools.resources.commands.models import Command


@dataclass(frozen=True, slots=True)
class CommandStarted:
    """Represent the start of a command execution.

    :ivar command: Command that started executing.
    """

    command: Command


@dataclass(frozen=True, slots=True)
class CommandStdout:
    """Represent bytes emitted to standard output.

    :ivar data: Bytes emitted by the process.
    """

    data: bytes


@dataclass(frozen=True, slots=True)
class CommandStderr:
    """Represent bytes emitted to standard error.

    :ivar data: Bytes emitted by the process.
    """

    data: bytes


@dataclass(frozen=True, slots=True)
class CommandExited:
    """Represent completion of a command process.

    :ivar exit_code: Process exit code.
    :ivar duration: Total elapsed execution duration.
    """

    exit_code: int
    duration: Duration


CommandEvent = CommandStarted | CommandStdout | CommandStderr | CommandExited
