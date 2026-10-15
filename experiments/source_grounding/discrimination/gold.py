# Copyright (c) 2026
# ruff: noqa: ANN401 -- bounded scientific wire contract
"""Single-call local discrimination gold, not global necessity or sufficiency."""

from typing import Any

from experiments.orchestration.storage import require
from experiments.orchestration.workers import evidence, schema
from experiments.source_grounding.response import object_schema

LABELS = ("USEFUL", "NOT_USEFUL", "UNCERTAIN")
QUOTE = 64
REASON = 32
INSTRUCTION = (
    "Blind candidate-discrimination primary. For each candidate independently judge "
    "source_usefulness: own source content materially helps satisfy or reason about "
    "the obligation; target_usefulness: own target content materially helps; "
    "pursuit_value: given complete source, target and native direct Reference, "
    "following this relation is a useful evidence-pursuit step. USEFUL / NOT_USEFUL "
    "/ UNCERTAIN are three independent judgments; never infer one from another. "
    "Not useful means no material help identified after reviewing complete content; "
    "uncertain means neither conclusion established confidently. No global REQUIRED, "
    "minimal witness, repository recall or task-sufficiency judgment. "
    "Provide at most one exact source and one exact target locator per candidate: "
    "source_key, quote of 1..64 Unicode characters, positive overlapping occurrence. "
    "Copy quote as an exact nonempty Unicode substring of that disclosed resource. "
    "Occurrence is 1-based among exact left-to-right overlapping matches, advancing "
    "one Unicode code point after each match. "
    "No normalization, fuzzy matching or repair. "
    "These are audit anchors into the complete disclosed resources, not compressed "
    "substitutes for them. USEFUL requires an own-endpoint anchor; UNCERTAIN may "
    "supply one where applicable; NOT_USEFUL requires none. Explain the pursuit "
    "distinction only, in <=32 Unicode characters; no decorative negative prose. "
    "If adequate adjudication/auditable representation is impossible within the "
    "frozen contract, set representation_complete=false: do not truncate adequate "
    "evidence or change a label to fit. Self-review all independent labels, exact "
    "quote/occurrence copying and every candidate. Repeated own-resource judgments "
    "for the same obligation must agree. All authorized information is supplied. "
    "Use no tools, filesystem, web or other reviewer; create no files. Return only "
    "the structured JSON response.\n"
)


def contract(count: int, keys: list[str], maximum_source: int) -> Any:
    """Construct a finite native schema and exact worst-case Unicode envelope."""
    label = {"type": "string", "enum": list(LABELS)}
    locator = object_schema(
        {
            "source_key": {"type": "string", "enum": keys},
            "quote": {"type": "string", "minLength": 1, "maxLength": QUOTE},
            "occurrence": {"type": "integer", "minimum": 1, "maximum": maximum_source},
        },
    )
    anchor = {"type": "array", "minItems": 0, "maxItems": 1, "items": locator}
    judgment = object_schema(
        {
            "candidate_id": {
                "type": "string",
                "enum": [f"c{i:04}" for i in range(count)],
            },
            "source_usefulness": label,
            "target_usefulness": label,
            "pursuit_value": label,
            "source_evidence": anchor,
            "target_evidence": anchor,
            "pursuit_reason": {"type": "string", "maxLength": REASON},
        },
    )
    return object_schema(
        {
            "judgments": {
                "type": "array",
                "minItems": count,
                "maxItems": count,
                "items": judgment,
            },
            "representation_complete": {"type": "boolean"},
            "self_review_complete": {"type": "boolean"},
        },
    )


def render(packet: Any) -> bytes:
    """Disclose each complete resource once; no host ranks, scores or treatment."""
    return INSTRUCTION.encode() + schema.canonical(packet)


def project(
    packet: Any,
    payload: Any,
    response_schema: Any,
    canonical_resources: Any,
) -> Any:
    """Validate every explicit judgment and deterministically reattach exact spans."""
    schema.validate(payload, response_schema)
    require(
        payload["representation_complete"] and payload["self_review_complete"],
        "EVIDENCE_REPRESENTATION_LIMIT",
    )
    table = canonical_resources
    require(len(table) == len(packet["resources"]), "Duplicate disclosed resource key")
    require(
        all(
            table[r["source_key"]]["content"] == r["content"]
            and table[r["source_key"]]["address"] == r["address"]
            for r in packet["resources"]
        ),
        "Canonical identity mapping differs from exact disclosure",
    )
    by = {r["candidate_id"]: r for r in payload["judgments"]}
    require(
        len(by) == len(packet["candidates"])
        and set(by) == {r["candidate_id"] for r in packet["candidates"]},
        "Complete unique candidate gold required",
    )
    consistency: dict[tuple[str, str], str] = {}
    result = []
    for candidate in packet["candidates"]:
        row = by[candidate["candidate_id"]]
        projected = {**row}
        for role in ("source", "target"):
            key = candidate[role + "_key"]
            label = row[role + "_usefulness"]
            locators = row[role + "_evidence"]
            require(
                label != "USEFUL" or len(locators) == 1,
                "Useful endpoint needs audit evidence",
            )
            cell = (candidate["obligation_id"], key)
            require(
                cell not in consistency or consistency[cell] == label,
                "Inconsistent own-resource gold",
            )
            consistency[cell] = label
            resolved = []
            for loc in locators:
                require(loc["source_key"] == key, "Foreign endpoint evidence")
                resolved.append(evidence.resolve(loc, table))
            projected[role + "_evidence"] = resolved
        result.append(projected)
    return {
        "schema": "candidate-discrimination-gold-v1",
        "case": packet["case"],
        "judgments": result,
    }
