# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, PLR2004 -- fictional end-to-end host lifecycle
"""No model calls: exact C-v2 replay, dynamic capacity and whole-stage spend."""

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
from experiments.orchestration.storage import materialize
from experiments.orchestration.workers import capacity, evidence, measurement, schema
from experiments.source_grounding import reviewer
from experiments.source_grounding.chunked import (
    archive,
    classification,
    disclosure,
    execution,
    packing,
    response,
)
from experiments.source_grounding.chunked.test_consolidation import fixture


def event(value: Any) -> bytes:
    return (json.dumps(value) + "\n").encode()


def setup(root: Path, *, all_useful: bool = False) -> tuple[Any, Any]:
    packet, _, global_response = fixture()
    if all_useful:
        content = packet["resources"][0]["content"]
        cid = reviewer.semantic("decoded-utf8-text-sha256-v1", content)
        packet["resources"] = [
            {
                "address": f"synthetic/r{i:04d}.txt",
                "content": content,
                "content_identity": cid,
                "document_identity": reviewer.semantic(
                    "whole-resource-exact-text-v1",
                    packet["frame"]["repository_id"],
                    f"synthetic/r{i:04d}.txt",
                    cid,
                ),
            }
            for i in range(50)
        ]
        pairs = tuple(
            v
            for row in packet["resources"]
            for v in (row["address"], row["content_identity"])
        )
        for field, semantic in (
            ("snapshot_id", "explicit-required-text-resources-sha256-v1"),
            ("corpus_id", "selected-observed-utf8-resource-occurrences-sha256-v1"),
        ):
            packet["frame"][field] = reviewer.semantic(
                semantic,
                packet["frame"]["repository_id"],
                *pairs,
            )
    part = packing.partition(packet)
    host = {
        "a1_partition": part,
        "a1_calls": len(part["batches"]),
        "semantic": execution.configuration(),
        "invocation_prefix": "SYNTHETIC-NO-MODEL/C2",
    }
    materialize(
        root,
        execution.packet_files(packet, Path(reviewer.__file__).read_bytes(), host),
    )
    return packet, global_response


def responder(
    packet: Any,
    global_response: Any,
    calls: list[str],
    *,
    all_useful: bool = False,
) -> Any:
    table = evidence.sources(packet)
    positive = {
        k
        for k, r in table.items()
        if all_useful or r["address"] == "synthetic/valve.txt"
    }

    async def invoke(
        stage: str,
        index: int,
        raw: bytes,
        contract: Any,
        invocation: str,
    ) -> Any:
        calls.append(stage)
        payload: Any
        if stage == "A1":
            payload = {
                "resources": [
                    {
                        "source_key": k,
                        "judgments": [
                            {
                                "obligation_id": "O1",
                                "state": "USEFUL" if k in positive else "NO_USEFUL",
                            },
                        ],
                    }
                    for k in table
                ],
            }
        elif stage == "A2":
            payload = {
                "cells": [
                    {
                        "source_key": k,
                        "obligation_id": "O1",
                        "resolution_state": "EVIDENCE_FOUND",
                        "semantic_statement": (
                            "The fictional valve opens at seven ticks."
                        ),
                        "locators": [
                            {
                                "source_key": k,
                                "quote": table[k]["content"],
                                "occurrence": 1,
                            },
                        ],
                        "uncertainty_note": "",
                        "representation_complete": True,
                    }
                    for k in positive
                ],
                "self_review": "Checked synthetic evidence.",
                "representation_complete": True,
            }
        else:
            payload = global_response
        schema.validate(payload, contract)
        stdout = (
            event({"type": "thread.started", "thread_id": f"SYNTHETIC/{stage}/{index}"})
            + event(
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": json.dumps(payload)},
                },
            )
            + json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 10,
                        "cached_input_tokens": 0,
                        "cache_write_input_tokens": 0,
                        "output_tokens": 5,
                        "reasoning_output_tokens": 2,
                    },
                },
            ).encode()
        )
        measured = measurement.capture(
            execution.configuration(),
            packet["case"],
            invocation,
            raw,
            SimpleNamespace(stdout=stdout, duration=Duration.seconds(1)),
            schema.canonical(payload),
            validated=True,
            failure=None,
        )
        return {
            "payload": payload,
            "provenance": {"thread_id": f"SYNTHETIC/{stage}/{index}"},
        }, measured

    return invoke


def test_c2_complete_host_pipeline_and_exact_replay(tmp_path: Path) -> None:
    root = tmp_path / "C2"
    packet, payload = setup(root)
    calls: list[str] = []
    asyncio.run(execution.execute(root, invoke=responder(packet, payload, calls)))
    assert calls == ["A1", "A2", "GLOBAL"]
    assert execution.validate(root)["complete_cells"] == 3
    assert b"C-v2" in (root / "stage_c_method.md").read_bytes()
    (root / "stage_c_review.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="canonical replay"):
        execution.validate(root)


def test_dynamic_b_byte_gate_precedes_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "C2"
    packet, payload = setup(root)
    monkeypatch.setattr(
        disclosure,
        "from_archive",
        lambda *_: disclosure.INSTRUCTION.encode() + "\U0001f600".encode() * 200000,
    )
    calls: list[str] = []
    with pytest.raises(ValueError, match="WORKLOAD_CAPACITY_LIMIT"):
        asyncio.run(execution.execute(root, invoke=responder(packet, payload, calls)))
    assert calls == ["A1", "A2"]
    assert not (root / "c2/GLOBAL/0/ENTERED.json").exists()


def test_all_eligible_partition_excess_launches_no_a2(tmp_path: Path) -> None:
    root = tmp_path / "C2"
    packet, payload = setup(root, all_useful=True)
    calls: list[str] = []
    with pytest.raises(ValueError, match="SEMANTIC_INVOCATION_BUDGET"):
        asyncio.run(
            execution.execute(
                root,
                invoke=responder(packet, payload, calls, all_useful=True),
            ),
        )
    assert calls == ["A1"]
    part = json.loads((root / "c2/a2-partition.json").read_bytes())
    assert len(part["batches"]) == 25
    assert not (root / "c2/A2").exists()


def test_native_capture_replay_rejects_transport_and_disclosure_changes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "C2"
    packet, payload = setup(root)
    calls: list[str] = []
    asyncio.run(execution.execute(root, invoke=responder(packet, payload, calls)))
    captured = json.loads(gzip.decompress((root / execution.EXTRA[0]).read_bytes()))
    coverage = classification.validate(packet, tuple(captured["a1"]))
    exact = archive.assemble(
        packet,
        tuple(captured["a2"]),
        digest(json_bytes(capacity.profile(execution.configuration()))),
        coverage=coverage,
    )
    table = evidence.sources(packet)
    contracts = {
        "A1": classification.contract(list(table), ["O1"]),
        "A2": response.pass_a2(
            1,
            [k for k in table if table[k]["address"] == "synthetic/valve.txt"],
            ["O1"],
            max(len(v["content"]) for v in table.values()),
        ),
        "GLOBAL": response.pass_b(len(coverage.grid), ["O1"]),
    }
    payloads = {
        "A1": captured["a1"][0][-1],
        "A2": captured["a2"][0][-1],
        "GLOBAL": payload,
    }
    files = {n: base64.b64decode(v) for n, v in captured["files"].items()}
    for stage, measured in zip(calls, captured["measurements"], strict=True):
        prefix = stage + "/0/"
        canonical = schema.canonical(payloads[stage])
        native = {
            "status": "PASS",
            "tool_calls": 0,
            "invocation": measured["measurement"]["invocation_id"],
            "input_sha256": measured["measurement"]["disclosure_digest"],
            "response_schema_sha256": digest(json_bytes(contracts[stage])),
        }
        if stage == "GLOBAL":
            raw = disclosure.from_archive(packet, exact)
        else:
            part = captured["a1_partition" if stage == "A1" else "a2_partition"]
            raw = packing.render(
                packet,
                part["batches"][0]["source_keys"],
                table,
                coverage if stage == "A2" else None,
            )
        events = event({"type": "thread.started", "thread_id": f"SYNTHETIC/{stage}/0"})
        events += event(
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": canonical.decode()},
            },
        )
        events += event(
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 5,
                    "reasoning_output_tokens": 2,
                },
            },
        )
        additions = {
            "receipt.json": json_bytes(native),
            "response-schema.json": json_bytes(contracts[stage]),
            "final-response.txt": canonical,
            "invocation-measurement.json": json_bytes(measured),
            "process/stdin.bin": raw,
            "process/stdout.log": events,
            "process/stderr.log": b"",
            "process/exit.json": json_bytes(
                {
                    "exit_code": 0,
                    "stdout_truncated": False,
                    "stderr_truncated": False,
                    "duration_seconds": 1,
                },
            ),
        }
        files.update({prefix + n: v for n, v in additions.items()})
    captured["files"] = {n: base64.b64encode(v).decode() for n, v in files.items()}
    execution.verify_process_captures(packet, captured, coverage, exact)
    address = "GLOBAL/0/process/stdin.bin"
    captured["files"][address] = base64.b64encode(b"unauthorized disclosure").decode()
    with pytest.raises(ValueError, match="disclosure replay"):
        execution.verify_process_captures(packet, captured, coverage, exact)
