# Copyright (c) 2026
"""Tests for capture-controlled model interaction Evidence."""

from __future__ import annotations

import asyncio
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from devtools.core.time import Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelInteractionId,
    ModelInteractionObservation,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelTermination,
    ModelUsage,
    Prompt,
)
from devtools.models.interaction.providers import LlamaCppRequestSettings, llama_cpp
from devtools.models.interaction.providers.llama_cpp import LlamaCppInteraction
from devtools.models.serving import ServingProfileFingerprint, ServingProfileIdentity
from devtools.observability.evidence import (
    CaptureAction,
    CapturedText,
    CaptureState,
    ModelInteractionCapturePolicy,
    ModelInteractionEvidence,
    ModelInteractionInspector,
)


def _observation(
    *,
    content: str = "OK",
    reasoning: str | None = None,
    thinking_enabled: bool | None = False,
    termination: ModelTermination | None = ModelTermination.NORMAL_STOP,
) -> ModelInteractionObservation:
    """Create one deterministic completed llama.cpp observation."""
    source = InteractionSource("llama-cpp")
    return ModelInteractionObservation(
        interaction_id=ModelInteractionId.parse(
            "00000000-0000-4000-8000-000000000001",
        ),
        provider="llama.cpp",
        source=source,
        request=ModelRequest(
            prompt=Prompt("Reply with exactly: OK", "user"),
            settings=ModelSettings(
                maximum_output_tokens=512,
                thinking_enabled=thinking_enabled,
            ),
            provider_settings=LlamaCppRequestSettings(),
        ),
        response=ModelResponse(
            content=content,
            reasoning_content=reasoning,
            source=source,
            usage=ModelUsage(input_tokens=57, output_tokens=2, total_tokens=59),
            termination=termination,
        ),
        started_at=Timestamp(datetime(2026, 1, 1, tzinfo=UTC)),
        completed_at=Timestamp(datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC)),
        provider_response_id="chatcmpl-1",
        provider_model="qwen3.8",
    )


def _profile() -> ServingProfileIdentity:
    """Create deterministic serving provenance without operational state."""
    return ServingProfileIdentity(
        fingerprint=ServingProfileFingerprint("qwen38-profile-v1"),
        provider="llama.cpp",
        served_model_alias="qwen38",
        context_capacity=32768,
        model_repository="unsloth/Qwen3.8-27B-GGUF",
        model_revision="16b6",
        artifact_filename="model.gguf",
        artifact_hash="abc",
        quantization="IQ4_XS",
        server_build="llama.cpp:b10868",
        template_reasoning_defaults="provider-default",
    )


def test_capture_enabled_preserves_structural_and_approved_payload_facts() -> None:
    """Scenario A records a complete approved diagnostic without raw transport data."""
    policy = ModelInteractionCapturePolicy(
        prompt=CaptureAction.CAPTURE,
        visible_content=CaptureAction.CAPTURE,
        provider_response_id=CaptureAction.CAPTURE,
        provider_model=CaptureAction.CAPTURE,
    )
    evidence = ModelInteractionEvidence.from_observation(
        _observation(), policy=policy, serving_profile=_profile(),
    )
    assert evidence.request.settings == ModelSettings(
        maximum_output_tokens=512,
        thinking_enabled=False,
    )
    assert evidence.request.provider_settings_type == "LlamaCppRequestSettings"
    assert evidence.request.prompt.value == "Reply with exactly: OK"
    assert evidence.response.visible_content.value == "OK"
    assert evidence.response.reasoning_content.state is CaptureState.UNAVAILABLE
    assert evidence.response.usage == ModelUsage(57, 2, 59)
    assert evidence.response.termination is ModelTermination.NORMAL_STOP
    assert evidence.provider_exchange.response_id.value == "chatcmpl-1"
    assert evidence.serving_profile == _profile()
    assert evidence.duration.total_seconds == 1


def test_omission_unavailability_and_redaction_are_distinct_and_nonleaking() -> None:
    """Scenarios B--D make all payload absence states explicit."""
    omitted = ModelInteractionEvidence.from_observation(
        _observation(),
        policy=ModelInteractionCapturePolicy(),
        serving_profile=None,
    )
    assert omitted.request.prompt.state is CaptureState.OMITTED
    assert omitted.request.prompt.value is None
    assert omitted.response.reasoning_content.state is CaptureState.UNAVAILABLE
    assert omitted.capture_manifest.visible_content is CaptureState.OMITTED

    redacted = ModelInteractionEvidence.from_observation(
        _observation(reasoning="secret thought"),
        policy=ModelInteractionCapturePolicy(
            visible_content=CaptureAction.REDACT,
            reasoning_content=CaptureAction.REDACT,
        ),
        serving_profile=None,
    )
    assert redacted.response.visible_content == CapturedText(
        CaptureState.REDACTED, "[REDACTED]",
    )
    assert redacted.response.reasoning_content.value == "[REDACTED]"
    assert "secret thought" not in str(redacted)
    assert "OK" not in str(redacted)


def test_output_limit_and_thinking_disabled_diagnostics_remain_independent() -> None:
    """Scenarios F and G retain actual response facts without inference."""
    limit = ModelInteractionEvidence.from_observation(
        _observation(
            content="",
            reasoning="Thinking...",
            thinking_enabled=True,
            termination=ModelTermination.OUTPUT_LIMIT,
        ),
        policy=ModelInteractionCapturePolicy(
            visible_content=CaptureAction.CAPTURE,
            reasoning_content=CaptureAction.CAPTURE,
        ),
        serving_profile=None,
    )
    assert limit.request.settings.thinking_enabled is True
    assert limit.response.visible_content.value == ""
    assert limit.response.reasoning_content.value == "Thinking..."
    assert limit.response.termination is ModelTermination.OUTPUT_LIMIT

    normal = ModelInteractionEvidence.from_observation(
        _observation(), policy=ModelInteractionCapturePolicy(), serving_profile=None,
    )
    assert normal.request.settings.thinking_enabled is False
    assert normal.response.termination is ModelTermination.NORMAL_STOP


def test_inspector_retains_optional_distinct_and_immutable_evidence() -> None:
    """Scenarios E, H, and I preserve optional collection and historical values."""
    inspector = ModelInteractionInspector(serving_profile=_profile())
    first = _observation()
    inspector.interaction_completed(first)
    second = ModelInteractionObservation(
        interaction_id=ModelInteractionId.new(),
        provider=first.provider,
        source=first.source,
        request=first.request,
        response=first.response,
        started_at=first.started_at,
        completed_at=first.completed_at,
    )
    inspector.interaction_completed(second)
    records = inspector.evidence_ids()
    assert len(records) == len((first, second))
    evidence = inspector.get_evidence(records[0])
    assert evidence is not None
    with pytest.raises(FrozenInstanceError):
        evidence.request.settings = ModelSettings()  # type: ignore[misc]
    assert inspector.get_evidence_for_interaction(first.interaction_id) is evidence
    inspector.accept(evidence)
    assert inspector.evidence_ids() == records
    inspector.clear()
    assert inspector.evidence_ids() == ()


def test_retained_evidence_is_independent_of_mutable_provider_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Scenario I snapshots mutable decoded provider data through the real seam."""
    provider_response: dict[str, object] = {
        "id": "chatcmpl-original",
        "model": "qwen-original",
        "choices": [
            {
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": "ORIGINAL"},
            },
        ],
    }

    async def post_chat_completion(
        _endpoint: object,
        _payload: dict[str, object],
    ) -> dict[str, object]:
        return provider_response

    monkeypatch.setattr(llama_cpp, "_post_chat_completion", post_chat_completion)
    inspector = ModelInteractionInspector(
        policy=ModelInteractionCapturePolicy(
            visible_content=CaptureAction.CAPTURE,
            provider_response_id=CaptureAction.CAPTURE,
            provider_model=CaptureAction.CAPTURE,
        ),
    )
    interaction = LlamaCppInteraction(
        endpoint="http://127.0.0.1:8080",
        model="qwen-requested",
        source=InteractionSource("qwen"),
        observer=inspector,
    )

    asyncio.run(
        interaction.send(
            ModelRequest(
                prompt=Prompt("Reply with exactly: OK", "user"),
                provider_settings=LlamaCppRequestSettings(),
            ),
        ),
    )
    evidence_id = inspector.evidence_ids()[0]
    evidence = inspector.get_evidence(evidence_id)
    assert evidence is not None
    assert evidence.response.visible_content.value == "ORIGINAL"
    assert evidence.provider_exchange.response_id.value == "chatcmpl-original"
    assert evidence.provider_exchange.provider_model.value == "qwen-original"

    provider_response["id"] = "chatcmpl-mutated"
    provider_response["model"] = "qwen-mutated"
    choices = provider_response["choices"]
    assert isinstance(choices, list)
    message = choices[0]["message"]
    assert isinstance(message, dict)
    message["content"] = "MUTATED"

    assert provider_response["id"] == "chatcmpl-mutated"
    assert provider_response["model"] == "qwen-mutated"
    assert message["content"] == "MUTATED"
    assert evidence.response.visible_content.value == "ORIGINAL"
    assert evidence.provider_exchange.response_id.value == "chatcmpl-original"
    assert evidence.provider_exchange.provider_model.value == "qwen-original"


def test_identity_and_capture_values_reject_invalid_construction() -> None:
    """Exercise boundary validation without adding untyped escape hatches."""
    with pytest.raises(ValueError, match="nonblank"):
        ServingProfileFingerprint(" ")
    assert str(ServingProfileFingerprint("profile")) == "profile"
    with pytest.raises(ValueError, match="positive"):
        ServingProfileIdentity(
            fingerprint=ServingProfileFingerprint("x"),
            provider="llama.cpp",
            served_model_alias="qwen",
            context_capacity=0,
        )
    with pytest.raises(ValueError, match="Provider"):
        ServingProfileIdentity(
            fingerprint=ServingProfileFingerprint("x"),
            provider=" ",
            served_model_alias="qwen",
            context_capacity=1,
        )
    with pytest.raises(ValueError, match="positive"):
        ServingProfileIdentity(
            fingerprint=ServingProfileFingerprint("x"),
            provider="llama.cpp",
            served_model_alias="qwen",
            context_capacity=True,
        )
    with pytest.raises(ValueError, match="must exist"):
        CapturedText(CaptureState.CAPTURED, None)
    with pytest.raises(ValueError, match="must exist"):
        CapturedText(CaptureState.OMITTED, "not retained")
    with pytest.raises(ValueError, match="provider cannot be blank"):
        ModelInteractionObservation(
            interaction_id=ModelInteractionId.new(),
            provider=" ",
            source=InteractionSource("source"),
            request=ModelRequest(Prompt("x", "user")),
            response=ModelResponse("x", InteractionSource("source")),
            started_at=Timestamp(datetime(2026, 1, 2, tzinfo=UTC)),
            completed_at=Timestamp(datetime(2026, 1, 1, tzinfo=UTC)),
        )
    source = InteractionSource("source")
    with pytest.raises(ValueError, match="cannot complete"):
        ModelInteractionObservation(
            interaction_id=ModelInteractionId.new(),
            provider="llama.cpp",
            source=source,
            request=ModelRequest(Prompt("x", "user")),
            response=ModelResponse("x", source),
            started_at=Timestamp(datetime(2026, 1, 2, tzinfo=UTC)),
            completed_at=Timestamp(datetime(2026, 1, 1, tzinfo=UTC)),
        )
    identity = ModelInteractionId.parse("00000000-0000-4000-8000-000000000009")
    assert str(identity) == "00000000-0000-4000-8000-000000000009"
