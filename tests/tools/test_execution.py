# Copyright (c) 2026
"""Tests for the experimental provider-neutral Tool execution boundary."""

from __future__ import annotations

import asyncio

import pytest

from devtools.tools import Tool, ToolInputError, ToolRunner


class _SemanticTool:
    """Record semantic admission and execution for one integer capability."""

    name = "double"
    description = "Double one non-negative integer."

    def __init__(self) -> None:
        """Create an empty recording Tool."""
        self.executed: list[int] = []
        self.validated: list[int] = []

    def validate(self, arguments: int) -> None:
        """Reject negative values before execution."""
        self.validated.append(arguments)
        if arguments < 0:
            msg = "Negative integers are unsupported."
            raise ToolInputError(msg)

    async def execute(self, arguments: int) -> str:
        """Record and render one admitted integer."""
        self.executed.append(arguments)
        return str(arguments * 2)


class _FailingTool:
    """Raise one unchanged ordinary execution failure."""

    name = "failing"
    description = "Raise one domain failure."

    def __init__(self, error: LookupError) -> None:
        """Store the exact domain failure to raise."""
        self._error = error

    def validate(self, arguments: str) -> None:
        """Admit every string for this failure probe."""
        del arguments

    async def execute(self, arguments: str) -> str:
        """Raise the configured ordinary execution error."""
        del arguments
        raise self._error


class _CancelledTool:
    """Raise one unchanged cancellation from execution."""

    name = "cancelled"
    description = "Raise one cancellation."

    def __init__(self, error: asyncio.CancelledError) -> None:
        """Store the exact cancellation to raise."""
        self._error = error

    def validate(self, arguments: None) -> None:
        """Admit the cancellation probe input."""
        del arguments

    async def execute(self, arguments: None) -> None:
        """Raise the original cancellation instance."""
        del arguments
        raise self._error


def test_runner_preserves_typed_result_after_semantic_admission() -> None:
    """ToolRunner preserves the Tool argument/result relationship."""

    async def exercise() -> None:
        tool = _SemanticTool()
        typed_tool: Tool[int, str] = tool
        result: str = await ToolRunner().execute(typed_tool, 3)

        assert result == "6"
        assert tool.validated == [3]
        assert tool.executed == [3]

    asyncio.run(exercise())


def test_runner_rejects_semantic_input_before_execution() -> None:
    """A ToolInputError leaves the Tool execution boundary unentered."""

    async def exercise() -> None:
        tool = _SemanticTool()

        with pytest.raises(ToolInputError, match="Negative"):
            await ToolRunner().execute(tool, -1)

        assert tool.validated == [-1]
        assert tool.executed == []

    asyncio.run(exercise())


def test_runner_propagates_ordinary_execution_errors_unchanged() -> None:
    """ToolRunner does not replace a Tool-owned ordinary failure."""

    async def exercise() -> None:
        message = "tool execution failed"
        error = LookupError(message)

        with pytest.raises(LookupError) as raised:
            await ToolRunner().execute(_FailingTool(error), "input")

        assert raised.value is error

    asyncio.run(exercise())


def test_runner_propagates_cancellation_unchanged() -> None:
    """ToolRunner leaves Tool cancellation under ordinary Python semantics."""

    async def exercise() -> None:
        message = "tool cancelled"
        error = asyncio.CancelledError(message)

        with pytest.raises(asyncio.CancelledError, match="tool cancelled"):
            await ToolRunner().execute(_CancelledTool(error), None)

    asyncio.run(exercise())


def test_repeated_runner_calls_are_independent() -> None:
    """Repeated execution neither deduplicates nor retries Tool calls."""

    async def exercise() -> None:
        runner = ToolRunner()
        tool = _SemanticTool()

        assert await runner.execute(tool, 2) == "4"
        assert await runner.execute(tool, 2) == "4"
        assert tool.executed == [2, 2]

    asyncio.run(exercise())
