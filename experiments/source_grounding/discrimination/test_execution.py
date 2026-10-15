# Copyright (c) 2026
# ruff: noqa: ANN401, S101, E501 -- synthetic host replay, never a model
"""Single-call host assembly and exact immutable publication artifacts."""

import asyncio
import base64
import gzip
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import load, materialize
from experiments.orchestration.workers import accounting, measurement, schema
from experiments.source_grounding.discrimination import execution, gold, sampling
from experiments.source_grounding.discrimination.test_design import fixture, judgments


def test_single_call_host_builder_and_replay(tmp_path: Path) -> None:
    """Exactly one injected synthetic response, tool-free host artifact assembly."""
    design, rows, universe = fixture()
    selected = sampling.design_sample(design, rows, universe)
    root = tmp_path / "primary"
    materialize(
        root,
        execution.packet_files(selected, {"synthetic": "frame"}, "SYNTHETIC-RUN"),
    )
    invoked = []

    async def invoke(raw: bytes, contract: Any, identity: str) -> Any:
        assert contract == selected["response_schema"]
        invoked.append(identity)
        events = b'{"type":"thread.started","thread_id":"synthetic"}\n{"type":"turn.completed","usage":{"input_tokens":10,"cached_input_tokens":0,"cache_write_input_tokens":0,"output_tokens":4,"reasoning_output_tokens":0}}\n'
        payload = judgments(selected["packet"])
        observed = measurement.capture(
            execution.configuration(),
            design["case"],
            identity,
            raw,
            SimpleNamespace(stdout=events, duration=Duration.seconds(1)),
            schema.canonical(payload),
            validated=True,
            failure=None,
        )
        return {
            "payload": payload,
            "provenance": {"thread_id": "synthetic", "status": "PASS", "tool_calls": 0},
        }, observed

    asyncio.run(execution.execute(root, invoke=invoke))
    assert len(invoked) == 1
    assert execution.validate(root)["status"] == "PASS"
    assert (
        load(root / "stage_c_review.json")["judgments"][0]["source_evidence"][0][
            "quote"
        ]
        == "aba"
    )
    with pytest.raises(ValueError, match="cannot be retried"):
        asyncio.run(execution.execute(root, invoke=invoke))
    assert len(invoked) == 1
    (root / "stage_c_statistics.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="replay"):
        execution.validate(root)


def test_native_capture_authentication(tmp_path: Path) -> None:
    """Fictional raw exec bytes authenticate usage/final message without a model."""
    design, rows, universe = fixture()
    design["case"] = "FICTIONAL-ONLY"
    selected = sampling.design_sample(design, rows, universe)
    root = tmp_path / "native"
    materialize(
        root,
        execution.packet_files(selected, {"synthetic": "frame"}, "FICTIONAL-RUN"),
    )
    payload = judgments(selected["packet"])
    receipt: dict[str, Any] = {
        "thread_id": "synthetic",
        "status": "PASS",
        "tool_calls": 0,
    }
    rendered = gold.render(selected["packet"])
    receipt.update(
        case=design["case"],
        frame={"synthetic": "frame"},
        invocation="FICTIONAL-RUN/FICTIONAL-ONLY/C",
        model="GPT-6 Astra",
        reasoning="High",
        instruction_sha256=digest(gold.INSTRUCTION.encode()),
        packet_sha256=digest(
            json_bytes({"case": design["case"], "frame": {"synthetic": "frame"}}),
        ),
        input_sha256=digest(rendered),
        input_characters=len(rendered.decode()),
        input_bytes=len(rendered),
        response_schema_sha256=digest(
            json_bytes(selected["response_schema"]),
        ),
        response_sha256=digest(schema.canonical(payload)),
        process_exit=0,
        transport="PASS",
        schema_validation="PASS",
    )
    # Native exec is JSONL: each event occupies one line.
    stdout = b"\n".join(
        json.dumps(v).encode()
        for v in [
            {"type": "thread.started", "thread_id": "synthetic"},
            {
                "type": "item.completed",
                "item": {
                    "id": "message",
                    "type": "agent_message",
                    "text": schema.canonical(payload).decode(),
                },
            },
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 4,
                    "reasoning_output_tokens": 0,
                },
            },
        ]
    )
    observed = measurement.capture(
        execution.configuration(),
        design["case"],
        "FICTIONAL-RUN/FICTIONAL-ONLY/C",
        gold.render(selected["packet"]),
        SimpleNamespace(stdout=stdout, duration=Duration.seconds(1)),
        schema.canonical(payload),
        validated=True,
        failure=None,
    )
    counted = accounting.accept(observed, "CANDIDATE_DISCRIMINATION_GOLD_VALID")
    files = {
        "receipt.json": json_bytes(receipt),
        "response-schema.json": json_bytes(schema.native(selected["response_schema"])),
        "final-response.txt": schema.canonical(payload),
        "invocation-measurement.json": json_bytes(observed),
        "process/stdin.bin": gold.render(selected["packet"]),
        "process/stdout.log": stdout,
        "process/stderr.log": b"",
        "process/exit.json": json_bytes(
            {
                "duration_seconds": 1,
                "exit_code": 0,
                "stdout_truncated": False,
                "stderr_truncated": False,
            },
        ),
    }
    captured = {
        "schema": "candidate-discrimination-capture-v1",
        "payload": payload,
        "receipt": receipt,
        "measurement": counted,
        "files": {k: base64.b64encode(v).decode() for k, v in files.items()},
        "input_sha256": selected["input"]["sha256"],
        "selection_sha256": selected["sha256"],
    }
    (root / execution.EXTRA[0]).write_bytes(
        gzip.compress(json_bytes(captured), mtime=0),
    )
    (root / execution.EXTRA[1]).write_bytes(json_bytes(counted))
    execution.build(root)
    assert execution.validate(root)["status"] == "PASS"
    captured["files"]["final-response.txt"] = base64.b64encode(b"{}").decode()
    (root / execution.EXTRA[0]).write_bytes(
        gzip.compress(json_bytes(captured), mtime=0),
    )
    with pytest.raises(ValueError, match="provenance"):
        execution.validate(root)
