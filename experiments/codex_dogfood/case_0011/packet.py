# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003, T201 -- strict case-local blind publication
"""Prepare fresh Stage C only; C.5 is a future separate blind review."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import shutil
from pathlib import Path
from tempfile import mkdtemp
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    digest,
    json_bytes,
    put_binary,
    put_json,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import ensure_absent
from experiments.codex_dogfood.case_0011.execute import committed_stage_a
from experiments.codex_dogfood.case_0011.freeze import load_inputs
from experiments.codex_dogfood.case_0011.protocol import CASE, definition

FILES = (
    "task.txt",
    "manifest.json",
    "resources.json.gz",
    "README.md",
    "FRESH_STAGE_C_INSTRUCTIONS.md",
    "integrity.json",
)
INSTRUCTIONS = """# Fresh independent Case 0011 Stage C

Remain solely in this external sterile directory. Do not access parent/sibling
filesystems, repository checkouts, Git history, prior adjudications, treatment
traces, information needs, queries, results, arm identities, parameters, ranks,
scores, costs, diagnostics, confirmation/reserve, or Stage C.5/D.
Verify every integrity.json file binding, exact archive SHA before decompression,
canonical payload SHA after decompression, task/manifest binding, and the complete
repository/snapshot/corpus/resource/content/obligation/cell frame.

Read the complete original task and every obligation/criterion/provenance. Only
frozen eligible contents are available. Independently adjudicate all cells as
REQUIRED, HELPFUL_ONLY, UNNECESSARY or UNRESOLVED. Record applicability, native
required units, exact content-bound support spans, complementary all-member
witness alternatives, inferability and task/repository-information gaps. Do not
use filenames alone, presumed need/query selection or treatment success as gold.
Retain unknowns and alternative structure. Compute complete coverage, exact label
counts, required unit/resource counts, and enumerate valid sufficient unions.

Record NO attestations for every excluded source above. Human maintainer treatment
inspection is NOT blind gold. Do not import MANUAL_AUDIT. Freeze reproducible
judgments/statistics/digests/method/build/isolated tests. Verify deterministic
replay and overwrite refusal, preserving original six inputs. Use only isolated
Stage C tests with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and --noconftest, no repository
collection. Declare output/cache whitelist and reject links/reparse points.
Stop before repository publication, C.5 or D. No effectiveness analysis here.
"""
README = "# Case 0011 independent task gold\n\nOnly the original task, caller obligations and full eligible resource contents enter this packet. No needs, query definitions or treatment outcomes. Follow FRESH_STAGE_C_INSTRUCTIONS.md.\n"


def render(native: dict[str, Any]) -> dict[str, bytes]:
    """Project an explicit metadata whitelist, without opening result files."""
    t, _, _ = definition()
    resources = [
        {
            "address": d.resource.address.value,
            "content_identity": d.resource.content_identity.value,
            "encoding": d.resource.encoding,
            "byte_size": d.resource.byte_size,
            "content": d.text,
        }
        for d in native["documents"].documents
    ]
    frame = {
        "repository_id": str(native["snapshot"].repository_id),
        "snapshot_id": str(native["snapshot"].id),
        "corpus_id": str(native["corpus"].id),
    }
    payload = json_bytes({**frame, "resources": resources})
    archive = gzip.compress(payload, mtime=0)
    manifest = {
        "schema": "case-0011-blind-task-v1",
        "case_identity": "case-0011",
        **frame,
        "task_identity": t["task_identity"],
        "task": t["task"],
        "task_sha256": t["task_sha256"],
        "obligations": t["obligations"],
        "resource_count": len(resources),
        "obligation_count": len(t["obligations"]),
        "expected_cell_count": len(resources) * len(t["obligations"]),
        "archive_sha256": digest(archive),
        "canonical_payload_sha256": digest(payload),
    }
    output = {
        "task.txt": t["task"].encode(),
        "manifest.json": json_bytes(manifest),
        "resources.json.gz": archive,
        "README.md": README.encode(),
        "FRESH_STAGE_C_INSTRUCTIONS.md": INSTRUCTIONS.encode(),
    }
    output["integrity.json"] = json_bytes(
        {
            "schema": "case-0011-blind-integrity-v1",
            "archive_sha256": digest(archive),
            "canonical_payload_sha256": digest(payload),
            "manifest_sha256": digest(output["manifest.json"]),
            "sha256": {n: digest(v) for n, v in output.items()},
        }
    )
    validate(output, native)
    return output


def validate(output: dict[str, bytes], native: dict[str, Any]) -> None:
    """Check exact packet partition and task/gold frame, never name-based guessing."""
    if set(output) != set(FILES):
        raise ValueError("Blind workspace whitelist differs")
    t, _, _ = definition()
    m = json.loads(output["manifest.json"])
    allowed = {
        "schema",
        "case_identity",
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "task_identity",
        "task",
        "task_sha256",
        "obligations",
        "resource_count",
        "obligation_count",
        "expected_cell_count",
        "archive_sha256",
        "canonical_payload_sha256",
    }
    if (
        set(m) != allowed
        or m["schema"] != "case-0011-blind-task-v1"
        or m["case_identity"] != "case-0011"
        or m["task_identity"] != t["task_identity"]
        or m["task_sha256"] != t["task_sha256"]
        or m["obligations"] != t["obligations"]
        or m["task"] != t["task"]
        or output["task.txt"] != t["task"].encode()
    ):
        raise ValueError("Task/obligation metadata leakage or binding failure")
    obkeys = {
        "identity",
        "predicate",
        "criterion",
        "requirement",
        "applicability_condition",
        "provenance",
        "author",
        "task_basis",
    }
    if any(set(o) != obkeys for o in m["obligations"]):
        raise ValueError("Need/query metadata leaked")
    raw = gzip.decompress(output["resources.json.gz"])
    r = json.loads(raw)
    docs = native["documents"].documents
    expected = [
        {
            "address": d.resource.address.value,
            "content_identity": d.resource.content_identity.value,
            "encoding": d.resource.encoding,
            "byte_size": d.resource.byte_size,
            "content": d.text,
        }
        for d in docs
    ]
    if (
        set(r) != {"repository_id", "snapshot_id", "corpus_id", "resources"}
        or r["resources"] != expected
        or len({d["address"] for d in expected}) != len(docs)
    ):
        raise ValueError("Resource/content frame differs")
    for k, value in (
        ("repository_id", native["snapshot"].repository_id),
        ("snapshot_id", native["snapshot"].id),
        ("corpus_id", native["corpus"].id),
    ):
        if m[k] != r[k] or m[k] != str(value):
            raise ValueError("Native frame differs")
    if (
        m["resource_count"] != len(docs)
        or m["obligation_count"] != len(t["obligations"])
        or m["expected_cell_count"] != len(docs) * len(t["obligations"])
    ):
        raise ValueError("Full-frame partition differs")
    s = json.loads(output["integrity.json"])
    if (
        m["archive_sha256"] != digest(output["resources.json.gz"])
        or m["canonical_payload_sha256"] != digest(raw)
        or s["archive_sha256"] != m["archive_sha256"]
        or s["canonical_payload_sha256"] != m["canonical_payload_sha256"]
        or s["manifest_sha256"] != digest(output["manifest.json"])
        or s["sha256"]
        != {n: digest(v) for n, v in output.items() if n != "integrity.json"}
    ):
        raise ValueError("Blind integrity binding differs")


def whitelist(root: Path) -> None:
    """Reject links/reparse points and every unexpected file or directory."""
    if (
        {p.name for p in root.iterdir()} != set(FILES)
        or root.is_symlink()
        or getattr(root.lstat(), "st_file_attributes", 0) & 0x400
    ):
        raise ValueError("Sterile directory shape differs")
    for p in root.iterdir():
        if (
            not p.is_file()
            or p.is_symlink()
            or getattr(p.lstat(), "st_file_attributes", 0) & 0x400
        ):
            raise ValueError("Sterile link or directory")


def build() -> dict[str, Any]:
    """Double-build only Stage C; C.5 remains deliberately unbuilt."""
    ensure_absent(CASE, ("adjudication", "sterile_workspace.json"))
    native = load_inputs()
    first, second = render(native), render(native)
    if first != second:
        raise ValueError("Packet double-build differs")
    target = CASE / "adjudication"
    target.mkdir()
    for n, value in first.items():
        if n.endswith(".gz"):
            put_binary(target / n, value)
        else:
            put_text(target / n, value.decode())
    commit = asyncio.run(committed_stage_a())
    sterile = Path(mkdtemp(prefix="case_0011_stage_c_sterile_" + commit[:7] + "_"))
    # Genuine external sterile publication boundary: exact byte copying.
    for n in FILES:
        shutil.copyfile(target / n, sterile / n)
        if (sterile / n).read_bytes() != first[n]:
            raise ValueError("Sterile destination bytes differ")
    whitelist(sterile)
    put_json(
        CASE / "sterile_workspace.json",
        {
            "path": str(sterile),
            "files": list(FILES),
            "sha256": {n: digest(v) for n, v in first.items()},
            "Stage_C": "NOT_PERFORMED",
            "Stage_C_5": "NOT_BUILT",
            "Stage_D": "NOT_PERFORMED",
        },
    )
    return verify()


def verify() -> dict[str, Any]:
    """Verify native double-build, repository packet and external byte identity."""
    native = load_inputs()
    target = CASE / "adjudication"
    whitelist(target)
    data = {n: (target / n).read_bytes() for n in FILES}
    validate(data, native)
    if data != render(native) or render(native) != render(native):
        raise ValueError("Packet deterministic replay differs")
    record = read_json(CASE / "sterile_workspace.json")
    sterile = Path(record["path"])
    whitelist(sterile)
    if any((sterile / n).read_bytes() != data[n] for n in FILES):
        raise ValueError("Sterile packet bytes differ")
    seal: dict[str, Any] = json.loads(data["integrity.json"])
    return seal


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    print(build() if args.operation == "build" else verify())
