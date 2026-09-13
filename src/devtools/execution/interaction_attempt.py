# Copyright (c) 2026
"""Lifecycle facts for one Runtime-managed model interaction attempt."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.core.identity import Identity
from devtools.core.time import Timestamp

if TYPE_CHECKING:
    from devtools.agents.conversation import ConversationId, MessageId
    from devtools.models.interaction import InteractionSource


@dataclass(frozen=True, slots=True)
class InteractionAttemptId:
    """Identify one Runtime-managed model interaction attempt."""

    value: Identity

    @classmethod
    def new(cls) -> InteractionAttemptId:
        """Generate a new interaction-attempt identity."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> InteractionAttemptId:
        """Parse UUID text as an interaction-attempt identity."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return canonical UUID text."""
        return str(self.value)


class InteractionAttemptState(StrEnum):
    """Identify current interaction-attempt lifecycle state."""

    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InteractionAttemptStage(StrEnum):
    """Identify the Runtime boundary where processing reached or stopped."""

    ADMISSION = "admission"
    CONTINUATION_LOOKUP = "continuation_lookup"
    INTERACTION_INVOCATION = "interaction_invocation"
    RESULT_VALIDATION = "result_validation"
    OUTPUT_RETENTION = "output_retention"
    CONTINUATION_REPLACEMENT = "continuation_replacement"


@dataclass(frozen=True, slots=True)
class InteractionAttemptSucceeded:
    """Represent a successful interaction-attempt outcome."""


@dataclass(frozen=True, slots=True)
class InteractionAttemptFailed:
    """Represent a failed interaction attempt at one Runtime boundary."""

    stage: InteractionAttemptStage


@dataclass(frozen=True, slots=True)
class InteractionAttemptCancelled:
    """Represent a cancelled interaction attempt at one Runtime boundary."""

    stage: InteractionAttemptStage


type InteractionAttemptOutcome = (
    InteractionAttemptSucceeded | InteractionAttemptFailed | InteractionAttemptCancelled
)


class InteractionAttempt:
    """Represent one mutable Runtime-managed model-interaction attempt."""

    __slots__ = (
        "_completed_at",
        "_conversation_id",
        "_id",
        "_interaction_source",
        "_message_id",
        "_started_at",
        "_state",
    )

    __hash__ = None  # type: ignore[assignment]

    def __init__(  # noqa: PLR0913
        self,
        *,
        id: InteractionAttemptId,  # noqa: A002
        conversation_id: ConversationId,
        message_id: MessageId,
        interaction_source: InteractionSource,
        started_at: Timestamp,
        state: InteractionAttemptState,
        completed_at: Timestamp | None,
    ) -> None:
        """Create or reconstruct one interaction-attempt lifecycle."""
        if state is InteractionAttemptState.RUNNING and completed_at is not None:
            msg = "Running attempt cannot have completed_at."
            raise ValueError(msg)
        if state is not InteractionAttemptState.RUNNING and completed_at is None:
            msg = "Terminal attempt requires completed_at."
            raise ValueError(msg)
        self._id = id
        self._conversation_id = conversation_id
        self._message_id = message_id
        self._interaction_source = interaction_source
        self._started_at = started_at
        self._state = state
        self._completed_at = completed_at

    @classmethod
    def new(
        cls,
        *,
        conversation_id: ConversationId,
        message_id: MessageId,
        interaction_source: InteractionSource,
    ) -> InteractionAttempt:
        """Create a newly running interaction attempt."""
        return cls(
            id=InteractionAttemptId.new(),
            conversation_id=conversation_id,
            message_id=message_id,
            interaction_source=interaction_source,
            started_at=Timestamp.now(),
            state=InteractionAttemptState.RUNNING,
            completed_at=None,
        )

    @property
    def id(self) -> InteractionAttemptId:
        """Return the stable attempt identity."""
        return self._id

    @property
    def conversation_id(self) -> ConversationId:
        """Return the owning conversation identity."""
        return self._conversation_id

    @property
    def message_id(self) -> MessageId:
        """Return the submitted conversation-message identity."""
        return self._message_id

    @property
    def interaction_source(self) -> InteractionSource:
        """Return the selected model-interaction source."""
        return self._interaction_source

    @property
    def started_at(self) -> Timestamp:
        """Return observed start time."""
        return self._started_at

    @property
    def state(self) -> InteractionAttemptState:
        """Return current lifecycle state."""
        return self._state

    @property
    def completed_at(self) -> Timestamp | None:
        """Return terminal time when known."""
        return self._completed_at

    def succeed(self) -> None:
        """Mark this attempt successful."""
        self._complete(InteractionAttemptState.SUCCEEDED)

    def fail(self) -> None:
        """Mark this attempt failed."""
        self._complete(InteractionAttemptState.FAILED)

    def cancel(self) -> None:
        """Mark this attempt cancelled."""
        self._complete(InteractionAttemptState.CANCELLED)

    def _complete(self, state: InteractionAttemptState) -> None:
        if self._state is not InteractionAttemptState.RUNNING:
            msg = "InteractionAttempt is already terminal."
            raise ValueError(msg)
        completed_at = Timestamp.now()
        self._state = state
        self._completed_at = completed_at

    def __eq__(self, other: object) -> bool:
        """Compare mutable lifecycle entities by object identity."""
        return self is other
