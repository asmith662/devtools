# Copyright (c) 2026
# ruff: noqa: D103 -- actual native composition and host admission
"""Any native host can select the procedure through the existing Agents seam."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

import pytest

from devtools.agents.model_tools import execute_model_tool_call
from devtools.models.interaction import ModelToolCall, Prompt, PromptMessage
from devtools.tools import ToolDescriptor, ToolRunner
from tests.tools.repository.fixtures import procedure, repository

if TYPE_CHECKING:
    from pathlib import Path


class Invocation:
    """One host-selected operation, no command registry or model-selected argv."""

    descriptor = ToolDescriptor(
        "validate_change",
        "Run the selected host procedure.",
        '{"type":"object","maxProperties":0}',
    )

    def materialize(self, arguments: str) -> None:
        """Accept only the already selected empty argument object."""
        if json.loads(arguments) != {}:
            msg = "Procedure scope and commands are host selected."
            raise ValueError(msg)


@pytest.mark.parametrize("authorized", [False, True])
def test_native_host_preserves_admission_and_feedback(
    tmp_path: Path,
    *,
    authorized: bool,
) -> None:
    async def run() -> None:
        revision, scope = await repository(tmp_path)
        tool = procedure(tmp_path, revision, scope)
        call = ModelToolCall("validate_change", "{}", "native-1")
        admitted = []

        async def admit(selected: ModelToolCall, arguments: None) -> None:
            assert selected is call
            assert arguments is None
            if not authorized:
                msg = "Host did not authorize this procedure"
                raise PermissionError(msg)
            admitted.append(selected.provider_call_id)

        operation = execute_model_tool_call(
            call,
            invocation=Invocation(),
            tool=tool,
            admit=admit,
            runner=ToolRunner(),
        )
        if not authorized:
            with pytest.raises(PermissionError, match="authorize"):
                await operation
            assert tool.inspection.observations == []
            assert not (tmp_path / ".local/count").exists()
            return
        result = await operation
        assert result.status == "passed"
        assert admitted == ["native-1"]
        prompt = Prompt(
            "",
            "messages",
            (
                PromptMessage("assistant", "", (call,)),
                PromptMessage(
                    "tool",
                    json.dumps({"status": result.status}),
                    tool_call_id=call.provider_call_id,
                ),
            ),
        )
        assert prompt.messages[-1].tool_call_id == "native-1"
        assert (tmp_path / ".local/count").read_text() == "x"

    asyncio.run(run())
