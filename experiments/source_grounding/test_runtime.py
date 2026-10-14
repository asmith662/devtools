# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, ASYNC240, FBT001, PLR2004 -- synthetic host-disclosure integration
"""Both actual semantic callers with fake responses; no real cohort treatment."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from experiments.orchestration.controller import Controller
from experiments.orchestration.isolation import PRIMARY, sterile
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load, materialize
from experiments.orchestration.tests.test_controller import fixture
from experiments.orchestration.workers import evidence, runtime, semantic
from experiments.source_grounding import reviewer, workers


def synthetic_packet(*, gold: bool) -> Any:
    rows = []
    for address, content in [
        ("synthetic/valve.txt", "The fictional valve opens at seven ticks."),
        ("synthetic/panel.txt", "The fictional panel is blue."),
        ("synthetic/bell.txt", "The fictional bell has a round shell."),
    ]:
        cid = reviewer.semantic("decoded-utf8-text-sha256-v1", content)
        rows.append(
            {
                "address": address,
                "content": content,
                "content_identity": cid,
                "document_identity": reviewer.semantic(
                    "whole-resource-exact-text-v1",
                    "SYNTHETIC-REPOSITORY",
                    address,
                    cid,
                ),
            },
        )
    rows.sort(key=lambda r: r["address"])
    pairs = tuple(v for row in rows for v in (row["address"], row["content_identity"]))
    frame = {
        "repository_id": "SYNTHETIC-REPOSITORY",
        "snapshot_id": reviewer.semantic(
            "explicit-required-text-resources-sha256-v1",
            "SYNTHETIC-REPOSITORY",
            *pairs,
        ),
        "corpus_id": reviewer.semantic(
            "selected-observed-utf8-resource-occurrences-sha256-v1",
            "SYNTHETIC-REPOSITORY",
            *pairs,
        ),
        "parent_tree": "a" * 40,
    }
    obligation = {
        "id": "O1",
        "requirement": "Report the fictional valve opening threshold.",
        "satisfaction": "Identify the exact tick threshold stated in the "
        "synthetic instrument resource.",
        "exclusions": "No real repository, model or historical task information.",
        "gap": "NONE: all synthetic information is disclosed.",
    }
    common = {
        "schema": "blind-semantic-gold-packet-v1"
        if gold
        else "source-grounding-packet-v1",
        "case": "SYNTHETIC-GOLD" if gold else "SYNTHETIC-GROUNDING",
        "task": "NON-SCIENTIFIC SYNTHETIC ENGINEERING: report the fictional "
        "valve opening threshold.",
        "frame": frame,
    }
    return {
        **common,
        **(
            {"obligations": [obligation], "resources": rows}
            if gold
            else {"cells": [{"obligation": obligation, "source": r} for r in rows]}
        ),
    }


def synthetic_judgments(packet: Any) -> Any:
    gold = "resources" in packet
    rows = packet["resources"] if gold else [c["source"] for c in packet["cells"]]
    valve = next(r for r in rows if r["address"] == "synthetic/valve.txt")

    table = evidence.sources(packet)

    span = {
        "source_key": evidence.source_key(valve, table),
        "occurrence": 1,
        "quote": valve["content"],
    }
    cells = []
    for row in rows:
        positive = row["address"] == valve["address"]
        cell: dict[str, Any] = {
            "obligation": "O1",
            "source_key": evidence.source_key(row, table),
            "spans": [span] if positive else [],
            "reason": "Synthetic timing evidence."
            if positive
            else "Synthetic unrelated material.",
        }
        extra: dict[str, Any] = (
            {"label": "REQUIRED" if positive else "UNNECESSARY"}
            if gold
            else {
                "verdict": "GROUNDED_SOURCE" if positive else "NOT_GROUNDED_SOURCE",
                "statement": "Valve opens at seven ticks." if positive else "",
                "assumptions": [],
                "uncertainty": "",
                "additional_information": "None.",
            }
        )
        cell.update(extra)
        cells.append(cell)
    return {
        "cells": cells,
        "units": [
            {
                "id": "U1",
                "obligation": "O1",
                "statement": "Valve opening threshold is seven ticks.",
                "basis": "REPOSITORY_SUPPORTED",
                "necessity": "Synthetic task asks for this threshold.",
                "alternatives": [[span]],
            },
        ]
        if gold
        else [],
        "gaps": {
            "TASK_INTERPRETATION_GAP": "NONE",
            "TASK_GAP": "NONE",
            "REPOSITORY_INFORMATION_GAP": "NONE",
            "unconditional_sufficiency": True,
            "qualification": "Synthetic engineering only.",
        }
        if gold
        else [],
        "self_review": "Audited all three synthetic cells and exact own-source spans.",
    }


def test_luna_designation_cannot_override_scientific_validator() -> None:
    packet = synthetic_packet(gold=True)
    packet["case"] = "FAKE-ENGINEERING-NON-SYNTHETIC-PREFIX"
    config = workers.configuration("Luna", reasoning="Medium", gold=True)
    review = semantic.review(synthetic_judgments(packet), packet, config)
    with pytest.raises(ValueError, match="restricted to synthetic Luna"):
        reviewer.validate(review, packet, ("GPT-6 Luna", "Medium"))


async def direct_path(root: Path, packet: Any, instructions: bytes, config: Any) -> Any:
    c = await fixture(
        root / "fixture-repository",
        root / "fixture-work",
        approved=False,
    )
    value = c.value
    value["semantic"] = {
        **config,
        "builder_argv": [
            *config["builder_argv"],
            "--model",
            config["model"],
            "--reasoning",
            config["reasoning"],
        ],
    }
    controller = Controller(c.repository, RunPlan.parse(value), c.work_root)
    host = root / "host-packet"
    files = workers.packet_files(
        packet,
        instructions,
        Path(reviewer.__file__).read_bytes(),
    )
    sterile(host, files)
    auth = root / "auth"
    materialize(auth, {"auth.json": Path(workers.AUTH_FILE).read_bytes()})
    env = {k: os.environ[k] for k in runtime.ENVIRONMENT if k in os.environ}
    env["CODEX_HOME"] = str(auth)
    result = await controller.semantic_primary(host, packet["case"], env)
    await workers.authenticate_primary(
        host,
        packet["case"],
        packet["frame"],
        root / "authentication",
        config,
    )
    return {"result": result, "host": host, "controller": controller}


@pytest.mark.parametrize("gold", [False, True])
def test_both_actual_callers_host_create_and_authenticate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    gold: bool,
) -> None:
    packet = synthetic_packet(gold=gold)
    config = workers.configuration("Luna", reasoning="Medium", gold=gold)
    instructions = b"NON-SCIENTIFIC SYNTHETIC: judgments only, no tools or files."

    async def fake(
        argv: Any,
        cwd: Path,
        _env: Any,
        _timeout: Any,
        _grace: Any,
        _logs: Any,
        **_kwargs: Any,
    ) -> Any:
        assert not any(cwd.iterdir())
        assert not (cwd / "packet.json").exists()
        text = json.dumps(synthetic_judgments(packet))
        Path(argv[argv.index("--output-last-message") + 1]).write_text(text + "\n")
        events = [
            {"type": "thread.started", "thread_id": "fresh-integration"},
            {"type": "item.completed", "item": {"type": "agent_message", "text": text}},
            {"type": "turn.completed", "usage": {}},
        ]
        return SimpleNamespace(
            failed=False,
            exit_code=0,
            stdout_truncated=False,
            stderr_truncated=False,
            stdout=b"\n".join(json.dumps(e).encode() for e in events),
            stderr=b"",
        )

    monkeypatch.setattr(semantic, "invoke", fake)

    async def run() -> None:
        if gold:
            response = await direct_path(tmp_path, packet, instructions, config)
            host = response["host"]
        else:
            await workers.ground(
                tmp_path / "host-packet",
                packet,
                instructions,
                Path(reviewer.__file__).read_bytes(),
                config,
            )
            host = tmp_path / "host-packet"
        assert all((host / name).is_file() for name in PRIMARY)
        result = load(host / "stage_c_review.json")
        assert result["attestation"]["model"] == "GPT-6 Luna"
        assert result["attestation"]["reasoning"] == "Medium"
        assert reviewer.validate(result, packet, ("GPT-6 Luna", "Medium"))["cells"] == 3

    asyncio.run(run())
