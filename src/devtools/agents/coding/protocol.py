# Copyright (c) 2026
"""Native coding disclosure/materialization; no host state, authority or effects."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, cast

from devtools.agents.coding.navigation import FIND, READ_UNIT, unit_read_request
from devtools.tools import ToolDescriptor
from devtools.tools.source import SourceReadRequest

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.context.retrieval.source.index import SourceSearchIndex
    from devtools.models.interaction import ModelToolCall

READ = ToolDescriptor(
    "read_source",
    "Read half-open Unicode offsets; omit end for a byte-bounded remaining prefix.",
    (
        '{"type":"object","properties":{"path":{"type":"string"},'
        '"start":{"type":"integer"},"end":{"type":"integer"}},'
        '"required":["path","start"],"additionalProperties":'
        "false}"
    ),
)
EDIT = ToolDescriptor(
    "replace_source",
    ("Propose an exact unique observed replacement; host admission is required."),
    (
        '{"type":"object","properties":{"path":{"type":"string"},'
        '"old_text":{"type":"string"},"new_text":{"type":"string"}},'
        '"required":["path","old_text","new_text"],'
        '"additionalProperties":false}'
    ),
)
CHECK = ToolDescriptor(
    "validate_candidate",
    "Request the host-fixed candidate checks.",
    '{"type":"object","maxProperties":0}',
)


@dataclass(frozen=True, slots=True)
class Invocation[Input]:
    """One explicitly selected native operation, not a Tool registry."""

    descriptor: ToolDescriptor
    decode: Callable[[str], Input]

    def materialize(self, serialized_arguments: str) -> Input:
        """Delegate effect-free materialization to the selected host operation."""
        return self.decode(serialized_arguments)


def arguments(
    serialized: str,
    fields: set[str],
    *,
    optional: frozenset[str] = frozenset(),
) -> dict[str, object]:
    """Validate this host's small native argument object, not arbitrary JSON Schema."""

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        value = dict(items)
        if len(value) != len(items):
            msg = "Duplicate coding argument member."
            raise ValueError(msg)
        return value

    value = json.loads(serialized, object_pairs_hook=pairs)
    if not isinstance(value, dict) or not fields <= set(value) <= fields | optional:
        msg = "Coding arguments do not match the admitted operation."
        raise ValueError(msg)
    return value


def classify_calls(
    calls: tuple[ModelToolCall, ...],
    *,
    navigation: bool,
) -> Literal["acquire", "edit", "stop"]:
    """Classify the whole batch before dispatch; availability is not authority."""
    if not calls:
        return "stop"
    if all(
        c.name in {READ.name, CHECK.name}
        or (navigation and c.name in {FIND.name, READ_UNIT.name})
        for c in calls
    ):
        return "acquire"
    if all(c.name == EDIT.name for c in calls):
        return "edit"
    msg = "Coding response contains an unadmitted or mixed operation."
    raise ValueError(msg)


def read_request(
    serialized: str,
    *,
    index: SourceSearchIndex,
    purpose: str,
    maximum_bytes: int,
    by_unit: bool,
) -> SourceReadRequest:
    """Bind candidate arguments to the selected index; Tools still validate scope."""
    if by_unit:
        return unit_read_request(
            index,
            arguments(serialized, {"unit_id", "snapshot_id"}),
            purpose=purpose,
            maximum_bytes=maximum_bytes,
        )
    values = arguments(serialized, {"path", "start"}, optional=frozenset({"end"}))
    unit = next(
        (u for u in index.views[0].units if u.resource.address.value == values["path"]),
        None,
    )
    if unit is None:
        msg = "Source path is outside the admitted corpus."
        raise ValueError(msg)
    return SourceReadRequest(
        purpose,
        unit,
        cast("int", values["start"]),
        cast("int | None", values.get("end", unit.end)),
        maximum_bytes,
    )
