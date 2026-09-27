# Copyright (c) 2026
# ruff: noqa: EM101, TRY003
"""Experiment-local validation for exact frozen retrieval judgment coverage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

JudgmentIdentity = tuple[str, str, str, str, str]
NeutralTargetIdentity = tuple[str, str]


def judgment_identity(row: Mapping[str, Any]) -> JudgmentIdentity:
    """Return the frozen purpose/query/snapshot/address/semantics identity."""
    need = row["information_need"]
    return (
        str(need["purpose"]),
        str(need["lexical_query"]),
        str(row["parent_snapshot_sha"]),
        str(row["address"]),
        str(row["usefulness_semantics"]),
    )


def neutral_target_identity(row: Mapping[str, Any]) -> NeutralTargetIdentity:
    """Return a neutral target key used to bind a decision to its frozen row."""
    return (str(row["neutral_case_id"]), str(row["neutral_resource_id"]))


def validate_neutral_target_coverage(
    targets: Iterable[Mapping[str, Any]],
    expected: Iterable[NeutralTargetIdentity] | None = None,
) -> dict[NeutralTargetIdentity, Mapping[str, Any]]:
    """Index frozen neutral targets and optionally enforce the expected set."""
    indexed: dict[NeutralTargetIdentity, Mapping[str, Any]] = {}
    identities: set[JudgmentIdentity] = set()
    for target in targets:
        neutral = neutral_target_identity(target)
        identity = judgment_identity(target)
        if neutral in indexed or identity in identities:
            raise ValueError("Frozen neutral judgment targets contain duplicates.")
        indexed[neutral] = target
        identities.add(identity)
    if expected is not None and set(indexed) != set(expected):
        raise ValueError(
            "Frozen neutral targets differ from expected unresolved pairs.",
        )
    return indexed


def validate_frozen_judgment_coverage(
    targets: Iterable[Mapping[str, Any]],
    decisions: Iterable[Mapping[str, Any]],
    states: Iterable[str],
    expected_targets: Iterable[NeutralTargetIdentity] | None = None,
) -> dict[JudgmentIdentity, Mapping[str, Any]]:
    """Validate exact target/decision identity coverage and return outcomes."""
    frozen = validate_neutral_target_coverage(targets, expected_targets)
    allowed_states = set(states)
    outcomes: dict[JudgmentIdentity, Mapping[str, Any]] = {}
    seen_neutral: set[NeutralTargetIdentity] = set()
    for decision in decisions:
        neutral = neutral_target_identity(decision)
        target = frozen.get(neutral)
        identity = judgment_identity(decision)
        rationale = decision.get("rationale")
        if (
            target is None
            or neutral in seen_neutral
            or judgment_identity(target) != identity
            or decision.get("judgment") not in allowed_states
            or not isinstance(rationale, str)
            or not rationale.strip()
            or identity in outcomes
        ):
            raise ValueError("Frozen judgment does not match an exact neutral target.")
        seen_neutral.add(neutral)
        outcomes[identity] = decision
    if seen_neutral != set(frozen):
        raise ValueError("Frozen judgment coverage is incomplete.")
    return outcomes


def validated_outcome_mappings(
    reused: Iterable[Mapping[str, Any]],
    new: Mapping[JudgmentIdentity, Mapping[str, Any]],
) -> tuple[
    dict[JudgmentIdentity, Mapping[str, Any]],
    dict[JudgmentIdentity, Mapping[str, Any]],
]:
    """Index reused outcomes and reject duplicates or overlap with new outcomes."""
    reused_by_identity: dict[JudgmentIdentity, Mapping[str, Any]] = {}
    for row in reused:
        identity = judgment_identity(row)
        if identity in reused_by_identity:
            raise ValueError("Reused frozen judgments contain duplicate identities.")
        reused_by_identity[identity] = row
    if set(reused_by_identity) & set(new):
        raise ValueError("Reused and new frozen judgments overlap.")
    return reused_by_identity, dict(new)
