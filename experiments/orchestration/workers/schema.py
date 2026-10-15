# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0911 -- bounded JSON vocabulary with one branch per type
"""Validate bounded responses and prove their canonical UTF-8 size envelopes."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from experiments.orchestration.storage import require

MAX_SEMANTIC_RESPONSE_UTF8_BYTES = 65536
MAX_NATIVE_SCHEMA_UTF8_BYTES = 262144
AGGREGATE = "x-aggregate-characters"
KEYWORDS = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "enum",
    "maxLength",
    "minLength",
    "maxItems",
    "minItems",
    "minimum",
    "maximum",
    "pattern",
    AGGREGATE,
}
ASCII_PATTERNS = {
    "^[A-Z0-9]+$": "A",
    "^[ce][0-9]+$": "e",
    "^O[0-9]+$": "O",
    "^U[0-9]+$": "U",
}


def canonical(value: Any) -> bytes:
    """Use exact Unicode, sorted keys and minified JSON without a trailing newline."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8", errors="strict")


def native(value: Any) -> Any:
    """Remove only the host's explicit aggregate cross-field assertion."""
    if isinstance(value, dict):
        return {key: native(child) for key, child in value.items() if key != AGGREGATE}
    if isinstance(value, list):
        return [native(child) for child in value]
    return value


def validate(value: Any, contract: dict[str, Any]) -> None:
    """Validate the supported native subset plus the host aggregate quote bound."""
    require(set(contract) <= KEYWORDS, "Unsupported semantic response schema")
    kind = contract["type"]
    types = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
    }
    require(kind in types and type(value) is types[kind], "Semantic schema type")
    if "enum" in contract:
        require(value in contract["enum"], "Semantic schema enum")
    if kind == "object":
        require(
            contract["additionalProperties"] is False
            and set(value) == set(contract["required"]) == set(contract["properties"]),
            "Semantic response object fields",
        )
        for name, child in contract["properties"].items():
            validate(value[name], child)
    elif kind == "array":
        require(
            contract.get("minItems", 0)
            <= len(value)
            <= contract.get("maxItems", len(value)),
            "Semantic array cardinality",
        )
        for item in value:
            validate(item, contract["items"])
        if AGGREGATE in contract:
            bound = contract[AGGREGATE]
            require(
                sum(len(item[bound["property"]]) for item in value) <= bound["maximum"],
                "Aggregate quote character limit",
            )
    elif kind == "string":
        value.encode("utf-8", errors="strict")
        require(
            contract.get("minLength", 0)
            <= len(value)
            <= contract.get("maxLength", len(value)),
            "Semantic string length",
        )
        if "pattern" in contract:
            require(
                re.fullmatch(contract["pattern"], value) is not None,
                "Semantic string pattern",
            )
    elif kind == "integer":
        require(
            contract.get("minimum", value) <= value <= contract.get("maximum", value),
            "Semantic integer bounds",
        )


def maximum(contract: dict[str, Any], *, bytes_measure: bool) -> Any:
    """Construct a witness attaining the proven maximum for the bounded subset.

    Every unrestricted Unicode scalar takes at most six canonical JSON bytes
    (control escapes); U+0000 attains six in both character and byte measures.
    The aggregate assertion is part of the host-valid response contract, not a
    claim that native JSON Schema can express a sum of string lengths.
    """
    require(set(contract) <= KEYWORDS, "Unsupported envelope schema")
    if "enum" in contract:

        def size(value: Any) -> int:
            raw = canonical(value)
            return len(raw) if bytes_measure else len(raw.decode())

        return max(contract["enum"], key=size)
    kind = contract["type"]
    if kind == "boolean":
        return False
    if kind == "integer":
        low, high = contract["minimum"], contract["maximum"]
        require(
            type(low) is int and type(high) is int and low <= high,
            "Finite integer bounds",
        )
        return max((low, high), key=lambda number: len(str(number)))
    if kind == "string":
        length = contract["maxLength"]
        require(
            type(length) is int and length >= contract.get("minLength", 0),
            "Finite string bound",
        )
        pattern = contract.get("pattern")
        if pattern:
            require(pattern in ASCII_PATTERNS, "Unproved envelope pattern")
            prefix = ASCII_PATTERNS[pattern]
            return prefix + ("0" if prefix != "A" else "A") * (length - 1)
        return "\0" * length
    if kind == "object":
        require(
            contract["additionalProperties"] is False
            and set(contract["required"]) == set(contract["properties"]),
            "Closed envelope object required",
        )
        return {
            key: maximum(child, bytes_measure=bytes_measure)
            for key, child in contract["properties"].items()
        }
    require(kind == "array", "Unsupported envelope type")
    count = contract["maxItems"]
    require(
        type(count) is int and count >= contract.get("minItems", 0),
        "Finite array bound",
    )
    result = [
        maximum(contract["items"], bytes_measure=bytes_measure) for _ in range(count)
    ]
    if AGGREGATE in contract and count:
        bound = contract[AGGREGATE]
        prop = bound["property"]
        string = contract["items"]["properties"][prop]
        require(
            string["type"] == "string"
            and set(string) <= {"type", "maxLength", "minLength"},
            "Aggregate plain-string property",
        )
        minimum = string.get("minLength", 0)
        remaining = min(bound["maximum"], count * string["maxLength"])
        require(remaining >= count * minimum, "Unsatisfiable aggregate bound")
        for index, item in enumerate(result):
            length = min(string["maxLength"], remaining - (count - index - 1) * minimum)
            item[prop] = "\0" * length
            remaining -= length
    return result


@dataclass(frozen=True)
class Envelope:
    """Exact maxima for host-valid responses in the supported bounded contract."""

    characters: int
    utf8_bytes: int


def envelope(contract: dict[str, Any]) -> Envelope:
    """Require constructive maximum witnesses to satisfy the full host contract."""
    chars = maximum(contract, bytes_measure=False)
    byte_value = maximum(contract, bytes_measure=True)
    validate(chars, contract)
    validate(byte_value, contract)
    return Envelope(len(canonical(chars).decode()), len(canonical(byte_value)))
