# Copyright (c) 2026
"""Exceptions for the :mod:`devtools.resources.commands` domain."""


class CommandError(Exception):
    """Base exception for command-execution failures."""


class CommandNotFoundError(CommandError):
    """Raised when the requested executable cannot be found."""


class CommandTimeoutError(CommandError):
    """Raised when command execution exceeds its timeout."""
