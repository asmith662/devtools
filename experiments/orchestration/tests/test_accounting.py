# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004 -- synthetic reported usage, no model call
"""Scientific acceptance is mandatory accounting, not transient display telemetry."""

import json
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration
from experiments.orchestration.workers import accounting, measurement


def capture() -> dict[str, Any]:
    result = SimpleNamespace(
        duration=Duration.seconds(2),
        stdout=json.dumps(
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 20,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 10,
                    "reasoning_output_tokens": 3,
                },
            },
        ).encode(),
    )
    return measurement.capture(
        {"model_id": "fake", "reasoning": "High"},
        "SYNTHETIC",
        "original-invocation",
        b"input",
        result,
        b"{}",
        validated=True,
        failure=None,
    )


def test_acceptance_is_separate_and_adoption_is_counted_once() -> None:
    value = capture()
    accepted = accounting.accept(value, "SYNTHETIC-ENGINEERING")
    assert value["measurement"]["accepted"] is False
    assert accepted["measurement"]["accepted"] is True
    adopted = accounting.adopted(accepted, "a" * 64)
    assert (
        adopted["measurement"]["invocation_id"]
        == accepted["measurement"]["invocation_id"]
    )
    total = accounting.aggregate((accepted, adopted))
    assert total.invocations == 1
    assert total.input_tokens == 100
    assert total.cached_input_tokens == 20
    assert total.reasoning_tokens == 3
    adopted["measurement"]["usage"]["input_tokens"] = 101
    with pytest.raises(ValueError, match="Conflicting"):
        accounting.aggregate((accepted, adopted))


def test_unknown_and_failed_usage_is_preserved_but_not_accepted() -> None:
    value = capture()
    value["measurement"]["usage"]["input_tokens"] = None
    assert accounting.aggregate((value,)).input_tokens is None
    with pytest.raises(ValueError, match="UNKNOWN"):
        accounting.accept(value, "mandatory")
    value["measurement"]["completed"] = False
    with pytest.raises(ValueError, match="Completed"):
        accounting.accept(value, "mandatory")
