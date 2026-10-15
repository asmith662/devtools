# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004 -- synthetic deterministic stage fixtures
"""Complete A1 grid, resource-oriented A2 and fail-closed evidence integration."""

import json
from copy import deepcopy
from typing import Any

import pytest

from experiments.orchestration.workers import evidence, schema
from experiments.source_grounding.chunked import classification, packing
from experiments.source_grounding.chunked.archive import assemble
from experiments.source_grounding.chunked.test_archive import coverage, fixture


def test_state_only_schema_and_complete_coverage() -> None:
    packet, _ = fixture()
    c = coverage(packet)
    assert len(c.grid) == 2
    contract = classification.contract(list(evidence.sources(packet)), ["O1", "O2"])
    assert schema.envelope(contract).utf8_bytes < 65536
    assert not {"reason", "quote", "evidence_id", "confidence"} & set(
        str(contract).split(),
    )
    value = json.loads(c.canonical)
    assert {cell["state"] for cell in value["cells"]} == {"USEFUL"}


@pytest.mark.parametrize(
    "fault",
    [
        "missing_resource",
        "duplicate_resource",
        "foreign",
        "missing_obligation",
        "duplicate_obligation",
        "unknown_obligation",
        "state",
        "rationale",
    ],
)
def test_a1_rejects_absent_ambiguous_and_extra_judgments(fault: str) -> None:
    packet, _ = fixture()
    keys = list(evidence.sources(packet))
    payload: Any = {
        "resources": [
            {
                "source_key": keys[0],
                "judgments": [
                    {"obligation_id": "O1", "state": "NO_USEFUL"},
                    {"obligation_id": "O2", "state": "UNCERTAIN"},
                ],
            },
        ],
    }
    resource = payload["resources"][0]
    if fault == "missing_resource":
        payload["resources"].clear()
    elif fault == "duplicate_resource":
        payload["resources"].append(deepcopy(resource))
    elif fault == "foreign":
        resource["source_key"] = "foreign"
    elif fault == "missing_obligation":
        resource["judgments"].pop()
    elif fault == "duplicate_obligation":
        resource["judgments"][1]["obligation_id"] = "O1"
    elif fault == "unknown_obligation":
        resource["judgments"][1]["obligation_id"] = "foreign"
    elif fault == "state":
        resource["judgments"][0]["state"] = "UNNECESSARY"
    else:
        resource["judgments"][0]["reason"] = "extra"
    with pytest.raises(ValueError, match=r"Semantic|Duplicate"):
        classification.validate(packet, (("A1", keys, payload),))


def test_a2_resources_once_and_explicit_empty_eligibility() -> None:
    packet, _ = fixture()
    c = coverage(packet)
    part = packing.partition(packet, c)
    table = evidence.sources(packet)
    raw = packing.render(packet, part["batches"][0]["source_keys"], table, c)
    disclosed = json.loads(raw[len(packing.INSTRUCTIONS.encode()) :])
    assert len(disclosed["resources"]) == 1
    assert len(disclosed["resources"][0]["eligible_obligations"]) == 2
    assert disclosed["resources"][0]["content"] == packet["resources"][0]["content"]
    none = coverage(packet, "NO_USEFUL")
    assert packing.partition(packet, none)["batches"] == []
    result = assemble(packet, (), "runtime", coverage=none)
    assert result.cards == ()
    assert json.loads(result.canonical)["cell_count"] == 2


def test_a1_useful_cannot_silently_lose_evidence() -> None:
    packet, response = fixture()
    response["cells"][0].update(
        resolution_state="REMAINS_UNCERTAIN",
        locators=[],
        uncertainty_note="Cannot resolve",
    )
    with pytest.raises(ValueError, match="mismatch"):
        assemble(packet, (("A2", response),), "runtime", coverage=coverage(packet))


def test_metadata_cannot_enter_a1_a2_disclosure() -> None:
    packet, _ = fixture()
    c = coverage(packet)
    table = evidence.sources(packet)
    altered = {**packet, "queries": "FORBIDDEN-RETRIEVAL", "B": "FORBIDDEN-TREATMENT"}
    for cov in (None, c):
        raw = packing.render(altered, list(table), table, cov)
        assert b"FORBIDDEN-RETRIEVAL" not in raw
        assert b"FORBIDDEN-TREATMENT" not in raw


def test_a1_partition_prototype_projection_is_preserved() -> None:
    packet, _ = fixture()
    packet["resources"].append(
        {
            **packet["resources"][0],
            "address": "another.txt",
            "document_identity": "different",
        },
    )
    part = packing.partition(packet)
    assert len(part["batches"]) == 1
    assert part["batches"][0]["cells"] == 4
    packet["resources"].reverse()
    assert packing.partition(packet)["batches"] == part["batches"]
