# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004, C901, PLR0912, COM812, T201 -- complete external stdlib-only validation boundary
"""Standalone initial-whitelist authentication, never a gold reviewer."""

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
PAYLOAD = {"case", "task_identity", "task_text", "obligations", "eligible_resources"}
OBLIGATION = {
    "identity",
    "title",
    "mandatory",
    "applicability",
    "task_span",
    "task_clause",
    "satisfaction",
}
RESOURCE = {
    "repository_id",
    "snapshot_id",
    "corpus_id",
    "document_identity",
    "address",
    "content_identity",
    "encoding",
    "utf8_bytes",
    "content",
}
TASK_ID = "case-0015-strict-bounded-filesystem-read-v1"
REPOSITORY = "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009"
SNAPSHOT = "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
CORPUS = "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa"
OBLIGATIONS_SHA256 = "ab28da351b530138082d72452da0cfff5659b4149278f1cc7cab2fabf22e49a3"
FORBIDDEN = {
    "field_definitions",
    "parameters",
    "b_content",
    "b_filename",
    "bm25f_formula",
    "df_union",
    "idf_union",
    "field_length",
    "average_length",
    "field_statistics",
    "decomposition",
    "candidate_results",
    "outcome",
    "outcome_vocabulary",
    "prior_interpretation",
    "query",
    "queries",
    "query_text",
    "analyzed_terms",
    "roles",
    "role",
    "weights",
    "weight",
    "multiplier",
    "generic_lexicon",
    "arms",
    "arm",
    "rank",
    "ranks",
    "score",
    "scores",
    "contributions",
    "results",
    "candidate_count",
    "decision_rule",
    "metrics",
    "gates",
    "cost",
    "timing",
    "inversions",
}


def sha(raw: bytes) -> str:
    """Hash exact physical bytes, with scopes kept distinct."""
    return hashlib.sha256(raw).hexdigest()


def semantic(semantics: str, *values: str) -> str:
    """Replay documented native framed identities at this standalone boundary."""
    h = hashlib.sha256()
    for value in (semantics, *values):
        raw = value.encode("utf-8")
        h.update(len(raw).to_bytes(8, "big"))
        h.update(raw)
    return h.hexdigest()


def canonical(value: object) -> bytes:
    """Require the frozen deterministic JSON representation."""
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode()


def tripwire(value: object) -> None:
    """Scan metadata recursively; original task/resource text is not censored."""
    if isinstance(value, dict):
        if FORBIDDEN & value.keys():
            raise ValueError("Deep treatment metadata leakage")
        for key, item in value.items():
            if key not in {
                "task_text",
                "content",
                "task_clause",
                "criterion",
                "title",
                "satisfaction",
                "address",
            }:
                tripwire(item)
    elif isinstance(value, list):
        for item in value:
            tripwire(item)
    elif isinstance(value, str) and re.search(
        r"stage[_ -]?b|bm25|rank|weight|query|arm[_ -]",
        value,
    ):
        raise ValueError("Deep treatment metadata value leakage")


def validate_payload(payload: dict[str, Any]) -> None:
    """Authenticate every semantic input identity without treatment information."""
    if (
        set(payload) != PAYLOAD
        or payload["case"] != "0015"
        or payload["task_identity"] != TASK_ID
    ):
        raise ValueError("Payload metadata allowlist/binding differs")
    if (
        sha(payload["task_text"].encode())
        != "a5626ce2aea7ff59d3b368e2a35ec2f4e88e7c8049fe35a42852ad1735f8e468"
    ):
        raise ValueError("Original task bytes differ")
    resources, obligations = payload["eligible_resources"], payload["obligations"]
    if (
        len(resources) != 515
        or len(obligations) != 6
        or len({r["address"] for r in resources}) != 515
    ):
        raise ValueError("Resource/obligation frame differs")
    if sha(canonical(obligations)) != OBLIGATIONS_SHA256:
        raise ValueError("Exact original obligation metadata/provenance differs")
    for index, obligation in enumerate(obligations, 1):
        if (
            set(obligation) != OBLIGATION
            or obligation["mandatory"] is not True
            or obligation["applicability"] != "APPLICABLE"
        ):
            raise ValueError("Obligation allowlist/applicability differs")
        if obligation["identity"] != {
            "task": {"value": TASK_ID},
            "value": "O" + str(index),
        }:
            raise ValueError("Obligation identity differs")
        span = obligation["task_span"]
        start = payload["task_text"].index("O" + str(index) + ". ")
        end = (
            payload["task_text"].index("O" + str(index + 1) + ". ")
            if index < 6
            else len(payload["task_text"])
        )
        if (
            span != {"start": start, "end": end}
            or payload["task_text"][start:end] != obligation["task_clause"]
        ):
            raise ValueError("Original task clause/span membership differs")
    addresses = []
    for resource in resources:
        if set(resource) != RESOURCE or (
            resource["repository_id"],
            resource["snapshot_id"],
            resource["corpus_id"],
        ) != (REPOSITORY, SNAPSHOT, CORPUS):
            raise ValueError("Resource metadata allowlist/frame differs")
        address = resource["address"]
        if (
            address.startswith(("experiments/", ".local/", ".git/", "/"))
            or "\\" in address
            or any(
                p in {"", ".", ".."}
                or "confirmation" in p.casefold()
                or "reserve" in p.casefold()
                for p in address.split("/")
            )
        ):
            raise ValueError("Restricted or noncanonical resource")
        if re.search(r"case[_ -]?00\d\d", resource["content"], re.IGNORECASE):
            raise ValueError("Prior-case resource leakage")
        content = semantic("decoded-utf8-text-sha256-v1", resource["content"])
        if (
            resource["encoding"] != "utf-8"
            or resource["utf8_bytes"] != len(resource["content"].encode())
            or resource["content_identity"] != content
            or resource["document_identity"]
            != semantic("whole-resource-exact-text-v1", REPOSITORY, address, content)
        ):
            raise ValueError("Native content/document identity differs")
        addresses.append(address)
    if addresses != sorted(addresses):
        raise ValueError("Resource collection order differs")
    pairs = tuple(v for r in resources for v in (r["address"], r["content_identity"]))
    if (
        semantic("explicit-required-text-resources-sha256-v1", REPOSITORY, *pairs)
        != SNAPSHOT
        or semantic(
            "selected-observed-utf8-resource-occurrences-sha256-v1", REPOSITORY, *pairs
        )
        != CORPUS
    ):
        raise ValueError("Native snapshot/corpus reconstruction differs")
    tripwire(payload)


def validate(root: Path) -> dict[str, Any]:
    """Reject extras/subdirectories/reparse points and authenticate exact scopes."""
    members = list(root.iterdir())
    for path in (root, *members):
        if (
            path.is_symlink()
            or getattr(path.lstat(), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise ValueError("Sterile symlink/junction/reparse point")
    if {p.name for p in members} != FILES or any(not p.is_file() for p in members):
        raise ValueError("Exact initial reviewer whitelist differs")
    raw = {p.name: p.read_bytes() for p in members}
    integrity, manifest = (
        json.loads(raw["integrity.json"]),
        json.loads(raw["manifest.json"]),
    )
    if set(integrity) != {
        "schema",
        "archive_sha256",
        "canonical_payload_sha256",
        "manifest_sha256",
        "sha256",
    } or set(integrity["sha256"]) != FILES - {"integrity.json"}:
        raise ValueError("Integrity metadata allowlist differs")
    if any(sha(raw[k]) != v for k, v in integrity["sha256"].items()):
        raise ValueError("Packet physical artifact digest differs")
    if set(manifest) != {
        "schema",
        "case",
        "task_identity",
        "resources",
        "obligations",
        "archive_sha256",
        "canonical_payload_sha256",
    } or (
        manifest["case"],
        manifest["task_identity"],
        manifest["resources"],
        manifest["obligations"],
    ) != ("0015", TASK_ID, 515, 6):
        raise ValueError("Manifest metadata binding/leakage")
    if (
        integrity["schema"] != "case-0015-blind-integrity-v1"
        or manifest["schema"] != "case-0015-blind-manifest-v1"
    ):
        raise ValueError("Packet schema differs")
    payload_raw = gzip.decompress(raw["resources.json.gz"])
    payload = json.loads(payload_raw)
    validate_payload(payload)
    if payload_raw != canonical(payload):
        raise ValueError("Canonical payload differs")
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
    tripwire(integrity)
    tripwire(manifest)
    return {
        "status": "PASS; NO ADJUDICATION",
        "files": sorted(FILES),
        **scopes,
        "integrity_sha256": sha(raw["integrity.json"]),
    }


if __name__ == "__main__":
    print(json.dumps(validate(Path(__file__).resolve().parent), indent=2))
