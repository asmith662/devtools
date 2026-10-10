# Copyright (c) 2026
# ruff: noqa: COM812, E501, FBT001, EM101, TRY003, T201 -- literal seals and CLI validation; formatter owns commas
"""One-shot prospective Stage A publication and no-execution deterministic replay."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import json
import sys
import tarfile
import unicodedata
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import eligible
from experiments.codex_dogfood.case_0012.freeze import (
    frame_resources,
    restore_frame,
    shape,
)
from experiments.codex_dogfood.case_0012.freeze import (
    prepare_frame as prepare_native_frame,
)
from experiments.codex_dogfood.case_0013 import protocol, reporting

if TYPE_CHECKING:
    from pathlib import Path

    from experiments.exact_hint_routing.routing import ExactFrame

CASE = protocol.CASE
PACKAGE = ROOT / "experiments/mechanism_routing"
GENERATED = (
    "inputs.json.gz",
    "resources.json.gz",
    "frame.json",
    "treatment.json",
    "trace.json",
    "TRACE.md",
    "STAGE_A_REVIEW.md",
    "TASK_REQUIREMENT_MATRIX.md",
    "trace.schema.json",
    "pre_execution.json",
)
AUTHORED = (
    "task.txt",
    "SELECTION.md",
    "README.md",
    "STAGE_C_PROTOCOL.md",
    ".gitattributes",
)
FORBIDDEN = (
    "execution_started.json",
    "results.json",
    "results.json.gz",
    "costs.json",
    "stage_b",
    "stage_b_integrity.json",
    "STAGE_B_REVIEW.md",
    "adjudication",
    "blind_packet",
    "gold.json",
)


def require(condition: bool, message: str) -> None:
    """Fail closed on a broken freeze or scientific contract."""
    if not condition:
        raise ValueError(message)


def implementation_files() -> tuple[Path, ...]:
    """Pin executable policy, controlled tests, inventory and reused substrates."""
    return tuple(
        sorted(
            {
                *CASE.glob("*.py"),
                CASE / "pytest.ini",
                *PACKAGE.rglob("*.py"),
                PACKAGE / "README.md",
                PACKAGE / "CAPABILITIES.md",
                PACKAGE / "pytest.ini",
                PACKAGE / ".gitattributes",
                *(ROOT / "experiments/exact_hint_routing").rglob("*.py"),
                ROOT / "experiments/exact_hint_routing/CAPABILITIES.md",
                ROOT / "experiments/codex_dogfood/acquisition/needs.py",
                ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
                ROOT / "experiments/codex_dogfood/case_0009/freeze.py",
                ROOT / "experiments/codex_dogfood/case_0012/freeze.py",
                ROOT / "experiments/codex_dogfood/case_0012/protocol.py",
                ROOT / "experiments/codex_dogfood/case_0012/blind.py",
            }
        )
    )


async def committed_blobs() -> dict[str, bytes]:
    """Read broad eligible committed bytes without task-directed acquisition."""
    tree = (
        (await git("ls-tree", "-r", "--name-only", protocol.START))
        .decode()
        .splitlines()
    )
    addresses = tuple(sorted(p for p in tree if eligible(p)))
    require(
        all(not p.startswith(("experiments/", ".local/")) for p in addresses),
        "Contaminated resource frame",
    )
    archive = await git(
        "-c",
        "core.autocrlf=false",
        "archive",
        "--format=tar",
        protocol.START,
        "--",
        *addresses,
    )
    blobs = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            require(
                member.isfile() and member.name in addresses, "Unexpected archive entry"
            )
            stream = bundle.extractfile(member)
            if stream is None:
                raise ValueError("Missing archive bytes")
            require(member.name not in blobs, "Duplicate archive resource")
            blobs[member.name] = stream.read()
    require(tuple(sorted(blobs)) == addresses, "Missing committed resource")
    return blobs


def prepare_frame(blobs: dict[str, bytes]) -> tuple[ExactFrame, dict[str, Any]]:
    """Reuse address-only native preparation; change only this case's Git origin."""
    frame, metadata = prepare_native_frame(blobs)
    metadata["source_head"] = protocol.START
    return frame, metadata


def artifacts(
    frame: ExactFrame, metadata: dict[str, Any], blobs: dict[str, bytes]
) -> dict[str, bytes]:
    """Reconstruct every public artifact without retrieval or exact resolution."""
    treatment = protocol.definition()
    trace = {
        "schema": "case-0013-stage-a-trace-v1",
        "stage": "STAGE_A",
        "treatment": treatment,
        "frame": metadata,
        "execution": treatment["execution"],
        "results": "ABSENT",
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
    }
    review = reporting.review(treatment, metadata)
    review += (
        "\n## Available mechanism inventory\n\n"
        + binary(PACKAGE / "CAPABILITIES.md").decode()
    )
    resources = frame_resources(frame)
    implementation = {
        p.relative_to(ROOT).as_posix(): digest(binary(p))
        for p in implementation_files()
    }
    implementation.update(
        {
            p: digest(raw)
            for p, raw in blobs.items()
            if p.startswith("src/") and p.endswith(".py")
        }
    )
    pre = {
        "schema": "case-0013-stage-a-pre-execution-v1",
        "source_head": protocol.START,
        "git_blob_sha256": {p: digest(raw) for p, raw in blobs.items()},
        "implementation_sha256": implementation,
        "frame_identity": frame.identity,
        "task_sha256": treatment["task_sha256"],
        "execution": treatment["execution"],
        "stage_b": "NOT_EXECUTED",
        "gold": "ABSENT",
        "python_runtime": sys.version,
        "unicode_version": unicodedata.unidata_version,
        "lock_sha256": None,
        "hash_scope": "canonical UTF-8 LF text, exact gzip; committed blob digests exact; operational .local excluded",
    }
    # uv.lock is not an acquisition resource; its runtime seal is set by build/verify.
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": trace["schema"],
        **shape(trace),
    }
    schema["properties"]["execution"] = {"const": treatment["execution"]}
    schema["properties"]["results"] = {"const": "ABSENT"}
    schema["properties"]["gold"] = {"const": "ABSENT"}
    return {
        "inputs.json.gz": gzip.compress(
            json_bytes({"metadata": metadata, "resources": resources}), mtime=0
        ),
        "resources.json.gz": gzip.compress(
            json_bytes({"resources": resources}), mtime=0
        ),
        "frame.json": json_bytes(metadata),
        "treatment.json": json_bytes(treatment),
        "trace.json": json_bytes(trace),
        "TRACE.md": review.encode(),
        "STAGE_A_REVIEW.md": review.encode(),
        "TASK_REQUIREMENT_MATRIX.md": reporting.matrix(treatment).encode(),
        "trace.schema.json": json_bytes(schema),
        "pre_execution.json": json_bytes(pre),
    }


async def output(
    frame: ExactFrame, metadata: dict[str, Any], blobs: dict[str, bytes]
) -> dict[str, bytes]:
    """Seal runtime configuration without adding it to task-relative resources."""
    result = artifacts(frame, metadata, blobs)
    pre = json.loads(result["pre_execution.json"])
    pre["lock_sha256"] = digest(await git("show", protocol.START + ":uv.lock"))
    result["pre_execution.json"] = json_bytes(pre)
    return result


def publish(values: dict[str, bytes], root: Path = CASE) -> None:
    """Refuse complete/partial overwrite before writing any scientific file."""
    require(set(values) == set(GENERATED), "Publication coverage differs")
    require(
        not any(
            (root / n).exists() for n in (*GENERATED, "integrity.json", *FORBIDDEN)
        ),
        "Stage A overwrite/execution refused",
    )
    for name, raw in values.items():
        if name.endswith(".gz"):
            put_binary(root / name, raw)
        else:
            put_text(root / name, raw.decode())
    hashes = {n: digest(raw) for n, raw in values.items()}
    hashes.update({n: digest(binary(root / n)) for n in AUTHORED})
    put_text(
        root / "integrity.json",
        json_bytes(
            {
                "schema": "case-0013-stage-a-integrity-v1",
                "sha256": hashes,
                "scope": "canonical UTF-8 LF text; exact gzip; operational handoff excluded",
            }
        ).decode(),
    )


async def verify(root: Path = CASE) -> dict[str, Any]:
    """Authenticate hashes, complete reconstruction and zero-execution contract."""
    require(
        not any((root / n).exists() for n in FORBIDDEN),
        "Unexpected execution/gold artifact",
    )
    seal = read_json(root / "integrity.json")
    require(set(seal["sha256"]) == {*GENERATED, *AUTHORED}, "Seal coverage differs")
    require(
        all(digest(binary(root / n)) == h for n, h in seal["sha256"].items()),
        "Stage A artifact hash differs",
    )
    blobs = await committed_blobs()
    image = json.loads(gzip.decompress(binary(root / "inputs.json.gz")))
    frame = restore_frame(image)
    native, metadata = prepare_frame(blobs)
    require(
        native == frame and metadata == image["metadata"],
        "Native committed frame differs",
    )
    rebuilt = await output(native, metadata, blobs)
    require(
        all(binary(root / n) == raw for n, raw in rebuilt.items()),
        "Deterministic Stage A replay differs",
    )
    require(
        all(binary(root / n) == binary(CASE / n) for n in AUTHORED),
        "Authored source differs",
    )
    require(
        set(protocol.definition()["execution"].values()) == {0}, "Execution occurred"
    )
    await git("merge-base", "--is-ancestor", protocol.START, "HEAD")
    return {
        "stage_a": "FROZEN",
        "replay": "PASSED",
        "resources": len(frame.snapshot.resources),
        "obligations": len(protocol.OBLIGATIONS),
        "hints": len(protocol.HINTS),
        "execution": protocol.definition()["execution"],
        "gold": "ABSENT",
        "stage_b": "NOT_EXECUTED",
    }


async def build() -> dict[str, Any]:
    """Freeze task authoring before broad observation on the expected parent."""
    require(
        not any(
            (CASE / n).exists() for n in (*GENERATED, "integrity.json", *FORBIDDEN)
        ),
        "Stage A overwrite/execution refused",
    )
    require(
        (await git("rev-parse", "HEAD")).decode().strip() == protocol.START,
        "Unexpected parent HEAD",
    )
    require(
        (await git("branch", "--show-current")).decode().strip() == "main",
        "Expected main",
    )
    require(
        not await git(
            "diff",
            protocol.START,
            "--name-only",
            "--",
            "src",
            "tests",
            "pyproject.toml",
            "uv.lock",
        ),
        "Production inputs changed",
    )
    protocol.definition()
    blobs = await committed_blobs()
    frame, metadata = prepare_frame(blobs)
    values = await output(frame, metadata, blobs)
    require(values == await output(frame, metadata, blobs), "Nondeterministic Stage A")
    publish(values)
    return await verify()


def main() -> None:
    """Expose build/replay only, never prospective treatment execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    operation = parser.parse_args().operation
    print(asyncio.run(build() if operation == "build" else verify()))


if __name__ == "__main__":
    main()
