# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004, T201, C901
"""Standalone stdlib-only five-file seal validator; no semantic reviewer."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import stat
from pathlib import Path
from typing import Any

FILES = {
    "README.md",
    "integrity.json",
    "manifest.json",
    "resources.json.gz",
    "validate_packet.py",
}
PAYLOAD = {"case", "task_identity", "task", "obligations", "resources"}
OBLIGATION = {"obligation", "mandatory", "task_clause", "satisfaction_criteria"}
RESOURCE = {
    "repository_id",
    "snapshot_id",
    "corpus_id",
    "address",
    "document_identity",
    "content_identity",
    "content",
}
TASK_ID = "case-0016-resource-pointer-disclosure-v1"
REPOSITORY = "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009"
SNAPSHOT = "636f86afb0fef7b8ccdd9adfd1c9f64dea76139b90d3d098f8f2b811bd90dfca"
CORPUS = "1e0df552f370938fcbbbf489a4bf433a25b4a218b1f624b72a21e463bcbdc7b0"
FORBIDDEN = {
    "query",
    "queries",
    "query_id",
    "query_text",
    "query_terms",
    "seeds",
    "seed",
    "exact_locators",
    "exact_results",
    "personalization",
    "pagerank",
    "ppr",
    "stationary_mass",
    "direct_restart_mass",
    "dangling_return_mass",
    "incoming_structural_flow",
    "pair_flow",
    "definition_flow",
    "graph",
    "nodes",
    "edges",
    "weights",
    "scores",
    "score",
    "rank",
    "ranks",
    "arms",
    "arm",
    "fusion",
    "rrf",
    "results",
    "candidates",
    "candidate_count",
    "graph_novelty",
    "map",
    "metrics",
    "gates",
    "decision_rule",
    "outcome",
    "cost",
    "timing",
    "failure_taxonomy",
    "historical_treatments",
}


def sha(raw: bytes) -> str:
    """Hash exact physical bytes."""
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    """Use frozen sorted ASCII JSON with final newline."""
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode()


def semantic(semantics: str, *values: str) -> str:
    """Replay existing documented native framed identities at external boundary."""
    h = hashlib.sha256()
    for value in (semantics, *values):
        raw = value.encode()
        h.update(len(raw).to_bytes(8, "big"))
        h.update(raw)
    return h.hexdigest()


def tripwire(value: object) -> None:
    """Inspect metadata recursively; natural task/source text remains unchanged."""
    if isinstance(value, dict):
        if FORBIDDEN & value.keys():
            raise ValueError("Treatment metadata leakage")
        for key, item in value.items():
            if key not in {
                "task",
                "task_clause",
                "satisfaction_criteria",
                "content",
                "address",
            }:
                tripwire(item)
    elif isinstance(value, list):
        for item in value:
            tripwire(item)
    elif isinstance(value, str) and re.search(
        r"stage[_ -]?b|bm25|pagerank|ppr|rrf|rank|query|arm[_ -]",
        value,
        re.IGNORECASE,
    ):
        raise ValueError("Treatment metadata value leakage")


def validate_payload(payload: dict[str, Any]) -> None:
    """Validate allowlist/frame/content/obligations without treatment metadata."""
    if (
        set(payload) != PAYLOAD
        or payload["case"] != "0016"
        or payload["task_identity"] != TASK_ID
    ):
        raise ValueError("Packet case/task/allowlist differs")
    obligations, resources = payload["obligations"], payload["resources"]
    if len(obligations) != 6 or len(resources) != 514:
        raise ValueError("Packet resource/obligation count differs")
    for index, row in enumerate(obligations, 1):
        if (
            set(row) != OBLIGATION
            or row["obligation"] != f"O{index}"
            or row["mandatory"] is not True
            or row["task_clause"] not in payload["task"]
            or not row["satisfaction_criteria"]
        ):
            raise ValueError("Mandatory obligation semantic input differs")
    addresses = []
    for row in resources:
        if set(row) != RESOURCE or tuple(
            row[k] for k in ("repository_id", "snapshot_id", "corpus_id")
        ) != (REPOSITORY, SNAPSHOT, CORPUS):
            raise ValueError("Resource allowlist/frame differs")
        address = row["address"]
        if (
            address.startswith(
                ("experiments/", "tests/experiments/", ".local/", ".git/", "/"),
            )
            or "\\" in address
            or any(
                p in {"", ".", ".."}
                or "confirmation" in p.casefold()
                or "reserve" in p.casefold()
                for p in address.split("/")
            )
        ):
            raise ValueError("Restricted/noncanonical resource")
        if re.search(r"case[_ -]?00\d\d", row["content"], re.IGNORECASE):
            raise ValueError("Prior-case content leakage")
        identity = semantic("decoded-utf8-text-sha256-v1", row["content"])
        if row["content_identity"] != identity or row["document_identity"] != semantic(
            "whole-resource-exact-text-v1",
            REPOSITORY,
            address,
            identity,
        ):
            raise ValueError("Native content/document identity differs")
        addresses.append(address)
    if len(set(addresses)) != 514 or addresses != sorted(addresses):
        raise ValueError("Unique canonical resource collection differs")
    pairs = tuple(v for r in resources for v in (r["address"], r["content_identity"]))
    if (
        semantic("explicit-required-text-resources-sha256-v1", REPOSITORY, *pairs)
        != SNAPSHOT
        or semantic(
            "selected-observed-utf8-resource-occurrences-sha256-v1",
            REPOSITORY,
            *pairs,
        )
        != CORPUS
    ):
        raise ValueError("Native snapshot/corpus identity differs")
    tripwire(payload)


def validate(root: Path) -> dict[str, Any]:
    """Reject extras/subdirectories/reparse points and authenticate digest scopes."""
    members = list(root.iterdir())
    for path in (root, *members):
        if (
            path.is_symlink()
            or getattr(path.lstat(), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise ValueError("Sterile symlink/junction/reparse point")
    if {p.name for p in members} != FILES or any(not p.is_file() for p in members):
        raise ValueError("Exact initial five-file whitelist differs")
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
        or set(integrity["sha256"]) != FILES - {"integrity.json"}
        or any(sha(raw[k]) != h for k, h in integrity["sha256"].items())
    ):
        raise ValueError("Packet physical integrity differs")
    if (
        set(manifest)
        != {
            "schema",
            "case",
            "task_identity",
            "resources",
            "obligations",
            "archive_sha256",
            "canonical_payload_sha256",
            "task_sha256",
            "obligations_sha256",
        }
        or (
            manifest["case"],
            manifest["task_identity"],
            manifest["resources"],
            manifest["obligations"],
        )
        != ("0016", TASK_ID, 514, 6)
        or integrity["schema"] != "case-0016-blind-integrity-v1"
        or manifest["schema"] != "case-0016-blind-manifest-v1"
    ):
        raise ValueError("Manifest allowlist/case/frame differs")
    payload_raw = gzip.decompress(raw["resources.json.gz"])
    payload = json.loads(payload_raw)
    validate_payload(payload)
    if (
        canonical(payload) != payload_raw
        or manifest["task_sha256"] != sha(payload["task"].encode())
        or manifest["obligations_sha256"] != sha(canonical(payload["obligations"]))
    ):
        raise ValueError("Canonical/task/obligation seal differs")
    scopes = {
        "archive_sha256": sha(raw["resources.json.gz"]),
        "canonical_payload_sha256": sha(payload_raw),
        "manifest_sha256": sha(raw["manifest.json"]),
    }
    for key, value in scopes.items():
        if integrity[key] != value or (
            key != "manifest_sha256" and manifest[key] != value
        ):
            raise ValueError("Packet digest scope differs")
    tripwire(manifest)
    tripwire(integrity)
    return {
        "status": "PASS; NO ADJUDICATION",
        "files": sorted(FILES),
        **scopes,
        "integrity_sha256": sha(raw["integrity.json"]),
    }


if __name__ == "__main__":
    print(json.dumps(validate(Path(__file__).resolve().parent), indent=2))
