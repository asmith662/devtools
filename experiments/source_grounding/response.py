# Copyright (c) 2026
# ruff: noqa: ANN401 -- fixed primary-response JSON schemas
"""Native structured judgments; scientific validation remains in reviewer.py."""

from __future__ import annotations

from typing import Any

from experiments.source_grounding import contracts


def object_schema(properties: dict[str, Any]) -> Any:
    """Declare exactly the maintained primary object fields."""
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def array_schema(items: Any) -> Any:
    """Declare homogeneous arrays; completeness remains packet-owned."""
    return {"type": "array", "items": items}


def schema(*, gold: bool) -> Any:
    """Keep grounding and blind-gold response vocabularies separate."""
    text = {"type": "string"}
    span = object_schema(
        {
            "source_key": text,
            "quote": text,
            "occurrence": {"type": "integer"},
        },
    )
    common = {
        "obligation": text,
        "source_key": text,
        "spans": array_schema(span),
        "reason": text,
    }
    if gold:
        cell = object_schema(
            {**common, "label": {"type": "string", "enum": list(contracts.LABELS)}},
        )
        unit = object_schema(
            {
                "id": text,
                "obligation": text,
                "statement": text,
                "basis": {
                    "type": "string",
                    "enum": [
                        "TASK_BACKED",
                        "REPOSITORY_SUPPORTED",
                        "TASK_AND_REPOSITORY_SUPPORTED",
                    ],
                },
                "necessity": text,
                "alternatives": array_schema(array_schema(span)),
            },
        )
        gaps = object_schema(
            {
                "TASK_INTERPRETATION_GAP": text,
                "TASK_GAP": text,
                "REPOSITORY_INFORMATION_GAP": text,
                "unconditional_sufficiency": {"type": "boolean"},
                "qualification": text,
            },
        )
    else:
        cell = object_schema(
            {
                **common,
                "verdict": {"type": "string", "enum": list(contracts.VERDICTS)},
                "statement": text,
                "assumptions": array_schema(text),
                "uncertainty": text,
                "additional_information": text,
            },
        )
        unit, gaps = text, array_schema(text)
    return object_schema(
        {
            "cells": array_schema(cell),
            "units": array_schema(unit),
            "gaps": gaps,
            "self_review": text,
        },
    )
