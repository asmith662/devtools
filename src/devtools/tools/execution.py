# Copyright (c) 2026
"""Standard experimental Tool execution boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.tools.protocols import Tool


class ToolRunner:
    """Validate and execute one Tool without altering its result or failures."""

    async def execute[ArgsT, ResultT](
        self,
        tool: Tool[ArgsT, ResultT],
        arguments: ArgsT,
    ) -> ResultT:
        """Validate semantic input, then execute the selected Tool once."""
        tool.validate(arguments)
        return await tool.execute(arguments)
