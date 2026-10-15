# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004 -- fictional deterministic complete artifact fixture
"""Exact reattachment, negative ownership and canonical builder authentication."""

import json
from pathlib import Path
from typing import Any

import pytest

from experiments.orchestration.workers.evidence import sources
from experiments.source_grounding import reviewer, workers
from experiments.source_grounding.chunked import (
    classification,
    consolidation,
    disclosure,
)
from experiments.source_grounding.chunked.archive import assemble
from experiments.source_grounding.test_runtime import synthetic_packet


def fixture() -> tuple[Any, Any, Any]:
    packet = synthetic_packet(gold=True)
    table = sources(packet)
    key = next(k for k, r in table.items() if r["address"] == "synthetic/valve.txt")
    a1 = {
        "resources": [
            {
                "source_key": k,
                "judgments": [
                    {
                        "obligation_id": "O1",
                        "state": "USEFUL" if k == key else "NO_USEFUL",
                    },
                ],
            }
            for k in table
        ],
    }
    coverage = classification.validate(packet, (("A1", list(table), a1),))
    a2 = {
        "cells": [
            {
                "source_key": key,
                "obligation_id": "O1",
                "resolution_state": "EVIDENCE_FOUND",
                "semantic_statement": "The fictional valve opens at seven ticks.",
                "locators": [
                    {
                        "source_key": key,
                        "quote": table[key]["content"],
                        "occurrence": 1,
                    },
                ],
                "uncertainty_note": "",
                "representation_complete": True,
            },
        ],
        "self_review": "Checked synthetic evidence.",
        "representation_complete": True,
    }
    archive = assemble(packet, (("A2", a2),), "synthetic-runtime", coverage=coverage)
    card = archive.cards[0]
    b = {
        "units": [
            {
                "id": "U1",
                "obligation": "O1",
                "statement": "The threshold is seven ticks.",
                "basis": "REPOSITORY_SUPPORTED",
                "necessity": "The fictional task asks for the threshold.",
                "alternatives": [
                    [{"cell_id": card.cell_id, "evidence_id": card.evidence_ids[0]}],
                ],
            },
        ],
        "gaps": {
            "TASK_INTERPRETATION_GAP": "NONE",
            "TASK_GAP": "NONE",
            "REPOSITORY_INFORMATION_GAP": "NONE",
            "unconditional_sufficiency": True,
            "qualification": "Synthetic only.",
        },
        "unresolved_cells": [],
        "self_review": "Checked units, alternatives and gaps.",
        "representation_complete": True,
    }
    return packet, archive, b


def test_final_projection_builds_exact_canonical_artifact_set(tmp_path: Path) -> None:
    packet, archive, payload = fixture()
    context, cards = disclosure.decode(disclosure.from_archive(packet, archive))
    assert context["negative_counts"] == {"O1": 2}
    assert context["cell_count"] == 3
    assert len(cards) == 1
    review = consolidation.assemble(packet, archive, payload)
    assert reviewer.validate(review, packet)["labels"] == {
        "UNNECESSARY": 2,
        "REQUIRED": 1,
    }
    files = workers.packet_files(
        packet,
        b"Synthetic method instructions",
        Path(reviewer.__file__).read_bytes(),
    )
    for name, raw in files.items():
        (tmp_path / name).write_bytes(raw)
    (tmp_path / "stage_c_review.json").write_bytes(reviewer.canonical(review))
    result = reviewer.products(tmp_path)
    assert json.loads(result["stage_c_validation.json"])["status"] == "PASS"
    for name, raw in result.items():
        (tmp_path / name).write_bytes(raw)
    assert reviewer.products(tmp_path) == result


@pytest.mark.parametrize(
    "fault",
    ["incomplete", "foreign", "cross_cell", "uncertainty", "witness"],
)
def test_global_projection_never_repairs_or_drops_findings(fault: str) -> None:
    packet, archive, b = fixture()
    if fault == "incomplete":
        b["representation_complete"] = False
    elif fault == "foreign":
        b["units"][0]["alternatives"][0][0]["evidence_id"] = "e99999"
    elif fault == "cross_cell":
        b["units"][0]["alternatives"][0][0]["cell_id"] = "c0000"
    elif fault == "uncertainty":
        b["unresolved_cells"] = ["c0000"]
    else:
        b["units"] = []
    with pytest.raises(ValueError, match=r"Incomplete|Foreign|Uncertainty|Necessary"):
        consolidation.assemble(packet, archive, b)
