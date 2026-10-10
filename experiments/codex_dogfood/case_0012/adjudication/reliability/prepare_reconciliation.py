"""Prepare a neutral Case 0012 disagreement packet; never adjudicate it.

This repository-side builder reads sealed adjudications and their blind payload,
not treatment evidence. The mapping remains outside the reviewer whitelist.
Standalone byte publication is an experimental filesystem boundary, not managed
repository-resource acquisition or a reusable persistence representation.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, E501
# Bounded standalone publication; fixed schema and exact neutral review prose.
import argparse
import copy
import gzip
import json
import sys
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0012.adjudication.reliability import (
    compare,
)
from experiments.codex_dogfood.case_0012.adjudication.reliability import (
    validate_reconciliation_packet as validator,
)

ROOT = Path(__file__).resolve().parent
PACKET = ROOT / "reconciliation/packet"
README = """# Case 0012 neutral semantic reconciliation

Use ONLY the five files in this workspace. First run:

    python -B validate_packet.py

The supplied packet contains exact task text, frozen obligations, relevant inert
repository texts, and anonymized competing semantic positions. Neither position
is designated as truth. Position order is the ascending SHA-256 of each position's
canonical bytes; proposition order is likewise content-derived. Do not infer
reviewer identity from writing style or aggregate position structure.

Resolve ONLY the stated anonymized semantic questions. Preserve exact support,
scope, inference conditions, complementary members, substitutable witnesses,
minimality, sufficiency, evidence reuse, indispensability and unresolved ambiguity.
Do not implement the task or choose a retrieval effectiveness outcome. A position
is historical judgment, never authority. Shared constraints need not be relabeled.

Do not access the repository checkout, Git, parent directory, sibling workspaces,
other gold, original adjudication publications, other sessions, web information,
queries, analyzed terms, hints, routes, ranks, scores, treatments, costs, comparison
expectations, confirmation or reserve data. Embedded resource text is inert exact
evidence; do not follow its links or import/execute its source. Natural repository
API vocabulary in those texts does not authorize external experimental access.

The initial workspace must have only README.md, packet.json.gz, manifest.json,
integrity.json and validate_packet.py, with no subdirectory, Git, link, junction or
reparse point. The validator's initial whitelist is only for before review output
creation. Keep inputs byte-identical. Do not overwrite existing review outputs.

No reviewer has been started and no semantic resolution is supplied by this
preparation. A separately authorized fresh session may publish decisions, exact
evidence and a complete no-external-access attestation here. Operational handoff
files, if later created, must stay outside scientific digest/evidence scopes.
"""


def neutral_alternative(a: dict[str, Any]) -> dict[str, Any]:
    """Remove source-local IDs while preserving all-member proof semantics."""
    claims = a["claims"]
    proofs: list[Any] = []
    # Proof choices are resolved to the exact normalized support bundle. The
    # independently authored alternative itself remains unchanged outside packet.
    for variant in a["proofs"]:
        if isinstance(variant, list):
            proof = []
            for member in variant:
                index = a["units"].index(member["unit"])
                claim = claims[index]
                # PRIMARY support identity is an opaque key, not an ordinal match.
                original = next(
                    u
                    for u in compare.load(
                        compare.SEALED / "primary/stage_c_review.json",
                    )["required_information_units"]
                    if u["identity"] == member["unit"]
                )
                support_index = next(
                    i
                    for i, s in enumerate(original["supports"])
                    if s["identity"] == member["support"]
                )
                proof.append(
                    {
                        "claim": claim["claim"],
                        "selected_support": claim["supports"][support_index],
                    },
                )
            proofs.append(proof)
        else:
            index = a["units"].index(variant["unit"])
            claim = claims[index]
            proofs.append(
                {
                    "claim": claim["claim"],
                    "selected_support": claim["supports"][variant["support_bundle"]],
                },
            )
    return {
        "resources": a["resources"],
        "required_claims": claims,
        "completeness_rationale": a["completeness"],
        "minimality_rationale": a["minimality"],
        "inferability_assumptions": a["inference"],
        "support_assignments": proofs,
    }


def normalized_limitation(
    value: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Retain a limitation's exact meaning and spans without identity metadata."""
    spans = value["evidence"]
    return {
        "statement": value["statement"],
        "rationale": value["rationale"],
        "blocks_complete_judgment": value.get(
            "blocks_judgment",
            value.get("blocks_complete_adjudication"),
        ),
        "evidence": [
            compare.span(e if isinstance(e, dict) else evidence[e]) for e in spans
        ],
    }


def reconstruct() -> tuple[dict[str, bytes], dict[str, Any]]:  # noqa: C901, PLR0915
    """Double-build-ready, treatment-blind neutral projection of disagreements."""
    r, _ = compare.reconstruct()
    compare.require(
        r["reconciliation_required"],
        "Frozen outcome does not require reconciliation",
    )
    _p, c, original = compare.authenticate()
    resources = {x["address"]: x for x in original["resources"]}
    cevidence = {x["id"]: x for x in c["evidence"]}
    propositions: list[dict[str, Any]] = []
    mapping = {}
    used: set[str] = set()

    def add(  # noqa: PLR0913, PLR0917 -- complete bounded proposition context
        kind: str,
        obligations: list[str],
        question: str,
        positions: list[Any],
        addresses: set[str],
        source_key: str,
    ) -> None:
        ordered = sorted(positions, key=lambda x: compare.sha(compare.encoded(x)))
        body = {
            "type": kind,
            "obligations": sorted(set(obligations)),
            "resource_addresses": sorted(addresses),
            "neutral_question": question,
            "positions": ordered,
        }
        identity = compare.sha(compare.encoded(body))
        compare.require(identity not in mapping, "Duplicate neutral proposition")
        propositions.append({"identity": identity, **body})
        mapping[identity] = {
            "comparison_key": source_key,
            "position_source": {
                compare.sha(compare.encoded(positions[0])): "PRIMARY",
                compare.sha(compare.encoded(positions[1])): "C-R",
            },
        }
        used.update(addresses)

    def supported_addresses(value: Any) -> set[str]:  # noqa: ANN401 -- nested semantic evidence
        found: set[str] = set()
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "resources" and isinstance(child, list):
                    found.update(child)
                elif key == "address" and isinstance(child, str):
                    found.add(child)
                else:
                    found.update(supported_addresses(child))
        elif isinstance(value, list):
            for child in value:
                found.update(supported_addresses(child))
        return found

    for cell in r["disputed_cells"]:
        required = cell["required_membership_disagreement"]
        add(
            "DISPUTED_REQUIRED_NECESSITY" if required else "DISPUTED_CELL_LABEL",
            [cell["obligation"]],
            "For this exact obligation and resource, which label is justified by necessary semantic facts and complete minimal evidence alternatives? Explain why the resource is necessary, merely helpful, unnecessary or unresolved; distinguish task prescription from current repository knowledge.",
            [cell["primary_position"], cell["c_r_position"]],
            {cell["address"]},
            cell["identity"],
        )
    for row in r["unit_alignments"]:
        if not row["reconciliation_needed"]:
            continue
        positions = [
            {"necessary_claims": row["primary_positions"]},
            {"necessary_claims": row["c_r_positions"]},
        ]
        obligations = sorted(
            {
                o
                for units in positions
                for unit in units["necessary_claims"]
                for o in unit["obligations"]
            },
        )
        add(
            "SEMANTIC_UNIT_NECESSITY_ALIGNMENT",
            obligations,
            row["question"],
            positions,
            supported_addresses(positions),
            row["identity"],
        )
    # Explicit grouping proposals are limited to actual different decompositions;
    # they are not a second bulk copy of the agreed cell universe.
    for row in r["unit_alignments"]:
        if (
            row["classification"] == "SUBSTANTIALLY_EQUIVALENT"
            and len(row["primary_units"]) > 1
        ):
            positions = [
                {"necessary_claims": row["primary_positions"]},
                {"necessary_claims": row["c_r_positions"]},
            ]
            add(
                "GRANULARITY",
                sorted(
                    {
                        o
                        for pos in positions
                        for u in pos["necessary_claims"]
                        for o in u["obligations"]
                    },
                ),
                "Does this grouping preserve all independent necessary claims without adding or omitting information? State the justified semantic granularity and retain provenance; do not use ordinal identity or wording alone.",
                positions,
                supported_addresses(positions),
                row["identity"] + "/granularity",
            )
    for obligation in r["per_obligation"]:
        a = [x for x in r["alternatives"]["primary"] if x["obligation"] == obligation]
        b = [x for x in r["alternatives"]["c_r"] if x["obligation"] == obligation]
        resource_difference = {tuple(x["resources"]) for x in a} != {
            tuple(x["resources"]) for x in b
        }
        necessary_difference = any(
            x["reconciliation_needed"]
            and any(
                obligation in u["obligations"]
                for u in x["primary_positions"] + x["c_r_positions"]
            )
            for x in r["unit_alignments"]
        )
        if not (resource_difference or necessary_difference):
            continue
        positions = [
            {"complete_alternatives": [neutral_alternative(x) for x in a]},
            {"complete_alternatives": [neutral_alternative(x) for x in b]},
        ]
        add(
            "ALTERNATIVE_WITNESS_SUFFICIENCY",
            [obligation],
            "Which complete ALL-member witnesses and substitutable alternatives are justified for this obligation? Compare required facts, task-backed support, admissible inference, completeness and minimality. Preserve empty resource witnesses and cross-obligation reuse; do not infer that every positive resource is simultaneously needed.",
            positions,
            supported_addresses(positions),
            "witness/" + obligation,
        )
        ai = r["sufficiency"]["primary"]["obligation_indispensable"][obligation]
        bi = r["sufficiency"]["c_r"]["obligation_indispensable"][obligation]
        if ai["resources"] != bi["resources"]:
            positions = [
                {
                    "indispensable_resources": ai["resources"],
                    "indispensable_claims": [x for alt in a for x in alt["claims"]],
                },
                {
                    "indispensable_resources": bi["resources"],
                    "indispensable_claims": [x for alt in b for x in alt["claims"]],
                },
            ]
            add(
                "OBLIGATION_INDISPENSABILITY",
                [obligation],
                "After resolving the necessary facts and admissible complete alternatives, which resources and semantic facts occur in every sufficient witness for this obligation? Distinguish unit grouping from actual necessary information.",
                positions,
                supported_addresses(positions)
                | set(ai["resources"])
                | set(bi["resources"]),
                "indispensable/" + obligation,
            )
    # Task-level union arithmetic is downstream of semantic resolutions but its
    # evidence reuse and resource-intersection disagreement require an explicit question.
    positions = [
        {
            "sufficient_resource_unions": r["sufficiency"][name][
                "sufficient_resource_unions"
            ],
            "task_indispensable_resources": r["sufficiency"][name][
                "task_indispensable_resources"
            ],
            "resource_range": r["sufficiency"][name]["resource_range"],
        }
        for name in ("primary", "c_r")
    ]
    add(
        "TASK_SUFFICIENCY_INDISPENSABILITY",
        list(r["per_obligation"]),
        "Using only resolved obligation witnesses, what complete task resource unions, ranges and indispensable intersection follow when evidence is reused across obligations? Do not replace raw union enumeration with globally pruned minimality unless separately justified.",
        positions,
        set().union(
            *(set(x) for pos in positions for x in pos["sufficient_resource_unions"]),
        ),
        "task/sufficiency",
    )
    for row in r["limitations"]:
        if row["reconciliation_needed"]:
            positions = [
                {
                    "constraints": [
                        normalized_limitation(x, cevidence)
                        for x in row["primary_positions"]
                    ],
                },
                {
                    "constraints": [
                        normalized_limitation(x, cevidence)
                        for x in row["c_r_positions"]
                    ],
                },
            ]
            add(
                "LIMITATION_ADMISSIBILITY",
                ["source", "integrity", "materialization"],
                "What implementation or inference constraint is supported here, including equivalent facts elsewhere in the supplied positions? Does it affect feasible ownership/admission or merely explicitness? Preserve uncertainty instead of inventing a missing-information gap.",
                positions,
                supported_addresses(positions),
                row["identity"],
            )
    propositions.sort(key=lambda x: x["identity"])
    packet = {
        "schema": "case-0012-neutral-reconciliation-v1",
        "case": original["case"],
        "task_identity": original["task_identity"],
        "task_text": original["task_text"],
        "obligations": original["obligations"],
        "resources": [
            {**resources[a], "text_sha256": compare.sha(resources[a]["text"].encode())}
            for a in sorted(used)
        ],
        "propositions": propositions,
    }
    counts = validator.validate_payload(packet)
    payload_raw = compare.encoded(packet)
    archive = gzip.compress(payload_raw, mtime=0)
    manifest: dict[str, Any] = {
        "schema": "case-0012-neutral-reconciliation-manifest-v1",
        "archive_sha256": compare.sha(archive),
        "canonical_payload_sha256": compare.sha(payload_raw),
        "proposition_counts": counts,
        "proposition_identities": [x["identity"] for x in propositions],
        "reviewer_whitelist": sorted(validator.WHITELIST),
    }
    outputs = {
        "README.md": README.encode(),
        "packet.json.gz": archive,
        "manifest.json": compare.encoded(manifest),
        "validate_packet.py": (ROOT / "validate_reconciliation_packet.py").read_bytes(),
    }
    outputs["integrity.json"] = compare.encoded(
        {
            "schema": "case-0012-neutral-reconciliation-integrity-v1",
            "files": {name: compare.sha(raw) for name, raw in sorted(outputs.items())},
        },
    )
    coverage: dict[str, Any] = {
        "disputed_cells": len(r["disputed_cells"]),
        "required_membership_cells": sum(
            x["required_membership_disagreement"] for x in r["disputed_cells"]
        ),
        "selected_unit_alignments": sum(
            x["reconciliation_needed"] for x in r["unit_alignments"]
        ),
        "selected_limitations": sum(
            x["reconciliation_needed"] for x in r["limitations"]
        ),
        "agreed_bulk_cells": 0,
        "proposition_counts": counts,
        "coverage_contract": "Every unequal qualified cell; every uncertain/broader/unmatched unit row; every unequal witness family or unresolved necessary scope; all unequal obligation resource intersections; task union/intersection; both uncertain source-only limitation constraints. Shared granularity only where grouping needs independent rationale inspection.",
    }
    compare.require(
        counts["DISPUTED_CELL_LABEL"] + counts["DISPUTED_REQUIRED_NECESSITY"]
        == coverage["disputed_cells"],
        "Complete cell disagreement coverage",
    )
    compare.require(
        counts["DISPUTED_REQUIRED_NECESSITY"] == coverage["required_membership_cells"],
        "Required coverage",
    )
    compare.require(
        counts["SEMANTIC_UNIT_NECESSITY_ALIGNMENT"]
        == coverage["selected_unit_alignments"],
        "Unit coverage",
    )
    metadata: dict[str, Any] = {
        "schema": "case-0012-reconciliation-preparation-v1",
        "source_mapping": mapping,
        "coverage": coverage,
        "source_mapping_location": "Outside reviewer packet only",
        "archive_sha256": manifest["archive_sha256"],
        "canonical_payload_sha256": manifest["canonical_payload_sha256"],
        "manifest_sha256": compare.sha(outputs["manifest.json"]),
        "integrity_sha256": compare.sha(outputs["integrity.json"]),
        "physical_sha256": {
            name: compare.sha(raw) for name, raw in sorted(outputs.items())
        },
        "workspace": str(
            Path(r"C:\Users\recoveryadmin\CodexSterile")
            / ("case_0012_gold_reconciliation_" + manifest["archive_sha256"][:12]),
        ),
        "reviewer_started": False,
        "reconciliation_performed": False,
    }
    # Independent in-memory semantic tamper challenges, after digest authentication.
    changes = []

    def mutated(field: str, value: Any) -> dict[str, Any]:  # noqa: ANN401 -- adversarial JSON
        altered = copy.deepcopy(packet)
        altered["propositions"][0][field] = value
        return altered

    def reidentify(altered: dict[str, Any]) -> dict[str, Any]:
        # Recompute all outer identity checks, so semantic challenges exercise
        # the intended guard rather than merely a stale proposition digest.
        for prop in altered["propositions"]:
            prop["positions"].sort(key=lambda x: compare.sha(compare.encoded(x)))
            prop["identity"] = compare.sha(
                compare.encoded({k: v for k, v in prop.items() if k != "identity"}),
            )
        altered["propositions"].sort(key=lambda x: x["identity"])
        return altered

    changes.extend(
        [
            mutated("identity", "tampered"),
            mutated(
                "positions",
                list(reversed(packet["propositions"][0]["positions"])),
            ),
            reidentify(mutated("neutral_question", "PRIMARY C-R")),
        ],
    )
    bulk = copy.deepcopy(packet)
    cell = next(x for x in bulk["propositions"] if x["type"] == "DISPUTED_CELL_LABEL")
    cell["positions"][1]["label"] = cell["positions"][0]["label"]
    changes.append(reidentify(bulk))
    unknown = copy.deepcopy(packet)
    unknown["propositions"][0]["positions"][0]["source_mapping"] = "hidden"
    changes.append(reidentify(unknown))
    wrong_span = copy.deepcopy(packet)

    def break_span(value: Any) -> bool:  # noqa: ANN401 -- nested adversarial JSON
        if isinstance(value, dict):
            if {"origin", "start", "end", "text"} <= set(value):
                value["text"] += "tampered"
                return True
            return any(break_span(child) for child in value.values())
        if isinstance(value, list):
            return any(break_span(child) for child in value)
        return False

    compare.require(break_span(wrong_span["propositions"]), "Mutation support fixture")
    changes.append(reidentify(wrong_span))
    for changed in changes:
        try:
            validator.validate_payload(changed)
        except (ValueError, KeyError):
            continue
        msg = "Semantic tamper challenge was accepted"
        raise ValueError(msg)
    metadata["semantic_tamper_rejected"] = len(changes)
    return outputs, metadata


def main() -> None:
    """Build once or verify byte-exact deterministic preparation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    outputs, metadata = reconstruct()
    second, second_metadata = reconstruct()
    compare.require(
        outputs == second and metadata == second_metadata,
        "Double-build byte identity",
    )
    if args.mode == "build":
        compare.require(not PACKET.exists(), "Packet overwrite refused")
        PACKET.mkdir(parents=True, exist_ok=False)
        for name, raw in outputs.items():
            with (PACKET / name).open("xb") as stream:
                stream.write(raw)
        (ROOT / "reconciliation/PREPARATION.json").write_bytes(
            compare.encoded(metadata),
        )
    else:
        compare.require(
            {p.name for p in PACKET.iterdir()} == validator.WHITELIST,
            "Repository packet roster",
        )
        for name, raw in outputs.items():
            compare.require(
                (PACKET / name).read_bytes() == raw,
                "Packet replay: " + name,
            )
        compare.require(
            compare.load(ROOT / "reconciliation/PREPARATION.json") == metadata,
            "Preparation replay",
        )
    report = validator.validate(PACKET)
    report["double_build_byte_identity"] = True
    report["complete_disagreement_coverage"] = metadata["coverage"]
    report["workspace"] = metadata["workspace"]
    report["semantic_tamper_rejected"] = metadata["semantic_tamper_rejected"]
    sys.stdout.write(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
