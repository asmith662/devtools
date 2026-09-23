# Copyright (c) 2026
# ruff: noqa: D103, E501
"""Synthetic checks for Increment-23 persistence and blindness mechanics."""

from __future__ import annotations

from typing import cast

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.purpose_relative_admission.validation_adjudication import (
    AdjudicationResourceMapping,
    BlindedAdjudicationItem,
    BlindedAdjudicationPackage,
    BlindedResourceEvidence,
    ImmutableAdjudicationRecord,
    freeze_adjudication_set,
)
from experiments.purpose_relative_admission.validation_execution import (
    artifact_envelope,
    audit_blinded_packages,
    audit_frozen_adjudication_artifact,
    frozen_adjudication_artifact,
    invalid_blinded_package_record,
    load_blinded_adjudication_packages,
    load_frozen_adjudication_artifact,
    project_blinded_resource_evidence,
    redact_repository_addresses,
    repair_blinded_package_artifact,
    validate_artifact_correspondence,
    validate_artifact_envelope,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment


def _evidence(*lines: str) -> BlindedResourceEvidence:
    return BlindedResourceEvidence("structural-outline", "python", lines)


def _package(
    *,
    evidence: object,
    visible_address: str | None = None,
) -> BlindedAdjudicationPackage:
    return BlindedAdjudicationPackage(
        "case",
        "information need",
        "purpose rationale",
        (
            BlindedAdjudicationItem(
                "resource-0123456789abcdef",
                cast("BlindedResourceEvidence", evidence),
                visible_address,
            ),
        ),
        "capture-case",
        "design",
    )


def _mapping(*, visible: bool = False) -> tuple[AdjudicationResourceMapping, ...]:
    return (
        AdjudicationResourceMapping(
            "resource-0123456789abcdef",
            RepositoryResourceAddress("src/example.py"),
            visible,
        ),
    )


def test_repository_address_redaction_is_deterministic_and_handles_path_separators() -> None:
    addresses = (RepositoryResourceAddress("src/example.py"),)

    first = redact_repository_addresses(
        text="src/example.py and src\\example.py",
        addresses=addresses,
    )
    second = redact_repository_addresses(
        text="src/example.py and src\\example.py",
        addresses=addresses,
    )

    assert first == second
    assert "src/example.py" not in first
    assert "src\\example.py" not in first


def test_blindness_audit_accepts_one_to_one_hidden_neutral_resource() -> None:
    result = audit_blinded_packages(
        packages=(_package(evidence=_evidence("Module purpose: bounded source")),),
        mappings=(_mapping(),),
        all_repository_addresses=(RepositoryResourceAddress("src/example.py"),),
    )

    assert result["passed"]
    assert result["cases"] == [
        {
            "case_name": "case",
            "material_resource_count": 1,
            "address_visibility_count": 0,
        },
    ]


def test_blindness_audit_rejects_unapproved_address_leak() -> None:
    result = audit_blinded_packages(
        packages=(
            _package(evidence=_evidence("Module purpose: source from src/example.py")),
        ),
        mappings=(_mapping(),),
        all_repository_addresses=(RepositoryResourceAddress("src/example.py"),),
    )

    assert not result["passed"]
    assert result["violation_count"] >= 1


@pytest.mark.parametrize(
    "leak",
    [
        "PurposeProfile.OUTGOING_DEPENDENCY",
        "RelationshipControl",
        "UsefulnessJudgment.USEFUL",
        "control=True",
        "relation_direction=outgoing",
        "lexical_rank=1 lexical_score=2.0",
        "admission=admitted qualification=qualified displacement=true",
        "oracle outcome",
        "FrozenValidationCase validation design case construction",
    ],
)
def test_blindness_audit_rejects_representative_semantic_leaks(leak: str) -> None:
    result = audit_blinded_packages(
        packages=(_package(evidence=_evidence(leak)),),
        mappings=(_mapping(),),
        all_repository_addresses=(RepositoryResourceAddress("src/example.py"),),
    )

    assert not result["passed"]
    assert any("bounded-evidence semantics" in item for item in result["violations"])


def test_blindness_audit_rejects_nested_prohibited_metadata() -> None:
    nested = cast(
        "object",
        {
            "representation": "structural-outline",
            "resource_kind": "python",
            "semantic_outline": [{"oracle": "member"}],
            "format_version": "fixture",
        },
    )
    result = audit_blinded_packages(
        packages=(_package(evidence=nested),),
        mappings=(_mapping(),),
        all_repository_addresses=(RepositoryResourceAddress("src/example.py"),),
    )

    assert not result["passed"]
    assert any("prohibited item fields" in item for item in result["violations"])


def test_projection_withholds_validation_answer_key_source() -> None:
    source = '''"""Frozen validation design and oracle admission outcomes."""
from somewhere import PurposeProfile, RelationshipControl, UsefulnessJudgment

control = RelationshipControl(direction="outgoing")
expected = UsefulnessJudgment.USEFUL
is_control = True
'''

    evidence = project_blinded_resource_evidence(text=source)

    assert evidence.representation == "withheld"
    serialized = repr(evidence)
    for prohibited in (
        "PurposeProfile",
        "RelationshipControl",
        "UsefulnessJudgment",
        "outgoing",
        "is_control",
        "oracle",
        "admission",
    ):
        assert prohibited not in serialized


def test_projection_retains_legitimate_structural_resource_evidence() -> None:
    source = '''"""Shared Okapi BM25 arithmetic."""

def calculate_term_contribution() -> float:
    return 1.0
'''

    evidence = project_blinded_resource_evidence(text=source)
    result = audit_blinded_packages(
        packages=(_package(evidence=evidence),),
        mappings=(_mapping(),),
        all_repository_addresses=(RepositoryResourceAddress("src/example.py"),),
    )

    assert evidence.representation == "structural-outline"
    assert "Module purpose: Shared Okapi BM25 arithmetic." in evidence.semantic_outline
    assert "Top-level declaration: calculate_term_contribution" in evidence.semantic_outline
    assert result["passed"]


def test_artifact_envelopes_are_deterministic_and_tamper_evident() -> None:
    first = artifact_envelope(schema="fixture-v1", payload={"b": 2, "a": 1})
    second = artifact_envelope(schema="fixture-v1", payload={"a": 1, "b": 2})

    assert first == second
    assert validate_artifact_envelope(first)
    first["payload"]["a"] = 3
    assert not validate_artifact_envelope(first)


def test_capture_package_and_mapping_bind_to_one_capture_identity() -> None:
    capture = artifact_envelope(
        schema="capture-v1",
        payload={"capture_set_identity": "capture", "design_fingerprint": "design"},
    )
    package = artifact_envelope(
        schema="package-v1",
        payload={"capture_set_identity": "capture", "design_fingerprint": "design"},
    )
    mapping = artifact_envelope(
        schema="mapping-v1",
        payload={"capture_set_identity": "capture", "design_fingerprint": "design"},
    )

    assert validate_artifact_correspondence(
        capture=capture,
        package=package,
        mapping=mapping,
    )
    mapping["payload"]["capture_set_identity"] = "different"
    assert not validate_artifact_correspondence(
        capture=capture,
        package=package,
        mapping=mapping,
    )


def test_repair_reprojects_existing_membership_without_mechanism_execution() -> None:
    capture = artifact_envelope(
        schema="capture-v1",
        payload={
            "capture_set_identity": "capture",
            "design_fingerprint": "design",
            "case_capture_identities": ["case-capture"],
        },
    )
    invalid = artifact_envelope(
        schema="package-v1",
        payload={
            "capture_set_identity": "capture",
            "design_fingerprint": "design",
            "package_set_identity": "invalid-package",
            "packages": [
                {
                    "case_name": "case",
                    "information_need": "need",
                    "purpose_rationale": "rationale",
                    "items": [
                        {
                            "neutral_id": "resource-0123456789abcdef",
                            "bounded_evidence": '"""Useful implementation."""\ndef operation():\n    pass\n',
                            "visible_address": None,
                        },
                    ],
                    "capture_identity": "case-capture",
                    "design_fingerprint": "design",
                    "protocol_version": "increment-23-blinded-adjudication-v1",
                },
            ],
        },
    )
    mapping = artifact_envelope(
        schema="mapping-v1",
        payload={
            "capture_set_identity": "capture",
            "design_fingerprint": "design",
            "mappings": [
                [
                    {
                        "neutral_id": "resource-0123456789abcdef",
                        "address": "src/example.py",
                        "address_visible_to_adjudicator": False,
                    },
                ],
            ],
        },
    )

    repaired = repair_blinded_package_artifact(
        capture=capture,
        invalid_package=invalid,
        mapping=mapping,
    )
    repaired_case = repaired["payload"]["packages"][0]
    loaded = load_blinded_adjudication_packages(repaired)

    assert validate_artifact_envelope(repaired)
    assert repaired_case["items"][0]["neutral_id"] == "resource-0123456789abcdef"
    assert repaired_case["items"][0]["bounded_evidence"]["representation"] == "structural-outline"
    assert repaired_case["protocol_version"] == "increment-23-blinded-adjudication-v2"
    assert repaired["payload"]["blindness_audit"]["passed"]
    assert loaded[0].case_name == "case"
    assert loaded[0].items[0].neutral_id == "resource-0123456789abcdef"
    assert isinstance(loaded[0].items[0].bounded_evidence.semantic_outline, tuple)


def test_invalid_package_record_retains_identity_without_judgments() -> None:
    invalid = artifact_envelope(schema="package-v1", payload={"value": 1})

    record = invalid_blinded_package_record(
        invalid_package=invalid,
        raw_sha256="a" * 64,
        preserved_filename=".invalid-package.json",
    )

    assert validate_artifact_envelope(record)
    assert record["payload"]["status"] == "invalid-for-adjudication"
    assert record["payload"]["contains_adjudication_judgments"] is False
    assert "judgments" not in record["payload"]


def test_frozen_adjudication_artifact_round_trips_only_blinded_state() -> None:
    package = _package(evidence=_evidence("Module purpose: relevant implementation."))
    records = (
        ImmutableAdjudicationRecord(
            neutral_id="resource-0123456789abcdef",
            judgment=UsefulnessJudgment.USEFUL,
            rationale="The visible outline directly identifies the requested implementation.",
            address_visible_to_adjudicator=False,
            provenance="independent-blinded-adjudication:corrected-v2-package-only",
        ),
    )
    frozen = freeze_adjudication_set(
        packages=(package,),
        records_by_case={package.case_name: records},
        package_set_identity="package-set",
    )
    artifact = frozen_adjudication_artifact(frozen)
    loaded = load_frozen_adjudication_artifact(
        envelope=artifact,
        packages=(package,),
        package_set_identity="package-set",
    )

    assert loaded == frozen
    assert audit_frozen_adjudication_artifact(artifact)["passed"]
    serialized = str(artifact)
    assert "is_control" not in serialized
    assert "repository_address" not in serialized
