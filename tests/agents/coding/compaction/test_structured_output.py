# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- strict format versus semantic truth controls
"""Provider-selected JSON never replaces fallible-note validation."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.compaction.format import (
    record,
    summary_payload,
    validate_summary,
)
from devtools.models.interaction import (
    ModelRequest,
    ModelResponse,
    PromptMessage,
    ProviderRequestSettings,
)
from tests.agents.coding.compaction.test_semantic import (
    Summarizer,
    latest,
    prepare,
    setup,
)
from tests.agents.coding.test_repository import EDIT, LIMITS, READ, Script

if TYPE_CHECKING:
    from pathlib import Path


def test_independent_settings_reach_auxiliary_request_only(tmp_path: Path) -> None:
    settings = ProviderRequestSettings("independent-json-capability")
    model = Summarizer()
    host = setup(tmp_path, model, provider_settings=settings, retain_payloads=True)
    host.request_compaction()
    acting = prepare(host)
    assert model.requests[0].provider_settings is settings
    assert acting.provider_settings is None
    assert latest(host).adopted
    assert latest(host).request is model.requests[0]
    usage = latest(host).usage
    assert usage is not None
    assert usage.input_tokens == 10


@pytest.mark.parametrize(
    "envelope",
    ["```json\n{}\n```", "Prose {}", "{} {}", "{} trailing"],
)
def test_no_fence_or_generic_json_salvage(envelope: str) -> None:
    with pytest.raises(json.JSONDecodeError):
        validate_summary(envelope, {}, frozenset(), {})


def test_real_citation_is_not_semantic_support_or_authority() -> None:
    original = PromptMessage(
        "assistant",
        "I have not run a check; the cause is unknown.",
    )
    observed = record(original)
    text = json.dumps(
        {
            "version": 1,
            "notes": [
                {
                    "kind": "decision",
                    "text": "A passing check proves the bug was caused by sorting.",
                    "refs": [{"index": 1, "digest": observed["digest"]}],
                },
            ],
            "sources": [],
        },
    )
    note = validate_summary(text, {1: str(observed["digest"])}, frozenset({1}), {})
    # Deliberately unsupported causality with exact membership is accepted as
    # untrusted interpretation, not certified truth. No source witness results.
    assert note.role == "assistant"
    assert "UNTRUSTED" in note.content
    assert note.tool_calls == ()
    assert note.tool_call_id is None
    assert "sorting" in note.content


@pytest.mark.parametrize("wrapper", ["```json\n{}\n```", " \t```json\r\n{}\r\n```\r\n"])
def test_explicit_one_fence_policy(wrapper: str) -> None:
    assert summary_payload(wrapper, allow_json_fence=False) == (wrapper, False)
    payload, normalized = summary_payload(wrapper, allow_json_fence=True)
    assert normalized
    assert json.loads(payload) == {}
    assert summary_payload("{}", allow_json_fence=True) == ("{}", False)


@pytest.mark.parametrize(
    "text",
    [
        "```JSON\n{}\n```",
        "```\n{}\n```",
        "```json\n{}\n``` prose",
        "```json\n{}\n```\n```json\n{}\n```",
        "```json\n{}",
        "```json\n{} {}\n```",
        "```json\n{\n```",
        "prose\n```json\n{}\n```",
    ],
)
def test_envelope_never_salvages_malformed_or_multiple_documents(text: str) -> None:
    with pytest.raises(ValueError, match=r"envelope|Expecting|Extra data"):
        validate_summary(
            summary_payload(text, allow_json_fence=True)[0],
            {},
            frozenset(),
            {},
        )


def test_shared_non_qwen_actor_consumes_normalized_notes_and_exact_source(
    tmp_path: Path,
) -> None:
    class Fenced(Summarizer):
        async def send(self, request: ModelRequest) -> ModelResponse:
            response = await super().send(request)
            return replace(response, content="```json\n" + response.content + "\n```")

    model = Fenced()
    host = setup(tmp_path, model, allow_json_fence=True, retain_payloads=True)
    original = tuple(host.messages)
    host.request_compaction()

    class Acting(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            assert "UNTRUSTED" in str(request.prompt)
            assert "irrelevant " * 20 not in str(request.prompt)
            if self.entries == 0:
                assert host.active_disclosures == ()
            return await super().send(request)

    actor = Acting([(READ,), (EDIT,)])
    result = asyncio.run(run_coding_agent(actor, limits=LIMITS, host=host))
    assert result.accepted
    assert actor.entries == 2
    assert len(model.requests) == 1
    assert tuple(host.messages[: len(original)]) == original
    receipt = latest(host)
    assert receipt.adopted
    assert receipt.normalized_json_fence
    assert receipt.response is not None
    assert receipt.response.content.startswith("```json\n")
    assert host.source_results


def test_invalid_envelope_policy_is_not_truthy_authorization(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="configuration"):
        setup(tmp_path, allow_json_fence="yes")


def test_normalization_does_not_relax_provenance_or_trigger_retry(
    tmp_path: Path,
) -> None:
    class Foreign(Summarizer):
        async def send(self, request: ModelRequest) -> ModelResponse:
            response = await super().send(request)
            return replace(response, content="```json\n" + response.content + "\n```")

    model = Foreign("foreign-ref")
    host = setup(tmp_path, model, allow_json_fence=True)
    deterministic = prepare(host)
    host.request_compaction()
    assert prepare(host) == deterministic
    assert latest(host).normalized_json_fence
    assert not latest(host).validated
    assert latest(host).status == "failed"
    assert prepare(host) == deterministic
    assert len(model.requests) == 1
