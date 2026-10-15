# Copyright (c) 2026
# ruff: noqa: ANN401 -- bounded experiment-owned A1 grid
"""State-only exhaustive blind coverage; absence never supplies a negative."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import evidence, schema
from experiments.source_grounding.chunked.cards import EvidenceState
from experiments.source_grounding.response import object_schema

INSTRUCTION = (
    "A1: classify every complete resource for every frozen obligation. "
    "USEFUL: complete content materially bears on satisfying or reasoning about "
    "the obligation. NO_USEFUL: after reviewing complete content, no materially "
    "bearing information identified. UNCERTAIN: cannot confidently determine "
    "material usefulness. Return every source/obligation exactly once, states "
    "only. No rationale, evidence, confidence or final gold labels. Absence is "
    "never a negative. No tools, filesystem or web. Return only schema JSON.\n"
)


def contract(keys: list[str], obligations: list[str]) -> Any:
    """Return resource-oriented finite output with no semantic free text."""
    judgment = object_schema(
        {
            "obligation_id": {"type": "string", "enum": obligations},
            "state": {"type": "string", "enum": [s.value for s in EvidenceState]},
        },
    )
    resource = object_schema(
        {
            "source_key": {"type": "string", "enum": keys},
            "judgments": {
                "type": "array",
                "minItems": len(obligations),
                "maxItems": len(obligations),
                "items": judgment,
            },
        },
    )
    return object_schema(
        {
            "resources": {
                "type": "array",
                "minItems": len(keys),
                "maxItems": len(keys),
                "items": resource,
            },
        },
    )


def render(packet: Any, keys: list[str], table: Any) -> bytes:
    """Disclose only complete raw resources and frozen task/obligations."""
    return INSTRUCTION.encode() + schema.canonical(
        {
            "case": packet["case"],
            "task": packet["task"],
            "obligations": packet["obligations"],
            "resources": [
                {
                    "source_key": k,
                    "address": table[k]["address"],
                    "content": table[k]["content"],
                }
                for k in keys
            ],
        },
    )


@dataclass(frozen=True)
class Coverage:
    """Host-authenticated complete explicit state grid and invocation bindings."""

    canonical: bytes
    grid: dict[tuple[str, str], EvidenceState]

    @property
    def root(self) -> str:
        """Bind complete classification and its original invocation provenance."""
        return digest(self.canonical)

    def authenticate(self, packet: Any) -> None:
        """Reject a mutable caller grid contradicting the exact capture."""
        value = json.loads(self.canonical)
        expected = {
            (k, o["id"])
            for k in evidence.sources(packet)
            for o in packet["obligations"]
        }
        cells = {
            (c["source_key"], c["obligation_id"]): EvidenceState(c["state"])
            for c in value["cells"]
        }
        require(
            value["packet_sha256"] == digest(json_bytes(packet))
            and value["case"] == packet["case"]
            and len(value["cells"]) == len(expected)
            and set(cells) == expected
            and cells == self.grid,
            "A1 coverage capture/grid/input mismatch",
        )


def validate(
    packet: Any,
    responses: tuple[tuple[str, list[str], dict[str, Any]], ...],
) -> Coverage:
    """Reject missing/duplicate/foreign resources or obligations, never infer state."""
    table = evidence.sources(packet)
    obligations = [o["id"] for o in packet["obligations"]]
    require(len(set(obligations)) == len(obligations), "Duplicate frozen obligation")
    grid: dict[tuple[str, str], EvidenceState] = {}
    seen: set[str] = set()
    invocations: set[str] = set()
    records = []
    for invocation, keys, payload in responses:
        require(invocation and invocation not in invocations, "Duplicate A1 invocation")
        require(
            len(set(keys)) == len(keys) and set(keys) <= set(table),
            "A1 batch sources",
        )
        require(not set(keys) & seen, "Duplicate A1 resource across batches")
        invocations.add(invocation)
        schema.validate(payload, contract(keys, obligations))
        batch_seen = set()
        for resource in payload["resources"]:
            key = resource["source_key"]
            require(key not in batch_seen, "Duplicate A1 resource")
            batch_seen.add(key)
            judged = set()
            for cell in resource["judgments"]:
                oid = cell["obligation_id"]
                require(oid not in judged, "Duplicate A1 obligation")
                judged.add(oid)
                grid[key, oid] = EvidenceState(cell["state"])
            require(judged == set(obligations), "Missing A1 obligation")
        require(batch_seen == set(keys), "Missing A1 resource")
        seen.update(batch_seen)
        records.append(
            {
                "invocation": invocation,
                "keys": keys,
                "response_sha256": digest(json_bytes(payload)),
            },
        )
    require(seen == set(table), "Missing A1 resources: no implicit negatives")
    expected = [
        (k, o)
        for k in sorted(table, key=lambda k: table[k]["address"])
        for o in obligations
    ]
    require(set(grid) == set(expected), "Incomplete Cartesian A1 coverage")
    raw = json_bytes(
        {
            "schema": "blind-a1-coverage-v1",
            "case": packet["case"],
            "packet_sha256": digest(json_bytes(packet)),
            "invocations": records,
            "cells": [
                {"source_key": k, "obligation_id": o, "state": grid[k, o].value}
                for k, o in expected
            ],
        },
    )
    return Coverage(raw, grid)
