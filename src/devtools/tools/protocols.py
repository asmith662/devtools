# Copyright (c) 2026
"""Structural protocols for experimental Tool execution."""

from __future__ import annotations

from typing import Protocol


class Tool[ArgsT, ResultT](Protocol):
    """Describe one named asynchronous capability with semantic input admission."""

    @property
    def name(self) -> str:
        """Return this Tool's nonblank local capability name."""

    @property
    def description(self) -> str:
        """Return a provider-neutral description of this Tool's applicability."""

    def validate(self, arguments: ArgsT) -> None:
        """Reject unsupported semantic input before execution begins."""

    async def execute(self, arguments: ArgsT) -> ResultT:
        """Execute admitted input and return the Tool-defined result."""
