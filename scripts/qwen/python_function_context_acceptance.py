# Copyright (c) 2026
# ruff: noqa: E402, INP001, T201
"""Run one bounded live B-0002 Python-function Context acceptance."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from devtools.context import (
    PythonFunctionExactNameQuery,
    Repository,
    RepositoryResourceAddress,
    assemble_python_function_context_model_request,
    derive_python_function_declarations,
    disclose_python_function_exact_name_retrieval,
    materialize_python_function_disclosure_source,
    observe_repository_resource,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelSettings,
    Prompt,
)
from devtools.models.interaction.providers import LlamaCppInteraction

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.models.interaction import (
        ModelInteraction,
        ModelTermination,
        ModelUsage,
    )

_DEFAULT_ENDPOINT = "http://127.0.0.1:8080"
_DEFAULT_MODEL = "qwen38-local"
_FUNCTION_NAME = "selected_function"
_RESOURCE_ADDRESS = RepositoryResourceAddress("module.py")
_MAXIMUM_OUTPUT_TOKENS = 64
_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024
_REPORT_SCHEMA = "b0002-python-function-context-live-acceptance/1"
_TASK = (
    "Read the supporting repository Context supplied after this task. Return only "
    "the exact string value returned by the direct module-body function named "
    "selected_function. Do not include quotes, code fences, or explanation. Do "
    "not execute the source."
)


@dataclass(frozen=True, slots=True)
class B0002ContextConsumptionReport:
    """Retain bounded facts from one Context-consumption interaction."""

    endpoint: str
    model: str
    model_source: str
    repository_snapshot_id: str
    queried_function_name: str
    retrieval_match_count: int
    rendered_context_utf8_bytes: int
    assembled_prompt_utf8_bytes: int
    expected_value: str
    task: str
    raw_response: str
    normalized_response: str
    reasoning_content: str | None
    termination: ModelTermination | None
    usage: ModelUsage | None
    passed: bool


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse one established local endpoint and caller-selected report path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default=_DEFAULT_ENDPOINT)
    parser.add_argument("--model", default=_DEFAULT_MODEL)
    parser.add_argument("--report-path", required=True, type=Path)
    return parser.parse_args(arguments)


async def run_acceptance(
    *,
    repository_root: Path,
    nonce: str,
    interaction: ModelInteraction,
    endpoint: str,
    model: str,
) -> B0002ContextConsumptionReport:
    """Exercise the production information path and one direct interaction."""
    module = repository_root / _RESOURCE_ADDRESS.value
    module.write_text(
        f'def {_FUNCTION_NAME}():\n    return "{nonce}"\n',
        encoding="utf-8",
        newline="",
    )
    snapshot = observe_repository_resource(
        repository=Repository.new(),
        root=ResolvedPath(repository_root),
        address=_RESOURCE_ADDRESS,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )
    analysis = derive_python_function_declarations(snapshot)
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=analysis.declarations,
        query=PythonFunctionExactNameQuery(_FUNCTION_NAME),
    )
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(
            prompt=Prompt(content=_TASK, role="user"),
            settings=ModelSettings(
                maximum_output_tokens=_MAXIMUM_OUTPUT_TOKENS,
                thinking_enabled=False,
            ),
        ),
        context=rendered,
    )
    if nonce in _TASK:
        msg = "Fixture nonce unexpectedly appears in the task."
        raise ValueError(msg)
    if rendered.text.count(nonce) != 1 or request.prompt.content.count(nonce) != 1:
        msg = "Fixture nonce must reach the request exactly once through Context."
        raise ValueError(msg)

    response = await interaction.send(request)
    normalized_response = response.content.strip()
    return B0002ContextConsumptionReport(
        endpoint=endpoint,
        model=model,
        model_source=str(response.source),
        repository_snapshot_id=str(snapshot.id),
        queried_function_name=_FUNCTION_NAME,
        retrieval_match_count=len(retrieval.matches),
        rendered_context_utf8_bytes=len(rendered.text.encode("utf-8")),
        assembled_prompt_utf8_bytes=len(request.prompt.content.encode("utf-8")),
        expected_value=nonce,
        task=_TASK,
        raw_response=response.content,
        normalized_response=normalized_response,
        reasoning_content=response.reasoning_content,
        termination=response.termination,
        usage=response.usage,
        passed=normalized_response == nonce,
    )


async def run(arguments: argparse.Namespace) -> B0002ContextConsumptionReport:
    """Run one disposable fixture against the established llama.cpp endpoint."""
    nonce = f"RI_NONCE_{uuid4().hex.upper()}"
    with tempfile.TemporaryDirectory(prefix="devtools-b0002-context-") as directory:
        return await run_acceptance(
            repository_root=Path(directory),
            nonce=nonce,
            interaction=LlamaCppInteraction(
                endpoint=arguments.endpoint,
                model=arguments.model,
                source=InteractionSource("qwen-b0002-context-acceptance"),
            ),
            endpoint=arguments.endpoint,
            model=arguments.model,
        )


def _usage_payload(usage: ModelUsage | None) -> dict[str, int | None] | None:
    """Serialize only provider-reported usage facts without estimation."""
    if usage is None:
        return None
    return {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens": usage.total_tokens,
    }


def _report_payload(report: B0002ContextConsumptionReport) -> dict[str, object]:
    """Serialize this experiment's bounded result without broader claims."""
    return {
        "schema": _REPORT_SCHEMA,
        "verdict": "PASS" if report.passed else "FAIL",
        "scope": "one bounded model consumption of supplied Python-function Context",
        "model": {
            "provider": "llama.cpp",
            "endpoint": report.endpoint,
            "served_name": report.model,
            "response_source": report.model_source,
            "thinking_enabled": False,
            "maximum_output_tokens": _MAXIMUM_OUTPUT_TOKENS,
        },
        "fixture": {
            "resource_address": str(_RESOURCE_ADDRESS),
            "queried_function_name": report.queried_function_name,
            "repository_snapshot_id": report.repository_snapshot_id,
            "expected_value": report.expected_value,
            "task": report.task,
            "task_contains_expected_value": report.expected_value in report.task,
        },
        "measurements": {
            "retrieval_match_count": report.retrieval_match_count,
            "rendered_context_utf8_bytes": report.rendered_context_utf8_bytes,
            "assembled_prompt_utf8_bytes": report.assembled_prompt_utf8_bytes,
            "model_usage": _usage_payload(report.usage),
        },
        "response": {
            "raw": report.raw_response,
            "normalized": report.normalized_response,
            "reasoning_content": report.reasoning_content,
            "termination": (
                report.termination.value if report.termination is not None else None
            ),
            "exact_acceptance_passed": report.passed,
        },
        "model_capabilities_exposed": {
            "repository_filesystem": False,
            "repository_search": False,
            "tools": False,
            "shell": False,
        },
    }


def _write_report(path: Path, payload: dict[str, object]) -> None:
    """Atomically write one caller-selected experiment artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{uuid4()}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as output:
            json.dump(payload, output, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        temporary_path.replace(path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def main(arguments: Sequence[str] | None = None) -> None:
    """Run one live attempt and persist its exact bounded verdict."""
    parsed = parse_arguments(arguments)
    try:
        report = asyncio.run(run(parsed))
    except Exception as error:
        _write_report(
            parsed.report_path,
            {
                "schema": _REPORT_SCHEMA,
                "verdict": "FAIL - RUNNER",
                "runner_failure": {
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                },
            },
        )
        raise SystemExit(1) from error
    _write_report(parsed.report_path, _report_payload(report))
    print(f"acceptance verdict: {'PASS' if report.passed else 'FAIL'}")
    print(f"expected value: {report.expected_value}")
    print(f"returned value: {report.normalized_response}")
    raise SystemExit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
