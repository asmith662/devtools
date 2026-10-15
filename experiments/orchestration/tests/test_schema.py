# Copyright (c) 2026
# ruff: noqa: S101, PLR2004 -- deterministic worst-case response fixtures
"""Prove host-valid response maxima without a model or average-English guesses."""

from copy import deepcopy
from typing import Any

import pytest

from experiments.orchestration.workers import schema
from experiments.source_grounding.chunked.response import pass_a2, pass_b


@pytest.mark.parametrize("cells", [744, 640, 444])
def test_pass_b_exact_maximum(cells: int) -> None:
    """All bounded free text and repeated fields are simultaneously maximal."""
    contract = pass_b(cells, ["O1", "O2"])
    bound = schema.envelope(contract)
    maximum = schema.maximum(contract, bytes_measure=True)
    assert len(schema.canonical(maximum)) == bound.utf8_bytes
    assert bound.utf8_bytes <= schema.MAX_SEMANTIC_RESPONSE_UTF8_BYTES
    assert len(maximum["units"]) == 8
    assert len(maximum["unresolved_cells"]) == cells


def test_pass_a_aggregate_bound_and_cardinality() -> None:
    """A resource's two obligation cells fit; a second resource cannot fit."""
    contract = pass_a2(2, ["a" * 64], ["O1", "O2"], 75076)
    bound = schema.envelope(contract)
    assert bound.characters == bound.utf8_bytes <= 65536
    assert (
        schema.envelope(pass_a2(4, ["a" * 64], ["O1", "O2"], 75076)).utf8_bytes > 65536
    )
    value = schema.maximum(contract, bytes_measure=True)
    for cell in value["cells"]:
        assert len(cell["locators"]) == 4
        assert sum(len(locator["quote"]) for locator in cell["locators"]) == 4096
    bad = deepcopy(value)
    bad["cells"][0]["locators"][1]["quote"] += "x"
    with pytest.raises(ValueError, match="Aggregate"):
        schema.validate(bad, contract)
    native = schema.native(contract)
    assert schema.AGGREGATE not in repr(native)
    assert schema.AGGREGATE in repr(contract)


@pytest.mark.parametrize("value", ["\0", "\U0001f600", "\r\n", '\\"', "a\u0301"])
def test_unicode_bound_is_worst_case(value: str) -> None:
    """Control escaping, not four-byte Unicode alone, sets the canonical maximum."""
    contract = {"type": "string", "maxLength": 8}
    assert len(schema.canonical(value)) <= schema.envelope(contract).utf8_bytes


def test_unbounded_and_unproved_contracts_reject() -> None:
    """A convenient estimate cannot stand in for an exact representation proof."""
    contracts: list[dict[str, Any]] = [
        {"type": "string"},
        {"type": "array", "items": {"type": "boolean"}},
        {"type": "string", "maxLength": 8, "pattern": "arbitrary"},
    ]
    for contract in contracts:
        with pytest.raises((KeyError, ValueError)):
            schema.envelope(contract)
