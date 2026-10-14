# Copyright (c) 2026
# ruff: noqa: ANN401, C901, PLR0911, PLR0912, PLR0915, ASYNC109, EM101, TRY003, T201, PLC0415, ASYNC240 -- narrow experiment/controller transport
"""Real stage adapters; scientific inputs come only from assigned workspaces."""

from __future__ import annotations

import argparse
import asyncio
import base64
import gzip
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from devtools.core.time import Timestamp
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration.isolation import (
    PRIMARY,
    preserve_packet,
    semantic_outputs,
    sterile,
)
from experiments.orchestration.observation import PROCESS_FIELDS, process_metadata
from experiments.orchestration.storage import bundle, load, materialize, require, safe
from experiments.orchestration.workers import codex
from experiments.orchestration.workers.process import invoke
from experiments.source_grounding import contracts, packets, reviewer

ENVIRONMENT = (
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "TEMP",
    "TMP",
    "USERPROFILE",
    "APPDATA",
    "LOCALAPPDATA",
    "COMSPEC",
)
AUTH_FILE = "C:/Users/recoveryadmin/.codex/auth.json"


def configuration(model: str) -> Any:
    """Freeze explicit requested model identity, never infer it from results."""
    return {
        "kind": "codex",
        "model": "GPT-6 " + model,
        "model_id": "gpt-6-" + model.lower(),
        "reasoning": "High",
        "cli_version": "0.162.1",
        "prompt_file": "INSTRUCTIONS.md",
        "auth_file": AUTH_FILE,
        "environment_allowlist": list(ENVIRONMENT),
    }


def write_files(root: Path, files: Any) -> None:
    """Never overwrite any previously produced scientific file."""
    require(
        not any(safe(root, n).exists() for n in files),
        "Scientific overwrite refused",
    )
    for name, raw in files.items():
        put_binary(safe(root, name), raw)


def candidate(root: Path, case: str, frame: Any, stage: str, files: Any) -> None:
    """Explicit ownership; no operational discovery used for publication."""
    write_files(
        root,
        {
            "candidate.json": json_bytes(
                {
                    "schema": "experiment-candidate-v1",
                    "case": case,
                    "frame": frame,
                    "stage": stage,
                    "files": {n: digest(raw) for n, raw in files.items()},
                },
            ),
        },
    )


def packet_files(payload: Any, instructions: bytes, builder: bytes) -> Any:
    """Construct a flat sterile packet without any treatment metadata."""
    builder = packets.builder(
        builder,
        gold=payload["schema"] == "blind-semantic-gold-packet-v1",
    )
    files = {
        "packet.json": json_bytes(payload),
        "INSTRUCTIONS.md": instructions,
        "stage_c_builder.py": builder,
    }
    files["packet_integrity.json"] = json_bytes(
        {
            "schema": "blind-primary-packet-integrity-v1",
            "files": {n: digest(raw) for n, raw in files.items()},
        },
    )
    return files


def gold_packet(design: Any, rows: Any) -> Any:
    """Build independent gold from parent-only inputs, never B."""
    return {
        "schema": "blind-semantic-gold-packet-v1",
        "case": design["case"],
        "task": design["task_text"],
        "frame": design["frame"],
        "obligations": [
            {k: o[k] for k in contracts.BLIND_OBLIGATION} for o in design["obligations"]
        ],
        "resources": [{k: r[k] for k in reviewer.SOURCE} for r in rows],
    }


async def command(  # noqa: PLR0913 -- invocation plus operational observer metadata
    argv: list[str],
    root: Path,
    logs: Path,
    timeout: int = 3600,
    env: Any = None,
    *,
    observer: Any = None,
    metadata: Any = None,
) -> Any:
    """Use the controller's owned process-tree lifecycle; never retry."""
    result = await invoke(
        argv,
        root,
        {k: os.environ[k] for k in ENVIRONMENT if k in os.environ}
        if env is None
        else env,
        timeout,
        10,
        logs,
        observer=observer,
        metadata=metadata,
    )
    require(
        not result.failed
        and not result.stdout_truncated
        and not result.stderr_truncated,
        "Worker/validator failed or truncated; attempt dead",
    )
    return result


async def authenticate_primary(root: Path, case: str, frame: Any, logs: Path) -> Any:
    """Authenticate seven original artifacts with separate-process exact replay."""
    p = reviewer.packet(root)
    require(p["case"] == case and p["frame"] == frame, "Primary foreign case/frame")
    review = load(root / "stage_c_review.json")
    statistics = reviewer.validate(review, p)
    outputs = reviewer.products(root)
    require(
        all((root / n).read_bytes() == raw for n, raw in outputs.items()),
        "Primary exact deterministic outputs",
    )
    await command(
        [
            sys.executable,
            "-B",
            str(root / "stage_c_builder.py"),
            "verify",
            "--root",
            str(root),
        ],
        root,
        logs,
    )
    files = {n: (root / n).read_bytes() for n in PRIMARY}
    semantic_outputs(files)
    return {
        "status": "PASS",
        **{k: v for k, v in review["attestation"].items() if k != "blindness"},
        "blindness": dict.fromkeys(reviewer.BLINDNESS, False),
        "complete_cells": statistics["cells"],
    }


def grounding_observer(root: Path) -> Any:
    """Append operational identity outside sterile packet and scientific outputs."""

    def observe(event: Any) -> None:
        fields = {k: event[k] for k in PROCESS_FIELDS if k in event}
        fields.setdefault("timestamp", str(Timestamp.now()))
        fields["operation"] = "source-grounding-worker"
        fields["process_role"] = "source grounding"
        with (root.parent / "operational.log").open("ab") as stream:
            stream.write((json.dumps(fields, sort_keys=True) + "\n").encode())
            stream.flush()

    return observe


async def ground(
    root: Path,
    payload: Any,
    instructions: bytes,
    builder: bytes,
    config: Any,
) -> Any:
    """One fresh isolated Sol invocation inside its existing controller B slot."""
    files = packet_files(payload, instructions, builder)
    sterile(root, files)
    reviewer.packet(root)
    require(config == configuration("Sol"), "Frozen source-grounding configuration")
    operational = root.parent / "grounding-operation"
    version = await command(
        [shutil.which("codex.cmd") or "codex", "--version"],
        root,
        operational / "version",
    )
    require(
        version.stdout.decode().strip() == "codex-cli 0.162.1",
        "Grounding CLI version",
    )
    # The enclosing immutable native journal claims grounding before this function.
    # No retry or workspace reuse is permitted after that claim, even prelaunch.
    auth = root.parent / "grounding-auth"
    materialize(auth, {"auth.json": Path(AUTH_FILE).read_bytes()})
    env = {k: os.environ[k] for k in ENVIRONMENT if k in os.environ}
    env["CODEX_HOME"] = str(auth)
    start = time.perf_counter_ns()
    result = await command(
        codex.argv(config, root),
        root,
        operational / "worker",
        7200,
        env,
        observer=grounding_observer(root),
        metadata={**process_metadata(config, root), "process_role": "source grounding"},
    )
    elapsed = time.perf_counter_ns() - start
    turn = parse_codex_turn_output(result.stdout)
    preserve_packet(root, files)
    await authenticate_primary(
        root,
        payload["case"],
        payload["frame"],
        operational / "validation",
    )
    review = load(root / "stage_c_review.json")
    usage = []
    for line in result.stdout.decode().splitlines():
        event = json.loads(line)
        if event.get("type") == "turn.completed":
            usage.append(event.get("usage"))
    tokens = {
        key: sum(u[key] for u in usage)
        if usage and all(isinstance(u, dict) and type(u.get(key)) is int for u in usage)
        else None
        for key in ("input_tokens", "output_tokens", "cached_input_tokens")
    }
    return {
        "review": review,
        "files_b64": {
            n: base64.b64encode((root / n).read_bytes()).decode("ascii")
            for n in PRIMARY
        },
        "costs": {
            "grounding_wall_ns": elapsed,
            "grounding_packet_bytes": sum(len(raw) for raw in files.values()),
            "source_grounding_packet_bytes": len(files["packet.json"]),
            "model_usage": usage,
            "model_tokens": tokens,
            "usage_availability": "CLI_REPORTED" if any(usage) else "NOT_AVAILABLE",
            "grounding_thread_id": turn.thread_id,
        },
    }


def prepared(root: Path, case: str, frame: Any) -> tuple[Any, Any]:
    """Authenticate serialized parent frame without lexical or RI acquisition."""
    from experiments.source_grounding.freeze import frame_contract

    design = load(root / "design.json")
    metadata = load(root / "frame.json")
    rows = json.loads(gzip.decompress((root / "resources.json.gz").read_bytes()))
    require(
        design["case"] == case
        and design["frame"]
        == frame
        == frame_contract(design["population"], metadata, rows),
        "Preparation case/frame",
    )
    require(
        design["parent_frame"]
        == {k: v for k, v in metadata.items() if k != "resources"},
        "Preparation metadata",
    )
    return design, rows


def run_stage(args: Any) -> Any:
    """Execute fixed controller stages without general policy decisions."""
    root, case, frame, stage = (
        args.workspace,
        args.case,
        json.loads(args.frame),
        args.stage,
    )
    logs = root.parent / (stage + "-adapter-logs")
    if stage in {"prepare", "prepare_validate"}:
        design, rows = prepared(root, case, frame)
        if stage == "prepare":
            files = {
                n: (root / n).read_bytes()
                for n in (
                    "design.json",
                    "frame.json",
                    "resources.json.gz",
                    "INSTRUCTIONS_GROUNDING.md",
                    "INSTRUCTIONS_GOLD.md",
                    "reviewer_codec.py",
                    "implementation.json",
                    "worker_configuration.json",
                )
            }
            candidate(root, case, frame, "prepare", files)
        return {"status": "PASS"}
    if stage == "packet":
        design, rows = prepared(root, case, frame)
        files = packet_files(
            gold_packet(design, rows),
            (root / "INSTRUCTIONS_GOLD.md").read_bytes(),
            (root / "reviewer_codec.py").read_bytes(),
        )
        write_files(root, files)
        candidate(root, case, frame, stage, files)
        return {"status": "PASS"}
    if stage == "packet_validate":
        p = reviewer.packet(root)
        require(p["case"] == case and p["frame"] == frame, "Packet case/frame")
        return {"status": "PASS"}
    if stage == "B":
        from experiments.source_grounding.capture import execute

        design, rows = prepared(root, case, frame)
        execute(
            root,
            design,
            rows,
            lambda payload: ground(
                root / "grounding-worker",
                payload,
                (root / "INSTRUCTIONS_GROUNDING.md").read_bytes(),
                (root / "reviewer_codec.py").read_bytes(),
                load(root / "worker_configuration.json")["workers"]["grounding"],
            ),
            implementation=load(root / "implementation.json")["implementation"],
            run_binding={
                "run_id": args.run_id,
                "stage_a_checkpoint": args.stage_a,
                "packet_checkpoint": args.packet_commit,
            },
        )
        integrity = load(root / "integrity.json")
        files = bundle(root, integrity["sha256"])
        files["integrity.json"] = (root / "integrity.json").read_bytes()
        candidate(root, case, frame, stage, files)
        return {"status": "PASS"}
    if stage == "B_validate":
        from experiments.source_grounding.capture import sealed

        rows = json.loads(gzip.decompress((root / "resources.json.gz").read_bytes()))
        data = load(root / "analysis_input.json")
        require(data["case"] == case and data["frame"] == frame, "B case/frame")
        return sealed(root, rows)
    if stage == "C_validate":
        return asyncio.run(authenticate_primary(root, case, frame, logs))
    if stage in {"import", "import_validate"}:
        # Reconstruct a transient verifier view; original primary bytes never change.
        view = root / "verification-view"
        files = {
            **{p.name: p.read_bytes() for p in (root / "packet").iterdir()},
            **{p.name: p.read_bytes() for p in (root / "primary").iterdir()},
        }
        if not view.exists():
            materialize(view, files)
        require(
            all((view / n).read_bytes() == raw for n, raw in files.items()),
            "Import view identity",
        )
        receipt = asyncio.run(authenticate_primary(view, case, frame, logs))
        gold = load(view / "stage_c_review.json")
        if stage == "import":
            projection = {
                "case": case,
                "frame": frame,
                "cells": gold["cells"],
                "statistics": load(view / "stage_c_statistics.json"),
                "primary_sha256": {n: digest(files[n]) for n in PRIMARY},
            }
            write_files(
                root,
                {
                    "gold.json": json_bytes(projection),
                    "import_authentication.json": json_bytes(receipt),
                },
            )
            owned = {"primary/" + n: files[n] for n in PRIMARY}
            owned.update(
                {
                    n: (root / n).read_bytes()
                    for n in ("gold.json", "import_authentication.json")
                },
            )
            candidate(root, case, frame, "import", owned)
        else:
            projection = load(root / "gold.json")
            require(
                projection
                == {
                    "case": case,
                    "frame": frame,
                    "cells": gold["cells"],
                    "statistics": load(view / "stage_c_statistics.json"),
                    "primary_sha256": {n: digest(files[n]) for n in PRIMARY},
                },
                "Canonical gold projection",
            )
        return {**receipt, "semantic_transformation": "NONE"}
    if stage in {"D", "D_validate"}:
        from experiments.source_grounding.analysis import analyze, render

        result = analyze(root)
        files = {
            "analysis.json": json_bytes(result),
            "analysis.md": render(result).encode(),
            "TRACE.md": render(result["trace"]).encode(),
            "trace.json": json_bytes(result["trace"]),
            "validation.json": json_bytes(
                {
                    "status": "PASS",
                    "join_defects": result["join_defects"],
                    "actual_rank_modifications": 0,
                },
            ),
        }
        files["integrity.json"] = json_bytes(
            {
                "sha256": {n: digest(raw) for n, raw in files.items()},
                "inputs": [c["input_hashes"] for c in result["cases"]],
            },
        )
        if stage == "D":
            write_files(root, files)
            candidate(root, case, frame, "D", files)
        else:
            require(
                all((root / n).read_bytes() == raw for n, raw in files.items()),
                "Stage D exact deterministic replay",
            )
        return {"status": "PASS"}
    raise ValueError("Unknown stage")


def main() -> None:
    """Run exactly the stage supplied by the approved controller."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--frame", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--stage-a", required=True)
    parser.add_argument("--packet-commit", default="")
    print(json.dumps(run_stage(parser.parse_args())))


if __name__ == "__main__":
    main()
