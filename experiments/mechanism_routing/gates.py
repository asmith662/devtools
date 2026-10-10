# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- formatter owns commas; frozen integer gates
"""Prospective U3 decision arithmetic; observations are unavailable at Stage A."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GateEvidence:
    """Supply independently validated later evidence, never router inputs."""

    contract_valid: bool
    router_sound: bool
    reach_safe: bool
    obligation_safe: bool
    preserves_b_gains: bool
    b_meaningful_gain_count: int
    invocations_b: int
    invocations_c: int
    mechanism_ns_b: int
    mechanism_ns_c: int
    charged_ns_b: int
    charged_ns_c: int
    unique_b: int
    unique_c: int
    bytes_b: int
    bytes_c: int
    positive_selective_value: bool

    def __post_init__(self) -> None:
        """Reject undefined denominator substitution and negative measurements."""
        integers = (
            self.b_meaningful_gain_count,
            self.invocations_b,
            self.invocations_c,
            self.mechanism_ns_b,
            self.mechanism_ns_c,
            self.charged_ns_b,
            self.charged_ns_c,
            self.unique_b,
            self.unique_c,
            self.bytes_b,
            self.bytes_c,
        )
        if any(value < 0 for value in integers):
            raise ValueError("Gate evidence cannot contain negative values")


def evaluate(e: GateEvidence) -> dict[str, bool | str]:
    """Use exact cross-products and frozen precedence; equality is not support."""
    invocation_reduction = (
        e.invocations_b > 0 and 4 * e.invocations_c <= 3 * e.invocations_b
    )
    mechanism_reduction = (
        e.mechanism_ns_b > 0 and 10 * e.mechanism_ns_c <= 9 * e.mechanism_ns_b
    )
    cost_safe = e.charged_ns_b > 0 and 20 * e.charged_ns_c <= 21 * e.charged_ns_b
    preserve_and_reduce = (
        e.b_meaningful_gain_count > 0
        and e.preserves_b_gains
        and invocation_reduction
        and mechanism_reduction
        and cost_safe
    )
    burden_gain = (
        e.unique_b > 0
        and 10 * e.unique_c <= 9 * e.unique_b
        and e.bytes_c <= e.bytes_b
        and e.charged_ns_b > 0
        and e.charged_ns_c <= e.charged_ns_b
    )
    safety = e.reach_safe and e.obligation_safe
    if not e.contract_valid:
        outcome = "EXPERIMENTAL_CONTRACT_DEFECT"
    elif not e.router_sound or not safety:
        outcome = "ROUTER_DEFECT"
    elif preserve_and_reduce or burden_gain:
        outcome = "SELECTIVE_MECHANISM_ROUTING_SUPPORTED"
    elif e.positive_selective_value:
        outcome = "COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER"
    else:
        outcome = "NO_MATERIAL_VALUE"
    return {
        "scientific_contract": e.contract_valid,
        "router_soundness": e.router_sound,
        "required_reach_safety": e.reach_safe,
        "obligation_safety": e.obligation_safe,
        "invocations_25_percent_reduction": invocation_reduction,
        "mechanism_cost_10_percent_reduction": mechanism_reduction,
        "charged_cost_within_5_percent": cost_safe,
        "preserve_b_gains_and_reduce": preserve_and_reduce,
        "burden_10_percent_gain_without_cost_increase": burden_gain,
        "outcome": outcome,
    }
