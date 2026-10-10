"""Deterministic publication of sealed Case 0012 judgments, without adjudication.

Standard-library bytes/JSON are the bounded research publication boundary.
This creates no framework API and reads no treatment, reserve or confirmation.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, E501, ANN401, D103, PLR2004, COM812
import argparse
import copy
import gzip
import hashlib
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ADJ = ROOT.parent
REC = ADJ / "reliability/reconciliation"
SOURCE_PAYLOAD = Path(
    "C:/Users/recoveryadmin/CodexSterile/case_0012_stage_c_r_2cbc95afb120/resources.json.gz"
)
LABELS = {"REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"}
# Exact schemas inspected in the sealed packet and original blind payload.
SHARED_RESOURCE_FIELDS = (
    "address",
    "byte_size",
    "content_identity",
    "document_identity",
    "encoding",
    "text",
)


def join_resources(packet: Any, original: Any, expected_addresses: set[str]) -> None:
    """Authenticate the explicit packet enrichment and exact scientific join."""
    shared = set(SHARED_RESOURCE_FIELDS)
    for rows, schema in ((original, shared), (packet, shared | {"text_sha256"})):
        require(all(set(r) == schema for r in rows), "Resource schema mismatch")
        for field in ("address", "document_identity"):
            identities = [r[field] for r in rows]
            require(
                len(identities) == len(set(identities)), "Duplicate resource identity"
            )
    require(
        {r["address"] for r in packet} == expected_addresses,
        "Missing/unexpected packet resource",
    )
    full = {r["address"]: r for r in original}
    require(expected_addresses <= full.keys(), "Missing original resource")
    for row in packet:
        digest = row["text_sha256"]
        require(
            isinstance(digest, str)
            and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            "Invalid text_sha256 syntax",
        )
        # prepare_reconciliation.py seals retained Unicode text encoded as UTF-8,
        # with no newline/Unicode normalization and no native identity framing.
        require(
            sha(row["text"].encode("utf-8")) == digest, "Packet text digest mismatch"
        )
        for field in SHARED_RESOURCE_FIELDS:
            require(
                row[field] == full[row["address"]][field],
                "Packet common field: " + field,
            )


def encoded(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def minimal(values: Any) -> list[list[str]]:
    candidates = sorted({tuple(sorted(x)) for x in values}, key=lambda x: (len(x), x))
    kept: list[tuple[str, ...]] = []
    for candidate in candidates:
        if not any(set(k) <= set(candidate) for k in kept):
            kept.append(candidate)
    return [list(x) for x in sorted(kept)]


def authenticate() -> tuple[Any, Any, Any, Any, Any]:
    pm, cm, rm = (
        load(ADJ / "IMPORT.json"),
        load(ADJ / "INDEPENDENT_IMPORT.json"),
        load(REC / "IMPORT.json"),
    )
    for directory, meta in [
        (ADJ / "primary", pm),
        (ADJ / "independent", cm),
        (REC / "review", rm),
    ]:
        for name, digest in meta["immutable_artifact_sha256"].items():
            require(
                sha((directory / name).read_bytes()) == digest,
                "Immutable source: " + name,
            )
    prep = load(REC / "PREPARATION.json")
    for name, digest in prep["physical_sha256"].items():
        require(sha((REC / "packet" / name).read_bytes()) == digest, "Packet: " + name)
    raw = gzip.decompress((REC / "packet/packet.json.gz").read_bytes())
    require(sha(raw) == prep["canonical_payload_sha256"], "Reconciliation payload")
    packet = json.loads(raw)
    require(
        sha(SOURCE_PAYLOAD.read_bytes())
        == pm["packet_digest_scopes"]["archive_sha256"],
        "Full blind archive",
    )
    raw = gzip.decompress(SOURCE_PAYLOAD.read_bytes())
    require(
        sha(raw) == pm["packet_digest_scopes"]["canonical_payload_sha256"],
        "Full blind payload",
    )
    payload = json.loads(raw)
    primary, independent = (
        load(ADJ / "primary/stage_c_review.json"),
        load(ADJ / "independent/stage_c_r_review.json"),
    )
    reconciliation = load(REC / "review/reconciliation.json")
    for key in ("case", "task_identity", "task_text", "frame"):
        require(
            primary[key] == independent[key] == payload[key], "Source binding: " + key
        )
    require(packet["task_text"] == payload["task_text"], "Reconciliation task")
    require(
        reconciliation["task_identity"] == payload["task_identity"],
        "Reconciliation task identity",
    )
    require(
        reconciliation["blindness_attestation"]["clean_treatment_blind"], "Blindness"
    )
    require(
        set(reconciliation["blindness_attestation"]["access"].values()) == {"NO"},
        "Blindness access",
    )
    for source in (primary, independent):
        for resource, original in zip(
            source["resources"], payload["resources"], strict=True
        ):
            for key in (
                "address",
                "document_identity",
                "content_identity",
                "byte_size",
                "encoding",
            ):
                require(resource[key] == original[key], "Source resource: " + key)
    join_resources(
        packet["resources"],
        payload["resources"],
        {a for p in packet["propositions"] for a in p["resource_addresses"]},
    )
    return primary, independent, reconciliation, packet, payload


def normalize_span(e: Any) -> Any:
    return {
        "origin": "TASK"
        if e.get("origin") == "TASK" or e.get("kind") == "task"
        else "RESOURCE",
        "address": e.get("address", e.get("resource_address")),
        "content_identity": e.get("content_identity"),
        "document_identity": e.get("document_identity", e.get("resource_identity")),
        "start": e["start"],
        "end": e["end"],
        "text": e["text"],
        "coordinate_system": "Unicode code points; zero-based; half-open",
    }


def validate_spans(value: Any, payload: Any) -> int:
    resources = {x["address"]: x for x in payload["resources"]}
    count = 0
    if isinstance(value, dict):
        if {"start", "end", "text", "origin"} <= value.keys():
            if value["origin"] == "TASK":
                text = payload["task_text"]
            else:
                resource = resources[value["address"]]
                require(
                    value["content_identity"] == resource["content_identity"],
                    "Support content identity",
                )
                require(
                    value["document_identity"] == resource["document_identity"],
                    "Support resource identity",
                )
                text = resource["text"]
            require(
                type(value["start"]) is int and type(value["end"]) is int,
                "Support coordinates",
            )
            require(0 <= value["start"] < value["end"] <= len(text), "Support bounds")
            require(
                text[value["start"] : value["end"]] == value["text"], "Support text"
            )
            count += 1
        for child in value.values():
            count += validate_spans(child, payload)
    elif isinstance(value, list):
        for child in value:
            count += validate_spans(child, payload)
    return count


def reconstruct_witnesses(units: Any, obligations: Any) -> Any:
    result = {}
    for ob in obligations:
        selected = [u for u in units if ob in u["obligations"]]
        candidates: list[list[str]] = [[]]
        for unit in selected:
            candidates = minimal(
                set(c) | set(s["resources"])
                for c in candidates
                for s in unit["supports"]
            )
        alternatives = []
        for members in candidates:
            assignments = {
                u["id"]: [
                    i
                    for i, s in enumerate(u["supports"])
                    if set(s["resources"]) <= set(members)
                ]
                for u in selected
            }
            removals = {
                r: [
                    u["id"]
                    for u in selected
                    if not any(
                        set(s["resources"]) <= (set(members) - {r})
                        for s in u["supports"]
                    )
                ]
                for r in members
            }
            require(
                all(assignments.values()) and all(removals.values()),
                "Witness completeness/minimality",
            )
            alternatives.append(
                {
                    "resources": members,
                    "required_unit_ids": [u["id"] for u in selected],
                    "support_assignment_options": assignments,
                    "removal_witnesses": removals,
                    "member_semantics": "ALL",
                    "alternative_semantics": "ANY",
                }
            )
        result[ob] = alternatives
    return result


def task_structure(witnesses: Any, obligations: Any) -> Any:
    combinations = []
    for picks in itertools.product(*(range(len(witnesses[ob])) for ob in obligations)):
        selected = [witnesses[ob][i] for ob, i in zip(obligations, picks, strict=True)]
        combinations.append(
            {
                "witnesses": {
                    ob: f"{ob}.reviewed-{i + 1:02}"
                    for ob, i in zip(obligations, picks, strict=True)
                },
                "resources": sorted(
                    set().union(*(set(w["resources"]) for w in selected))
                ),
                "units": sorted(
                    set().union(*(set(w["required_unit_ids"]) for w in selected))
                ),
            }
        )
    resource_unions = sorted({tuple(c["resources"]) for c in combinations})
    unit_unions = sorted({tuple(c["units"]) for c in combinations})
    return {
        "complete_task_combinations": combinations,
        "distinct_sufficient_resource_unions": [list(x) for x in resource_unions],
        "minimal_complete_resource_unions": minimal(resource_unions),
        "distinct_sufficient_unit_unions": [list(x) for x in unit_unions],
        "minimum_sufficient_resources": min(map(len, resource_unions)),
        "maximum_sufficient_resources": max(map(len, resource_unions)),
        "minimum_sufficient_units": min(map(len, unit_unions)),
        "maximum_sufficient_units": max(map(len, unit_unions)),
        "task_indispensable_resources": sorted(
            set.intersection(*(set(x) for x in resource_unions))
        ),
        "task_indispensable_units": sorted(
            set.intersection(*(set(x) for x in unit_unions))
        ),
        "task_only_sufficient": any(not x for x in resource_unions),
    }


def construct_gold() -> Any:  # noqa: PLR0915 -- one bounded sealed judgment join
    primary, independent, reconciliation, packet, payload = authenticate()
    obs = [o["key"] for o in payload["obligations"]]
    decisions = {d["proposition_identity"]: d for d in reconciliation["decisions"]}
    propositions = {p["identity"]: p for p in packet["propositions"]}
    require(
        len(decisions) == len(propositions) == 148
        and decisions.keys() == propositions.keys(),
        "Decision roster",
    )
    mapping = load(REC / "PREPARATION.json")["source_mapping"]
    cell_decisions = {}
    for identity, decision in decisions.items():
        prop = propositions[identity]
        require(
            decision["type"] == prop["type"]
            and decision["obligations"] == prop["obligations"],
            "Decision context",
        )
        require(
            decision["decision_sha256"]
            == sha(
                encoded({k: v for k, v in decision.items() if k != "decision_sha256"})
            ),
            "Decision seal",
        )
        if decision["type"].startswith("DISPUTED_"):
            j = decision["final_reconciled_judgment"]
            key = (j["obligation"], j["resource_address"])
            require(
                prop["obligations"] == [key[0]]
                and prop["resource_addresses"] == [key[1]],
                "Cell proposition",
            )
            require(
                mapping[identity]["comparison_key"].split("|")[:2]
                == [payload["task_identity"] + "/" + key[0], key[1]],
                "Proposition source mapping",
            )
            require(key not in cell_decisions, "Duplicate cell decision")
            cell_decisions[key] = decision
    cr = {(x["obligation"], x["resource_address"]): x for x in independent["cells"]}
    evidence = {e["id"]: e for e in independent["evidence"]}
    cells = []
    for original in primary["cells"]:
        ob = original["obligation"].rsplit("/", 1)[-1]
        key = (ob, original["address"])
        other = cr[key]
        require(
            original["document_identity"] == other["resource_identity"],
            "Cell source identity",
        )
        decision = cell_decisions.get(key)
        require(
            (original["label"] != other["label"]) == (decision is not None),
            "Unreconciled or agreed relabeling",
        )
        cell = {
            "case": payload["case"],
            "task_identity": payload["task_identity"],
            "obligation": ob,
            "obligation_identity": original["obligation"],
            "address": original["address"],
            "document_identity": original["document_identity"],
            "content_identity": original["content_identity"],
        }
        if decision:
            cell.update(
                label=decision["final_reconciled_judgment"]["label"],
                evidence=[
                    normalize_span(e)
                    for e in decision["repository_evidence"] + decision["task_evidence"]
                ],
                rationale=decision["rationale"],
                inferability=decision["ambiguity"],
                provenance={
                    "kind": "RECONCILED_DISAGREEMENT",
                    "proposition_identity": decision["proposition_identity"],
                    "decision_sha256": decision["decision_sha256"],
                    "source_labels": [original["label"], other["label"]],
                },
            )
        else:
            cell.update(
                label=original["label"],
                evidence={
                    "PRIMARY": [normalize_span(e) for e in original["evidence"]],
                    "C-R": [normalize_span(evidence[e]) for e in other["evidence"]],
                },
                rationale={"PRIMARY": original["rationale"], "C-R": other["rationale"]},
                inferability={
                    "PRIMARY": original["inferability_rationale"],
                    "C-R": other["inferability_rationale"],
                },
                provenance={
                    "kind": "INHERITED_AGREEMENT",
                    "source_labels": [original["label"], other["label"]],
                },
            )
        cells.append(cell)
    units = copy.deepcopy(reconciliation["semantic_units"])
    for unit in units:
        unit["reviewed_identity"] = (
            payload["task_identity"] + "/reviewed-unit/" + unit["id"]
        )
        unit["support_status"] = (
            "TASK_ONLY"
            if all(not s["resources"] for s in unit["supports"])
            else "REPOSITORY_SUPPORTED"
        )
        unit["provenance"] = {
            "reconciliation_sha256": sha(
                (REC / "review/reconciliation.json").read_bytes()
            ),
            "decisions": [
                d["proposition_identity"]
                for d in decisions.values()
                if unit["id"]
                in d["final_reconciled_judgment"].get("necessary_unit_ids", [])
                or unit["id"]
                in d["final_reconciled_judgment"].get("indispensable_unit_ids", [])
            ],
            "basis": "Sealed final shared reconciliation structure; no source precedence",
        }
    native_units = reconciliation["semantic_units"]
    witnesses = reconstruct_witnesses(native_units, obs)
    require(
        witnesses == reconciliation["witnesses_by_obligation"],
        "Reconciled exact witness reconstruction",
    )
    structure = task_structure(witnesses, obs)
    require(
        structure["minimal_complete_resource_unions"]
        == reconciliation["task_sufficiency"]["sufficient_resource_unions"],
        "Reconciled task union",
    )
    require(
        structure["task_indispensable_resources"]
        == reconciliation["task_sufficiency"]["task_indispensable_resources"],
        "Task intersection",
    )
    intersections = {
        ob: sorted(set.intersection(*(set(w["resources"]) for w in witnesses[ob])))
        for ob in obs
    }
    for decision in decisions.values():
        j, typ = decision["final_reconciled_judgment"], decision["type"]
        if typ == "ALTERNATIVE_WITNESS_SUFFICIENCY":
            require(
                j["complete_alternatives"] == witnesses[decision["obligations"][0]],
                "Applied witness decision",
            )
        if typ in {"ALTERNATIVE_WITNESS_SUFFICIENCY", "OBLIGATION_INDISPENSABILITY"}:
            require(
                j["indispensable_resources"]
                == intersections[decision["obligations"][0]],
                "Applied indispensability decision",
            )
        if typ in {"GRANULARITY", "SEMANTIC_UNIT_NECESSITY_ALIGNMENT"}:
            require(
                j["replacement_claims"]
                == [
                    next(u["claim"] for u in units if u["id"] == identity)
                    for identity in j["necessary_unit_ids"]
                ],
                "Applied semantic decision",
            )
    limitations = [
        dict(
            d["final_reconciled_judgment"],
            provenance={
                "proposition_identity": d["proposition_identity"],
                "decision_sha256": d["decision_sha256"],
            },
            evidence=[
                normalize_span(e) for e in d["repository_evidence"] + d["task_evidence"]
            ],
        )
        for d in decisions.values()
        if d["type"] == "LIMITATION_ADMISSIBILITY"
    ]
    decorator = next(u for u in units if u["id"] == "materialization.decorators")
    limitations.append(
        {
            "statement": decorator["claim"],
            "necessity_rationale": decorator["necessity_rationale"],
            "evidence": [e for s in decorator["supports"] for e in s["evidence"]],
            "provenance": decorator["provenance"],
            "blocks_complete_judgment": False,
        }
    )
    incomplete = [
        u["id"]
        for u in units
        if not u["supports"] or any(not s["evidence"] for s in u["supports"])
    ]
    unrepresented = [ob for ob in obs if not any(ob in u["obligations"] for u in units)]
    unresolved = [
        d["proposition_identity"]
        for d in decisions.values()
        if d["ambiguity"]["state"] != "RESOLVED"
    ]
    gaps = {
        "task_gap": unrepresented,
        "repository_information_gap": incomplete,
        "task_interpretation_gap": unresolved,
    }
    require(not any(gaps.values()), "Reviewed gap")
    return {
        "schema": "case-0012-reviewed-gold-v1",
        "case": payload["case"],
        "task_identity": payload["task_identity"],
        "task_text": payload["task_text"],
        "frame": payload["frame"],
        "obligations": payload["obligations"],
        "resources": [
            {k: v for k, v in r.items() if k != "text"} for r in payload["resources"]
        ],
        "cells": cells,
        "semantic_units": units,
        "witnesses_by_obligation": witnesses,
        "obligation_indispensable_resources": intersections,
        "obligation_indispensable_units": {
            ob: sorted({u for w in witnesses[ob] for u in w["required_unit_ids"]})
            for ob in obs
        },
        "task_sufficiency": structure,
        "gaps": gaps,
        "limitations": limitations,
        "reconciled_decisions": list(decisions.values()),
        "decision_applications": {
            identity: {
                "type": d["type"],
                "source_mapping": mapping[identity],
                "final_judgment": d["final_reconciled_judgment"],
            }
            for identity, d in decisions.items()
        },
        "provenance": {
            "source_sha256": {
                "PRIMARY": sha((ADJ / "primary/stage_c_review.json").read_bytes()),
                "C-R": sha((ADJ / "independent/stage_c_r_review.json").read_bytes()),
                "reconciliation": sha(
                    (REC / "review/reconciliation.json").read_bytes()
                ),
            },
            "policy": "Agreed source labels inherited; all disputed propositions use sealed reconciliation exclusively. No adjudication, reliability rerun or treatment access.",
        },
    }


def statistics(gold: Any) -> Any:
    return {
        "cells": len(gold["cells"]),
        "labels": dict(sorted(Counter(c["label"] for c in gold["cells"]).items())),
        "provenance": dict(
            sorted(Counter(c["provenance"]["kind"] for c in gold["cells"]).items())
        ),
        "required_resource_union": sorted(
            {c["address"] for c in gold["cells"] if c["label"] == "REQUIRED"}
        ),
        "per_obligation": {
            o["key"]: dict(
                sorted(
                    Counter(
                        c["label"] for c in gold["cells"] if c["obligation"] == o["key"]
                    ).items()
                )
            )
            for o in gold["obligations"]
        },
        "units": len(gold["semantic_units"]),
        "support_split": dict(
            sorted(Counter(u["support_status"] for u in gold["semantic_units"]).items())
        ),
        "witnesses": {
            ob: len(ws) for ob, ws in gold["witnesses_by_obligation"].items()
        },
        "task_combinations": len(
            gold["task_sufficiency"]["complete_task_combinations"]
        ),
    }


def validate(gold: Any) -> int:
    _, _, _, _, payload = authenticate()
    expected = {
        (o["key"], r["address"], r["document_identity"], r["content_identity"])
        for o in gold["obligations"]
        for r in payload["resources"]
    }
    actual = [
        (c["obligation"], c["address"], c["document_identity"], c["content_identity"])
        for c in gold["cells"]
    ]
    require(
        len(actual) == len(set(actual)) == len(expected) == 4779
        and set(actual) == expected,
        "Complete qualified cell frame",
    )
    require(all(c["label"] in LABELS for c in gold["cells"]), "Unresolved cell")
    for ob, witnesses in gold["witnesses_by_obligation"].items():
        require(
            {
                c["address"]
                for c in gold["cells"]
                if c["obligation"] == ob and c["label"] == "REQUIRED"
            }
            == set().union(*(set(w["resources"]) for w in witnesses)),
            "Required/witness membership",
        )
    stats = statistics(gold)
    require(
        stats["provenance"]
        == {"INHERITED_AGREEMENT": 4673, "RECONCILED_DISAGREEMENT": 106},
        "Agreement/reconciliation coverage",
    )
    require(
        len(gold["decision_applications"]) == len(gold["reconciled_decisions"]) == 148,
        "No unused reconciliation decision",
    )
    require(
        stats["units"] == 61
        and stats["support_split"] == {"TASK_ONLY": 28, "REPOSITORY_SUPPORTED": 33},
        "Unit inventory",
    )
    require(
        len({u["reviewed_identity"] for u in gold["semantic_units"]}) == 61,
        "Unit identity",
    )
    require(
        stats["witnesses"]
        == {
            "source": 4,
            "integrity": 4,
            "materialization": 2,
            "choices": 1,
            "assembly": 1,
            "exports": 1,
            "tests": 1,
            "documentation": 1,
            "validation": 1,
        },
        "Witness counts",
    )
    task = gold["task_sufficiency"]
    require(stats["task_combinations"] == 32, "Task combination mathematics")
    require(
        len(task["minimal_complete_resource_unions"]) == 4
        and all(len(x) == 14 for x in task["minimal_complete_resource_unions"]),
        "Minimal task unions",
    )
    require(
        len(task["task_indispensable_resources"]) == 12
        and not task["task_only_sufficient"],
        "Task indispensability",
    )
    require(
        encoded(gold) == encoded(construct_gold()),
        "Exact source inheritance and 148 applied decisions/structure",
    )
    return validate_spans(gold, payload)


def markdown(gold: Any) -> bytes:
    lines = [
        "# Case 0012 reviewed gold",
        "",
        "Final semantic target: agreed source labels plus authoritative sealed reconciliation. ALL witness members are jointly necessary; ANY complete witness for an obligation substitutes. No treatment evidence enters this target.",
        "",
        "## Exact task",
        "",
        "```text",
        gold["task_text"].rstrip(),
        "```",
        "",
        "## Final statistics",
        "",
        "```json",
        encoded(statistics(gold)).decode().rstrip(),
        "```",
        "",
    ]
    for name in (
        "obligations",
        "semantic_units",
        "witnesses_by_obligation",
        "obligation_indispensable_resources",
        "obligation_indispensable_units",
        "task_sufficiency",
        "gaps",
        "limitations",
        "decision_applications",
        "provenance",
    ):
        lines += [
            "## " + name.replace("_", " ").title(),
            "",
            "```json",
            encoded(gold[name]).decode().rstrip(),
            "```",
            "",
        ]
    lines += [
        "## Every REQUIRED and HELPFUL_ONLY cell",
        "",
        "The complete 4,779-cell queryable mapping is reviewed_gold.json.cells. Below are all positive cells with exact support, rationale, inferability and provenance.",
        "",
    ]
    for cell in gold["cells"]:
        if cell["label"] != "UNNECESSARY":
            lines += [
                f"### {cell['obligation']} / {cell['address']} / {cell['label']}",
                "",
                "```json",
                encoded(cell).decode().rstrip(),
                "```",
                "",
            ]
    return "\n".join(lines).encode()


def write_new(files: dict[Path, bytes]) -> None:
    if any(path.exists() for path in files):
        message = "Refusing to overwrite reviewed artifacts"
        raise FileExistsError(message)
    for path, raw in files.items():
        with path.open("xb") as stream:
            stream.write(raw)


def outputs() -> dict[str, bytes]:
    gold = construct_gold()
    spans = validate(gold)
    files = {
        "reviewed_gold.json": encoded(gold),
        "reviewed_statistics.json": encoded(statistics(gold)),
        "REVIEWED_GOLD.md": markdown(gold),
    }
    files["reviewed_validation.json"] = encoded(
        {
            "status": "PASS",
            "cells": 4779,
            "missing": 0,
            "unexpected": 0,
            "duplicates": 0,
            "unresolved": 0,
            "decisions_applied": 148,
            "inherited_agreements": 4673,
            "reconciled_cell_disagreements": 106,
            "unused_decisions": 0,
            "support_spans": spans,
            "checks": [
                "sealed source integrity",
                "blindness attestation",
                "complete frame",
                "source agreement inheritance",
                "all disagreement verdicts",
                "proposition mapping",
                "unit structure and split",
                "exact witness memberships and removal proofs",
                "all 32 task combinations",
                "four minimal 14-resource unions",
                "12 indispensable resources",
                "all obligation intersections",
                "gap and limitation structure",
                "deterministic statistics",
                "deterministic JSON/Markdown",
            ],
            "adversarial_validation": "Focused test_materialize.py: overwrite refusal and resealed cell/unit/witness/span/gap/decision tamper rejection",
        }
    )
    files["reviewed_hashes.json"] = encoded(
        {
            "schema": "case-0012-reviewed-hashes-v1",
            "files": {name: sha(raw) for name, raw in files.items()},
            "builder_sha256": sha(Path(__file__).read_bytes()),
            "scope": "Physical outputs and materializer; .local excluded",
        }
    )
    return files


def verify() -> Any:
    files = outputs()
    for name, raw in files.items():
        require((ROOT / name).read_bytes() == raw, "Exact reconstruction: " + name)
    return {
        "status": "PASS",
        "statistics": load(ROOT / "reviewed_statistics.json"),
        "sha256": {name: sha(raw) for name, raw in files.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    if args.mode == "build":
        write_new({ROOT / name: raw for name, raw in outputs().items()})
    sys.stdout.write(encoded(verify()).decode())


if __name__ == "__main__":
    main()
