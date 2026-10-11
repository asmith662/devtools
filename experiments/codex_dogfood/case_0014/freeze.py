# Copyright (c) 2026
# ruff: noqa: E501, EM101, TRY003, T201, COM812 -- explicit bounded scientific CLI
"""Freeze/replay native resource observation only; never build an index or score."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import json
import re
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_text,
)
from experiments.codex_dogfood.case_0014 import protocol

CASE = protocol.CASE
PACKAGE = ROOT / "experiments/query_term_weighting"
REPOSITORY = Repository(RepositoryId.parse("5cf96d9e-d6a5-44a6-83d3-1e24f6e00009"))
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
    "README.md",
    ".gitattributes",
)
FORBIDDEN = (
    "stage_b",
    "adjudication",
    "gold.json",
    "index.pkl",
    "index.pkl.gz",
    "results.json",
    "execution_started.json",
    "execution_completed.json",
    "costs.json",
    "analysis.json",
)
PRIOR_CASE = re.compile(rb"case[_ -]?00\d\d", re.IGNORECASE)


def eligible(path: str) -> bool:
    """Select broad whole resources without task/query signals or held-out reads."""
    if any(
        "confirmation" in p.casefold() or "reserve" in p.casefold()
        for p in path.split("/")
    ):
        return False
    return path in {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "scripts/validate_development.py",
    } or (
        path.startswith(("src/", "tests/", "docs/"))
        and Path(path).suffix in {".py", ".md", ".toml", ".yaml", ".yml"}
        and path != "docs/implementation_ledger.md"
        and not path.startswith(
            ("tests/experiments/", "docs/research/", "docs/reports/")
        )
    )


def implementation_files() -> tuple[Path, ...]:
    """Seal local implementations/tests, canonical source and external adapters."""
    return tuple(
        sorted(
            {
                *CASE.glob("*.py"),
                *PACKAGE.glob("*.py"),
                *PACKAGE.glob("*.md"),
                PACKAGE / "pytest.ini",
                PACKAGE / ".gitattributes",
                ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
                ROOT / "uv.lock",
                ROOT / "pyproject.toml",
                *(ROOT / p for p in protocol.SCORER["canonical_sources"]),
                *(ROOT / "src/devtools/context/repository").glob("*.py"),
                ROOT / "src/devtools/context/localization/identity.py",
                ROOT / "tests/context/retrieval/lexical/_helpers.py",
                *(ROOT / "src/devtools/resources/filesystem").rglob("*.py"),
                *(ROOT / "src/devtools/resources/commands").rglob("*.py"),
                *(ROOT / "src/devtools/core/paths").rglob("*.py"),
            }
        )
    )


async def committed_blobs() -> tuple[dict[str, bytes], list[str]]:
    """Archive path-filtered committed inputs; exclude prior-case whole resources."""
    tree = (
        (await git("ls-tree", "-r", "--name-only", protocol.START))
        .decode()
        .splitlines()
    )
    addresses = sorted(p for p in tree if eligible(p))
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
            if not member.isfile() or member.name not in addresses:
                raise ValueError("Unexpected committed archive entry")
            stream = bundle.extractfile(member)
            if stream is None:
                raise ValueError("Missing archive bytes")
            raw = stream.read()
            if PRIOR_CASE.search(raw):
                excluded.append(member.name)
            else:
                blobs[member.name] = raw
    if sorted([*blobs, *excluded]) != addresses:
        raise ValueError("Committed archive coverage differs")
    return dict(sorted(blobs.items())), sorted(excluded)


def frame(blobs: dict[str, bytes]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Observe native snapshot/corpus/document identities with zero lexical analysis."""
    with TemporaryDirectory(prefix="case0014-observation-") as temporary:
        root = Path(temporary)
        for address, raw in blobs.items():
            put_text(root / address, raw.decode("utf-8"))
        discovery = discover_repository_resource_addresses(
            repository=REPOSITORY,
            root=resolve_path(root),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        addresses = tuple(RepositoryResourceAddress(p) for p in sorted(blobs))
        snapshot = observe_repository_resources(
            repository=REPOSITORY,
            root=resolve_path(root),
            addresses=addresses,
            maximum_resource_bytes=1 << 20,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery, selected_addresses=addresses
            ),
            snapshot=snapshot,
        )
        documents = represent_repository_text_corpus(corpus=corpus)
        rows = [
            {
                "repository_id": str(REPOSITORY.id),
                "snapshot_id": str(snapshot.id),
                "corpus_id": str(corpus.id),
                "document_identity": str(d.id),
                "address": str(r.address),
                "content_identity": str(r.content_identity),
                "content": r.content,
                "encoding": r.encoding,
                "utf8_bytes": len(r.content.encode("utf-8")),
                "source_blob_sha256": digest(blobs[str(r.address)]),
            }
            for r, d in zip(snapshot.resources, documents.documents, strict=True)
        ]
        metadata = {
            "repository_id": str(REPOSITORY.id),
            "snapshot_id": str(snapshot.id),
            "corpus_id": str(corpus.id),
            "source_head": protocol.START,
            "resource_count": len(rows),
            "resource_order": "canonical resource address ascending",
            "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
            "resources": [{k: v for k, v in r.items() if k != "content"} for r in rows],
        }
    return metadata, rows


def no_execution(destination: Path) -> None:
    """Reject prospective execution artifacts; allow only reviewed Stage A names."""
    if any((destination / name).exists() for name in FORBIDDEN):
        raise ValueError("Prospective execution/gold forbidden at Stage A")
    allowed = {
        *GENERATED,
        *AUTHORED,
        *(p.name for p in CASE.glob("*.py")),
        "__pycache__",
        ".pytest_cache",
    }
    if destination.exists() and any(
        p.name not in allowed for p in destination.iterdir()
    ):
        raise ValueError("Unexpected Stage A artifact or execution file")


def render(title: str, design: dict[str, Any], metadata: dict[str, Any]) -> str:
    """Expose every frozen fact, term span, multiplier and exclusion without ranks."""
    parts = [
        f"# {title}\n\nR1.7 CURRENT; Stage B NOT EXECUTED; effectiveness UNKNOWN.\n\n"
    ]

    def section(name: str, value: object) -> None:
        parts.append(f"## {name}\n\n```json\n{json_bytes(value).decode()}```\n\n")

    parts.append("## Exact task\n\n" + str(design["task_text"]) + "\n")
    section(
        "Hypothesis and scientific boundary",
        {k: design[k] for k in ("hypothesis", "boundary")},
    )
    parts.append(
        "## Selection record\n\n" + binary(CASE / "SELECTION.md").decode() + "\n"
    )
    section(
        "Criteria frozen before authoring",
        json.loads(binary(CASE / "SELECTION_CRITERIA.json")),
    )
    section(
        "Existing canonical scorer and weighting equation", design["scorer_semantics"]
    )
    section(
        "Complete term roles, lexicon, multipliers and arms",
        {k: design[k] for k in ("taxonomy", "weights", "weight_rationale", "arms")},
    )
    parts.append(
        "## Requirement matrix\n\n| Requirement | Mandatory obligation | Query | Title |\n|---|---|---|---|\n"
    )
    parts.extend(
        f"| {row['requirement']} | {row['obligation']} | {row['query_identity']} | {row['title']} |\n"
        for row in design["requirement_matrix"]
    )
    parts.append(
        "\n## Every frozen query and analyzed term\n\nAll spans are half-open character offsets. Duplicate observations remain; distinct terms score once. Each term is scoped by its enclosing query/obligation identity.\n\n"
    )
    for query in design["queries"]:
        key = query["identity"]["value"]
        obligation = query["obligation"]["value"]
        source = query["source"]["span"]
        parts.append(
            f"### {key} / {obligation}\n\nExact query:\n\n```text\n{query['native_query']['text']}\n```\n\nTask clause [{source['start']}, {source['end']}):\n\n"
        )
        parts.append(str(design["task_text"])[source["start"] : source["end"]] + "\n")
        parts.append(
            "| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |\n|---|---|---|---:|---:|---:|---|\n"
        )
        for term in query["terms"]:
            spans = ", ".join(
                f"[{o['start']},{o['end']})={o['observed_text']}"
                for o in term["observations"]
            )
            a, b, c = term["multipliers"]
            parts.append(
                f"| `{term['analyzed_term']}` | {spans} | {term['role']} | {a} | {b} | {c} | {term['classification_provenance']} |\n"
            )
        parts.append(
            "\nLiteral copy provenance:\n\n```json\n"
            + json_bytes(query["anchors"]).decode()
            + "```\n\n"
        )
    section(
        "Whole-task canonical safety/reference lane", design["global_reference_lane"]
    )
    section(
        "Ranking/candidate safety, metrics and witness burden accounting",
        {
            k: design[k]
            for k in ("candidate_invariants", "metrics", "burden_accounting")
        },
    )
    section("Single-run cost accounting", design["cost_accounting"])
    section("Exact frozen decision rule and precedence", design["decision_rule"])
    section(
        "Failure attribution and exclusions",
        {
            k: design[k]
            for k in (
                "failure_taxonomy",
                "failure_definitions",
                "SEARCH_POLICY_FAILURE",
                "gold_policy",
                "execution_policy",
            )
        },
    )
    section(
        "Frozen native frame and resource eligibility",
        {
            "binding": {k: v for k, v in metadata.items() if k != "resources"},
            "policy": design["frame_policy"],
            "complete_identity_inventory": "frame.json; every resource binds repository/snapshot/corpus/document/address/content identity and source blob SHA-256; resources.json.gz retains exact whole content",
        },
    )
    section("No prospective execution", design["no_execution"])
    parts.append(
        "Maintainer reviews Stage A. Only after authorization execute the prospective lexical treatments once.\n"
    )
    return "".join(parts)


async def expected() -> dict[str, bytes]:
    """Reconstruct all prospective artifacts; observation and query analysis only."""
    await git("merge-base", "--is-ancestor", protocol.START, "HEAD")
    blobs, excluded = await committed_blobs()
    metadata, resources = frame(blobs)
    design = protocol.authored()
    design["frame_policy"] = {
        "path_eligibility": "Broad source/test/doc/config selection; no experiments, research/reports/ledger, held-out paths or operational files",
        "prior_case_leakage": "Exclude entire original resource if case[_ -]?00\\d\\d marker occurs, case-insensitive; never strip or rewrite text",
        "excluded_prior_case_resources": excluded,
        "task_query_independent": True,
    }
    trace = {
        "case": "0014",
        "protocol": design,
        "frame": metadata,
        "no_execution": protocol.COUNTS,
        "outcome": "NOT_EVALUATED",
    }
    values = {
        "resources.json.gz": gzip.compress(json_bytes(resources), mtime=0),
        "frame.json": json_bytes(metadata),
        "protocol.json": json_bytes(design),
        "trace.json": json_bytes(trace),
        "TRACE.md": render("Case 0014 prospective trace", design, metadata).encode(),
        "STAGE_A_REVIEW.md": render(
            "Case 0014 Stage A human review", design, metadata
        ).encode(),
        "validation.json": json_bytes(
            {
                "status": "PASS",
                "checks": [
                    "committed source frame reconstruction",
                    "exact native repository/snapshot/corpus/content/document identities",
                    "task/query-only classification replay",
                    "all terms and observations retained",
                    "positive frozen weights",
                    "three-arm isolation",
                    "unchanged canonical scorer contract",
                    "reference lane task identity",
                    "deterministic JSON/Markdown/gzip replay",
                    "zero prospective execution and gold absent",
                    "allowlisted future blind packet policy",
                    "implementation and authored artifact hashes",
                ],
                "no_execution": protocol.COUNTS,
            }
        ),
    }
    integrity = {
        "schema": "case-0014-stage-a-integrity-v1",
        "source_head": protocol.START,
        "runtime": {
            "python": list(sys.version_info[:3]),
            "implementation": sys.implementation.name,
        },
        "hash_scopes": "Exact gzip bytes; canonical UTF-8 LF text bytes; Git text eol=lf; .local and operational handoff excluded",
        "artifacts": {k: digest(v) for k, v in sorted(values.items())},
        "authored": {p: digest(binary(CASE / p)) for p in AUTHORED},
        "implementation": {
            p.relative_to(ROOT).as_posix(): digest(binary(p))
            for p in implementation_files()
        },
        "scientific_scope_excludes": [
            ".local/",
            "operational result handoff",
            "controlled fixture outputs",
            "publication timing",
        ],
        "no_execution": protocol.COUNTS,
    }
    values["integrity.json"] = json_bytes(integrity)
    return values


async def publish(destination: Path) -> None:
    """Refuse overwrite before observation; exclusively materialize Stage A."""
    no_execution(destination)
    if any((destination / p).exists() for p in GENERATED):
        raise FileExistsError("Refusing to overwrite frozen Stage A")
    values = await expected()
    for name, raw in values.items():
        if name.endswith(".gz"):
            put_binary(destination / name, raw)
        else:
            put_text(destination / name, raw.decode())


async def verify(destination: Path) -> None:
    """Reject any tamper by exact deterministic scientific reconstruction."""
    no_execution(destination)
    for name, raw in (await expected()).items():
        if binary(destination / name) != raw:
            raise ValueError("Stage A tamper/replay mismatch: " + name)


def main() -> None:
    """Run only Stage A publication or verification, never a treatment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    asyncio.run(verify(CASE) if args.verify else publish(CASE))
    print(
        "Case 0014 Stage A PASS; prospective index/query/scoring/ranking counts = 0; gold ABSENT"
    )


if __name__ == "__main__":
    main()
