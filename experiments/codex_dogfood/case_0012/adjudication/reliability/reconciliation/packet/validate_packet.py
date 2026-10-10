"""Validate the exact initial, treatment-blind reconciliation packet whitelist.

Standalone standard-library boundary. Never import or execute embedded resources.
Run from the fresh reviewer workspace before creating any review outputs.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, PLR2004
# Standalone packet validator; fixed schema numbers and exact instructions.
import gzip
import hashlib
import json
import re
import stat
import sys
from collections import Counter
from pathlib import Path
from typing import Any

WHITELIST = {
    "README.md",
    "packet.json.gz",
    "manifest.json",
    "integrity.json",
    "validate_packet.py",
}


def require(condition: bool, message: str) -> None:  # noqa: FBT001 -- predicate guard
    """Fail a mandatory packet invariant."""
    if not condition:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    """Hash physical bytes."""
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:  # noqa: ANN401 -- heterogeneous packet JSON
    """Encode one deterministic, explicit digest scope."""
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode()


def validate_payload(payload: dict[str, Any]) -> dict[str, int]:  # noqa: C901
    """Check exact positions, neutral ordering, coverage and evidence spans."""
    require(
        set(payload)
        == {
            "schema",
            "case",
            "task_identity",
            "task_text",
            "obligations",
            "resources",
            "propositions",
        },
        "Unexpected payload metadata",
    )
    require(payload["schema"] == "case-0012-neutral-reconciliation-v1", "Schema")
    require(payload["case"] == "case-0012", "Case")
    texts = {r["address"]: r["text"] for r in payload["resources"]}
    require(len(texts) == len(payload["resources"]), "Duplicate resource")
    for r in payload["resources"]:
        require(
            set(r)
            == {
                "address",
                "content_identity",
                "document_identity",
                "encoding",
                "byte_size",
                "text",
                "text_sha256",
            },
            "Unexpected resource metadata",
        )
        require(sha(r["text"].encode()) == r["text_sha256"], "Resource text seal")
        require("stage_b" not in r["address"].casefold(), "Excluded addressed evidence")
    obligations = {o["key"]: o for o in payload["obligations"]}
    require(len(obligations) == len(payload["obligations"]) == 9, "Obligation frame")
    propositions = payload["propositions"]
    require(
        len({p["identity"] for p in propositions}) == len(propositions),
        "Duplicate proposition",
    )
    require(
        [p["identity"] for p in propositions]
        == sorted(p["identity"] for p in propositions),
        "Neutral proposition order",
    )
    used_resources: set[str] = set()

    def inspect(value: Any) -> None:  # noqa: ANN401 -- recursive exact packet JSON
        if isinstance(value, dict):
            require(
                not (
                    {
                        "provenance",
                        "source_id",
                        "primary",
                        "c_r",
                        "model",
                        "chronology",
                        "outcome",
                        "source_mapping",
                        "rank",
                        "score",
                        "cost",
                        "treatment",
                        "query",
                    }
                    & set(value)
                ),
                "Source/treatment metadata",
            )
            if {"origin", "start", "end", "text"} <= set(value):
                text = (
                    payload["task_text"]
                    if value["origin"] == "TASK"
                    else texts[value["address"]]
                )
                require(
                    text[value["start"] : value["end"]] == value["text"],
                    "Support-span tamper",
                )
                if value["origin"] != "TASK":
                    used_resources.add(value["address"])
            for key, child in value.items():
                if key in {"resources", "required_resources"} and isinstance(
                    child,
                    list,
                ):
                    used_resources.update(child)
                inspect(child)
        elif isinstance(value, list):
            for child in value:
                inspect(child)
        elif isinstance(value, str):
            require(
                re.search(
                    r"\bPRIMARY\b|\bC-R\b|\bC_R\b|stage_c_r|GPT-6|SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT|HIGH_RELIABILITY|MATERIAL_DISAGREEMENT",
                    value,
                    re.IGNORECASE,
                )
                is None,
                "Reviewer/source/outcome leakage",
            )

    counts: Counter[str] = Counter()
    for p in propositions:
        require(
            set(p)
            == {
                "identity",
                "type",
                "obligations",
                "resource_addresses",
                "neutral_question",
                "positions",
            },
            "Unexpected proposition metadata",
        )
        require(
            bool(p["neutral_question"]) and set(p["obligations"]) <= set(obligations),
            "Proposition context",
        )
        require(set(p["resource_addresses"]) <= set(texts), "Missing relevant resource")
        used_resources.update(p["resource_addresses"])
        hashes = [sha(canonical(position)) for position in p["positions"]]
        require(
            len(hashes) == 2 and hashes == sorted(hashes),
            "Neutral content-derived competing-position order",
        )
        body = {k: v for k, v in p.items() if k != "identity"}
        require(p["identity"] == sha(canonical(body)), "Proposition identity")
        if p["type"] in {"DISPUTED_CELL_LABEL", "DISPUTED_REQUIRED_NECESSITY"}:
            labels = [x["label"] for x in p["positions"]]
            require(labels[0] != labels[1], "Agreed bulk cell leakage")
            require(
                ("REQUIRED" in labels) == (p["type"] == "DISPUTED_REQUIRED_NECESSITY"),
                "Disputed required classification",
            )
        inspect(p)
        counts[p["type"]] += 1
    require(used_resources == set(texts), "Unused or missing evidence leakage")
    return dict(sorted(counts.items()))


def validate(root: Path) -> dict[str, Any]:
    """Check an initial flat workspace and all independent digest scopes."""
    info = root.lstat()
    require(
        not info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
        if hasattr(info, "st_file_attributes")
        else not root.is_symlink(),
        "Workspace reparse point",
    )
    entries = list(root.iterdir())
    require({p.name for p in entries} == WHITELIST, "Exact reviewer whitelist")
    for p in entries:
        info = p.lstat()
        require(
            stat.S_ISREG(info.st_mode) and not p.is_symlink(),
            "Non-regular packet file",
        )
        require(
            not getattr(info, "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT,
            "Link/junction/reparse point",
        )
    integrity = json.loads((root / "integrity.json").read_bytes())
    manifest = json.loads((root / "manifest.json").read_bytes())
    require(
        set(integrity["files"]) == WHITELIST - {"integrity.json"},
        "Integrity scope",
    )
    for name, digest in integrity["files"].items():
        require(sha((root / name).read_bytes()) == digest, "Physical tamper: " + name)
    archive = (root / "packet.json.gz").read_bytes()
    raw = gzip.decompress(archive)
    payload = json.loads(raw)
    require(raw == canonical(payload), "Canonical payload bytes")
    require(sha(archive) == manifest["archive_sha256"], "Archive digest")
    require(sha(raw) == manifest["canonical_payload_sha256"], "Payload digest")
    counts = validate_payload(payload)
    require(counts == manifest["proposition_counts"], "Proposition coverage counts")
    require(
        [p["identity"] for p in payload["propositions"]]
        == manifest["proposition_identities"],
        "Exact proposition roster",
    )
    return {
        "status": "PASS; NO RECONCILIATION",
        "files": sorted(WHITELIST),
        "proposition_counts": counts,
        "archive_sha256": sha(archive),
        "canonical_payload_sha256": sha(raw),
        "manifest_sha256": sha((root / "manifest.json").read_bytes()),
        "integrity_sha256": sha((root / "integrity.json").read_bytes()),
    }


if __name__ == "__main__":
    sys.stdout.write(
        json.dumps(validate(Path(__file__).resolve().parent), indent=2) + "\n",
    )
