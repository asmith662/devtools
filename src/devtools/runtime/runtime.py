# Copyright (c) 2026
"""Stateless coordination of one Interaction with a Session."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from devtools.evidence import (
    Attempt,
    AttemptCancelled,
    AttemptFailed,
    AttemptObserver,
    AttemptStage,
    AttemptSucceeded,
    AttemptTerminalEvidence,
    EvidenceSink,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.context.message import Message
    from devtools.context.session import Session
    from devtools.interactions import Interaction, InteractionTurn


class Runtime:
    """Coordinate one caller-selected interaction with one session."""

    __slots__ = ("_evidence_sink", "_observer")

    def __init__(
        self,
        *,
        observer: AttemptObserver | None = None,
        evidence_sink: EvidenceSink | None = None,
    ) -> None:
        """Create a stateless Runtime with optional Evidence configuration.

        :param observer: Fixed synchronous observer for created Attempts.
        :param evidence_sink: Fixed synchronous terminal Evidence sink.
        """
        self._observer = observer
        self._evidence_sink = evidence_sink

    @property
    def observer(self) -> AttemptObserver | None:
        """Return this Runtime's fixed optional Attempt observer."""
        return self._observer

    @property
    def evidence_sink(self) -> EvidenceSink | None:
        """Return this Runtime's fixed optional terminal Evidence sink."""
        return self._evidence_sink

    async def send(
        self,
        *,
        session: Session,
        interaction: Interaction,
        message: Message,
    ) -> InteractionTurn:
        """Apply one interaction to a session.

        :param session: Retained interaction lifecycle to update.
        :param interaction: Explicitly selected interaction.
        :param message: Input message to retain and submit.
        :returns: The interaction's unchanged turn result.
        :raises ValueError: If the returned message has a different source than
            the selected interaction.
        """
        observer = self._observer
        evidence_sink = self._evidence_sink

        async with session.turn():
            session.add(message)
            attempt = self._start_attempt(
                observer,
                evidence_sink,
                session,
                interaction,
                message,
            )
            stage = AttemptStage.CONTINUATION_LOOKUP

            try:
                conversation = session.conversation_for(interaction.source)
                stage = AttemptStage.INTERACTION_INVOCATION
                turn = await interaction.send(message, conversation=conversation)
                stage = AttemptStage.RESULT_VALIDATION
                self._validate_turn_source(turn, interaction)
                stage = AttemptStage.OUTPUT_RETENTION
                session.add(turn.message)

                if turn.conversation is not None:
                    stage = AttemptStage.CONTINUATION_REPLACEMENT
                    session.set_conversation(turn.conversation)
            except asyncio.CancelledError:
                if attempt is not None:
                    self._finish_attempt(
                        observer,
                        evidence_sink,
                        attempt,
                        attempt.cancel,
                        AttemptCancelled(stage),
                    )
                raise
            except Exception:
                if attempt is not None:
                    self._finish_attempt(
                        observer,
                        evidence_sink,
                        attempt,
                        attempt.fail,
                        AttemptFailed(stage),
                    )
                raise

            if attempt is not None:
                self._finish_attempt(
                    observer,
                    evidence_sink,
                    attempt,
                    attempt.succeed,
                    AttemptSucceeded(),
                )

            return turn

    @staticmethod
    def _start_attempt(
        observer: AttemptObserver | None,
        evidence_sink: EvidenceSink | None,
        session: Session,
        interaction: Interaction,
        message: Message,
    ) -> Attempt | None:
        """Create and admit one Attempt when Evidence configuration needs it."""
        if observer is None and evidence_sink is None:
            return None

        attempt = Attempt.new(
            session_id=session.id,
            message_id=message.id,
            interaction_source=interaction.source,
        )
        if observer is None:
            return attempt

        try:
            observer.attempt_started(attempt)
        except asyncio.CancelledError:
            Runtime._finish_attempt(
                observer,
                evidence_sink,
                attempt,
                attempt.cancel,
                AttemptCancelled(AttemptStage.ADMISSION),
            )
            raise
        except Exception:
            Runtime._finish_attempt(
                observer,
                evidence_sink,
                attempt,
                attempt.fail,
                AttemptFailed(AttemptStage.ADMISSION),
            )
            raise

        return attempt

    @staticmethod
    def _validate_turn_source(
        turn: InteractionTurn,
        interaction: Interaction,
    ) -> None:
        """Validate that the selected Interaction produced the returned Message."""
        if turn.message.source != interaction.source:
            msg = "Interaction turn message source does not match interaction source."
            raise ValueError(msg)

    @staticmethod
    def _finish_attempt(
        observer: AttemptObserver | None,
        evidence_sink: EvidenceSink | None,
        attempt: Attempt,
        terminalize: Callable[[], None],
        outcome: AttemptSucceeded | AttemptFailed | AttemptCancelled,
    ) -> None:
        """Apply terminal accounting and independent secondary delivery."""
        if not Runtime._terminalize_attempt(terminalize):
            return

        evidence = Runtime._construct_terminal_evidence(
            evidence_sink,
            attempt,
            outcome,
        )
        Runtime._notify_finished(observer, attempt)
        Runtime._accept_evidence(evidence_sink, evidence)

    @staticmethod
    def _terminalize_attempt(terminalize: Callable[[], None]) -> bool:
        """Apply terminal accounting without replacing a primary outcome."""
        try:
            terminalize()
        except asyncio.CancelledError:
            return False
        except Exception:  # noqa: BLE001
            return False
        return True

    @staticmethod
    def _construct_terminal_evidence(
        evidence_sink: EvidenceSink | None,
        attempt: Attempt,
        outcome: AttemptSucceeded | AttemptFailed | AttemptCancelled,
    ) -> AttemptTerminalEvidence | None:
        """Construct terminal Evidence once when a configured sink needs it."""
        occurred_at = attempt.completed_at
        if evidence_sink is None or occurred_at is None:
            return None

        try:
            return AttemptTerminalEvidence.new(
                attempt_id=attempt.id,
                occurred_at=occurred_at,
                outcome=outcome,
            )
        except asyncio.CancelledError:
            return None
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _notify_finished(
        observer: AttemptObserver | None,
        attempt: Attempt,
    ) -> None:
        """Attempt finished observation without replacing a primary outcome."""
        if observer is None:
            return

        try:
            observer.attempt_finished(attempt)
        except asyncio.CancelledError:
            return
        except Exception:  # noqa: BLE001
            return

    @staticmethod
    def _accept_evidence(
        evidence_sink: EvidenceSink | None,
        evidence: AttemptTerminalEvidence | None,
    ) -> None:
        """Attempt terminal Evidence acceptance once without replacing primary."""
        if evidence_sink is None or evidence is None:
            return

        try:
            evidence_sink.accept(evidence)
        except asyncio.CancelledError:
            return
        except Exception:  # noqa: BLE001
            return
