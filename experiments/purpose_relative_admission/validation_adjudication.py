# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM102, I001, TC001, TRY003
"""Build blinded Increment-23 adjudication packages and immutable freezes."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.purpose_relative_admission.validation_capture import CapturedCaseSurface
from experiments.purpose_relative_import.cases import UsefulnessJudgment

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

_PROTOCOL_VERSION = "increment-23-blinded-adjudication-v2"
_EVIDENCE_FORMAT_VERSION = "increment-23-structural-resource-evidence-v1"
_JUDGMENT_RECORD_VERSION = "increment-23-blinded-judgment-record-v2"
_ADJUDICATION_SET_PROTOCOL = "increment-23-frozen-blinded-adjudication-v2"


@dataclass(frozen=True, slots=True)
class AdjudicationResourceMapping:
    """Keep the neutral-to-real identity mapping outside the adjudicator payload."""

    neutral_id: str
    address: RepositoryResourceAddress
    address_visible_to_adjudicator: bool


@dataclass(frozen=True, slots=True)
class BlindedResourceEvidence:
    """Expose only a structural resource outline or an opaque safety withholding."""

    representation: str
    resource_kind: str
    semantic_outline: tuple[str, ...]
    format_version: str = _EVIDENCE_FORMAT_VERSION

    def __post_init__(self) -> None:
        """Keep the adjudicator representation finite and structurally explicit."""
        if self.representation not in {"structural-outline", "withheld"}:
            msg = "Blinded evidence requires a supported structural representation."
            raise ValueError(msg)
        if not self.resource_kind or not self.semantic_outline:
            msg = "Blinded evidence requires a resource kind and nonempty outline."
            raise ValueError(msg)
        if self.representation == "withheld" and self.semantic_outline != (
            "Semantic evidence unavailable under the blinded structural projection.",
        ):
            msg = "Withheld blinded evidence must use the invariant safety notice."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class BlindedAdjudicationItem:
    """The only resource-local evidence visible during blinded judgment."""

    neutral_id: str
    bounded_evidence: BlindedResourceEvidence
    visible_address: str | None


@dataclass(frozen=True, slots=True)
class BlindedAdjudicationPackage:
    """Purpose and bounded resource evidence without mechanism outcome metadata."""

    case_name: str
    information_need: str
    purpose_rationale: str
    items: tuple[BlindedAdjudicationItem, ...]
    capture_identity: str
    design_fingerprint: str
    protocol_version: str = _PROTOCOL_VERSION


@dataclass(frozen=True, slots=True)
class ImmutableAdjudicationRecord:
    """One frozen blinded usefulness judgment without hidden evaluation truth."""

    neutral_id: str
    judgment: UsefulnessJudgment
    rationale: str
    address_visible_to_adjudicator: bool
    provenance: str
    record_version: str = _JUDGMENT_RECORD_VERSION

    def __post_init__(self) -> None:
        """Require only facts legitimately available during blinded judgment."""
        if not self.rationale or not self.provenance:
            msg = "An immutable adjudication record requires rationale and provenance."
            raise ValueError(msg)
        if self.record_version != _JUDGMENT_RECORD_VERSION:
            msg = "Blinded adjudication record version is unsupported."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class FrozenAdjudication:
    """Completed, fingerprinted judgment evidence before unblinding/evaluation."""

    design_fingerprint: str
    capture_identity: str
    package_identity: str
    protocol_version: str
    records: tuple[ImmutableAdjudicationRecord, ...]
    fingerprint: str


@dataclass(frozen=True, slots=True)
class FrozenAdjudicationSet:
    """All case freezes bound to the exact corrected blinded package set."""

    design_fingerprint: str
    package_set_identity: str
    protocol_version: str
    cases: tuple[tuple[str, FrozenAdjudication], ...]
    fingerprint: str


@dataclass(frozen=True, slots=True)
class UnblindedAdjudication:
    """Correlate frozen judgments with addresses after the authorized boundary."""

    frozen_fingerprint: str
    records: tuple[
        tuple[RepositoryResourceAddress, ImmutableAdjudicationRecord], ...
    ]

    def by_address(self) -> dict[
        RepositoryResourceAddress, ImmutableAdjudicationRecord
    ]:
        """Expose one fresh evaluation lookup without mutating frozen records."""
        return dict(self.records)


def build_blinded_adjudication_package(
    *,
    capture: CapturedCaseSurface,
    purpose_rationale: str,
    bounded_evidence_by_address: Mapping[
        RepositoryResourceAddress, BlindedResourceEvidence
    ],
    address_visible: Mapping[RepositoryResourceAddress, bool],
) -> tuple[BlindedAdjudicationPackage, tuple[AdjudicationResourceMapping, ...]]:
    """Project only the frozen need and bounded evidence into a blinded package."""
    mappings = tuple(
        AdjudicationResourceMapping(
            _neutral_id(capture=capture, address=address),
            address,
            address_visible.get(address, False),
        )
        for address in capture.material_addresses
    )
    items = tuple(
        BlindedAdjudicationItem(
            mapping.neutral_id,
            bounded_evidence_by_address[mapping.address],
            mapping.address.value if mapping.address_visible_to_adjudicator else None,
        )
        for mapping in mappings
    )
    return (
        BlindedAdjudicationPackage(
            capture.case_name,
            capture.information_need,
            purpose_rationale,
            items,
            capture.identity(),
            capture.design_fingerprint,
        ),
        mappings,
    )


def freeze_adjudication(
    *,
    package: BlindedAdjudicationPackage,
    records: Sequence[ImmutableAdjudicationRecord],
) -> FrozenAdjudication:
    """Require one completed immutable record for each material package item."""
    record_ids = tuple(record.neutral_id for record in records)
    item_ids = tuple(item.neutral_id for item in package.items)
    if len(record_ids) != len(set(record_ids)) or set(record_ids) != set(item_ids):
        msg = "Adjudication freeze requires exactly one record for every material resource."
        raise ValueError(msg)
    record_by_id = {record.neutral_id: record for record in records}
    ordered = tuple(record_by_id[item.neutral_id] for item in package.items)
    package_identity = blinded_adjudication_package_identity(package)
    fingerprint = _freeze_fingerprint(
        design_fingerprint=package.design_fingerprint,
        capture_identity=package.capture_identity,
        package_identity=package_identity,
        protocol_version=package.protocol_version,
        records=ordered,
    )
    return FrozenAdjudication(
        package.design_fingerprint,
        package.capture_identity,
        package_identity,
        package.protocol_version,
        ordered,
        fingerprint,
    )


def validate_frozen_adjudication(
    *, package: BlindedAdjudicationPackage, frozen: FrozenAdjudication
) -> None:
    """Validate a complete freeze while the adjudicator remains blinded."""
    if frozen.design_fingerprint != package.design_fingerprint:
        msg = "Frozen adjudication design fingerprint differs from blinded package."
        raise ValueError(msg)
    if frozen.capture_identity != package.capture_identity:
        msg = "Frozen adjudication capture identity differs from blinded package."
        raise ValueError(msg)
    expected_package_identity = blinded_adjudication_package_identity(package)
    if frozen.package_identity != expected_package_identity:
        msg = "Frozen adjudication package identity differs from blinded package."
        raise ValueError(msg)
    if frozen.protocol_version != package.protocol_version:
        msg = "Frozen adjudication protocol differs from blinded package."
        raise ValueError(msg)
    expected = _freeze_fingerprint(
        design_fingerprint=frozen.design_fingerprint,
        capture_identity=frozen.capture_identity,
        package_identity=frozen.package_identity,
        protocol_version=frozen.protocol_version,
        records=frozen.records,
    )
    if expected != frozen.fingerprint:
        msg = "Frozen adjudication fingerprint no longer matches its records."
        raise ValueError(msg)
    if len({record.neutral_id for record in frozen.records}) != len(package.items):
        msg = "Frozen adjudication does not cover every material resource."
        raise ValueError(msg)
    expected_ids = {item.neutral_id for item in package.items}
    if {record.neutral_id for record in frozen.records} != expected_ids:
        msg = "Frozen adjudication record identities do not cover the blinded package."
        raise ValueError(msg)
    if tuple(record.neutral_id for record in frozen.records) != tuple(
        item.neutral_id for item in package.items
    ):
        msg = "Frozen adjudication record order differs from the blinded package."
        raise ValueError(msg)


def freeze_adjudication_set(
    *,
    packages: Sequence[BlindedAdjudicationPackage],
    records_by_case: Mapping[str, Sequence[ImmutableAdjudicationRecord]],
    package_set_identity: str,
) -> FrozenAdjudicationSet:
    """Freeze exact ordered case coverage using blinded-phase facts only."""
    case_names = tuple(package.case_name for package in packages)
    if len(case_names) != len(set(case_names)) or set(records_by_case) != set(case_names):
        msg = "Adjudication set requires exactly one record collection per blinded case."
        raise ValueError(msg)
    designs = {package.design_fingerprint for package in packages}
    if len(designs) != 1 or not package_set_identity:
        msg = "Adjudication set requires one design and a package-set identity."
        raise ValueError(msg)
    cases = tuple(
        (
            package.case_name,
            freeze_adjudication(
                package=package,
                records=records_by_case[package.case_name],
            ),
        )
        for package in packages
    )
    design_fingerprint = next(iter(designs))
    fingerprint = _adjudication_set_fingerprint(
        design_fingerprint=design_fingerprint,
        package_set_identity=package_set_identity,
        protocol_version=_ADJUDICATION_SET_PROTOCOL,
        cases=cases,
    )
    frozen = FrozenAdjudicationSet(
        design_fingerprint,
        package_set_identity,
        _ADJUDICATION_SET_PROTOCOL,
        cases,
        fingerprint,
    )
    validate_frozen_adjudication_set(
        packages=packages,
        frozen=frozen,
        package_set_identity=package_set_identity,
    )
    return frozen


def validate_frozen_adjudication_set(
    *,
    packages: Sequence[BlindedAdjudicationPackage],
    frozen: FrozenAdjudicationSet,
    package_set_identity: str,
) -> None:
    """Validate complete package-set coverage without crossing the blind boundary."""
    if frozen.package_set_identity != package_set_identity:
        msg = "Frozen adjudication package-set identity differs from blinded package set."
        raise ValueError(msg)
    if frozen.protocol_version != _ADJUDICATION_SET_PROTOCOL:
        msg = "Frozen adjudication-set protocol is unsupported."
        raise ValueError(msg)
    expected_names = tuple(package.case_name for package in packages)
    actual_names = tuple(case_name for case_name, _case in frozen.cases)
    if actual_names != expected_names or len(actual_names) != len(set(actual_names)):
        msg = "Frozen adjudication cases do not exactly match blinded package order."
        raise ValueError(msg)
    package_by_name = {package.case_name: package for package in packages}
    for case_name, case_frozen in frozen.cases:
        package = package_by_name[case_name]
        validate_frozen_adjudication(package=package, frozen=case_frozen)
        if any(
            record.address_visible_to_adjudicator
            != (item.visible_address is not None)
            for record, item in zip(case_frozen.records, package.items, strict=True)
        ):
            msg = "Frozen address-visibility facts differ from the blinded package."
            raise ValueError(msg)
    designs = {package.design_fingerprint for package in packages}
    if designs != {frozen.design_fingerprint}:
        msg = "Frozen adjudication-set design differs from blinded packages."
        raise ValueError(msg)
    expected = _adjudication_set_fingerprint(
        design_fingerprint=frozen.design_fingerprint,
        package_set_identity=frozen.package_set_identity,
        protocol_version=frozen.protocol_version,
        cases=frozen.cases,
    )
    if expected != frozen.fingerprint:
        msg = "Frozen adjudication-set fingerprint no longer matches its cases."
        raise ValueError(msg)


def unblind_records(
    *,
    package: BlindedAdjudicationPackage,
    capture: CapturedCaseSurface,
    frozen: FrozenAdjudication,
    mappings: Sequence[AdjudicationResourceMapping],
) -> UnblindedAdjudication:
    """Map frozen neutral records to captured resources only for evaluation."""
    validate_frozen_adjudication(package=package, frozen=frozen)
    if frozen.design_fingerprint != capture.design_fingerprint:
        msg = "Frozen adjudication design fingerprint differs from retained capture."
        raise ValueError(msg)
    if frozen.capture_identity != capture.identity():
        msg = "Frozen adjudication capture identity differs from retained capture."
        raise ValueError(msg)
    mapping_ids = tuple(mapping.neutral_id for mapping in mappings)
    mapping_addresses = tuple(mapping.address for mapping in mappings)
    if (
        len(mapping_ids) != len(set(mapping_ids))
        or len(mapping_addresses) != len(set(mapping_addresses))
    ):
        msg = "Neutral identity mapping must remain one-to-one."
        raise ValueError(msg)
    mapping_by_id = {mapping.neutral_id: mapping.address for mapping in mappings}
    if set(mapping_by_id) != {record.neutral_id for record in frozen.records}:
        msg = "Neutral identity mapping does not match frozen adjudication records."
        raise ValueError(msg)
    if set(mapping_addresses) != set(capture.material_addresses):
        msg = "Neutral identity mapping does not cover the captured material surface."
        raise ValueError(msg)
    return UnblindedAdjudication(
        frozen.fingerprint,
        tuple(
            (mapping_by_id[record.neutral_id], record)
            for record in frozen.records
        ),
    )


def _neutral_id(*, capture: CapturedCaseSurface, address: RepositoryResourceAddress) -> str:
    value = f"{capture.design_fingerprint}|{capture.case_name}|{address.value}".encode()
    return f"resource-{hashlib.sha256(value).hexdigest()[:16]}"


def blinded_adjudication_package_identity(
    package: BlindedAdjudicationPackage,
) -> str:
    """Identify the exact adjudicator-visible question and resource evidence."""
    return hashlib.sha256(
        json.dumps(
            package,
            default=_json_default,
            separators=(",", ":"),
            sort_keys=True,
        ).encode(),
    ).hexdigest()


def _freeze_fingerprint(
    *,
    design_fingerprint: str,
    capture_identity: str,
    package_identity: str,
    protocol_version: str,
    records: Sequence[ImmutableAdjudicationRecord],
) -> str:
    payload = {
        "design": design_fingerprint,
        "capture": capture_identity,
        "package": package_identity,
        "protocol": protocol_version,
        "records": records,
    }
    return hashlib.sha256(
        json.dumps(payload, default=_json_default, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def _adjudication_set_fingerprint(
    *,
    design_fingerprint: str,
    package_set_identity: str,
    protocol_version: str,
    cases: Sequence[tuple[str, FrozenAdjudication]],
) -> str:
    payload = {
        "design": design_fingerprint,
        "package_set": package_set_identity,
        "protocol": protocol_version,
        "cases": cases,
    }
    return hashlib.sha256(
        json.dumps(payload, default=_json_default, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def _json_default(value: object) -> object:
    if isinstance(value, UsefulnessJudgment):
        return value.value
    if hasattr(value, "__slots__"):
        return {slot: getattr(value, slot) for slot in value.__slots__}
    raise TypeError(f"Cannot serialize {type(value).__name__}.")
