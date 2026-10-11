# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- frozen case-local JSON boundary
"""Authenticate unchanged Stage A while permitting separate later-stage ownership."""

from __future__ import annotations

import gzip
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    read_json,
)
from experiments.codex_dogfood.case_0012.freeze import restore_frame
from experiments.codex_dogfood.case_0013 import freeze, protocol

STAGE_A = "6b18b6e12bbab5a0e131e0afe2fb57b5410b4f16"


async def authenticate() -> dict[str, Any]:  # noqa: C901 -- complete immutable authority boundary
    """Verify exact checkpoint bytes, source seal, reconstruction and native frame."""
    if any(
        (freeze.CASE / name).exists() for name in freeze.FORBIDDEN if name != "stage_b"
    ):
        raise ValueError("Unexpected root-level execution/gold artifact")
    await git("merge-base", "--is-ancestor", STAGE_A, "HEAD")
    prefix = "experiments/codex_dogfood/case_0013/"
    authoritative = json.loads(
        await git("show", STAGE_A + ":" + prefix + "integrity.json")
    )
    if read_json(freeze.CASE / "integrity.json") != authoritative:
        raise ValueError("Authoritative Stage A integrity differs")
    if set(authoritative["sha256"]) != {*freeze.GENERATED, *freeze.AUTHORED}:
        raise ValueError("Stage A seal coverage differs")
    for name, h in authoritative["sha256"].items():
        if (
            digest(binary(freeze.CASE / name)) != h
            or digest(await git("show", STAGE_A + ":" + prefix + name)) != h
        ):
            raise ValueError("Authoritative Stage A artifact differs: " + name)
    pre = read_json(freeze.CASE / "pre_execution.json")
    for name, h in pre["implementation_sha256"].items():
        if digest(binary(ROOT / name)) != h:
            raise ValueError("Sealed Stage A implementation differs: " + name)
    blobs = await freeze.committed_blobs()
    image = json.loads(gzip.decompress(binary(freeze.CASE / "inputs.json.gz")))
    frame = restore_frame(image)
    native, metadata = freeze.prepare_frame(blobs)
    if native != frame or metadata != image["metadata"]:
        raise ValueError("Stage A native frame reconstruction differs")
    rebuilt = await freeze.output(native, metadata, blobs)
    if any(binary(freeze.CASE / name) != raw for name, raw in rebuilt.items()):
        raise ValueError("Stage A deterministic reconstruction differs")
    t = protocol.definition()
    if set(t["execution"].values()) != {0} or t["gold"] != "ABSENT":
        raise ValueError("Frozen Stage A zero-execution/gold contract differs")
    return {
        "stage_a": STAGE_A,
        "authentication": "PASS",
        "frame": metadata,
        "initial_execution": t["execution"],
        "gold": "ABSENT",
    }
