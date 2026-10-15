# Copyright (c) 2026

"""Certificates bind a workload/profile, not an inferred absolute maximum."""

from copy import deepcopy
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.workers import capacity, runtime
from experiments.orchestration.workers.budget import BudgetError


def config() -> dict[str, Any]:
    """Create metadata only; no external process or model is invoked."""
    return {
        "model_id": "gpt-6-astra",
        "reasoning": "High",
        "runtime": runtime.configuration(),
        "bounded_response": True,
    }


def receipt() -> dict[str, Any]:
    """Build a synthetic certificate for pure validation tests only."""
    profile = capacity.profile(config())
    return {
        "schema": capacity.SCHEMA,
        "status": "PASS",
        "engineering_only": True,
        "profile": profile,
        "profile_sha256": digest(json_bytes(profile)),
        "method_response_maximum_bytes": 65536,
        "input_characters": 700000,
        "input_bytes": 700000,
        "response_bytes": 59752,
        "checks": dict.fromkeys(
            [
                "process",
                "sole_response",
                "schema",
                "zero_tools",
                "empty_cwd",
                "final_agreement",
                "usage",
                "not_truncated",
                "single_invocation",
            ],
            True,
        ),
    }


def test_empirical_envelope_and_dynamic_rejection() -> None:
    """Unknown absolute output/context maxima need not become invented numbers."""
    value = receipt()
    capacity.authenticate(value, config())
    capacity.check_input(value, config(), b"x" * 700000)
    with pytest.raises(BudgetError, match="WORKLOAD_CAPACITY_LIMIT"):
        capacity.check_input(value, config(), b"x" * 700001)
    with pytest.raises(BudgetError, match="WORKLOAD_CAPACITY_LIMIT"):
        capacity.check_input(value, config(), ("\U0001f600" * 200000).encode())


@pytest.mark.parametrize(
    "mutation",
    ["profile", "output", "input", "checks", "model", "runtime"],
)
def test_incompatible_and_inadequate_evidence_rejects(mutation: str) -> None:
    """No stale receipt or weaker permission/model profile is accepted."""
    value, configuration = deepcopy(receipt()), config()
    if mutation == "profile":
        value["profile"]["python"] = "other"
    elif mutation == "output":
        value["response_bytes"] = 100
    elif mutation == "input":
        value["input_characters"] = 699999
    elif mutation == "checks":
        value["checks"]["zero_tools"] = False
    elif mutation == "model":
        configuration["model_id"] = "gpt-6-sol"
    else:
        configuration["runtime"] = {"weak": True}
    with pytest.raises(ValueError, match=r"profile|envelope|evidence"):
        capacity.authenticate(value, configuration)
