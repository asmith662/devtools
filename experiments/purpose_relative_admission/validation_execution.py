# Copyright (c) 2026
# ruff: noqa: ANN401, E501, PLR0913, T201
# mypy: disable-error-code="arg-type,attr-defined,index,no-any-return,no-untyped-call,union-attr"
"""Execute one Increment-23 capture and persist separate blinded evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import (
    directional_reservation_v1_fingerprint,
)
from experiments.purpose_relative_admission.direct_resolution import (
    run_exact_name_direct_resolution_control,
)
from experiments.purpose_relative_admission.evaluation import (
    _function_declarations,
    construct_frozen_case_ranking,
)
from experiments.purpose_relative_admission.reservation import direction_for_profile
from experiments.purpose_relative_admission.surfaces import (
    construct_relationship_surfaces,
)
from experiments.purpose_relative_admission.validation_adjudication import (
    AdjudicationResourceMapping,
    BlindedAdjudicationItem,
    BlindedAdjudicationPackage,
    BlindedResourceEvidence,
    FrozenAdjudication,
    FrozenAdjudicationSet,
    ImmutableAdjudicationRecord,
    build_blinded_adjudication_package,
    validate_frozen_adjudication_set,
)
from experiments.purpose_relative_admission.validation_capture import (
    CapturedCaseSurface,
    RepositoryCheckpoint,
    captured_direct_resolution_control,
)
from experiments.purpose_relative_admission.validation_design import (
    INCREMENT_22_RULE_FINGERPRINT,
    FrozenValidationCase,
    direct_resolution_validation_controls,
    frozen_validation_cases,
    increment_23_validation_design_fingerprint,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment
from experiments.purpose_relative_import.comparison import (
    _derive_relations,
    blind_insert,
)
from scripts.retrieval_bm25_baseline import run_benchmark

if TYPE_CHECKING:
    from collections.abc import Sequence

_EXPECTED_DESIGN_FINGERPRINT = "c36d39f18258e918f8a1023a22d821619fc08cb8840d4ed80aae31832feabef7"
_EXPECTED_RULE_FINGERPRINT = "7e215ac2961a4329074e9a25d35d3decc554f394435aa0b73cb2251254160345"
_CHECKPOINT_HEAD = "0f61f3d328bad3d4743130e2e1fb1e8f6698fb19"
_CAPTURE_SCHEMA = "devtools-b0002-increment-23-hidden-surface-capture-v1"
_PACKAGE_SCHEMA = "devtools-b0002-increment-23-blinded-adjudication-package-v2"
_MAPPING_SCHEMA = "devtools-b0002-increment-23-neutral-resource-mapping-v1"
_INVALIDATION_SCHEMA = (
    "devtools-b0002-increment-23-invalid-blinded-package-record-v1"
)
_FROZEN_ADJUDICATION_SCHEMA = (
    "devtools-b0002-increment-23-frozen-adjudication-v2"
)
_PURPOSE_RATIONALE = (
    "Judge whether each supplied resource is materially useful for answering the "
    "frozen information need, using only the bounded evidence shown."
)
_FORBIDDEN_BLINDED_ITEM_FIELDS = frozenset(
    {
        "rank",
        "score",
        "lexical_rank",
        "lexical_score",
        "top_five",
        "top_fifteen",
        "mechanism_origin",
        "purpose_profile",
        "relationship_control",
        "relation_source",
        "relation_target",
        "relation_direction",
        "support_count",
        "relation_identity",
        "expected_judgment",
        "usefulness_judgment",
        "is_control",
        "qualification",
        "admission",
        "abstention",
        "displacement",
        "blind_reference",
        "oracle",
        "final_outcome",
    },
)
_SEMANTIC_LEAK_PATTERNS = (
    ("purpose-profile", re.compile(r"\bPurposeProfile\b|\bpurpose[_ -]?profiles?\b|\bprofiles?[_ -]?controls?\b", re.IGNORECASE)),
    ("relationship-control", re.compile(r"\bRelationshipControl\b|\brelationship[_ -]?controls?\b|\bdirect[_ -]?resolution[_ -]?controls?\b", re.IGNORECASE)),
    ("usefulness-answer", re.compile(r"\bUsefulnessJudgment\b|\bexpected[_ -]?usefulness\b|\brelevance judgments?\b", re.IGNORECASE)),
    ("control-answer", re.compile(r"\bcontrol\s*=\s*True\b|\bis_control\b|\bexplicit[_ -]?control\b", re.IGNORECASE)),
    ("relation-mechanism", re.compile(r"\brelation[_ -]?(?:source|target|direction|support(?:_count)?)\b", re.IGNORECASE)),
    ("lexical-mechanism", re.compile(r"\blexical[_ -]?(?:rank|score)\b", re.IGNORECASE)),
    ("mechanism-origin", re.compile(r"\bmechanism[_ -]?(?:origin|provenance)\b", re.IGNORECASE)),
    ("decision-outcome", re.compile(r"\b(?:qualification|admission|abstention|displacement|oracle)(?:[_ -]?(?:status|outcome|result|membership))?\b", re.IGNORECASE)),
    ("validation-answer-key", re.compile(r"\bFrozenValidationCase\b|\bvalidation[_ -]?design\b|\bcase[_ -]?construction\b|\bfrozen[_ -]?(?:cases|increment[_ -]?23)\b", re.IGNORECASE)),
)
_REPOSITORY_ADDRESS_SHAPE = re.compile(
    r"(?i)(?:^|[\s\"'`(])(?:src|tests|docs|experiments|scripts)[\\/]"
    r"[A-Za-z0-9_.\\/-]+",
)
_WITHHELD_OUTLINE = (
    "Semantic evidence unavailable under the blinded structural projection.",
)


def run_surface_capture(*, repository_root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Run one judgment-free repository capture and build three linked artifacts."""
    design_fingerprint = increment_23_validation_design_fingerprint()
    rule_fingerprint = directional_reservation_v1_fingerprint()
    if design_fingerprint != _EXPECTED_DESIGN_FINGERPRINT:
        msg = "Increment-23 validation design fingerprint changed."
        raise RuntimeError(msg)
    if rule_fingerprint != _EXPECTED_RULE_FINGERPRINT or rule_fingerprint != INCREMENT_22_RULE_FINGERPRINT:
        msg = "Increment-22 directional-reservation-v1 fingerprint changed."
        raise RuntimeError(msg)

    benchmark = run_benchmark(repository_root=repository_root)
    relations, relation_coverage, interpretations = _derive_relations(benchmark.snapshot)
    checkpoint = RepositoryCheckpoint(
        str(benchmark.definition.discovery.repository_id),
        str(benchmark.snapshot.id),
        str(benchmark.corpus.id),
        len(benchmark.documents.documents),
        (
            ("maximum_discovered_resources", 10_000),
            ("maximum_traversal_entries", 20_000),
            ("maximum_resource_bytes", 1_048_576),
        ),
    )
    cases = frozen_validation_cases()
    captures = tuple(
        _capture_case(
            case=case,
            checkpoint=checkpoint,
            index=benchmark.index,
            relations=relations,
            interpretations=interpretations,
            design_fingerprint=design_fingerprint,
        )
        for case in cases
    )

    declarations = _function_declarations(benchmark.snapshot)
    direct_controls = tuple(
        captured_direct_resolution_control(
            name=control.name,
            result=run_exact_name_direct_resolution_control(
                declared_name=control.declared_name,
                declarations=declarations,
            ),
        )
        for control in direct_resolution_validation_controls()
    )
    all_addresses = tuple(benchmark.definition.selected_addresses)
    packages_and_mappings = tuple(
        _package_case(
            capture=capture,
            snapshot=benchmark.snapshot,
            all_repository_addresses=all_addresses,
        )
        for capture in captures
    )
    packages = tuple(value[0] for value in packages_and_mappings)
    mappings = tuple(value[1] for value in packages_and_mappings)
    capture_set_identity = _digest(
        {
            "design_fingerprint": design_fingerprint,
            "rule_fingerprint": rule_fingerprint,
            "checkpoint": checkpoint,
            "case_capture_identities": tuple(capture.identity() for capture in captures),
            "direct_controls": direct_controls,
        },
    )
    package_set_identity = _digest(
        {
            "capture_set_identity": capture_set_identity,
            "packages": packages,
        },
    )
    mapping_set_identity = _digest(
        {
            "capture_set_identity": capture_set_identity,
            "mappings": mappings,
        },
    )
    audit = audit_blinded_packages(
        packages=packages,
        mappings=mappings,
        all_repository_addresses=all_addresses,
    )
    if not audit["passed"]:
        msg = "Blinded adjudication package failed its mechanical blindness audit."
        raise RuntimeError(msg)

    capture_payload = {
        "scope": "hidden internal experiment evidence; not an adjudicator input",
        "repository_checkpoint": {
            "branch": "main",
            "head": _CHECKPOINT_HEAD,
            "checkpoint": checkpoint,
        },
        "acquisition": {
            "discovered_resource_count": len(benchmark.discovery.addresses),
            "examined_entry_count": benchmark.discovery.examined_entry_count,
            "selected_resource_count": len(benchmark.definition.selected_addresses),
            "observed_resource_count": len(benchmark.snapshot.resources),
            "document_count": len(benchmark.documents.documents),
            "bounds": dict(checkpoint.acquisition_bounds),
        },
        "relation_coverage": relation_coverage,
        "design_fingerprint": design_fingerprint,
        "rule_fingerprint": rule_fingerprint,
        "capture_set_identity": capture_set_identity,
        "case_capture_identities": [capture.identity() for capture in captures],
        "cases": captures,
        "direct_resolution_controls": direct_controls,
        "successful_capture_run_count": 1,
        "mechanical_failure_history": [],
    }
    package_payload = {
        "scope": "adjudicator-facing blinded evidence only",
        "design_fingerprint": design_fingerprint,
        "capture_set_identity": capture_set_identity,
        "package_set_identity": package_set_identity,
        "packages": packages,
        "blindness_audit": audit,
    }
    mapping_payload = {
        "scope": "hidden neutral-id mapping; not an adjudicator input",
        "design_fingerprint": design_fingerprint,
        "capture_set_identity": capture_set_identity,
        "mapping_set_identity": mapping_set_identity,
        "case_capture_identities": [capture.identity() for capture in captures],
        "mappings": mappings,
    }
    return (
        artifact_envelope(schema=_CAPTURE_SCHEMA, payload=capture_payload),
        artifact_envelope(schema=_PACKAGE_SCHEMA, payload=package_payload),
        artifact_envelope(schema=_MAPPING_SCHEMA, payload=mapping_payload),
    )


def _capture_case(
    *,
    case: FrozenValidationCase,
    checkpoint: RepositoryCheckpoint,
    index: Any,
    relations: tuple[Any, ...],
    interpretations: Mapping[RepositoryResourceAddress, tuple[Any, ...]],
    design_fingerprint: str,
) -> CapturedCaseSurface:
    ranking = construct_frozen_case_ranking(
        name=case.name,
        query=case.query_text,
        profile=case.profile,
        index=index,
        relations=relations,
        interpretations_by_address=interpretations,
    )
    outgoing = construct_relationship_surfaces(surfaces=ranking.outgoing)
    incoming = construct_relationship_surfaces(surfaces=ranking.incoming)
    direction = direction_for_profile(case.profile)
    eligible = (
        ()
        if direction is None
        else outgoing
        if direction is ImportRelationshipDirection.OUTGOING
        else incoming
    )
    canonical = tuple(item.address for item in ranking.lexical[:5])
    return CapturedCaseSurface(
        case.name,
        case.information_need,
        case.query_text,
        case.profile,
        case.route,
        design_fingerprint,
        checkpoint,
        ranking.lexical[:5],
        ranking.lexical,
        tuple(item.address for item in ranking.lexical[5:15]),
        outgoing,
        incoming,
        eligible,
        ranking.practical.retained_targets,
        ranking.practical,
        (*outgoing, *incoming),
        blind_insert(
            canonical=canonical,
            relationship_surfaces=(*ranking.outgoing, *ranking.incoming),
        ),
        None,
    )


def _package_case(
    *,
    capture: CapturedCaseSurface,
    snapshot: Any,
    all_repository_addresses: Sequence[RepositoryResourceAddress],
) -> tuple[BlindedAdjudicationPackage, tuple[AdjudicationResourceMapping, ...]]:
    evidence = {
        address: project_blinded_resource_evidence(
            text=redact_repository_addresses(
                text=snapshot.resource_at(address).content,
                addresses=all_repository_addresses,
            ),
        )
        for address in capture.material_addresses
    }
    return build_blinded_adjudication_package(
        capture=capture,
        purpose_rationale=_PURPOSE_RATIONALE,
        bounded_evidence_by_address=evidence,
        address_visible={},
    )


def project_blinded_resource_evidence(*, text: str) -> BlindedResourceEvidence:
    """Derive a structural outline without exposing arbitrary resource bodies."""
    evidence = _python_structural_evidence(text=text)
    if evidence is None:
        evidence = _markdown_structural_evidence(text=text)
    if evidence is None or _semantic_evidence_violations(evidence):
        return BlindedResourceEvidence("withheld", "unavailable", _WITHHELD_OUTLINE)
    return evidence


def _python_structural_evidence(*, text: str) -> BlindedResourceEvidence | None:
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return None
    outline: list[str] = []
    module_summary = ast.get_docstring(tree, clean=True)
    if module_summary:
        outline.append(f"Module purpose: {_first_semantic_line(module_summary)}")
    declarations = tuple(
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
        and not (node.name.startswith("__") and node.name.endswith("__"))
    )
    outline.extend(f"Top-level declaration: {name}" for name in declarations[:40])
    if not outline:
        outline.append("Python resource with no module purpose or top-level declarations.")
    return BlindedResourceEvidence("structural-outline", "python", tuple(outline))


def _markdown_structural_evidence(*, text: str) -> BlindedResourceEvidence | None:
    headings = tuple(
        line.strip()
        for line in text.splitlines()
        if re.fullmatch(r"#{1,4}\s+[^#].*", line.strip())
    )
    if not headings:
        return None
    return BlindedResourceEvidence(
        "structural-outline",
        "markdown",
        tuple(f"Document heading: {heading}" for heading in headings[:40]),
    )


def _first_semantic_line(value: str) -> str:
    return " ".join(value.strip().splitlines()[0].split())


def _semantic_evidence_violations(value: object) -> tuple[str, ...]:
    """Defensively reject known leak classes after safe structural projection."""
    serialized = _canonical_json(_json_value(value))
    violations = [
        label for label, pattern in _SEMANTIC_LEAK_PATTERNS if pattern.search(serialized)
    ]
    if _REPOSITORY_ADDRESS_SHAPE.search(serialized):
        violations.append("repository-address-shape")
    return tuple(violations)


def redact_repository_addresses(
    *,
    text: str,
    addresses: Sequence[RepositoryResourceAddress],
) -> str:
    """Remove exact repository addresses from otherwise exact observed content."""
    redacted = text
    for address in sorted(addresses, key=lambda item: (-len(item.value), item.value)):
        redacted = redacted.replace(address.value, "[repository-address-redacted]")
        redacted = redacted.replace(address.value.replace("/", "\\"), "[repository-address-redacted]")
    return redacted


def audit_blinded_packages(
    *,
    packages: Sequence[BlindedAdjudicationPackage],
    mappings: Sequence[Sequence[AdjudicationResourceMapping]],
    all_repository_addresses: Sequence[RepositoryResourceAddress],
) -> dict[str, Any]:
    """Fail closed on prohibited fields, unapproved addresses, or mapping mismatch."""
    violations: list[str] = []
    material_counts: list[dict[str, Any]] = []
    for package, case_mappings in zip(packages, mappings, strict=True):
        item_ids = tuple(item.neutral_id for item in package.items)
        mapping_ids = tuple(mapping.neutral_id for mapping in case_mappings)
        if len(item_ids) != len(set(item_ids)) or item_ids != mapping_ids:
            violations.append(f"{package.case_name}: neutral IDs are not one-to-one and ordered.")
        item_payloads = [_json_value(item) for item in package.items]
        for item_payload, mapping in zip(item_payloads, case_mappings, strict=True):
            prohibited = _FORBIDDEN_BLINDED_ITEM_FIELDS & _nested_mapping_keys(
                item_payload,
            )
            if prohibited:
                violations.append(f"{package.case_name}: prohibited item fields {sorted(prohibited)}.")
            serialized = _canonical_json(item_payload)
            semantic_violations = _semantic_evidence_violations(
                item_payload["bounded_evidence"],
            )
            if semantic_violations:
                violations.append(
                    f"{package.case_name}: prohibited bounded-evidence semantics "
                    f"{list(semantic_violations)}.",
                )
            for address in all_repository_addresses:
                variants = (address.value, address.value.replace("/", "\\"))
                if any(value in serialized for value in variants) and (
                    not mapping.address_visible_to_adjudicator
                    or mapping.address != address
                ):
                    violations.append(
                        f"{package.case_name}: unapproved repository address leaked.",
                    )
                    break
            if mapping.address_visible_to_adjudicator != (item_payload["visible_address"] is not None):
                violations.append(f"{package.case_name}: address visibility fact mismatches item.")
        material_counts.append(
            {
                "case_name": package.case_name,
                "material_resource_count": len(package.items),
                "address_visibility_count": sum(item.visible_address is not None for item in package.items),
            },
        )
    return {
        "passed": not violations,
        "violation_count": len(violations),
        "violations": violations,
        "cases": material_counts,
        "checks": [
            "one neutral identifier per material resource",
            "no prohibited mechanism field at any serialized item depth",
            "structural bounded evidence contains no protected semantic leak class",
            "no unapproved repository address in serialized blinded items",
            "address visibility facts correspond to serialized items",
        ],
    }


def _nested_mapping_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        return {
            *(str(key) for key in value),
            *(
                nested
                for item in value.values()
                for nested in _nested_mapping_keys(item)
            ),
        }
    if isinstance(value, list | tuple):
        return {
            nested for item in value for nested in _nested_mapping_keys(item)
        }
    return set()


def repair_blinded_package_artifact(
    *,
    capture: Mapping[str, Any],
    invalid_package: Mapping[str, Any],
    mapping: Mapping[str, Any],
) -> dict[str, Any]:
    """Reproject retained raw evidence without reacquisition or mechanism replay."""
    if not validate_artifact_correspondence(
        capture=capture,
        package=invalid_package,
        mapping=mapping,
    ):
        msg = "Blindness repair inputs do not belong to one intact capture."
        raise ValueError(msg)
    capture_payload = capture["payload"]
    invalid_payload = invalid_package["payload"]
    mapping_payload = mapping["payload"]
    capture_identities = capture_payload["case_capture_identities"]
    invalid_packages = invalid_payload["packages"]
    mapping_groups = mapping_payload["mappings"]
    if not (
        len(capture_identities) == len(invalid_packages) == len(mapping_groups)
    ):
        msg = "Blindness repair inputs have different case cardinalities."
        raise ValueError(msg)

    repaired_packages: list[BlindedAdjudicationPackage] = []
    typed_mapping_groups: list[tuple[AdjudicationResourceMapping, ...]] = []
    for capture_identity, invalid_case, mapping_group in zip(
        capture_identities,
        invalid_packages,
        mapping_groups,
        strict=True,
    ):
        repaired_case, typed_mappings = _repair_blinded_case(
            capture_identity=capture_identity,
            invalid_case=invalid_case,
            mapping_group=mapping_group,
        )
        repaired_packages.append(repaired_case)
        typed_mapping_groups.append(typed_mappings)

    repaired = tuple(repaired_packages)
    typed_mappings = tuple(typed_mapping_groups)
    all_material_addresses = tuple(
        item.address for group in typed_mappings for item in group
    )
    audit = audit_blinded_packages(
        packages=repaired,
        mappings=typed_mappings,
        all_repository_addresses=all_material_addresses,
    )
    if not audit["passed"]:
        msg = "Corrected blinded package failed the strengthened blindness audit."
        raise ValueError(msg)
    capture_set_identity = capture_payload["capture_set_identity"]
    package_set_identity = _digest(
        {
            "capture_set_identity": capture_set_identity,
            "packages": repaired,
        },
    )
    payload = {
        "scope": "adjudicator-facing structural blinded evidence only",
        "design_fingerprint": capture_payload["design_fingerprint"],
        "capture_set_identity": capture_set_identity,
        "package_set_identity": package_set_identity,
        "packages": repaired,
        "blindness_audit": audit,
    }
    return artifact_envelope(schema=_PACKAGE_SCHEMA, payload=payload)


def load_blinded_adjudication_packages(
    envelope: Mapping[str, Any],
) -> tuple[BlindedAdjudicationPackage, ...]:
    """Load only the validated v2 adjudicator view, without hidden artifacts."""
    if envelope.get("schema") != _PACKAGE_SCHEMA or not validate_artifact_envelope(
        envelope,
    ):
        msg = "Blinded adjudication artifact is not an intact v2 package."
        raise ValueError(msg)
    payload = envelope["payload"]
    expected_set_identity = _digest(
        {
            "capture_set_identity": payload["capture_set_identity"],
            "packages": payload["packages"],
        },
    )
    if payload["package_set_identity"] != expected_set_identity:
        msg = "Blinded adjudication package-set identity does not reconstruct."
        raise ValueError(msg)
    packages = tuple(_load_blinded_case(value) for value in payload["packages"])
    if any(
        package.design_fingerprint != payload["design_fingerprint"]
        for package in packages
    ):
        msg = "Blinded case design differs from its package set."
        raise ValueError(msg)
    return packages


def _load_blinded_case(value: Mapping[str, Any]) -> BlindedAdjudicationPackage:
    return BlindedAdjudicationPackage(
        value["case_name"],
        value["information_need"],
        value["purpose_rationale"],
        tuple(
            BlindedAdjudicationItem(
                item["neutral_id"],
                BlindedResourceEvidence(
                    item["bounded_evidence"]["representation"],
                    item["bounded_evidence"]["resource_kind"],
                    tuple(item["bounded_evidence"]["semantic_outline"]),
                    item["bounded_evidence"]["format_version"],
                ),
                item["visible_address"],
            )
            for item in value["items"]
        ),
        value["capture_identity"],
        value["design_fingerprint"],
        value["protocol_version"],
    )


def _repair_blinded_case(
    *,
    capture_identity: str,
    invalid_case: Mapping[str, Any],
    mapping_group: Sequence[Mapping[str, Any]],
) -> tuple[BlindedAdjudicationPackage, tuple[AdjudicationResourceMapping, ...]]:
    if invalid_case["capture_identity"] != capture_identity:
        msg = "Blinded case does not bind to the retained case capture."
        raise ValueError(msg)
    invalid_items = invalid_case["items"]
    if len(invalid_items) != len(mapping_group):
        msg = "Blinded case and neutral mapping cardinalities differ."
        raise ValueError(msg)
    typed_mappings = tuple(
        AdjudicationResourceMapping(
            item["neutral_id"],
            RepositoryResourceAddress(item["address"]),
            item["address_visible_to_adjudicator"],
        )
        for item in mapping_group
    )
    repaired_items = tuple(
        _repair_blinded_item(invalid_item=invalid_item, mapping=typed_mapping)
        for invalid_item, typed_mapping in zip(
            invalid_items,
            typed_mappings,
            strict=True,
        )
    )
    return (
        BlindedAdjudicationPackage(
            invalid_case["case_name"],
            invalid_case["information_need"],
            invalid_case["purpose_rationale"],
            repaired_items,
            capture_identity,
            invalid_case["design_fingerprint"],
        ),
        typed_mappings,
    )


def _repair_blinded_item(
    *,
    invalid_item: Mapping[str, Any],
    mapping: AdjudicationResourceMapping,
) -> BlindedAdjudicationItem:
    if invalid_item["neutral_id"] != mapping.neutral_id:
        msg = "Blinded item and neutral mapping identities differ."
        raise ValueError(msg)
    if invalid_item["visible_address"] is not None:
        msg = "The invalid package unexpectedly exposed an address field."
        raise ValueError(msg)
    raw_evidence = invalid_item["bounded_evidence"]
    if not isinstance(raw_evidence, str):
        msg = "Blindness repair requires the retained v1 raw evidence carrier."
        raise TypeError(msg)
    return BlindedAdjudicationItem(
        mapping.neutral_id,
        project_blinded_resource_evidence(text=raw_evidence),
        None,
    )


def invalid_blinded_package_record(
    *,
    invalid_package: Mapping[str, Any],
    raw_sha256: str,
    preserved_filename: str,
) -> dict[str, Any]:
    """Record why one byte-preserved adjudicator package cannot be used."""
    if not validate_artifact_envelope(invalid_package):
        msg = "Cannot invalidate an internally damaged artifact envelope."
        raise ValueError(msg)
    return artifact_envelope(
        schema=_INVALIDATION_SCHEMA,
        payload={
            "preserved_filename": preserved_filename,
            "raw_sha256": raw_sha256,
            "envelope_content_identity": invalid_package["content_identity"],
            "status": "invalid-for-adjudication",
            "reason": "semantic-blindness-failed-arbitrary-resource-body-exposed-experiment-control-state",
            "contains_adjudication_judgments": False,
        },
    )


def frozen_adjudication_artifact(
    frozen: FrozenAdjudicationSet,
) -> dict[str, Any]:
    """Serialize a blinded freeze without addresses or evaluation truth."""
    return artifact_envelope(
        schema=_FROZEN_ADJUDICATION_SCHEMA,
        payload={
            "design_fingerprint": frozen.design_fingerprint,
            "package_set_identity": frozen.package_set_identity,
            "protocol_version": frozen.protocol_version,
            "adjudication_fingerprint": frozen.fingerprint,
            "cases": [
                {
                    "case_name": case_name,
                    "design_fingerprint": case_frozen.design_fingerprint,
                    "capture_identity": case_frozen.capture_identity,
                    "package_identity": case_frozen.package_identity,
                    "protocol_version": case_frozen.protocol_version,
                    "adjudication_fingerprint": case_frozen.fingerprint,
                    "records": [
                        {
                            "neutral_id": record.neutral_id,
                            "judgment": record.judgment.value,
                            "rationale": record.rationale,
                            "address_visible_to_adjudicator": record.address_visible_to_adjudicator,
                            "provenance": record.provenance,
                            "record_version": record.record_version,
                        }
                        for record in case_frozen.records
                    ],
                }
                for case_name, case_frozen in frozen.cases
            ],
        },
    )


def load_frozen_adjudication_artifact(
    *,
    envelope: Mapping[str, Any],
    packages: Sequence[BlindedAdjudicationPackage],
    package_set_identity: str,
) -> FrozenAdjudicationSet:
    """Reconstruct and validate a complete freeze while still blinded."""
    if envelope.get("schema") != _FROZEN_ADJUDICATION_SCHEMA or not validate_artifact_envelope(
        envelope,
    ):
        msg = "Frozen adjudication artifact is not an intact v2 envelope."
        raise ValueError(msg)
    payload = envelope["payload"]
    cases = tuple(
        (
            case["case_name"],
            FrozenAdjudication(
                case["design_fingerprint"],
                case["capture_identity"],
                case["package_identity"],
                case["protocol_version"],
                tuple(
                    ImmutableAdjudicationRecord(
                        record["neutral_id"],
                        UsefulnessJudgment(record["judgment"]),
                        record["rationale"],
                        record["address_visible_to_adjudicator"],
                        record["provenance"],
                        record["record_version"],
                    )
                    for record in case["records"]
                ),
                case["adjudication_fingerprint"],
            ),
        )
        for case in payload["cases"]
    )
    frozen = FrozenAdjudicationSet(
        payload["design_fingerprint"],
        payload["package_set_identity"],
        payload["protocol_version"],
        cases,
        payload["adjudication_fingerprint"],
    )
    validate_frozen_adjudication_set(
        packages=packages,
        frozen=frozen,
        package_set_identity=package_set_identity,
    )
    return frozen


def audit_frozen_adjudication_artifact(
    envelope: Mapping[str, Any],
) -> dict[str, Any]:
    """Defensively audit the allowlisted frozen blinded representation."""
    violations: list[str] = []
    if envelope.get("schema") != _FROZEN_ADJUDICATION_SCHEMA or not validate_artifact_envelope(
        envelope,
    ):
        violations.append("artifact envelope or schema is invalid")
        return {"passed": False, "violations": violations}
    payload = envelope["payload"]
    allowed_payload = {
        "design_fingerprint",
        "package_set_identity",
        "protocol_version",
        "adjudication_fingerprint",
        "cases",
    }
    allowed_case = {
        "case_name",
        "design_fingerprint",
        "capture_identity",
        "package_identity",
        "protocol_version",
        "adjudication_fingerprint",
        "records",
    }
    allowed_record = {
        "neutral_id",
        "judgment",
        "rationale",
        "address_visible_to_adjudicator",
        "provenance",
        "record_version",
    }
    if set(payload) != allowed_payload:
        violations.append("payload fields differ from the blinded freeze allowlist")
    for case in payload.get("cases", ()):  # pragma: no branch - malformed input is reported
        if set(case) != allowed_case:
            violations.append("case fields differ from the blinded freeze allowlist")
        for record in case.get("records", ()):
            if set(record) != allowed_record:
                violations.append("record fields differ from the blinded freeze allowlist")
            if record.get("address_visible_to_adjudicator") is not False:
                violations.append("a frozen record reports visible address evidence")
            rationale = str(record.get("rationale", ""))
            if _REPOSITORY_ADDRESS_SHAPE.search(rationale):
                violations.append("a rationale contains an address-shaped value")
            if any(
                pattern.search(rationale)
                for _name, pattern in _SEMANTIC_LEAK_PATTERNS
            ):
                violations.append("a rationale contains prohibited mechanism semantics")
    return {
        "passed": not violations,
        "violations": violations,
        "case_count": len(payload.get("cases", ())),
        "record_count": sum(
            len(case.get("records", ())) for case in payload.get("cases", ())
        ),
    }


def artifact_envelope(*, schema: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    """Wrap deterministic content with an independently recomputable identity."""
    serialized_payload = _json_value(payload)
    return {
        "schema": schema,
        "content_identity": _digest(serialized_payload),
        "payload": serialized_payload,
    }


def validate_artifact_envelope(envelope: Mapping[str, Any]) -> bool:
    """Validate a retained artifact without repository acquisition or reranking."""
    return envelope.get("content_identity") == _digest(envelope.get("payload"))


def validate_artifact_correspondence(
    *,
    capture: Mapping[str, Any],
    package: Mapping[str, Any],
    mapping: Mapping[str, Any],
) -> bool:
    """Confirm three envelopes bind to one capture and remain internally intact."""
    if not all(validate_artifact_envelope(item) for item in (capture, package, mapping)):
        return False
    capture_identity = capture["payload"]["capture_set_identity"]
    return (
        package["payload"]["capture_set_identity"] == capture_identity
        and mapping["payload"]["capture_set_identity"] == capture_identity
        and package["payload"]["design_fingerprint"] == capture["payload"]["design_fingerprint"]
        and mapping["payload"]["design_fingerprint"] == capture["payload"]["design_fingerprint"]
    )


def write_artifact(*, path: Path, envelope: Mapping[str, Any]) -> None:
    """Persist one deterministic retained JSON artifact."""
    path.write_text(
        json.dumps(envelope, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(_json_value(value)).encode()).hexdigest()


def _canonical_json(value: object) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def _json_value(value: object) -> Any:
    if isinstance(value, RepositoryResourceAddress):
        return value.value
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _json_value(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    return value


def main() -> None:
    """Perform the one authorized capture and write three separated artifacts."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--capture-path", type=Path, required=True)
    parser.add_argument("--package-path", type=Path, required=True)
    parser.add_argument("--mapping-path", type=Path, required=True)
    parsed = parser.parse_args()
    capture, package, mapping = run_surface_capture(
        repository_root=parsed.repository_root.resolve(),
    )
    write_artifact(path=parsed.capture_path, envelope=capture)
    write_artifact(path=parsed.package_path, envelope=package)
    write_artifact(path=parsed.mapping_path, envelope=mapping)
    print("Increment-23 surface capture artifacts written; adjudication not started.")


if __name__ == "__main__":
    main()
