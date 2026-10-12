# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, T201, COM812, E501
"""Graph-3 Stage A observation/seal/replay only; no treatment entry point."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import json
import tarfile
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
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
    "AMENDMENT.md",
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
            "\n\n## Prospective amendment\n\n",
            binary(CASE / "AMENDMENT.md").decode(),
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
    original = await authenticate_original()
    require_unchanged_contract(original["protocol"], design)
    if (
        digest(json_bytes(metadata)) != original["seal"]["artifacts"]["frame.json"]
        or digest(gzip.compress(json_bytes(resources), mtime=0))
        != original["seal"]["artifacts"]["resources.json.gz"]
    ):
        raise ValueError("Amendment changed frozen frame/resources")
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
        "original Stage A seal and all committed blob identities",
        "restricted prospective contract amendment; unchanged task/frame/RI/seeds/PPR/RRF/gates",
        "flow-only B membership/ranking/fusion, full stationary accounting, definition-flow sums",
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
            "prior_stage_a_checkpoint": protocol.PRIOR_STAGE_A,
            "prior_integrity_sha256": protocol.PRIOR_INTEGRITY_SHA256,
            "original_stage_a_authenticated_files": original["authenticated_files"],
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


async def authenticate_original() -> dict[str, Any]:
    """Authenticate original Git seal/inputs without any treatment operation."""
    await git("merge-base", "--is-ancestor", protocol.PRIOR_STAGE_A, "HEAD")
    prefix = "experiments/codex_dogfood/case_0016/"
    raw = await git("show", protocol.PRIOR_STAGE_A + ":" + prefix + "integrity.json")
    if digest(raw) != protocol.PRIOR_INTEGRITY_SHA256:
        raise ValueError("Original Stage A integrity hash mismatch")
    seal = json.loads(raw)
    expected_files = {
        prefix + p: h
        for section in ("artifacts", "authored")
        for p, h in seal[section].items()
    }
    expected_files.update(seal["implementation"])
    expected_files.update(seal["historical_development"])
    semaphore = asyncio.Semaphore(4)

    async def check(path: str, sha: str) -> None:
        async with semaphore:
            data = await git("show", protocol.PRIOR_STAGE_A + ":" + path)
        if digest(data) != sha:
            raise ValueError("Original sealed blob mismatch: " + path)
        # All reused native code, gates, view, seed policy and historical sources
        # remain byte-identical. Only authorized experiment consumers may change.
        unchanged = not path.startswith(
            (prefix, "experiments/task_conditioned_graph/")
        ) or path.endswith(("/gates.py", "/view.py", "/seeds.py"))
        if unchanged and digest(binary(ROOT / path)) != sha:
            raise ValueError("Unchanged implementation changed: " + path)

    await asyncio.gather(*(check(p, h) for p, h in expected_files.items()))
    original_protocol = json.loads(
        await git("show", protocol.PRIOR_STAGE_A + ":" + prefix + "protocol.json")
    )
    original_trace = json.loads(
        await git("show", protocol.PRIOR_STAGE_A + ":" + prefix + "trace.json")
    )
    if (
        original_trace["no_execution"] != protocol.COUNTS
        or seal["no_execution"] != protocol.COUNTS
    ):
        raise ValueError("Original Stage A is not unexecuted")
    for name in (
        "task.txt",
        "SELECTION.md",
        "SELECTION_CRITERIA.json",
        "AUDIT.md",
        ".gitattributes",
    ):
        if digest(binary(CASE / name)) != seal["authored"][name]:
            raise ValueError("Immutable authored input changed: " + name)
    return {
        "seal": seal,
        "protocol": original_protocol,
        "authenticated_files": len(expected_files) + 1,
    }


def require_unchanged_contract(
    original: dict[str, Any], amended: dict[str, Any]
) -> None:
    """Allow only the expressly authorized ranking/diagnostic clarification."""
    before = json.loads(json_bytes(original))
    after = json.loads(json_bytes(amended))
    after.pop("prospective_amendment")
    for value in (before, after):
        value["arms"].pop("B")
        value["pagerank"].pop("result")
        value["pagerank"].pop("trace")
        value.pop("definition_projection")
        value["map_diagnostic"].pop("budget")
        value.pop("attribution_policy")
        value["decision_rule"].pop("implementation_checks")
    if before != after:
        raise ValueError("Unauthorized prospective contract change")


async def amend(destination: Path) -> None:
    """Replace only original unexecuted artifacts once, preserving immutable bytes."""
    no_execution(destination)
    original = await authenticate_original()
    for name, sha in original["seal"]["artifacts"].items():
        if digest(binary(destination / name)) != sha:
            raise ValueError("Refusing amendment overwrite of non-original artifacts")
    if (
        digest(binary(destination / "integrity.json"))
        != protocol.PRIOR_INTEGRITY_SHA256
    ):
        raise ValueError("Refusing amendment overwrite of non-original seal")
    values = await expected()
    for name, raw in values.items():
        if name in {"frame.json", "resources.json.gz"}:
            if binary(destination / name) != raw:
                raise ValueError("Immutable frame/resources changed")
            continue
        write(TextFile(resolve_path(destination / name), raw.decode()), overwrite=True)


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
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--verify", action="store_true")
    actions.add_argument("--amend", action="store_true")
    args = parser.parse_args()
    asyncio.run(
        verify(CASE) if args.verify else amend(CASE) if args.amend else publish(CASE)
    )
    print("Case 0016 Graph-3 Stage A PASS; prospective execution counts=0; gold ABSENT")


if __name__ == "__main__":
    main()
