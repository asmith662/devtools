# Copyright (c) 2026
# ruff: noqa: PLR2004, EM101, TRY003, T201 -- fixed prospective frame cardinalities
"""Validate the flat independent adjudication packet using only Python stdlib."""

from __future__ import annotations

import gzip
import hashlib
import json
import stat
from pathlib import Path
from typing import Any

FILES = {
    "manifest.json",
    "resources.json.gz",
    "README.md",
    "validate_packet.py",
    "integrity.json",
}
PAYLOAD = {"case", "task_identity", "task_text", "obligations", "resources", "frame"}
OBLIGATION = {
    "identity",
    "key",
    "statement",
    "criterion",
    "applicability",
    "task_basis",
}
RESOURCE = {
    "address",
    "content_identity",
    "text",
    "encoding",
    "byte_size",
    "document_identity",
}
FRAME = {"repository_id", "snapshot_id", "corpus_id", "frame_identity", "source_head"}


def sha(raw: bytes) -> str:
    """Compute one explicit physical or canonical digest scope."""
    return hashlib.sha256(raw).hexdigest()


def validate_payload(payload: dict[str, Any]) -> None:
    """Whitelist metadata structurally; retained source text is never censored."""
    if set(payload) != PAYLOAD or set(payload["frame"]) != FRAME:
        raise ValueError("Blind payload whitelist differs")
    if len(payload["resources"]) != 531 or len(payload["obligations"]) != 9:
        raise ValueError("Blind resource/obligation coverage differs")
    if any(set(r) != RESOURCE for r in payload["resources"]) or any(
        set(o) != OBLIGATION for o in payload["obligations"]
    ):
        raise ValueError("Treatment field leaked into blind payload")
    if (
        len({r["address"] for r in payload["resources"]}) != 531
        or len({o["identity"] for o in payload["obligations"]}) != 9
    ):
        raise ValueError("Duplicate blind identities")
    for r in payload["resources"]:
        if len(r["text"].encode("utf-8")) != r["byte_size"]:
            raise ValueError("Blind UTF-8 content volume differs")
    for o in payload["obligations"]:
        for basis in o["task_basis"]:
            if (
                set(basis) != {"start", "end", "text"}
                or payload["task_text"][basis["start"] : basis["end"]] != basis["text"]
            ):
                raise ValueError("Blind task basis differs")


def validate(root: Path) -> dict[str, Any]:  # noqa: C901 -- complete flat integrity boundary
    """Reject extras, directories/reparse points, leakage and changed digest scopes."""
    if (
        root.is_symlink()
        or getattr(root.stat(), "st_file_attributes", 0)
        & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise ValueError("Workspace is a reparse point")
    members = list(root.iterdir())
    if {p.name for p in members} != FILES:
        raise ValueError("Sterile file whitelist differs")
    for p in members:
        if (
            not p.is_file()
            or p.is_symlink()
            or getattr(p.stat(), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise ValueError("Sterile member is not a native regular file")
    raw = {p.name: p.read_bytes() for p in members}
    integrity = json.loads(raw["integrity.json"])
    if set(integrity) != {
        "schema",
        "archive_sha256",
        "canonical_payload_sha256",
        "manifest_sha256",
        "sha256",
    } or set(integrity["sha256"]) != FILES - {"integrity.json"}:
        raise ValueError("Blind integrity whitelist differs")
    if any(sha(raw[n]) != h for n, h in integrity["sha256"].items()):
        raise ValueError("Blind file digest differs")
    manifest = json.loads(raw["manifest.json"])
    if set(manifest) != {
        "schema",
        "case",
        "task_identity",
        "frame",
        "resources",
        "obligations",
        "archive_sha256",
        "canonical_payload_sha256",
    }:
        raise ValueError("Blind manifest leaked fields")
    payload_raw = gzip.decompress(raw["resources.json.gz"])
    payload = json.loads(payload_raw)
    validate_payload(payload)
    if (
        payload_raw
        != (
            json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
        ).encode()
    ):
        raise ValueError("Blind canonical payload differs")
    for key, expected in (
        ("archive_sha256", sha(raw["resources.json.gz"])),
        ("canonical_payload_sha256", sha(payload_raw)),
        ("manifest_sha256", sha(raw["manifest.json"])),
    ):
        if integrity[key] != expected or (
            key != "manifest_sha256" and manifest[key] != expected
        ):
            raise ValueError("Blind digest scope differs")
    if (
        manifest["frame"] != payload["frame"]
        or manifest["case"] != payload["case"]
        or manifest["task_identity"] != payload["task_identity"]
        or manifest["resources"] != 531
        or manifest["obligations"] != 9
    ):
        raise ValueError("Blind manifest binding differs")
    return {
        "status": "VERIFIED; NO ADJUDICATION",
        **{
            k: integrity[k]
            for k in ("archive_sha256", "canonical_payload_sha256", "manifest_sha256")
        },
        "integrity_sha256": sha(raw["integrity.json"]),
        "files": sorted(FILES),
    }


if __name__ == "__main__":
    print(json.dumps(validate(Path(__file__).resolve().parent), indent=2))
