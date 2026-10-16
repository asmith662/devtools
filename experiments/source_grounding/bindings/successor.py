# Copyright (c) 2026
# ruff: noqa: ASYNC240, COM812, INP001, T201 -- bounded prospective publication, never execution
"""Replay execution-only bindings against the unchanged candidate-06 science."""

import argparse
import asyncio
import copy
import json
from pathlib import Path
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
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import load, require
from experiments.source_grounding import freeze

SOURCE = "2aad8a1c8ccc3cd19a0476d7da13f1d95a833d42"
PREDECESSOR = "92250292dacfb8289d129063d5523dd87b63162b"
ORIGINAL = (
    "experiments/source_grounding/plans/candidate-discrimination-startup-run-plan.json"
)
ORIGINAL_SHA = "64d0d087fb2ace87a2c01c931f3c03eda71d0e1d7af1a762afd10bc35f1a5f48"
PREFIX = "experiments/source_grounding/bindings/"
INTEGRITY = PREFIX + "execution-07-integrity.json"
BINDING = PREFIX + "execution-07.json"
BUILDER = PREFIX + "successor.py"
PLAN = (
    "experiments/source_grounding/plans/candidate-discrimination-pipeline-run-plan.json"
)


async def bindings() -> dict[str, bytes]:
    """Retain artifact bytes and fail if scientific implementation has changed."""
    raw = (ROOT / ORIGINAL).read_bytes()
    require(digest(raw) == ORIGINAL_SHA, "Frozen original plan changed")
    require(raw == await git("show", PREDECESSOR + ":" + ORIGINAL), "Predecessor bytes")
    old = RunPlan.parse(json.loads(raw))
    prior = load(ROOT / old.value["stage_a"]["integrity"]["path"])
    artifacts = prior["artifacts"]
    for address, sha in artifacts.items():
        data = (ROOT / address).read_bytes()
        require(digest(data) == sha, "Frozen scientific artifact changed: " + address)
        require(
            data == await git("show", PREDECESSOR + ":" + address), "Scientific bytes"
        )
    current = freeze.implementations()
    for address, sha in prior["implementation"].items():
        observed = digest((ROOT / address).read_bytes())
        if not address.startswith(("src/devtools/", "experiments/orchestration/")):
            require(observed == sha, "Scientific implementation changed: " + address)
        current.setdefault(address, observed)
    for address, sha in current.items():
        require(
            digest(await git("show", SOURCE + ":" + address)) == sha, "Source binding"
        )
    current[BUILDER] = digest(Path(__file__).read_bytes())
    integrity = json_bytes({**prior, "implementation": current})
    preserved = dict(artifacts)
    for case in old.value["cases"]:
        for item in case["inputs"]:
            address = item["path"]
            require(
                digest((ROOT / address).read_bytes()) == item["sha256"], "Input bytes"
            )
            preserved[address] = item["sha256"]
    for binding in old.value["adopted_branches"].values():
        for address in (
            binding["path"],
            str(Path(binding["path"]).parent / "closure.json.gz").replace("\\", "/"),
            binding["prospective_compatibility"]["path"],
        ):
            data = (ROOT / address).read_bytes()
            await Repository(ROOT, push=False).authenticate_blob(PREDECESSOR, address)
            preserved[address] = digest(data)
    record = {
        "schema": "source-grounding-prospective-execution-binding-v1",
        "source_checkpoint": SOURCE,
        "predecessor_checkpoint": PREDECESSOR,
        "predecessor_plan": ORIGINAL,
        "predecessor_plan_sha256": ORIGINAL_SHA,
        "predecessor_run_id": old.identity(old.value["controller_implementation"]),
        "supersedes_stage_a_checkpoint": old.value["stage_a"]["checkpoint"],
        "protocol_sha256": old.value["stage_a"]["protocol"]["sha256"],
        "integrity_sha256": digest(integrity),
        "controller_sha256": digest(json_bytes(implementation())),
        "scientific_artifacts_preserved": preserved,
        "implementation_changes": {
            address: {"old": prior["implementation"].get(address), "new": sha}
            for address, sha in current.items()
            if prior["implementation"].get(address) != sha
        },
        "scientific_semantics": "BYTE_IDENTICAL",
        "maximum_fresh_calls": 4,
        "approval": "NONE_FOR_REPLACEMENT",
        "scientific_execution": 0,
        "gold_access": False,
        "confirmation_reserve_access": False,
    }
    return {INTEGRITY: integrity, BINDING: json_bytes(record)}


async def plan(checkpoint: str) -> dict[str, Any]:
    """Derive identity using RunPlan; change only prospective execution bindings."""
    value: dict[str, Any] = copy.deepcopy(load(ROOT / ORIGINAL))
    value["attempt"] += 1
    value["name"] = "purpose-relative-source-grounding-candidate-discrimination-07"
    value["stage_a"]["checkpoint"] = checkpoint
    value["stage_a"]["integrity"] = {
        "path": INTEGRITY,
        "sha256": digest((ROOT / INTEGRITY).read_bytes()),
    }
    value["implementation"] = load(ROOT / INTEGRITY)["implementation"]
    value["controller_implementation"] = implementation()
    for case in value["cases"]:
        for item in case["inputs"]:
            if item["name"] == "implementation.json":
                item.update(value["stage_a"]["integrity"])
    for argv in [*value["commands"].values(), value["semantic"]["argv"]]:
        argv[argv.index("--stage-a") + 1] = checkpoint
    RunPlan.parse(value)
    await entrypoints.check(ROOT, value)
    return value


async def main() -> None:
    """Build once or verify exact replay; no controller run/approve is reachable."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify", "plan", "verify-plan"))
    parser.add_argument("--checkpoint")
    args = parser.parse_args()
    if args.mode in {"plan", "verify-plan"}:
        require(bool(args.checkpoint), "Committed binding checkpoint required")
        files = {PLAN: json_bytes(await plan(args.checkpoint))}
    else:
        files = await bindings()
    for address, raw in files.items():
        destination = ROOT / address
        if args.mode in {"verify", "verify-plan"}:
            require(destination.read_bytes() == raw, "Replay differs: " + address)
        else:
            require(not destination.exists(), "Prospective overwrite refused")
            put_binary(destination, raw)
    print(json.dumps({"status": "PASS", "artifacts": len(files), "authority": "NONE"}))


if __name__ == "__main__":
    asyncio.run(main())
