# Copyright (c) 2026

"""Authenticate complete Pass-A cells and archive exact evidence outside Pass B."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import evidence
from experiments.orchestration.workers.budget import BudgetError, FailureClass
from experiments.orchestration.workers.schema import validate as validate_schema
from experiments.source_grounding.chunked.cards import (
    AGGREGATE_QUOTE_CHARACTERS,
    MAX_CELLS,
    MAX_LOCATORS,
    EvidenceCard,
    EvidenceState,
    ResolutionState,
)
from experiments.source_grounding.chunked.response import pass_a2

if TYPE_CHECKING:
    from experiments.source_grounding.chunked.classification import Coverage


@dataclass(frozen=True)
class EvidenceArchive:
    """Canonical archive bytes and a separate immutable semantic card projection."""

    canonical: bytes
    cards: tuple[EvidenceCard, ...]
    coverage_root: str

    @property
    def sha256(self) -> str:
        """Bind all exact evidence and invocation provenance, not a mutable path."""
        return digest(self.canonical)


def assemble(  # noqa: PLR0915 -- one strict input-to-evidence projection
    packet: dict[str, Any],
    responses: tuple[tuple[str, dict[str, Any]], ...],
    runtime_sha256: str,
    *,
    coverage: Coverage,
) -> EvidenceArchive:
    """Resolve content locators without repair and require full Cartesian coverage.

    The caller owns packet, invocation and runtime authentication. This projection
    never establishes invocation success or authority from a model's assertion.
    """
    table = evidence.sources(packet)
    coverage.authenticate(packet)
    obligations = [o["id"] for o in packet["obligations"]]
    require(len(set(obligations)) == len(obligations), "Duplicate obligation")
    keys = sorted(table, key=lambda key: table[key]["address"])
    all_cells = [(key, obligation) for key in keys for obligation in obligations]
    require(
        len(all_cells) <= MAX_CELLS and set(coverage.grid) == set(all_cells),
        "Complete A1 coverage required",
    )
    require(
        json.loads(coverage.canonical)["packet_sha256"] == digest(json_bytes(packet)),
        "A1 packet binding",
    )
    expected = [
        pair for pair in all_cells if coverage.grid[pair] != EvidenceState.NO_USEFUL
    ]
    indices = {pair: i for i, pair in enumerate(all_cells)}
    seen: dict[tuple[str, str], EvidenceCard] = {}
    records: dict[str, Any] = {}
    cells: dict[str, Any] = {}
    invocation_ids = set()
    for invocation, payload in responses:
        require(invocation and invocation not in invocation_ids, "Duplicate invocation")
        invocation_ids.add(invocation)
        require(
            set(payload) == {"cells", "self_review", "representation_complete"},
            "Pass-A response fields",
        )
        require(
            type(payload["self_review"]) is str and payload["self_review"].strip(),
            "Pass-A self review",
        )
        if payload["representation_complete"] is not True:
            raise BudgetError(
                FailureClass.EVIDENCE_REPRESENTATION_LIMIT,
                "Incomplete Pass-A response",
            )
        response_sha256 = digest(json_bytes(payload))
        try:
            validate_schema(
                payload,
                pass_a2(
                    len(payload["cells"]),
                    list(table),
                    obligations,
                    max(1, *(len(r["content"]) for r in table.values())),
                ),
            )
        except ValueError as error:
            if str(error) in {
                "Semantic string length",
                "Semantic array cardinality",
                "Aggregate quote character limit",
            }:
                raise BudgetError(
                    FailureClass.EVIDENCE_REPRESENTATION_LIMIT,
                    "A2 bounds: statement512, uncertainty256, quote4096, locators4",
                ) from error
            raise
        for cell in payload["cells"]:
            require(
                set(cell)
                == {
                    "source_key",
                    "obligation_id",
                    "resolution_state",
                    "semantic_statement",
                    "locators",
                    "uncertainty_note",
                    "representation_complete",
                },
                "Pass-A cell fields",
            )
            pair = (cell["source_key"], cell["obligation_id"])
            require(
                pair in expected and pair not in seen,
                "Duplicate/foreign Pass-A cell",
            )
            index = indices[pair]
            locators = cell["locators"]
            require(type(locators) is list, "Pass-A evidence locators")
            if len(locators) > MAX_LOCATORS:
                raise BudgetError(
                    FailureClass.EVIDENCE_REPRESENTATION_LIMIT,
                    "Too many exact locators",
                )
            require(
                all(
                    type(locator) is dict and locator.get("source_key") == pair[0]
                    for locator in locators
                ),
                "Evidence must belong to its own cell source",
            )
            exact = [evidence.resolve(locator, table) for locator in locators]
            require(
                all(span["quote"].strip() for span in exact),
                "A2 requires non-whitespace exact evidence",
            )
            if sum(len(span["quote"]) for span in exact) > AGGREGATE_QUOTE_CHARACTERS:
                raise BudgetError(
                    FailureClass.EVIDENCE_REPRESENTATION_LIMIT,
                    "Aggregate quote characters exceed 4096",
                )
            ids = tuple(
                f"e{index * MAX_LOCATORS + slot:05d}" for slot in range(len(exact))
            )
            card = EvidenceCard(
                f"c{index:04d}",
                pair[0],
                pair[1],
                coverage.grid[pair],
                evidence.text(cell["semantic_statement"]),
                ids,
                evidence.text(cell["uncertainty_note"]),
                cell["representation_complete"],
                ResolutionState(cell["resolution_state"]),
            )
            require(
                type(card.representation_complete) is bool,
                "Representation flag must be boolean",
            )
            card.validate()
            seen[pair] = card
            cells[card.cell_id] = {
                "invocation_id": invocation,
                "response_sha256": response_sha256,
                "card": asdict(card),
            }
            for identifier, span in zip(ids, exact, strict=True):
                records[identifier] = {
                    "evidence_id": identifier,
                    "case": packet["case"],
                    "obligation_id": pair[1],
                    "source_key": pair[0],
                    "cell_id": card.cell_id,
                    **span,
                }
    require(
        set(seen) == set(expected),
        "Incomplete Pass-A resource/obligation coverage",
    )
    ordered = tuple(seen[pair] for pair in expected)
    root = coverage.root
    raw = json_bytes(
        {
            "schema": "source-grounding-evidence-archive-v2",
            "case": packet["case"],
            "packet_sha256": digest(json_bytes(packet)),
            "runtime_sha256": runtime_sha256,
            "coverage_root": root,
            "cell_count": len(all_cells),
            "a1": json.loads(coverage.canonical),
            "cells": cells,
            "evidence": records,
        },
    )
    return EvidenceArchive(raw, ordered, root)


def reattach(
    archive: EvidenceArchive,
    cell_id: str,
    evidence_id: str,
) -> dict[str, Any]:
    """Return exact archived spans only for authenticated cell-local references."""
    value = json.loads(archive.canonical)
    require(evidence_id in value["evidence"], "Foreign evidence reference")
    record = value["evidence"][evidence_id]
    require(record["cell_id"] == cell_id, "Foreign cell evidence reference")
    return {name: record[name] for name in ("source", "start", "end", "quote")}
