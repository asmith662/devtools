# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0913, PLR0917, PLR0915, ASYNC109, ASYNC240, TRY300 -- bounded external-Agent semantic transport
"""Deliver host-owned disclosure and authenticate one tool-free JSON response."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration.observation import notify_operational
from experiments.orchestration.storage import binary, load, require, safe
from experiments.orchestration.workers import (
    capacity,
    codex,
    evidence,
    measurement,
    runtime,
)
from experiments.orchestration.workers import schema as response_schema
from experiments.orchestration.workers.budget import BudgetError, FailureClass
from experiments.orchestration.workers.process import invoke


def review(payload: Any, packet: Any, configuration: Any) -> Any:
    """Host assigns immutable identity and observed single-primary metadata."""
    require(
        configuration.get("evidence_locator") == evidence.CONTRACT,
        "Frozen exact-content locator contract required",
    )
    require(
        set(payload) == {"cells", "units", "gaps", "self_review"},
        "Primary judgment fields",
    )
    return {
        "schema": "blind-primary-review-v1",
        "case": packet["case"],
        "frame": packet["frame"],
        "packet_sha256": digest(json_bytes(packet)),
        "attestation": {
            "model": configuration["model"],
            "reasoning": configuration["reasoning"],
            "second_reviewer": False,
            "reconciliation": False,
            "host_routing_independently_verified": False,
            "blindness": configuration["blindness"],
        },
        **evidence.judgments(payload, packet),
    }


def strict_object(text: str) -> dict[str, Any]:
    """Reject duplicate keys, constants, fences, prose and non-object responses."""

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        require(len(dict(items)) == len(items), "Duplicate semantic JSON key")
        return dict(items)

    def constant(_value: str) -> Any:
        message = "Non-finite semantic JSON constant"
        raise ValueError(message)

    value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    require(isinstance(value, dict), "Semantic payload must be one JSON object")
    return dict(value)


def validate_schema(value: Any, schema: Any) -> None:
    """Validate only the fixed object/array/scalar/enum schema subset we emit."""
    response_schema.validate(value, schema)


def render_disclosure(
    configuration: Any,
    packet_raw: bytes,
    instruction_raw: bytes,
    invocation: str,
) -> bytes:
    """Render the exact legacy input independently of process/scientific entry."""
    packet = strict_object(packet_raw.decode("utf-8"))
    require(packet_raw == json_bytes(packet), "Canonical disclosed packet required")
    disclosure = {
        "schema": "host-semantic-disclosure-v1",
        "case": packet["case"],
        "frame": packet["frame"],
        "invocation": invocation,
        "model": configuration["model"],
        "reasoning": configuration["reasoning"],
        "instruction_sha256": digest(instruction_raw),
        "packet_sha256": digest(packet_raw),
        "instruction": instruction_raw.decode("utf-8"),
        "evidence_locator_contract": evidence.CONTRACT,
        "packet": evidence.disclosure(packet)
        if configuration.get("evidence_locator") == evidence.CONTRACT
        else packet,
    }
    return (
        "All authorized information is supplied below. Do not use shell or tools; "
        "do not inspect the filesystem or web; create no files. Return ONLY one "
        "JSON object matching the supplied response schema, containing your judgments. "
        "The HOST owns packet authentication, identifiers/attestation, serialization "
        "and builder execution. Never guess unseen content.\n"
        + json_bytes(disclosure).decode()
    ).encode()


def preflight_input(
    configuration: Any,
    rendered: bytes,
    schema: Any,
    *,
    engineering: bool = False,
) -> Any:
    """Run before a caller's ENTERED callback; repeat immediately before launch.

    Character, byte and schema gates do not invent a tokenizer or model context.
    Non-synthetic bounded work additionally needs an authenticated compatible
    empirical workload receipt. That receipt is not execution authority.
    """
    chars = len(rendered.decode("utf-8", errors="strict"))
    if chars > capacity.INPUT_CHARACTERS or len(rendered) > capacity.INPUT_BYTES:
        raise BudgetError(
            FailureClass.WORKLOAD_CAPACITY_LIMIT,
            f"{chars} chars/{len(rendered)} bytes exceed candidate workload; no model",
        )
    bound = response_schema.envelope(schema)
    if bound.utf8_bytes > response_schema.MAX_SEMANTIC_RESPONSE_UTF8_BYTES:
        raise BudgetError(
            FailureClass.OUTPUT_LIMIT,
            "Response envelope exceeds method capacity",
        )
    native = json_bytes(response_schema.native(schema))
    if len(native) > response_schema.MAX_NATIVE_SCHEMA_UTF8_BYTES:
        raise BudgetError(
            FailureClass.OUTPUT_SCHEMA_LIMIT,
            "Native response schema exceeds bounded host contract",
        )
    if not engineering:
        runtime.authenticate_configuration(configuration)
        root = Path(__file__).resolve().parents[3]
        binding = configuration["capacity_receipt"]
        receipt = load(safe(root, binding["path"]))
        capacity.check_input(receipt, configuration, rendered)
    return {
        "schema": "semantic-exact-preentry-budget-v1",
        "status": "PASS",
        "input_sha256": digest(rendered),
        "input_characters": chars,
        "input_bytes": len(rendered),
        "schema_sha256": digest(json_bytes(schema)),
        "native_schema_bytes": len(native),
        "response_maximum_bytes": bound.utf8_bytes,
        "context_tokens": "UNKNOWN",
        "policy": "EMPIRICAL_WORKLOAD_COMPATIBILITY; NOT_MAXIMUM_CAPACITY",
    }


async def primary(
    configuration: Any,
    packet_raw: bytes,
    instruction_raw: bytes,
    schema: Any,
    invocation: str,
    logs: Path,
    environment: dict[str, str],
    timeout: float,
    grace: float,
    *,
    observer: Any = None,
    metadata: Any = None,
    rendered_input: bytes | None = None,
    empty_directory: Path | None = None,
) -> Any:
    """No science files enter the empty CWD; stdout is transport, final is payload."""
    packet = strict_object(packet_raw.decode("utf-8"))
    require(packet_raw == json_bytes(packet), "Canonical disclosed packet required")
    if not packet["case"].startswith("SYNTHETIC-"):
        runtime.authenticate_configuration(configuration)
    logs.mkdir(parents=True, exist_ok=False)
    empty = empty_directory if empty_directory is not None else logs / "empty-cwd"
    if configuration.get("bounded_response") or configuration.get("transport_receipt"):
        require(
            not empty.resolve().is_relative_to(Path(__file__).resolve().parents[3]),
            "Bounded semantic CWD must be outside the repository checkout",
        )
    empty.mkdir()
    schema_path, response_path = (
        logs / "response-schema.json",
        logs / "final-response.txt",
    )
    put_binary(schema_path, json_bytes(response_schema.native(schema)))
    prompt = render_disclosure(configuration, packet_raw, instruction_raw, invocation)
    if rendered_input is not None:
        require(
            configuration.get("evidence_locator") is None,
            "Direct bounded disclosure cannot use legacy packet projection",
        )
        rendered_input.decode("utf-8", errors="strict")
        require(
            instruction_raw and instruction_raw in rendered_input,
            "Frozen instructions absent from disclosure",
        )
        prompt = rendered_input
    if configuration.get("bounded_response"):
        require(
            response_schema.envelope(schema).utf8_bytes
            <= response_schema.MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
            "Semantic response contract exceeds method envelope",
        )
    common = {
        "semantic": True,
        "fresh": True,
        "model": configuration["model"],
        "reasoning": configuration["reasoning"],
        "instruction_sha256": digest(instruction_raw),
        "packet_sha256": digest(packet_raw),
        **(metadata or {}),
    }
    last_process: dict[str, Any] = {}
    result, response, validated, failure = None, None, False, None

    def observe(event: Any) -> None:
        last_process.update(event)
        notify_operational(observer, event)

    try:
        if configuration.get("bounded_response"):
            budget_result = preflight_input(
                configuration,
                prompt,
                schema,
                engineering=packet["case"].startswith("SYNTHETIC-"),
            )
            put_binary(logs / "semantic-budget.json", json_bytes(budget_result))
        command = codex.argv(
            configuration,
            empty,
            schema=schema_path,
            response=response_path,
        )
        put_binary(
            logs / "configuration-preflight.json",
            json_bytes(
                {
                    **runtime.preflight(command),
                    "argv": command,
                    "configuration": configuration,
                },
            ),
        )
        result = await invoke(
            command,
            empty,
            environment,
            timeout,
            grace,
            logs / "process",
            observer=observe,
            metadata=common,
            stdin_bytes=prompt,
        )
        require(
            not result.failed
            and not result.stdout_truncated
            and not result.stderr_truncated,
            "Semantic process failed/timed out/truncated; no retry",
        )
        turn = parse_codex_turn_output(result.stdout)
        events = [
            strict_object(line)
            for line in result.stdout.decode().splitlines()
            if line.strip()
        ]
        require(
            sum(e.get("type") == "thread.started" for e in events) == 1
            and sum(e.get("type") == "turn.completed" for e in events) == 1,
            "Ambiguous semantic transport",
        )
        items = [
            e.get("item", {}) for e in events if e.get("type", "").startswith("item.")
        ]
        require(
            all(i.get("type") in {"agent_message", "reasoning", "error"} for i in items)
            and b"tools::router" not in result.stderr,
            "Semantic tool attempt; response rejected",
        )
        require(
            sum(i.get("type") == "agent_message" for i in items) == 1,
            "Ambiguous semantic assistant response",
        )
        require(
            response_path.is_file(),
            "Semantic final payload missing despite process success",
        )
        final = binary(response_path).decode("utf-8")
        require(
            final.rstrip("\r\n") == turn.final_message.rstrip("\r\n"),
            "Final response differs from completed transport message",
        )
        payload = strict_object(final)
        validate_schema(payload, schema)
        response = response_schema.canonical(payload)
        if configuration.get("bounded_response"):
            require(
                len(response) <= response_schema.MAX_SEMANTIC_RESPONSE_UTF8_BYTES,
                "EVIDENCE_REPRESENTATION_LIMIT: semantic response exceeds "
                "method envelope",
            )
        if configuration.get("evidence_locator") == evidence.CONTRACT:
            evidence.judgments(payload, packet)
        require(not any(empty.iterdir()), "Semantic CWD mutation; response rejected")
        validated = True
        provenance = {
            "status": "PASS",
            "invocation": invocation,
            "case": packet["case"],
            "frame": packet["frame"],
            "model": configuration["model"],
            "reasoning": configuration["reasoning"],
            "thread_id": turn.thread_id,
            "instruction_sha256": digest(instruction_raw),
            "packet_sha256": digest(packet_raw),
            "input_sha256": digest(prompt),
            "input_characters": len(prompt.decode()),
            "input_bytes": len(prompt),
            "canonical_response_characters": len(response.decode()),
            "canonical_response_bytes": len(response),
            "response_schema_sha256": digest(json_bytes(schema)),
            "response_sha256": digest(binary(response_path)),
            "process_exit": result.exit_code,
            "transport": "PASS",
            "payload": "PRESENT",
            "schema_validation": "PASS",
            "evidence_projection": "PASS"
            if configuration.get("evidence_locator") == evidence.CONTRACT
            else "NOT_APPLICABLE",
            "scientific_artifact_authentication": "HOST_BUILDER_REQUIRED",
            "tool_calls": 0,
            "scientific_filesystem_dependency": False,
            "host_routing_independently_verified": False,
            "usage": next(
                e.get("usage", {}) for e in events if e.get("type") == "turn.completed"
            ),
        }
        put_binary(logs / "receipt.json", json_bytes(provenance))
        return {"payload": payload, "provenance": provenance}
    except Exception as error:
        failure = type(error).__name__ + ": " + str(error)
        notify_operational(
            observer,
            {
                **last_process,
                **common,
                "status": "FAILED",
                "failure_category": "SEMANTIC_RESPONSE_INVALID",
                "error": str(error),
                "stdout_path": str(logs / "process/stdout.log"),
                "stderr_path": str(logs / "process/stderr.log"),
                "workspace": str(empty),
            },
        )
        raise
    finally:
        put_binary(
            logs / "invocation-measurement.json",
            json_bytes(
                measurement.capture(
                    configuration,
                    packet["case"],
                    invocation,
                    prompt,
                    result,
                    response,
                    validated=validated,
                    failure=failure,
                    raw_stdout=binary(logs / "process/stdout.log")
                    if (logs / "process/stdout.log").is_file()
                    else None,
                ),
            ),
        )
