# Copyright (c) 2026
"""Python-source address candidates projected from repository discovery.

This bounded selector inspects only canonical repository-relative addresses
from a completed discovery result. A positive result means only that an address
ends with the exact, case-sensitive ``.py`` suffix used by this local
convention. It does not inspect or classify resource content.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.repository.discovery import RepositoryResourceDiscovery
    from devtools.context.repository.resource import RepositoryResourceAddress


@dataclass(frozen=True, slots=True)
class PythonSourceAddressCandidateEvidence:
    """Record the native address observation supporting one candidate."""

    matched_suffix: str

    MECHANISM: ClassVar[str] = "exact-case-sensitive-dot-py-address-suffix-v1"
    NATIVE_OBSERVATION: ClassVar[str] = "repository-address-ends-with-dot-py"


@dataclass(frozen=True, slots=True)
class PythonSourceAddressCandidate:
    """Retain one discovered address and its local candidacy evidence."""

    address: RepositoryResourceAddress
    evidence: PythonSourceAddressCandidateEvidence


@dataclass(frozen=True, slots=True)
class PythonSourceAddressCandidateSelection:
    """Retain one purpose-sensitive projection over completed discovery."""

    discovery: RepositoryResourceDiscovery
    candidates: tuple[PythonSourceAddressCandidate, ...]

    @property
    def addresses(self) -> tuple[RepositoryResourceAddress, ...]:
        """Expose candidate addresses in their original discovery order."""
        return tuple(candidate.address for candidate in self.candidates)


def select_python_source_address_candidates(
    discovery: RepositoryResourceDiscovery,
) -> PythonSourceAddressCandidateSelection:
    """Nominate exact lowercase ``.py`` discovered addresses as candidates."""
    suffix = ".py"
    return PythonSourceAddressCandidateSelection(
        discovery=discovery,
        candidates=tuple(
            PythonSourceAddressCandidate(
                address=address,
                evidence=PythonSourceAddressCandidateEvidence(
                    matched_suffix=suffix,
                ),
            )
            for address in discovery.addresses
            if address.value.endswith(suffix)
        ),
    )
