# Copyright (c) 2026
# ruff: noqa: INP001, SLF001
"""Deterministic tests for the B-0002 live Context acceptance runner."""

from __future__ import annotations

import asyncio
import importlib.util
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelUsage,
)

if TYPE_CHECKING:
    from types import ModuleType

_SCRIPT_PATH = Path("scripts/qwen/python_function_context_acceptance.py").resolve()
_NONCE = "RI_NONCE_DETERMINISTIC_8C24B1"
_MAXIMUM_OUTPUT_TOKENS = 64
_SHA256_HEX_LENGTH = 64


@pytest.fixture
def acceptance() -> ModuleType:
    """Load the operational script without making scripts a package API."""
    specification = importlib.util.spec_from_file_location(
        "test_python_function_context_acceptance",
        _SCRIPT_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@dataclass(slots=True)
class _ScriptedInteraction:
    """Return one fixed response while retaining the exact canonical request."""

    response_content: str
    calls: list[ModelRequest] = field(default_factory=list)
    source: InteractionSource = field(
        default_factory=lambda: InteractionSource("scripted-qwen"),
    )

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Record one request without provider, filesystem, or Tool behavior."""
        self.calls.append(request)
        return ModelResponse(
            content=self.response_content,
            reasoning_content="Literal extraction from supplied Context.",
            source=self.source,
            termination=ModelTermination.NORMAL_STOP,
            usage=ModelUsage(input_tokens=101, output_tokens=7, total_tokens=108),
        )


def test_runner_defaults_to_established_qwen_service(acceptance: ModuleType) -> None:
    """CLI defaults reuse the existing endpoint and served-name convention."""
    arguments = acceptance.parse_arguments(["--report-path", "report.json"])

    assert arguments.endpoint == "http://127.0.0.1:8080"
    assert arguments.model == "qwen38-local"
    assert arguments.report_path == Path("report.json")


def test_full_pipeline_accepts_exact_context_dependent_response(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The deterministic fake consumes the exact request produced by every layer."""
    interaction = _ScriptedInteraction(f" \n{_NONCE}\r\n")

    report = asyncio.run(
        acceptance.run_acceptance(
            repository_root=tmp_path,
            nonce=_NONCE,
            interaction=interaction,
            endpoint="http://127.0.0.1:8080",
            model="qwen38-local",
        ),
    )

    assert report.passed is True
    assert report.expected_value == _NONCE
    assert report.raw_response == f" \n{_NONCE}\r\n"
    assert report.normalized_response == _NONCE
    assert report.queried_function_name == "selected_function"
    assert report.retrieval_match_count == 1
    assert len(report.repository_snapshot_id) == _SHA256_HEX_LENGTH
    assert report.rendered_context_utf8_bytes > len(_NONCE.encode("utf-8"))
    assert report.assembled_prompt_utf8_bytes > report.rendered_context_utf8_bytes
    assert report.termination is ModelTermination.NORMAL_STOP
    assert report.usage == ModelUsage(101, 7, 108)
    assert len(interaction.calls) == 1
    request = interaction.calls[0]
    assert isinstance(request, ModelRequest)
    assert request.prompt.role == "user"
    assert _NONCE not in report.task
    assert request.prompt.content.count(_NONCE) == 1
    assert 'return "RI_NONCE_DETERMINISTIC_8C24B1"' in request.prompt.content
    assert request.settings.maximum_output_tokens == _MAXIMUM_OUTPUT_TOKENS
    assert request.settings.thinking_enabled is False
    assert request.conversation is None
    assert request.provider_settings is None
    assert request.tools == ()

    payload = acceptance._report_payload(report)
    assert payload["schema"] == "b0002-python-function-context-live-acceptance/1"
    assert payload["verdict"] == "PASS"
    assert payload["fixture"]["task_contains_expected_value"] is False
    assert payload["measurements"] == {
        "retrieval_match_count": 1,
        "rendered_context_utf8_bytes": report.rendered_context_utf8_bytes,
        "assembled_prompt_utf8_bytes": report.assembled_prompt_utf8_bytes,
        "model_usage": {
            "input_tokens": 101,
            "output_tokens": 7,
            "total_tokens": 108,
        },
    }
    assert payload["response"]["exact_acceptance_passed"] is True
    assert payload["model_capabilities_exposed"] == {
        "repository_filesystem": False,
        "repository_search": False,
        "tools": False,
        "shell": False,
    }


def test_acceptance_rejects_nonmatching_model_text(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """A plausible explanation cannot satisfy the strict extraction criterion."""
    report = asyncio.run(
        acceptance.run_acceptance(
            repository_root=tmp_path,
            nonce=_NONCE,
            interaction=_ScriptedInteraction(f'The value is "{_NONCE}".'),
            endpoint="local",
            model="scripted",
        ),
    )

    assert report.passed is False
    assert report.normalized_response == f'The value is "{_NONCE}".'
    assert acceptance._report_payload(report)["verdict"] == "FAIL"


def test_report_writer_persists_one_stable_json_artifact(
    acceptance: ModuleType,
    tmp_path: Path,
) -> None:
    """The experiment report is caller-selected and local to this acceptance."""
    report_path = tmp_path / "reports" / "acceptance.json"
    payload = {"schema": "test", "verdict": "PASS"}

    acceptance._write_report(report_path, payload)

    assert json.loads(report_path.read_text(encoding="utf-8")) == payload
    assert report_path.read_bytes().endswith(b"\n")
    assert list(report_path.parent.glob(".*.tmp")) == []
