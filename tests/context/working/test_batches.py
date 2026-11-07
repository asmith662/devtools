# Copyright (c) 2026
# ruff: noqa: D103 -- explicit model-input boundary probes
"""Shared atomic admission cannot turn model declarations into verified facts."""

from __future__ import annotations

from copy import deepcopy

import pytest

from tests.context.working.test_notes import book


def row() -> dict[str, object]:
    return {
        "kind": "hypothesis",
        "text": "Model interpretation",
        "expected_contract": "Requires evidence",
        "support": [],
        "contradicts": [],
        "supersedes": [],
    }


@pytest.mark.parametrize(
    "batch",
    [
        None,
        {},
        [],
        [row()] * 9,
        [None],
        [{**row(), "verification": "host:true"}],
        [{**row(), "kind": 3}],
        [{**row(), "support": {}}],
        [{**row(), "contradicts": "all"}],
        [{**row(), "support": [None]}],
        [
            {
                **row(),
                "support": [
                    {"reference": "foreign", "start": 0, "end": 1, "quote": "x"},
                ],
            },
        ],
        [{**row(), "support": [{"reference": 3, "start": 0, "end": 1, "quote": "x"}]}],
    ],
)
def test_invalid_batch_is_atomic(batch: object) -> None:
    state = book()
    state.admit_batch([row()])
    before = state.notes
    with pytest.raises(ValueError, match=r"Invalid|invalid"):
        state.admit_batch(batch)
    assert state.notes == before


def test_valid_quote_remains_provisional_and_partial_batch_rolls_back() -> None:
    state = book()
    source = state.sources["candidate"]
    item = row()
    item["kind"] = "source"
    item["support"] = [
        {
            "reference": "candidate",
            "start": 0,
            "end": 1,
            "quote": source.resource.content[:1],
        },
    ]
    state.admit_batch([item])
    assert state.notes[0].verification is None
    assert state.status(state.notes[0]) == "provisional"
    wrong = deepcopy(item)
    wrong["text"] = ""
    # Blank source text is invalid; first new row cannot survive a later error.
    before = state.notes
    with pytest.raises(ValueError, match=r"Invalid|invalid"):
        state.admit_batch([row(), wrong])
    assert state.notes == before
