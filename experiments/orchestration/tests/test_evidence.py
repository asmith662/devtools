# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, PT011, FBT001 -- exact synthetic locator regressions
"""Representation projection cannot manufacture or repair semantic evidence."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from experiments.orchestration.workers import evidence, semantic
from experiments.source_grounding import response, reviewer, workers
from experiments.source_grounding.test_runtime import (
    synthetic_judgments,
    synthetic_packet,
)


def resolve(content: str, quote: str, occurrence: Any = 1) -> Any:
    row = dict.fromkeys(evidence.IDENTITY, "synthetic") | {"content": content}
    return evidence.resolve(
        {"source_key": "key", "quote": quote, "occurrence": occurrence},
        {"key": row},
    )


@pytest.mark.parametrize(
    ("content", "quote", "occurrence", "start", "end"),
    [
        ("abc", "b", 1, 1, 2),
        ("ab ab ab", "ab", 1, 0, 2),
        ("ab ab ab", "ab", 3, 6, 8),
        ("aaaa", "aa", 3, 2, 4),
        ("😀écat", "cat", 1, 2, 5),
        ("x😀éz", "😀é", 1, 1, 3),
        ("a\r\nb", "\r\n", 1, 1, 3),
        ("a\nb\nc", "a\nb", 1, 0, 3),
        ("abc", "a", 1, 0, 1),
        ("abc", "c", 1, 2, 3),
        ("abc", "abc", 1, 0, 3),
        (
            "The fictional valve opens at seven ticks.",
            "The fictional valve opens at seven ticks.",
            1,
            0,
            41,
        ),
    ],
)
def test_exact_unicode_projection(
    content: str,
    quote: str,
    occurrence: int,
    start: int,
    end: int,
) -> None:
    result = resolve(content, quote, occurrence)
    assert result == {
        "source": dict.fromkeys(evidence.IDENTITY, "synthetic"),
        "start": start,
        "end": end,
        "quote": quote,
    }
    assert content[result["start"] : result["end"]] == quote


@pytest.mark.parametrize(
    ("quote", "occurrence"),
    [
        ("", 1),
        ("ABSENT", 1),
        ("a", 0),
        ("a", -1),
        ("a", 3),
        ("a", True),
        ("a", "1"),
        (None, 1),
        ("\ud800", 1),
    ],
)
def test_invalid_locators_fail_without_repair(quote: Any, occurrence: Any) -> None:
    with pytest.raises(ValueError):
        resolve("aa", quote, occurrence)


@pytest.mark.parametrize(
    "locator",
    [
        None,
        {},
        {"source_key": "foreign", "quote": "a", "occurrence": 1},
        {"source_key": "key", "quote": "a", "occurrence": 1, "end": 46},
    ],
)
def test_foreign_or_malformed_locator(locator: Any) -> None:
    with pytest.raises(ValueError):
        evidence.resolve(locator, {"key": {"content": "a"}})


def test_duplicate_source_key_and_rank_independence() -> None:
    packet = synthetic_packet(gold=True)
    original = evidence.sources(packet)
    packet["resources"].reverse()
    assert evidence.sources(packet) == original
    packet["resources"].append(deepcopy(packet["resources"][0]))
    with pytest.raises(ValueError, match="Duplicate source key"):
        evidence.sources(packet)


@pytest.mark.parametrize("gold", [True, False])
def test_all_cells_units_and_alternatives_project_without_mutation(gold: bool) -> None:
    packet = synthetic_packet(gold=gold)
    payload = synthetic_judgments(packet)
    original = deepcopy(payload)
    semantic.validate_schema(payload, response.schema(gold=gold))
    canonical = evidence.judgments(payload, packet)
    assert payload == original
    for cell, authored in zip(canonical["cells"], payload["cells"], strict=True):
        assert cell["source"]["address"].startswith("synthetic/")
        assert "source_key" not in cell
        assert cell["reason"] == authored["reason"]
        for span in cell["spans"]:
            assert (span["start"], span["end"]) == (0, 41)
    if gold:
        assert (
            canonical["units"][0]["alternatives"][0][0]
            == canonical["cells"][-1]["spans"][0]
        )
    positive = next(cell for cell in payload["cells"] if cell["spans"])
    positive["spans"][0]["quote"] += "wrong"
    with pytest.raises(ValueError, match="not found"):
        evidence.judgments(payload, packet)


def test_model_contract_contains_no_raw_offsets_or_mechanical_identity() -> None:
    schema = response.schema(gold=True)
    locator = schema["properties"]["cells"]["items"]["properties"]["spans"]["items"]
    assert set(locator["properties"]) == {"source_key", "quote", "occurrence"}
    packet = synthetic_packet(gold=True)
    disclosed = evidence.disclosure(packet)
    assert all(
        set(row) == {"source_key", "address", "content"}
        for row in disclosed["resources"]
    )
    assert packet["resources"][0]["document_identity"]


def test_unit_alternative_locator_cannot_be_repaired() -> None:
    packet = synthetic_packet(gold=True)
    payload = synthetic_judgments(packet)
    payload["units"][0]["alternatives"] = [
        [
            {
                "source_key": next(iter(evidence.sources(packet))),
                "quote": "ABSENT",
                "occurrence": 1,
            },
        ],
    ]
    with pytest.raises(ValueError, match="not found"):
        evidence.judgments(payload, packet)


def test_missing_useful_locator_fails_existing_scientific_authentication() -> None:
    packet = synthetic_packet(gold=False)
    payload = synthetic_judgments(packet)
    positive = next(cell for cell in payload["cells"] if cell["spans"])
    positive["spans"] = []
    config = workers.configuration("Luna", reasoning="Medium", gold=False)
    review = semantic.review(payload, packet, config)
    with pytest.raises(ValueError):
        reviewer.validate(review, packet, ("GPT-6 Luna", "Medium"))
