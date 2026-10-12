# Copyright (c) 2026
# ruff: noqa: EM101, TRY003
"""Authenticate sealed Stage A independently of subsequently added stages."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    read_json,
)
from experiments.codex_dogfood.case_0016 import freeze, protocol

STAGE_A = "e05d9d08297496c4ff5a8e0be1084c4ce1c99a35"
PACKAGE = Path(__file__).resolve().parent
EXECUTION = "case-0016-stage-b-1"
CAPTURE = PACKAGE / "attempts" / EXECUTION
INTEGRITY = "c93c4594c3821211d3129f4fb9c19c41c2ccf035abb12f8de7c2025f0dbbf505"


def source_hashes() -> dict[str, str]:
    """Bind capture code and every explicitly reused capture substrate."""
    paths = {*PACKAGE.glob("*.py"), PACKAGE / "README.md"}
    for folder in ("case_0012/stage_b", "case_0015/stage_b"):
        paths.update((ROOT / "experiments/codex_dogfood" / folder).glob("*.py"))
    paths.update((ROOT / "experiments/bm25f").glob("*.py"))
    paths.add(ROOT / "experiments/codex_dogfood/case_0009/artifacts.py")
    return {p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(paths)}


async def authenticate() -> dict[str, Any]:
    """Verify physical/committed bytes, original ancestry and deterministic replay."""
    if digest(binary(freeze.CASE / "integrity.json")) != INTEGRITY:
        raise ValueError("Amended Stage A integrity differs")
    original = await freeze.authenticate_original()
    seal = read_json(freeze.CASE / "integrity.json")
    prefix = freeze.CASE.relative_to(ROOT).as_posix() + "/"
    files = {
        prefix + p: h
        for section in ("artifacts", "authored")
        for p, h in seal[section].items()
    }
    files.update(seal["implementation"])
    files.update(seal["historical_development"])
    files[prefix + "integrity.json"] = INTEGRITY
    semaphore = asyncio.Semaphore(4)

    async def check(path: str, sha: str) -> None:
        async with semaphore:
            raw = await git("show", STAGE_A + ":" + path)
        if digest(raw) != sha or digest(binary(ROOT / path)) != sha:
            raise ValueError("Stage A physical/committed seal mismatch: " + path)

    await asyncio.gather(*(check(p, h) for p, h in files.items()))
    for name, raw in (await freeze.expected()).items():
        if binary(freeze.CASE / name) != raw:
            raise ValueError("Stage A deterministic replay differs: " + name)
    trace = read_json(freeze.CASE / "trace.json")
    if (
        seal["no_execution"] != protocol.COUNTS
        or trace["no_execution"] != protocol.COUNTS
    ):
        raise ValueError("Frozen initial prospective counters differ")
    frame = read_json(freeze.CASE / "frame.json")
    return {
        "stage_a": STAGE_A,
        "original_stage_a": protocol.PRIOR_STAGE_A,
        "original_integrity_sha256": protocol.PRIOR_INTEGRITY_SHA256,
        "original_authenticated_files": original["authenticated_files"],
        "amended_authenticated_files": len(files),
        "amended_integrity_sha256": INTEGRITY,
        "protocol_sha256": digest(binary(freeze.CASE / "protocol.json")),
        "frame": {k: frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")},
        "initial_counts": protocol.COUNTS,
        "deterministic_stage_a_replay": "PASS",
    }
