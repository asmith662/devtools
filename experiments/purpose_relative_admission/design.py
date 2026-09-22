# Copyright (c) 2026
# ruff: noqa: E501, I001
"""Frozen Increment-22 configuration, separate from surfacing and admission."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum

from experiments.purpose_relative_import.cases import PurposeRelativeNeed, purpose_relative_needs


class PurposeProfile(StrEnum):
    """Precommitted purpose profile; it is never inferred from query text."""

    LOCAL_DEFINITION_OR_GOVERNANCE = "local-definition-or-governance"
    OUTGOING_DEPENDENCY = "outgoing-dependency"
    INCOMING_CONSUMER_OR_TEST = "incoming-consumer-or-test"


class ExperimentPartition(StrEnum):
    """Precommitted calibration or held-out role."""

    CALIBRATION = "calibration"
    HELD_OUT = "held-out"


@dataclass(frozen=True, slots=True)
class FrozenAdmissionCase:
    """One existing need plus its immutable partition and purpose profile."""

    need: PurposeRelativeNeed
    partition: ExperimentPartition
    profile: PurposeProfile


@dataclass(frozen=True, slots=True)
class DirectResolutionControl:
    """Exact-name control excluded from heterogeneous five-resource metrics."""

    name: str
    declared_name: str


_ASSIGNMENTS = (
    ("filename-field-fusion", ExperimentPartition.CALIBRATION, PurposeProfile.OUTGOING_DEPENDENCY),
    ("resolution-becomes-relation", ExperimentPartition.CALIBRATION, PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE),
    ("lexical-span-semantics-without-expansion", ExperimentPartition.CALIBRATION, PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE),
    ("filesystem-tool-error-translation", ExperimentPartition.CALIBRATION, PurposeProfile.OUTGOING_DEPENDENCY),
    ("observation-resource-snapshot-flow", ExperimentPartition.HELD_OUT, PurposeProfile.OUTGOING_DEPENDENCY),
    ("public-relation-tests", ExperimentPartition.HELD_OUT, PurposeProfile.INCOMING_CONSUMER_OR_TEST),
    ("relation-source-availability", ExperimentPartition.HELD_OUT, PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE),
    ("observation-safe-change", ExperimentPartition.HELD_OUT, PurposeProfile.INCOMING_CONSUMER_OR_TEST),
    ("import-resolution-safe-change", ExperimentPartition.HELD_OUT, PurposeProfile.INCOMING_CONSUMER_OR_TEST),
    ("filesystem-translation-safe-change", ExperimentPartition.HELD_OUT, PurposeProfile.INCOMING_CONSUMER_OR_TEST),
    ("context-disclosure-architecture", ExperimentPartition.HELD_OUT, PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE),
    ("context-disclosure-implementation", ExperimentPartition.HELD_OUT, PurposeProfile.INCOMING_CONSUMER_OR_TEST),
)

_DIRECT_CONTROLS = (
    DirectResolutionControl("exact-name-disclosure", "disclose_python_function_exact_name_retrieval"),
    DirectResolutionControl("exact-name-rendering", "render_materialized_python_function_context"),
)


def frozen_admission_cases() -> tuple[FrozenAdmissionCase, ...]:
    """Bind existing frozen needs to the supplied immutable design mapping."""
    needs = {need.name: need for need in purpose_relative_needs()}
    return tuple(
        FrozenAdmissionCase(needs[name], partition, profile)
        for name, partition, profile in _ASSIGNMENTS
    )


def direct_resolution_controls() -> tuple[DirectResolutionControl, ...]:
    """Return controls whose exact lookup bypasses heterogeneous admission."""
    return _DIRECT_CONTROLS


def directional_reservation_v1_fingerprint() -> str:
    """Fingerprint every frozen behavior-affecting design input."""
    payload = {
        "semantics": "increment-22-directional-reservation-v1",
        "lexical_protected_ranks": [1, 2, 3, 4],
        "reservation_rank": 5,
        "seed_ranks": [1, 2, 3],
        "minimum_distinct_relation_supports": 2,
        "maximum_relationship_admissions": 1,
        "profile_direction": {
            PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE.value: None,
            PurposeProfile.OUTGOING_DEPENDENCY.value: "outgoing",
            PurposeProfile.INCOMING_CONSUMER_OR_TEST.value: "incoming",
        },
        "ordering": ["support-count-desc", "minimum-seed-rank-asc", "encounter-order-asc", "address-serialization-tie-break"],
        "assignments": [(name, partition.value, profile.value) for name, partition, profile in _ASSIGNMENTS],
        "direct_controls": [(control.name, control.declared_name) for control in _DIRECT_CONTROLS],
    }
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()
