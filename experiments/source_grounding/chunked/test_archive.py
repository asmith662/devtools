# Copyright (c) 2026
# ruff: noqa: S101, PLR2004, ANN401 -- synthetic exact archive fixtures
"""No model call or real scientific judgment is needed to authenticate archives."""

import json
from copy import deepcopy
from typing import Any

import pytest

from experiments.orchestration.workers.evidence import sources
from experiments.source_grounding.chunked import classification
from experiments.source_grounding.chunked.archive import assemble, reattach
from experiments.source_grounding.chunked.disclosure import decode, maximum_disclosure


def fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    """Build a fictional source with duplicate and Unicode evidence."""
    packet = {
        "schema": "blind-semantic-gold-packet-v1",
        "case": "SYNTHETIC-ARCHIVE",
        "frame": {"repository_id": "fictional"},
        "task": "Fictional task",
        "obligations": [{"id": "O1"}, {"id": "O2"}],
        "resources": [
            {
                "address": "fiction.txt",
                "document_identity": "doc",
                "content_identity": "content",
                "content": "\U0001f600 fact fact\r\n",
            },
        ],
    }
    key = next(iter(sources(packet)))
    response = {
        "representation_complete": True,
        "self_review": "Synthetic audit",
        "cells": [
            {
                "source_key": key,
                "obligation_id": obligation,
                "resolution_state": "EVIDENCE_FOUND",
                "semantic_statement": "Fictional fact supports the obligation",
                "locators": [{"source_key": key, "quote": "fact", "occurrence": 2}],
                "uncertainty_note": "",
                "representation_complete": True,
            }
            for obligation in ("O1", "O2")
        ],
    }
    return packet, response


def coverage(packet: Any, state: str = "USEFUL") -> classification.Coverage:
    """Construct an explicit complete synthetic A1 matrix, not implicit negatives."""
    keys = list(sources(packet))
    payload = {
        "resources": [
            {
                "source_key": key,
                "judgments": [
                    {"obligation_id": o["id"], "state": state}
                    for o in packet["obligations"]
                ],
            }
            for key in keys
        ],
    }
    return classification.validate(packet, (("A1", keys, payload),))


def test_complete_exact_archive_and_canonical_reattachment() -> None:
    """Host-only exact spans retain the model's selected occurrence unchanged."""
    packet, response = fixture()
    result = assemble(
        packet,
        (("invocation", response),),
        "runtime",
        coverage=coverage(packet),
    )
    assert result == assemble(
        packet,
        (("invocation", response),),
        "runtime",
        coverage=coverage(packet),
    )
    value = json.loads(result.canonical)
    assert value["cell_count"] == 2
    span = reattach(result, "c0000", "e00000")
    assert span["start"] == 7
    assert span["end"] == 11
    assert span["quote"] == "fact"
    with pytest.raises(ValueError, match="Foreign cell"):
        reattach(result, "c0001", "e00000")
    with pytest.raises(ValueError, match="Foreign evidence"):
        reattach(result, "c0000", "unavailable")


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "duplicate",
        "foreign",
        "incomplete",
        "summary",
        "locators",
        "uncertainty",
        "quote",
        "state",
    ],
)
def test_cell_coverage_and_representation_fail_closed(mutation: str) -> None:
    """Invalid or overflowing evidence never becomes NO_USEFUL."""
    packet, response = fixture()
    cell = response["cells"][0]
    if mutation == "missing":
        response["cells"].pop()
    elif mutation == "duplicate":
        response["cells"].append(deepcopy(cell))
    elif mutation == "foreign":
        cell["source_key"] = "foreign"
    elif mutation == "incomplete":
        cell["representation_complete"] = False
    elif mutation == "summary":
        cell["semantic_statement"] = "x" * 513
    elif mutation == "locators":
        cell["locators"] *= 5
    elif mutation == "uncertainty":
        cell["uncertainty_note"] = "x" * 257
    elif mutation == "quote":
        cell["locators"][0]["quote"] = "incorrect quote"
    else:
        cell["resolution_state"] = "UNNECESSARY"
    with pytest.raises(
        ValueError,
        match=r"Pass-A|EVIDENCE_REPRESENTATION_LIMIT|foreign|found|ResolutionState|Semantic",
    ):
        assemble(
            packet,
            (("invocation", response),),
            "runtime",
            coverage=coverage(packet),
        )


def test_quote_aggregate_and_uncertainty_remain_explicit() -> None:
    """A full-source quote is bounded by quoted text, not source size alone."""
    packet, response = fixture()
    packet["resources"][0]["content"] = "x" * 4097
    for cell in response["cells"]:
        cell["locators"][0].update(quote="x" * 4097, occurrence=1)
    with pytest.raises(ValueError, match="4096"):
        assemble(
            packet,
            (("invocation", response),),
            "runtime",
            coverage=coverage(packet),
        )
    for cell in response["cells"]:
        cell.update(
            resolution_state="REMAINS_UNCERTAIN",
            uncertainty_note="Unresolved",
            locators=[],
        )
    result = assemble(
        packet,
        (("invocation", response),),
        "runtime",
        coverage=coverage(packet, "UNCERTAIN"),
    )
    assert all(c.state == "UNCERTAIN" for c in result.cards)


def test_maximum_frame_preserves_context_and_excludes_raw_content() -> None:
    """Size exact packet metadata without disclosing the source quotation archive."""
    packet, _ = fixture()
    packet["resources"][0]["content"] = "SYNTHETIC-RAW-CONTENT-SENTINEL"
    raw = maximum_disclosure(packet)
    context, cards = decode(raw)
    assert context["task"] == packet["task"]
    assert context["obligations"] == packet["obligations"]
    assert {c.source_key for c in cards} == set(sources(packet))
    assert b"SYNTHETIC-RAW-CONTENT-SENTINEL" not in raw
    assert b"document_identity" not in raw
    assert b"content_identity" not in raw
