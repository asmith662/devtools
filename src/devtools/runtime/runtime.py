# Copyright (c) 2026
"""Stateless coordination of an Agent interaction with a Session."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from devtools.evidence import Attempt, AttemptObserver

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.agents import Agent, AgentTurn
    from devtools.context.message import Message
    from devtools.context.session import Session


class Runtime:
    """Coordinate one caller-selected agent interaction with one session."""

    __slots__ = ("_observer",)

    def __init__(self, *, observer: AttemptObserver | None = None) -> None:
        """Create a stateless Runtime with optional Attempt observation.

        :param observer: Fixed synchronous observer for created Attempts.
        """
        self._observer = observer

    @property
    def observer(self) -> AttemptObserver | None:
        """Return this Runtime's fixed optional Attempt observer."""
        return self._observer

    async def send(
        self,
        *,
        session: Session,
        agent: Agent,
        message: Message,
    ) -> AgentTurn:
        """Apply one agent interaction to a session.

        :param session: Retained interaction lifecycle to update.
        :param agent: Explicitly selected responder.
        :param message: Input message to retain and submit.
        :returns: The agent's unchanged turn result.
        :raises ValueError: If the returned message has a different source than
            the selected agent.
        """
        observer = self._observer

        async with session.turn():
            session.add(message)
            attempt = self._start_attempt(observer, session, agent, message)

            try:
                turn = await self._process_turn(session, agent, message)
            except asyncio.CancelledError:
                if observer is not None and attempt is not None:
                    self._observe_terminal_attempt(
                        observer,
                        attempt,
                        attempt.cancel,
                    )
                raise
            except Exception:
                if observer is not None and attempt is not None:
                    self._observe_terminal_attempt(
                        observer,
                        attempt,
                        attempt.fail,
                    )
                raise

            if observer is not None and attempt is not None:
                self._observe_terminal_attempt(observer, attempt, attempt.succeed)

            return turn

    @staticmethod
    def _start_attempt(
        observer: AttemptObserver | None,
        session: Session,
        agent: Agent,
        message: Message,
    ) -> Attempt | None:
        """Create and admit one observed Attempt when configured."""
        if observer is None:
            return None

        attempt = Attempt.new(
            session_id=session.id,
            message_id=message.id,
            agent_source=agent.source,
        )
        try:
            observer.attempt_started(attempt)
        except asyncio.CancelledError:
            Runtime._observe_terminal_attempt(observer, attempt, attempt.cancel)
            raise
        except Exception:
            Runtime._observe_terminal_attempt(observer, attempt, attempt.fail)
            raise

        return attempt

    @staticmethod
    async def _process_turn(
        session: Session,
        agent: Agent,
        message: Message,
    ) -> AgentTurn:
        """Perform Runtime's one canonical Agent processing sequence."""
        conversation = session.conversation_for(agent.source)
        turn = await agent.send(message, conversation=conversation)
        Runtime._validate_turn_source(turn, agent)
        session.add(turn.message)

        if turn.conversation is not None:
            session.set_conversation(turn.conversation)

        return turn

    @staticmethod
    def _validate_turn_source(turn: AgentTurn, agent: Agent) -> None:
        """Validate that the selected Agent produced the returned Message."""
        if turn.message.source != agent.source:
            msg = "Agent turn message source does not match agent source."
            raise ValueError(msg)

    @staticmethod
    def _observe_terminal_attempt(
        observer: AttemptObserver,
        attempt: Attempt,
        terminalize: Callable[[], None],
    ) -> None:
        """Best-effort terminal observation without replacing primary outcomes."""
        try:
            terminalize()
        except asyncio.CancelledError:
            return
        except Exception:  # noqa: BLE001
            return

        try:
            observer.attempt_finished(attempt)
        except asyncio.CancelledError:
            return
        except Exception:  # noqa: BLE001
            return
