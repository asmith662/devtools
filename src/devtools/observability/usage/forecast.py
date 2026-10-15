# Copyright (c) 2026
"""Transparent small-sample planning ranges, never tokenizer or billing claims."""

from __future__ import annotations

import math
from dataclasses import dataclass

from devtools.observability.evidence.invocation import (
    Availability,
    InvocationMeasurement,
)

SMALL_DISCLOSURE_BYTES = 1024


@dataclass(frozen=True, slots=True)
class TokenRange:
    """A planning bracket with explicit provenance, not a confidence interval."""

    lower: int | None
    upper: int | None
    availability: Availability
    provenance: str


@dataclass(frozen=True, slots=True)
class InvocationForecast:
    """One prospective fresh call and its exactly rendered disclosure size."""

    invocation: str
    model: str
    reasoning_effort: str
    execution_profile: str
    disclosed_characters: int
    disclosed_bytes: int
    disclosure_digest: str
    response_maximum_bytes: int
    input_tokens: TokenRange
    output_tokens: TokenRange
    observed_small_input_floor: TokenRange
    calibrations: tuple[str, ...]


def forecast(  # noqa: PLR0913 -- named independent invocation dimensions
    *,
    invocation: str,
    model: str,
    reasoning_effort: str,
    execution_profile: str,
    disclosed_characters: int,
    disclosed_bytes: int,
    disclosure_digest: str,
    response_maximum_bytes: int,
    calibrations: tuple[InvocationMeasurement, ...],
) -> InvocationForecast:
    """Use matched observed envelopes instead of fitting a model to three points.

    Input ranges span observed input counts, with zero as the conservative lower
    end if no measured small-input floor exists. Larger unobserved disclosures
    scale the observed upper bracket and are explicitly extrapolated. Output's
    generous one-token-per-byte planning ceiling is ESTIMATED, not an authenticated
    tokenizer bound. The actual measured categories remain separate evidence.
    """
    matched = tuple(
        m
        for m in calibrations
        if m.requested_model == model
        and m.reasoning_effort.casefold() == reasoning_effort.casefold()
        and m.execution_profile == execution_profile
    )
    input_known = []
    for m in matched:
        count, size = m.usage.input_tokens, m.disclosed_bytes.value
        if count is not None and size is not None and size > 0:
            input_known.append((count, size))
    tiny = tuple(count for count, size in input_known if size <= SMALL_DISCLOSURE_BYTES)
    unknown = TokenRange(
        None,
        None,
        Availability.UNKNOWN,
        "No compatible reported calibration",
    )
    floor = (
        TokenRange(
            min(tiny),
            max(tiny),
            Availability.REPORTED,
            "Observed small-disclosure calls; not proven fixed overhead",
        )
        if tiny
        else unknown
    )
    if input_known:
        max_bytes = max(size for _, size in input_known)
        largest = max(count for count, _ in input_known)
        scale = max(1.0, disclosed_bytes / max_bytes)
        input_estimate = TokenRange(
            floor.lower if tiny else 0,
            math.ceil(largest * scale),
            Availability.ESTIMATED,
            "LOW_CONFIDENCE_MATCHED_EMPIRICAL_BRACKET"
            + (
                "; EXTRAPOLATED_BYTES"
                if scale > 1
                else "; WITHIN_OBSERVED_BYTE_ENVELOPE"
            ),
        )
    else:
        input_estimate = unknown
    output_known = tuple(
        m.usage.output_tokens for m in matched if m.usage.output_tokens is not None
    )
    output_estimate = (
        TokenRange(
            0,
            max(response_maximum_bytes, *output_known),
            Availability.ESTIMATED,
            "LOW_CONFIDENCE_BYTE_PLANNING_CEILING; NOT_A_TOKENIZER_OR_CAPACITY_BOUND",
        )
        if output_known
        else unknown
    )
    return InvocationForecast(
        invocation,
        model,
        reasoning_effort,
        execution_profile,
        disclosed_characters,
        disclosed_bytes,
        disclosure_digest,
        response_maximum_bytes,
        input_estimate,
        output_estimate,
        floor,
        tuple(m.invocation_id for m in matched),
    )
