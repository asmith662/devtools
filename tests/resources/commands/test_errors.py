# Copyright (c) 2026
"""Tests for public command-domain error types."""

from devtools.resources.commands import (
    CommandError,
    CommandNotFoundError,
    CommandTimeoutError,
)


def test_command_errors_share_the_domain_base_type() -> None:
    """Specific command errors remain catchable as command-domain failures."""
    assert issubclass(CommandNotFoundError, CommandError)
    assert issubclass(CommandTimeoutError, CommandError)
    assert issubclass(CommandError, Exception)
