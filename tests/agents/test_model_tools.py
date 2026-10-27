# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- literal composition contract controls
"""Host selection/admission and one existing ToolRunner execution, independently."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

import pytest

from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.models.interaction import ModelToolCall
from devtools.tools import ToolDescriptor, ToolRunner

if TYPE_CHECKING:
    from collections.abc import Awaitable

DESCRIPTOR = ToolDescriptor("read_exact", "Read one integer.", "{}")


@dataclass
class Invocation:
    """A host-selected typed materializer, independent of any application."""

    events: list[str]
    descriptor: ToolDescriptor = DESCRIPTOR
    error: BaseException | None = None

    def materialize(self, serialized_arguments: str) -> int:
        """Accept the literal host fixture, not arbitrary executable input."""
        self.events.append("materialize")
        if self.error is not None:
            raise self.error
        assert serialized_arguments == '{"value":7}'
        return 7


@dataclass
class SelectedTool:
    """An ordinary Tool with a name distinct from its selected operation."""

    events: list[str]
    name = "multiplexed_read_capability"
    description = "Host-owned capability."
    result: object = None
    error: BaseException | None = None
    validation_error: BaseException | None = None

    def validate(self, arguments: int) -> None:
        """Semantic validation is ToolRunner's job, not authority."""
        self.events.append("validate")
        assert arguments == 7
        if self.validation_error is not None:
            raise self.validation_error

    async def execute(self, arguments: int) -> object:
        """Record entry before a possibly lost result; never retry."""
        self.events.append("execute")
        assert arguments == 7
        if self.error is not None:
            raise self.error
        return self.result


def test_selected_operation_admission_order_and_result_identity() -> None:
    events: list[str] = []
    result = object()
    call = ModelToolCall("read_exact", '{"value":7}', "native-1")

    async def admit(selected: ModelToolCall, value: int) -> None:
        assert selected is call
        assert value == 7
        events.append("admit")

    actual = asyncio.run(
        execute_model_tool_call(
            call,
            invocation=Invocation(events),
            tool=SelectedTool(events, result=result),
            admit=admit,
            runner=ToolRunner(),
        ),
    )
    assert actual is result
    assert events == ["materialize", "admit", "validate", "execute"]


def test_conflicting_native_operation_refused_before_materialization() -> None:
    events: list[str] = []

    async def admit(_call: ModelToolCall, _value: int) -> None:
        pytest.fail("Conflicting native operation reached admission")

    with pytest.raises(ValueError, match="host-selected invocation"):
        asyncio.run(
            execute_model_tool_call(
                ModelToolCall("unselected", '{"value":7}', "native-1"),
                invocation=Invocation(events),
                tool=SelectedTool(events),
                admit=admit,
                runner=ToolRunner(),
            ),
        )
    assert events == []


@pytest.mark.parametrize("stage", ["materialize", "admit", "validate", "execute"])
@pytest.mark.parametrize("cancel", [False, True])
def test_original_failure_or_cancellation_and_effect_entry_survive(
    stage: str,
    *,
    cancel: bool,
) -> None:
    events: list[str] = []
    error = asyncio.CancelledError("cancel") if cancel else OSError("lost result")
    invocation = Invocation(events, error=error if stage == "materialize" else None)
    tool = SelectedTool(
        events,
        error=error if stage == "execute" else None,
        validation_error=error if stage == "validate" else None,
    )

    async def admit(_call: ModelToolCall, _value: int) -> None:
        events.append("admit")
        if stage == "admit":
            raise error

    with pytest.raises(type(error)) as raised:
        asyncio.run(
            execute_model_tool_call(
                ModelToolCall("read_exact", '{"value":7}', "native-1"),
                invocation=invocation,
                tool=tool,
                admit=admit,
                runner=ToolRunner(),
            ),
        )
    assert raised.value is error
    order = ["materialize", "admit", "validate", "execute"]
    assert events == order[: order.index(stage) + 1]


def test_admission_is_required_and_not_a_synchronous_permission_boolean() -> None:
    events: list[str] = []

    def broken_admission(_call: ModelToolCall, _value: int) -> Awaitable[None]:
        return cast("Awaitable[None]", object())

    with pytest.raises(TypeError, match="await"):
        asyncio.run(
            execute_model_tool_call(
                ModelToolCall("read_exact", '{"value":7}', "native-1"),
                invocation=Invocation(events),
                tool=SelectedTool(events),
                admit=broken_admission,
                runner=ToolRunner(),
            ),
        )
    assert events == ["materialize"]


def test_descriptor_projection_uses_existing_immutable_model_value() -> None:
    descriptor = ToolDescriptor("read_exact", "Literal source.", '{"z":1,"a":2}')
    actual = normalize_tool_descriptor(descriptor)
    assert (actual.name, actual.description, actual.input_schema_json) == (
        "read_exact",
        "Literal source.",
        '{"a":2,"z":1}',
    )
    assert not hasattr(actual, "tool")


@pytest.mark.parametrize(
    ("schema", "error"),
    [("{", ValueError), ("[]", TypeError)],
)
def test_projection_defensively_refuses_broken_external_descriptor(
    schema: str,
    error: type[Exception],
) -> None:
    descriptor = object.__new__(ToolDescriptor)
    object.__setattr__(descriptor, "input_schema_json", schema)
    with pytest.raises(error, match="Tool descriptor input schema"):
        normalize_tool_descriptor(descriptor)
