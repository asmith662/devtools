# Copyright (c) 2026
"""Tests for structured command execution events."""

from dataclasses import FrozenInstanceError

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import (
    Command,
    CommandExited,
    CommandStarted,
    CommandStderr,
    CommandStdout,
)


def test_command_events_are_immutable_value_objects() -> None:
    """Each event retains its structured observation data immutably."""
    command = Command("python", ("-c", "pass"))
    started = CommandStarted(command)
    stdout = CommandStdout(b"out")
    stderr = CommandStderr(b"error")
    exited = CommandExited(0, Duration.seconds(1))
    attribute = "data"

    assert started == CommandStarted(command)
    assert stdout == CommandStdout(b"out")
    assert stderr == CommandStderr(b"error")
    assert exited == CommandExited(0, Duration.seconds(1))
    assert hash(started) == hash(CommandStarted(command))

    with pytest.raises(FrozenInstanceError):
        setattr(stdout, attribute, b"changed")
