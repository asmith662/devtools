# Copyright (c) 2026
"""Lossless, length-framed blind EvidenceCard disclosure; no exact quote archive."""

from __future__ import annotations

import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from experiments.source_grounding.chunked.archive import EvidenceArchive

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers.evidence import sources
from experiments.source_grounding.chunked.cards import (
    EvidenceCard,
    EvidenceState,
    ResolutionState,
    maximal_cards,
)

CONTRACT = "blind-evidence-card-unicode-frame-v2"
HEADER_FIELDS = 7
INSTRUCTION = (
    "Consolidate every local evidence finding globally, independently of retrieval "
    "or treatment. Determine necessary semantic units, conjunctive evidence, "
    "disjunctive alternatives, gaps, unconditional sufficiency and qualifications. "
    "Reference cell_id/evidence_id; do not invent, reproduce or request quotations. "
    "USEFUL/NO_USEFUL/UNCERTAIN are local evidence states, not final gold labels. "
    "Preserve uncertainty. If adequate representation is impossible, report "
    "representation_complete=false; never truncate, relabel or omit findings. "
    "All authorized information is supplied here. Use no tools, filesystem or web. "
    "Return only the structured response required by the frozen response schema.\n"
    "Each card header is: cell_id source_key obligation_id A1_state "
    "A2_resolution_state completeness "
    "evidence_count evidence_ids. It is followed by summary and uncertainty_note, "
    "each encoded as decimal Unicode-code-point length, colon, then exactly that "
    "many characters. Length framing is literal: no escaping or normalization.\n"
)


def _field(value: str) -> str:
    """Retain every valid Unicode code point, including framing-looking content."""
    value.encode("utf-8", errors="strict")
    return f"{len(value)}:{value}"


def render(context: dict[str, Any], cards: tuple[EvidenceCard, ...]) -> bytes:
    """Render the complete supplied blind context and every card exactly once."""
    require(
        set(context)
        == {
            "case",
            "task",
            "obligations",
            "coverage_root",
            "cell_count",
            "resource_count",
            "negative_counts",
            "unresolved_cells",
            "card_count",
        },
        "Blind consolidation context allowlist",
    )
    require(
        context["card_count"] == len(cards)
        and sum(context["negative_counts"].values()) + len(cards)
        == context["cell_count"],
        "EvidenceCard coverage count",
    )
    require(len({c.cell_id for c in cards}) == len(cards), "Duplicate EvidenceCard")
    head = json.dumps(
        context,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    parts = [CONTRACT + "\n", INSTRUCTION, _field(head), "\n"]
    for card in cards:
        card.validate()
        header = [
            card.cell_id,
            card.source_key,
            card.obligation_id,
            card.state.value,
            card.resolution_state.value,
            "true",
            str(len(card.evidence_ids)),
            *card.evidence_ids,
        ]
        require(
            all(v and not any(c.isspace() for c in v) for v in header),
            "Invalid mechanical EvidenceCard identity",
        )
        parts.extend(
            (
                " ".join(header) + "\n",
                _field(card.summary),
                _field(card.uncertainty_note),
                "\n",
            ),
        )
    return "".join(parts).encode("utf-8", errors="strict")


def decode(raw: bytes) -> tuple[dict[str, Any], tuple[EvidenceCard, ...]]:
    """Authenticate exact replay of host disclosure without inspecting judgments."""
    text = raw.decode("utf-8", errors="strict")
    prefix = CONTRACT + "\n" + INSTRUCTION
    require(text.startswith(prefix), "EvidenceCard disclosure contract")
    offset = len(prefix)

    def field() -> str:
        nonlocal offset
        colon = text.find(":", offset)
        require(colon >= offset, "Missing field length")
        digits = text[offset:colon]
        require(digits.isascii() and digits.isdecimal(), "Invalid field length")
        size = int(digits)
        require(size <= len(text) - colon - 1, "Truncated field")
        offset = colon + 1 + size
        return text[colon + 1 : offset]

    context = json.loads(field())
    require(type(context) is dict, "Blind context must be an object")
    require(text[offset : offset + 1] == "\n", "Context separator")
    offset += 1
    cards = []
    for _ in range(context["card_count"]):
        end = text.find("\n", offset)
        require(end >= offset, "Truncated card header")
        header = text[offset:end].split(" ")
        require(
            len(header) >= HEADER_FIELDS and header[5] == "true",
            "Invalid card header",
        )
        require(
            int(header[6]) == len(header) - HEADER_FIELDS,
            "Evidence reference count",
        )
        offset = end + 1
        summary, uncertainty = field(), field()
        require(text[offset : offset + 1] == "\n", "Card separator")
        offset += 1
        cards.append(
            EvidenceCard(
                header[0],
                header[1],
                header[2],
                EvidenceState(header[3]),
                summary,
                tuple(header[HEADER_FIELDS:]),
                uncertainty,
                representation_complete=True,
                resolution_state=ResolutionState(header[4]),
            ),
        )
    result = tuple(cards)
    require(
        offset == len(text) and render(context, result) == raw,
        "Exact disclosure replay",
    )
    return context, result


def maximum_disclosure(packet: dict[str, Any]) -> bytes:
    """Render maximum cards with exact frozen task/obligation/identity lengths.

    This is prospective sizing only: placeholder maximum text is not a judgment
    or scientific primary. No resource content enters the resulting disclosure.
    """
    table = sources(packet)
    require("resources" in packet, "Full blind parent packet required")
    keys = sorted(table, key=lambda key: table[key]["address"])
    obligations = sorted(o["id"] for o in packet["obligations"])
    require(obligations and len(set(obligations)) == len(obligations), "Obligations")
    cards = tuple(
        replace(
            card,
            source_key=keys[index // len(obligations)],
            obligation_id=obligations[index % len(obligations)],
            state=EvidenceState.USEFUL,
        )
        for index, card in enumerate(maximal_cards(len(keys) * len(obligations)))
    )
    context = {
        "case": packet["case"],
        "task": packet["task"],
        "obligations": packet["obligations"],
        "coverage_root": digest(json_bytes([asdict(card) for card in cards])),
        "cell_count": len(cards),
        "card_count": len(cards),
        "resource_count": len(keys),
        "negative_counts": dict.fromkeys(obligations, 0),
        "unresolved_cells": [],
    }
    return render(context, cards)


def from_archive(packet: dict[str, Any], archive: EvidenceArchive) -> bytes:
    """Retain all eligible findings, explicit negative counts and unresolved IDs."""
    value = json.loads(archive.canonical)
    require(
        value["packet_sha256"] == digest(json_bytes(packet)),
        "Archive packet binding",
    )
    negatives = dict.fromkeys((o["id"] for o in packet["obligations"]), 0)
    for cell in value["a1"]["cells"]:
        if cell["state"] == "NO_USEFUL":
            negatives[cell["obligation_id"]] += 1
    context = {
        "case": packet["case"],
        "task": packet["task"],
        "obligations": packet["obligations"],
        "coverage_root": archive.coverage_root,
        "cell_count": value["cell_count"],
        "resource_count": len(packet["resources"]),
        "card_count": len(archive.cards),
        "negative_counts": negatives,
        "unresolved_cells": [
            c.cell_id
            for c in archive.cards
            if c.resolution_state == ResolutionState.REMAINS_UNCERTAIN
        ],
    }
    return render(context, archive.cards)
