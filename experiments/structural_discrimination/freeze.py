# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, EM101, TRY003, E501 -- bounded codec and exact authored clauses
"""Publish/replay the prospective cohort without any treatment or holdout read."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import json
import platform
import re
import tarfile
from pathlib import Path
from typing import Any

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_text,
)
from experiments.structural_discrimination.cases import CASES
from experiments.structural_discrimination.frames import (
    POPULATION_SHA,
    SEED,
    START,
    observe,
    public_cards,
)
from experiments.structural_discrimination.protocol import EVIDENCE_SCHEMA, PROTOCOL

PACKAGE = Path(__file__).resolve().parent
PREFIX = "experiments/structural_discrimination/"
NO_EXECUTION = dict.fromkeys(
    (
        "bm25",
        "exact_lookup",
        "reference_derivation",
        "structural_annotation",
        "local_pairs",
        "pagerank",
        "rrf",
        "semantic_reviewer",
        "gold",
    ),
    0,
)


def implementations() -> dict[str, str]:
    """Bind exact local design and canonical evaluator/observation/proof sources."""
    paths = {
        *PACKAGE.glob("*.py"),
        PACKAGE / "README.md",
        PACKAGE / ".gitattributes",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
        ROOT / "experiments/codex_dogfood/case_0015/freeze.py",
        ROOT / "experiments/codex_dogfood/case_0015/protocol.py",
        *(ROOT / "experiments/codex_dogfood/verification").glob("*.py"),
        *(ROOT / "src/devtools/context").rglob("*.py"),
        *(ROOT / "src/devtools/core").rglob("*.py"),
        *(ROOT / "src/devtools/resources/commands").rglob("*.py"),
        *(ROOT / "src/devtools/resources/filesystem").rglob("*.py"),
    }
    return {p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(paths)}


def validate_design(card: Any, authored: Any, metadata: Any, rows: Any) -> None:
    """Check identity/basis/query/obligation bindings without semantic outcomes."""
    if (
        authored["task_text"] != card["task_text"]
        or authored["population_case"] != card["case_id"]
    ):
        raise ValueError("Task/case binding differs")
    if (
        metadata["source_head"] != card["frame"]["parent_commit"]
        or metadata["source_tree"] != card["frame"]["parent_tree"]
    ):
        raise ValueError("Parent binding differs")
    resources = {r["address"]: r for r in rows}
    if len(resources) != len(rows) or len(rows) != metadata["resource_count"]:
        raise ValueError("Resource completeness differs")
    if not set(authored["authoring_basis"]) <= resources.keys():
        raise ValueError("Authoring basis absent from own parent")
    obligations = authored["obligations"]
    if [o["id"] for o in obligations] != ["O1", "O2", "O3"]:
        raise ValueError("Minimum obligation frame differs")
    for obligation in obligations:
        if any(
            not obligation[k].strip()
            for k in (
                "requirement",
                "facts_to_discover",
                "satisfaction",
                "excluded_interpretation",
                "need",
                "query",
            )
        ):
            raise ValueError("Incomplete obligation/need/query")
        # No task contains an exact path/identifier locator. Plain natural words
        # avoid accidental child/helper names, and remain independently authored.
        if re.search(r"[\\/]|\.py\b|\b\w+_\w+\b", obligation["query"]):
            raise ValueError("Query contains an unauthored implementation locator")


def case_record(case: str, card: Any, metadata: Any, rows: Any) -> Any:
    """Separate task, predicate, need, query and later retrieval action."""
    authored = CASES[case]
    validate_design(card, authored, metadata, rows)
    task = LocalizationTaskIdentity(f"case-{case}:" + card["case_id"])
    provenance = TaskProvenance(
        card["task_source"]["task_sha256"],
        TaskTextSpan(0, len(card["task_text"].rstrip("\n"))),
        "Exact original commit message; minimum predicates interpreted from own parent only",
    )
    obligations = []
    for position, obligation in enumerate(authored["obligations"], 1):
        oid = LocalizationObligationIdentity(task, obligation["id"])
        qid = LocalizationQueryIdentity(task, f"Q{position}")
        obligations.append(
            {
                **obligation,
                "obligation_identity": {"task": oid.task.value, "value": oid.value},
                "query_identity": {"task": qid.task.value, "value": qid.value},
                "query_association": oid.value,
                "information_need_identity": f"N{position}",
                "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
                "task_backed_source_span": {
                    "start": provenance.span.start,
                    "end": provenance.span.end,
                }
                if provenance.span
                else None,
                "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text",
                "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
            }
        )
    by_address = {r["address"]: r for r in rows}
    return {
        "schema": "direct-structural-discrimination-case-stage-a-v1",
        "case_id": "case-" + case,
        "population_case_id": card["case_id"],
        "public_task_card": card,
        "task_identity": task.value,
        "task_text": card["task_text"],
        "task_provenance": {
            "source_sha256": provenance.source_identity,
            "explanation": provenance.explanation,
        },
        "parent_frame": {k: v for k, v in metadata.items() if k != "resources"},
        "authoring_basis_sha256": {
            p: by_address[p]["source_blob_sha256"] for p in authored["authoring_basis"]
        },
        "interpretation_gaps": authored["interpretation_gaps"],
        "ambiguities": authored["ambiguities"],
        "obligations": obligations,
        "shared_protocol_sha256": digest(json_bytes(PROTOCOL)),
        "exact_route": "NOT_APPLICABLE",
        "status": PROTOCOL["status"],
        "no_execution": NO_EXECUTION,
    }


def blind_record(record: Any) -> Any:
    """Freeze a semantic input allowlist, excluding acquisition/evidence hints."""
    return {
        "schema": "direct-discrimination-future-blind-spec-v1",
        "case_id": record["case_id"],
        "task_identity": record["task_identity"],
        "task_text": record["task_text"],
        "parent_frame": record["parent_frame"],
        "interpretation_gaps": record["interpretation_gaps"],
        "ambiguities": record["ambiguities"],
        "obligations": [
            {
                k: o[k]
                for k in (
                    "id",
                    "requirement",
                    "satisfaction",
                    "excluded_interpretation",
                    "obligation_identity",
                )
            }
            for o in record["obligations"]
        ],
        "resources": "Complete resources.json.gz accompanies this spec; authoring basis/queries/needs/protocol/evaluator are omitted",
        "gold_status": "NOT_CREATED",
    }


def render_case(record: Any) -> str:
    """Expose a reviewable task/frame/obligation/query freeze, without results."""
    task_text: str = record["task_text"]
    return (
        f"# Case {record['case_id'][5:]} — direct structural discrimination Stage A\n\n"
        "Stage B NOT EXECUTED; gold ABSENT; effectiveness NOT EVALUATED.\n\n"
        "[Shared architecture/protocol](../../structural_discrimination/README.md) applies unchanged to all three cohort cases.\n\n"
        "Original task:\n\n" + task_text + "\n"
        "Exact prospective case record:\n\n```json\n"
        + json_bytes(record).decode()
        + "```\n\n"
        "All parent identities: frame.json; exact included parent content: resources.json.gz. "
        "blind_spec.json is an input allowlist for later clean adjudication, not gold. "
        "No child implementation, changed paths or diff is available here.\n"
    )


async def expected() -> dict[str, bytes]:
    """Construct only authenticated parent observations and prospective artifacts."""
    cards = await public_cards()
    files: dict[str, bytes] = {}
    records = []
    for case, card in zip(sorted(CASES), cards, strict=True):
        metadata, rows = await observe(card)
        record = case_record(case, card, metadata, rows)
        prefix = f"experiments/codex_dogfood/case_{case}/"
        files.update(
            {
                prefix + ".gitattributes": b"* text eol=lf\n*.gz binary\n",
                prefix + "task.txt": card["task_text"].encode(),
                prefix + "frame.json": json_bytes(metadata),
                prefix + "resources.json.gz": gzip.compress(json_bytes(rows), mtime=0),
                prefix + "protocol.json": json_bytes(record),
                prefix + "blind_spec.json": json_bytes(blind_record(record)),
                prefix + "README.md": render_case(record).encode(),
            }
        )
        records.append(record)
    cohort = {
        "schema": "direct-structural-discrimination-cohort-stage-a-v1",
        "starting_head": START,
        "population_freeze_sha256": POPULATION_SHA,
        "population_selection_seed": SEED,
        "selection": "first THREE existing frozen population entries, no sampling/reroll",
        "cases": records,
        "authoring_order": "Own-parent interpretation0017 fixed before source semantics of later parents; same authoring protocol; no outcome or gold",
        "no_execution": NO_EXECUTION,
        "holdout_access": "NO",
        "confirmation_reserve_access": "NO",
        "modern_harness_source": "Inspected/bound as evaluator only; isolated from parent-only obligation authority and clean reviewer input",
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
    }
    files[PREFIX + "cohort.json"] = json_bytes(cohort)
    files[PREFIX + "protocol.json"] = json_bytes(PROTOCOL)
    files[PREFIX + "evidence_schema.json"] = json_bytes(EVIDENCE_SCHEMA)
    review = (
        "# Direct structural discrimination cohort Stage A review\n\n"
        "PROSPECTIVELY FROZEN; NO TREATMENT EXECUTION; NO GOLD; NO CHILD HOLDOUT ACCESS.\n\n"
        + binary(PACKAGE / "README.md").decode()
        + "\n## Complete cohort freeze\n\n```json\n"
        + json_bytes(cohort).decode()
        + "```\n"
        + "\n## Exact shared protocol\n\n```json\n"
        + json_bytes(PROTOCOL).decode()
        + "```\n"
        + "\n## Exact evidence schema\n\n```json\n"
        + json_bytes(EVIDENCE_SCHEMA).decode()
        + "```\n"
    )
    files[PREFIX + "STAGE_A_REVIEW.md"] = review.encode()
    files[PREFIX + "validation.json"] = json_bytes(
        {
            "status": "PASS",
            "scope": "Stage A structural protocol and parent observation ONLY",
            "checks": [
                "public committed population/seed",
                "first-three identity/order",
                "exact parent trees and every archive Git blob",
                "canonical observation/corpus/document/content",
                "own-parent authoring basis",
                "task/obligation/need/query/action separation",
                "same protocol, no ranking change",
                "blind-spec allowlist",
                "zero treatment/gold/deep execution",
                "deterministic expected artifacts and source bindings",
            ],
            "cohort_cases": len(records),
            "obligations": sum(len(r["obligations"]) for r in records),
            "no_execution": NO_EXECUTION,
        }
    )
    files[PREFIX + "integrity.json"] = json_bytes(
        {
            "schema": "direct-structural-discrimination-stage-a-integrity-v1",
            "starting_head": START,
            "artifacts": {p: digest(raw) for p, raw in sorted(files.items())},
            "implementation": implementations(),
            "public_population_sha256": POPULATION_SHA,
            "hash_scope": "Git blob-content UTF-8 LF source; deterministic gzip mtime0; self hash excluded; no operational .local evidence",
            "no_execution": NO_EXECUTION,
        }
    )
    return files


def compare(files: dict[str, bytes], actual: dict[str, bytes]) -> None:
    """Reject any prospective task/frame/query/protocol/manifest byte change."""
    if files != actual:
        raise ValueError("Stage A artifact bytes differ")


async def build() -> None:
    """Publish the cohort once; refuse overwriting even a partial freeze."""
    files = await expected()
    if any((ROOT / p).exists() for p in files):
        raise FileExistsError("Stage A overwrite refused")
    for path, raw in files.items():
        if path.endswith(".gz"):
            put_binary(ROOT / path, raw)
        else:
            put_text(ROOT / path, raw.decode())


async def authenticate_publication(checkpoint: str, files: dict[str, bytes]) -> None:
    """Authenticate an externally identified Stage A Git publication, not itself.

    Caller checkpoint is the authority. Construction equality before publication is
    distinct from this committed-source/artifact authentication.
    """
    seal_address = PREFIX + "integrity.json"
    committed = await git("show", checkpoint + ":" + seal_address)
    if committed != files[seal_address]:
        raise ValueError("Authoritative Stage A publication differs")
    seal = json.loads(committed)
    bindings = {
        **seal["implementation"],
        **{p: digest(raw) for p, raw in files.items()},
    }
    archive = await git(
        "-c",
        "core.autocrlf=false",
        "archive",
        "--format=tar",
        checkpoint,
        "--",
        *sorted(bindings),
    )
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            stream = bundle.extractfile(member)
            if not member.isfile() or member.name not in bindings or stream is None:
                raise ValueError("Unexpected publication source")
            if member.name in seen or digest(stream.read()) != bindings[member.name]:
                raise ValueError("Publication artifact/implementation bytes differ")
            seen.add(member.name)
    if seen != set(bindings):
        raise ValueError("Incomplete publication authentication")


async def verify(checkpoint: str | None = None) -> dict[str, str]:
    """Observe exact parent data afresh; never enter raw native capture replay."""
    files = await expected()
    compare(files, {p: (ROOT / p).read_bytes() for p in files})
    if checkpoint is not None:
        await authenticate_publication(checkpoint, files)
    return {p: digest(raw) for p, raw in files.items()}


def main() -> None:
    """Offer Stage A build/verify only; capture is deliberately not an option."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument(
        "--checkpoint",
        help="Externally authoritative Stage A Git checkpoint; omission proves prepublication byte equivalence only",
    )
    args = parser.parse_args()
    if args.command == "build":
        asyncio.run(build())
    else:
        rendered = json_bytes(
            {
                "authority": args.checkpoint or "PREPUBLICATION_EQUIVALENCE_ONLY",
                "artifacts": asyncio.run(verify(args.checkpoint)),
            }
        )
        print(rendered.decode())  # noqa: T201 -- scientific CLI


if __name__ == "__main__":
    main()
