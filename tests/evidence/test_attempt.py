# Copyright (c) 2026
"""Tests for application-level processing attempts."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from devtools import evidence
from devtools.context import MessageId, MessageSource, SessionId
from devtools.evidence import Attempt, AttemptId, AttemptObserver, AttemptState
from devtools.evidence.attempt import Attempt as AttemptFromSubmodule
from devtools.evidence.attempt import AttemptId as AttemptIdFromSubmodule
from devtools.evidence.attempt import AttemptState as AttemptStateFromSubmodule
from devtools.identity import Identity
from devtools.time import Timestamp

if TYPE_CHECKING:
    from collections.abc import Callable


def _timestamp(offset: int = 0) -> Timestamp:
    """Return one deterministic UTC timestamp."""
    value = datetime(2026, 8, 16, 12, 0, tzinfo=UTC)
    return Timestamp(value + timedelta(seconds=offset))


def _attempt(  # noqa: PLR0913
    *,
    id: AttemptId | None = None,  # noqa: A002
    session_id: SessionId | None = None,
    message_id: MessageId | None = None,
    agent_source: MessageSource | None = None,
    started_at: Timestamp | None = None,
    state: AttemptState = AttemptState.RUNNING,
    completed_at: Timestamp | None = None,
) -> Attempt:
    """Build one deterministic Attempt with configurable reconstruction state."""
    return Attempt(
        id=(
            id
            or AttemptId.parse("10000000-0000-4000-8000-000000000001")
        ),
        session_id=(
            session_id
            or SessionId.parse("20000000-0000-4000-8000-000000000001")
        ),
        message_id=(
            message_id
            or MessageId.parse("30000000-0000-4000-8000-000000000001")
        ),
        agent_source=agent_source or MessageSource("codex"),
        started_at=started_at or _timestamp(),
        state=state,
        completed_at=completed_at,
    )


def test_root_and_submodule_expose_the_same_attempt_types() -> None:
    """Evidence public imports are canonical type identities."""
    assert Attempt is AttemptFromSubmodule
    assert AttemptId is AttemptIdFromSubmodule
    assert AttemptState is AttemptStateFromSubmodule
    assert AttemptObserver is evidence.AttemptObserver
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
    ]


def test_attempt_id_is_an_immutable_semantic_identity() -> None:
    """AttemptId follows the existing semantic Identity-wrapper contract."""
    parsed = AttemptId.parse("12345678-1234-5678-1234-567812345678")
    equivalent = AttemptId(Identity.parse(str(parsed)))
    generated = AttemptId.new()
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert generated.value.value.version == expected_uuid_version
    assert str(parsed) == "12345678-1234-5678-1234-567812345678"
    assert parsed == equivalent
    assert hash(parsed) == hash(equivalent)

    with pytest.raises(ValueError, match="badly formed"):
        AttemptId.parse("not-a-uuid")
    with pytest.raises(FrozenInstanceError):
        parsed.value = Identity.new()  # type: ignore[misc]


def test_attempt_id_accepts_non_v4_identity_text() -> None:
    """AttemptId preserves generic Identity UUID-version parsing behavior."""
    non_v4 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

    parsed = AttemptId.parse(non_v4)

    assert parsed.value.value.version == 1
    assert str(parsed) == non_v4


def test_attempt_state_has_exact_stable_members() -> None:
    """Attempt lifecycle states are intentionally small and string-valued."""
    assert tuple(AttemptState) == (
        AttemptState.RUNNING,
        AttemptState.SUCCEEDED,
        AttemptState.FAILED,
        AttemptState.CANCELLED,
    )
    assert [state.value for state in AttemptState] == [
        "running",
        "succeeded",
        "failed",
        "cancelled",
    ]


def test_attempt_new_creates_running_lifecycle_with_exact_attribution() -> None:
    """Attempt.new creates fresh lifecycle state without embedding domain objects."""
    session_id = SessionId.parse("20000000-0000-4000-8000-000000000001")
    message_id = MessageId.parse("30000000-0000-4000-8000-000000000001")
    source = MessageSource("codex")

    attempt = Attempt.new(
        session_id=session_id,
        message_id=message_id,
        agent_source=source,
    )

    assert isinstance(attempt.id, AttemptId)
    assert attempt.session_id is session_id
    assert attempt.message_id is message_id
    assert attempt.agent_source is source
    assert isinstance(attempt.started_at, Timestamp)
    assert attempt.state is AttemptState.RUNNING
    assert attempt.completed_at is None


def test_attempt_properties_are_read_only() -> None:
    """Attribution and lifecycle state mutate only through lifecycle methods."""
    attempt = _attempt()

    with pytest.raises(AttributeError):
        attempt.id = AttemptId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.session_id = SessionId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.message_id = MessageId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.agent_source = MessageSource("qwen")  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.started_at = Timestamp.now()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.state = AttemptState.FAILED  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.completed_at = Timestamp.now()  # type: ignore[misc]


@pytest.mark.parametrize(
    ("method_name", "expected_state"),
    [
        ("succeed", AttemptState.SUCCEEDED),
        ("fail", AttemptState.FAILED),
        ("cancel", AttemptState.CANCELLED),
    ],
)
def test_attempt_terminal_methods_complete_running_lifecycle(
    method_name: str,
    expected_state: AttemptState,
) -> None:
    """Each semantic terminal method captures completion and preserves attribution."""
    attempt = _attempt()
    attribution = (
        attempt.id,
        attempt.session_id,
        attempt.message_id,
        attempt.agent_source,
        attempt.started_at,
    )
    method: Callable[[], None] = getattr(attempt, method_name)

    assert method() is None  # type: ignore[func-returns-value]
    assert attempt.state is expected_state
    assert isinstance(attempt.completed_at, Timestamp)
    assert (
        attempt.id,
        attempt.session_id,
        attempt.message_id,
        attempt.agent_source,
        attempt.started_at,
    ) == attribution


def test_attempt_completion_timestamp_failure_preserves_running_lifecycle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Timestamp failure does not partially terminalize the shared lifecycle path."""
    attempt = _attempt()
    attribution = (
        attempt.id,
        attempt.session_id,
        attempt.message_id,
        attempt.agent_source,
        attempt.started_at,
    )
    error = RuntimeError("timestamp unavailable")

    def raise_timestamp_error() -> Timestamp:
        raise error

    monkeypatch.setattr(
        "devtools.evidence.attempt.Timestamp.now",
        raise_timestamp_error,
    )

    with pytest.raises(RuntimeError) as raised:
        attempt.succeed()

    assert raised.value is error
    assert attempt.state is AttemptState.RUNNING
    assert attempt.completed_at is None
    assert (
        attempt.id,
        attempt.session_id,
        attempt.message_id,
        attempt.agent_source,
        attempt.started_at,
    ) == attribution


@pytest.mark.parametrize("first_method", ["succeed", "fail", "cancel"])
@pytest.mark.parametrize("later_method", ["succeed", "fail", "cancel"])
def test_attempt_rejects_all_terminal_retransitions(
    first_method: str,
    later_method: str,
) -> None:
    """Terminal attempts reject every later lifecycle method deterministically."""
    attempt = _attempt()
    first: Callable[[], None] = getattr(attempt, first_method)
    later: Callable[[], None] = getattr(attempt, later_method)
    first()

    with pytest.raises(ValueError, match=r"Attempt is already terminal\."):
        later()


@pytest.mark.parametrize(
    ("state", "completed_at"),
    [
        (AttemptState.RUNNING, None),
        (AttemptState.SUCCEEDED, _timestamp(1)),
        (AttemptState.FAILED, _timestamp(1)),
        (AttemptState.CANCELLED, _timestamp(1)),
    ],
)
def test_attempt_reconstruction_preserves_valid_lifecycle_state(
    state: AttemptState,
    completed_at: Timestamp | None,
) -> None:
    """Direct construction preserves valid deterministic reconstruction state."""
    identifier = AttemptId.parse("10000000-0000-4000-8000-000000000001")
    session_id = SessionId.parse("20000000-0000-4000-8000-000000000001")
    message_id = MessageId.parse("30000000-0000-4000-8000-000000000001")
    source = MessageSource("codex")
    started_at = _timestamp()

    attempt = _attempt(
        id=identifier,
        session_id=session_id,
        message_id=message_id,
        agent_source=source,
        started_at=started_at,
        state=state,
        completed_at=completed_at,
    )

    assert attempt.id is identifier
    assert attempt.session_id is session_id
    assert attempt.message_id is message_id
    assert attempt.agent_source is source
    assert attempt.started_at is started_at
    assert attempt.state is state
    assert attempt.completed_at is completed_at


@pytest.mark.parametrize(
    ("state", "completed_at", "message"),
    [
        (
            AttemptState.RUNNING,
            _timestamp(1),
            "Running attempt cannot have completed_at.",
        ),
        (AttemptState.SUCCEEDED, None, "Terminal attempt requires completed_at."),
        (AttemptState.FAILED, None, "Terminal attempt requires completed_at."),
        (AttemptState.CANCELLED, None, "Terminal attempt requires completed_at."),
    ],
)
def test_attempt_rejects_invalid_reconstructed_lifecycle_state(
    state: AttemptState,
    completed_at: Timestamp | None,
    message: str,
) -> None:
    """State/completion coherence is the constructor's intrinsic invariant."""
    with pytest.raises(ValueError, match=message):
        _attempt(state=state, completed_at=completed_at)


def test_attempt_reconstruction_allows_earlier_completion_wall_clock() -> None:
    """Attempt records wall-clock observations without requiring monotonic order."""
    attempt = _attempt(
        started_at=_timestamp(1),
        state=AttemptState.SUCCEEDED,
        completed_at=_timestamp(),
    )

    assert attempt.completed_at is not None
    assert attempt.completed_at.value < attempt.started_at.value


def test_attempts_use_object_identity_equality_and_are_unhashable() -> None:
    """Mutable Attempts separate object equality from semantic AttemptId equality."""
    first = _attempt()
    second = _attempt()

    assert first is not second
    assert first != second
    assert first.id == second.id
    with pytest.raises(TypeError, match="unhashable"):
        hash(first)


def test_repeated_message_and_cross_session_attempts_are_valid() -> None:
    """Attempt attribution permits factual repeated and cross-Session processing."""
    message_id = MessageId.parse("30000000-0000-4000-8000-000000000001")
    first_session = SessionId.parse("20000000-0000-4000-8000-000000000001")
    second_session = SessionId.parse("20000000-0000-4000-8000-000000000002")
    source = MessageSource("codex")
    first = Attempt.new(
        session_id=first_session,
        message_id=message_id,
        agent_source=source,
    )
    repeated = Attempt.new(
        session_id=first_session,
        message_id=message_id,
        agent_source=source,
    )
    cross_session = Attempt.new(
        session_id=second_session,
        message_id=message_id,
        agent_source=source,
    )

    assert first.id != repeated.id
    assert first.message_id is repeated.message_id is cross_session.message_id
    assert first.session_id is repeated.session_id
    assert cross_session.session_id is second_session
    assert first.agent_source is repeated.agent_source is cross_session.agent_source
