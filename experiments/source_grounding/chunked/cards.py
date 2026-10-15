# Copyright (c) 2026
"""Evidence-card bounds and exact sizing under the authenticated JSON disclosure."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from hashlib import sha256

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.orchestration.workers.budget import BudgetError, FailureClass

SUMMARY_CHARACTERS = 512
UNCERTAINTY_CHARACTERS = 256
MAX_LOCATORS = 4
AGGREGATE_QUOTE_CHARACTERS = 4096
TRANSPORT_CHARACTERS = 1048576
MAX_CELLS = 10000


class EvidenceState(StrEnum):
    """Local evidence judgments, distinct from final global gold labels."""

    USEFUL = "USEFUL"
    NO_USEFUL = "NO_USEFUL"
    UNCERTAIN = "UNCERTAIN"


class ResolutionState(StrEnum):
    """A2 resolves evidence, never final global necessity or a new negative."""

    EVIDENCE_FOUND = "EVIDENCE_FOUND"
    REMAINS_UNCERTAIN = "REMAINS_UNCERTAIN"


@dataclass(frozen=True)
class EvidenceCard:
    """Bounded semantic disclosure; exact quotes belong to the host archive."""

    cell_id: str
    source_key: str
    obligation_id: str
    state: EvidenceState
    summary: str
    evidence_ids: tuple[str, ...]
    uncertainty_note: str
    representation_complete: bool
    resolution_state: ResolutionState = ResolutionState.EVIDENCE_FOUND

    def validate(self) -> None:
        """Overflow or incomplete representation is never a scientific negative."""
        self.summary.encode("utf-8", errors="strict")
        self.uncertainty_note.encode("utf-8", errors="strict")
        if (
            not self.representation_complete
            or not self.summary.strip()
            or len(self.summary) > SUMMARY_CHARACTERS
            or len(self.uncertainty_note) > UNCERTAINTY_CHARACTERS
            or len(self.evidence_ids) > MAX_LOCATORS
        ):
            raise BudgetError(
                FailureClass.EVIDENCE_REPRESENTATION_LIMIT,
                "Incomplete or overflowing EvidenceCard; do not truncate or relabel",
            )
        if (
            len(set(self.evidence_ids)) != len(self.evidence_ids)
            or self.state == EvidenceState.NO_USEFUL
            or (
                self.state == EvidenceState.USEFUL
                and self.resolution_state != ResolutionState.EVIDENCE_FOUND
            )
            or (
                self.resolution_state == ResolutionState.EVIDENCE_FOUND
                and not self.evidence_ids
            )
            or (
                self.resolution_state == ResolutionState.REMAINS_UNCERTAIN
                and (self.evidence_ids or not self.uncertainty_note)
            )
        ):
            message = "EvidenceCard state/evidence/uncertainty mismatch"
            raise ValueError(message)


def worst_case_cards(cell_count: int) -> bytes:
    """Size permitted Unicode values, granting short packet-local reference IDs.

    U+1F600 is one legal Unicode code point and twelve characters in the current
    ensure_ascii JSON representation. This is a representational stress fixture,
    not a semantic judgment on any real resource. No resource text is consulted.
    The packet envelope/instructions are deliberately absent: this is already a
    lower bound on the full maximum rendered disclosure.
    """
    return json_bytes(
        {
            "cards": [
                asdict(card) for card in maximal_cards(cell_count, reference_digits=4)
            ],
        },
    )


def maximal_cards(
    cell_count: int,
    *,
    reference_digits: int = 5,
) -> tuple[EvidenceCard, ...]:
    """Build the same maximum free-text stress frame for lossless codecs."""
    if not 0 < cell_count <= MAX_CELLS:
        message = "Unsupported prospective cell-count bound"
        raise ValueError(message)
    cards = []
    for index in range(cell_count):
        card = EvidenceCard(
            cell_id=f"c{index:04d}",
            source_key=sha256(str(index // 2).encode()).hexdigest(),
            obligation_id=f"O{index % 2 + 1}",
            state=EvidenceState.UNCERTAIN,
            summary="\U0001f600" * SUMMARY_CHARACTERS,
            evidence_ids=tuple(
                f"e{index * 4 + i:0{reference_digits}d}" for i in range(4)
            ),
            uncertainty_note="\U0001f600" * UNCERTAINTY_CHARACTERS,
            representation_complete=True,
        )
        card.validate()
        cards.append(card)
    return tuple(cards)


def require_strong_fit(rendered: bytes) -> None:
    """Enforce the prospective seventy-percent ceiling before plan creation."""
    count = len(rendered.decode("utf-8", errors="strict"))
    if count * 10 > TRANSPORT_CHARACTERS * 7:
        raise BudgetError(
            FailureClass.TRANSPORT_CHARACTER_LIMIT,
            f"Pass-B lower-bound disclosure {count} chars exceeds 70% of "
            f"{TRANSPORT_CHARACTERS}; no prospective plan may be produced",
        )
