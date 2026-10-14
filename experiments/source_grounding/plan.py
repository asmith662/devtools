# Copyright (c) 2026
# ruff: noqa: ANN401, E501, T201 -- deterministic prospective plan, never approval
"""Create the real v2 plan only after remotely durable scientific Stage A."""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    digest,
    git,
    json_bytes,
    put_binary,
)
from experiments.orchestration.controller import implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import require
from experiments.source_grounding.cases import CASES
from experiments.source_grounding.freeze import PACKAGE, PREFIX

PLAN_ADDRESS = "experiments/source_grounding/plans/corrected-run-plan.json"


def source_scope(bound_implementation: dict[str, str]) -> list[str]:
    """Name every maintained adapter module; never recurse into scientific data."""
    owned = sorted(
        p.relative_to(PACKAGE.parents[1]).as_posix() for p in PACKAGE.glob("*.py")
    )
    frozen = sorted(
        address
        for address in bound_implementation
        if address.startswith(PREFIX)
        and address.endswith(".py")
        and "/" not in address[len(PREFIX) :]
    )
    require(
        bool(owned) and frozen == owned,
        "Maintained static source ownership differs from Stage A",
    )
    return frozen


def validation_commands(bound_implementation: dict[str, str]) -> list[list[str]]:
    """Use the same exact source addresses for all implementation static tools."""
    scope = source_scope(bound_implementation)
    return [
        [
            "uv",
            "run",
            "pytest",
            "--no-cov",
            "-q",
            "experiments/source_grounding/test_contracts.py",
            "experiments/source_grounding/test_scope.py",
        ],
        ["uv", "run", "ruff", "check", *scope],
        ["uv", "run", "ruff", "format", "--check", *scope],
        ["uv", "run", "mypy", "--strict", *scope],
    ]


async def derive(checkpoint: str) -> Any:
    """Bind committed Stage A, never require or create execution approval."""
    require(
        (await git("rev-parse", checkpoint)).decode().strip() == checkpoint,
        "Full Stage A checkpoint required",
    )
    require(
        (await git("rev-parse", "origin/main")).decode().strip() == checkpoint
        or (await git("merge-base", checkpoint, "origin/main")).decode().strip()
        == checkpoint,
        "Stage A not remotely durable",
    )
    integrity_raw = await git(
        "show",
        checkpoint + ":" + PREFIX + "stage_a/integrity.json",
    )
    integrity = json.loads(integrity_raw)
    cases = []
    for case in CASES:
        base = f"experiments/codex_dogfood/case_{case}/"
        design = json.loads(
            await git("show", checkpoint + ":" + base + "protocol.json"),
        )
        addresses = {
            "design.json": base + "protocol.json",
            "frame.json": base + "frame.json",
            "resources.json.gz": base + "resources.json.gz",
            "INSTRUCTIONS_GROUNDING.md": PREFIX + "INSTRUCTIONS_GROUNDING.md",
            "INSTRUCTIONS_GOLD.md": PREFIX + "INSTRUCTIONS_GOLD.md",
            "reviewer_codec.py": PREFIX + "reviewer.py",
            "implementation.json": PREFIX + "stage_a/integrity.json",
            "worker_configuration.json": PREFIX + "stage_a/protocol.json",
        }
        cases.append(
            {
                "id": case,
                "frame": design["frame"],
                "inputs": [
                    {
                        "path": address,
                        "name": name,
                        "sha256": digest(await git("show", checkpoint + ":" + address)),
                    }
                    for name, address in addresses.items()
                ],
            },
        )
    commands = {
        stage: [
            "{python}",
            "-B",
            "{repository}/experiments/source_grounding/entry.py",
            stage,
            "--workspace",
            "{workspace}",
            "--case",
            "{case}",
            "--frame",
            "{frame}",
            "--run-id",
            "{run_id}",
            "--stage-a",
            checkpoint,
            "--packet-commit",
            "{packet_commit}",
        ]
        for stage in (
            "prepare",
            "prepare_validate",
            "packet",
            "packet_validate",
            "B",
            "B_validate",
            "C_validate",
            "import",
            "import_validate",
            "D",
            "D_validate",
        )
    }
    # File execution must use installed framework + repo-owned experiment imports.
    # workers.py bootstraps only its trusted code root, never into semantic input.
    checks = validation_commands(integrity["implementation"])
    value = {
        "schema": "experiment-controller-plan-v2",
        "name": "purpose-relative-source-grounding-02",
        "attempt": 2,
        "stage_a": {
            "checkpoint": checkpoint,
            "protocol": {
                "path": PREFIX + "stage_a/protocol.json",
                "sha256": digest(
                    await git(
                        "show",
                        checkpoint + ":" + PREFIX + "stage_a/protocol.json",
                    ),
                ),
            },
            "integrity": {
                "path": PREFIX + "stage_a/integrity.json",
                "sha256": digest(integrity_raw),
            },
        },
        "cases": cases,
        "commands": commands,
        "semantic": json.loads(
            await git("show", checkpoint + ":" + PREFIX + "stage_a/protocol.json"),
        )["workers"]["gold"],
        "publication": {
            "root": PREFIX + "runs",
            "remote": "origin",
            "branch": "main",
            "push": True,
            "subjects": {
                "PACKET": "Freeze source grounding blind packets",
                "B": "Capture purpose-relative source grounding cohort",
                "C": "Import purpose-relative source grounding gold",
                "D": "Evaluate purpose-relative source grounding cohort",
            },
        },
        "validation": {
            "local": checks,
            "checkpoint": checks,
            "final": [
                *checks,
                [
                    "uv",
                    "run",
                    "python",
                    "-m",
                    "experiments.source_grounding.timing",
                    "--plan",
                    PLAN_ADDRESS,
                ],
            ],
        },
        "concurrency": {"cases": 3, "workers": 3, "semantic": 1},
        "timeouts": {"worker": 21600, "validation": 3600, "grace": 10},
        "retry": "NEVER_SCIENTIFIC",
        "implementation": integrity["implementation"],
        "controller_implementation": implementation(),
        "cache": {
            "enabled": False,
            "observation_semantics": "source-grounding-serialized-parent-frame-v1",
            "configuration": {
                "native_indices_or_RI_cached": False,
                "disabled_reason": "Preparation authenticates disclosed bytes without deriving a new cache surface; controller rejects input/output cache ownership overlap. Stage A observation cache is operational only.",
                "input_surface": "exact serialized Stage A frame; validators always run",
                "progress": "controller progress.json/log/state and immutable worker receipts",
                "final_verification": "all stage receipts, B sealed proof, exact primary import and deterministic D replay; FINAL protected/static once",
            },
            "surfaces": ["frame.json", "resources.json.gz", "design.json"],
        },
    }
    RunPlan.parse(value)
    return value


async def main() -> None:
    """Create once or verify exact plan bytes; never authorize execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    parser.add_argument("--stage-a", required=True)
    args = parser.parse_args()
    raw = json_bytes(await derive(args.stage_a))
    path = PACKAGE.parents[1] / PLAN_ADDRESS
    if args.mode == "build":
        require(not path.exists(), "Run plan overwrite refused")
        put_binary(path, raw)
    else:
        require(path.read_bytes() == raw, "Run plan deterministic rebuild differs")
    print(
        json.dumps(
            {
                "status": "PASS",
                "plan_sha256": digest(raw),
                "execution_authorized": "NO",
            },
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
