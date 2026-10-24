# Copyright (c) 2026
"""Model-facing input for one model interaction."""

from dataclasses import dataclass

from devtools.models.interaction.tools import ModelToolCall


@dataclass(frozen=True, slots=True)
class PromptMessage:
    """One invocation-input message, not a durable ConversationMessage."""

    role: str
    content: str
    tool_calls: tuple[ModelToolCall, ...] = ()
    tool_call_id: str | None = None
    reasoning_content: str | None = None

    def __post_init__(self) -> None:
        """Reject malformed roles and tool-result/call associations locally."""
        if self.reasoning_content is not None and (
            self.role != "assistant" or not isinstance(self.reasoning_content, str)
        ):
            msg = "Only assistant input may retain textual provider reasoning."
            raise ValueError(msg)
        if self.role not in {"system", "user", "assistant", "tool"} or not isinstance(
            self.content,
            str,
        ):
            msg = "Prompt message requires a supported role and textual content."
            raise ValueError(msg)
        if not isinstance(self.tool_calls, tuple) or any(
            not isinstance(call, ModelToolCall) for call in self.tool_calls
        ):
            msg = "Prompt message calls must be a tuple of ModelToolCall values."
            raise TypeError(msg)
        if self.tool_calls and self.role != "assistant":
            msg = "Only assistant messages may contain Tool calls."
            raise ValueError(msg)
        if (self.role == "tool") != bool(self.tool_call_id):
            msg = "Only Tool results require a nonempty Tool call ID."
            raise ValueError(msg)
        if self.tool_call_id is not None and (
            not isinstance(self.tool_call_id, str) or not self.tool_call_id.strip()
        ):
            msg = "Tool call ID must be nonblank text."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Prompt:
    """Represent single text input or explicit structured invocation messages.

    Structured input uses empty content and role ``messages``. These are selected
    invocation inputs, not a persistent Conversation or provider continuation.
    """

    content: str
    role: str
    messages: tuple[PromptMessage, ...] = ()

    def __post_init__(self) -> None:  # noqa: C901 -- strict complete exchange admission
        """Reject dual input and incomplete, duplicate or uncorrelated exchanges."""
        if not isinstance(self.messages, tuple) or any(
            not isinstance(message, PromptMessage) for message in self.messages
        ):
            msg = "Prompt messages must be a tuple of PromptMessage values."
            raise TypeError(msg)
        if not self.messages:
            if self.role == "messages":
                msg = "Structured Prompt requires messages."
                raise ValueError(msg)
            return
        if self.content or self.role != "messages":
            msg = "Structured Prompt cannot also contain single-message input."
            raise ValueError(msg)
        pending: set[str] = set()
        for message in self.messages:
            if message.role == "tool":
                if message.tool_call_id not in pending:
                    msg = "Tool result does not match a pending assistant call."
                    raise ValueError(msg)
                pending.remove(message.tool_call_id)
            else:
                if pending:
                    msg = (
                        "All assistant Tool calls require results before continuation."
                    )
                    raise ValueError(msg)
                for call in message.tool_calls:
                    if not call.provider_call_id or call.provider_call_id in pending:
                        msg = "Assistant Tool call IDs must be nonempty and unique."
                        raise ValueError(msg)
                    pending.add(call.provider_call_id)
        if pending:
            msg = "Prompt ends with unresolved Tool calls."
            raise ValueError(msg)
