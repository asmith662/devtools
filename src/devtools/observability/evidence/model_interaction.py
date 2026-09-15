# Copyright (c) 2026
"""Capture-controlled immutable Evidence for one model-interaction occurrence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, cast

from devtools.core.time import Duration, Timestamp
from devtools.observability.evidence.terminal import EvidenceId

if TYPE_CHECKING:
    from devtools.models.interaction import (
        ModelInteractionId,
        ModelInteractionObservation,
        ModelSettings,
        ModelTermination,
        ModelToolCall,
        ModelToolDefinition,
        ModelUsage,
        ProviderRequestSettings,
    )
    from devtools.models.interaction.models import InteractionSource
    from devtools.models.serving.identity import ServingProfileIdentity


class CaptureAction(StrEnum):
    """Select how one approved payload category is retained."""

    CAPTURE = "capture"
    OMIT = "omit"
    REDACT = "redact"


class CaptureState(StrEnum):
    """Describe the historical retention state of one payload category."""

    CAPTURED = "captured"
    OMITTED = "omitted"
    REDACTED = "redacted"
    UNAVAILABLE = "unavailable"
    PARTIAL = "partial"


@dataclass(frozen=True, slots=True)
class ModelInteractionCapturePolicy:
    """Choose retention for approved model-interaction payload classes."""

    prompt: CaptureAction = CaptureAction.OMIT
    visible_content: CaptureAction = CaptureAction.OMIT
    reasoning_content: CaptureAction = CaptureAction.OMIT
    provider_response_id: CaptureAction = CaptureAction.OMIT
    provider_model: CaptureAction = CaptureAction.OMIT
    tool_schemas: CaptureAction = CaptureAction.OMIT
    tool_call_arguments: CaptureAction = CaptureAction.OMIT


@dataclass(frozen=True, slots=True)
class ModelInteractionCaptureManifest:
    """Make payload availability and retention decisions inspectable."""

    prompt: CaptureState
    visible_content: CaptureState
    reasoning_content: CaptureState
    provider_response_id: CaptureState
    provider_model: CaptureState
    tool_schemas: CaptureState
    tool_call_arguments: CaptureState


@dataclass(frozen=True, slots=True)
class CapturedText:
    """Retain one approved textual payload without conflating absence states."""

    state: CaptureState
    value: str | None

    def __post_init__(self) -> None:
        """Enforce the manifest/value relationship."""
        retained = self.state in {CaptureState.CAPTURED, CaptureState.REDACTED}
        if retained != (self.value is not None):
            msg = (
                "Captured text value must exist exactly for captured or redacted "
                "state."
            )
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class CapturedModelRequest:
    """Record structural request facts and policy-controlled prompt text."""

    role: str
    prompt: CapturedText
    settings: ModelSettings
    conversation_present: bool
    provider_settings_type: str | None
    tools: tuple[CapturedModelToolDefinition, ...]


@dataclass(frozen=True, slots=True)
class CapturedModelResponse:
    """Record structural response facts and policy-controlled model text."""

    source: InteractionSource
    visible_content: CapturedText
    reasoning_content: CapturedText
    usage: ModelUsage | None
    termination: ModelTermination | None
    conversation_present: bool
    tool_calls: tuple[CapturedModelToolCall, ...]


@dataclass(frozen=True, slots=True)
class CapturedModelToolDefinition:
    """Record one disclosed normalized Tool without executable capability."""

    name: str
    description: str
    input_schema: CapturedText


@dataclass(frozen=True, slots=True)
class CapturedModelToolCall:
    """Record one returned normalized Tool request without authority."""

    name: str
    provider_call_id: str | None
    arguments: CapturedText


@dataclass(frozen=True, slots=True)
class ProviderExchange:
    """Retain bounded provider-boundary facts only through interaction Evidence."""

    provider: str
    response_id: CapturedText
    provider_model: CapturedText


@dataclass(frozen=True, slots=True, kw_only=True)
class ModelInteractionEvidence:
    """Record immutable historical truth for one observed model invocation."""

    id: EvidenceId
    interaction_id: ModelInteractionId
    occurred_at: Timestamp
    observed_at: Timestamp
    duration: Duration
    request: CapturedModelRequest
    response: CapturedModelResponse
    serving_profile: ServingProfileIdentity | None
    capture_manifest: ModelInteractionCaptureManifest
    provider_exchange: ProviderExchange

    @classmethod
    def from_observation(
        cls,
        observation: ModelInteractionObservation,
        *,
        policy: ModelInteractionCapturePolicy,
        serving_profile: ServingProfileIdentity | None,
    ) -> ModelInteractionEvidence:
        """Construct immutable Evidence while source payloads are still available."""
        prompt = _capture(observation.request.prompt.content, policy.prompt)
        visible = _capture(observation.response.content, policy.visible_content)
        reasoning = _capture(
            observation.response.reasoning_content,
            policy.reasoning_content,
        )
        response_id = _capture(
            observation.provider_response_id,
            policy.provider_response_id,
        )
        provider_model = _capture(observation.provider_model, policy.provider_model)
        tools = tuple(
            _captured_tool_definition(tool, policy.tool_schemas)
            for tool in observation.request.tools
        )
        tool_calls = tuple(
            _captured_tool_call(call, policy.tool_call_arguments)
            for call in observation.response.tool_calls
        )
        manifest = ModelInteractionCaptureManifest(
            prompt=prompt.state,
            visible_content=visible.state,
            reasoning_content=reasoning.state,
            provider_response_id=response_id.state,
            provider_model=provider_model.state,
            tool_schemas=_aggregate_capture_state(
                tuple(tool.input_schema for tool in tools),
            ),
            tool_call_arguments=_aggregate_capture_state(
                tuple(call.arguments for call in tool_calls),
            ),
        )
        return cls(
            id=EvidenceId.new(),
            interaction_id=observation.interaction_id,
            occurred_at=observation.completed_at,
            observed_at=Timestamp.now(),
            duration=cast(
                "Duration",
                observation.completed_at - observation.started_at,
            ),
            request=CapturedModelRequest(
                role=observation.request.prompt.role,
                prompt=prompt,
                settings=observation.request.settings,
                conversation_present=observation.request.conversation is not None,
                provider_settings_type=_provider_settings_type(
                    observation.request.provider_settings,
                ),
                tools=tools,
            ),
            response=CapturedModelResponse(
                source=observation.response.source,
                visible_content=visible,
                reasoning_content=reasoning,
                usage=observation.response.usage,
                termination=observation.response.termination,
                conversation_present=observation.response.conversation is not None,
                tool_calls=tool_calls,
            ),
            serving_profile=serving_profile,
            capture_manifest=manifest,
            provider_exchange=ProviderExchange(
                provider=observation.provider,
                response_id=response_id,
                provider_model=provider_model,
            ),
        )


class ModelInteractionInspector:
    """Collect and inspect process-local model-interaction Evidence."""

    __slots__ = (
        "_evidence_by_id",
        "_evidence_by_interaction_id",
        "_policy",
        "_serving_profile",
    )

    def __init__(
        self,
        *,
        policy: ModelInteractionCapturePolicy | None = None,
        serving_profile: ServingProfileIdentity | None = None,
    ) -> None:
        """Create an optional observer with explicit capture configuration."""
        self._policy = policy or ModelInteractionCapturePolicy()
        self._serving_profile = serving_profile
        self._evidence_by_id: dict[EvidenceId, ModelInteractionEvidence] = {}
        self._evidence_by_interaction_id: dict[
            ModelInteractionId, ModelInteractionEvidence,
        ] = {}

    def interaction_completed(self, observation: ModelInteractionObservation) -> None:
        """Construct and collect Evidence for one completed observed interaction."""
        self.accept(
            ModelInteractionEvidence.from_observation(
                observation,
                policy=self._policy,
                serving_profile=self._serving_profile,
            ),
        )

    def accept(self, evidence: ModelInteractionEvidence) -> None:
        """Retain the first immutable Evidence for each interaction occurrence."""
        if evidence.interaction_id in self._evidence_by_interaction_id:
            return
        self._evidence_by_id[evidence.id] = evidence
        self._evidence_by_interaction_id[evidence.interaction_id] = evidence

    def get_evidence(self, evidence_id: EvidenceId) -> ModelInteractionEvidence | None:
        """Return one collected Evidence record."""
        return self._evidence_by_id.get(evidence_id)

    def get_evidence_for_interaction(
        self,
        interaction_id: ModelInteractionId,
    ) -> ModelInteractionEvidence | None:
        """Return Evidence correlated to one interaction occurrence."""
        return self._evidence_by_interaction_id.get(interaction_id)

    def evidence_ids(self) -> tuple[EvidenceId, ...]:
        """Return retained Evidence identities in insertion order."""
        return tuple(self._evidence_by_id)

    def clear(self) -> None:
        """Discard process-local inspection references."""
        self._evidence_by_id.clear()
        self._evidence_by_interaction_id.clear()


def _capture(value: str | None, action: CaptureAction) -> CapturedText:
    """Capture one approved text value without admitting unavailable payloads."""
    if value is None:
        return CapturedText(CaptureState.UNAVAILABLE, None)
    if action is CaptureAction.CAPTURE:
        return CapturedText(CaptureState.CAPTURED, value)
    if action is CaptureAction.REDACT:
        return CapturedText(CaptureState.REDACTED, "[REDACTED]")
    return CapturedText(CaptureState.OMITTED, None)


def _provider_settings_type(value: ProviderRequestSettings | None) -> str | None:
    """Retain extension presence structurally without serializing its values."""
    return type(value).__name__ if value is not None else None


def _captured_tool_definition(
    tool: ModelToolDefinition,
    action: CaptureAction,
) -> CapturedModelToolDefinition:
    """Capture a disclosed schema without retaining an executable Tool."""
    return CapturedModelToolDefinition(
        name=tool.name,
        description=tool.description,
        input_schema=_capture(tool.input_schema_json, action),
    )


def _captured_tool_call(
    call: ModelToolCall,
    action: CaptureAction,
) -> CapturedModelToolCall:
    """Capture untrusted returned arguments without materializing input."""
    return CapturedModelToolCall(
        name=call.name,
        provider_call_id=call.provider_call_id,
        arguments=_capture(call.arguments_json, action),
    )


def _aggregate_capture_state(values: tuple[CapturedText, ...]) -> CaptureState:
    """Summarize collection retention without hiding partially captured values."""
    if not values:
        return CaptureState.UNAVAILABLE
    states = {value.state for value in values}
    if len(states) == 1:
        return values[0].state
    return CaptureState.PARTIAL
