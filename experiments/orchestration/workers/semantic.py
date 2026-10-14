# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0913, PLR0917, ASYNC109, ASYNC240, TRY300 -- bounded external-Agent semantic transport
"""Deliver host-owned disclosure and authenticate one tool-free JSON response."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration.observation import notify_operational
from experiments.orchestration.storage import binary, require
from experiments.orchestration.workers import codex, evidence, runtime
from experiments.orchestration.workers.process import invoke

if TYPE_CHECKING:
    from pathlib import Path


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
    require(
        set(schema)
        <= {"type", "properties", "required", "additionalProperties", "items", "enum"},
        "Unsupported semantic response schema",
    )
    kind = schema["type"]
    types = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
    }
    require(
        kind in types and type(value) is types[kind],
        "Semantic response schema type",
    )
    if "enum" in schema:
        require(value in schema["enum"], "Semantic response schema enum")
    if kind == "object":
        require(
            schema["additionalProperties"] is False
            and set(value) == set(schema["required"]) == set(schema["properties"]),
            "Semantic response object fields",
        )
        for name, child in schema["properties"].items():
            validate_schema(value[name], child)
    elif kind == "array":
        for item in value:
            validate_schema(item, schema["items"])


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
) -> Any:
    """No science files enter the empty CWD; stdout is transport, final is payload."""
    packet = strict_object(packet_raw.decode("utf-8"))
    require(packet_raw == json_bytes(packet), "Canonical disclosed packet required")
    if not packet["case"].startswith("SYNTHETIC-"):
        runtime.authenticate_configuration(configuration)
    logs.mkdir(parents=True, exist_ok=False)
    empty = logs / "empty-cwd"
    empty.mkdir()
    schema_path, response_path = (
        logs / "response-schema.json",
        logs / "final-response.txt",
    )
    put_binary(schema_path, json_bytes(schema))
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
    prompt = (
        "All authorized information is supplied below. Do not use shell or tools; "
        "do not inspect the filesystem or web; create no files. Return ONLY one "
        "JSON object matching the supplied response schema, containing your judgments. "
        "The HOST owns packet authentication, identifiers/attestation, serialization "
        "and builder execution. Never guess unseen content.\n"
        + json_bytes(disclosure).decode()
    ).encode()
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

    def observe(event: Any) -> None:
        last_process.update(event)
        notify_operational(observer, event)

    try:
        result = await invoke(
            codex.argv(
                configuration,
                empty,
                schema=schema_path,
                response=response_path,
            ),
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
        if configuration.get("evidence_locator") == evidence.CONTRACT:
            evidence.judgments(payload, packet)
        require(not any(empty.iterdir()), "Semantic CWD mutation; response rejected")
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
