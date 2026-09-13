# Copyright (c) 2026
# ruff: noqa: E501
"""Tests for application-level processing attempts."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from devtools import execution
from devtools.agents.conversation import ConversationId, InteractionSource, MessageId
from devtools.core.identity import Identity
from devtools.core.time import Timestamp
from devtools.execution import (
    InteractionAttempt,
    InteractionAttemptId,
    InteractionAttemptObserver,
    InteractionAttemptState,
)
from devtools.execution.interaction_attempt import (
    InteractionAttempt as AttemptFromSubmodule,
)
from devtools.execution.interaction_attempt import (
    InteractionAttemptId as AttemptIdFromSubmodule,
)
from devtools.execution.interaction_attempt import (
    InteractionAttemptState as AttemptStateFromSubmodule,
)

if TYPE_CHECKING:
    from collections.abc import Callable


def _timestamp(offset: int = 0) -> Timestamp:
    """Return one deterministic UTC timestamp."""
    value = datetime(2026, 8, 16, 12, 0, tzinfo=UTC)
    return Timestamp(value + timedelta(seconds=offset))


def _attempt(  # noqa: PLR0913
    *,
    id: InteractionAttemptId | None = None,  # noqa: A002
    conversation_id: ConversationId | None = None,
    message_id: MessageId | None = None,
    interaction_source: InteractionSource | None = None,
    started_at: Timestamp | None = None,
    state: InteractionAttemptState = InteractionAttemptState.RUNNING,
    completed_at: Timestamp | None = None,
) -> InteractionAttempt:
    """Build one deterministic InteractionAttempt with configurable reconstruction state."""
    return InteractionAttempt(
        id=(id or InteractionAttemptId.parse("10000000-0000-4000-8000-000000000001")),
        conversation_id=(
            conversation_id
            or ConversationId.parse("20000000-0000-4000-8000-000000000001")
        ),
        message_id=(
            message_id or MessageId.parse("30000000-0000-4000-8000-000000000001")
        ),
        interaction_source=interaction_source or InteractionSource("codex"),
        started_at=started_at or _timestamp(),
        state=state,
        completed_at=completed_at,
    )


def test_root_and_submodule_expose_the_same_attempt_types() -> None:
    """Evidence public imports are canonical type identities."""
    assert InteractionAttempt is AttemptFromSubmodule
    assert InteractionAttemptId is AttemptIdFromSubmodule
    assert InteractionAttemptState is AttemptStateFromSubmodule
    assert InteractionAttemptObserver.__module__ == "devtools.execution.protocols"
    assert execution.__all__ == [
        "InteractionAttempt",
        "InteractionAttemptCancelled",
        "InteractionAttemptFailed",
        "InteractionAttemptId",
        "InteractionAttemptObserver",
        "InteractionAttemptOutcome",
        "InteractionAttemptStage",
        "InteractionAttemptState",
        "InteractionAttemptSucceeded",
        "Runtime",
    ]


def test_attempt_id_is_an_immutable_semantic_identity() -> None:
    """InteractionAttemptId follows the existing semantic Identity-wrapper contract."""
    parsed = InteractionAttemptId.parse("12345678-1234-5678-1234-567812345678")
    equivalent = InteractionAttemptId(Identity.parse(str(parsed)))
    generated = InteractionAttemptId.new()
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert generated.value.value.version == expected_uuid_version
    assert str(parsed) == "12345678-1234-5678-1234-567812345678"
    assert parsed == equivalent
    assert hash(parsed) == hash(equivalent)

    with pytest.raises(ValueError, match="badly formed"):
        InteractionAttemptId.parse("not-a-uuid")
    with pytest.raises(FrozenInstanceError):
        parsed.value = Identity.new()  # type: ignore[misc]


def test_attempt_id_accepts_non_v4_identity_text() -> None:
    """InteractionAttemptId preserves generic Identity UUID-version parsing behavior."""
    non_v4 = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

    parsed = InteractionAttemptId.parse(non_v4)

    assert parsed.value.value.version == 1
    assert str(parsed) == non_v4


def test_attempt_state_has_exact_stable_members() -> None:
    """InteractionAttempt lifecycle states are intentionally small and string-valued."""
    assert tuple(InteractionAttemptState) == (
        InteractionAttemptState.RUNNING,
        InteractionAttemptState.SUCCEEDED,
        InteractionAttemptState.FAILED,
        InteractionAttemptState.CANCELLED,
    )
    assert [state.value for state in InteractionAttemptState] == [
        "running",
        "succeeded",
        "failed",
        "cancelled",
    ]


def test_attempt_new_creates_running_lifecycle_with_exact_attribution() -> None:
    """InteractionAttempt.new creates fresh lifecycle state without embedding domain objects."""
    conversation_id = ConversationId.parse("20000000-0000-4000-8000-000000000001")
    message_id = MessageId.parse("30000000-0000-4000-8000-000000000001")
    source = InteractionSource("codex")

    attempt = InteractionAttempt.new(
        conversation_id=conversation_id,
        message_id=message_id,
        interaction_source=source,
    )

    assert isinstance(attempt.id, InteractionAttemptId)
    assert attempt.conversation_id is conversation_id
    assert attempt.message_id is message_id
    assert attempt.interaction_source is source
    assert isinstance(attempt.started_at, Timestamp)
    assert attempt.state is InteractionAttemptState.RUNNING
    assert attempt.completed_at is None


def test_attempt_properties_are_read_only() -> None:
    """Attribution and lifecycle state mutate only through lifecycle methods."""
    attempt = _attempt()

    with pytest.raises(AttributeError):
        attempt.id = InteractionAttemptId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.conversation_id = ConversationId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.message_id = MessageId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.interaction_source = InteractionSource("qwen")  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.started_at = Timestamp.now()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.state = InteractionAttemptState.FAILED  # type: ignore[misc]
    with pytest.raises(AttributeError):
        attempt.completed_at = Timestamp.now()  # type: ignore[misc]


@pytest.mark.parametrize(
    ("method_name", "expected_state"),
    [
        ("succeed", InteractionAttemptState.SUCCEEDED),
        ("fail", InteractionAttemptState.FAILED),
        ("cancel", InteractionAttemptState.CANCELLED),
    ],
)
def test_attempt_terminal_methods_complete_running_lifecycle(
    method_name: str,
    expected_state: InteractionAttemptState,
) -> None:
    """Each semantic terminal method captures completion and preserves attribution."""
    attempt = _attempt()
    attribution = (
        attempt.id,
        attempt.conversation_id,
        attempt.message_id,
        attempt.interaction_source,
        attempt.started_at,
    )
    method: Callable[[], None] = getattr(attempt, method_name)

    assert method() is None  # type: ignore[func-returns-value]
    assert attempt.state is expected_state
    assert isinstance(attempt.completed_at, Timestamp)
    assert (
        attempt.id,
        attempt.conversation_id,
        attempt.message_id,
        attempt.interaction_source,
        attempt.started_at,
    ) == attribution


def test_attempt_completion_timestamp_failure_preserves_running_lifecycle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Timestamp failure does not partially terminalize the shared lifecycle path."""
    attempt = _attempt()
    attribution = (
        attempt.id,
        attempt.conversation_id,
        attempt.message_id,
        attempt.interaction_source,
        attempt.started_at,
    )
    error = RuntimeError("timestamp unavailable")

    def raise_timestamp_error() -> Timestamp:
        raise error

    monkeypatch.setattr(
        "devtools.execution.interaction_attempt.Timestamp.now",
        raise_timestamp_error,
    )

    with pytest.raises(RuntimeError) as raised:
        attempt.succeed()

    assert raised.value is error
    assert attempt.state is InteractionAttemptState.RUNNING
    assert attempt.completed_at is None
    assert (
        attempt.id,
        attempt.conversation_id,
        attempt.message_id,
        attempt.interaction_source,
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

    with pytest.raises(ValueError, match=r"InteractionAttempt is already terminal\."):
        later()


@pytest.mark.parametrize(
    ("state", "completed_at"),
    [
        (InteractionAttemptState.RUNNING, None),
        (InteractionAttemptState.SUCCEEDED, _timestamp(1)),
        (InteractionAttemptState.FAILED, _timestamp(1)),
        (InteractionAttemptState.CANCELLED, _timestamp(1)),
    ],
)
def test_attempt_reconstruction_preserves_valid_lifecycle_state(
    state: InteractionAttemptState,
    completed_at: Timestamp | None,
) -> None:
    """Direct construction preserves valid deterministic reconstruction state."""
    identifier = InteractionAttemptId.parse("10000000-0000-4000-8000-000000000001")
    conversation_id = ConversationId.parse("20000000-0000-4000-8000-000000000001")
    message_id = MessageId.parse("30000000-0000-4000-8000-000000000001")
    source = InteractionSource("codex")
    started_at = _timestamp()

    attempt = _attempt(
        id=identifier,
        conversation_id=conversation_id,
        message_id=message_id,
        interaction_source=source,
        started_at=started_at,
        state=state,
        completed_at=completed_at,
    )

    assert attempt.id is identifier
    assert attempt.conversation_id is conversation_id
    assert attempt.message_id is message_id
    assert attempt.interaction_source is source
    assert attempt.started_at is started_at
    assert attempt.state is state
    assert attempt.completed_at is completed_at


@pytest.mark.parametrize(
    ("state", "completed_at", "message"),
    [
        (
            InteractionAttemptState.RUNNING,
            _timestamp(1),
            "Running attempt cannot have completed_at.",
        ),
        (
            InteractionAttemptState.SUCCEEDED,
            None,
            "Terminal attempt requires completed_at.",
        ),
        (
            InteractionAttemptState.FAILED,
            None,
            "Terminal attempt requires completed_at.",
        ),
        (
            InteractionAttemptState.CANCELLED,
            None,
            "Terminal attempt requires completed_at.",
        ),
    ],
)
def test_attempt_rejects_invalid_reconstructed_lifecycle_state(
    state: InteractionAttemptState,
    completed_at: Timestamp | None,
    message: str,
) -> None:
    """State/completion coherence is the constructor's intrinsic invariant."""
    with pytest.raises(ValueError, match=message):
        _attempt(state=state, completed_at=completed_at)


def test_attempt_reconstruction_allows_earlier_completion_wall_clock() -> None:
    """InteractionAttempt records wall-clock observations without requiring monotonic order."""
    attempt = _attempt(
        started_at=_timestamp(1),
        state=InteractionAttemptState.SUCCEEDED,
        completed_at=_timestamp(),
    )

    assert attempt.completed_at is not None
    assert attempt.completed_at.value < attempt.started_at.value


def test_attempts_use_object_identity_equality_and_are_unhashable() -> None:
    """Mutable Attempts separate object equality from semantic InteractionAttemptId equality."""
    first = _attempt()
    second = _attempt()

    assert first is not second
    assert first != second
    assert first.id == second.id
    with pytest.raises(TypeError, match="unhashable"):
        hash(first)


def test_repeated_message_and_cross_session_attempts_are_valid() -> None:
    """InteractionAttempt attribution permits factual repeated and cross-Conversation processing."""
    message_id = MessageId.parse("30000000-0000-4000-8000-000000000001")
    first_session = ConversationId.parse("20000000-0000-4000-8000-000000000001")
    second_session = ConversationId.parse("20000000-0000-4000-8000-000000000002")
    source = InteractionSource("codex")
    first = InteractionAttempt.new(
        conversation_id=first_session,
        message_id=message_id,
        interaction_source=source,
    )
    repeated = InteractionAttempt.new(
        conversation_id=first_session,
        message_id=message_id,
        interaction_source=source,
    )
    cross_session = InteractionAttempt.new(
        conversation_id=second_session,
        message_id=message_id,
        interaction_source=source,
    )

    assert first.id != repeated.id
    assert first.message_id is repeated.message_id is cross_session.message_id
    assert first.conversation_id is repeated.conversation_id
    assert cross_session.conversation_id is second_session
    assert (
        first.interaction_source
        is repeated.interaction_source
        is cross_session.interaction_source
    )
