# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0915, ASYNC240 -- frozen experiment-local host lifecycle
"""C-v2 host execution and exact replay; importing never executes science."""

from __future__ import annotations

import ast
import base64
import gzip
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from devtools.core.time import Duration
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration.isolation import PRIMARY, semantic_outputs
from experiments.orchestration.semantic_limits import InvocationBudget, InvocationLimits
from experiments.orchestration.storage import (
    exclusive,
    load,
    materialize,
    require,
    save,
)
from experiments.orchestration.workers import (
    accounting,
    capacity,
    codex,
    evidence,
    measurement,
    output_capacity,
    runtime,
    schema,
    semantic,
)
from experiments.source_grounding import packets, reviewer, workers
from experiments.source_grounding.chunked import (
    archive,
    classification,
    consolidation,
    disclosure,
    packing,
    response,
)

ROOT = Path(__file__).resolve().parents[3]
A1_CALLS = {"0022": 3, "0023": 3, "0024": 2}
POLICY: dict[str, Any] = {
    "A1": A1_CALLS,
    "A2_per_case": 24,
    "A2_cohort": 72,
    "GLOBAL_per_case": 1,
    "Astra_cohort": 83,
    "Sol_fresh": 1,
    "fresh_cohort": 84,
    "case_maximum": 28,
}
EXTRA = ("c2-capture.json.gz", "c2-usage.json")
METHOD = (
    b"# C-v2 blind gold\n\nDefinitions preserved; procedure amended. Fresh Astra/High "
    b"A1 exhaustive state-only coverage, selective A2 exact-evidence extraction, "
    b"host archive/cards, fresh global consolidation, host exact reattachment and "
    b"minimal-witness validation. No second reviewer, reconciliation or scientific "
    b"retry. A1 false negatives and omitted A2 evidence are unrecoverable. "
    b"Representation, capacity and invocation limits fail closed. Multiple calls "
    b"increase burden. Host routing not independently verified.\n"
)
LOG_FILES = (
    "receipt.json",
    "response-schema.json",
    "final-response.txt",
    "invocation-measurement.json",
    "process/stdin.bin",
    "process/stdout.log",
    "process/stderr.log",
    "process/exit.json",
)


def configuration() -> Any:
    """Bind unchanged Astra transport to both separate empirical receipts."""
    return {
        "model": "GPT-6 Astra",
        "model_id": "gpt-6-astra",
        "reasoning": "High",
        "runtime": runtime.configuration(),
        "bounded_response": True,
        "capacity_receipt": {
            "path": capacity.RECEIPT_ADDRESS,
            "sha256": digest((ROOT / capacity.RECEIPT_ADDRESS).read_bytes()),
        },
        "output_receipt": {
            "path": output_capacity.ADDRESS,
            "sha256": digest((ROOT / output_capacity.ADDRESS).read_bytes()),
        },
    }


def check(config: Any, raw: bytes, contract: Any) -> Any:
    """Exact empirical input and attained output gates precede semantic entry."""
    result = semantic.preflight_input(config, raw, contract)
    binding = config["output_receipt"]
    path = ROOT / binding["path"]
    require(
        digest(path.read_bytes()) == binding["sha256"],
        "Output receipt digest differs",
    )
    receipt = load(path)
    output_capacity.authenticate(receipt, config, ROOT)
    require(
        schema.envelope(contract).utf8_bytes <= receipt["response_bytes"],
        "OUTPUT_LIMIT: exceeds certified output workload",
    )
    return result


def packet_files(packet: Any, codec: bytes, host: Any) -> dict[str, bytes]:
    """Specialize only the method description in the existing standalone codec."""
    tree = ast.parse(packets.builder(codec, gold=True))
    found = 0
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, bytes)
            and node.value.startswith(b"# Method\n")
        ):
            node.value = METHOD
            found += 1
    require(found == 1, "Frozen C2 builder method projection")
    builder = (ast.unparse(ast.fix_missing_locations(tree)) + "\n").encode()
    files = {
        "packet.json": json_bytes(packet),
        "INSTRUCTIONS.md": METHOD,
        "stage_c_builder.py": builder,
    }
    files["packet_integrity.json"] = json_bytes(
        {
            "schema": "blind-primary-packet-integrity-v1",
            "files": {n: digest(v) for n, v in files.items()},
        },
    )
    files["c2-host.json"] = json_bytes(host)
    return files


def products(root: Path) -> dict[str, bytes]:
    """Preserve canonical gold/statistics while declaring the amended method."""
    files = reviewer.products(root)
    files["stage_c_method.md"] = METHOD
    hashes = json.loads(files["stage_c_hashes.json"])
    hashes["sha256"]["stage_c_method.md"] = digest(METHOD)
    files["stage_c_hashes.json"] = reviewer.canonical(hashes)
    return files


async def execute(root: Path, *, invoke: Any = None) -> None:  # noqa: C901 -- sequential fail-closed scientific phases
    """Execute one prospectively bound case; no resume or automatic retry."""
    packet = reviewer.packet(root)
    host = load(root / "c2-host.json")
    case = packet["case"]
    part1 = packing.partition(packet)
    require(part1 == host["a1_partition"], "Frozen A1 partition differs")
    expected = host["a1_calls"]
    require(
        case.startswith("SYNTHETIC-")
        or (case in A1_CALLS and expected == A1_CALLS[case]),
        "Frozen scientific cohort/count",
    )
    require(len(part1["batches"]) == expected, "A1 exact invocation count")
    config = host["semantic"]
    require(
        config["model_id"] == "gpt-6-astra" and config["reasoning"] == "High",
        "C2 primary model/effort",
    )
    limit = expected + 24 + 1
    budget = InvocationBudget(
        InvocationLimits({"A1": expected, "A2": 24, "GLOBAL": 1}, {case: limit}, limit),
    )
    operation = root / "c2"
    operation.mkdir(exist_ok=False)
    identity = host["invocation_prefix"]

    def names(stage: str, part: Any) -> tuple[str, ...]:
        return tuple(f"{identity}/{stage}/{b['index']}" for b in part["batches"])

    budget.reserve("A1", case, part1["partition_sha256"], names("A1", part1))
    budget.reserve("GLOBAL", case, "FROZEN_GLOBAL", (identity + "/GLOBAL/0",))
    save(operation / "spend.json", budget.snapshot())
    table = evidence.sources(packet)
    obligations = [o["id"] for o in packet["obligations"]]
    captures: list[Any] = []
    threads: set[str] = set()
    retained: dict[str, bytes] = {}
    if invoke is None:
        version = await workers.command(
            [codex.executable(config), "--no-daemon", "--version"],
            root,
            operation / "version",
        )
        require(
            version.stdout.decode().strip() == "codex-cli 0.162.1",
            "Scientific CLI runtime changed before entry",
        )

    async def call(
        stage: str,
        index: int,
        raw: bytes,
        instruction: bytes,
        contract: Any,
    ) -> tuple[str, Any, Any]:
        invocation = f"{identity}/{stage}/{index}"
        folder = operation / stage / str(index)
        folder.mkdir(parents=True)
        checked: dict[str, Any] = {}

        def preflight() -> None:
            checked.update(check(config, raw, contract))

        def entered() -> None:
            save(operation / "spend.json", budget.snapshot())
            exclusive(
                folder / "ENTERED.json",
                {
                    "invocation": invocation,
                    "budget": checked,
                    "profile": capacity.profile(config),
                },
            )

        budget.enter(invocation, preflight, entered)
        if invoke is None:
            auth = folder / "auth"
            materialize(auth, {"auth.json": Path(workers.AUTH_FILE).read_bytes()})
            env = {k: os.environ[k] for k in runtime.ENVIRONMENT if k in os.environ}
            env["CODEX_HOME"] = str(auth)
            result = await semantic.primary(
                config,
                json_bytes({"case": case, "frame": packet["frame"]}),
                instruction,
                contract,
                invocation,
                folder / "worker",
                env,
                7200,
                10,
                rendered_input=raw,
                empty_directory=folder / "empty-cwd",
            )
            measured = load(folder / "worker/invocation-measurement.json")
            for name in LOG_FILES:
                retained[f"{stage}/{index}/{name}"] = (
                    folder / "worker" / name
                ).read_bytes()
        else:
            result, measured = await invoke(stage, index, raw, contract, invocation)
        thread = result["provenance"]["thread_id"]
        require(thread not in threads, "C2 thread reused")
        threads.add(thread)
        exclusive(
            folder / "RETURNED.json",
            {
                "invocation": invocation,
                "payload_sha256": digest(json_bytes(result["payload"])),
            },
        )
        for name in ("ENTERED.json", "RETURNED.json"):
            retained[f"{stage}/{index}/{name}"] = (folder / name).read_bytes()
        return invocation, result["payload"], measured

    a1 = []
    pending = []
    for batch in part1["batches"]:
        keys = batch["source_keys"]
        invocation, payload, measured = await call(
            "A1",
            batch["index"],
            classification.render(packet, keys, table),
            classification.INSTRUCTION.encode(),
            classification.contract(keys, obligations),
        )
        a1.append((invocation, keys, payload))
        pending.append(measured)
    coverage = classification.validate(packet, tuple(a1))
    captures.extend(accounting.accept(m, "C2_A1_COMPLETE_COVERAGE") for m in pending)
    put_binary(operation / "a1-coverage.json", coverage.canonical)
    part2 = packing.partition(packet, coverage)
    put_binary(operation / "a2-partition.json", json_bytes(part2))
    # Reserve every eligible resource batch together; never take a fitting subset.
    budget.reserve("A2", case, part2["partition_sha256"], names("A2", part2))
    save(operation / "spend.json", budget.snapshot())
    a2 = []
    pending = []
    for batch in part2["batches"]:
        keys = batch["source_keys"]
        invocation, payload, measured = await call(
            "A2",
            batch["index"],
            packing.render(packet, keys, table, coverage),
            packing.INSTRUCTIONS.encode(),
            response.pass_a2(
                batch["cells"],
                keys,
                obligations,
                max(1, *(len(table[k]["content"]) for k in keys)),
            ),
        )
        a2.append((invocation, payload))
        pending.append(measured)
    exact = archive.assemble(
        packet,
        tuple(a2),
        digest(json_bytes(capacity.profile(config))),
        coverage=coverage,
    )
    captures.extend(accounting.accept(m, "C2_A2_COMPLETE_EVIDENCE") for m in pending)
    put_binary(operation / "evidence-archive.json", exact.canonical)
    raw = disclosure.from_archive(packet, exact)
    invocation, payload, measured = await call(
        "GLOBAL",
        0,
        raw,
        disclosure.INSTRUCTION.encode(),
        response.pass_b(len(coverage.grid), obligations),
    )
    review = consolidation.assemble(packet, exact, payload)
    captures.append(accounting.accept(measured, "C2_GLOBAL_CANONICAL_GOLD_VALID"))
    capture = {
        "schema": "source-grounding-C2-capture-v1",
        "packet_sha256": digest(json_bytes(packet)),
        "a1_partition": part1,
        "a1": a1,
        "a2_partition": part2,
        "a2": a2,
        "global": payload,
        "coverage_sha256": coverage.root,
        "archive_sha256": exact.sha256,
        "spend": budget.snapshot(),
        "measurements": captures,
        "files": {n: base64.b64encode(v).decode() for n, v in retained.items()},
    }
    encoded = json_bytes(capture)
    require(len(encoded) <= 128 << 20, "EVIDENCE_REPRESENTATION_LIMIT: capture closure")
    put_binary(root / EXTRA[0], gzip.compress(encoded, mtime=0))
    put_binary(
        root / EXTRA[1],
        json_bytes(
            {
                "invocations": captures,
                "totals": asdict(accounting.aggregate(tuple(captures))),
                "stage": {
                    s: asdict(
                        accounting.aggregate(
                            tuple(
                                c
                                for c in captures
                                if f"/{s}/" in c["measurement"]["invocation_id"]
                            ),
                        ),
                    )
                    for s in ("A1", "A2", "GLOBAL")
                },
            },
        ),
    )
    put_binary(root / "stage_c_review.json", reviewer.canonical(review))
    await workers.command(
        [
            sys.executable,
            "-B",
            str(root / "stage_c_builder.py"),
            "build",
            "--root",
            str(root),
        ],
        root,
        root / "c2-builder-logs",
    )
    validate(root)


def validate(root: Path) -> Any:
    """Replay classification, archive, reattachment and canonical artifacts only."""
    packet = reviewer.packet(root)
    with gzip.open(root / EXTRA[0], "rb") as stream:
        raw = stream.read((128 << 20) + 1)
    require(len(raw) <= 128 << 20, "C2 capture expansion bound")
    captured = json.loads(raw)
    require(
        captured["packet_sha256"] == digest(json_bytes(packet)),
        "C2 packet binding",
    )
    require(captured["a1_partition"] == packing.partition(packet), "C2 A1 replay")
    coverage = classification.validate(packet, tuple(captured["a1"]))
    require(coverage.root == captured["coverage_sha256"], "C2 coverage root")
    require(
        captured["a2_partition"] == packing.partition(packet, coverage),
        "C2 A2 replay",
    )
    require(
        len(captured["a2_partition"]["batches"]) <= POLICY["A2_per_case"],
        "SEMANTIC_INVOCATION_BUDGET",
    )
    exact = archive.assemble(
        packet,
        tuple(captured["a2"]),
        digest(json_bytes(capacity.profile(load(root / "c2-host.json")["semantic"]))),
        coverage=coverage,
    )
    require(exact.sha256 == captured["archive_sha256"], "C2 evidence root")
    review = consolidation.assemble(packet, exact, captured["global"])
    require(
        reviewer.canonical(review) == (root / "stage_c_review.json").read_bytes(),
        "C2 canonical replay differs",
    )
    require(
        all((root / n).read_bytes() == v for n, v in products(root).items()),
        "C2 products replay differs",
    )
    usage = load(root / EXTRA[1])
    require(
        usage["invocations"] == captured["measurements"]
        and usage["totals"]
        == asdict(accounting.aggregate(tuple(captured["measurements"]))),
        "C2 usage replay",
    )
    for capture in captured["measurements"]:
        accounting.accept(capture, "REPLAY")
    if not packet["case"].startswith("SYNTHETIC-"):
        verify_process_captures(packet, captured, coverage, exact)
    semantic_outputs({n: (root / n).read_bytes() for n in PRIMARY})
    return {
        "status": "PASS",
        "model": "GPT-6 Astra",
        "reasoning": "High",
        "second_reviewer": False,
        "reconciliation": False,
        "host_routing_independently_verified": False,
        "blindness": dict.fromkeys(reviewer.BLINDNESS, False),
        "method": "C-v2",
        "complete_cells": len(coverage.grid),
    }


def verify_process_captures(
    packet: Any,
    captured: Any,
    coverage: Any,
    exact: Any,
) -> None:
    """Rebuild every authorized disclosure and normalized provider measurement."""
    config = configuration()
    table = evidence.sources(packet)
    obligations = [o["id"] for o in packet["obligations"]]
    expected = []
    payloads = {row[0]: row[-1] for phase in ("a1", "a2") for row in captured[phase]}
    for phase, partition in (
        ("A1", captured["a1_partition"]),
        ("A2", captured["a2_partition"]),
    ):
        for batch in partition["batches"]:
            keys = batch["source_keys"]
            raw = packing.render(
                packet,
                keys,
                table,
                coverage if phase == "A2" else None,
            )
            contract = (
                classification.contract(keys, obligations)
                if phase == "A1"
                else response.pass_a2(
                    batch["cells"],
                    keys,
                    obligations,
                    max(1, *(len(table[k]["content"]) for k in keys)),
                )
            )
            expected.append((phase, batch["index"], raw, contract))
    expected.append(
        (
            "GLOBAL",
            0,
            disclosure.from_archive(packet, exact),
            response.pass_b(len(coverage.grid), obligations),
        ),
    )
    captures = captured["measurements"]
    require(len(captures) == len(expected), "C2 measurement coverage")
    files = {
        n: base64.b64decode(v, validate=True) for n, v in captured["files"].items()
    }
    allowed = {
        f"{phase}/{index}/{name}"
        for phase, index, _, _ in expected
        for name in (*LOG_FILES, "ENTERED.json", "RETURNED.json")
    }
    require(set(files) == allowed, "C2 process capture closure")
    for (phase, index, raw, contract), accepted in zip(expected, captures, strict=True):
        prefix = f"{phase}/{index}/"
        require(
            files[prefix + "process/stdin.bin"] == raw,
            "C2 disclosure replay/leakage",
        )
        entered = json.loads(files[prefix + "ENTERED.json"])
        native = json.loads(files[prefix + "receipt.json"])
        require(
            entered["invocation"]
            == native["invocation"]
            == accepted["measurement"]["invocation_id"]
            and native["status"] == "PASS"
            and native["tool_calls"] == 0
            and entered["budget"]["input_sha256"] == digest(raw),
            "C2 entry/process identity",
        )
        exit_record = json.loads(files[prefix + "process/exit.json"])
        require(
            exit_record["exit_code"] == 0
            and not exit_record["stdout_truncated"]
            and not exit_record["stderr_truncated"],
            "C2 process completion",
        )
        result = SimpleNamespace(
            stdout=files[prefix + "process/stdout.log"],
            duration=Duration.seconds(exit_record["duration_seconds"]),
        )
        payload = semantic.strict_object(files[prefix + "final-response.txt"].decode())
        turn = parse_codex_turn_output(result.stdout)
        events = [
            semantic.strict_object(line)
            for line in result.stdout.decode().splitlines()
            if line.strip()
        ]
        items = [
            e.get("item", {}) for e in events if e.get("type", "").startswith("item.")
        ]
        require(
            sum(e.get("type") == "turn.completed" for e in events) == 1
            and sum(i.get("type") == "agent_message" for i in items) == 1
            and all(
                i.get("type") in {"agent_message", "reasoning", "error"} for i in items
            )
            and semantic.strict_object(turn.final_message) == payload
            and b"tools::router" not in files[prefix + "process/stderr.log"],
            "C2 tool-free final transport agreement",
        )
        schema.validate(payload, contract)
        returned = json.loads(files[prefix + "RETURNED.json"])
        if phase == "GLOBAL":
            frozen_payload = captured["global"]
        else:
            frozen_payload = payloads[native["invocation"]]
        require(
            payload == frozen_payload
            and returned["payload_sha256"] == digest(json_bytes(payload))
            and native["input_sha256"] == digest(raw)
            and native["response_schema_sha256"]
            == digest(files[prefix + "response-schema.json"])
            == digest(json_bytes(contract)),
            "C2 captured semantic response/provenance differs",
        )
        observed = measurement.capture(
            config,
            packet["case"],
            native["invocation"],
            raw,
            result,
            schema.canonical(payload),
            validated=True,
            failure=None,
        )
        require(
            accounting.accept(observed, accepted["acceptance_domain"]) == accepted,
            "C2 raw/normalized scientific usage differs",
        )
