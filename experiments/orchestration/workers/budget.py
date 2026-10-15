# Copyright (c) 2026
# ruff: noqa: ANN401, PLC0415 -- explicit receipt compatibility; lazy import avoids cycle
"""Exact pre-entry semantic capacities; characters, bytes and tokens stay distinct."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Any


class FailureClass(StrEnum):
    """Closed capacity and evidence-representation failure vocabulary."""

    TRANSPORT_CHARACTER_LIMIT = "TRANSPORT_CHARACTER_LIMIT"
    MODEL_CONTEXT_LIMIT = "MODEL_CONTEXT_LIMIT"
    UNKNOWN_CONTEXT_LIMIT = "UNKNOWN_CONTEXT_LIMIT"
    OUTPUT_SCHEMA_LIMIT = "OUTPUT_SCHEMA_LIMIT"
    OUTPUT_LIMIT = "OUTPUT_LIMIT"
    EVIDENCE_REPRESENTATION_LIMIT = "EVIDENCE_REPRESENTATION_LIMIT"
    WORKLOAD_CAPACITY_LIMIT = "WORKLOAD_CAPACITY_LIMIT"
    SEMANTIC_INVOCATION_BUDGET = "SEMANTIC_INVOCATION_BUDGET"


class BudgetError(ValueError):
    """A failed pre-entry check; never an execution or retry receipt."""

    def __init__(self, category: FailureClass, detail: str) -> None:
        """Retain actionable category separately from human diagnostic text."""
        self.category = category
        super().__init__(f"{category}: {detail}")


@dataclass(frozen=True)
class BudgetSpec:
    """Frozen invocation capacities and the sources of claims about them."""

    runtime_identity: str
    model: str
    reasoning: str
    execution_profile: str
    transport_characters: int
    transport_provenance: str
    safety_characters: int
    schema_bytes_limit: int
    response_bytes_limit: int
    context_tokens: int | None = None
    context_provenance: str = "UNKNOWN"
    estimated_input_tokens: int | None = None
    estimator_identity: str = "UNKNOWN"
    reserved_output_reasoning_tokens: int | None = None
    unknown_context_allowed: bool = False
    output_tokens_limit: int | None = None
    output_limit_provenance: str = "UNKNOWN"
    response_token_upper_bound: int | None = None
    output_estimator_identity: str = "UNKNOWN"
    reserved_reasoning_tokens: int | None = None

    def __post_init__(self) -> None:
        """Reject invalid bounds or an estimate without an identified estimator."""
        if (
            self.transport_characters <= self.safety_characters
            or self.safety_characters < 0
            or self.schema_bytes_limit <= 0
            or self.response_bytes_limit <= 0
            or not self.transport_provenance
            or (
                self.estimated_input_tokens is not None
                and self.estimator_identity == "UNKNOWN"
            )
            or any(
                value is not None and value < 0
                for value in (
                    self.context_tokens,
                    self.estimated_input_tokens,
                    self.reserved_output_reasoning_tokens,
                    self.output_tokens_limit,
                    self.response_token_upper_bound,
                    self.reserved_reasoning_tokens,
                )
            )
        ):
            message = "Invalid semantic budget specification"
            raise ValueError(message)

    @property
    def identity(self) -> str:
        """Any policy/bound change changes the prospective partition binding."""
        return sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class BudgetResult:
    """Exact rendered-input/schema observations, never a scientific outcome."""

    specification_sha256: str
    input_sha256: str
    input_characters: int
    input_bytes: int
    schema_sha256: str
    schema_characters: int
    schema_bytes: int
    counting_status: str = "EXACT"


def check(spec: BudgetSpec, rendered: bytes, schema: bytes) -> BudgetResult:
    """Validate already-rendered UTF-8 bytes before an ENTERED journal exists."""
    chars = len(rendered.decode("utf-8", errors="strict"))
    schema_chars = len(schema.decode("utf-8", errors="strict"))
    maximum = spec.transport_characters - spec.safety_characters
    if chars > maximum:
        raise BudgetError(
            FailureClass.TRANSPORT_CHARACTER_LIMIT,
            f"input={chars} chars/{len(rendered)} bytes; allowed={maximum}",
        )
    if len(schema) > spec.schema_bytes_limit:
        raise BudgetError(FailureClass.OUTPUT_SCHEMA_LIMIT, "Response schema too large")
    known = (
        spec.context_tokens,
        spec.estimated_input_tokens,
        spec.reserved_output_reasoning_tokens,
    )
    if None in known:
        if not spec.unknown_context_allowed:
            raise BudgetError(
                FailureClass.UNKNOWN_CONTEXT_LIMIT,
                "Context/estimator/output reservation unavailable",
            )
    else:
        context, estimate, reserve = (value for value in known if value is not None)
        if estimate + reserve > context:
            raise BudgetError(
                FailureClass.MODEL_CONTEXT_LIMIT,
                "Context budget exceeded",
            )
    return BudgetResult(
        spec.identity,
        sha256(rendered).hexdigest(),
        chars,
        len(rendered),
        sha256(schema).hexdigest(),
        schema_chars,
        len(schema),
    )


def check_response(spec: BudgetSpec, response: bytes) -> None:
    """Capacity failure is separate from semantic/schema acceptance."""
    if len(response) > spec.response_bytes_limit:
        raise BudgetError(FailureClass.OUTPUT_LIMIT, "Retained response exceeds bound")


def require_output_ready(
    spec: BudgetSpec,
    *,
    receipt: Any = None,
    configuration: Any = None,
) -> None:
    """Require identified output capacity, representation bound and reservation.

    A local retained-byte ceiling is not a provider output reservation. Published
    API model limits do not establish an active external-Agent runtime profile.
    """
    if receipt is not None:
        from experiments.orchestration.workers.capacity import authenticate
        from experiments.orchestration.workers.schema import (
            MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
        )

        authenticate(receipt, configuration)
        if spec.response_bytes_limit > MAX_SEMANTIC_RESPONSE_UTF8_BYTES:
            raise BudgetError(
                FailureClass.OUTPUT_LIMIT,
                "Method response envelope exceeded",
            )
        return
    values = (
        spec.output_tokens_limit,
        spec.response_token_upper_bound,
        spec.reserved_reasoning_tokens,
    )
    if (
        any(value is None for value in values)
        or spec.output_limit_provenance == "UNKNOWN"
        or spec.output_estimator_identity == "UNKNOWN"
    ):
        raise BudgetError(
            FailureClass.OUTPUT_LIMIT,
            "Output readiness UNKNOWN: runtime output capacity, authenticated "
            "response-token bound and reasoning reservation are required",
        )
    limit, response, reasoning = (value for value in values if value is not None)
    if limit <= 0 or response < 0 or reasoning < 0 or response + reasoning > limit:
        raise BudgetError(
            FailureClass.OUTPUT_LIMIT,
            f"Output bound plus reservation exceeds capacity: "
            f"{response}+{reasoning}>{limit}",
        )
