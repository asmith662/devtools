# Copyright (c) 2026
# ruff: noqa: ANN401, ASYNC240, T201, PLR2004, COM812 -- narrow prospective direct-script startup gate
"""Prove declared Python worker imports before plan validity, never run a stage."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor
from devtools.resources.commands.errors import CommandError
from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration.storage import binary, load, require, safe

SCHEMA = "python-worker-entrypoint-preflight-v1"


def inventory(value: Any) -> list[str]:
    """Inventory unique explicit Python scripts, independent of cases/stages."""
    commands = list(value["commands"].values())
    if value["semantic"].get("kind") == "process":
        commands.append(value["semantic"]["argv"])
    scripts = set()
    for argv in commands:
        if argv[0] != "{python}":
            continue
        require(
            len(argv) >= 3
            and argv[1] == "-B"
            and argv[2].startswith("{repository}/")
            and argv[2].endswith(".py"),
            "PLAN_INVALID: unsupported Python worker startup shape",
        )
        scripts.add(argv[2].removeprefix("{repository}/"))
    return sorted(scripts)


def validate(value: Any) -> None:
    """Keep old plans readable; new bound gates must cover the exact inventory."""
    if "worker_entrypoints" not in value:
        return
    contract = value["worker_entrypoints"]
    require(
        set(contract) == {"schema", "mode", "timeout_seconds", "scripts"}
        and contract["schema"] == SCHEMA
        and contract["mode"] == "DIRECT_SCRIPT_HELP"
        and type(contract["timeout_seconds"]) is int
        and 1 <= contract["timeout_seconds"] <= 60
        and isinstance(contract["scripts"], dict)
        and sorted(contract["scripts"]) == inventory(value),
        "PLAN_INVALID: incomplete worker-entrypoint preflight inventory",
    )
    for address, sha in contract["scripts"].items():
        safe(Path.cwd(), address)
        require(
            len(sha) == 64
            and set(sha) <= set("0123456789abcdef")
            and value["implementation"].get(address) == sha,
            "PLAN_INVALID: entrypoint implementation binding",
        )


async def check(root: Path, value: Any) -> dict[str, Any]:
    """Execute --help in fresh external CWDs; no workspace or semantic entry."""
    validate(value)
    scripts = inventory(value)
    required = any("source_grounding/discrimination/" in p for p in scripts)
    require(
        not required or "worker_entrypoints" in value,
        "PLAN_INVALID: discrimination worker-entrypoint preflight required",
    )
    if "worker_entrypoints" not in value:
        return {"status": "NOT_APPLICABLE", "scope": "LEGACY_UNBOUND_PLAN"}
    contract = value["worker_entrypoints"]
    results = []
    for address, expected in contract["scripts"].items():
        script = safe(root, address)
        require(
            digest(binary(script)) == expected, "PLAN_INVALID: startup bytes changed"
        )
        with tempfile.TemporaryDirectory(prefix="devtools-worker-preflight-") as folder:
            cwd = resolve_path(Path(folder)).value
            require(
                not cwd.is_relative_to(root.resolve())
                and cwd != script.parent.resolve(),
                "PLAN_INVALID: startup preflight requires external disposable CWD",
            )
            argv = [sys.executable, "-B", str(script), "--help"]
            try:
                result = await CommandExecutor().execute(
                    Command(argv[0])
                    .args(*argv[1:])
                    .cwd(resolve_path(cwd))
                    .with_timeout(Duration.seconds(contract["timeout_seconds"])),
                )
            except (CommandError, OSError) as error:
                message = (
                    "PLAN_INVALID: worker-entrypoint preflight process failed: "
                    + address
                )
                raise ValueError(message) from error
            require(
                result.exit_code == 0
                and not result.stdout_truncated
                and not result.stderr_truncated
                and b"usage:" in result.stdout.lower()
                and not list(cwd.iterdir())
                and digest(binary(script)) == expected,
                "PLAN_INVALID: worker-entrypoint startup preflight failed: "
                + address
                + ": "
                + result.stderr.decode("utf-8", errors="replace")[:2048],
            )
            results.append(
                {
                    "script": address,
                    "sha256": expected,
                    "argv": argv,
                    "python_version": sys.version,
                    "cwd": str(cwd),
                    "external_cwd": True,
                    "cwd_unchanged": True,
                    "exit_code": result.exit_code,
                    "stdout_sha256": digest(result.stdout),
                    "stderr_sha256": digest(result.stderr),
                },
            )
    return {"schema": SCHEMA, "status": "PASS", "scripts": results, "model_calls": 0}


def main() -> None:
    """Expose the same harmless gate used before PLAN_VALID for manual checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(asyncio.run(check(args.repository.resolve(), load(args.plan)))))


if __name__ == "__main__":
    main()
