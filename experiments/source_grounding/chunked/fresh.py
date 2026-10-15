# Copyright (c) 2026
# ruff: noqa: ANN401, ASYNC240 -- fresh treatment uses existing scientific capture
"""Add operational pre-entry/usage gates around unchanged fresh B semantics."""

import asyncio
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration.isolation import PRIMARY, preserve_packet, sterile
from experiments.orchestration.storage import bundle, load, materialize, require
from experiments.orchestration.workers import (
    accounting,
    budget,
    capacity,
    codex,
    output_capacity,
    runtime,
    schema,
    semantic,
)
from experiments.source_grounding import capture, response, workers
from experiments.source_grounding.chunked import execution

RESPONSE_BYTES = 63357


def configuration() -> Any:
    """Preserve Sol/High native judgment schema and locator semantics."""
    original = workers.configuration("Sol")
    original.pop("smoke_receipt", None)
    original["transport_receipt"] = execution.configuration()["capacity_receipt"]
    original["output_receipt"] = execution.configuration()["output_receipt"]
    return original


def run(root: Path, args: Any) -> None:
    """Only the explicitly fresh case may acquire treatment or launch Sol."""
    require(args.case == "0024", "Adopted cases cannot execute fresh B")
    design, rows = workers.prepared(
        root,
        args.case,
        json.loads(args.frame),
    )
    config = load(root / "worker_configuration.json")["workers"]["grounding"]
    require(config == configuration(), "Frozen fresh B configuration")
    invocation = args.run_id + "/0024/B/Sol"
    prepared: dict[str, Any] = {}

    def preflight(payload: Any) -> None:
        files = workers.packet_files(
            payload,
            (root / "INSTRUCTIONS_GROUNDING.md").read_bytes(),
            (root / "reviewer_codec.py").read_bytes(),
        )
        raw = semantic.render_disclosure(
            config,
            files["packet.json"],
            files["INSTRUCTIONS.md"],
            invocation,
        )
        runtime.authenticate_configuration(config)
        certificate = load(execution.ROOT / config["transport_receipt"]["path"])
        # Transport/tool semantics are CLI properties, not Sol quality evidence.
        capacity.check_input(
            certificate,
            {**config, "model_id": "gpt-6-astra", "bounded_response": True},
            raw,
        )
        spec = budget.BudgetSpec(
            runtime_identity=digest(
                json_bytes(capacity.profile(execution.configuration())),
            ),
            model="GPT-6 Sol",
            reasoning="High",
            execution_profile="SEMANTIC_WORKER",
            transport_characters=1048576,
            transport_provenance="EMPIRICALLY_OBSERVED: blocked C-v1 turn/start",
            safety_characters=348576,
            schema_bytes_limit=262144,
            response_bytes_limit=63357,
            unknown_context_allowed=True,
            context_provenance=(
                "EMPIRICAL_TRANSPORT_COMPATIBILITY; MODEL_CONTEXT_UNKNOWN"
            ),
        )
        observed = budget.check(spec, raw, json_bytes(response.schema(gold=False)))
        output_capacity.authenticate(
            load(execution.ROOT / output_capacity.ADDRESS),
            execution.configuration(),
            execution.ROOT,
        )
        prepared.update(
            files=files,
            raw=raw,
            payload_sha256=digest(json_bytes(payload)),
        )
        put_binary(
            root / "grounding-preentry-budget.json",
            json_bytes(
                {
                    "observed": observed.__dict__,
                    "invocation": invocation,
                    "reserved_calls": 1,
                    "case_cap": 28,
                    "schema_semantics": "UNCHANGED",
                    "accepted_response_utf8_limit": 63357,
                    "model_context": "UNKNOWN",
                    "compatibility_assumption": (
                        "CLI transport/tool semantics model-independent; "
                        "semantic quality model-dependent"
                    ),
                },
            ),
        )

    async def ground(payload: Any) -> Any:
        require(
            digest(json_bytes(payload)) == prepared["payload_sha256"],
            "Fresh B disclosure changed after gate",
        )
        folder = root / "grounding-worker"
        sterile(folder, prepared["files"])
        auth = root / "grounding-auth"
        materialize(auth, {"auth.json": Path(workers.AUTH_FILE).read_bytes()})
        env = {k: os.environ[k] for k in runtime.ENVIRONMENT if k in os.environ}
        env["CODEX_HOME"] = str(auth)
        started = time.perf_counter_ns()
        result = await semantic.primary(
            config,
            prepared["files"]["packet.json"],
            prepared["files"]["INSTRUCTIONS.md"],
            config["response_schema"],
            invocation,
            root / "grounding-operation/worker",
            env,
            7200,
            10,
            observer=workers.grounding_observer(folder),
        )
        require(
            len(schema.canonical(result["payload"])) <= RESPONSE_BYTES,
            "OUTPUT_LIMIT: fresh B host response envelope",
        )
        workers.write_files(
            folder,
            {
                "stage_c_review.json": json_bytes(
                    semantic.review(result["payload"], payload, config),
                ),
            },
        )
        await workers.command(
            [
                sys.executable,
                "-B",
                str(folder / "stage_c_builder.py"),
                "build",
                "--root",
                str(folder),
            ],
            folder,
            root / "grounding-operation/builder",
        )
        preserve_packet(folder, prepared["files"])
        await workers.authenticate_primary(
            folder,
            args.case,
            payload["frame"],
            root / "grounding-operation/validator",
            config,
        )
        measured = accounting.accept(
            load(root / "grounding-operation/worker/invocation-measurement.json"),
            "TREATMENT_B_VALID",
        )
        return {
            "review": load(folder / "stage_c_review.json"),
            "files_b64": {
                n: base64.b64encode((folder / n).read_bytes()).decode() for n in PRIMARY
            },
            "costs": {
                "grounding_wall_ns": time.perf_counter_ns() - started,
                "grounding_packet_bytes": sum(
                    len(v) for v in prepared["files"].values()
                ),
                "source_grounding_packet_bytes": len(prepared["files"]["packet.json"]),
                "model_usage": [result["provenance"]["usage"]],
                "model_tokens": {
                    k: result["provenance"]["usage"].get(k)
                    for k in ("input_tokens", "cached_input_tokens", "output_tokens")
                },
                "usage_availability": "CLI_REPORTED",
                "invocation_measurement": measured,
                "grounding_thread_id": result["provenance"]["thread_id"],
            },
        }

    async def authenticate_version() -> None:
        version = await workers.command(
            [codex.executable(config), "--no-daemon", "--version"],
            root,
            root / "grounding-operation/version",
        )
        require(
            version.stdout.decode().strip() == "codex-cli 0.162.1",
            "Scientific CLI runtime changed before entry",
        )

    asyncio.run(authenticate_version())
    capture.execute(
        root,
        design,
        rows,
        ground,
        implementation=load(root / "implementation.json")["implementation"],
        run_binding={
            "run_id": args.run_id,
            "stage_a_checkpoint": args.stage_a,
            "packet_checkpoint": args.packet_commit,
        },
        grounding_preflight=preflight,
    )

    files = bundle(root, load(root / "integrity.json")["sha256"])
    files.update(
        {
            "integrity.json": (root / "integrity.json").read_bytes(),
            "grounding-preentry-budget.json": (
                root / "grounding-preentry-budget.json"
            ).read_bytes(),
        },
    )
    workers.candidate(root, args.case, design["frame"], "B", files)
