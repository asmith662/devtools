# Copyright (c) 2026
"""Immutable host-selected checks over the existing managed Command substrate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.core.paths import resolve_path
from devtools.resources.commands import CommandExecutor, CommandOutputPolicy
from devtools.tools.errors import ToolInputError

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath
    from devtools.resources.commands import Command, CommandResult
    from devtools.tools.source import SourceScope

_OUTPUT_POLICY = CommandOutputPolicy()


@dataclass(frozen=True, slots=True)
class FixedCheck:
    """One named host-owned argv, cwd, timeout and success policy."""

    name: str
    command: Command


@dataclass(frozen=True, slots=True)
class FixedCheckPlan:
    """A bounded ordered selection; no model input can change its Commands.

    Optional source scope attests only those declared text resources, not a
    universal dependency/toolchain closure. With no scope, command exit/output
    is the entire claim; the host must supply any stronger admission contract.
    """

    root: ResolvedPath
    checks: tuple[FixedCheck, ...]
    source_scope: SourceScope | None = None
    output_policy: CommandOutputPolicy = _OUTPUT_POLICY

    def __post_init__(self) -> None:
        """Refuse mutable, ambiguous, unbounded or foreign working plans."""
        if (
            not isinstance(self.checks, tuple)
            or not self.checks
            or len({check.name for check in self.checks}) != len(self.checks)
            or any(not check.name.strip() for check in self.checks)
            or (self.source_scope is not None and self.source_scope.root != self.root)
        ):
            msg = "Fixed check plan requires distinct names and matching host scope."
            raise ValueError(msg)
        for check in self.checks:
            command = check.command
            if (
                command.working_directory is None
                or not command.working_directory.value.is_relative_to(self.root.value)
                or command.timeout is None
                or command.timeout.total_seconds <= 0
            ):
                msg = "Fixed checks require scoped working directories and timeouts."
                raise ValueError(msg)

    def select(self, name: str) -> FixedCheck:
        """Resolve only a host-fixed name, never model-supplied executable input."""
        for check in self.checks:
            if check.name == name:
                return check
        msg = "Check is not in the host-admitted plan."
        raise ToolInputError(msg)


@dataclass(frozen=True, slots=True)
class FixedCheckResult:
    """Retain known execution even if post-execution source checking fails."""

    check: FixedCheck
    command_result: CommandResult
    inputs_current: bool | None
    input_error: Exception | None = None

    @property
    def passed(self) -> bool:
        """Report only this declared check, never candidate/protected acceptance."""
        return (
            self.command_result.succeeded
            and not self.command_result.stdout_truncated
            and not self.command_result.stderr_truncated
            and self.inputs_current is not False
        )


class FixedCheckTool:
    """Run one admitted name once; exceptions/cancellation never imply no effect."""

    name = "run_fixed_check"
    description = "Execute one immutable host-selected bounded check."

    def __init__(self, plan: FixedCheckPlan) -> None:
        """Bind the immutable plan and canonical executor output policy."""
        self.plan = plan
        self.executor = CommandExecutor(output_policy=plan.output_policy)

    def validate(self, arguments: str) -> None:
        """Check selection and declared input correspondence before entry."""
        check = self.plan.select(arguments)
        cwd = check.command.working_directory
        if (
            resolve_path(self.plan.root.value) != self.plan.root
            or cwd is None
            or resolve_path(cwd.value) != cwd
        ):
            msg = "Fixed check working scope changed."
            raise ToolInputError(msg)
        if self.plan.source_scope is not None:
            self.plan.source_scope.check_current()

    async def execute(self, arguments: str) -> FixedCheckResult:
        """Delegate once and preserve known results or the original exception."""
        check = self.plan.select(arguments)
        result = await self.executor.execute(check.command)
        current: bool | None = None
        error: Exception | None = None
        if self.plan.source_scope is not None:
            try:
                self.plan.source_scope.check_current()
                current = True
            except Exception as failure:  # noqa: BLE001 -- retain completed Command plus original secondary failure
                current, error = False, failure
        return FixedCheckResult(check, result, current, error)
