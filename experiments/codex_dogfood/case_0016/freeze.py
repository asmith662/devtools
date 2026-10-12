# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, T201, COM812, E501
"""Graph-3 Stage A observation/seal/replay only; no treatment entry point."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import tarfile
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_text,
)
from experiments.codex_dogfood.case_0015.freeze import PRIOR_CASE, eligible, frame
from experiments.codex_dogfood.case_0016 import protocol

CASE = protocol.CASE
if TYPE_CHECKING:
    from pathlib import Path
GENERATED = (
    "resources.json.gz",
    "frame.json",
    "protocol.json",
    "trace.json",
    "TRACE.md",
    "STAGE_A_REVIEW.md",
    "validation.json",
    "integrity.json",
)
AUTHORED = (
    "task.txt",
    "SELECTION.md",
    "SELECTION_CRITERIA.json",
    "AUDIT.md",
    "README.md",
    ".gitattributes",
)


def no_execution(destination: Path) -> None:
    """Enforce a closed Stage A allowlist without execution files or gold."""
    allowed = {
        *GENERATED,
        *AUTHORED,
        "__init__.py",
        "protocol.py",
        "freeze.py",
        "blind.py",
        "test_freeze.py",
    }
    if destination.exists():
        for path in destination.iterdir():
            if path.name in {"__pycache__", ".pytest_cache"} and path.is_dir():
                continue
            if not path.is_file() or path.name not in allowed:
                raise ValueError("Unexpected prospective artifact: " + path.name)


def implementation_files() -> tuple[Path, ...]:
    """Seal experiment and its reused native dependencies, never operational data."""
    return tuple(
        sorted(
            {
                *CASE.glob("*.py"),
                *protocol.PACKAGE.glob("*.py"),
                protocol.PACKAGE / "README.md",
                protocol.PACKAGE / "pytest.ini",
                protocol.PACKAGE / ".gitattributes",
                ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
                ROOT / "experiments/codex_dogfood/case_0015/freeze.py",
                ROOT / "experiments/codex_dogfood/case_0015/protocol.py",
                ROOT / "uv.lock",
                ROOT / "pyproject.toml",
                ROOT / "tests/context/retrieval/test_structural.py",
                ROOT / "tests/context/retrieval/test_composition.py",
                *(ROOT / "src/devtools/context").rglob("*.py"),
                *(ROOT / "src/devtools/resources/filesystem").rglob("*.py"),
                *(ROOT / "src/devtools/resources/commands").rglob("*.py"),
                *(ROOT / "src/devtools/core/paths").rglob("*.py"),
            }
        )
    )


async def committed_inputs() -> tuple[dict[str, bytes], list[str]]:
    """Archive broad eligible committed content, never inspect graph facts/ranks."""
    tree = (
        (await git("ls-tree", "-r", "--name-only", protocol.START))
        .decode()
        .splitlines()
    )
    addresses = sorted(path for path in tree if eligible(path))
    archive = await git(
        "-c",
        "core.autocrlf=false",
        "archive",
        "--format=tar",
        protocol.START,
        "--",
        *addresses,
    )
    blobs: dict[str, bytes] = {}
    excluded = []
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            stream = bundle.extractfile(member)
            if not member.isfile() or member.name not in addresses or stream is None:
                raise ValueError("Unexpected committed archive member")
            raw = stream.read()
            if PRIOR_CASE.search(raw):
                excluded.append(member.name)
            else:
                blobs[member.name] = raw
    if sorted([*blobs, *excluded]) != addresses:
        raise ValueError("Committed source coverage mismatch")
    return dict(sorted(blobs.items())), sorted(excluded)


def render(design: dict[str, Any], metadata: dict[str, Any]) -> str:
    """Expose complete task, audit and protocol without prospective execution."""
    return "".join(
        [
            "# Case 0016 Graph-3 Stage A review\n\nStage B NOT EXECUTED; gold ABSENT; effectiveness NOT_EVALUATED.\n\n",
            binary(CASE / "AUDIT.md").decode(),
            "\n\n## Selection\n\n",
            binary(CASE / "SELECTION.md").decode(),
            "\n\n## Frozen selection criteria\n\n```json\n",
            binary(CASE / "SELECTION_CRITERIA.json").decode(),
            "```\n\n## Exact task\n\n",
            design["task_text"],
            *[
                "\n\n## "
                + key.replace("_", " ")
                + "\n\n```json\n"
                + json_bytes(value).decode()
                + "```\n"
                for key, value in design.items()
                if key != "task_text"
            ],
            "\n## Frozen native frame\n\n```json\n",
            json_bytes(
                {k: v for k, v in metadata.items() if k != "resources"}
            ).decode(),
            "```\n\n",
            "All resource identities: frame.json; exact retained contents: resources.json.gz. No prospective RI reference derivation, graph, exact resolution, lexical retrieval, rank, candidate result, map or gold was produced. Synthetic fixtures are separate and contain no Case 0016 resources.\n\n",
            "Maintainer reviews frozen Case 0016 Graph-3 Stage A. Then separately execute canonical BM25, task-conditioned reference PPR and frozen RRF prospectively exactly once. STOP before Stage B now.\n",
        ]
    )


async def expected() -> dict[str, bytes]:
    """Recreate native observation and deterministic scientific artifacts only."""
    await git("merge-base", "--is-ancestor", protocol.START, "HEAD")
    blobs, excluded = await committed_inputs()
    metadata, resources = frame(blobs)  # Reuse native observation, never retrieval.
    if any(
        row["content"] != blobs[row["address"]].decode("utf-8") for row in resources
    ):
        raise ValueError("Native observation changed committed source text")
    metadata["source_head"] = protocol.START
    design = protocol.authored()
    design["frame_policy"] = {
        "eligibility": "Broad committed source/test/docs/config; exclude experiments, tests/experiments, research/reports/ledger, held-out/operational paths before content reads",
        "prior_case_text": "Exclude whole resource containing case[_ -]?00\\d\\d marker; never strip natural content",
        "excluded_prior_case_resources": excluded,
        "task_query_independent": True,
    }
    trace = {
        "case": "0016",
        "source_head": protocol.START,
        "frame": metadata,
        "protocol": design,
        "no_execution": protocol.COUNTS,
        "scope": "Stage A observation only; synthetic fixture execution segregated",
        "outcome": "NOT_EVALUATED",
    }
    checks = [
        "source checkpoint ancestry",
        "committed native snapshot/corpus/content/document identities",
        "six mandatory task clauses and exact shared queries",
        "audit/gap ownership and selection provenance",
        "reference-only sqrt projection and fixed uniform seeds/PPR/RRF contracts",
        "exact frozen gates and blind input allowlist",
        "implementation and authored seals",
        "deterministic JSON/Markdown/gzip byte replay",
        "closed no-execution allowlist and gold absence",
    ]
    values = {
        "resources.json.gz": gzip.compress(json_bytes(resources), mtime=0),
        "frame.json": json_bytes(metadata),
        "protocol.json": json_bytes(design),
        "trace.json": json_bytes(trace),
        "TRACE.md": render(design, metadata).encode(),
        "STAGE_A_REVIEW.md": render(design, metadata).encode(),
        "validation.json": json_bytes(
            {"status": "PASS", "checks": checks, "no_execution": protocol.COUNTS}
        ),
    }
    historical = [
        f"experiments/increment_{i}/graph_round_{word}_{suffix}"
        for i, word in ((32, "one"), (33, "two"))
        for suffix in ("development_results.json", "freeze.json")
    ]
    historical += [
        "experiments/increment_32/README.md",
        "experiments/increment_33/README.md",
    ]
    values["integrity.json"] = json_bytes(
        {
            "schema": "case-0016-graph3-stage-a-integrity-v1",
            "source_head": protocol.START,
            "artifacts": {k: digest(v) for k, v in sorted(values.items())},
            "authored": {p: digest(binary(CASE / p)) for p in AUTHORED},
            "implementation": {
                p.relative_to(ROOT).as_posix(): digest(binary(p))
                for p in implementation_files()
            },
            "historical_development": {p: digest(binary(ROOT / p)) for p in historical},
            "hash_scope": "Exact deterministic gzip and UTF-8 LF text bytes, Git eol=lf; integrity excludes its own self hash",
            "excluded": [
                ".local",
                "operational handoff",
                "synthetic fixture outputs",
                "timings",
            ],
            "no_execution": protocol.COUNTS,
        }
    )
    return values


async def publish(destination: Path) -> None:
    """Refuse overwrite before reading committed frame input."""
    no_execution(destination)
    if any((destination / name).exists() for name in GENERATED):
        raise FileExistsError("Refusing overwrite of frozen Graph-3 Stage A")
    for name, raw in (await expected()).items():
        if name.endswith(".gz"):
            put_binary(destination / name, raw)
        else:
            put_text(destination / name, raw.decode())


async def verify(destination: Path) -> None:
    """Reject modified scientific artifacts or unexpected execution artifacts."""
    no_execution(destination)
    for name, raw in (await expected()).items():
        if binary(destination / name) != raw:
            raise ValueError("Stage A tamper/replay mismatch: " + name)


def main() -> None:
    """Stage A CLI has no retrieval execution path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    asyncio.run(verify(CASE) if args.verify else publish(CASE))
    print("Case 0016 Graph-3 Stage A PASS; prospective execution counts=0; gold ABSENT")


if __name__ == "__main__":
    main()
