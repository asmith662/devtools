# Copyright (c) 2026
"""Typed Git inspection over the established managed Commands substrate."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.observability.commands.inspection import CommandInspector
from devtools.observability.commands.models import CommandOrigin, CommandPattern
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.commands.availability import discover_executable
from devtools.tools.errors import ToolInputError

_TIMEOUT = Duration.seconds(15)
_MIN_STATUS_RECORD = 4
_MAX_COMMANDS = 128
_ORIGIN_PREFIX_LIMIT = 96

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath
    from devtools.observability.commands.models import CommandObservation


class GitInspectionError(ValueError):
    """Git did not provide a complete supported repository observation."""


def _text(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeError as error:
        msg = "Git inspection text encoding is unsupported."
        raise GitInspectionError(msg) from error


@dataclass(frozen=True, slots=True)
class GitChange:
    """Exact root-relative UTF-8 path with separate index and worktree status."""

    path: str
    index: str
    worktree: str
    original_path: str | None = None

    @property
    def untracked(self) -> bool:
        """Distinguish a new untracked entry from staged/unstaged tracked changes."""
        return self.index == self.worktree == "?"

    @property
    def unmerged(self) -> bool:
        """Retain explicit index conflicts rather than silently validating them."""
        return self.index + self.worktree in {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def parse_porcelain(data: bytes) -> tuple[GitChange, ...]:
    """Parse porcelain-v1 -z, including reversed NUL-delimited rename paths.

    Paths are literal, never English/quoted display text. Unsupported non-UTF8
    names and malformed/truncated output refuse rather than drop a change.
    """
    if not data:
        return ()
    if not data.endswith(b"\0"):
        msg = "Git status framing is incomplete."
        raise GitInspectionError(msg)
    try:
        fields = iter(data[:-1].decode("utf-8").split("\x00"))
        result = []
        seen = set()
        for record in fields:
            if (
                len(record) < _MIN_STATUS_RECORD
                or record[2] != " "
                or record[:2] == "  "
                or any(c not in " MADRCTU?!" for c in record[:2])
                or ("?" in record[:2] and record[:2] != "??")
                or ("!" in record[:2] and record[:2] != "!!")
            ):
                msg = "Git status record is malformed."
                raise GitInspectionError(msg)
            path = record[3:]
            original = next(fields) if "R" in record[:2] or "C" in record[:2] else None
            if not path or original == "" or path in seen:
                msg = "Git status paths are incomplete or duplicated."
                raise GitInspectionError(msg)
            seen.add(path)
            result.append(GitChange(path, record[0], record[1], original))
        return tuple(result)
    except (UnicodeDecodeError, StopIteration) as error:
        msg = "Git status encoding or rename framing is unsupported."
        raise GitInspectionError(msg) from error


@dataclass(frozen=True, slots=True)
class GitInspection:
    """Rechecked Git observation, not an atomic snapshot or source-content digest."""

    root: ResolvedPath
    revision: str
    changes: tuple[GitChange, ...]
    stable: bool


class GitInspectionTool:
    """Inspect only the host-selected exact root, without index/worktree mutation."""

    name = "inspect_repository"
    description = (
        "Inspect current revision and literal staged/unstaged/untracked paths."
    )

    def __init__(
        self,
        root: ResolvedPath,
        *,
        origin: CommandOrigin,
        timeout: Duration = _TIMEOUT,
        maximum_bytes: int = 1 << 20,
    ) -> None:
        """Bind root, caller provenance and finite command/output limits."""
        if (
            timeout.total_seconds <= 0
            or maximum_bytes < 1
            or len(origin.call) > _ORIGIN_PREFIX_LIMIT
        ):
            msg = "Git inspection requires positive time and output limits."
            raise ValueError(msg)
        self.root, self.origin, self.timeout = root, origin, timeout
        self.executor = CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=maximum_bytes,
                max_stderr_bytes=2048,
            ),
        )
        self.observations: list[CommandObservation] = []

    def validate(self, arguments: None) -> None:
        """Refuse model-selected roots/argv and changed canonical working roots."""
        if (
            arguments is not None
            or resolve_path(self.root.value) != self.root
            or not self.root.value.is_dir()
        ):
            msg = "Git inspection requires the admitted existing canonical root."
            raise ToolInputError(msg)

    async def _git(self, operation: str, *arguments: str) -> bytes:
        if len(self.observations) >= _MAX_COMMANDS:
            msg = "Git inspection observation bound exceeded."
            raise GitInspectionError(msg)
        capability = discover_executable("git")
        if capability.path is None:
            msg = "Git executable is unavailable."
            raise GitInspectionError(msg)
        index = len(self.observations)
        origin = CommandOrigin(
            self.origin.agent,
            self.origin.task,
            self.origin.run,
            self.origin.call + "/git-" + str(index),
        )
        inspector = CommandInspector(
            origin,
            CommandPattern(
                "git",
                operation,
                tuple("flag" for _ in arguments),
                (capability.platform, "git"),
                "tools.repository.GitInspectionTool",
            ),
        )
        try:
            result = await inspector.observe(
                self.executor.start(
                    Command(str(capability.path))
                    .args("--no-optional-locks", *arguments)
                    .cwd(self.root)
                    .with_timeout(self.timeout),
                ),
            )
        finally:
            self.observations.append(inspector.observation)
        if result.failed or result.stdout_truncated or result.stderr_truncated:
            msg = "Git inspection command failed or its output was truncated."
            raise GitInspectionError(msg)
        return result.stdout

    async def execute(self, arguments: None) -> GitInspection:
        """Authenticate root/HEAD and recheck state; no retry on an unknown effect."""
        del arguments
        root = (
            _text(await self._git("root", "rev-parse", "--show-toplevel"))
            .removesuffix("\n")
            .removesuffix("\r")
        )
        if not Path(root).is_absolute() or resolve_path(root) != self.root:
            msg = "Git reports a different repository root."
            raise GitInspectionError(msg)
        before = await self._git("revision", "rev-parse", "--verify", "HEAD")
        revision = _text(before.strip())
        if not re.fullmatch("(?:[0-9a-f]{40}|[0-9a-f]{64})", revision):
            msg = "Git revision is not a supported object identity."
            raise GitInspectionError(msg)
        argv = (
            "status",
            "--porcelain=v1",
            "-z",
            "--no-renames",
            "--untracked-files=all",
            "--ignore-submodules=none",
        )
        first = await self._git("status", *argv)
        changes = parse_porcelain(first)
        after = await self._git("revision", "rev-parse", "--verify", "HEAD")
        second = await self._git("status", *argv)
        parse_porcelain(second)
        return GitInspection(
            self.root,
            revision,
            changes,
            before == after and first == second,
        )
