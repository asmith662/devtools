# Copyright (c) 2026
# ruff: noqa: ANN401 -- deterministic blind resource/output-aware partition
"""Pack canonical parent resources without retrieval, judgments or treatment state."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import evidence
from experiments.orchestration.workers.capacity import INPUT_BYTES, INPUT_CHARACTERS
from experiments.orchestration.workers.schema import (
    MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
    canonical,
    envelope,
)
from experiments.source_grounding.chunked import classification
from experiments.source_grounding.chunked.cards import EvidenceState
from experiments.source_grounding.chunked.response import pass_a2

INSTRUCTIONS = (
    "A2: review only the disclosed A1 USEFUL/UNCERTAIN cells. Complete resource "
    "content is disclosed once with all eligible obligations. USEFUL requires "
    "EVIDENCE_FOUND, complete representation and valid own-source evidence. "
    "UNCERTAIN may resolve to EVIDENCE_FOUND or REMAINS_UNCERTAIN; never silently "
    "convert uncertainty to a negative or reconsider another resource. "
    "Give the minimum locally sufficient exact evidence: source_key, exact quote, "
    "positive overlapping occurrence. Do not author offsets or canonical identity. "
    "semantic_statement <=512 Unicode characters; <=4 locators; aggregate quote "
    "text <=4096 "
    "Unicode characters per cell; uncertainty_note <=256. Never truncate, normalize "
    "or change a state to fit. If adequate representation is impossible set "
    "representation_complete=false. Do not assign final gold labels or global "
    "necessity. Audit exact quote/occurrence copying, states and all cells in "
    "self_review (<=256 characters). All authorized information is supplied; "
    "use no tools, filesystem or web; write no files. Return only schema JSON.\n"
)


def render(
    packet: Any,
    keys: list[str],
    table: Any,
    coverage: classification.Coverage | None = None,
) -> bytes:
    """Disclose complete source content exactly once, with no treatment metadata."""
    if coverage is None:
        return classification.render(packet, keys, table)
    return INSTRUCTIONS.encode() + canonical(
        {
            "case": packet["case"],
            "task": packet["task"],
            "resources": [
                {
                    "source_key": key,
                    "address": table[key]["address"],
                    "content": table[key]["content"],
                    "eligible_obligations": [
                        {
                            "obligation": o,
                            "a1_state": coverage.grid[key, o["id"]].value,
                        }
                        for o in packet["obligations"]
                        if coverage.grid[key, o["id"]] != EvidenceState.NO_USEFUL
                    ],
                }
                for key in keys
            ],
        },
    )


def partition(
    packet: Any,
    coverage: classification.Coverage | None = None,
) -> dict[str, Any]:
    """Choose each largest prefix satisfying both frozen input and output bounds."""
    table = evidence.sources(packet)
    require("resources" in packet, "Complete blind parent packet required")
    ordered = sorted(table, key=lambda key: table[key]["address"])
    obligations = [o["id"] for o in packet["obligations"]]
    if coverage is not None:
        coverage.authenticate(packet)
        require(
            set(coverage.grid) == {(k, o) for k in ordered for o in obligations},
            "Complete A1 grid required before A2 partition",
        )
        ordered = [
            k
            for k in ordered
            if any(coverage.grid[k, o] != EvidenceState.NO_USEFUL for o in obligations)
        ]
    batches: list[dict[str, Any]] = []
    position = 0
    while position < len(ordered):
        selected: list[str] = []
        best: dict[str, Any] | None = None
        for key in ordered[position:]:
            candidate = [*selected, key]
            raw = render(packet, candidate, table, coverage)
            cells = (
                sum(
                    coverage.grid[k, o] != EvidenceState.NO_USEFUL
                    for k in candidate
                    for o in obligations
                )
                if coverage is not None
                else len(candidate) * len(obligations)
            )
            contract = (
                pass_a2(
                    cells,
                    candidate,
                    obligations,
                    max(1, *(len(table[k]["content"]) for k in candidate)),
                )
                if coverage is not None
                else classification.contract(candidate, obligations)
            )
            bound = envelope(contract)
            if (
                len(raw.decode()) > INPUT_CHARACTERS
                or len(raw) > INPUT_BYTES
                or bound.utf8_bytes > MAX_SEMANTIC_RESPONSE_UTF8_BYTES
            ):
                break
            selected = candidate
            best = {
                "index": len(batches),
                "source_keys": selected,
                "cells": cells,
                "input_sha256": digest(raw),
                "input_characters": len(raw.decode()),
                "input_bytes": len(raw),
                "response_schema_sha256": digest(json_bytes(contract)),
                "response_maximum_characters": bound.characters,
                "response_maximum_bytes": bound.utf8_bytes,
            }
        if best is None:
            message = "Single resource exceeds pre-entry input/output envelope"
            raise ValueError(message)
        batches.append(best)
        position += len(selected)
    require(
        [key for batch in batches for key in batch["source_keys"]] == ordered,
        "Exact resource partition coverage",
    )
    value = {
        "schema": "blind-a2-partition-v1"
        if coverage is not None
        else "blind-a1-partition-v1",
        "case": packet["case"],
        "packet_sha256": digest(json_bytes(packet)),
        "instruction_sha256": digest(
            (
                INSTRUCTIONS if coverage is not None else classification.INSTRUCTION
            ).encode(),
        ),
        "a1_coverage_root": coverage.root if coverage is not None else None,
        "input_character_limit": INPUT_CHARACTERS,
        "input_byte_limit": INPUT_BYTES,
        "response_byte_limit": MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
        "batches": batches,
    }
    return {**value, "partition_sha256": digest(json_bytes(value))}
