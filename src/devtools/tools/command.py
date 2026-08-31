# Copyright (c) 2026
"""Experimental Tool bridge over direct command execution."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.commands import Command, CommandExecutor, CommandResult


class CommandTool:
    """Execute an existing Command through its supplied CommandExecutor."""

    _NAME = "run_command"
    _DESCRIPTION = "Execute one existing direct command specification."

    def __init__(self, executor: CommandExecutor) -> None:
        """Create a Tool bridge over one CommandExecutor."""
        self._executor = executor

    @property
    def name(self) -> str:
        """Return the stable local capability name."""
        return self._NAME

    @property
    def description(self) -> str:
        """Return the provider-neutral capability description."""
        return self._DESCRIPTION

    def validate(self, arguments: Command) -> None:
        """Admit every already-valid Command specification."""
        del arguments

    async def execute(self, arguments: Command) -> CommandResult:
        """Delegate directly to Commands without changing its semantics."""
        return await self._executor.execute(arguments)
