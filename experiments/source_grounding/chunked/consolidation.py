# Copyright (c) 2026
# ruff: noqa: ANN401 -- exact bounded scientific representation projection
"""Reattach host evidence and derive canonical labels from global semantic units."""

from __future__ import annotations

import itertools
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import evidence, schema
from experiments.orchestration.workers.budget import BudgetError, FailureClass
from experiments.source_grounding import reviewer
from experiments.source_grounding.chunked import response
from experiments.source_grounding.chunked.archive import EvidenceArchive, reattach
from experiments.source_grounding.chunked.cards import ResolutionState

WITNESS_EXPANSION_LIMIT = 1000000


def assemble(packet: Any, archive: EvidenceArchive, payload: Any) -> Any:
    """No evidence or semantic repair; incomplete uncertainty cannot become gold."""
    value = json.loads(archive.canonical)
    require(
        value["packet_sha256"] == digest(json_bytes(packet)),
        "Archive packet differs",
    )
    obligations = [o["id"] for o in packet["obligations"]]
    schema.validate(payload, response.pass_b(value["cell_count"], obligations))
    unresolved = {
        c.cell_id
        for c in archive.cards
        if c.resolution_state == ResolutionState.REMAINS_UNCERTAIN
    }
    require(
        set(payload["unresolved_cells"]) == unresolved
        and len(payload["unresolved_cells"]) == len(unresolved),
        "Uncertainty accounting differs",
    )
    if not payload["representation_complete"] or unresolved:
        raise BudgetError(
            FailureClass.EVIDENCE_REPRESENTATION_LIMIT,
            "Incomplete global representation or unresolved evidence; no final gold",
        )
    cards = {c.cell_id: c for c in archive.cards}
    units = []
    for unit in payload["units"]:
        alternatives = []
        for references in unit["alternatives"]:
            spans = []
            for ref in references:
                require(
                    ref["cell_id"] in cards
                    and cards[ref["cell_id"]].obligation_id == unit["obligation"],
                    "Foreign unit cell/obligation",
                )
                spans.append(reattach(archive, ref["cell_id"], ref["evidence_id"]))
            alternatives.append(spans)
        units.append({**unit, "alternatives": alternatives})
    required: set[tuple[str, str]] = set()
    for oid in obligations:
        choices = [
            [{s["source"]["address"] for s in alt} for alt in unit["alternatives"]]
            for unit in units
            if unit["obligation"] == oid
        ]
        count = 1
        for choice_set in choices:
            count *= len(choice_set)
        require(
            count <= WITNESS_EXPANSION_LIMIT,
            "Witness expansion bound; no truncation",
        )
        for witness in reviewer.minimal(
            set().union(*parts) for parts in itertools.product(*choices)
        ):
            required.update((oid, address) for address in witness)
    table = evidence.sources(packet)
    by_pair = {(c.source_key, c.obligation_id): c for c in archive.cards}
    cells = []
    for cell in value["a1"]["cells"]:
        key, oid = cell["source_key"], cell["obligation_id"]
        source = {
            k: table[key][k]
            for k in ("address", "document_identity", "content_identity")
        }
        if cell["state"] == "NO_USEFUL":
            require((key, oid) not in by_pair, "Contradictory negative evidence")
            label, spans, reason = (
                "UNNECESSARY",
                [],
                "A1 explicitly classified NO_USEFUL; complete coverage "
                + archive.coverage_root,
            )
        else:
            card = by_pair[key, oid]
            spans = [reattach(archive, card.cell_id, eid) for eid in card.evidence_ids]
            label = (
                "REQUIRED" if (oid, source["address"]) in required else "HELPFUL_ONLY"
            )
            reason = card.summary
        cells.append(
            {
                "obligation": oid,
                "source": source,
                "label": label,
                "spans": spans,
                "reason": reason,
            },
        )
    review = {
        "schema": "blind-primary-review-v1",
        "case": packet["case"],
        "frame": packet["frame"],
        "packet_sha256": digest(json_bytes(packet)),
        "attestation": {
            "model": "GPT-6 Astra",
            "reasoning": "High",
            "second_reviewer": False,
            "reconciliation": False,
            "host_routing_independently_verified": False,
            "blindness": ["NO_ACCESS:" + name for name in reviewer.BLINDNESS],
        },
        "cells": cells,
        "units": units,
        "gaps": payload["gaps"],
        "self_review": payload["self_review"],
    }
    reviewer.validate(review, packet)
    return review
