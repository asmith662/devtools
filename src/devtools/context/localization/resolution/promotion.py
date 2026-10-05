# Copyright (c) 2026
# ruff: noqa: COM812
"""Explicit complete-support seam into the existing accepted witness algebra."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.localization.assessment import (
    LocalizationEvidenceReference,
    SupportedWitness,
)
from devtools.context.localization.obligation import WitnessSet
from devtools.context.localization.resolution.contract import (
    HypothesisResolutionDisposition,
)
from devtools.context.localization.resolution.view import WitnessResolutionView

if TYPE_CHECKING:
    from devtools.context.localization.association.hypothesis import (
        CandidateHypothesisIdentity,
    )
    from devtools.context.localization.resolution.contract import (
        CandidateHypothesisResolution,
    )


@dataclass(frozen=True, slots=True)
class PromotedWitnessHypothesis:
    """Supply accepted values while retaining every explicit resolution decision."""

    resolution: CandidateHypothesisResolution

    def __post_init__(self) -> None:
        """Permit only complete explicit all-member support."""
        WitnessResolutionView(self.resolution.candidates, self.resolution.members)
        if (
            self.resolution.disposition
            is not HypothesisResolutionDisposition.COMPLETELY_SUPPORTED
        ):
            msg = "Witness promotion requires a completely supported hypothesis."
            raise ValueError(msg)

    @property
    def witness_set(self) -> WitnessSet:
        """Reuse native targets and existing complementary witness algebra."""
        return WitnessSet(tuple(item.member.target for item in self.resolution.members))

    @property
    def supported_witnesses(self) -> tuple[SupportedWitness, ...]:
        """Retain native evidence references and the immutable caller decision."""
        return tuple(
            SupportedWitness(
                item.member.target,
                (
                    *item.basis,
                    LocalizationEvidenceReference(
                        item, item.repository_id, item.snapshot_id
                    ),
                ),
            )
            for item in self.resolution.members
        )


def promote_supported_hypothesis(
    view: WitnessResolutionView, identity: CandidateHypothesisIdentity
) -> PromotedWitnessHypothesis:
    """Explicitly create accepted values; mutate no assessment or readiness."""
    resolution = view.for_hypothesis(identity)
    if resolution is None:
        msg = "Witness promotion requires a recorded hypothesis resolution."
        raise ValueError(msg)
    return PromotedWitnessHypothesis(resolution)
