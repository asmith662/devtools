# Copyright (c) 2026
"""Privacy-selected command facts with explicit origin and unavailable outcomes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from devtools.core.time import Duration

type CommandOutcome = Literal["succeeded", "failed", "cancelled", "unknown", "conflict"]
type ArgumentRole = Literal["flag", "path", "value", "script", "opaque"]
_MAX_ARGUMENT_ROLES = 64
_MAX_CAPABILITIES = 16


@dataclass(frozen=True, slots=True)
class CommandOrigin:
    """Host-authenticated association, not identities supplied by command output.

    These are host/external correlation keys, not parallel framework UUIDs.
    The host must select nonprivate opaque labels in its own namespace.
    """

    agent: str
    task: str
    run: str
    call: str

    def __post_init__(self) -> None:
        """Refuse unbounded or blank origin keys before capture."""
        if any(
            not re.fullmatch("[A-Za-z0-9._:/-]{1,128}", value)
            for value in (self.agent, self.task, self.run, self.call)
        ):
            msg = "Command origin requires bounded opaque correlation labels."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class CommandPattern:
    """Explicit host projection; never retain raw argv, shell text or env values."""

    family: str
    operation: str
    argument_roles: tuple[ArgumentRole, ...] = ()
    capabilities: tuple[str, ...] = ()
    equivalent_tool: str | None = None

    def __post_init__(self) -> None:
        """Bound structural labels and restrict arguments to value-free roles."""
        labels = (self.family, self.operation, *self.capabilities)
        if self.equivalent_tool is not None:
            labels += (self.equivalent_tool,)
        if (
            not isinstance(self.argument_roles, tuple)
            or not isinstance(self.capabilities, tuple)
            or len(self.argument_roles) > _MAX_ARGUMENT_ROLES
            or len(self.capabilities) > _MAX_CAPABILITIES
            or any(not re.fullmatch("[A-Za-z0-9._:/-]{1,128}", s) for s in labels)
            or any(
                r not in {"flag", "path", "value", "script", "opaque"}
                for r in self.argument_roles
            )
        ):
            msg = (
                "Command pattern requires bounded structural labels and argument roles."
            )
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class CommandObservation:
    """One qualified observation; source distinguishes local facts and CLI reports.

    No raw command, output, stdin, source text, environment or credentials are
    retained. None means unknown, including process entry and elapsed duration.
    This value is process-local and does not authenticate a durable receipt.
    """

    origin: CommandOrigin
    pattern: CommandPattern
    source: Literal["framework-events", "framework-result", "codex-jsonl"]
    entered: bool | None = None
    outcome: CommandOutcome = "unknown"
    exit_code: int | None = None
    duration: Duration | None = None
    events_dropped: int = 0
    capture_incomplete: bool = False

    def __post_init__(self) -> None:
        """Keep known exit/outcome facts consistent without inferring missing values."""
        if (
            self.events_dropped < 0
            or (self.exit_code is not None and type(self.exit_code) is not int)
            or (self.outcome in {"succeeded", "failed"} and self.exit_code is None)
            or (self.entered is False and self.exit_code is not None)
        ):
            msg = "Command observation has inconsistent known facts."
            raise ValueError(msg)
