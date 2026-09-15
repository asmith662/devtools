# Copyright (c) 2026
"""Tests for normalized model-facing Tool values."""

from dataclasses import FrozenInstanceError

import pytest

from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    ModelToolDefinition,
    Prompt,
)
from devtools.tools import ToolDescriptor
from experiments.qwen.model_tool_composition import normalize_tool_descriptor

_SCHEMA = (
    '{"type":"object","properties":{"path":{"type":"string"}},'
    '"required":["path"]}'
)


def test_descriptor_and_definition_are_immutable_disclosure_values() -> None:
    """A model disclosure contains only name, description, and JSON Schema."""
    descriptor = ToolDescriptor("read_repository_file", "Read one file.", _SCHEMA)
    definition = normalize_tool_descriptor(descriptor)
    assert descriptor.input_schema_json == definition.input_schema_json
    assert "root" not in descriptor.input_schema_json
    with pytest.raises(FrozenInstanceError):
        definition.name = "other"  # type: ignore[misc]


def test_descriptor_normalization_is_a_real_composition_boundary() -> None:
    """Descriptor text crosses into a separately owned normalized model value."""
    descriptor = ToolDescriptor(
        "read_repository_file",
        "Read one file.",
        '{"properties":{"path":{"type":"string"}},"type":"object"}',
    )
    definition = normalize_tool_descriptor(descriptor)
    assert definition.name == descriptor.name
    assert definition.description == descriptor.description
    assert definition.input_schema_json == (
        '{"properties":{"path":{"type":"string"}},"type":"object"}'
    )
    assert not hasattr(definition, "tool")
    assert not hasattr(definition, "runner")


def test_model_tool_call_preserves_untrusted_json_without_tool_admission() -> None:
    """A requested invocation is valid model output, not executable Tool input."""
    call = ModelToolCall(
        name="read_repository_file",
        arguments_json='{"path":"src/labels.py"}',
        provider_call_id="call-1",
    )
    assert call.arguments_json == '{"path":"src/labels.py"}'
    assert call.provider_call_id == "call-1"


def test_request_and_response_reject_invalid_or_duplicate_tool_collections() -> None:
    """Tool collections are immutable normalized model values, not arbitrary lists."""
    tool = ModelToolDefinition("read", "Read.", "{}")
    with pytest.raises(TypeError, match="tuple"):
        ModelRequest(Prompt("x", "user"), tools=[tool])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unique"):
        ModelRequest(Prompt("x", "user"), tools=(tool, tool))
    with pytest.raises(TypeError, match="tuple"):
        ModelResponse("x", InteractionSource("model"), tool_calls=[()])  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("factory", "match"),
    [
        (lambda: ToolDescriptor(" ", "x", "{}"), "name"),
        (lambda: ToolDescriptor("x", " ", "{}"), "description"),
        (lambda: ToolDescriptor("x", "x", "[]"), "object"),
        (lambda: ToolDescriptor("x", "x", "bad"), "valid JSON"),
        (lambda: ModelToolDefinition("x", "x", "not-json"), "valid JSON"),
        (lambda: ModelToolDefinition(" ", "x", "{}"), "name"),
        (lambda: ModelToolDefinition("x", " ", "{}"), "description"),
        (lambda: ModelToolDefinition("x", "x", "[]"), "object"),
        (lambda: ModelToolCall("x", "[]"), "object"),
        (lambda: ModelToolCall("x", "not-json"), "valid JSON"),
        (lambda: ModelToolCall(" ", "{}"), "name"),
        (lambda: ModelToolCall("x", "{}", " "), "ID"),
    ],
)
def test_tool_values_reject_malformed_disclosure_or_call_data(
    factory: object,
    match: str,
) -> None:
    """No malformed provider or disclosure value is silently normalized."""
    with pytest.raises((TypeError, ValueError), match=match):
        factory()  # type: ignore[operator]
