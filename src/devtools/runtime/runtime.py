# Copyright (c) 2026
"""Stateless coordination of an Agent interaction with a Session."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.agents import Agent, AgentTurn
    from devtools.context.message import Message
    from devtools.context.session import Session


class Runtime:
    """Coordinate one caller-selected agent interaction with one session."""

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
        async with session.turn():
            session.add(message)
            conversation = session.conversation_for(agent.source)
            turn = await agent.send(message, conversation=conversation)

            if turn.message.source != agent.source:
                msg = "Agent turn message source does not match agent source."
                raise ValueError(msg)

            session.add(turn.message)

            if turn.conversation is not None:
                session.set_conversation(turn.conversation)

            return turn
