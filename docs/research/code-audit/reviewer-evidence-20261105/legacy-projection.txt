# Copyright (c) 2026
"""Bounded task-local claims and host attestations, selected into Context."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from typing import TYPE_CHECKING, Literal

from devtools.context.working.evidence import SourceAnchor, SourceBinding, coverage

if TYPE_CHECKING:
    from collections.abc import Mapping

type NoteKind = Literal[
    "source",
    "hypothesis",
    "relationship",
    "question",
    "conclusion",
]
KINDS = {"source", "hypothesis", "relationship", "question", "conclusion"}
MAXIMUM_NOTES = 32


@dataclass(frozen=True, slots=True)
class NoteScope:
    """Bind existing task, actor/role and episode identities without inventing IDs."""

    task: str
    role: str
    episode: str

    def __post_init__(self) -> None:
        """Require explicit finite provenance at the consumer boundary."""
        if any(not v.strip() or len(v) > 256 for v in asdict(self).values()):  # noqa: PLR2004
            msg = "Working notes require bounded task, role and episode identities."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class WorkingNote:
    """An immutable scoped claim; verification is an explicit host attestation."""

    sequence: int
    kind: NoteKind
    text: str
    expected_contract: str
    support: tuple[SourceAnchor, ...] = ()
    contradicts: tuple[int, ...] = ()
    supersedes: tuple[int, ...] = ()
    verification: str | None = None


class WorkingNotes:
    """Retain notes independently of active messages, never a Memory database.

    The consumer persists the checkpoint in its existing authenticated episode.
    Restoring trusted checkpoints is distinct from admitting model-written notes.
    Source bindings are reconstructed from original disclosures, not checkpoints.
    """

    def __init__(
        self,
        scope: NoteScope,
        sources: Mapping[str, SourceBinding],
    ) -> None:
        """Start one isolated notebook over explicitly approved source evidence."""
        self.scope = scope
        self.sources = dict(sources)
        self._notes: list[WorkingNote] = []

    @property
    def notes(self) -> tuple[WorkingNote, ...]:
        """Expose immutable history, including superseded and stale claims."""
        return tuple(self._notes)

    def record(  # noqa: PLR0913 -- explicit claim, contract and supporting evidence
        self,
        kind: NoteKind,
        text: str,
        expected_contract: str,
        support: tuple[SourceAnchor, ...] = (),
        *,
        contradicts: tuple[int, ...] = (),
        supersedes: tuple[int, ...] = (),
    ) -> WorkingNote:
        """Admit a provisional model claim, never a verified semantic assertion."""
        if (
            len(self._notes) >= MAXIMUM_NOTES
            or kind not in KINDS
            or (not text if kind == "source" else not text.strip())
            or len(text) > 1024  # noqa: PLR2004 -- finite task-local notes
            or len(expected_contract) > 1024  # noqa: PLR2004
            or (kind != "question" and not expected_contract.strip())
            or len(support) > 4  # noqa: PLR2004
            or (kind == "source" and not support)
        ):
            msg = "Invalid or exhausted working-note bounds."
            raise ValueError(msg)
        for anchor in support:
            if anchor.reference not in self.sources or not self.sources[
                anchor.reference
            ].current(anchor):
                msg = "Working note cites unavailable or stale evidence."
                raise ValueError(msg)
        for sequence in (*contradicts, *supersedes):
            if type(sequence) is not int or not 1 <= sequence <= len(self._notes):
                msg = "Working note relation names an unavailable predecessor."
                raise ValueError(msg)
        if any(self._notes[n - 1].verification for n in supersedes):
            msg = "A model note cannot supersede a host verification."
            raise ValueError(msg)
        note = WorkingNote(
            len(self._notes) + 1,
            kind,
            text,
            expected_contract,
            support,
            contradicts,
            supersedes,
        )
        self._notes.append(note)
        return note

    def observe(self, anchor: SourceAnchor) -> WorkingNote:
        """Verify literal source quotation only, never an arbitrary paraphrase."""
        note = self.record("source", anchor.quote, "exact source quotation", (anchor,))
        verified = replace(note, verification="host:exact-source-quotation")
        self._notes[-1] = verified
        return verified

    def attest(self, sequence: int, verification: str) -> WorkingNote:
        """Record explicit trusted-host verification, unavailable to model input.

        The receipt identifies the host's checking process, not a framework proof
        of general semantics. The original model claim remains in history.
        """
        if (
            type(sequence) is not int
            or not 1 <= sequence <= len(self._notes)
            or not verification.strip()
            or len(verification) > 256  # noqa: PLR2004
        ):
            msg = "Host verification needs an exact note and check receipt."
            raise ValueError(msg)
        old = self._notes[sequence - 1]
        note = self.record(
            old.kind,
            old.text,
            old.expected_contract,
            old.support,
            contradicts=old.contradicts,
        )
        verified = replace(note, supersedes=(sequence,), verification=verification)
        self._notes[-1] = verified
        return verified

    def status(self, note: WorkingNote) -> str:
        """Derive applicability and dispute state without deleting historical notes."""
        superseded = {sequence for n in self._notes for sequence in n.supersedes}
        if note.sequence in superseded:
            return "superseded"
        if any(
            a.reference not in self.sources or not self.sources[a.reference].current(a)
            for a in note.support
        ):
            return "stale"
        opponents = [
            n
            for n in self._notes
            if note.sequence in n.contradicts and n.sequence not in superseded
        ]
        if any(
            n.verification
            and all(
                a.reference in self.sources and self.sources[a.reference].current(a)
                for a in n.support
            )
            for n in opponents
        ):
            return "contradicted"
        if opponents:
            return "contested"
        return "host-verified" if note.verification else "provisional"

    def checkpoint(self) -> dict[str, object]:
        """Serialize notes; original source remains with its evidence owner."""
        return {
            "schema": "task-role-working-notes-v1",
            "scope": asdict(self.scope),
            "notes": [asdict(n) for n in self._notes],
        }

    def restore(self, scope: NoteScope, notes: tuple[WorkingNote, ...]) -> None:
        """Restore a trusted episode checkpoint, never raw model output or authority."""
        if self._notes or scope != self.scope or len(notes) > MAXIMUM_NOTES:
            msg = "Working checkpoint has incompatible role/episode or bounds."
            raise ValueError(msg)
        if any(n.sequence != i for i, n in enumerate(notes, 1)):
            msg = "Working checkpoint note sequence is inconsistent."
            raise ValueError(msg)
        self._notes.extend(notes)

    def project(self, maximum_bytes: int) -> dict[str, object]:
        """Select whole notes and bounded coverage; omitted notes remain recoverable."""
        if type(maximum_bytes) is not int or maximum_bytes <= 0:
            msg = "Working Context requires a positive finite byte bound."
            raise ValueError(msg)
        sources = []
        for binding in self.sources.values():
            merged, gaps = coverage(len(binding.resource.content), binding.spans)
            sources.append(
                {
                    "reference": binding.reference,
                    "resource": str(binding.resource.address),
                    "version": str(binding.resource.content_identity),
                    "snapshot": str(binding.snapshot) if binding.snapshot else None,
                    "verified_disclosed_ranges": merged,
                    "unread_gaps": gaps,
                    "origin": "restored-baseline"
                    if binding.live
                    else "retained-subject",
                },
            )
        selected = [
            {**asdict(note), "status": self.status(note)} for note in self._notes
        ]
        view: dict[str, object] = {
            "kind": "task_role_working_context",
            "scope": asdict(self.scope),
            "rule": (
                "Model notes are fallible claims, not repository facts or authority. "
                "Host verification is scoped to its stated check. Historical ranges "
                "are not proof source is active after Context reduction; "
                "reopen exact evidence."
            ),
            "sources": sources,
            "notes": selected,
            "omitted_notes": 0,
            "omitted_sources": 0,
        }
        while len(json.dumps(view, ensure_ascii=False).encode()) > maximum_bytes:
            if selected:
                selected.pop(0)
                view["omitted_notes"] = len(self._notes) - len(selected)
            elif sources:
                sources.pop()
                view["omitted_sources"] = len(self.sources) - len(sources)
            else:
                msg = "Mandatory working Context cannot fit its byte budget."
                raise ValueError(msg)
        return view
