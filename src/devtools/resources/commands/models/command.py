# Copyright (c) 2026
"""Command specification model."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath
    from devtools.core.time import Duration


def _validate_executable(executable: object) -> None:
    """Validate that the executable is a string.

    :param executable: Candidate executable value.
    :raises TypeError: If the executable is not a string.
    """
    if not isinstance(executable, str):
        msg = f"Command executable must be a string, got {type(executable).__name__}."
        raise TypeError(msg)


def _validate_arguments(arguments: object) -> None:
    """Validate that the arguments form a tuple of strings.

    :param arguments: Candidate arguments value.
    :raises TypeError: If the arguments are not a tuple of strings.
    """
    if not isinstance(arguments, tuple):
        msg = f"Command arguments must be a tuple, got {type(arguments).__name__}."
        raise TypeError(msg)
    for argument in arguments:
        if not isinstance(argument, str):
            msg = (
                "Command arguments must only contain strings, "
                f"got {type(argument).__name__}."
            )
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class Command:
    """Describe an immutable command execution specification.

    A command identifies an executable separately from its arguments and does
    not imply shell parsing, interpolation, or quoting.

    Fluent methods return new command instances and never mutate the original.

    Example::

        command = (
            Command("uv")
            .args("run", "pytest", "-q")
            .cwd(project_root)
            .with_timeout(Duration.minutes(2))
        )

    :ivar executable: Executable name or path.
    :ivar arguments: Ordered executable arguments.
    :ivar working_directory: Optional resolved working directory.
    :ivar timeout: Optional maximum execution duration.
    """

    executable: str
    arguments: tuple[str, ...] = ()
    working_directory: ResolvedPath | None = None
    timeout: Duration | None = None

    def __post_init__(self) -> None:
        """Validate command invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the command specification.

        :raises TypeError: If the executable is not a string, or the
            arguments are not a tuple whose members are all strings.
        :raises ValueError: If the executable is empty or whitespace-only.
        """
        _validate_executable(self.executable)
        _validate_arguments(self.arguments)
        if not self.executable.strip():
            msg = "Command executable cannot be empty."
            raise ValueError(msg)

    @property
    def argv(self) -> tuple[str, ...]:
        """Return the complete process argument vector.

        :returns: Executable followed by all ordered arguments.
        """
        return (self.executable, *self.arguments)

    def args(self, *arguments: str) -> Command:
        """Append arguments to the command.

        Existing arguments are preserved and the supplied arguments are
        appended in order.

        :param arguments: Arguments to append.
        :returns: New command containing the appended arguments.
        :raises TypeError: If any supplied argument is not a string.
        """
        return replace(
            self,
            arguments=(*self.arguments, *arguments),
        )

    def with_args(self, *arguments: str) -> Command:
        """Replace all command arguments.

        :param arguments: Complete replacement argument sequence.
        :returns: New command containing only the supplied arguments.
        :raises TypeError: If any supplied argument is not a string.
        """
        return replace(
            self,
            arguments=arguments,
        )

    def without_args(self) -> Command:
        """Remove all command arguments.

        :returns: New command with no arguments.
        """
        return replace(
            self,
            arguments=(),
        )

    def with_executable(self, executable: str) -> Command:
        """Replace the command executable.

        :param executable: Replacement executable name or path.
        :returns: New command with the replacement executable.
        :raises TypeError: If the replacement executable is not a string.
        :raises ValueError: If the replacement executable is blank.
        """
        return replace(
            self,
            executable=executable,
        )

    def cwd(self, working_directory: ResolvedPath) -> Command:
        """Set the command working directory.

        :param working_directory: Directory in which the command should run.
        :returns: New command with the supplied working directory.
        """
        return replace(
            self,
            working_directory=working_directory,
        )

    def without_cwd(self) -> Command:
        """Remove the configured working directory.

        :returns: New command without an explicit working directory.
        """
        return replace(
            self,
            working_directory=None,
        )

    def with_timeout(self, timeout: Duration) -> Command:
        """Set the maximum command execution duration.

        :param timeout: Maximum execution duration.
        :returns: New command with the supplied timeout.
        """
        return replace(
            self,
            timeout=timeout,
        )

    def without_timeout(self) -> Command:
        """Remove the configured execution timeout.

        :returns: New command without an execution timeout.
        """
        return replace(
            self,
            timeout=None,
        )
