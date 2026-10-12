# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, S301
"""Authenticate immutable engineering inputs, without scientific replay or gold."""

from __future__ import annotations

import asyncio
import gzip
import hashlib
import io
import json
import pickle
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from experiments.codex_dogfood.case_0009.artifacts import ROOT, git
from experiments.codex_dogfood.case_0012.stage_b.durability import unpack

CASE = ROOT / "experiments/codex_dogfood/case_0016"
CAPTURE = CASE / "stage_b/attempts/case-0016-stage-b-2"
CHECKPOINT = "ba1c51037d7d0a255e4e2c3c2476a3a37470d6cf"
SEAL = "b94bcd6dd1b7b0be12b487da70041c1f72b05fa2aa8234c589ad6b9829d734b0"
RETURN_COUNT = 464


def sha(raw: bytes) -> str:
    """Hash physical bytes at this explicit sealed artifact boundary."""
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path) -> Any:
    """Decode an authenticated case-local binary artifact, preserving order."""
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def authenticate() -> dict[str, str]:
    """Check trusted manifest and workload files before any native unpickling."""
    if sha((CAPTURE / "integrity.json").read_bytes()) != SEAL:
        raise ValueError("Authoritative attempt-2 manifest differs")
    seal = read_json(CAPTURE / "integrity.json")
    hashes = {}
    for name, expected in seal["sha256"].items():
        path = CAPTURE / name
        if not path.resolve().is_relative_to(CAPTURE.resolve()):
            raise ValueError("Manifest path escapes capture")
        actual = sha(path.read_bytes())
        if actual != expected:
            raise ValueError("Input tamper: " + name)
        hashes[name] = actual
    for name in ("resources.json.gz", "frame.json", "protocol.json"):
        raw = (CASE / name).read_bytes()
        committed = asyncio.run(
            git("show", CHECKPOINT + ":" + (CASE / name).relative_to(ROOT).as_posix()),
        )
        if raw != committed:
            raise ValueError("Committed frame/protocol mismatch: " + name)
        hashes["stage_a/" + name] = sha(raw)
    return hashes


def native_inputs() -> dict[str, Any]:
    """Load trusted shared-memo native returns, omitting canonical re-encoding.

    authenticate() must run first. Each native compressed segment is also checked
    by the existing unpack primitive. This is an engineering workload adapter,
    not a substitute for the completed scientific Journal.load validation.
    """
    stream = io.BytesIO()
    context = read_json(CAPTURE / "native_context.json")
    stream.write(unpack(context["native"]))
    records = [
        read_json(path)
        for path in sorted((CAPTURE / "operations").glob("*.returned.json"))
    ]
    if len(records) != RETURN_COUNT:
        raise ValueError("Expected 464 authoritative native returns")
    for record in records:
        stream.write(unpack(record["native"]))
    stream.seek(0)
    loader = pickle.Unpickler(stream)
    values = loader.load()
    for record in records:
        identity, value = loader.load()
        if identity != record["operation"]["identity"]:
            raise ValueError("Native segment identity mismatch")
        values[identity] = value
    return cast("dict[str, Any]", values)
