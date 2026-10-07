# Copyright (c) 2026
# ruff: noqa: C901, COM812, EM101, PLR0912, TRY003, T201 -- bounded blind packet
"""Build deterministic full-frame blind inputs, never read treatment results."""

from __future__ import annotations

import argparse
import gzip
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_binary,
    put_text,
)
from experiments.codex_dogfood.case_0009.freeze import ensure_absent
from experiments.codex_dogfood.case_0010.freeze import CASE, load_inputs
from experiments.codex_dogfood.case_0010.protocol import TASK

README = """# Case 0010 independent blind packet

Use only this sterile directory's manifest, full resource archive, digest record
and fresh Stage C instructions. There are no treatment results or gold here.
Verify exact archive_sha256 before decompression; canonical_payload_sha256 seals
the uncompressed canonical JSON bytes. Gold requires fresh independent semantic
adjudication. Do not execute repository-wide pytest or access the parent checkout.
"""
INSTRUCTIONS = """# Fresh independent Case 0010 Stage C

Remain solely in this external sterile workspace. Verify every file hash in
integrity.json, archive_sha256 before decompression, and canonical_payload_sha256
after decompression. Verify identities and full resource/obligation/cell frame.
Read the complete caller task and predicates in manifest.json; inspect frozen
resources only. Do not access any repository checkout or external experiment.

Independently adjudicate every obligation/resource cell as REQUIRED, HELPFUL_ONLY,
UNNECESSARY or UNRESOLVED. Relevance is obligation-relative. Record applicability,
required information units and resource-to-unit links. Record acceptable all-of
witness alternatives independently; do not mix incompatible alternatives.
Record distinct units, unique required resources, alternative counts and minimum/
maximum sufficient union. Distinguish inferable-at-start from inherent-discovery
requirements and explicit task/repository-information gaps. Do not calculate
retrieval effectiveness or assume a resource is required because a query names it.

Record ten blindness attestations NO: Arm A results accessed; challenger results
accessed; treatment ranks accessed; treatment scores accessed; treatment comparison
accessed; treatment costs accessed; analyzer diagnostics accessed; historical/
provisional gold accessed; confirmation/reserve accessed; effectiveness analysis
performed. Stop if any cannot be truthfully asserted. This packet includes no
query-lane identities, arm definitions, parameter configurations or treatment data.

Freeze reproducible judgments.json, gold_statistics.json, judgments.sha256 and
method/build/isolated-validation artifacts in this workspace. Preserve the original
blind inputs. Produce complete deterministic coverage validation, replay and
overwrite refusal. Do not run bare pytest or any broader repository collection:
use only your exact Stage C test with plugin autoload disabled and --noconftest.
If using a workspace whitelist, allow only the listed blind inputs, your explicitly
named clean Stage C output files and runtime caches created after execution.
Publication is a later byte-for-byte checkpoint; no joined effectiveness here.
"""
BLIND_FILES = (
    "FRESH_STAGE_C_INSTRUCTIONS.md",
    "README.md",
    "manifest.json",
    "resources.json.gz",
    "integrity.json",
)


def render(native: dict[str, Any]) -> dict[str, bytes]:
    """Only Stage A native task/frame enters the blind payload."""
    snapshot, corpus, task = native["snapshot"], native["corpus"], native["task"]
    resource_rows = [
        {
            "address": d.resource.address.value,
            "content_identity": d.resource.content_identity.value,
            "encoding": d.resource.encoding,
            "byte_size": d.resource.byte_size,
            "content": d.text,
        }
        for d in native["documents"].documents
    ]
    resources = {
        "repository_id": str(snapshot.repository_id),
        "snapshot_id": str(snapshot.id),
        "corpus_id": str(corpus.id),
        "resources": resource_rows,
    }
    payload = json_bytes(resources)
    archive = gzip.compress(payload, mtime=0)
    manifest = {
        "schema": "case-0010-blind-task-v1",
        "case_identity": "case-0010",
        "task": TASK,
        "task_identity": task.identity.value,
        "repository_id": str(snapshot.repository_id),
        "snapshot_id": str(snapshot.id),
        "corpus_id": str(corpus.id),
        "obligations": [
            {
                "identity": ob.identity.value,
                "predicate": ob.predicate,
                "requirement": ob.requirement.value,
            }
            for ob in task.obligations
        ],
        "resource_count": len(resource_rows),
        "obligation_count": len(task.obligations),
        "expected_cell_count": len(resource_rows) * len(task.obligations),
        "archive_sha256": digest(archive),
        "canonical_payload_sha256": digest(payload),
    }
    output = {
        "manifest.json": json_bytes(manifest),
        "resources.json.gz": archive,
        "README.md": README.encode(),
        "FRESH_STAGE_C_INSTRUCTIONS.md": INSTRUCTIONS.encode(),
    }
    output["integrity.json"] = json_bytes(
        {
            "schema": "case-0010-blind-integrity-v1",
            "archive_sha256": digest(archive),
            "canonical_payload_sha256": digest(payload),
            "manifest_sha256": digest(output["manifest.json"]),
            "sha256": {n: digest(v) for n, v in output.items()},
        }
    )
    validate(output, native)
    return output


def validate(output: dict[str, bytes], native: dict[str, Any]) -> None:
    """Strict metadata whitelist and full occurrence/content coverage, no rank join."""
    if set(output) != set(BLIND_FILES):
        raise ValueError("Unexpected blind file.")
    manifest = json.loads(output["manifest.json"])
    allowed = {
        "schema",
        "case_identity",
        "task",
        "task_identity",
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "obligations",
        "resource_count",
        "obligation_count",
        "expected_cell_count",
        "archive_sha256",
        "canonical_payload_sha256",
    }
    if set(manifest) != allowed or manifest["task"] != TASK:
        raise ValueError("Unexpected blind metadata.")
    if any(
        set(ob) != {"identity", "predicate", "requirement"}
        for ob in manifest["obligations"]
    ):
        raise ValueError("Query/treatment fields leaked into obligations.")
    payload = gzip.decompress(output["resources.json.gz"])
    resources = json.loads(payload)
    if set(resources) != {"repository_id", "snapshot_id", "corpus_id", "resources"}:
        raise ValueError("Unexpected resource metadata.")
    docs = native["documents"].documents
    if (
        len(resources["resources"]) != len(docs)
        or manifest["resource_count"] != len(docs)
        or manifest["expected_cell_count"]
        != len(docs) * len(native["task"].obligations)
    ):
        raise ValueError("Full frame coverage differs.")
    for row, doc in zip(resources["resources"], docs, strict=True):
        if (
            set(row)
            != {"address", "content_identity", "encoding", "byte_size", "content"}
            or row["address"] != doc.resource.address.value
            or row["content_identity"] != doc.resource.content_identity.value
            or row["content"] != doc.text
        ):
            raise ValueError("Occurrence/content identity differs.")
    if len({r["address"] for r in resources["resources"]}) != len(docs):
        raise ValueError("Duplicate resource identity.")
    for key, expected in (
        ("repository_id", str(native["snapshot"].repository_id)),
        ("snapshot_id", str(native["snapshot"].id)),
        ("corpus_id", str(native["corpus"].id)),
    ):
        if manifest[key] != expected or resources[key] != expected:
            raise ValueError("Blind frame differs.")
    if manifest["archive_sha256"] != digest(output["resources.json.gz"]) or manifest[
        "canonical_payload_sha256"
    ] != digest(payload):
        raise ValueError("Blind digest scope differs.")
    seal = json.loads(output["integrity.json"])
    if set(seal["sha256"]) != set(BLIND_FILES) - {"integrity.json"}:
        raise ValueError("Blind digest coverage differs.")
    for name, expected in seal["sha256"].items():
        if digest(output[name]) != expected:
            raise ValueError("Blind exact file hash differs.")


def build() -> dict[str, Any]:
    """Publish only after two independently rendered byte-identical builds."""
    target = CASE / "adjudication"
    ensure_absent(CASE, ("adjudication",))
    native = load_inputs()
    a, b = render(native), render(native)
    if a != b:
        raise ValueError("Blind double build differs.")
    target.mkdir()
    for name, content in a.items():
        if name.endswith(".gz"):
            put_binary(target / name, content)
        else:
            put_text(target / name, content.decode())
    return verify()


def verify() -> dict[str, Any]:
    """Require exact regeneration and whitelist without opening treatment captures."""
    target = CASE / "adjudication"
    if {p.name for p in target.iterdir()} != set(BLIND_FILES) or any(
        p.is_symlink() or not p.is_file() for p in target.iterdir()
    ):
        raise ValueError("Blind directory shape differs.")
    observed = {n: binary(target / n) for n in BLIND_FILES}
    native = load_inputs()
    validate(observed, native)
    if observed != render(native):
        raise ValueError("Blind packet replay differs.")
    seal: dict[str, Any] = json.loads(observed["integrity.json"])
    return seal


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    print(build() if args.operation == "build" else verify())
