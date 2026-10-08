"""Validate and replay bounded manual decisions. No adjudication or materialization."""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import validate_packet as v

OUTPUTS = {
    "c5_reconciliation_v2_decisions.json",
    "c5_reconciliation_v2_validation.json",
    "c5_reconciliation_v2_hashes.json",
}
ATTESTATIONS = {
    "only_packet_evidence_used",
    "no_treatment_access",
    "no_confirmation_access",
    "no_source_identity_access",
    "no_omitted_pair_adjudication",
    "no_absent_pair_default",
    "no_full_frame_derivation",
    "no_stage_d",
}
DIAGNOSTICS = {
    "FULLY_DIRECTLY_COVERED",
    "FULLY_COVERED_ONLY_COLLECTIVELY",
    "INCOMPLETE",
    "AMBIGUOUS",
}
COLLECTIVE = {
    "VALID_MINIMAL_COLLECTIVE_SET",
    "VALID_BUT_NOT_MINIMAL",
    "INSUFFICIENT",
    "AMBIGUOUS",
}


def text(value: Any) -> None:
    assert isinstance(value, str) and value.strip(), "nonempty rationale required"
    v.check_leakage(value)


def check_decisions(packet: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any]:
    """Strict closed schema; identities are limited to supplied propositions."""
    assert set(artifact) == {
        "schema",
        "packet_identity",
        "bindings",
        "decisions",
        "decision_category_counts",
        "unresolved_count",
        "method",
        "blindness_attestations",
    }, "bounded output schema; no full mapping or defaults"
    assert artifact["schema"] == "case-0011-c5-reconciliation-decisions-v2"
    assert artifact["packet_identity"] == v.sha(v.canonical(packet))
    assert artifact["bindings"] == packet["bindings"]
    assert set(artifact["method"]) == {"scope", "procedure", "provenance"}
    assert artifact["method"]["scope"] == "BOUNDED_110_PROPOSITION_DECISIONS_ONLY"
    assert artifact["method"]["provenance"] == "TREATMENT_BLIND_SEMANTIC_RECONCILIATION"
    text(artifact["method"]["procedure"])
    assert set(artifact["blindness_attestations"]) == ATTESTATIONS
    assert all(value is True for value in artifact["blindness_attestations"].values())
    propositions = {p["identity"]: p for p in packet["propositions"]}
    rows = artifact["decisions"]
    assert isinstance(rows, list)
    identities = [r["identity"] for r in rows]
    assert identities == sorted(propositions), (
        "exact 110 identities; no duplicate/missing/unexpected"
    )
    for row in rows:
        assert set(row) == {
            "identity",
            "kind",
            "subject",
            "decision",
            "payload",
            "evidence_references",
        }
        p = propositions[row["identity"]]
        kind, result, decision = row["kind"], row["payload"], row["decision"]
        assert kind == p["kind"] and row["subject"] == p["subject"]
        assert decision in p["decisions"], "allowed decision vocabulary"
        references = row["evidence_references"]
        allowed = {f"proposition:{p['identity']}/{name}" for name in p["positions"]}
        assert isinstance(references, list) and references == sorted(set(references))
        assert references and set(references) <= allowed, (
            "supplied anonymized evidence only"
        )
        if decision.startswith("ACCEPT_POSITION_"):
            name = decision.lower().removeprefix("accept_")
            assert f"proposition:{p['identity']}/{name}" in references
            selected = p["positions"][name]
        elif decision == "CONFIRM_PROPOSITION":
            selected = p["positions"]["position_1"]
        else:
            selected = None
        v.check_leakage(result)
        if kind in {"PAIR_LABEL", "DIRECT_RATIONALE"}:
            assert set(result) == {
                "label",
                "rationale",
                "covered_component",
                "missing_component",
                "complete_unit_counterfactual",
            }
            assert result["label"] in packet["semantics"]["mapping_labels"]
            text(result["rationale"])
            text(result["complete_unit_counterfactual"])
            for field in ("covered_component", "missing_component"):
                assert (
                    result[field] is None
                    or isinstance(result[field], str)
                    and result[field].strip()
                )
            if result["label"] == "PARTIALLY_COVERS":
                text(result["covered_component"])
                text(result["missing_component"])
            if selected:
                assert result["label"] == selected["label"]
            if kind == "DIRECT_RATIONALE":
                assert result["label"] == "DIRECTLY_COVERS", (
                    "shared agreed label is immutable"
                )
            elif decision == "UNRESOLVED":
                assert result["label"] == "AMBIGUOUS"
        elif kind in {"UNIT_STATUS", "NEED_CLASSIFICATION", "UNIT_GRANULARITY"}:
            field = {
                "UNIT_STATUS": "status",
                "NEED_CLASSIFICATION": "classification",
                "UNIT_GRANULARITY": "classification",
            }[kind]
            assert set(result) == {field, "rationale"}
            permitted = {
                "UNIT_STATUS": packet["semantics"]["unit_coverage"],
                "NEED_CLASSIFICATION": packet["semantics"]["need_labels"],
                "UNIT_GRANULARITY": p.get("permitted_categories", []),
            }[kind]
            assert result[field] in permitted
            text(result["rationale"])
            if selected:
                assert (
                    result[field]
                    == selected["category" if kind == "UNIT_GRANULARITY" else field]
                )
            if decision == "UNRESOLVED":
                assert (
                    result[field]
                    == {
                        "UNIT_STATUS": "AMBIGUOUS_ONLY",
                        "NEED_CLASSIFICATION": "AMBIGUOUS",
                        "UNIT_GRANULARITY": "AMBIGUOUS_GRANULARITY",
                    }[kind]
                )
        elif kind == "ALTERNATIVE_COMPLETENESS":
            assert set(result) == {
                "strict_direct_complete",
                "granularity_aware_state",
                "rationale",
                "members",
            }
            assert type(result["strict_direct_complete"]) is bool or (
                decision == "UNRESOLVED" and result["strict_direct_complete"] is None
            )
            supplied = any("diagnostic_state" in pos for pos in p["positions"].values())
            assert (
                result["granularity_aware_state"] in DIAGNOSTICS
                if supplied
                else result["granularity_aware_state"] is None
            )
            if selected:
                assert (
                    result["strict_direct_complete"]
                    == selected["strict_direct_complete"]
                )
                if "diagnostic_state" in selected:
                    assert (
                        result["granularity_aware_state"]
                        == selected["diagnostic_state"]
                    )
            text(result["rationale"])
            alternative = next(
                a
                for group in packet["semantics"]["alternatives"]
                for a in group["alternatives"]
                if a["identity"] == p["subject"]["alternative"]
            )
            members = result["members"]
            assert [m["unit"] for m in members] == sorted(alternative["units"])
            for member in members:
                assert set(member) == {"unit", "rationale"}
                text(member["rationale"])
        elif kind == "COLLECTIVE_COVERAGE":
            assert set(result) == {"rationale", "sets"}
            text(result["rationale"])
            proposed = p["positions"]["position_1"]["sets"]
            assert len(result["sets"]) == len(proposed)
            for final, original in zip(result["sets"], proposed, strict=True):
                assert set(final) == {
                    "needs",
                    "classification",
                    "rationale",
                    "contributions",
                    "minimality_analysis",
                }
                assert final["needs"] == original["needs"], (
                    "retain each supplied proposed set"
                )
                assert final["classification"] in COLLECTIVE
                if decision == "CONFIRM_PROPOSITION":
                    assert final["classification"] == "VALID_MINIMAL_COLLECTIVE_SET"
                if decision == "UNRESOLVED":
                    assert final["classification"] == "AMBIGUOUS"
                text(final["rationale"])
                text(final["minimality_analysis"])
                assert [m["need"] for m in final["contributions"]] == sorted(
                    original["needs"]
                )
                for member in final["contributions"]:
                    assert set(member) == {
                        "need",
                        "distinct_contribution",
                        "removal_analysis",
                    }
                    text(member["distinct_contribution"])
                    text(member["removal_analysis"])
        else:
            raise AssertionError("unexpected kind")
    counts = dict(sorted(Counter(r["decision"] for r in rows).items()))
    assert artifact["decision_category_counts"] == counts
    unresolved = sum(r["decision"] == "UNRESOLVED" for r in rows)
    assert artifact["unresolved_count"] == unresolved
    return {
        "schema": "case-0011-c5-reconciliation-validation-v2",
        "status": "PASS",
        "propositions": 110,
        "proposition_counts": v.COUNTS,
        "duplicate_propositions": 0,
        "missing_propositions": 0,
        "unexpected_propositions": 0,
        "decision_category_counts": counts,
        "unresolved_count": unresolved,
        "scope": "BOUNDED_110_PROPOSITION_DECISIONS_ONLY",
        "absent_pair_default": None,
    }


def replay(packet: dict[str, Any], artifact: dict[str, Any]) -> dict[str, bytes]:
    validation = check_decisions(packet, artifact)
    files = {
        "c5_reconciliation_v2_decisions.json": v.canonical(artifact),
        "c5_reconciliation_v2_validation.json": v.canonical(validation),
    }
    files["c5_reconciliation_v2_hashes.json"] = v.canonical(
        {
            "schema": "case-0011-c5-reconciliation-hashes-v2",
            "packet_identity": artifact["packet_identity"],
            "files": {name: v.sha(raw) for name, raw in sorted(files.items())},
        }
    )
    return files


def publish(root: Path, artifact: dict[str, Any]) -> None:
    assert not any((root / name).exists() for name in OUTPUTS), "OVERWRITE_REFUSED"
    v.validate(root)
    packet = v.load(gzip.decompress((root / "packet.json.gz").read_bytes()))
    files = replay(packet, artifact)
    assert files == replay(packet, artifact), "deterministic replay"
    for name, raw in files.items():
        with (root / name).open("xb") as stream:
            stream.write(raw)
    validate_completed(root)


def validate_completed(root: Path) -> dict[str, Any]:
    v.validate(root, completed=True)
    packet = v.load(gzip.decompress((root / "packet.json.gz").read_bytes()))
    artifact = v.load((root / "c5_reconciliation_v2_decisions.json").read_bytes())
    for name, raw in replay(packet, artifact).items():
        assert (root / name).read_bytes() == raw, "replay mismatch"
    return check_decisions(packet, artifact)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    if len(sys.argv) == 2 and sys.argv[1] == "--validate-completed":
        print(json.dumps(validate_completed(root), sort_keys=True, indent=2))
    else:
        raise SystemExit(
            "Import publish(root, artifact) after manual decisions; "
            "no automatic adjudication."
        )
