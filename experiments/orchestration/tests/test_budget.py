# Copyright (c) 2026
# ruff: noqa: S101, PLR2004 -- deterministic capacity fixtures
"""Budget failures precede entry and do not infer unknown token capacities."""

from dataclasses import replace
from typing import Any

import pytest

from experiments.orchestration.workers.budget import (
    BudgetError,
    BudgetSpec,
    FailureClass,
    check,
    check_response,
    require_output_ready,
)


def spec() -> BudgetSpec:
    """Bind an explicitly unknown-context synthetic policy."""
    return BudgetSpec(
        "synthetic-runtime",
        "synthetic-model",
        "High",
        "SEMANTIC_WORKER",
        100,
        "EMPIRICALLY_OBSERVED:synthetic-fixture",
        10,
        100,
        100,
    )


def test_exact_unicode_bytes_schema_and_explicit_unknown_policy() -> None:
    """A Unicode character, its UTF8 bytes and token estimate are distinct."""
    with pytest.raises(BudgetError) as error:
        check(spec(), b"x", b"{}")
    assert error.value.category == FailureClass.UNKNOWN_CONTEXT_LIMIT
    result = check(
        replace(spec(), unknown_context_allowed=True),
        "\U0001f600".encode(),
        b"{}",
    )
    assert result.input_characters == 1
    assert result.input_bytes == 4
    assert result.schema_characters == result.schema_bytes == 2
    assert result.counting_status == "EXACT"
    assert result.specification_sha256 != replace(spec(), safety_characters=11).identity


def test_known_context_and_all_capacity_failures() -> None:
    """Failure categories remain actionable without launching a process."""
    policy = replace(
        spec(),
        context_tokens=100,
        estimated_input_tokens=80,
        estimator_identity="identified-test-estimator",
        reserved_output_reasoning_tokens=20,
    )
    assert check(policy, b"x", b"{}").input_characters == 1
    for candidate, raw, schema, category in [
        (policy, b"x" * 91, b"{}", FailureClass.TRANSPORT_CHARACTER_LIMIT),
        (policy, b"x", b"x" * 101, FailureClass.OUTPUT_SCHEMA_LIMIT),
        (
            replace(policy, estimated_input_tokens=81),
            b"x",
            b"{}",
            FailureClass.MODEL_CONTEXT_LIMIT,
        ),
    ]:
        with pytest.raises(BudgetError) as error:
            check(candidate, raw, schema)
        assert error.value.category == category
    check_response(policy, b"x" * 100)
    with pytest.raises(BudgetError) as error:
        check_response(policy, b"x" * 101)
    assert error.value.category == FailureClass.OUTPUT_LIMIT
    with pytest.raises(UnicodeError):
        check(policy, b"\xff", b"{}")


@pytest.mark.parametrize(
    "changes",
    [
        {"safety_characters": -1},
        {"safety_characters": 100},
        {"schema_bytes_limit": 0},
        {"response_bytes_limit": 0},
        {"transport_provenance": ""},
        {"estimated_input_tokens": 1},
        {"context_tokens": -1},
    ],
)
def test_invalid_budget_specification_rejected(changes: dict[str, Any]) -> None:
    """Invalid policy must not become a successful capacity receipt."""
    with pytest.raises(ValueError, match="specification"):
        replace(spec(), **changes)


def test_retained_bytes_do_not_establish_runtime_output_readiness() -> None:
    """Unknown output capacity cannot become ready through a host buffer limit."""
    with pytest.raises(BudgetError, match="Output readiness UNKNOWN"):
        require_output_ready(spec())
    ready = replace(
        spec(),
        output_tokens_limit=100,
        output_limit_provenance="REPORTED:synthetic-runtime-profile",
        response_token_upper_bound=60,
        output_estimator_identity="authenticated-synthetic-upper-bound",
        reserved_reasoning_tokens=40,
    )
    require_output_ready(ready)
    with pytest.raises(BudgetError, match="exceeds capacity"):
        require_output_ready(replace(ready, response_token_upper_bound=61))
