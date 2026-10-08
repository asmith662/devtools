"""Reconstruct case-local reviewed gold from explicitly named frozen inputs only."""

# Standalone evidence JSON boundary, matching the existing comparison scripts.
# ruff: noqa: INP001, CPY001, E501, COM812, ANN401, D103, S101, PLR2004, PERF401
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent
ADJ = ROOT.parent
EXPECTED = "f3d7c291b9ca17e1e4a7b73400871cc8be3b8bd27b28303dcd822f6ed3094a44"
SEAL = "e5b66451b82cbd76247c79f54fd0eede7518a0707a9e7616b4831a57e633f4cf"
PACKET_HASHES = {
    "resources.json.gz": "9dc80a838e4f172e69607f21510a07a26ea83bb8e2b7710270aa33e722a0995a",
    "packet.json": "91b678abb54f845418fc9071bed36c1c297c9486dd2f090ec91d5ce97dc772a7",
    "manifest.json": "5cedf52680a85468aaecd60a2ee370e486ef29746706dda0983c5ab5cca8da3f",
    "integrity.json": "e5ed5e905889c52ffc3396116af57d61333a4836fc1717efee5b544b2a04b002",
}
PAYLOAD = "d669af3f74bd184c3c7792bc2ffa1e10fc1d70bbf6b1e3ec6f48c9341d2588f1"
HANDOFF = (
    "`.local/codex-result.md` is an operational, ignored, non-authoritative result "
    "handoff used to relay Codex output. It is not repository feature semantics, "
    "not part of implementation correctness, not a repository resource, and not "
    "eligible as a task obligation, information need, witness, required resource, "
    "task gap, or repository-information gap."
)


def canonical(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(path.read_bytes()))


def write_new(files: dict[Path, bytes]) -> None:
    if any(p.exists() for p in files):
        msg = "Refusing to overwrite frozen artifacts"
        raise FileExistsError(msg)
    for p, raw in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("xb") as stream:
            stream.write(raw)


def verify_inputs() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]
]:
    rec = ADJ / "reconciliation"
    assert sha((rec / "reconciliation.json").read_bytes()) == EXPECTED
    r = load(rec / "reconciliation.json")
    for name, digest in PACKET_HASHES.items():
        assert sha((rec / name).read_bytes()) == digest
    assert sha(gzip.decompress((rec / "resources.json.gz").read_bytes())) == PAYLOAD
    for name, digest in r["input_bindings"]["files"].items():
        assert sha((rec / name).read_bytes()) == digest
    assert r["input_bindings"]["archive_sha256"] == PACKET_HASHES["resources.json.gz"]
    assert r["input_bindings"]["canonical_payload_sha256"] == PAYLOAD
    assert r["input_bindings"]["integrity_sha256"] == PACKET_HASHES["integrity.json"]
    packet, manifest = load(rec / "packet.json"), load(ADJ / "manifest.json")
    assert (
        sha(canonical(packet["agreed_cells"])) == packet["agreed_cell_sha256"] == SEAL
    )
    assert r["agreed_cell_inheritance"]["seal"] == SEAL
    assert sha((ADJ / "resources.json.gz").read_bytes()) == manifest["archive_sha256"]
    payload = gzip.decompress((ADJ / "resources.json.gz").read_bytes())
    assert sha(payload) == manifest["canonical_payload_sha256"]
    resources = json.loads(payload)["resources"]
    assert len(resources) == len({x["address"] for x in resources}) == 531
    for resource in resources:
        raw = resource["content"].encode()
        # Native decoded-text identities are length-framed semantic digests,
        # distinct from archive/raw UTF-8 content hashes.
        content_digest = hashlib.sha256()
        for part in (b"decoded-utf8-text-sha256-v1", raw):
            content_digest.update(len(part).to_bytes(8, "big"))
            content_digest.update(part)
        assert content_digest.hexdigest() == resource["content_identity"]
        assert len(raw) == resource["byte_size"]
    neutral = json.loads(gzip.decompress((rec / "resources.json.gz").read_bytes()))[
        "resources"
    ]
    full = {x["address"]: x for x in resources}
    assert all(x == full[x["address"]] for x in neutral)
    for x in load(rec / "manifest.json")["resources"]:
        assert sha(full[x["address"]]["content"].encode()) == x["content_sha256"]
    assert r["frame"] == packet["frame"]
    assert all(manifest[k] == v for k, v in r["frame"].items())
    assert (
        packet["task"] == manifest["task"] == (ADJ / "task.txt").read_bytes().decode()
    )
    assert packet["obligations"] == manifest["obligations"]
    return r, packet, manifest, resources


def verify_support(value: Any, contents: dict[str, dict[str, Any]]) -> int:
    count = 0
    if isinstance(value, dict):
        if {"address", "excerpt", "excerpt_sha256"} <= value.keys():
            resource = contents[value["address"]]
            text = resource["content"]
            assert sha(value["excerpt"].encode()) == value["excerpt_sha256"]
            if "start_character" in value:
                start, end = value["start_character"], value["end_character"]
                assert 0 <= start < end <= len(text)
                assert text[start:end] == value["excerpt"]
            else:
                assert value["excerpt"] in text
            if "content_identity" in value:
                assert value["content_identity"] == resource["content_identity"]
            count += 1
        count += sum(verify_support(v, contents) for v in value.values())
    elif isinstance(value, list):
        count += sum(verify_support(v, contents) for v in value)
    return count


def structure(obligations: list[dict[str, Any]]) -> dict[str, Any]:
    combinations = []
    for combo in itertools.product(*(o["alternatives"] for o in obligations)):
        combinations.append(
            {
                "alternatives": [a["id"] for a in combo],
                "resources": sorted({x for a in combo for x in a["resources"]}),
                "units": sorted({x for a in combo for x in a["units"]}),
            }
        )
    unions = sorted({tuple(c["resources"]) for c in combinations})
    unit_unions = sorted({tuple(c["units"]) for c in combinations})
    minimum, maximum = min(map(len, unions)), max(map(len, unions))
    return {
        "alternative_counts": {
            o["obligation"]: len(o["alternatives"]) for o in obligations
        },
        "complete_task_combinations": combinations,
        "combination_count": len(combinations),
        "sufficient_resource_unions": [list(u) for u in unions],
        "sufficient_unit_unions": [list(u) for u in unit_unions],
        "minimum_sufficient_resource_union_size": minimum,
        "maximum_sufficient_resource_union_size": maximum,
        "minimum_sufficient_unions": [list(u) for u in unions if len(u) == minimum],
        "maximum_sufficient_unions": [list(u) for u in unions if len(u) == maximum],
        "task_indispensable_resources": sorted(
            set.intersection(*(set(u) for u in unions))
        ),
        "task_indispensable_units": sorted(
            set.intersection(*(set(u) for u in unit_unions))
        ),
        "obligation_indispensability": [
            {
                "obligation": o["obligation"],
                "resources": sorted(
                    set.intersection(*(set(a["resources"]) for a in o["alternatives"]))
                ),
                "units": sorted(
                    set.intersection(*(set(a["units"]) for a in o["alternatives"]))
                ),
            }
            for o in obligations
        ],
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:  # noqa: C901, PLR0912, PLR0915 -- finite sealed reconstruction
    r, packet, manifest, resources = verify_inputs()
    primary = load(ADJ / "judgments.json")
    independent = load(ADJ / "reliability/stage_c_r_review.json")
    assert (
        sha((ADJ / "judgments.json").read_bytes())
        == "71da4b04a8507cc341303129dc70d4cdf4ab0ff4e0a7b700422b287e2793d4a6"
    )
    assert (
        sha((ADJ / "reliability/stage_c_r_review.json").read_bytes())
        == "0323ae030d05a1508336181fe3fd671c7a87762680a5e434fec404ce74143576"
    )
    assert primary["frozen_obligations"] == manifest["obligations"]
    assert independent["frozen_manifest"] == manifest
    assert primary["frame"] == independent["frame"] == r["frame"]
    pc = {
        (c["obligation_id"], c["resource_address"]): (c["content_identity"], c["label"])
        for c in primary["cells"]
    }
    ic = {
        (c["obligation"], c["resource"]["address"]): (
            c["resource"]["content_identity"],
            c["label"],
        )
        for c in independent["cells"]
    }
    expected = {
        (o["identity"], x["address"])
        for o in manifest["obligations"]
        for x in resources
    }
    assert (
        len(primary["cells"])
        == len(independent["cells"])
        == len(pc)
        == len(ic)
        == len(expected)
        == 4779
    )
    assert set(pc) == set(ic) == expected
    agreed = [
        {
            "obligation": o,
            "address": a,
            "content_identity": pc[o, a][0],
            "label": pc[o, a][1],
        }
        for o, a in sorted(expected)
        if pc[o, a] == ic[o, a]
    ]
    assert agreed == packet["agreed_cells"]
    decisions = {d["proposition_id"]: d for d in r["decisions"]}
    assert len(decisions) == len(r["decisions"]) == len(packet["propositions"]) == 140
    assert set(decisions) == {p["id"] for p in packet["propositions"]}
    for index, prop in enumerate(packet["propositions"]):
        d = decisions[prop["id"]]
        assert d["packet_index"] == index
        assert (d["kind"], d["subject"]) == (prop["kind"], prop["subject"])
        assert d["decision"] in prop["decisions"]
        assert d["decision"] != "UNRESOLVED"
        assert d["reason"]
        assert d["exact_evidence"]
    contents = {x["address"]: x for x in resources}
    contents["task.txt"] = {
        "content": manifest["task"],
        "content_identity": sha(manifest["task"].encode()),
    }
    support_count = verify_support(r, contents)
    verify_support(packet["positions"], contents)
    units = []
    unit_ids = {u["id"] for u in r["units"]}
    assert len(unit_ids) == len(r["units"])
    source_claims = {
        u["id"] for pos in packet["positions"].values() for u in pos["units"]
    }
    assert source_claims == {x["claim_id"] for x in r["source_unit_dispositions"]}
    fragments = {
        u for x in r["source_unit_dispositions"] for u in x["reconciled_fragments"]
    }
    assert fragments == unit_ids
    for u in r["units"]:
        assert u["id"] == "reconciled-unit-" + sha(
            canonical(
                {
                    k: v
                    for k, v in u.items()
                    if k not in {"id", "alternative_membership"}
                }
            )
        )
        ds = [
            d
            for d in r["decisions"]
            if d["kind"] == "UNIT" and u["id"] in d["reconciled_value"]["units"]
        ]
        assert ds
        assert u["necessity"] == "REQUIRED"
        assert u["supports"]
        units.append(
            {
                **u,
                "provenance": [
                    {
                        "kind": "reconciled replacement"
                        if d["decision"] == "REPLACE_WITH_RECONCILED_JUDGMENT"
                        else "accepted position",
                        "decision": d["decision"],
                        "proposition_id": d["proposition_id"],
                    }
                    for d in ds
                ],
            }
        )
    obligations = [
        d["reconciled_value"] for d in r["decisions"] if d["kind"] == "ALTERNATIVES"
    ]
    obligations.sort(key=lambda o: o["obligation"])
    assert {o["obligation"] for o in obligations} == {
        o["identity"] for o in manifest["obligations"]
    }
    by_unit = {u["id"]: u for u in units}
    for o in obligations:
        assert o["alternative_logic"] == "ANY_COMPLETE_ALTERNATIVE"
        for a in o["alternatives"]:
            assert a["id"] == "reconciled-alternative-" + sha(
                canonical({k: v for k, v in a.items() if k != "id"})
            )
            assert a["member_logic"] == "ALL_COMPLEMENTARY"
            assert a["obligation"] == o["obligation"]
            assert set(a["units"]) <= unit_ids
            assert set(a["evidence_bindings"]) == set(a["units"])
            assert set(a["resources"]) == {
                s["address"] for spans in a["evidence_bindings"].values() for s in spans
            }
            for uid, spans in a["evidence_bindings"].items():
                assert spans
                assert all(s in by_unit[uid]["supports"] for s in spans)
                assert o["obligation"] in by_unit[uid]["obligations"]
    for u in units:
        assert {canonical(s) for s in u["supports"]} == {
            canonical(s)
            for o in obligations
            for a in o["alternatives"]
            for s in a["evidence_bindings"].get(u["id"], [])
        }
        assert set(u["alternative_membership"]) == {
            a["id"]
            for o in obligations
            for a in o["alternatives"]
            if u["id"] in a["units"]
        }
        assert set(u["obligations"]) == {
            o["obligation"]
            for o in obligations
            for a in o["alternatives"]
            if u["id"] in a["units"]
        }
    cells = {
        (c["obligation"], c["address"]): {
            **c,
            "provenance": "INHERITED_AGREEMENT",
            "seal": SEAL,
        }
        for c in agreed
    }
    for d in r["decisions"]:
        if d["kind"] == "CELL":
            c = d["reconciled_value"]
            key = (c["obligation"], c["address"])
            assert key not in cells
            assert key == tuple(d["subject"])
            cells[key] = {
                **c,
                "provenance": "RECONCILED_DISPUTE",
                "proposition_id": d["proposition_id"],
                "reason": d["reason"],
            }
    for e in r["agreed_cell_inheritance"]["exceptions"]:
        key = (e["obligation"], e["address"])
        assert cells[key]["provenance"] == "INHERITED_AGREEMENT"
        assert cells[key]["label"] == e["inherited_label"]
        cells[key] = {
            **cells[key],
            "label": e["reconciled_label"],
            "provenance": "RECONCILED_EXCEPTION",
            "exception": e,
        }
    assert set(cells) == expected
    for (o, a), c in cells.items():
        assert c["content_identity"] == contents[a]["content_identity"]
        binding = sorted(
            {
                uid
                for ob in obligations
                if ob["obligation"] == o
                for alt in ob["alternatives"]
                for uid, spans in alt["evidence_bindings"].items()
                if any(s["address"] == a for s in spans)
            }
        )
        assert bool(binding) == (c["label"] == "REQUIRED")
        if c["provenance"] == "RECONCILED_DISPUTE":
            assert c["units"] == binding
        c["reviewed_units"] = binding
    st = structure(obligations)
    for d in r["decisions"]:
        if d["kind"] == "INDISPENSABILITY":
            value = d["reconciled_value"]
            if d["subject"] == "task":
                assert value["task_resources"] == st["task_indispensable_resources"]
                assert value["task_units"] == st["task_indispensable_units"]
            else:
                ob = next(
                    o
                    for o in st["obligation_indispensability"]
                    if o["obligation"] == d["subject"]
                )
                assert value["indispensable_resources"] == ob["resources"]
                assert value["indispensable_units"] == ob["units"]
    summary = r["summary"]
    assert st["combination_count"] == summary["complete_task_alternative_combinations"]
    assert st["alternative_counts"] == summary["alternative_counts"]
    assert sorted(st["sufficient_resource_unions"]) == sorted(
        summary["sufficient_resource_unions"]
    )
    assert sorted(st["sufficient_unit_unions"]) == sorted(
        summary["sufficient_unit_unions"]
    )
    required_union = sorted(
        {c["address"] for c in cells.values() if c["label"] == "REQUIRED"}
    )
    assert required_union == summary["required_resource_union"]
    assert len(units) == summary["required_unit_count"]
    limitations = [
        d["reconciled_value"] for d in r["decisions"] if d["kind"] == "LIMITATIONS"
    ]
    assert sorted(canonical(x) for x in limitations) == sorted(
        canonical(x) for x in summary["accepted_interpretation_limitations"]
    )
    gap = next(d["reconciled_value"] for d in r["decisions"] if d["kind"] == "TASK_GAP")
    assert gap["task_gaps"] == "NONE"
    assert not gap["supplemental_task_semantic_units"]
    labels = dict(sorted(Counter(c["label"] for c in cells.values()).items()))
    provenance = dict(sorted(Counter(c["provenance"] for c in cells.values()).items()))
    changes = {}
    for name, source in (("primary", pc), ("independent", ic)):
        changes[name] = [
            {
                "obligation": o,
                "address": a,
                "before": source[o, a][1],
                "after": cells[o, a]["label"],
            }
            for o, a in sorted(expected)
            if source[o, a][1] != cells[o, a]["label"]
        ]
    bindings = {
        str(p.relative_to(ADJ)): sha(p.read_bytes())
        for p in (
            ADJ / "judgments.json",
            ADJ / "manifest.json",
            ADJ / "resources.json.gz",
            ADJ / "reliability/stage_c_r_review.json",
            ADJ / "reconciliation/reconciliation.json",
            ADJ / "reconciliation/packet.json",
        )
    }
    gold = {
        "schema": "case-0011-reviewed-gold-v1",
        "frame": r["frame"],
        "input_bindings": bindings,
        "task": manifest["task"],
        "frozen_obligations": manifest["obligations"],
        "resources": [
            {k: x[k] for k in ("address", "content_identity", "byte_size", "encoding")}
            for x in resources
        ],
        "cells": [cells[k] for k in sorted(cells)],
        "units": units,
        "obligations": obligations,
        "task_gap": gap,
        "interpretation_limitations": [
            {
                **x,
                "constrains_implementation": True,
                "blocks_no_judgment": True,
                "requires_no_inherent_discovery": True,
            }
            for x in limitations
        ],
        "required_semantics": "REQUIRED means necessary within at least one acceptable witness alternative for that obligation; it does not mean present in every alternative or every valid task solution. The entire required union is not simultaneously necessary.",
        "handoff_safeguard": HANDOFF,
    }
    stats = {
        "schema": "case-0011-reviewed-statistics-v1",
        "resources": len(resources),
        "obligations": len(obligations),
        "cells": len(cells),
        "label_counts": labels,
        "cell_provenance_counts": provenance,
        "duplicate_identities": 0,
        "missing_identities": 0,
        "unexpected_identities": 0,
        "unresolved_propositions": 0,
        "decision_counts": {
            **dict(Counter(d["decision"] for d in r["decisions"])),
            "UNRESOLVED": 0,
        },
        "required_unit_count": len(units),
        "required_resource_union": required_union,
        "source_support_assertions": support_count,
        "changes": changes,
        **st,
    }
    return gold, stats


def artifacts() -> dict[Path, bytes]:
    gold, stats = build()
    raw = canonical(gold)
    return {
        ROOT / "reviewed_gold.json": raw,
        ROOT / "reviewed_statistics.json": canonical(stats),
        ROOT / "reviewed_gold.sha256": (sha(raw) + "  reviewed_gold.json\n").encode(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = artifacts()
    if args.check:
        assert all(p.read_bytes() == raw for p, raw in files.items())
    else:
        write_new(files)


if __name__ == "__main__":
    main()
