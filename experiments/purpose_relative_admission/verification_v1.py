# Copyright (c) 2026
"""Versioned, read-only binding verification; never rerun a scientific policy.

The original v1/v2 producers and consumers remain frozen. These adapters check
their canonical pair/order contract before returning labels for new analysis.
Internal consistency is not independent authentication of caller-supplied bytes.
"""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Any

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.purpose_relative_admission.validation_adjudication import (
    UnblindedAdjudication,
    unblind_records,
)
from experiments.purpose_relative_admission.validation_execution import (
    _digest,
    load_blinded_adjudication_packages,
    load_frozen_adjudication_artifact,
    validate_artifact_correspondence,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from experiments.purpose_relative_admission.validation_adjudication import (
        AdjudicationResourceMapping,
        BlindedAdjudicationPackage,
        FrozenAdjudication,
    )
    from experiments.purpose_relative_admission.validation_capture import (
        CapturedCaseSurface,
    )

VERSION = "increment-23-canonical-binding-verification-v1"
_PROTOCOL = "increment-23-blinded-adjudication-v2"
_SCHEMAS = (
    "devtools-b0002-increment-23-hidden-surface-capture-v1",
    "devtools-b0002-increment-23-blinded-adjudication-package-v2",
    "devtools-b0002-increment-23-neutral-resource-mapping-v1",
    "devtools-b0002-increment-23-frozen-adjudication-v2",
)


def _pairs(
    design: str,
    case: str,
    addresses: Sequence[RepositoryResourceAddress],
) -> tuple[tuple[str, RepositoryResourceAddress], ...]:
    """Reconstruct the frozen producer's exact neutral-ID preimage, not a new ID."""
    return tuple(
        (
            "resource-"
            + hashlib.sha256(f"{design}|{case}|{address.value}".encode()).hexdigest()[
                :16
            ],
            address,
        )
        for address in addresses
    )


def verified_unblind_records(
    *,
    package: BlindedAdjudicationPackage,
    capture: CapturedCaseSurface,
    frozen: FrozenAdjudication,
    mappings: Sequence[AdjudicationResourceMapping],
) -> UnblindedAdjudication:
    """Require canonical pairs and order before the original unblinding boundary."""
    if package.protocol_version != _PROTOCOL or frozen.protocol_version != _PROTOCOL:
        msg = "Unsupported historical binding protocol."
        raise ValueError(msg)
    if (package.case_name, package.information_need) != (
        capture.case_name,
        capture.information_need,
    ):
        msg = "Package question differs from its capture."
        raise ValueError(msg)
    expected = _pairs(
        capture.design_fingerprint,
        capture.case_name,
        capture.material_addresses,
    )
    actual = tuple((m.neutral_id, m.address) for m in mappings)
    if actual != expected or len({p[0] for p in expected}) != len(expected):
        msg = "Canonical neutral/address bindings or order differ from capture."
        raise ValueError(msg)
    for mapping, item, record in zip(
        mappings,
        package.items,
        frozen.records,
        strict=True,
    ):
        if (
            type(mapping.address_visible_to_adjudicator) is not bool
            or record.address_visible_to_adjudicator
            != mapping.address_visible_to_adjudicator
            or mapping.address_visible_to_adjudicator
            != (item.visible_address is not None)
            or (
                item.visible_address is not None
                and item.visible_address != mapping.address.value
            )
        ):
            msg = "Mapping visibility differs from the blinded package."
            raise ValueError(msg)
    return unblind_records(
        package=package,
        capture=capture,
        frozen=frozen,
        mappings=mappings,
    )


def _capture_identity(case: Mapping[str, Any]) -> str:
    """Project the exact CapturedCaseSurface.identity v1 descriptor from saved JSON."""
    fields = {
        "case": "case_name",
        "design": "design_fingerprint",
        "checkpoint": "checkpoint",
        "lexical_top_five": "lexical_top_five",
        "lexical_top_fifteen": "lexical_top_fifteen",
        "top_fifteen_adjudication_addresses": "top_fifteen_adjudication_addresses",
        "outgoing": "outgoing_surfaces",
        "incoming": "incoming_surfaces",
        "eligible": "profile_eligible_surfaces",
        "retained": "retained_targets",
        "practical": "practical",
        "blind_input": "blind_reference_input",
        "blind_top_five": "blind_reference_top_five",
        "oracle_top_five": "oracle_top_five",
    }
    return _digest({key: case[value] for key, value in fields.items()})


def _material(case: Mapping[str, Any]) -> tuple[RepositoryResourceAddress, ...]:
    """Reconstruct ordered material membership without retrieval or label access."""
    admitted = case["practical"]["admitted_target"]
    addresses = [
        *(item["address"] for item in case["lexical_top_five"]),
        *(item["address"] for item in case["profile_eligible_surfaces"]),
        *(item["address"] for item in case["retained_targets"]),
        *([admitted["address"]] if admitted is not None else []),
        *case["top_fifteen_adjudication_addresses"],
    ]
    return tuple(dict.fromkeys(RepositoryResourceAddress(value) for value in addresses))


def verify_artifact_bindings(
    *,
    capture: Mapping[str, Any],
    package: Mapping[str, Any],
    mapping: Mapping[str, Any],
    frozen: Mapping[str, Any],
) -> dict[str, UnblindedAdjudication]:
    """Check supported retained artifacts before any new positional/ranked analysis.

    Callers must separately authenticate original input bytes and custody. No
    ranks, metrics, judgments or source are generated, repaired or persisted.
    """
    try:
        return _verify(capture, package, mapping, frozen)
    except (KeyError, TypeError) as error:
        msg = "Incomplete or malformed historical binding artifacts."
        raise ValueError(msg) from error


def _verify(
    capture: Mapping[str, Any],
    package: Mapping[str, Any],
    mapping: Mapping[str, Any],
    frozen: Mapping[str, Any],
) -> dict[str, UnblindedAdjudication]:
    if tuple(x.get("schema") for x in (capture, package, mapping, frozen)) != _SCHEMAS:
        msg = "Unsupported historical binding schemas."
        raise ValueError(msg)
    if not validate_artifact_correspondence(
        capture=capture,
        package=package,
        mapping=mapping,
    ):
        msg = "Historical artifact envelopes or capture links differ."
        raise ValueError(msg)
    cp, mp = capture["payload"], mapping["payload"]
    cases = cp["cases"]
    identities = tuple(_capture_identity(case) for case in cases)
    if (
        list(identities) != cp["case_capture_identities"]
        or list(identities) != mp["case_capture_identities"]
    ):
        msg = "Case capture identities do not reconstruct."
        raise ValueError(msg)
    expected_capture = _digest(
        {
            "design_fingerprint": cp["design_fingerprint"],
            "rule_fingerprint": cp["rule_fingerprint"],
            "checkpoint": cp["repository_checkpoint"]["checkpoint"],
            "case_capture_identities": identities,
            "direct_controls": cp["direct_resolution_controls"],
        },
    )
    if cp["capture_set_identity"] != expected_capture or mp[
        "mapping_set_identity"
    ] != _digest(
        {
            "capture_set_identity": expected_capture,
            "mappings": mp["mappings"],
        },
    ):
        msg = "Capture or mapping set identity does not reconstruct."
        raise ValueError(msg)
    packages = load_blinded_adjudication_packages(package)
    frozen_set = load_frozen_adjudication_artifact(
        envelope=frozen,
        packages=packages,
        package_set_identity=package["payload"]["package_set_identity"],
    )
    names = tuple(case["case_name"] for case in cases)
    if (
        not names
        or len(set(names)) != len(names)
        or names != tuple(p.case_name for p in packages)
    ):
        msg = "Captured case population/order differs from packages."
        raise ValueError(msg)
    result = {}
    for case, identity, p, (_, f), bindings in zip(
        cases,
        identities,
        packages,
        frozen_set.cases,
        mp["mappings"],
        strict=True,
    ):
        result[p.case_name] = _verify_case(case, identity, p, f, bindings)
    return result


def _verify_case(
    case: Mapping[str, Any],
    identity: str,
    p: BlindedAdjudicationPackage,
    f: FrozenAdjudication,
    bindings: Sequence[Mapping[str, Any]],
) -> UnblindedAdjudication:
    """Verify one ordered canonical join after authenticating enclosing artifacts."""
    if p.protocol_version != _PROTOCOL or (
        p.capture_identity,
        p.design_fingerprint,
        p.information_need,
    ) != (identity, case["design_fingerprint"], case["information_need"]):
        msg = "Captured question/frame differs from package."
        raise ValueError(msg)
    pairs = _pairs(case["design_fingerprint"], case["case_name"], _material(case))
    actual = tuple(
        (b["neutral_id"], RepositoryResourceAddress(b["address"])) for b in bindings
    )
    if (
        actual != pairs
        or len({x[0] for x in pairs}) != len(pairs)
        or tuple(x[0] for x in pairs) != tuple(r.neutral_id for r in f.records)
    ):
        msg = "Canonical neutral/address bindings or positional order differ."
        raise ValueError(msg)
    for b, item, (_, address) in zip(bindings, p.items, pairs, strict=True):
        if (
            type(b["address_visible_to_adjudicator"]) is not bool
            or b["address_visible_to_adjudicator"] != (item.visible_address is not None)
            or item.visible_address not in (None, address.value)
        ):
            msg = "Mapping visibility differs from the blinded package."
            raise ValueError(msg)
    return UnblindedAdjudication(
        f.fingerprint,
        tuple(
            (address, record)
            for (_, address), record in zip(pairs, f.records, strict=True)
        ),
    )
