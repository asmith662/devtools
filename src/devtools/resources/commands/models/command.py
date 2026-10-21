# Copyright (c) 2026
"""Command specification model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath
    from devtools.core.time import Duration


def _validate_environment(environment: object) -> None:
    """Validate that the environment is an optional mapping of str to str.

    :param environment: Candidate environment value.
    :raises TypeError: If the environment is neither a mapping nor None, or
        if any key or value is not a string.
    :raises ValueError: If a name is empty, contains '=' or NUL, or a value
        contains NUL.
    """
    if environment is None:
        return
    if not isinstance(environment, Mapping):
        msg = (
            "Command environment must be a mapping or None, "
            f"got {type(environment).__name__}."
        )
        raise TypeError(msg)
    for key, value in environment.items():
        if not isinstance(key, str):
            msg = f"Command environment keys must be strings, got {type(key).__name__}."
            raise TypeError(msg)
        if not isinstance(value, str):
            msg = (
                "Command environment values must be strings, "
                f"got {type(value).__name__}."
            )
            raise TypeError(msg)
        if not key:
            msg = "Command environment names cannot be empty."
            raise ValueError(msg)
        if "=" in key:
            msg = "Command environment names cannot contain '='."
            raise ValueError(msg)
        if "\0" in key:
            msg = "Command environment names cannot contain NUL."
            raise ValueError(msg)
        if "\0" in value:
            msg = "Command environment values cannot contain NUL."
            raise ValueError(msg)


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


def _validate_stdin(stdin: object) -> None:
    """Validate that standard input is immutable bytes or None.

    :param stdin: Candidate standard input value.
    :raises TypeError: If the value is neither ``bytes`` nor ``None``.
    """
    if stdin is not None and not isinstance(stdin, bytes):
        msg = f"Command stdin must be bytes or None, got {type(stdin).__name__}."
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
    stdin: bytes | None = None
    environment: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        """Validate command invariants."""
        self._validate()
        if self.environment is not None:
            object.__setattr__(
                self,
                "environment",
                MappingProxyType(dict(self.environment)),
            )

    def _validate(self) -> None:
        """Validate the command specification.

        :raises TypeError: If the executable is not a string, the arguments
            are not a tuple of strings, stdin is not bytes or None, or the
            environment is not a mapping of str to str.
        :raises ValueError: If the executable is empty or whitespace-only,
            or an environment name is empty or contains '=' or NUL.
        """
        _validate_executable(self.executable)
        _validate_arguments(self.arguments)
        _validate_stdin(self.stdin)
        _validate_environment(self.environment)
        if not self.executable.strip():
            msg = "Command executable cannot be empty."
            raise ValueError(msg)

    def __hash__(self) -> int:
        """Return an order-independent hash of the command specification."""
        env_hash = (
            hash(frozenset(self.environment.items()))
            if self.environment is not None
            else 0
        )
        return hash(
            (
                self.executable,
                self.arguments,
                self.working_directory,
                self.timeout,
                self.stdin,
                env_hash,
            ),
        )

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

    def with_stdin(self, stdin: bytes) -> Command:
        """Set the standard input payload delivered to the child.

        :param stdin: Immutable byte payload for standard input.
        :returns: New command with the supplied standard input.
        :raises TypeError: If the payload is not ``bytes``.
        """
        return replace(
            self,
            stdin=stdin,
        )

    def without_stdin(self) -> Command:
        """Remove the configured standard input payload.

        :returns: New command with inherited standard input.
        """
        return replace(
            self,
            stdin=None,
        )

    def with_environment(self, environment: Mapping[str, str]) -> Command:
        """Replace the per-command environment overrides.

        The supplied mapping overlays the parent environment for this command
        only.  The caller's mapping is snapshotted defensively and the returned
        command exposes a read-only view.

        :param environment: Environment variable overrides.
        :returns: New command with the supplied environment overrides.
        :raises TypeError: If the value is not a mapping, or a key or value is
            not a string.
        :raises ValueError: If a name is empty, contains '=' or NUL, or a
            value contains NUL.
        """
        return replace(
            self,
            environment=environment,
        )

    def without_environment(self) -> Command:
        """Remove per-command environment overrides.

        :returns: New command that inherits the parent environment.
        """
        return replace(
            self,
            environment=None,
        )
