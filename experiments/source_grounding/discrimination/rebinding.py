# Copyright (c) 2026
# ruff: noqa: ANN401, T201, COM812 -- binding-only prospective artifact assembly
"""Copy frozen candidate science exactly; rebind executable startup, never run it."""

import argparse
import asyncio
import copy
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    digest,
    git,
    json_bytes,
    put_binary,
)
from experiments.orchestration import entrypoints
from experiments.orchestration.controller import implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load, require
from experiments.source_grounding import freeze
from experiments.source_grounding import plan as maintained

PREVIOUS = "experiments/source_grounding/stage_a/candidate-05"
PREVIOUS_PLAN = (
    "experiments/source_grounding/plans/candidate-discrimination-run-plan.json"
)
ADDRESS = "experiments/source_grounding/stage_a/candidate-06"
PLAN = (
    "experiments/source_grounding/plans/candidate-discrimination-startup-run-plan.json"
)
FAILED = "b34e9e288e30f7289e14453f8a2f9ca8acd6940dee05037486c403c803b5d2c6"
DISPOSITION = (
    "experiments/source_grounding/invalidations/" + FAILED + "/invalidation.json"
)
ENTRY = "experiments/source_grounding/discrimination/entry.py"
PRIOR_STAGE_A = "27badaca445dcda280e69b65fb662b1523d3d1a0"


def contract() -> Any:
    """Bind the one unique direct Python plan worker shared by every stage."""
    return {
        "schema": entrypoints.SCHEMA,
        "mode": "DIRECT_SCRIPT_HELP",
        "timeout_seconds": 30,
        "scripts": {ENTRY: digest((ROOT / ENTRY).read_bytes())},
    }


async def stage_a(engineering: str) -> dict[str, bytes]:
    """No candidate regeneration, resampling or semantic inspection occurs."""
    await git(
        "merge-base",
        "--is-ancestor",
        "52e697cea6b4ce066898031938e127f0c565fc3a",
        engineering,
    )
    files = {}
    unchanged = {}
    names = [
        "METHOD.md",
        "cohort.json",
        "economics.json",
        "0024-treatment-template.bin",
    ]
    names += [
        f"{case}-{kind}.json"
        for case in ("0022", "0023", "0024")
        for kind in ("universe", "selection")
    ]
    for name in names:
        raw = (ROOT / PREVIOUS / name).read_bytes()
        require(
            raw == await git("show", PRIOR_STAGE_A + ":" + PREVIOUS + "/" + name),
            "Original scientific bytes changed",
        )
        files[ADDRESS + "/" + name] = raw
        unchanged[name] = digest(raw)
    p = copy.deepcopy(load(ROOT / PREVIOUS / "protocol.json"))
    disposition = load(ROOT / DISPOSITION)
    p["preserved_evidence"].update(disposition["journal_sha256"])
    p["preserved_evidence"].update(disposition["preserved_run_context_sha256"])
    p["worker_entrypoints"] = contract()
    p["binding_revision"] = {
        "schema": "candidate-startup-binding-only-v1",
        "previous_stage_a": PRIOR_STAGE_A,
        "previous_path": PREVIOUS,
        "failed_run_id": FAILED,
        "failed_approval_checkpoint": disposition["approval_checkpoint"],
        "failed_approval_use": "HISTORICAL_ONLY; DO_NOT_RESUME",
        "engineering_checkpoint": engineering,
        "scientific_method": "UNCHANGED",
        "scientific_contract": "ALL_FROZEN_SCIENTIFIC_SEMANTICS_UNCHANGED",
        "maximum_fresh_calls": 4,
        "unchanged_scientific_files": unchanged,
        "only_change": (
            "Correct executable module ownership and prospectively gate "
            "real direct-script startup before PLAN_VALID"
        ),
    }
    p["scientific_method"] = ADDRESS + "/METHOD.md"
    argv = p["workers"]["gold"]["argv"]
    argv[argv.index("--stage-a") + 1] = engineering
    files[ADDRESS + "/protocol.json"] = json_bytes(p)
    pinned = freeze.implementations()
    for address, sha in load(ROOT / PREVIOUS / "integrity.json")[
        "implementation"
    ].items():
        if "/engineering/host_disclosure/" in address:
            require(
                digest((ROOT / address).read_bytes()) == sha,
                "Capacity evidence changed",
            )
            pinned[address] = sha
    files[ADDRESS + "/integrity.json"] = json_bytes(
        {
            "schema": "source-grounding-stage-a-integrity-v1",
            "artifacts": {n: digest(raw) for n, raw in files.items()},
            "implementation": pinned,
        }
    )
    return files


async def run_plan(checkpoint: str) -> Any:
    """Bind identical scientific inputs to corrected implementation and a new ID."""
    value = copy.deepcopy(load(ROOT / PREVIOUS_PLAN))
    p = load(ROOT / ADDRESS / "protocol.json")
    integrity = load(ROOT / ADDRESS / "integrity.json")
    value.update(
        name="purpose-relative-source-grounding-candidate-discrimination-06",
        attempt=6,
        stage_a={
            "checkpoint": checkpoint,
            **{
                name: {
                    "path": ADDRESS + "/" + name + ".json",
                    "sha256": digest((ROOT / ADDRESS / (name + ".json")).read_bytes()),
                }
                for name in ("protocol", "integrity")
            },
        },
        implementation=integrity["implementation"],
        controller_implementation=implementation(),
        preserved_evidence=p["preserved_evidence"],
        worker_entrypoints=p["worker_entrypoints"],
    )
    for case in value["cases"]:
        for item in case["inputs"]:
            if item["path"].startswith(PREVIOUS + "/"):
                item["path"] = ADDRESS + item["path"][len(PREVIOUS) :]
                item["sha256"] = digest((ROOT / item["path"]).read_bytes())
    for argv in [*value["commands"].values(), value["semantic"]["argv"]]:
        argv[argv.index("--stage-a") + 1] = checkpoint
    checks = maintained.validation_commands(integrity["implementation"])
    checks[0].append("experiments/source_grounding/discrimination")
    value["validation"] = dict.fromkeys(("local", "checkpoint", "final"), checks)
    RunPlan.parse(value)
    await entrypoints.check(ROOT, value)
    return value


async def main() -> None:
    """Write once or replay prospective bytes; no approval/scientific execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify", "plan", "verify-plan"))
    parser.add_argument("--checkpoint", required=True)
    args = parser.parse_args()
    files = (
        {PLAN: json_bytes(await run_plan(args.checkpoint))}
        if args.mode in {"plan", "verify-plan"}
        else await stage_a(args.checkpoint)
    )
    for address, raw in files.items():
        path = ROOT / address
        if args.mode in {"verify", "verify-plan"}:
            require(path.read_bytes() == raw, "Binding-only replay differs: " + address)
        else:
            require(not path.exists(), "Prospective overwrite refused")
            put_binary(path, raw)
    print(
        json.dumps(
            {
                "status": "PASS",
                "artifacts": len(files),
                "execution_authorized": "NO",
                "scientific_ENTERED": 0,
            }
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
