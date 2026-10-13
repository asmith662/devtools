# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, T201 -- standalone external packet boundary
"""Authenticate exactly five blind files using stdlib only; never adjudicate."""

from __future__ import annotations

import gzip
import hashlib
import json
import stat
from pathlib import Path
from typing import Any

# CASE_BOUNDARY
BOUND: dict[str, Any] = {'case_id': 'case-0018', 'task_identity': 'case-0018:historical-development-002', 'resources': 382, 'obligations': 3, 'canonical_payload_sha256': '66aa4b49ee362d786e4c879db318f9c94d56e2d960743a983653d11c77e72b4f', 'task_sha256': 'c540758bc3ab5600a985737892b93beb9045e7c56f00f44ef78ada4ab4369c97', 'obligations_sha256': '02165c1a7a58d9131ad9beea72e5cd7bc35abf86325d572d71edbfbe89dbeaeb', 'gaps_sha256': '37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570', 'frame_sha256': 'dcdd7d10f1b40c08d47cbe52ce5232da5cd0b47595f6ee3ba701069f3a4ff6b9'}
FILES = {
    "README.md",
    "integrity.json",
    "manifest.json",
    "resources.json.gz",
    "validate_packet.py",
}
RESOURCE = {
    "repository_id",
    "snapshot_id",
    "corpus_id",
    "address",
    "document_identity",
    "content_identity",
    "content",
    "source_blob_sha256",
    "git_blob_oid",
}
FORBIDDEN = {
    "query",
    "queries",
    "query_identity",
    "need",
    "information_need",
    "rank",
    "ranks",
    "score",
    "scores",
    "annotations",
    "supports",
    "local_pairs",
    "timings",
    "child_commit",
    "child_tree",
    "changed_paths",
    "diff",
    "authoring_basis_sha256",
    "implementation",
    "execution",
    "stage_b_checkpoint",
}


def sha(raw: bytes) -> str:
    """Hash exact bytes at the standalone external boundary."""
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    """Match the frozen sorted ASCII JSON codec exactly."""
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode()


def semantic(semantics: str, *values: str) -> str:
    """Replay documented native framed identities without repository access."""
    h = hashlib.sha256()
    for value in (semantics, *values):
        raw = value.encode()
        h.update(len(raw).to_bytes(8, "big"))
        h.update(raw)
    return h.hexdigest()


def metadata(value: Any) -> None:
    """Reject treatment metadata keys while preserving exact natural source text."""
    if isinstance(value, dict):
        if FORBIDDEN & value.keys():
            raise ValueError("Treatment or child metadata leakage")
        for item in value.values():
            metadata(item)
    elif isinstance(value, list):
        for item in value:
            metadata(item)


def validate_payload(payload: Any, bound: Any) -> None:  # noqa: C901 -- complete standalone frame/input boundary
    """Authenticate the exact frozen blind allowlist, task, gap and full frame."""
    if set(payload) != {
        "case_id",
        "task_identity",
        "task_text",
        "parent_frame",
        "interpretation_gaps",
        "ambiguities",
        "obligations",
        "resources",
        "gold_status",
    }:
        raise ValueError("Blind payload allowlist differs")
    if (
        payload["case_id"] != bound["case_id"]
        or payload["task_identity"] != bound["task_identity"]
        or payload["gold_status"] != "NOT_CREATED"
        or sha(canonical(payload)) != bound["canonical_payload_sha256"]
    ):
        raise ValueError("Exact blind payload/case identity differs")
    if (
        sha(payload["task_text"].encode()) != bound["task_sha256"]
        or sha(canonical(payload["obligations"])) != bound["obligations_sha256"]
        or sha(canonical(payload["interpretation_gaps"])) != bound["gaps_sha256"]
        or sha(canonical(payload["parent_frame"])) != bound["frame_sha256"]
    ):
        raise ValueError("Task/obligation/gap/frame binding differs")
    frame = payload["parent_frame"]
    rows = payload["resources"]
    if (
        len(rows) != bound["resources"]
        or len(payload["obligations"]) != bound["obligations"]
    ):
        raise ValueError("Blind resource/obligation counts differ")
    for i, obligation in enumerate(payload["obligations"], 1):
        if (
            set(obligation)
            != {
                "id",
                "requirement",
                "satisfaction",
                "excluded_interpretation",
                "obligation_identity",
            }
            or obligation["id"] != f"O{i}"
            or obligation["obligation_identity"]
            != {"task": payload["task_identity"], "value": f"O{i}"}
        ):
            raise ValueError("Frozen obligation interpretation differs")
    addresses = []
    for row in rows:
        if set(row) != RESOURCE or any(
            row[k] != frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")
        ):
            raise ValueError("Resource allowlist/frame differs")
        address = row["address"]
        if (
            address.startswith(
                ("/", "experiments/", "tests/experiments/", ".git/", ".local/"),
            )
            or "\\" in address
            or any(
                p in {"", ".", ".."}
                or "confirmation" in p.casefold()
                or "reserve" in p.casefold()
                for p in address.split("/")
            )
        ):
            raise ValueError("Restricted resource address")
        content = row["content"].encode()
        blob = hashlib.sha1(
            f"blob {len(content)}\0".encode() + content,
            usedforsecurity=False,
        ).hexdigest()
        content_id = semantic("decoded-utf8-text-sha256-v1", row["content"])
        if (
            sha(content) != row["source_blob_sha256"]
            or blob != row["git_blob_oid"]
            or content_id != row["content_identity"]
            or row["document_identity"]
            != semantic(
                "whole-resource-exact-text-v1",
                frame["repository_id"],
                address,
                content_id,
            )
        ):
            raise ValueError("Exact resource bytes/native identity differs")
        addresses.append(address)
    if addresses != sorted(set(addresses)):
        raise ValueError("Unique ordered frame differs")
    pairs = tuple(v for row in rows for v in (row["address"], row["content_identity"]))
    if frame["snapshot_id"] != semantic(
        "explicit-required-text-resources-sha256-v1",
        frame["repository_id"],
        *pairs,
    ) or frame["corpus_id"] != semantic(
        "selected-observed-utf8-resource-occurrences-sha256-v1",
        frame["repository_id"],
        *pairs,
    ):
        raise ValueError("Snapshot/corpus identity differs")
    metadata(payload)


def validate(root: Path, bound: Any = None) -> dict[str, Any]:
    """Reject extras/reparse points and authenticate every packet digest scope."""
    bound = BOUND if bound is None else bound
    members = list(root.iterdir())
    for path in (root, *members):
        if (
            path.is_symlink()
            or getattr(path.lstat(), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise ValueError("Sterile reparse point/symlink")
    if {p.name for p in members} != FILES or any(not p.is_file() for p in members):
        raise ValueError("Exact initial five files required")
    raw = {p.name: p.read_bytes() for p in members}
    integrity, manifest = (
        json.loads(raw["integrity.json"]),
        json.loads(raw["manifest.json"]),
    )
    if (
        set(integrity)
        != {
            "schema",
            "archive_sha256",
            "canonical_payload_sha256",
            "manifest_sha256",
            "sha256",
        }
        or integrity["schema"] != "treatment-blind-integrity-v1"
        or set(integrity["sha256"]) != FILES - {"integrity.json"}
        or any(sha(raw[name]) != h for name, h in integrity["sha256"].items())
    ):
        raise ValueError("Physical packet integrity differs")
    payload_raw = gzip.decompress(raw["resources.json.gz"])
    payload = json.loads(payload_raw)
    validate_payload(payload, bound)
    expected_manifest = {
        "schema": "treatment-blind-manifest-v1",
        **bound,
        "archive_sha256": sha(raw["resources.json.gz"]),
    }
    if manifest != expected_manifest or payload_raw != canonical(payload):
        raise ValueError("Canonical manifest/payload differs")
    scopes = {
        "archive_sha256": sha(raw["resources.json.gz"]),
        "canonical_payload_sha256": sha(payload_raw),
        "manifest_sha256": sha(raw["manifest.json"]),
    }
    if any(integrity[k] != value for k, value in scopes.items()):
        raise ValueError("Packet digest scope differs")
    return {
        "status": "PASS; NO ADJUDICATION",
        "case_id": bound["case_id"],
        **scopes,
        "integrity_sha256": sha(raw["integrity.json"]),
        "files": sorted(FILES),
    }


if __name__ == "__main__":
    print(json.dumps(validate(Path(__file__).resolve().parent), indent=2))
