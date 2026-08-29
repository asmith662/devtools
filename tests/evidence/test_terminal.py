# Copyright (c) 2026
"""Tests for immutable terminal Attempt Evidence values."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from devtools import evidence
from devtools.evidence import (
    Attempt,
    AttemptCancelled,
    AttemptFailed,
    AttemptId,
    AttemptObserver,
    AttemptStage,
    AttemptState,
    AttemptSucceeded,
    AttemptTerminalEvidence,
    AttemptTerminalOutcome,
    EvidenceId,
    terminal,
)
from devtools.evidence.terminal import (
    AttemptCancelled as AttemptCancelledFromSubmodule,
)
from devtools.evidence.terminal import AttemptFailed as AttemptFailedFromSubmodule
from devtools.evidence.terminal import AttemptStage as AttemptStageFromSubmodule
from devtools.evidence.terminal import AttemptSucceeded as AttemptSucceededFromSubmodule
from devtools.evidence.terminal import (
    AttemptTerminalEvidence as AttemptTerminalEvidenceFromSubmodule,
)
from devtools.evidence.terminal import (
    AttemptTerminalOutcome as AttemptTerminalOutcomeFromSubmodule,
)
from devtools.evidence.terminal import EvidenceId as EvidenceIdFromSubmodule
from devtools.identity import Identity
from devtools.time import Timestamp


def _timestamp(offset: int = 0) -> Timestamp:
    """Return one deterministic UTC timestamp."""
    value = datetime(2026, 8, 23, 12, 0, tzinfo=UTC)
    return Timestamp(value + timedelta(seconds=offset))


def test_terminal_root_and_submodule_api_are_canonical() -> None:
    """Terminal Evidence public imports preserve canonical type identities."""
    assert EvidenceId is EvidenceIdFromSubmodule
    assert AttemptStage is AttemptStageFromSubmodule
    assert AttemptSucceeded is AttemptSucceededFromSubmodule
    assert AttemptFailed is AttemptFailedFromSubmodule
    assert AttemptCancelled is AttemptCancelledFromSubmodule
    assert AttemptTerminalEvidence is AttemptTerminalEvidenceFromSubmodule
    assert AttemptTerminalOutcome is AttemptTerminalOutcomeFromSubmodule
    assert evidence.__all__ == [
        "Attempt",
        "AttemptCancelled",
        "AttemptFailed",
        "AttemptId",
        "AttemptObserver",
        "AttemptStage",
        "AttemptState",
        "AttemptSucceeded",
        "AttemptTerminalEvidence",
        "AttemptTerminalOutcome",
        "EvidenceId",
        "EvidenceSink",
    ]
    assert evidence.Attempt is Attempt
    assert evidence.AttemptId is AttemptId
    assert evidence.AttemptObserver is AttemptObserver
    assert evidence.AttemptState is AttemptState


def test_terminal_submodule_declares_its_exact_public_api() -> None:
    """Terminal wildcard exports exclude implementation imports."""
    assert terminal.__all__ == [
        "AttemptCancelled",
        "AttemptFailed",
        "AttemptStage",
        "AttemptSucceeded",
        "AttemptTerminalEvidence",
        "AttemptTerminalOutcome",
        "EvidenceId",
    ]


def test_evidence_id_is_an_immutable_semantic_identity() -> None:
    """EvidenceId follows the existing semantic Identity-wrapper contract."""
    parsed = EvidenceId.parse("12345678-1234-5678-1234-567812345678")
    equivalent = EvidenceId(Identity.parse(str(parsed)))
    generated = EvidenceId.new()

    expected_uuid_version = len(("one", "two", "three", "four"))

    assert generated.value.value.version == expected_uuid_version
    assert str(parsed) == "12345678-1234-5678-1234-567812345678"
    assert parsed == equivalent
    assert hash(parsed) == hash(equivalent)
    with pytest.raises(ValueError, match="badly formed"):
        EvidenceId.parse("not-a-uuid")
    with pytest.raises(FrozenInstanceError):
        parsed.value = Identity.new()  # type: ignore[misc]


def test_evidence_id_accepts_non_v4_identity_text() -> None:
    """EvidenceId preserves generic Identity UUID-version parsing behavior."""
    parsed = EvidenceId.parse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

    assert parsed.value.value.version == 1
    assert str(parsed) == "6ba7b810-9dad-11d1-80b4-00c04fd430c8"


def test_attempt_stage_has_exact_stable_members() -> None:
    """Stages describe only stable Runtime processing boundaries."""
    assert tuple(AttemptStage) == (
        AttemptStage.ADMISSION,
        AttemptStage.CONTINUATION_LOOKUP,
        AttemptStage.AGENT_INVOCATION,
        AttemptStage.RESULT_VALIDATION,
        AttemptStage.OUTPUT_RETENTION,
        AttemptStage.CONTINUATION_REPLACEMENT,
    )
    assert [stage.value for stage in AttemptStage] == [
        "admission",
        "continuation_lookup",
        "agent_invocation",
        "result_validation",
        "output_retention",
        "continuation_replacement",
    ]


def test_terminal_outcomes_are_immutable_hashable_typed_values() -> None:
    """Success, failure, and cancellation remain minimal typed outcome values."""
    succeeded = AttemptSucceeded()
    failed = AttemptFailed(AttemptStage.AGENT_INVOCATION)
    cancelled = AttemptCancelled(AttemptStage.RESULT_VALIDATION)
    outcomes: tuple[AttemptTerminalOutcome, ...] = (
        succeeded,
        failed,
        cancelled,
    )

    assert outcomes == (
        AttemptSucceeded(),
        AttemptFailed(AttemptStage.AGENT_INVOCATION),
        AttemptCancelled(AttemptStage.RESULT_VALIDATION),
    )
    assert all(hash(outcome) == hash(outcome) for outcome in outcomes)
    with pytest.raises(FrozenInstanceError):
        failed.stage = AttemptStage.OUTPUT_RETENTION  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        cancelled.stage = AttemptStage.OUTPUT_RETENTION  # type: ignore[misc]


def test_attempt_succeeded_is_an_empty_typed_value() -> None:
    """Successful outcomes intentionally carry no semantic fields."""
    assert AttemptSucceeded.__dataclass_fields__ == {}
    with pytest.raises(TypeError):
        AttemptSucceeded("unexpected")  # type: ignore[call-arg]


def test_attempt_failed_requires_stage() -> None:
    """Failed outcomes require an explicit Runtime boundary."""
    with pytest.raises(TypeError):
        AttemptFailed()  # type: ignore[call-arg]


def test_attempt_cancelled_requires_stage() -> None:
    """Cancelled outcomes require an explicit Runtime boundary."""
    with pytest.raises(TypeError):
        AttemptCancelled()  # type: ignore[call-arg]


def test_terminal_evidence_reconstructs_as_an_immutable_value() -> None:
    """Direct reconstruction retains factual values without time-order validation."""
    identifier = EvidenceId.parse("10000000-0000-4000-8000-000000000001")
    attempt_id = AttemptId.parse("20000000-0000-4000-8000-000000000001")
    outcome = AttemptFailed(AttemptStage.OUTPUT_RETENTION)
    record = AttemptTerminalEvidence(
        id=identifier,
        attempt_id=attempt_id,
        occurred_at=_timestamp(1),
        observed_at=_timestamp(),
        outcome=outcome,
    )
    equivalent = AttemptTerminalEvidence(
        id=identifier,
        attempt_id=attempt_id,
        occurred_at=_timestamp(1),
        observed_at=_timestamp(),
        outcome=outcome,
    )

    assert record.id is identifier
    assert record.attempt_id is attempt_id
    assert record.outcome is outcome
    assert record.observed_at.value < record.occurred_at.value
    assert record is not equivalent
    assert record == equivalent
    assert hash(record) == hash(equivalent)
    with pytest.raises(FrozenInstanceError):
        record.id = EvidenceId.new()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        record.attempt_id = AttemptId.new()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        record.occurred_at = _timestamp()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        record.observed_at = _timestamp()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        record.outcome = AttemptSucceeded()  # type: ignore[misc]


def test_terminal_evidence_new_owns_identity_and_observation_time() -> None:
    """The factory preserves supplied facts while allocating record facts."""
    attempt_id = AttemptId.parse("20000000-0000-4000-8000-000000000001")
    occurred_at = _timestamp()
    outcome = AttemptCancelled(AttemptStage.AGENT_INVOCATION)

    first = AttemptTerminalEvidence.new(
        attempt_id=attempt_id,
        occurred_at=occurred_at,
        outcome=outcome,
    )
    second = AttemptTerminalEvidence.new(
        attempt_id=attempt_id,
        occurred_at=occurred_at,
        outcome=outcome,
    )

    assert isinstance(first, AttemptTerminalEvidence)
    assert isinstance(first.id, EvidenceId)
    assert first.id != second.id
    assert first.attempt_id is attempt_id
    assert first.occurred_at is occurred_at
    assert isinstance(first.observed_at, Timestamp)
    assert first.outcome is outcome
