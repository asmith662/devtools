# Copyright (c) 2026
# ruff: noqa: ANN401, T201, ASYNC240, PLR0915 -- explicitly authorized read-only scientific authentication and exact-byte sealing
"""Seal returned B22/B23 without retrieval, model calls or semantic interpretation."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from devtools.core.time import Duration
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.orchestration.adoption import SCHEMA, AdoptedBranch, pack
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import binary, bundle, load, require
from experiments.orchestration.workers import accounting, measurement, semantic
from experiments.source_grounding.capture import sealed

ORIGIN = "b6cd4408b4dbc86a50c335f4a364898ff3b45c123becb7b6865c34208d3e1982"
STAGE_A = "f1c0839bba3e39bc3973099164c48d46e5bf631a"
PACKET = "816deef3a9db342ec82fcb9bf02843cc0d5d7911"
DESTINATION = "experiments/orchestration/engineering/adopted_branches"


async def build(repository: Path, case: str) -> dict[str, Any]:
    """Preserve the complete sealed closure and original process usage exactly."""
    require(
        case in {"0022", "0023"},
        "Only authorized completed branches may be sealed",
    )
    science = repository / "experiments/source_grounding/runs" / ORIGIN
    journal = science / "journal" / case / "B"
    entered_raw, returned_raw = (
        binary(journal / "ENTERED.json"),
        binary(journal / "RETURNED.json"),
    )
    entered, returned = load(journal / "ENTERED.json"), load(journal / "RETURNED.json")
    require(not (journal / "FAILED.json").exists(), "Failed branch cannot be sealed")
    root = Path(returned["workspace"])
    require(
        root == Path("C:/ExperimentWorkers") / ORIGIN / case / "B",
        "Exact origin worker ownership required",
    )
    files = {
        "artifacts/" + name: raw
        for name, raw in bundle(root, returned["files"]).items()
    }
    rows = load_rows(root)
    validation = sealed(root, rows)
    require(validation == returned["validation"], "Original validator receipt differs")
    marker = load(root / "native/execution_started.json")
    require(
        marker["run_binding"]
        == {
            "run_id": ORIGIN,
            "stage_a_checkpoint": STAGE_A,
            "packet_checkpoint": PACKET,
        },
        "Original Stage A/PACKET binding differs",
    )
    config = load(root / "worker_configuration.json")["workers"]["grounding"]
    receipt_path = root / "grounding-operation/worker"
    primary = load(receipt_path / "receipt.json")
    prompt = binary(receipt_path / "process/stdin.bin")
    packet_raw, instructions = (
        binary(root / "grounding-worker/packet.json"),
        binary(root / "grounding-worker/INSTRUCTIONS.md"),
    )
    require(
        semantic.render_disclosure(
            config,
            packet_raw,
            instructions,
            primary["invocation"],
        )
        == prompt,
        "Prospective unchanged-B disclosure compatibility failed",
    )
    require(
        primary["model"] == "GPT-6 Sol"
        and primary["reasoning"] == "High"
        and primary["tool_calls"] == 0,
        "Original Sol/High tool-free process required",
    )
    repo = Repository(repository, push=False)
    contracts = {}
    for address in [
        *(
            "experiments/source_grounding/" + n
            for n in (
                "capture.py",
                "contracts.py",
                "reviewer.py",
                "response.py",
                "packets.py",
                "workers.py",
                "INSTRUCTIONS_GROUNDING.md",
            )
        ),
        "experiments/orchestration/workers/evidence.py",
    ]:
        original = await repo.git("show", STAGE_A + ":" + address)
        require(
            binary(repository / address) == original,
            "B scientific contract changed: " + address,
        )
        contracts[address] = digest(original)
    require(
        not (science / "journal/0023/C/ENTERED.json").exists()
        and not (science / "journal/0024/B/ENTERED.json").exists(),
        "Unexpected later branch entry",
    )
    require(
        not any((science / "C").glob("**/stage_c_review.json")),
        "Unexpected published gold",
    )
    failed_c = binary(science / "journal/0022/C/FAILED.json")
    for sibling in ("0022", "0023", "0024"):
        require(
            not (
                Path("C:/ExperimentWorkers")
                / ORIGIN
                / sibling
                / "C/stage_c_review.json"
            ).exists(),
            "Forbidden later gold exists",
        )
    compatibility = {
        "schema": "unchanged-source-grounding-B-v1",
        "scientific_contract": contracts,
        "original_disclosure_replay_sha256": digest(prompt),
        "semantic_interpretation": "NONE",
    }
    independence = {
        "packet_commit": PACKET,
        "sibling_dependency": False,
        "downstream_dependency": False,
        "forbidden_later_evidence_available": False,
        "C22_failed_journal_sha256": digest(failed_c),
        "disclosure_immutable": True,
        "semantic_tool_calls": 0,
        "host_routing_independently_verified": False,
    }
    exit_record = load(receipt_path / "process/exit.json")
    result = SimpleNamespace(
        stdout=binary(receipt_path / "process/stdout.log"),
        duration=Duration.seconds(exit_record["duration_seconds"]),
    )
    usage = accounting.accept(
        measurement.capture(
            config,
            case,
            primary["invocation"],
            prompt,
            result,
            None,
            validated=True,
            failure=None,
        ),
        "ORIGINAL_COMPLETED_BRANCH_SEAL; NOT_OLD_PUBLICATION",
    )
    provenance = {
        "ENTERED.json": entered_raw,
        "RETURNED.json": returned_raw,
        "semantic-receipt.json": binary(receipt_path / "receipt.json"),
        "process-exit.json": binary(receipt_path / "process/exit.json"),
        "stdout.jsonl": result.stdout,
        "stderr.log": binary(receipt_path / "process/stderr.log"),
        "disclosure.bin": prompt,
        "instruction.bin": instructions,
        "response-schema.json": binary(receipt_path / "response-schema.json"),
        "final-response.txt": binary(receipt_path / "final-response.txt"),
        "origin-run.json": binary(science / "run.json"),
        "origin-approval.json": binary(science / "authorization/approval.json"),
        "origin-PACKET-publication.json": binary(science / "publications/PACKET.json"),
        "compatibility.json": json_bytes(compatibility),
        "independence.json": json_bytes(independence),
        "old-runtime.json": json_bytes(config["runtime"]),
    }
    files.update({"provenance/" + name: raw for name, raw in provenance.items()})
    context = load(science / "run.json")
    protocol_binding = context["plan"]["stage_a"]["protocol"]
    original_protocol = await repo.git("show", STAGE_A + ":" + protocol_binding["path"])
    require(
        digest(original_protocol) == protocol_binding["sha256"],
        "Original protocol digest differs",
    )
    files["provenance/Stage-A-protocol.json"] = original_protocol
    files["provenance/C22-FAILED.json"] = failed_c
    require(
        context["plan"]["stage_a"]["checkpoint"] == STAGE_A
        and entered["inputs_sha256"] == returned["inputs_sha256"],
        "Origin plan/input mismatch",
    )
    compressed = pack(files)
    inventory = {
        name: {"bytes": len(raw), "sha256": digest(raw)}
        for name, raw in sorted(files.items())
    }
    value = {
        "schema": SCHEMA,
        "origin": {
            "run_id": ORIGIN,
            "attempt": context["plan"]["attempt"],
            "case": case,
            "operation": "B",
            "stage_a": STAGE_A,
            "packet_commit": PACKET,
        },
        "frame": returned["frame"],
        "input_sha256": entered["inputs_sha256"],
        "scientific_files": returned["files"],
        "validation": validation,
        "model": primary["model"],
        "reasoning": primary["reasoning"],
        "runtime": config["runtime"],
        "implementation": marker["implementation"],
        "original_usage": usage,
        "compatibility": compatibility,
        "compatibility_sha256": digest(json_bytes(compatibility)),
        "independence": independence,
        "closure_file": "closure.json.gz",
        "closure_sha256": digest(compressed),
        "inventory": inventory,
        "inventory_sha256": digest(json_bytes(inventory)),
        "eligibility": {
            "entered": True,
            "returned": True,
            "failed": False,
            "complete_artifact_closure": True,
            "independent": True,
            "unchanged_branch_semantics": True,
        },
    }
    raw = json_bytes(value)
    AdoptedBranch.authenticate(
        raw,
        compressed,
        digest(raw),
        value["compatibility_sha256"],
    )
    destination = repository / DESTINATION / ORIGIN / case
    require(not destination.exists(), "Branch seal overwrite prohibited")
    destination.mkdir(parents=True)
    put_binary(destination / ".gitattributes", b"* -text -whitespace\n")
    put_binary(destination / "closure.json.gz", compressed)
    put_binary(destination / "seal.json", raw)
    return {
        "case": case,
        "path": (destination / "seal.json").relative_to(repository).as_posix(),
        "sha256": digest(raw),
        "compatibility_sha256": value["compatibility_sha256"],
        "closure_bytes": len(compressed),
        "artifact_count": len(returned["files"]),
        "artifact_bytes": sum(
            len(v) for n, v in files.items() if n.startswith("artifacts/")
        ),
        "usage": asdict(accounting.aggregate((usage,))),
    }


def load_rows(root: Path) -> Any:
    """Decode only the authorized parent resource observation, not native archives."""
    return json.loads(gzip.decompress(binary(root / "resources.json.gz")))


async def main() -> None:
    """Require an explicit sealing command; importing executes no experiment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true", required=True)
    parser.parse_args()
    repository = Path(__file__).resolve().parents[2]
    for case in ("0022", "0023"):
        print(json_bytes(await build(repository, case)).decode())


if __name__ == "__main__":
    asyncio.run(main())
