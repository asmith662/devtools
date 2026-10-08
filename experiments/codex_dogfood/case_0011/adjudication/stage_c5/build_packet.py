"""Prepare a treatment-free semantic coverage packet; never adjudicate coverage."""

# Case-local JSON evidence boundary; no production API or acquisition execution.
# ruff: noqa: INP001, CPY001, E501, COM812, ANN401, D103, S101, PLR2004
from __future__ import annotations

import argparse
import gzip
import itertools
import json
import re
import stat
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0011.adjudication.reviewed.build_reviewed_gold import (
    ADJ,
    canonical,
    load,
    sha,
    write_new,
)
from experiments.codex_dogfood.case_0011.adjudication.reviewed.build_reviewed_gold import (
    artifacts as gold_artifacts,
)

ROOT = Path(__file__).resolve().parent
CASE = ADJ.parent
AUTHOR_SHA = "5f60a2d04a0b94c34c5b0014282f9393ce8bc4ff947d3d5754e84ff320a1e7ff"
MAPPING_LABELS = {
    "DIRECTLY_COVERS": "The information need explicitly seeks evidence capable of establishing the required unit.",
    "PARTIALLY_COVERS": "The need seeks only part of the required unit and would not reasonably establish it completely.",
    "DOES_NOT_COVER": "The need asks a materially different repository question.",
    "AMBIGUOUS": "The semantic relationship cannot be defended confidently from the packet.",
}
UNIT_COVERAGE = {
    "COVERED": "At least one DIRECTLY_COVERS mapping.",
    "PARTIAL_ONLY": "No direct mapping and at least one PARTIALLY_COVERS.",
    "UNCOVERED": "No direct, partial or ambiguous mapping.",
    "AMBIGUOUS_ONLY": "No direct or partial mapping and at least one AMBIGUOUS.",
}
NEED_LABELS = {
    "NECESSARY": "Directly covers at least one required unit that no other need directly covers.",
    "USEFUL_REDUNDANT": "Directly covers required units, but all are directly covered by another need.",
    "PARTIAL_ONLY": "Has partial mappings but no direct mapping.",
    "UNNECESSARY": "Has no direct or partial mapping to required units.",
    "MISFORMULATED": "Intended task concern is recognizable, but the need's statement cannot reasonably guide acquisition of the required fact.",
    "AMBIGUOUS": "Cannot classify defensibly.",
}
INSTRUCTIONS = """# Stage C.5 semantic information-need coverage

Verify integrity.json, archive bytes and decompressed payload before reading.
Use only these four supplied regular files. Do not seek a repository checkout,
Git, source files, lexical queries, acquisition outputs, resource answer paths,
ranks, scores, costs, treatment arms, models, confirmation or Stage D outcomes.

Determine whether the frozen manual InformationNeeds semantically cover the
required information units. This is semantic review, not implementation or
acquisition evaluation. Every need must be compared to every unit. Do not prune
by shared words or owning obligation: cross-obligation coverage is allowed.
ALL units inside an alternative are complementary; ANY complete alternative
suffices for its obligation. A REQUIRED unit is necessary in at least one
acceptable witness alternative, not necessarily in every valid task solution.
Do not mix incompatible alternatives or flatten them to a simultaneous union.

For each mapping choose exactly one frozen mapping label and give a rationale.
DIRECTLY_COVERS must state (1) the fact the need seeks, (2) the fact the unit
establishes, and (3) why answering the need would establish the unit. Shared
wording alone is insufficient. Preserve partial and ambiguous outcomes.
Derive unit coverage only from semantic decisions using the frozen definitions;
AMBIGUOUS_ONLY takes precedence over UNCOVERED when ambiguous mappings remain.
U1 requires DIRECT coverage. Classify every need semantically, with rationale,
using the supplied need labels; do not infer usefulness from word overlap.
MISFORMULATED and AMBIGUOUS require explicit reviewer judgment rather than a
mechanical shortcut based only on mapping counts.

The statements describe required facts with answer-location names omitted.
Opaque unit and alternative identities carry no quality or chronological rank.
Freeze the complete mapping decisions, rationales, need classifications,
coverage derivation, identity checks and output digests before any later join.
Do not change the task, obligations, needs, units or alternatives. Do not perform
Stage D or conclude U1 effectiveness. Stop if packet integrity or blindness fails.
"""

# Exact allowlists, including nested objects. No wildcard metadata propagation.
KEYS = {
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
    "information_needs",
    "obligation",
    "reason",
    "anchors",
    "units",
    "alternative_membership",
    "alternatives",
    "member_logic",
    "alternative_logic",
    "mapping_frame",
    "need",
    "unit",
    "mapping_labels",
    "unit_coverage",
    "need_labels",
    "direct_coverage_rule",
    *MAPPING_LABELS,
    *UNIT_COVERAGE,
    *NEED_LABELS,
}
FORBIDDEN = re.compile(
    r"(?:\b(?:primary|stage_c_r|reconciled|reconciliation|chronology|gpt|astra|position_[12])\b|(?:src|docs|scripts)/[^\s]+|tests/(?:context|models|experiments)[^\s]*|\b[\w-]+\.(?:py|md|toml|json)\b)",
    re.IGNORECASE,
)
LOCATION_SUBSTITUTIONS = {
    "src/tests/experiments": "source, test and experiment trees",
    "uv run python scripts/validate_development.py": "the documented protected development entry point",
    "tests/experiments": "the experiment test tree",
    "architecture.md": "The governing architecture document",
}


def neutral_statement(statement: str) -> str:
    for name, replacement in LOCATION_SUBSTITUTIONS.items():
        statement = statement.replace(name, replacement)
    return statement


def check_metadata(value: Any) -> None:
    if isinstance(value, dict):
        assert set(value) <= KEYS, set(value) - KEYS
        for v in value.values():
            check_metadata(v)
    elif isinstance(value, list):
        for v in value:
            check_metadata(v)
    elif isinstance(value, str):
        assert not FORBIDDEN.search(value), value


def frozen_needs(task: str) -> list[dict[str, Any]]:
    # Parse the allowed authoring container solely to project semantic records.
    # Query keys/values are never selected, printed, compared or returned.
    assert sha((CASE / "authoring.json").read_bytes()) == AUTHOR_SHA
    authored = load(CASE / "authoring.json")
    lines = task.splitlines(keepends=True)
    output = []
    for ob in authored["obligations"]:
        for row in ob["needs"]:
            spans = []
            for number in row["task_lines"]:
                assert 1 <= number <= len(lines)
                start = sum(map(len, lines[: number - 1]))
                spans.append(
                    {
                        "line": number,
                        "start": start,
                        "end": start + len(lines[number - 1]),
                        "text": lines[number - 1],
                        "origin": "VERBATIM_TASK",
                    }
                )
            output.append(
                {
                    "identity": f"{authored['task_identity']}/{ob['id']}/{row['id']}",
                    "obligation": ob["id"],
                    "statement": row["statement"],
                    "reason": row["reason"],
                    "task_basis": spans,
                    "anchors": row["hints"],
                    "author": authored["author"],
                    "provenance": "manual from task/obligation/criterion only; before source inspection",
                }
            )
    assert len(output) == len({n["identity"] for n in output}) == 18
    return output


def packet() -> tuple[dict[str, Any], dict[str, Any]]:
    frozen_gold = gold_artifacts()
    assert all(p.read_bytes() == raw for p, raw in frozen_gold.items())
    gold = load(ADJ / "reviewed/reviewed_gold.json")
    needs = frozen_needs(gold["task"])
    unit_map = {
        u["id"]: "unit-"
        + sha(
            canonical(
                {
                    "statement": neutral_statement(u["statement"]),
                    "obligations": u["obligations"],
                }
            )
        )
        for u in gold["units"]
    }
    # Distinct resource witnesses can establish the same semantic units.
    # Retain distinct opaque identities without exposing those resources.
    alt_map = {
        a["id"]: "alternative-" + sha(a["id"].encode())
        for o in gold["obligations"]
        for a in o["alternatives"]
    }
    units = [
        {
            "identity": unit_map[u["id"]],
            "statement": neutral_statement(u["statement"]),
            "obligations": u["obligations"],
            "alternative_membership": sorted(
                alt_map[a] for a in u["alternative_membership"]
            ),
        }
        for u in gold["units"]
    ]
    units.sort(key=lambda u: u["identity"])
    assert len(units) == len({u["identity"] for u in units})
    alternatives = [
        {
            "obligation": o["obligation"],
            "alternative_logic": "ANY_COMPLETE_ALTERNATIVE",
            "alternatives": [
                {
                    "identity": alt_map[a["id"]],
                    "member_logic": "ALL_COMPLEMENTARY",
                    "units": sorted(unit_map[u] for u in a["units"]),
                }
                for a in o["alternatives"]
            ],
        }
        for o in gold["obligations"]
    ]
    output = {
        "schema": "case-0011-semantic-coverage-packet-v1",
        "frame": gold["frame"],
        "task": gold["task"],
        "obligations": gold["frozen_obligations"],
        "information_needs": needs,
        "units": units,
        "alternatives": alternatives,
        "mapping_frame": [
            {"need": n["identity"], "unit": u["identity"]}
            for n, u in itertools.product(needs, units)
        ],
        "mapping_labels": MAPPING_LABELS,
        "unit_coverage": UNIT_COVERAGE,
        "need_labels": NEED_LABELS,
        "direct_coverage_rule": "U1 requires at least one DIRECTLY_COVERS mapping for every required unit.",
    }
    check_packet(output)
    audit = {
        "reviewed_gold_sha256": sha((ADJ / "reviewed/reviewed_gold.json").read_bytes()),
        "frozen_needs_sha256": sha(canonical(needs)),
        "authoring_source_sha256": AUTHOR_SHA,
        "unit_projection": unit_map,
        "alternative_projection": alt_map,
        "location_substitutions": LOCATION_SUBSTITUTIONS,
    }
    return output, audit


def check_packet(value: dict[str, Any]) -> None:
    assert set(value) == {
        "schema",
        "frame",
        "task",
        "obligations",
        "information_needs",
        "units",
        "alternatives",
        "mapping_frame",
        "mapping_labels",
        "unit_coverage",
        "need_labels",
        "direct_coverage_rule",
    }
    check_metadata(value)
    assert set(value["frame"]) == {
        "case_identity",
        "task_identity",
        "repository_id",
        "snapshot_id",
        "corpus_id",
    }
    assert value["mapping_labels"] == MAPPING_LABELS
    assert value["unit_coverage"] == UNIT_COVERAGE
    assert value["need_labels"] == NEED_LABELS
    needs, units = value["information_needs"], value["units"]
    for n in needs:
        assert set(n) == {
            "identity",
            "obligation",
            "statement",
            "reason",
            "task_basis",
            "anchors",
            "author",
            "provenance",
        }
    for u in units:
        assert set(u) == {
            "identity",
            "statement",
            "obligations",
            "alternative_membership",
        }
    nids, uids = {n["identity"] for n in needs}, {u["identity"] for u in units}
    assert len(nids) == len(needs)
    assert len(uids) == len(units)
    for pair in value["mapping_frame"]:
        assert set(pair) == {"need", "unit"}
    assert len(value["mapping_frame"]) == len(nids) * len(uids)
    assert {(p["need"], p["unit"]) for p in value["mapping_frame"]} == set(
        itertools.product(nids, uids)
    )
    obs = {o["identity"] for o in value["obligations"]}
    assert {n["obligation"] for n in needs} <= obs
    aids = set()
    for o in value["alternatives"]:
        assert set(o) == {"obligation", "alternative_logic", "alternatives"}
        assert o["obligation"] in obs
        assert o["alternative_logic"] == "ANY_COMPLETE_ALTERNATIVE"
        for a in o["alternatives"]:
            assert set(a) == {"identity", "member_logic", "units"}
            assert a["identity"] not in aids
            assert a["member_logic"] == "ALL_COMPLEMENTARY"
            aids.add(a["identity"])
            assert set(a["units"]) <= uids
    for u in units:
        membership = {
            a["identity"]
            for o in value["alternatives"]
            for a in o["alternatives"]
            if u["identity"] in a["units"]
        }
        assert membership == set(u["alternative_membership"])


def artifacts() -> tuple[dict[Path, bytes], dict[str, Any]]:
    value, audit = packet()
    payload = canonical(value)
    archive = gzip.compress(payload, mtime=0)
    manifest = {
        "schema": "case-0011-semantic-coverage-manifest-v1",
        "frame": value["frame"],
        "reviewed_gold_sha256": audit["reviewed_gold_sha256"],
        "frozen_needs_sha256": audit["frozen_needs_sha256"],
        "need_count": len(value["information_needs"]),
        "required_unit_count": len(value["units"]),
        "mapping_count": len(value["mapping_frame"]),
        "archive_sha256": sha(archive),
        "canonical_payload_sha256": sha(payload),
    }
    files = {
        ROOT / "packet.json.gz": archive,
        ROOT / "manifest.json": canonical(manifest),
        ROOT / "C5_INSTRUCTIONS.md": INSTRUCTIONS.encode(),
    }
    integrity = {
        "schema": "case-0011-semantic-coverage-integrity-v1",
        "archive_sha256": sha(archive),
        "canonical_payload_sha256": sha(payload),
        "manifest_sha256": sha(files[ROOT / "manifest.json"]),
        "files": {p.name: sha(raw) for p, raw in files.items()},
    }
    files[ROOT / "integrity.json"] = canonical(integrity)
    audit["integrity_sha256"] = sha(files[ROOT / "integrity.json"])
    audit["archive_sha256"] = sha(archive)
    audit["canonical_payload_sha256"] = sha(payload)
    audit["manifest_sha256"] = sha(files[ROOT / "manifest.json"])
    return files, audit


def validate_files(files: dict[str, bytes]) -> None:
    assert set(files) == {
        "C5_INSTRUCTIONS.md",
        "manifest.json",
        "packet.json.gz",
        "integrity.json",
    }
    manifest, integrity = (
        json.loads(files["manifest.json"]),
        json.loads(files["integrity.json"]),
    )
    assert set(manifest) == {
        "schema",
        "frame",
        "reviewed_gold_sha256",
        "frozen_needs_sha256",
        "need_count",
        "required_unit_count",
        "mapping_count",
        "archive_sha256",
        "canonical_payload_sha256",
    }
    assert set(integrity) == {
        "schema",
        "archive_sha256",
        "canonical_payload_sha256",
        "manifest_sha256",
        "files",
    }
    assert set(integrity["files"]) == set(files) - {"integrity.json"}
    for name, digest in integrity["files"].items():
        assert sha(files[name]) == digest
    assert sha(files["manifest.json"]) == integrity["manifest_sha256"]
    assert (
        sha(files["packet.json.gz"])
        == integrity["archive_sha256"]
        == manifest["archive_sha256"]
    )
    raw = gzip.decompress(files["packet.json.gz"])
    assert (
        sha(raw)
        == integrity["canonical_payload_sha256"]
        == manifest["canonical_payload_sha256"]
    )
    value = json.loads(raw)
    check_packet(value)
    assert raw == canonical(value)
    assert value["frame"] == manifest["frame"]
    assert sha(canonical(value["information_needs"])) == manifest["frozen_needs_sha256"]
    assert len(value["information_needs"]) == manifest["need_count"]
    assert len(value["units"]) == manifest["required_unit_count"]
    assert len(value["mapping_frame"]) == manifest["mapping_count"]
    assert files["C5_INSTRUCTIONS.md"] == INSTRUCTIONS.encode()


def review_markdown(value: dict[str, Any]) -> bytes:
    lines = [
        "# C.5 packet pre-review transparency",
        "",
        "PREPARED ONLY. No semantic mappings have been adjudicated; this is not C.5 gold.",
        "",
        "The reviewer receives only four regular files: C5_INSTRUCTIONS.md, manifest.json, packet.json.gz and integrity.json. No queries, answer resource paths/filenames, ranks, scores or results are included. Integrity digests bind the frozen inputs without exposing answers. Location names in three unit statements are replaced by semantic descriptions; all other statements are verbatim.",
        "",
        "## Exact instructions",
        "",
        INSTRUCTIONS,
        "## Task",
        "",
        value["task"],
        "## Obligations and criteria",
        "",
    ]
    for o in value["obligations"]:
        lines.extend([f"### {o['identity']}", "", canonical(o).decode(), ""])
    lines.extend(["## Frozen InformationNeeds", ""])
    for n in value["information_needs"]:
        lines.extend([canonical(n).decode(), ""])
    lines.extend(["## Required unit statements and membership", ""])
    for u in value["units"]:
        lines.extend([canonical(u).decode(), ""])
    lines.extend(
        [
            "## Alternative structures",
            "",
            canonical(value["alternatives"]).decode(),
            "",
            "## Complete mapping frame",
            "",
            f"{len(value['information_needs'])} needs × {len(value['units'])} units = {len(value['mapping_frame'])} pairs. Includes all cross-obligation pairs; no lexical pruning.",  # noqa: RUF001 -- intentional multiplication sign
            "",
            "## Labels",
            "",
            canonical(
                {
                    "mapping_labels": MAPPING_LABELS,
                    "unit_coverage": UNIT_COVERAGE,
                    "need_labels": NEED_LABELS,
                }
            ).decode(),
            "",
            "UNCOVERED excludes ambiguous-only units; AMBIGUOUS_ONLY takes precedence. U1 requires DIRECT coverage. Need classifications require future semantic reviewer decisions.",
            "",
        ]
    )
    return "\n".join(lines).encode()


def workspace_check(destination: Path, files: dict[str, bytes]) -> None:
    assert destination.is_dir()
    assert not destination.is_symlink()
    assert not destination.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert {p.name for p in destination.iterdir()} == set(files)
    for p in destination.iterdir():
        assert p.is_file()
        assert not p.is_symlink()
        assert not p.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
        assert p.read_bytes() == files[p.name]
    validate_files(files)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sterile", type=Path)
    args = parser.parse_args()
    files, audit = artifacts()
    validate_files({p.name: raw for p, raw in files.items()})
    if args.sterile:
        dest = args.sterile.resolve()
        assert not dest.is_relative_to(CASE.parents[2])
        if dest.exists():
            msg = "Refusing to overwrite sterile workspace"
            raise FileExistsError(msg)
        dest.mkdir(parents=True)
        write_new({dest / p.name: raw for p, raw in files.items()})
        workspace_check(dest, {p.name: raw for p, raw in files.items()})
    elif args.check:
        assert all(p.read_bytes() == raw for p, raw in files.items())
    else:
        value, _ = packet()
        write_new(
            {
                **files,
                ROOT / "projection_audit.json": canonical(audit),
                ROOT / "C5_PACKET_REVIEW.md": review_markdown(value),
            }
        )


if __name__ == "__main__":
    main()
