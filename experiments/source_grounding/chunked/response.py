# Copyright (c) 2026
# ruff: noqa: ANN401 -- method-owned finite response contracts
"""Bounded C2 judgment representations; overflow is never scientific completion."""

from __future__ import annotations

from typing import Any

from experiments.orchestration.workers.schema import AGGREGATE
from experiments.source_grounding.response import object_schema


def text(maximum: int) -> dict[str, Any]:
    """Bound a Unicode string without restricting its semantic vocabulary."""
    return {"type": "string", "minLength": 0, "maxLength": maximum}


def array(items: Any, maximum: int) -> dict[str, Any]:
    """Allow incomplete responses to report no entries rather than invent them."""
    return {"type": "array", "minItems": 0, "maxItems": maximum, "items": items}


def pass_a2(
    cells: int,
    source_keys: list[str],
    obligations: list[str],
    occurrence: int,
) -> Any:
    """Retain full per-cell capacities including the aggregate exact quote bound."""
    key = {"type": "string", "enum": source_keys}
    locator = object_schema(
        {
            "source_key": key,
            "quote": {"type": "string", "minLength": 1, "maxLength": 4096},
            "occurrence": {"type": "integer", "minimum": 1, "maximum": occurrence},
        },
    )
    locators = array(locator, 4)
    locators[AGGREGATE] = {"property": "quote", "maximum": 4096}
    cell = object_schema(
        {
            "source_key": key,
            "obligation_id": {"type": "string", "enum": obligations},
            "resolution_state": {
                "type": "string",
                "enum": ["EVIDENCE_FOUND", "REMAINS_UNCERTAIN"],
            },
            "semantic_statement": text(512),
            "locators": locators,
            "uncertainty_note": text(256),
            "representation_complete": {"type": "boolean"},
        },
    )
    return object_schema(
        {
            "cells": array(cell, cells),
            "self_review": text(256),
            "representation_complete": {"type": "boolean"},
        },
    )


def pass_b(cells: int, obligations: list[str]) -> Any:
    """Allocate generous explicit two-obligation unit/alternative/gap capacity.

    Eight units, eight alternatives per unit and four conjunctive evidence
    references per alternative are representational capacities, not claims that
    real science necessarily fits. Inadequacy requires incomplete representation.
    Existing million-combination witness safeguards remain independently binding.
    """
    cell = {"type": "string", "minLength": 5, "maxLength": 5, "pattern": "^[ce][0-9]+$"}
    evidence = {
        "type": "string",
        "minLength": 6,
        "maxLength": 6,
        "pattern": "^[ce][0-9]+$",
    }
    reference = object_schema({"cell_id": cell, "evidence_id": evidence})
    unit = object_schema(
        {
            "id": {
                "type": "string",
                "minLength": 2,
                "maxLength": 8,
                "pattern": "^U[0-9]+$",
            },
            "obligation": {"type": "string", "enum": obligations},
            "statement": text(256),
            "basis": {
                "type": "string",
                "enum": [
                    "TASK_BACKED",
                    "REPOSITORY_SUPPORTED",
                    "TASK_AND_REPOSITORY_SUPPORTED",
                ],
            },
            "necessity": text(256),
            "alternatives": array(array(reference, 4), 8),
        },
    )
    gaps = object_schema(
        {
            "TASK_INTERPRETATION_GAP": text(384),
            "TASK_GAP": text(384),
            "REPOSITORY_INFORMATION_GAP": text(384),
            "unconditional_sufficiency": {"type": "boolean"},
            "qualification": text(512),
        },
    )
    return object_schema(
        {
            "units": array(unit, 8),
            "gaps": gaps,
            "unresolved_cells": array(cell, cells),
            "self_review": text(512),
            "representation_complete": {"type": "boolean"},
        },
    )
