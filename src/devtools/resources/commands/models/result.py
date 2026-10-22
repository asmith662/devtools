# Copyright (c) 2026
"""Command execution models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.core.time import Duration
    from devtools.resources.commands import Command


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
        """Return whether the exit code is in the command's success policy.

        :returns: ``True`` when the raw exit code is a member of
            :attr:`Command.success_exit_codes`.
        """
        return self.exit_code in self.command.success_exit_codes

    @property
    def failed(self) -> bool:
        """Return whether the exit code is outside the success policy.

        :returns: ``True`` when the raw exit code is not a member of
            :attr:`Command.success_exit_codes`.
        """
        return not self.succeeded

    def stdout_text(
        self,
        *,
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> str:
        """Return the captured standard output decoded as text.

        This is an explicit decoded view over the retained :attr:`stdout`
        bytes. The retained bytes are not modified and the truncation flags
        are unchanged. Decoding uses the native codec contract: invalid
        bytes raise :class:`UnicodeDecodeError` under ``errors="strict"``,
        while replacement or ignore policies apply, and unknown encodings
        raise :class:`LookupError`.

        :param encoding: Codec name used to decode the retained bytes.
        :param errors: Error handling scheme passed to the codec.
        :returns: The decoded standard output text.
        """
        return self.stdout.decode(encoding=encoding, errors=errors)

    def stderr_text(
        self,
        *,
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> str:
        """Return the captured standard error decoded as text.

        This is an explicit decoded view over the retained :attr:`stderr`
        bytes. The retained bytes are not modified and the truncation flags
        are unchanged. Decoding uses the native codec contract: invalid
        bytes raise :class:`UnicodeDecodeError` under ``errors="strict"``,
        while replacement or ignore policies apply, and unknown encodings
        raise :class:`LookupError`.

        :param encoding: Codec name used to decode the retained bytes.
        :param errors: Error handling scheme passed to the codec.
        :returns: The decoded standard error text.
        """
        return self.stderr.decode(encoding=encoding, errors=errors)
