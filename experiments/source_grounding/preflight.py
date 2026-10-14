# Copyright (c) 2026
# ruff: noqa: T201 -- non-live launcher preflight only
"""Check installed launcher/version/help/argv. Never issue a model request."""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
from pathlib import Path

from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import ROOT, digest
from experiments.orchestration.storage import require
from experiments.orchestration.workers import codex
from experiments.source_grounding.freeze import PACKAGE
from experiments.source_grounding.workers import command, configuration


async def main() -> None:
    """Only version and help processes; argv construction is inert."""
    executable = shutil.which("codex.cmd") or shutil.which("codex")
    require(executable is not None, "Codex executable unavailable")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / ".local/source-grounding-launcher-preflight",
    )
    root = resolve_path(parser.parse_args().output, base_directory=ROOT).value
    root.mkdir(parents=True, exist_ok=False)
    version = await command([str(executable), "--version"], root, root / "version")
    require(
        version.stdout.decode().strip() == "codex-cli 0.162.1",
        "Required Codex version differs",
    )
    help_text = await command([str(executable), "exec", "--help"], root, root / "help")
    require(
        all(
            flag in help_text.stdout.decode()
            for flag in (
                "--ignore-user-config",
                "--ignore-rules",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "--model",
                "--json",
            )
        ),
        "Installed launcher contract differs",
    )
    # Real packets use this exact basename; no packet or semantic output is built.
    (root / "INSTRUCTIONS.md").write_bytes(
        (PACKAGE / "INSTRUCTIONS_GOLD.md").read_bytes(),
    )
    commands = []
    for model in ("Sol", "Astra"):
        config = configuration(model)
        argv = codex.argv(config, root)
        require(
            config["model_id"] in argv
            and 'model_reasoning_effort="high"' in argv
            and "resume" not in argv
            and "fork" not in argv,
            "Frozen fresh model invocation",
        )
        commands.append(
            {
                "model": config["model"],
                "model_id": config["model_id"],
                "reasoning": config["reasoning"],
                "argv_sha256": digest(repr(argv).encode()),
            },
        )
    print(
        json.dumps(
            {
                "status": "PASS",
                "installed": version.stdout.decode().strip(),
                "required": "codex-cli 0.162.1",
                "executable": executable,
                "configurations": commands,
                "live_model_calls": 0,
            },
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
