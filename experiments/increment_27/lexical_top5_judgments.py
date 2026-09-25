# Copyright (c) 2026
# ruff: noqa: C901, E501, EM101, EM102, PLC0415, PLR0912, PLR2004, RUF001, TRY003, TRY004
"""Freeze blinded Increment-27 top-five usefulness judgments."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import cast

TOP5_FREEZE_IDENTITY = "ace8c18e42bc88f1304030c399f29daea66baf26772558ed867244e9dd20ce44"
NEW_POPULATION_IDENTITY = "f2dabd43c8de35b9bc3f9ae4ef5d8d0149849bee6270d9f9744a6f533fc19555"
BLINDED_INPUT_SHA256 = "00889562f8ef02d7ed8ef0a3804e92d36e5fd22a569776bbfceb44b806343b72"
EXPECTED_TARGET_COUNT = 133
INPUT_FILENAME = "lexical_top5_blinded_judgment_input.json"
OUTPUT_FILENAME = "lexical_top5_frozen_judgments.json"
SCHEMA = "devtools-increment-27-top5-frozen-judgments-v1"
ALLOWED_LABELS = {"USEFUL", "NOT_USEFUL", "UNJUDGED"}
USEFULNESS_SEMANTICS: dict[str, object] = {
    "USEFUL": (
        "The parent-snapshot resource contains information that would materially "
        "help a capable software-engineering agent address the stated InformationNeed."
    ),
    "NOT_USEFUL": (
        "The parent-snapshot resource does not materially help with the stated "
        "InformationNeed, even if it has superficial lexical overlap."
    ),
    "UNJUDGED": (
        "The exposed evidence is insufficient for a defensible USEFUL or "
        "NOT_USEFUL decision; this state is not negative evidence."
    ),
}

# Codes follow the frozen neutral case/resource order. They are keyed only by
# the blinded case identity and do not encode retrieval membership or ranking.
_DECISION_CODES = {
    "case-0823453974f4e6c4": "NNUNU",
    "case-0ed68cbc825aaef9": "UUUUUN",
    "case-0f4e8e1a43e320fe": "NNUUUN",
    "case-2cf3e30589b09d74": "UNNUNN",
    "case-2fb416eae793db8a": "UUNNUN",
    "case-3958eef42f3e9a50": "N",
    "case-472d8dd425b5ac4d": "NUUUUUNUU",
    "case-4a15285ac83dbb4a": "UUNNU",
    "case-4a6de9fc4a4b0143": "UNUUNNUUUN",
    "case-4f103eaefc7cdefe": "UUNUUNN",
    "case-5470817e4f7742d8": "UUUNNUU",
    "case-6ff35afc3599b44c": "N",
    "case-7853ef02a8275716": "UUN",
    "case-7d19d4edd0d5ebb6": "",
    "case-815441957a9e4508": "NNUUNUUUU",
    "case-8b3affb5684c9d42": "XXXXX",
    "case-99814e23b6ff12ca": "UU",
    "case-9f3e137266cdff0c": "NUUNNU",
    "case-aeac7535dbf4104c": "UUUUUNUU",
    "case-bfec94bfce504d9c": "NUUUUUNNUUNU",
    "case-c7bf712837ca051d": "UUUUNUNUU",
    "case-ddeb4b6d7e50df8e": "",
    "case-e183edf6d71034e3": "NNNNNNN",
    "case-f29de00eb4ff4cec": "UNN",
}
_CODE_TO_LABEL = {"U": "USEFUL", "N": "NOT_USEFUL", "X": "UNJUDGED"}
_TASK_PREFIX = "Address the historical maintenance task: "


def canonical_json_bytes(value: object) -> bytes:
    """Serialize a JSON value with the experiment's stable UTF-8 encoding."""
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def content_identity(value: object) -> str:
    """Return the stable SHA-256 identity of a canonical JSON value."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def validate_blinded_input(value: object) -> dict[str, object]:
    """Validate the exact neutral input schema and reject outcome/origin fields."""
    if not isinstance(value, dict) or set(value) != {"content_identity", "payload", "schema"}:
        raise ValueError("Blinded input has an unexpected root shape.")
    if value["schema"] != "devtools-increment-27-top5-blinded-judgment-input-v1":
        raise ValueError("Blinded input schema changed.")
    if value["content_identity"] != NEW_POPULATION_IDENTITY:
        raise ValueError("Blinded population identity changed.")
    payload = value["payload"]
    if not isinstance(payload, dict) or set(payload) != {"cases", "schema"}:
        raise ValueError("Blinded input payload has an unexpected shape.")
    if payload["schema"] != value["schema"]:
        raise ValueError("Blinded input schema markers disagree.")
    cases = payload["cases"]
    if not isinstance(cases, list) or len(cases) != 24:
        raise ValueError("Blinded input must contain exactly 24 development cases.")

    identities: set[str] = set()
    targets: set[tuple[str, str]] = set()
    total = 0
    for case in cases:
        if not isinstance(case, dict) or set(case) != {
            "information_need",
            "neutral_case_id",
            "parent_snapshot_sha",
            "resources",
        }:
            raise ValueError("A blinded case contains unexpected or hidden fields.")
        case_id = case["neutral_case_id"]
        if not isinstance(case_id, str) or case_id in identities:
            raise ValueError("Blinded case identities must be unique strings.")
        identities.add(case_id)
        need = case["information_need"]
        if not isinstance(need, dict) or set(need) != {"lexical_query", "purpose"}:
            raise ValueError("InformationNeed contains unexpected fields.")
        if not all(isinstance(need[key], str) and need[key] for key in need):
            raise ValueError("InformationNeed purpose and query must be nonempty text.")
        if not isinstance(case["parent_snapshot_sha"], str):
            raise ValueError("Parent snapshot identity must be text.")
        resources = case["resources"]
        if not isinstance(resources, list):
            raise ValueError("Case resources must be a list.")
        for resource in resources:
            if not isinstance(resource, dict) or set(resource) != {
                "address",
                "content",
                "neutral_resource_id",
            }:
                raise ValueError("A blinded resource contains unexpected fields.")
            if not all(
                isinstance(resource[key], str) and resource[key]
                for key in ("address", "content", "neutral_resource_id")
            ):
                raise ValueError("Blinded resource identity and content are required.")
            pair = (case_id, resource["address"])
            if pair in targets:
                raise ValueError("Blinded input contains a duplicate case/resource pair.")
            targets.add(pair)
            total += 1
    if total != EXPECTED_TARGET_COUNT:
        raise ValueError("Blinded input must contain exactly 133 new targets.")
    if set(_DECISION_CODES) != identities:
        raise ValueError("Blinded input development cases differ from the adjudicated set.")
    return cast("dict[str, object]", value)


def _resource_subject(resource: dict[str, object]) -> str:
    address = str(resource["address"])
    content = str(resource["content"])
    if address.endswith(".py"):
        try:
            import ast

            docstring = ast.get_docstring(ast.parse(content))
        except SyntaxError:
            docstring = None
        if docstring:
            first_sentence = re.split(r"(?<=[.!?])\s+", docstring.strip(), maxsplit=1)[0]
            return first_sentence.rstrip(".")
    for line in content.splitlines():
        heading = re.match(r"^#\s+(.+?)\s*#*$", line.strip())
        if heading:
            return heading.group(1).strip(" `")
    return Path(address).stem.replace("_", " ").replace("-", " ")


def _rationale(
    *,
    label: str,
    purpose: str,
    resource: dict[str, object],
) -> str:
    if label == "UNJUDGED":
        return (
            "The exposed purpose and query are truncated to ‘ed evidence’ and do "
            "not identify the requested evidence work, so this content cannot be "
            "defensibly classified against a concrete need."
        )
    task = purpose.removeprefix(_TASK_PREFIX).strip().rstrip(".")
    subject = _resource_subject(resource)
    address = str(resource["address"])
    if label == "USEFUL":
        if address.startswith("tests/"):
            return (
                f"Its tests specify or exercise {subject}, giving concrete behavior "
                f"and boundary expectations for the requested work to {task.lower()}."
            )
        if address.endswith(".md"):
            return (
                f"It documents {subject}, which explains a package or interface "
                f"boundary the requested work to {task.lower()} must respect."
            )
        return (
            f"It implements {subject}, the mechanism the requested work to "
            f"{task.lower()} needs to extend or integrate."
        )
    return (
        f"It covers {subject}, while the stated need is to {task.lower()}; its "
        "content does not specify or validate that requested behavior."
    )


def build_frozen_judgments(input_path: Path) -> dict[str, object]:
    """Build and validate the deterministic 133-target judgment artifact."""
    raw = input_path.read_bytes()
    input_sha = hashlib.sha256(raw).hexdigest()
    if input_sha != BLINDED_INPUT_SHA256:
        raise ValueError("Frozen blinded input file hash changed.")
    blinded = validate_blinded_input(json.loads(raw))
    payload = cast("dict[str, object]", blinded["payload"])
    cases = cast("list[dict[str, object]]", payload["cases"])
    records: list[dict[str, str]] = []
    for case in cases:
        case_id = str(case["neutral_case_id"])
        resources = cast("list[dict[str, object]]", case["resources"])
        codes = _DECISION_CODES[case_id]
        if len(codes) != len(resources):
            raise ValueError(f"Decision count does not match frozen targets for {case_id}.")
        need = cast("dict[str, str]", case["information_need"])
        for code, resource in zip(codes, resources, strict=True):
            label = _CODE_TO_LABEL[code]
            records.append(
                {
                    "case_id": case_id,
                    "resource_id": str(resource["neutral_resource_id"]),
                    "address": str(resource["address"]),
                    "judgment": label,
                    "rationale": _rationale(
                        label=label,
                        purpose=need["purpose"],
                        resource=resource,
                    ),
                },
            )
    records.sort(key=lambda record: (record["case_id"], record["resource_id"]))
    pair_identity = content_identity(
        [
            {"case_id": row["case_id"], "address": row["address"], "resource_id": row["resource_id"]}
            for row in records
        ],
    )
    artifact_payload: dict[str, object] = {
        "top5_freeze_identity": TOP5_FREEZE_IDENTITY,
        "new_blinded_population_identity": NEW_POPULATION_IDENTITY,
        "blinded_input_sha256": input_sha,
        "new_pair_population_identity": pair_identity,
        "judgment_semantics": USEFULNESS_SEMANTICS,
        "judgments": records,
        "provenance": {
            "method": "semantic adjudication using only the committed blinded input",
            "model": "GPT-6 Luna, Medium",
            "retrieval_evidence_joined": False,
        },
    }
    artifact: dict[str, object] = {
        "schema": SCHEMA,
        "content_identity": content_identity(artifact_payload),
        "payload": artifact_payload,
    }
    validate_frozen_judgments(blinded, artifact)
    return artifact


def validate_frozen_judgments(input_value: object, artifact_value: object) -> None:
    """Require exact target binding, three-state labels, rationales, and blinding."""
    blinded = validate_blinded_input(input_value)
    if not isinstance(artifact_value, dict) or set(artifact_value) != {
        "content_identity",
        "payload",
        "schema",
    }:
        raise ValueError("Judgment artifact has an unexpected root shape.")
    if artifact_value["schema"] != SCHEMA:
        raise ValueError("Judgment artifact schema changed.")
    payload = artifact_value["payload"]
    if not isinstance(payload, dict) or set(payload) != {
        "blinded_input_sha256",
        "judgment_semantics",
        "judgments",
        "new_blinded_population_identity",
        "new_pair_population_identity",
        "provenance",
        "top5_freeze_identity",
    }:
        raise ValueError("Judgment artifact payload must be an object.")
    if artifact_value["content_identity"] != content_identity(payload):
        raise ValueError("Judgment artifact content identity is invalid.")
    expected_pairs = {
        (str(case["neutral_case_id"]), str(resource["address"]), str(resource["neutral_resource_id"]))
        for case in cast("list[dict[str, object]]", cast("dict[str, object]", blinded["payload"])["cases"])
        for resource in cast("list[dict[str, object]]", case["resources"])
    }
    if payload.get("top5_freeze_identity") != TOP5_FREEZE_IDENTITY:
        raise ValueError("Judgment artifact is not bound to the frozen top-five freeze.")
    if payload.get("new_blinded_population_identity") != NEW_POPULATION_IDENTITY:
        raise ValueError("Judgment artifact is not bound to the blinded population.")
    if payload.get("blinded_input_sha256") != BLINDED_INPUT_SHA256:
        raise ValueError("Judgment artifact input hash binding changed.")
    judgments = payload.get("judgments")
    if not isinstance(judgments, list) or len(judgments) != EXPECTED_TARGET_COUNT:
        raise ValueError("Judgment artifact must contain exactly 133 records.")
    actual_pairs: list[tuple[str, str, str]] = []
    for row in judgments:
        if not isinstance(row, dict) or set(row) != {
            "address",
            "case_id",
            "judgment",
            "rationale",
            "resource_id",
        }:
            raise ValueError("Judgment record contains prohibited or unexpected fields.")
        if row["judgment"] not in ALLOWED_LABELS:
            raise ValueError("Judgment label is outside the three-state semantics.")
        if not isinstance(row["rationale"], str) or not row["rationale"].strip():
            raise ValueError("Every judgment requires a concise rationale.")
        actual_pairs.append(
            (str(row["case_id"]), str(row["address"]), str(row["resource_id"])),
        )
    if len(set(actual_pairs)) != EXPECTED_TARGET_COUNT or set(actual_pairs) != expected_pairs:
        raise ValueError("Judgment records do not bind one-to-one to the frozen targets.")
    if payload.get("judgment_semantics") != USEFULNESS_SEMANTICS:
        raise ValueError("Judgment semantics changed.")
    if payload.get("provenance") != {
        "method": "semantic adjudication using only the committed blinded input",
        "model": "GPT-6 Luna, Medium",
        "retrieval_evidence_joined": False,
    }:
        raise ValueError("Judgment provenance changed.")


def write_frozen_judgments(*, experiment_root: Path) -> dict[str, object]:
    """Write the frozen judgment artifact and return its aggregate label counts."""
    input_path = experiment_root / "increment_27" / INPUT_FILENAME
    output_path = experiment_root / "increment_27" / OUTPUT_FILENAME
    artifact = build_frozen_judgments(input_path)
    output_path.write_bytes(canonical_json_bytes(artifact) + b"\n")
    counts = Counter(
        row["judgment"]
        for row in cast("list[dict[str, str]]", cast("dict[str, object]", artifact["payload"])["judgments"])
    )
    return {
        "total": EXPECTED_TARGET_COUNT,
        "USEFUL": counts["USEFUL"],
        "NOT_USEFUL": counts["NOT_USEFUL"],
        "UNJUDGED": counts["UNJUDGED"],
        "content_identity": artifact["content_identity"],
    }
