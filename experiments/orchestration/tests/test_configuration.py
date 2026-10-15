# Copyright (c) 2026
# ruff: noqa: S101, D103 -- offline known-shape checks do not invoke Codex
"""Reject the historical provider failure before any real exec process."""

from pathlib import Path

import pytest

from experiments.orchestration.workers import codex, runtime


def test_generated_semantic_profile_passes_and_never_overrides_provider(
    tmp_path: Path,
) -> None:
    config = {
        "model_id": "gpt-6-astra",
        "reasoning": "High",
        "runtime": runtime.configuration(),
    }
    argv = codex.argv(
        config,
        tmp_path,
        schema=tmp_path / "schema",
        response=tmp_path / "response",
    )
    result = runtime.preflight(argv)
    assert result["status"] == "PASS"
    assert result["provider_transport_retries"] == "BUILTIN_RUNTIME_DEFAULT"
    assert result["underlying_request_count"] == "UNKNOWN"
    assert result["automatic_scientific_retries"] == 0
    assert not any("model_providers" in a for a in argv)


@pytest.mark.parametrize(
    "value",
    [
        "model_providers.openai.request_max_retries=0",
        "model_providers.openai.stream_max_retries=0",
        'model_providers={openai={name="bad"}}',
        'model_providers.custom.name="also forbidden"',
        "unknown.setting=true",
        'features.shell_tool="false"',
        'permissions.semantic-worker.network.enabled="false"',
    ],
)
def test_reserved_provider_and_unknown_shapes_fail_locally(value: str) -> None:
    with pytest.raises(ValueError, match=r"Provider|Unsupported"):
        runtime.preflight(["-c", value])
