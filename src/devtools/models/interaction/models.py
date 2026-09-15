# Copyright (c) 2026
"""Values exchanged at the model-invocation boundary."""

from __future__ import annotations

from dataclasses import dataclass, field

from devtools.models.interaction.prompt import Prompt
from devtools.models.interaction.tools import ModelToolDefinition


def validate_maximum_output_tokens(value: int | None) -> None:
    """Validate one optional request-side output-token constraint."""
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        msg = "Maximum output tokens must be a positive integer."
        raise ValueError(msg)


def validate_thinking_enabled(value: object) -> None:
    """Validate one optional request-side thinking-mode control."""
    if value is None:
        return
    if not isinstance(value, bool):
        msg = "Thinking enabled must be a boolean or None."
        raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class ModelSettings:
    """Represent portable, per-invocation model settings."""

    maximum_output_tokens: int | None = None
    thinking_enabled: bool | None = None

    def __post_init__(self) -> None:
        """Validate only established portable request semantics."""
        validate_maximum_output_tokens(self.maximum_output_tokens)
        validate_thinking_enabled(self.thinking_enabled)


@dataclass(frozen=True, slots=True)
class ProviderRequestSettings:
    """Identify immutable provider-owned request settings."""

    provider: str

    def __post_init__(self) -> None:
        """Validate the provider discriminator used at adapter admission."""
        if not self.provider.strip():
            msg = "Provider request settings provider cannot be blank."
            raise ValueError(msg)
        if self.provider != self.provider.strip():
            msg = (
                "Provider request settings provider cannot have surrounding whitespace."
            )
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class InteractionSource:
    """Identify the model interaction that owns provider continuation state."""

    value: str

    def __post_init__(self) -> None:
        """Validate source identifier invariants."""
        if not self.value.strip():
            msg = "ModelInteraction source cannot be blank."
            raise ValueError(msg)
        if self.value != self.value.strip():
            msg = "ModelInteraction source cannot have surrounding whitespace."
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the source identifier."""
        return self.value


@dataclass(frozen=True, slots=True)
class ConversationRef:
    """Represent opaque continuation state owned by one ModelInteraction."""

    source: InteractionSource
    value: str

    def __post_init__(self) -> None:
        """Validate continuation identifier invariants."""
        if not self.value.strip():
            msg = "Conversation reference cannot be blank."
            raise ValueError(msg)
        if self.value != self.value.strip():
            msg = "Conversation reference cannot have surrounding whitespace."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ModelRequest:
    """Represent one immutable semantic request to a model interaction."""

    prompt: Prompt
    settings: ModelSettings = field(default_factory=ModelSettings)
    conversation: ConversationRef | None = None
    provider_settings: ProviderRequestSettings | None = None
    tools: tuple[ModelToolDefinition, ...] = ()

    def __post_init__(self) -> None:
        """Reject values outside the narrow portable request contract."""
        if not isinstance(self.prompt, Prompt):
            msg = "Model request prompt must be a Prompt."
            raise TypeError(msg)
        if not isinstance(self.settings, ModelSettings):
            msg = "Model request settings must be ModelSettings."
            raise TypeError(msg)
        if self.conversation is not None and not isinstance(
            self.conversation,
            ConversationRef,
        ):
            msg = "Model request conversation must be a ConversationRef or None."
            raise TypeError(msg)
        if self.provider_settings is not None and not isinstance(
            self.provider_settings,
            ProviderRequestSettings,
        ):
            msg = (
                "Model request provider settings must be a provider extension "
                "or None."
            )
            raise TypeError(msg)
        if not isinstance(self.tools, tuple) or not all(
            isinstance(tool, ModelToolDefinition) for tool in self.tools
        ):
            msg = "Model request tools must be a tuple of ModelToolDefinition values."
            raise TypeError(msg)
        if len({tool.name for tool in self.tools}) != len(self.tools):
            msg = "Model request Tool definition names must be unique."
            raise ValueError(msg)
