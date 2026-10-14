# Copyright (c) 2026
# ruff: noqa: ANN401 -- bounded blind-primary packet/response representation
"""Exact-content locators for the two maintained blind-primary packet shapes.

This codec projects representation only. It never repairs semantic judgments.
Occurrences include overlaps, advancing one Unicode code point after each match.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require

CONTRACT = "exact-quote-overlapping-occurrence-v1"
IDENTITY = ("address", "document_identity", "content_identity")


def text(value: Any) -> str:
    """Reject nonstrings and unpaired Unicode surrogates without normalization."""
    require(type(value) is str, "Evidence text must be a Unicode string")
    value.encode("utf-8", errors="strict")
    return str(value)


def sources(packet: Any) -> dict[str, Any]:
    """Assign packet-local content-derived keys, independent of rank/order."""
    require(
        packet["schema"]
        in {"blind-semantic-gold-packet-v1", "source-grounding-packet-v1"},
        "Unsupported evidence packet",
    )
    rows = (
        packet["resources"]
        if "resources" in packet
        else [cell["source"] for cell in packet["cells"]]
    )
    result: dict[str, Any] = {}
    for row in rows:
        identity = {name: text(row[name]) for name in IDENTITY}
        content = text(row["content"])
        key = digest(json_bytes([CONTRACT, packet["case"], packet["frame"], identity]))
        if key in result:
            require(
                result[key] == row,
                "Duplicate source key with inconsistent content",
            )
            require("resources" not in packet, "Duplicate source key")
        result[key] = {**identity, "content": content}
    return result


def source_key(row: Any, table: dict[str, Any]) -> str:
    """Resolve an authenticated packet row without relying on its array position."""
    matches = [key for key, value in table.items() if value == row]
    require(len(matches) == 1, "Source row must have one packet-local identity")
    return matches[0]


def disclosure(packet: Any) -> Any:
    """Disclose original content and address; host retains canonical identities."""
    table = sources(packet)
    projected = deepcopy(packet)

    def row(value: Any) -> Any:
        return {
            "source_key": source_key(value, table),
            "address": value["address"],
            "content": value["content"],
        }

    if "resources" in packet:
        projected["resources"] = [row(value) for value in packet["resources"]]
    else:
        for cell in projected["cells"]:
            cell["source"] = row(cell["source"])
    return projected


def canonical_source(key: Any, table: dict[str, Any]) -> Any:
    """Only disclosed keys can yield canonical source identities."""
    require(type(key) is str and key in table, "Foreign or malformed source key")
    return {name: table[key][name] for name in IDENTITY}


def resolve(locator: Any, table: dict[str, Any]) -> Any:
    """Select the explicit overlapping occurrence and derive exact Unicode bounds."""
    require(
        type(locator) is dict and set(locator) == {"source_key", "quote", "occurrence"},
        "Malformed evidence locator",
    )
    identity = canonical_source(locator["source_key"], table)
    quote = text(locator["quote"])
    require(bool(quote), "Empty evidence quote")
    occurrence = locator["occurrence"]
    require(type(occurrence) is int and occurrence > 0, "Invalid evidence occurrence")
    content = text(table[locator["source_key"]]["content"])
    start = -1
    for _ in range(occurrence):
        start = content.find(quote, start + 1)
        require(start >= 0, "Evidence quote occurrence not found")
    end = start + len(quote)
    require(content[start:end] == quote, "Exact evidence projection mismatch")
    return {"source": identity, "start": start, "end": end, "quote": quote}


def judgments(payload: Any, packet: Any) -> Any:
    """Project all cell and unit-alternative locators, preserving judgments."""
    table = sources(packet)
    result = deepcopy(payload)
    for cell in result["cells"]:
        require("source" not in cell, "Model must not author canonical source identity")
        cell["source"] = canonical_source(cell.pop("source_key"), table)
        cell["spans"] = [resolve(locator, table) for locator in cell["spans"]]
    if "resources" in packet:
        for unit in result["units"]:
            unit["alternatives"] = [
                [resolve(locator, table) for locator in alternative]
                for alternative in unit["alternatives"]
            ]
    return result
