# Copyright (c) 2026
"""Narrow coordination of one ModelInteraction with one Conversation."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    ConversationMessageRole,
)
from devtools.execution.interaction_attempt import (
    InteractionAttempt,
    InteractionAttemptCancelled,
    InteractionAttemptFailed,
    InteractionAttemptOutcome,
    InteractionAttemptStage,
    InteractionAttemptSucceeded,
)
from devtools.models.interaction import (
    ModelInteraction,
    ModelResponse,
    Prompt,
    validate_maximum_output_tokens,
    validate_thinking_enabled,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.execution.protocols import InteractionAttemptObserver


class Runtime:
    """Coordinate one caller-selected model interaction with a Conversation."""

    __slots__ = ("_observer",)

    def __init__(self, *, observer: InteractionAttemptObserver | None = None) -> None:
        """Create a stateless Runtime with optional lifecycle observation."""
        self._observer = observer

    @property
    def observer(self) -> InteractionAttemptObserver | None:
        """Return the fixed optional interaction-attempt observer."""
        return self._observer

    async def send(
        self,
        *,
        conversation: Conversation,
        interaction: ModelInteraction,
        message: ConversationMessage,
        maximum_output_tokens: int | None = None,
        thinking_enabled: bool | None = None,
    ) -> ModelResponse:
        """Retain one message, invoke a model, and retain its response."""
        observer = self._observer
        async with conversation.turn():
            conversation.add(message)
            attempt = self._start_attempt(observer, conversation, interaction, message)
            stage = InteractionAttemptStage.CONTINUATION_LOOKUP
            try:
                continuation = conversation.conversation_for(interaction.source)
                stage = InteractionAttemptStage.INTERACTION_INVOCATION
                prompt = Prompt(content=message.content, role=message.role.value)
                validate_thinking_enabled(thinking_enabled)
                if maximum_output_tokens is None and thinking_enabled is None:
                    response = await interaction.send(prompt, conversation=continuation)
                elif maximum_output_tokens is None:
                    response = await interaction.send(
                        prompt,
                        conversation=continuation,
                        thinking_enabled=thinking_enabled,
                    )
                elif thinking_enabled is None:
                    validate_maximum_output_tokens(maximum_output_tokens)
                    response = await interaction.send(
                        prompt,
                        conversation=continuation,
                        maximum_output_tokens=maximum_output_tokens,
                    )
                else:
                    validate_maximum_output_tokens(maximum_output_tokens)
                    response = await interaction.send(
                        prompt,
                        conversation=continuation,
                        maximum_output_tokens=maximum_output_tokens,
                        thinking_enabled=thinking_enabled,
                    )
                stage = InteractionAttemptStage.RESULT_VALIDATION
                self._validate_response_source(response, interaction)
                stage = InteractionAttemptStage.OUTPUT_RETENTION
                conversation.add(
                    ConversationMessage.new(
                        response.content,
                        role=ConversationMessageRole.ASSISTANT,
                        source=response.source,
                    ),
                )
                if response.conversation is not None:
                    stage = InteractionAttemptStage.CONTINUATION_REPLACEMENT
                    conversation.set_conversation(response.conversation)
            except asyncio.CancelledError:
                self._finish_attempt(
                    observer,
                    attempt,
                    attempt.cancel if attempt is not None else None,
                    InteractionAttemptCancelled(stage),
                )
                raise
            except Exception:
                self._finish_attempt(
                    observer,
                    attempt,
                    attempt.fail if attempt is not None else None,
                    InteractionAttemptFailed(stage),
                )
                raise
            self._finish_attempt(
                observer,
                attempt,
                attempt.succeed if attempt is not None else None,
                InteractionAttemptSucceeded(),
            )
            return response

    @staticmethod
    def _start_attempt(
        observer: InteractionAttemptObserver | None,
        conversation: Conversation,
        interaction: ModelInteraction,
        message: ConversationMessage,
    ) -> InteractionAttempt | None:
        if observer is None:
            return None
        attempt = InteractionAttempt.new(
            conversation_id=conversation.id,
            message_id=message.id,
            interaction_source=interaction.source,
        )
        try:
            observer.attempt_started(attempt)
        except asyncio.CancelledError:
            Runtime._finish_attempt(
                observer,
                attempt,
                attempt.cancel,
                InteractionAttemptCancelled(InteractionAttemptStage.ADMISSION),
            )
            raise
        except Exception:
            Runtime._finish_attempt(
                observer,
                attempt,
                attempt.fail,
                InteractionAttemptFailed(InteractionAttemptStage.ADMISSION),
            )
            raise
        return attempt

    @staticmethod
    def _validate_response_source(
        response: ModelResponse,
        interaction: ModelInteraction,
    ) -> None:
        if response.source != interaction.source:
            msg = "Model response source does not match model interaction source."
            raise ValueError(msg)

    @staticmethod
    def _finish_attempt(
        observer: InteractionAttemptObserver | None,
        attempt: InteractionAttempt | None,
        terminalize: Callable[[], None] | None,
        outcome: InteractionAttemptOutcome,
    ) -> None:
        if observer is None or attempt is None or terminalize is None:
            return
        try:
            terminalize()
        except asyncio.CancelledError:
            return
        except Exception:  # noqa: BLE001
            return
        try:
            observer.attempt_finished(attempt, outcome)
        except asyncio.CancelledError:
            return
        except Exception:  # noqa: BLE001
            return
