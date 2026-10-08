"""Build a neutral disagreement packet; source mapping stays outside the packet."""

# Standalone non-installable JSON evidence scripts; long sealed claims remain literal.
# ruff: noqa: INP001, CPY001, E501, COM812, ANN401, D103, S101
from __future__ import annotations

import argparse
import gzip
import json
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

from compare_gold import (
    ROOT,
    canonical,
    compare,
    load,
    normalized,
    sha,
    structure,
    write_new,
)

DEST = ROOT.parent / "reconciliation"
DECISIONS = [
    "ACCEPT_POSITION_1",
    "ACCEPT_POSITION_2",
    "REPLACE_WITH_RECONCILED_JUDGMENT",
    "UNRESOLVED",
]
INSTRUCTIONS = """# Case 0011 disagreement reconciliation

Use only the six supplied files. Verify integrity.json before parsing packet.json
or resources.json.gz. The archive hash binds compressed bytes; the payload hash
binds the exact decompressed UTF-8 JSON bytes. Verify resource text and raw UTF-8
digests against manifest.json. Do not import or execute frozen resource code.

Resolve only the listed propositions. Positions are competing claims, with no
truth reference or automatic preference. They are ordered by canonical claim
digest, unrelated to quality or necessity. Unit and alternative identifiers are
content-derived and do not establish equivalence. Examine the exact original
task, frozen obligations, full supplied resources, necessity claims, exact source
support and complementary/competing alternative structures. ALL members within
one alternative are complementary; ANY complete alternative is sufficient under
that position. Never flatten alternatives to a union when deciding sufficiency.

For each proposition choose ACCEPT_POSITION_1, ACCEPT_POSITION_2,
REPLACE_WITH_RECONCILED_JUDGMENT, or UNRESOLVED. Explain necessity and exact source
support. For units/alternatives, a narrower reconciled statement may be necessary.
No majority voting and no automatic preference for fewer resources. Diagnostic
alignment proposals are not decisions. Preserve uncertainty and separate task
gaps from interpretation limitations and missing repository information.
Absence of a matching unit is not an explicit UNNECESSARY judgment. Consult the
competing cell and alternative claims. Multiple candidate unit pairs can share a
unit; explain consistency across those decisions rather than voting on pairs.

The agreed-cell seal binds qualified identities and labels inherited from both
positions. Preserve these cells unless a concrete contradiction uncovered during
reconciliation affects them; record every exception and its supporting evidence.
Do not silently re-adjudicate the entire 4,779-cell frame. The seal and list permit
later proof of inherited versus reconciled cells; the full corpus is not supplied.

Do not access outside files, repository history, other adjudications, information
needs, queries, treatment results, ranks, scores, model identities, adjudication
chronology or confirmation. Do not implement the task, perform C.5 or Stage D.
Write reconciled judgments and an explicit decision for every proposition only
in this workspace. Do not modify any of the six packet files. Ask the caller for
additional frozen evidence if a concrete disputed claim cannot be adjudicated
from these full resources; do not seek evidence yourself.
"""

METADATA_KEYS = {
    "schema",
    "frame",
    "case_identity",
    "task_identity",
    "repository_id",
    "snapshot_id",
    "corpus_id",
    "task",
    "obligations",
    "identity",
    "applicability_condition",
    "author",
    "criterion",
    "name",
    "statement",
    "predicate",
    "provenance",
    "requirement",
    "task_basis",
    "end",
    "line",
    "origin",
    "start",
    "text",
    "positions",
    "position_1",
    "position_2",
    "cells",
    "obligation",
    "address",
    "content_identity",
    "label",
    "rationale",
    "units",
    "id",
    "necessity",
    "scope",
    "supports",
    "start_character",
    "end_character",
    "excerpt",
    "excerpt_sha256",
    "alternatives",
    "resources",
    "applicability",
    "task_gaps",
    "limitations",
    "repository_gaps",
    "supplemental_units",
    "indispensability",
    "task_resources",
    "task_units",
    "by_obligation",
    "indispensable_resources",
    "indispensable_units",
    "propositions",
    "kind",
    "subject",
    "claims",
    "question",
    "decisions",
    "agreed_cells",
    "agreed_cell_sha256",
    "ordering_rule",
    "unit_proposals",
    "classification",
    "source_overlap",
    "common_obligations",
    "span_1",
    "span_2",
    "resource_count",
    "byte_size",
    "encoding",
    "content_sha256",
    "files",
    "archive_sha256",
    "canonical_payload_sha256",
    "packet_sha256",
    "manifest_sha256",
    "rationale_support",
    "task_lines",
}
FORBIDDEN_METADATA = re.compile(
    r"\b(primary|review|astra|gpt[- ]?6|stage_c_r|chronology|first adjudicat|second adjudicat)\b",
    re.IGNORECASE,
)


def neutral_text(text: str) -> str:
    # Only deictic source self-references are changed, never necessity substance.
    return re.sub(r"\b[Tt]his review\b", "This position", text)


def support(span: dict[str, Any]) -> dict[str, Any]:
    return {
        k: span[k]
        for k in (
            "address",
            "start_character",
            "end_character",
            "excerpt",
            "excerpt_sha256",
        )
    }


def neutral_position(
    gold: dict[str, Any], raw: dict[str, Any], *, independent: bool
) -> tuple[dict[str, Any], dict[str, str]]:
    units, mapping = [], {}
    for u in gold["units"]:
        claim = {
            "statement": u["statement"],
            "necessity": u["necessity"],
            "scope": u["scope"],
            "obligations": u["obligations"],
            "supports": [support(s) for s in u["supports"]],
            "rationale": neutral_text(u["rationale"]),
        }
        uid = "unit-" + sha(canonical(claim))
        mapping[u["id"]] = uid
        units.append({"id": uid, **claim})
    obs = []
    for o in gold["obligations"]:
        alts = []
        for a in o["alternatives"]:
            claim = {
                "resources": sorted(a["resources"]),
                "units": sorted(mapping[u] for u in a["units"]),
                "rationale": neutral_text(a["rationale"]),
                "supports": [
                    support({"address": e["resource_address"], **s})
                    for e in a["support"]
                    for s in e["spans"]
                ],
            }
            aid = "alternative-" + sha(canonical(claim))
            mapping[a["id"]] = aid
            alts.append({"id": aid, **claim})
        obs.append(
            {
                "id": o["id"],
                "applicability": o["applicability"],
                "rationale": neutral_text(o["rationale"]),
                "alternatives": sorted(alts, key=lambda a: a["id"]),
            }
        )
    limitations = []
    originals = (
        raw["task_interpretation_limitations"]
        if independent
        else raw["task_interpretation_gaps"]
    )
    evidence = {e["evidence_id"]: e for e in raw.get("source_support", [])}
    for limitation in originals:
        claim = {"statement": neutral_text(limitation["statement"])}
        if independent:
            claim["units"] = sorted(mapping[u] for u in limitation["units"])
            claim["task_lines"] = limitation["task_lines"]
            additional = limitation.get("additional_support")
            if additional:
                # This support declares lines rather than character offsets.
                claim["rationale_support"] = {
                    "address": additional["resource"]["address"],
                    "excerpt": additional["excerpt"],
                    "excerpt_sha256": additional["excerpt_sha256"],
                }
        else:
            claim["rationale"] = limitation["disposition"]
            claim["supports"] = [
                support({"address": evidence[e]["resource_address"], **s})
                for e in limitation["evidence_ids"]
                for s in evidence[e]["spans"]
            ]
        limitations.append(claim)
    if independent:
        task_gaps = {
            "statement": raw["task_gap"],
            "rationale": neutral_text(raw["task_gap_rationale"]),
        }
        repository_gaps = {
            "statement": raw["repository_information_gap"],
            "rationale": raw["repository_gap_rationale"],
        }
    else:
        task_gaps = {
            "statement": [
                {
                    "statement": g["statement"],
                    "rationale": g["applicability_reason"],
                    "scope": g["missing_obligation_scope"],
                    "units": [mapping[u] for u in g["supplemental_required_unit_ids"]],
                }
                for g in raw["task_gaps"]
            ]
        }
        repository_gaps = {
            "statement": raw["repository_information_gaps"],
            "rationale": raw["repository_gap_review"],
        }
    st = structure(gold)
    indispensability = {
        "task_resources": st["indispensable_resources"],
        "task_units": sorted(mapping[u] for u in st["indispensable_units"]),
        "by_obligation": [
            {
                "obligation": o["obligation"],
                "indispensable_resources": o["indispensable_resources"],
                "indispensable_units": sorted(
                    mapping[u] for u in o["indispensable_units"]
                ),
            }
            for o in st["by_obligation"]
        ],
    }
    return {
        "cells": [
            {**c, "units": sorted(mapping[u] for u in c["units"])}
            for c in gold["cells"]
        ],
        "units": sorted(units, key=lambda u: u["id"]),
        "obligations": obs,
        "task_gaps": task_gaps,
        "limitations": limitations,
        "repository_gaps": repository_gaps,
        "supplemental_units": sorted(
            mapping[u["id"]]
            for u in gold["units"]
            if u["scope"] == "SUPPLEMENTAL_TASK_GAP"
        ),
        "indispensability": indispensability,
    }, mapping


def metadata_check(value: Any, *, key: str = "") -> None:
    if isinstance(value, dict):
        assert set(value) <= METADATA_KEYS, set(value) - METADATA_KEYS
        for k, v in value.items():
            metadata_check(v, key=k)
    elif isinstance(value, list):
        for v in value:
            metadata_check(v, key=key)
    elif isinstance(value, str) and key not in {
        "excerpt",
        "text",
        "task",
        "address",
        "subject",
        "rationale_support",
    }:
        assert not FORBIDDEN_METADATA.search(value), value


def validate_packet(
    packet: dict[str, Any], resources: list[dict[str, Any]], comparison: dict[str, Any]
) -> None:
    assert set(packet) == {
        "schema",
        "frame",
        "task",
        "obligations",
        "positions",
        "propositions",
        "agreed_cells",
        "agreed_cell_sha256",
        "ordering_rule",
        "unit_proposals",
    }
    assert set(packet["positions"]) == {"position_1", "position_2"}
    metadata_check(packet)
    assert packet["agreed_cells"] == comparison["agreed_cells"]
    assert packet["agreed_cell_sha256"] == sha(canonical(packet["agreed_cells"]))
    props = packet["propositions"]
    assert len({p["id"] for p in props}) == len(props)
    assert {tuple(p["subject"]) for p in props if p["kind"] == "CELL"} == {
        (c["obligation"], c["address"]) for c in comparison["disputed_cells"]
    }
    content = {r["address"]: r["content"] for r in resources}
    for name, position in packet["positions"].items():
        assert set(position) == {
            "cells",
            "units",
            "obligations",
            "task_gaps",
            "limitations",
            "repository_gaps",
            "supplemental_units",
            "indispensability",
        }
        assert len(position["cells"]) == comparison["disagreement_count"]
        unit_ids = {u["id"] for u in position["units"]}
        for u in position["units"]:
            assert u["id"] == "unit-" + sha(
                canonical({k: v for k, v in u.items() if k != "id"})
            )
            for s in u["supports"]:
                assert (
                    content[s["address"]][s["start_character"] : s["end_character"]]
                    == s["excerpt"]
                )
                assert sha(s["excerpt"].encode()) == s["excerpt_sha256"]
        assert {(c["obligation"], c["address"]) for c in position["cells"]} == {
            tuple(p["subject"]) for p in props if p["kind"] == "CELL"
        }
        for o in position["obligations"]:
            for a in o["alternatives"]:
                assert set(a["units"]) <= unit_ids
                assert set(a["resources"]) <= set(content)
                assert a["id"] == "alternative-" + sha(
                    canonical({k: v for k, v in a.items() if k != "id"})
                )
        assert {u["id"] for u in position["units"]} <= {
            uid for prop in props if prop["kind"] == "UNIT" for uid in prop["subject"]
        }
        assert {canonical(limitation) for limitation in position["limitations"]} == {
            canonical(limitation)
            for prop in props
            if prop["kind"] == "LIMITATIONS"
            for limitation in prop["claims"][name]
        }
        assert {u["id"] for u in position["units"]} == {
            u["id"]
            for prop in props
            if prop["kind"] == "UNIT"
            for u in prop["claims"][name]
        }
    assert {p["subject"] for p in props if p["kind"] == "ALTERNATIVES"} == {
        o["identity"] for o in packet["obligations"]
    }
    assert {p["subject"] for p in props if p["kind"] == "INDISPENSABILITY"} == {
        "task",
        *[o["identity"] for o in packet["obligations"]],
    }
    assert {p["kind"] for p in props} >= {"TASK_GAP", "LIMITATIONS"}
    assert all(p["decisions"] == DECISIONS for p in props)


def build() -> tuple[dict[Path, bytes], dict[str, Any]]:
    comparison = compare()
    primary, review = (
        load(ROOT.parent / "judgments.json"),
        load(ROOT / "stage_c_r_review.json"),
    )
    p, r = normalized(primary, review)
    candidates = [
        neutral_position(p, primary, independent=False),
        neutral_position(r, review, independent=True),
    ]
    # Strip all agreed cells before digest ordering. No source name participates.
    disputed = {(c["obligation"], c["address"]) for c in comparison["disputed_cells"]}
    for pos, _ in candidates:
        pos["cells"] = sorted(
            [c for c in pos["cells"] if (c["obligation"], c["address"]) in disputed],
            key=lambda c: (c["obligation"], c["address"]),
        )
    order = sorted(range(2), key=lambda i: sha(canonical(candidates[i][0])))
    positions = {f"position_{n}": candidates[i][0] for n, i in enumerate(order, 1)}
    mappings = {f"position_{n}": candidates[i][1] for n, i in enumerate(order, 1)}
    source_position = {
        ("primary" if i == 0 else "review"): f"position_{n}"
        for n, i in enumerate(order, 1)
    }
    props = []

    def proposition(kind: str, subject: Any, claims: dict[str, Any]) -> None:
        claim = {
            "kind": kind,
            "subject": subject,
            "claims": claims,
            "question": "Which necessity and source-support judgment is warranted by the frozen task and evidence?",
            "decisions": DECISIONS,
        }
        props.append({"id": "proposition-" + sha(canonical(claim)), **claim})

    for key in sorted(disputed):
        proposition(
            "CELL",
            list(key),
            {
                name: next(
                    c for c in pos["cells"] if (c["obligation"], c["address"]) == key
                )
                for name, pos in positions.items()
            },
        )
    # Pair candidates without treating diagnostic alignment as truth.
    left, right = source_position["primary"], source_position["review"]
    groups = [
        [mappings[left][a["primary"]], mappings[right][a["review"]]]
        for a in comparison["units"]["proposals"]
    ]
    groups.extend(
        [mappings[left][uid]] for uid in comparison["units"]["unmatched_primary"]
    )
    groups.extend(
        [mappings[right][uid]] for uid in comparison["units"]["unmatched_review"]
    )
    for group in groups:
        proposition(
            "UNIT",
            sorted(group),
            {
                name: [u for u in pos["units"] if u["id"] in group]
                for name, pos in positions.items()
            },
        )
    for o in p["obligations"]:
        oid = o["id"]
        proposition(
            "ALTERNATIVES",
            oid,
            {
                name: next(v for v in pos["obligations"] if v["id"] == oid)
                for name, pos in positions.items()
            },
        )
        proposition(
            "INDISPENSABILITY",
            oid,
            {
                name: next(
                    v
                    for v in pos["indispensability"]["by_obligation"]
                    if v["obligation"] == oid
                )
                for name, pos in positions.items()
            },
        )
    proposition(
        "INDISPENSABILITY",
        "task",
        {
            name: {
                k: v for k, v in pos["indispensability"].items() if k != "by_obligation"
            }
            for name, pos in positions.items()
        },
    )
    proposition(
        "TASK_GAP",
        "task",
        {
            name: {
                "task_gaps": pos["task_gaps"],
                "supplemental_units": pos["supplemental_units"],
            }
            for name, pos in positions.items()
        },
    )
    # Three semantic candidates plus three unmatched limitations, each questioned.
    for pi, ri in [(0, 0), (1, 2), (2, 4), (3, None), (None, 1), (None, 3)]:
        claims = {
            left: [] if pi is None else [positions[left]["limitations"][pi]],
            right: [] if ri is None else [positions[right]["limitations"][ri]],
        }
        proposition("LIMITATIONS", "limitation-" + sha(canonical(claims)), claims)
    proposals = []
    for a in comparison["units"]["proposals"]:
        left, right = source_position["primary"], source_position["review"]
        classification = (
            a["classification"]
            .replace("PRIMARY", left.upper())
            .replace("REVIEW", right.upper())
        )
        proposals.append(
            {
                "claims": {
                    left: mappings[left][a["primary"]],
                    right: mappings[right][a["review"]],
                },
                "classification": classification,
                "common_obligations": a["common_obligations"],
                "source_overlap": [
                    {
                        "address": s["address"],
                        "span_1": s["primary_span"]
                        if left == "position_1"
                        else s["review_span"],
                        "span_2": s["review_span"]
                        if left == "position_1"
                        else s["primary_span"],
                    }
                    for s in a["source_overlap"]
                ],
                "supports": {
                    left: [support(s) for s in a["primary_supports"]],
                    right: [support(s) for s in a["review_supports"]],
                },
                "rationale": a["semantic_rationale"],
            }
        )
    manifest = load(ROOT.parent / "manifest.json")
    packet = {
        "schema": "case-0011-neutral-disagreement-v1",
        "frame": comparison["frame"],
        "task": manifest["task"],
        "obligations": manifest["obligations"],
        "positions": positions,
        "propositions": sorted(props, key=lambda p: p["id"]),
        "agreed_cells": comparison["agreed_cells"],
        "agreed_cell_sha256": comparison["agreed_cell_sha256"],
        "ordering_rule": "Ascending SHA-256 of canonical complete neutral claim payloads; identifiers and original source mapping excluded.",
        "unit_proposals": sorted(proposals, key=lambda a: sha(canonical(a))),
    }
    addresses = {a for _, a in disputed}
    for pos in positions.values():
        addresses.update(s["address"] for u in pos["units"] for s in u["supports"])
        addresses.update(
            a
            for o in pos["obligations"]
            for alt in o["alternatives"]
            for a in alt["resources"]
        )
        addresses.update(
            limitation["rationale_support"]["address"]
            for limitation in pos["limitations"]
            if "rationale_support" in limitation
        )
    original = json.loads(
        gzip.decompress((ROOT.parent / "resources.json.gz").read_bytes())
    )
    resources = sorted(
        [v for v in original["resources"] if v["address"] in addresses],
        key=lambda r: r["address"],
    )
    assert {r["address"] for r in resources} == addresses
    validate_packet(packet, resources, comparison)
    payload = canonical({"frame": comparison["frame"], "resources": resources})
    archive = gzip.compress(payload, mtime=0)
    # Normalize gzip OS byte across Python/platform versions.
    archive = archive[:9] + b"\xff" + archive[10:]
    resource_manifest = {
        "schema": "case-0011-reconciliation-manifest-v1",
        "frame": comparison["frame"],
        "resource_count": len(resources),
        "resources": [
            {k: r[k] for k in ("address", "byte_size", "content_identity", "encoding")}
            | {"content_sha256": sha(r["content"].encode())}
            for r in resources
        ],
        "archive_sha256": sha(archive),
        "canonical_payload_sha256": sha(payload),
        "packet_sha256": sha(canonical(packet)),
    }
    files = {
        DEST / "packet.json": canonical(packet),
        DEST / "resources.json.gz": archive,
        DEST / "manifest.json": canonical(resource_manifest),
        DEST / "INSTRUCTIONS.md": INSTRUCTIONS.encode(),
        DEST / "task.txt": manifest["task"].encode(),
    }
    integrity = {
        "schema": "case-0011-reconciliation-integrity-v1",
        "files": {p.name: sha(v) for p, v in files.items()},
        "archive_sha256": sha(archive),
        "canonical_payload_sha256": sha(payload),
        "manifest_sha256": sha(canonical(resource_manifest)),
        "packet_sha256": sha(canonical(packet)),
    }
    files[DEST / "integrity.json"] = canonical(integrity)
    audit = {
        "schema": "case-0011-neutral-source-map-v1",
        "source_mapping": source_position,
        "identifier_mapping": mappings,
        "neutral_claim_digests": {n: sha(canonical(v)) for n, v in positions.items()},
        "packet_file_hashes": {p.name: sha(v) for p, v in files.items()},
        "canonical_payload_sha256": sha(payload),
        "propositions": len(props),
        "resources": len(resources),
        "text_transform": "Only source self-reference 'This review' becomes 'This position'; original sealed claims remain in outside-packet comparison. Frozen resource bytes and original task/obligations unchanged.",
        "coverage_policy": "All label disagreements, all required units including ambiguous/unmatched/partial claims, all nine alternative structures, all task/obligation indispensability, task gap and every limitation. Agreed cells are inheritance records, not adjudication questions.",
    }
    return files, audit


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files, audit = build()
    assert (files, audit) == build(), "Nondeterministic build"
    files[ROOT / "packet_audit.json"] = canonical(audit)
    if args.check:
        assert all(p.read_bytes() == raw for p, raw in files.items())
    else:
        write_new(files)


if __name__ == "__main__":
    main()
