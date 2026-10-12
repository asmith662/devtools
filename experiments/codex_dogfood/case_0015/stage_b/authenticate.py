# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, C901, PLR2004 -- complete immutable authentication boundary, frozen identities
"""Authenticate committed Stage A while permitting separate later-stage owners."""

from __future__ import annotations

import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0015 import freeze, protocol

STAGE_A = "d7e28de0e103bdf0e494a0156311fa1c14b6c9f8"
PREFIX = "experiments/codex_dogfood/case_0015/"


async def authenticate() -> dict[str, Any]:
    """Use the unchanged established deterministic engine and committed seals."""
    await git("merge-base", "--is-ancestor", STAGE_A, "HEAD")
    seal_bytes = await git("show", STAGE_A + ":" + PREFIX + "integrity.json")
    if (
        digest(seal_bytes)
        != "86438745a88c79fa0fafd132f454fcc807de0afc93d7d01a210f740338896619"
        or seal_bytes != binary(freeze.CASE / "integrity.json")
    ):
        raise ValueError("Authoritative Stage A integrity mismatch")
    seal = json.loads(seal_bytes)
    for name, expected in {**seal["artifacts"], **seal["authored"]}.items():
        if (
            digest(binary(freeze.CASE / name)) != expected
            or digest(await git("show", STAGE_A + ":" + PREFIX + name)) != expected
        ):
            raise ValueError("Stage A artifact mismatch: " + name)
    for name, expected in seal["implementation"].items():
        if (
            digest(binary(ROOT / name)) != expected
            or digest(await git("show", STAGE_A + ":" + name)) != expected
        ):
            raise ValueError("Frozen implementation mismatch: " + name)
    # The original root-only no-execution layout guard intentionally rejects
    # later-stage directories. Replay its unchanged deterministic engine here;
    # later stages own their own exclusive attempts and absence guards.
    for name, raw in (await freeze.expected()).items():
        if binary(freeze.CASE / name) != raw:
            raise ValueError("Established Stage A deterministic replay differs")
    design = read_json(freeze.CASE / "protocol.json")
    if (
        design["no_execution"] != protocol.COUNTS
        or design["source_head"] != protocol.START
    ):
        raise ValueError("Stage A initial counts/source mismatch")
    if json_bytes(design["queries"]) != json_bytes(protocol.authored()["queries"]):
        raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: frozen queries changed")
    metadata = read_json(freeze.CASE / "frame.json")
    if (
        metadata["resource_count"] != 515
        or metadata["snapshot_id"]
        != "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
        or metadata["corpus_id"]
        != "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa"
    ):
        raise ValueError("Frozen frame binding mismatch")
    return {
        "status": "PASS",
        "stage_a": STAGE_A,
        "integrity_sha256": digest(seal_bytes),
        "protocol_sha256": digest(binary(freeze.CASE / "protocol.json")),
        "frame": {k: v for k, v in metadata.items() if k != "resources"},
        "initial_counts": protocol.COUNTS,
    }
