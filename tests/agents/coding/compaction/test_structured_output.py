# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- strict format versus semantic truth controls
"""Provider-selected JSON never replaces fallible-note validation."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding.compaction.format import record, validate_summary
from devtools.models.interaction import PromptMessage, ProviderRequestSettings
from tests.agents.coding.compaction.test_semantic import (
    Summarizer,
    latest,
    prepare,
    setup,
)

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
