# Copyright (c) 2026
"""Application-level processing attempt lifecycle values."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.identity import Identity
from devtools.time import Timestamp

if TYPE_CHECKING:
    from devtools.context.message import MessageId, MessageSource
    from devtools.context.session import SessionId


@dataclass(frozen=True, slots=True)
class AttemptId:
    """Represent an immutable semantic identity for one processing attempt.

    :ivar value: Generic identity backing this attempt-specific identity.
    """

    value: Identity

    @classmethod
    def new(cls) -> AttemptId:
        """Generate a new attempt identity.

        :returns: Newly generated attempt identity.
        """
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> AttemptId:
        """Parse an attempt identity from UUID text.

        :param value: UUID string representation.
        :returns: Parsed attempt identity.
        :raises ValueError: If the supplied value is not a valid UUID.
        """
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return the canonical attempt identity representation.

        :returns: Canonical UUID string.
        """
        return str(self.value)


class AttemptState(StrEnum):
    """Identify the lifecycle state of one application processing attempt."""

    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Attempt:
    """Represent one mutable application-level processing attempt."""

    __slots__ = (
        "_completed_at",
        "_id",
        "_interaction_source",
        "_message_id",
        "_session_id",
        "_started_at",
        "_state",
    )

    __hash__ = None  # type: ignore[assignment]

    def __init__(  # noqa: PLR0913
        self,
        *,
        id: AttemptId,  # noqa: A002
        session_id: SessionId,
        message_id: MessageId,
        interaction_source: MessageSource,
        started_at: Timestamp,
        state: AttemptState,
        completed_at: Timestamp | None,
    ) -> None:
        """Create or reconstruct one processing attempt lifecycle.

        :param id: Stable application-owned attempt identity.
        :param session_id: Session owning the attempted input processing.
        :param message_id: Input Message selected for processing.
        :param interaction_source: Source attribution for the selected Interaction.
        :param started_at: Observed wall-clock start time.
        :param state: Current or final lifecycle state.
        :param completed_at: Observed terminal time, if the attempt is terminal.
        :raises ValueError: If state and completion time are inconsistent.
        """
        if state is AttemptState.RUNNING:
            if completed_at is not None:
                msg = "Running attempt cannot have completed_at."
                raise ValueError(msg)
        elif completed_at is None:
            msg = "Terminal attempt requires completed_at."
            raise ValueError(msg)

        self._id = id
        self._session_id = session_id
        self._message_id = message_id
        self._interaction_source = interaction_source
        self._started_at = started_at
        self._state = state
        self._completed_at = completed_at

    @classmethod
    def new(
        cls,
        *,
        session_id: SessionId,
        message_id: MessageId,
        interaction_source: MessageSource,
    ) -> Attempt:
        """Create a newly running processing attempt.

        :param session_id: Session owning the attempted input processing.
        :param message_id: Input Message selected for processing.
        :param interaction_source: Source attribution for the selected Interaction.
        :returns: Newly running Attempt with fresh identity and start time.
        """
        return cls(
            id=AttemptId.new(),
            session_id=session_id,
            message_id=message_id,
            interaction_source=interaction_source,
            started_at=Timestamp.now(),
            state=AttemptState.RUNNING,
            completed_at=None,
        )

    @property
    def id(self) -> AttemptId:
        """Return this attempt's stable application-owned identity."""
        return self._id

    @property
    def session_id(self) -> SessionId:
        """Return the Session semantic identity attributed to this attempt."""
        return self._session_id

    @property
    def message_id(self) -> MessageId:
        """Return the input Message semantic identity attributed to this attempt."""
        return self._message_id

    @property
    def interaction_source(self) -> MessageSource:
        """Return the selected Interaction source attribution for this attempt."""
        return self._interaction_source

    @property
    def started_at(self) -> Timestamp:
        """Return the observed wall-clock start time."""
        return self._started_at

    @property
    def state(self) -> AttemptState:
        """Return the current lifecycle state."""
        return self._state

    @property
    def completed_at(self) -> Timestamp | None:
        """Return the observed terminal time, when the attempt is terminal."""
        return self._completed_at

    def succeed(self) -> None:
        """Mark this running attempt as successfully completed."""
        self._complete(AttemptState.SUCCEEDED)

    def fail(self) -> None:
        """Mark this running attempt as failed."""
        self._complete(AttemptState.FAILED)

    def cancel(self) -> None:
        """Mark this running attempt as cancelled."""
        self._complete(AttemptState.CANCELLED)

    def _complete(self, state: AttemptState) -> None:
        """Apply one terminal lifecycle transition."""
        if self._state is not AttemptState.RUNNING:
            msg = "Attempt is already terminal."
            raise ValueError(msg)

        completed_at = Timestamp.now()

        self._state = state
        self._completed_at = completed_at

    def __eq__(self, other: object) -> bool:
        """Compare mutable attempt entities by Python object identity."""
        return self is other
