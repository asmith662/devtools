# Copyright (c) 2026
# ruff: noqa: PLR2004, EM101, TRY003, T201, C901 -- exact sealed frame and external stdlib boundary
"""Standalone initial-whitelist validator; run before reviewer outputs exist."""

from __future__ import annotations

import gzip
import hashlib
import json
import stat
from pathlib import Path
from typing import Any

FILES = {
    "README.md",
    "manifest.json",
    "integrity.json",
    "resources.json.gz",
    "validate_packet.py",
}
PAYLOAD = {"case", "task_identity", "task_text", "obligations", "resources"}
OBLIGATION = {
    "identity",
    "key",
    "statement",
    "criterion",
    "applicability",
    "task_basis",
}
RESOURCE = {"address", "content_identity", "text", "encoding", "byte_size"}
KEYS = {
    "structure",
    "integrity",
    "manifest",
    "projection",
    "compatibility",
    "exports",
    "tests",
    "documentation",
    "validation",
}


def sha(raw: bytes) -> str:
    """Hash exact bytes for explicit packet digest scopes."""
    return hashlib.sha256(raw).hexdigest()


def content_identity(text: str) -> str:
    """Replay sealed native length-framed decoded UTF-8 content identity semantics."""
    h = hashlib.sha256()
    for value in ("decoded-utf8-text-sha256-v1", text):
        encoded = value.encode("utf-8")
        h.update(len(encoded).to_bytes(8, "big"))
        h.update(encoded)
    return h.hexdigest()


def validate_payload(p: dict[str, Any]) -> None:
    """Enforce exact metadata allowlist; natural original text is not censored."""
    if (
        set(p) != PAYLOAD
        or p["case"] != "case-0013"
        or p["task_identity"] != "case-0013-context-disclosure-manifest"
    ):
        raise ValueError("Blind payload metadata allowlist differs")
    if (
        len(p["resources"]) != 531
        or len(p["obligations"]) != 9
        or {o["key"] for o in p["obligations"]} != KEYS
    ):
        raise ValueError("Blind resource/obligation frame differs")
    if any(set(r) != RESOURCE for r in p["resources"]) or any(
        set(o) != OBLIGATION for o in p["obligations"]
    ):
        raise ValueError("Treatment metadata leakage")
    if (
        len({r["address"] for r in p["resources"]}) != 531
        or len({o["identity"] for o in p["obligations"]}) != 9
    ):
        raise ValueError("Duplicate blind identity")
    for r in p["resources"]:
        a = r["address"]
        if a.startswith(("experiments/", ".local/", ".git/")) or any(
            "confirmation" in part.casefold() or "reserve" in part.casefold()
            for part in a.split("/")
        ):
            raise ValueError("Restricted/treatment resource leakage")
        if (
            r["encoding"] != "utf-8"
            or len(r["text"].encode("utf-8")) != r["byte_size"]
            or content_identity(r["text"]) != r["content_identity"]
        ):
            raise ValueError("Retained content identity/encoding/bytes differ")
    for o in p["obligations"]:
        if o["identity"] != p["task_identity"] + "/" + o["key"]:
            raise ValueError("Blind obligation identity differs")
        for b in o["task_basis"]:
            if (
                set(b) != {"start", "end", "text"}
                or p["task_text"][b["start"] : b["end"]] != b["text"]
            ):
                raise ValueError("Task basis metadata/span differs")


def validate(root: Path) -> dict[str, Any]:
    """Reject extras, links/reparse points, metadata leakage and changed digests."""
    members = list(root.iterdir())
    for path in (root, *members):
        if (
            path.is_symlink()
            or getattr(path.lstat(), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise ValueError("Sterile reparse point")
    if {p.name for p in members} != FILES or any(not p.is_file() for p in members):
        raise ValueError("Sterile initial whitelist differs")
    raw = {p.name: p.read_bytes() for p in members}
    integrity = json.loads(raw["integrity.json"])
    if set(integrity) != {
        "schema",
        "archive_sha256",
        "canonical_payload_sha256",
        "manifest_sha256",
        "sha256",
    } or set(integrity["sha256"]) != FILES - {"integrity.json"}:
        raise ValueError("Integrity metadata allowlist differs")
    if any(sha(raw[n]) != h for n, h in integrity["sha256"].items()):
        raise ValueError("Packet file digest differs")
    manifest = json.loads(raw["manifest.json"])
    if set(manifest) != {
        "schema",
        "case",
        "task_identity",
        "resources",
        "obligations",
        "archive_sha256",
        "canonical_payload_sha256",
    }:
        raise ValueError("Manifest metadata leakage")
    payload_raw = gzip.decompress(raw["resources.json.gz"])
    p = json.loads(payload_raw)
    validate_payload(p)
    if (
        payload_raw
        != (json.dumps(p, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode()
    ):
        raise ValueError("Canonical payload differs")
    for k, value in (
        ("archive_sha256", sha(raw["resources.json.gz"])),
        ("canonical_payload_sha256", sha(payload_raw)),
        ("manifest_sha256", sha(raw["manifest.json"])),
    ):
        if integrity[k] != value or (k != "manifest_sha256" and manifest[k] != value):
            raise ValueError("Packet digest scope differs")
    if (
        manifest["case"],
        manifest["task_identity"],
        manifest["resources"],
        manifest["obligations"],
    ) != (p["case"], p["task_identity"], 531, 9):
        raise ValueError("Manifest semantic binding differs")
    return {
        "status": "PASS; NO ADJUDICATION",
        "files": sorted(FILES),
        **{
            k: integrity[k]
            for k in ("archive_sha256", "canonical_payload_sha256", "manifest_sha256")
        },
        "integrity_sha256": sha(raw["integrity.json"]),
    }


if __name__ == "__main__":
    print(json.dumps(validate(Path(__file__).resolve().parent), indent=2))
