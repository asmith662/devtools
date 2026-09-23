# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM102, PLR2004, TC001, TRY003
"""Retain Increment-23 mechanism evidence without consulting judgments."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import PurposeProfile
from experiments.purpose_relative_admission.direct_resolution import (
    DirectResolutionControlResult,
)
from experiments.purpose_relative_admission.reservation import (
    DirectionalReservationResult,
    RelationshipSurface,
    RetainedRelationshipTarget,
)
from experiments.purpose_relative_admission.validation_design import (
    ValidationRoute,
)
from experiments.purpose_relative_import.comparison import RankedLexicalSurface


@dataclass(frozen=True, slots=True)
class RepositoryCheckpoint:
    """Identity and bounded acquisition facts for one later real capture."""

    repository_id: str
    snapshot_id: str
    corpus_id: str
    document_count: int
    acquisition_bounds: tuple[tuple[str, int], ...]


@dataclass(frozen=True, slots=True)
class CapturedDirectResolutionControl:
    """Retain a direct-resolution result outside heterogeneous K=5 evidence."""

    name: str
    result: DirectResolutionControlResult


@dataclass(frozen=True, slots=True)
class CapturedCaseSurface:
    """One judgment-free bounded surface and all typed mechanism provenance."""

    case_name: str
    information_need: str
    query_text: str
    profile: PurposeProfile
    route: ValidationRoute
    design_fingerprint: str
    checkpoint: RepositoryCheckpoint
    lexical_top_five: tuple[RankedLexicalSurface, ...]
    lexical_top_fifteen: tuple[RankedLexicalSurface, ...]
    top_fifteen_adjudication_addresses: tuple[RepositoryResourceAddress, ...]
    outgoing_surfaces: tuple[RelationshipSurface, ...]
    incoming_surfaces: tuple[RelationshipSurface, ...]
    profile_eligible_surfaces: tuple[RelationshipSurface, ...]
    retained_targets: tuple[RetainedRelationshipTarget, ...]
    practical: DirectionalReservationResult
    blind_reference_input: tuple[RelationshipSurface, ...]
    blind_reference_top_five: tuple[RepositoryResourceAddress, ...]
    oracle_top_five: tuple[RepositoryResourceAddress, ...] | None

    def __post_init__(self) -> None:
        """Reject capture records that could not be replayed deterministically."""
        if len(self.lexical_top_five) != 5:
            msg = "A heterogeneous capture requires exactly five canonical lexical results."
            raise ValueError(msg)
        if tuple(item.address for item in self.lexical_top_five) != self.practical.addresses[:5] and self.practical.disposition.value == "abstained":
            msg = "An abstaining practical result must preserve canonical lexical top five."
            raise ValueError(msg)
        if self.profile_eligible_surfaces and any(
            surface.direction is not self.practical.direction
            for surface in self.profile_eligible_surfaces
        ):
            msg = "Eligible relationship surfaces must retain only the profile direction."
            raise ValueError(msg)

    @property
    def rank_five_address(self) -> RepositoryResourceAddress:
        """Expose the sole lexical resource at reservation risk."""
        return self.lexical_top_five[4].address

    @property
    def material_addresses(self) -> tuple[RepositoryResourceAddress, ...]:
        """Deduplicate adjudication resources without discarding retained evidence."""
        ordered: list[RepositoryResourceAddress] = []
        for address in (
            *(item.address for item in self.lexical_top_five),
            *(item.address for item in self.profile_eligible_surfaces),
            *(item.address for item in self.retained_targets),
            *((self.practical.admitted_target.address,) if self.practical.admitted_target else ()),
            *self.top_fifteen_adjudication_addresses,
        ):
            if address not in ordered:
                ordered.append(address)
        return tuple(ordered)

    def identity(self) -> str:
        """Fingerprint retained evidence, including repeated relation encounters."""
        payload = {
            "case": self.case_name,
            "design": self.design_fingerprint,
            "checkpoint": self.checkpoint,
            "lexical_top_five": self.lexical_top_five,
            "lexical_top_fifteen": self.lexical_top_fifteen,
            "top_fifteen_adjudication_addresses": self.top_fifteen_adjudication_addresses,
            "outgoing": self.outgoing_surfaces,
            "incoming": self.incoming_surfaces,
            "eligible": self.profile_eligible_surfaces,
            "retained": self.retained_targets,
            "practical": self.practical,
            "blind_input": self.blind_reference_input,
            "blind_top_five": self.blind_reference_top_five,
            "oracle_top_five": self.oracle_top_five,
        }
        return _fingerprint(payload)


def captured_direct_resolution_control(
    *, name: str, result: DirectResolutionControlResult
) -> CapturedDirectResolutionControl:
    """Wrap an existing typed direct-resolution result without K=5 interpretation."""
    if result.applicable_to_heterogeneous_k5_metrics:
        msg = "Direct-resolution controls must remain outside heterogeneous K=5 metrics."
        raise ValueError(msg)
    return CapturedDirectResolutionControl(name, result)


def _fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, default=_json_default, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def _json_default(value: object) -> object:
    if isinstance(value, RepositoryResourceAddress):
        return value.value
    if isinstance(value, ImportRelationshipDirection | PurposeProfile | ValidationRoute):
        return value.value
    if hasattr(value, "__dict__"):
        return value.__dict__
    if hasattr(value, "__slots__"):
        return {slot: getattr(value, slot) for slot in value.__slots__}
    raise TypeError(f"Cannot serialize {type(value).__name__}.")
