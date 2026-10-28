# Copyright (c) 2026
# ruff: noqa: TRY301 -- normalize invalid external fields at this bounded JSON boundary
"""Bounded projection of available Codex exec JSONL command items; no invocation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.observability.commands.models import (
    CommandObservation,
    CommandOrigin,
    CommandPattern,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.observability.commands.models import CommandOutcome

_UNKNOWN = CommandPattern("unknown", "unclassified", ("opaque",), ("codex-jsonl",))


def project_known_command(command: str) -> CommandPattern:
    """Recognize a finite exact vocabulary; never parse arbitrary shell text.

    Callers can supply another trusted value-free projection. Shell wrappers,
    unknown flags, paths and all unrecognized commands remain opaque by default.
    No raw string, hash, output or environment is retained in returned analytics.
    """
    if command in {"git status --porcelain=v1 -z", "git status --porcelain"}:
        return CommandPattern(
            "git",
            "status",
            ("flag",),
            ("git",),
            "tools.repository.GitInspectionTool",
        )
    if command in {"git diff --check", "git diff --check HEAD"}:
        return CommandPattern(
            "git",
            "whitespace",
            ("flag",),
            ("git",),
            "tools.checks.FixedCheckTool",
        )
    return _UNKNOWN


@dataclass(slots=True)
class _Item:
    pattern: CommandPattern = _UNKNOWN
    command_digest: str | None = field(default=None, repr=False)
    exit_codes: set[int] = field(default_factory=set)
    terminal_statuses: set[str] = field(default_factory=set)
    terminal: bool = False
    conflict: bool = False


@dataclass(frozen=True, slots=True)
class CodexCommandReport:
    """Selected CLI facts; terminal observation never certifies a complete feed."""

    observations: tuple[CommandObservation, ...]
    malformed_records: int
    terminal_observed: bool


class CodexCommandObserver:
    """Reconcile selected item IDs within exactly one host-associated CLI run.

    Identical repeats are idempotent, partial/out-of-order updates retain known
    fields, contradictory command/exit/terminal claims remain explicit conflicts.
    No raw payload or private record is persisted. Default CodexAgent is untouched.
    """

    def __init__(
        self,
        origin: CommandOrigin,
        *,
        project: Callable[[str], CommandPattern] = project_known_command,
        maximum_line_bytes: int = 65536,
        maximum_records: int = 4096,
    ) -> None:
        """Bind a unique run namespace and explicit finite input/retention policy."""
        if min(maximum_line_bytes, maximum_records) < 1:
            msg = "Codex command observation requires positive bounds."
            raise ValueError(msg)
        self.origin, self.project = origin, project
        self.maximum_line_bytes, self.maximum_records = (
            maximum_line_bytes,
            maximum_records,
        )
        self._items: dict[str, _Item] = {}
        self._records = self._malformed = 0
        self._terminal = False

    def feed(self, line: bytes) -> None:  # noqa: C901, PLR0912, PLR0915 -- validate a bounded event before committing any facts
        """Consume one complete UTF8 JSON object under bounds, retaining no payload."""
        self._records += 1
        try:
            if (
                len(line) > self.maximum_line_bytes
                or self._records > self.maximum_records
            ):
                msg = "Bound exceeded"
                raise TypeError(msg)
            event = json.loads(
                line.decode("utf-8"),
                object_pairs_hook=_pairs,
                parse_constant=_constant,
            )
            if not isinstance(event, dict) or not isinstance(event.get("type"), str):
                msg = "Invalid event"
                raise TypeError(msg)
            if event["type"] in {"turn.completed", "turn.failed"}:
                self._terminal = True
            if event["type"] not in {"item.started", "item.updated", "item.completed"}:
                return
            item = event.get("item")
            if not isinstance(item, dict):
                msg = "Invalid item"
                raise TypeError(msg)
            if item.get("type") != "command_execution":
                return
            identity = item.get("id")
            if not isinstance(identity, str) or not re.fullmatch(
                r"item_[0-9]{1,12}",
                identity,
            ):
                msg = "Invalid item identity"
                raise TypeError(msg)
            CommandOrigin(
                self.origin.agent,
                self.origin.task,
                self.origin.run,
                self.origin.call + "/" + identity,
            )
            state = self._items.get(identity, _Item())
            command = item.get("command")
            # Validate the entire observation before changing retained state.
            pattern = self.project(command) if isinstance(command, str) else None
            if ("command" in item and not isinstance(command, str)) or (
                pattern is not None and not isinstance(pattern, CommandPattern)
            ):
                msg = "Invalid command projection"
                raise ValueError(msg)
            code = item.get("exit_code")
            if code is not None and type(code) is not int:
                msg = "Invalid exit"
                raise ValueError(msg)
            status = item.get("status")
            if status is not None and status not in {
                "in_progress",
                "completed",
                "failed",
            }:
                msg = "Invalid status"
                raise ValueError(msg)
            if pattern is not None and isinstance(command, str):
                digest = hashlib.sha256(command.encode()).hexdigest()
                state.conflict |= (
                    state.command_digest is not None and state.command_digest != digest
                )
                if state.command_digest is None:
                    state.pattern, state.command_digest = pattern, digest
            if code is not None:
                state.exit_codes.add(code)
            if event["type"] == "item.completed":
                state.terminal = True
                if status is not None:
                    state.terminal_statuses.add(status)
            state.conflict |= (
                len(state.exit_codes) > 1 or len(state.terminal_statuses) > 1
            )
            state.conflict |= (
                "failed" in state.terminal_statuses and 0 in state.exit_codes
            ) or "in_progress" in state.terminal_statuses
            self._items[identity] = state
        except (ValueError, TypeError, UnicodeError, RecursionError):
            self._malformed += 1
            msg = (
                "Codex command event is malformed, unsupported or outside "
                "capture bounds."
            )
            raise CodexOutputError(msg) from None

    def report(self) -> CodexCommandReport:
        """Expose normalized facts only, retaining unknown entry/duration explicitly."""
        observations = []
        for identity, item in self._items.items():
            code = next(iter(item.exit_codes)) if len(item.exit_codes) == 1 else None
            outcome: CommandOutcome = "conflict" if item.conflict else "unknown"
            if not item.conflict and item.terminal and code is not None:
                outcome = "succeeded" if code == 0 else "failed"
            observations.append(
                CommandObservation(
                    CommandOrigin(
                        self.origin.agent,
                        self.origin.task,
                        self.origin.run,
                        self.origin.call + "/" + identity,
                    ),
                    item.pattern,
                    "codex-jsonl",
                    outcome=outcome,
                    exit_code=None if item.conflict else code,
                    capture_incomplete=bool(self._malformed)
                    or not self._terminal
                    or item.conflict,
                ),
            )
        return CodexCommandReport(tuple(observations), self._malformed, self._terminal)


def _pairs(values: list[tuple[str, object]]) -> dict[str, object]:
    result = dict(values)
    if len(result) != len(values):
        msg = "Duplicate JSON member"
        raise ValueError(msg)
    return result


def _constant(_value: str) -> None:
    msg = "Nonstandard JSON constant"
    raise ValueError(msg)
