# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- bounded prospective review adapter
"""Independent review working Context over existing subject and read receipts."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from devtools.agents.coding.protocol import arguments
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.working import (
    NoteScope,
    SourceAnchor,
    SourceBinding,
    WorkingNote,
    WorkingNotes,
)
from devtools.models.interaction import PromptMessage

if TYPE_CHECKING:
    from devtools.context.planning.source import SourceRangeDisclosureOption
    from devtools.context.repository.snapshot import RepositorySnapshot
    from scripts.backlog.native.execution import Capture

PROJECTION_BYTES = 8192
CONTRACT = {"schema": "review-working-notes-v1", "projection_bytes": PROJECTION_BYTES}
PREFIX = "WORKING_NOTES\n"
MAXIMUM_BATCH = 8
PROCEDURE = """Evidence-first independent review: claim -> expected contract -> exact
observed evidence -> contradiction/uncertainty check -> supported finding.
Matching quotation proves the quotation, not your interpretation. Passing checks
or a cited source do not prove a defect. Keep hypotheses and unresolved questions
explicit; prefer insufficient-evidence to an invented blocking defect. Verify
helper/caller relationships against both source units before relying on them.
You may retain notes in assistant content alongside an existing read_source call;
no additional model call is needed per note. Use WORKING_NOTES followed by newline
and JSON {"working_notes":[{"kind":"hypothesis","text":"claim",
"expected_contract":"requirement or explicit uncertainty","support":[
{"reference":"candidate","start":0,"end":1,"quote":"exact character"}],
"contradicts":[],"supersedes":[]}]}. Kinds: source, hypothesis, relationship,
question, conclusion. Every note is provisional, even source claims. Only the host
can verify; no model field can declare truth. Quotes use half-open Unicode offsets
inside disclosed ranges. At most 8 notes per response, 32 retained including
revisions, 1024 characters per text/contract, 4 support quotes of 512 characters.
Use predecessor sequence numbers to correct/supersede your provisional notes or
record a contradiction. Missing evidence is a question, not proof of absence.
Live evidence reopens through read_source under existing read authorization;
archived candidate quotes reopen from retained subject Context, never the live
baseline at the same path. Source coverage is disclosure, not semantic assessment.
On the final reserved call submit the unchanged submit_review_proposal contract;
notes alone are not a conclusion and do not create more calls, reads or authority.
"""


class ReviewNotes:
    """Consumer adapter; persistence stays in the native immutable capture."""

    def __init__(
        self,
        packet: dict[str, Any],
        snapshot: RepositorySnapshot,
        capture: Capture,
    ) -> None:
        """Seed only the independent subject; never coding/private host records."""
        self.capture = capture
        self.scope = NoteScope(
            packet["subject"]["item"],
            "independent-reviewer:" + packet["policy"]["actor"],
            packet["sha256"],
        )
        evidence = packet["subject"]["evidence"]
        sources = {}
        for name in ("baseline", "candidate"):
            value = evidence[name]
            resource = RepositoryResourceOccurrence(
                RepositoryResourceAddress(value["path"]),
                ContentIdentity.from_text(value["text"]),
                value["text"],
                "utf-8",
                len(value["text"].encode()),
            )
            live = (
                name == "baseline" and value["path"] in packet["policy"]["read_paths"]
            )
            if live:
                actual = snapshot.resource_at(resource.address)
                if actual.content != resource.content:
                    raise ValueError("Working baseline differs from current snapshot")
                resource = actual
            sources[name] = SourceBinding(
                name,
                resource,
                packet["subject"]["references"][name],
                ((0, len(resource.content)),),
                snapshot.id if live else None,
                live=live,
            )
        for resource in snapshot.resources:
            path = str(resource.address)
            if (
                path in packet["policy"]["read_paths"]
                and path != evidence["baseline"]["path"]
            ):
                name = "source:" + path
                sources[name] = SourceBinding(
                    name,
                    resource,
                    packet["subject"]["inputs"][path],
                    (),
                    snapshot.id,
                    live=True,
                )
        self.book = WorkingNotes(self.scope, sources)

    def persist(self, origin: str) -> None:
        """Charge a checkpoint to the existing finite episode capture budget."""
        self.capture.add(
            "review-working-state",
            {"state": self.book.checkpoint(), "origin": origin},
        )

    def observed(self, reference: str, option: SourceRangeDisclosureOption) -> None:
        """Register only completed exact disclosures, never read preflight intent."""
        binding = SourceBinding(
            reference,
            option.unit.resource,
            option.identity,
            (option.span,),
            option.snapshot_id,
            live=True,
        )
        self.book.sources[reference] = binding
        key = "source:" + str(option.unit.resource.address)
        if key in self.book.sources:
            old = self.book.sources[key]
            self.book.sources[key] = SourceBinding(
                key,
                binding.resource,
                binding.receipt,
                (*old.spans, option.span),
                binding.snapshot,
                live=True,
            )
        start, end = option.span
        if start < end:
            end = min(end, start + 512)
            self.book.observe(
                binding.anchor(start, end, option.unit.resource.content[start:end]),
            )
        self.persist("completed-read:" + reference)

    def accept(self, content: str, origin: str) -> bool:
        """Validate a whole optional note batch; model input cannot attest facts."""
        if not content.startswith(PREFIX):
            return False
        value = arguments(content.removeprefix(PREFIX), {"working_notes"})
        rows = value["working_notes"]
        if not isinstance(rows, list) or not 1 <= len(rows) <= MAXIMUM_BATCH:
            raise ValueError("Invalid finite review working-note batch")
        following = WorkingNotes(self.scope, self.book.sources)
        following.restore(self.scope, self.book.notes)
        for row in rows:
            # Existing strict decoder rejects duplicate/extra members recursively.
            note: dict[str, Any] = arguments(
                json.dumps(row),
                {
                    "kind",
                    "text",
                    "expected_contract",
                    "support",
                    "contradicts",
                    "supersedes",
                },
            )
            if not all(
                isinstance(note[k], str) for k in ("kind", "text", "expected_contract")
            ) or not all(
                isinstance(note[k], list)
                for k in ("support", "contradicts", "supersedes")
            ):
                raise ValueError("Invalid working-note field types")
            anchors = []
            for item in note["support"]:
                anchor: dict[str, Any] = arguments(
                    json.dumps(item),
                    {"reference", "start", "end", "quote"},
                )
                ref = anchor["reference"]
                if not isinstance(ref, str) or ref not in following.sources:
                    raise ValueError("Unavailable independent source reference")
                anchors.append(
                    following.sources[ref].anchor(
                        anchor["start"],
                        anchor["end"],
                        anchor["quote"],
                    ),
                )
            following.record(
                note["kind"],
                note["text"],
                note["expected_contract"],
                tuple(anchors),
                contradicts=tuple(note["contradicts"]),
                supersedes=tuple(note["supersedes"]),
            )
        self.book = following
        self.persist(origin)
        return True

    def message(self) -> PromptMessage:
        """Reassemble bounded working Context independently of retained raw history."""
        overhead = (
            len(
                json.dumps(
                    {"procedure": PROCEDURE, "working_context": {}},
                    ensure_ascii=False,
                ).encode(),
            )
            - 2
        )
        value = {
            "procedure": PROCEDURE,
            "working_context": self.book.project(PROJECTION_BYTES - overhead),
        }
        text = json.dumps(value, ensure_ascii=False)
        if len(text.encode()) > PROJECTION_BYTES:
            raise ValueError("Review working Context exceeds its declared bound")
        return PromptMessage("user", text)

    def restore(self, state: dict[str, Any]) -> None:
        """Recover only an authenticated episode state; source receipts stay separate.

        Caller reconstructs this adapter's bindings from the approved subject and
        completed read receipts before supplying the latest sealed checkpoint.
        This operation grants no redispatch/resume authority to a consumed review.
        """
        if (
            set(state) != {"schema", "scope", "notes"}
            or state["schema"] != "task-role-working-notes-v1"
        ):
            raise ValueError("Unsupported working-note checkpoint")
        scope = NoteScope(**state["scope"])
        notes = tuple(
            WorkingNote(
                **{
                    **n,
                    "support": tuple(
                        SourceAnchor(
                            **{
                                **a,
                                "resource": RepositoryResourceAddress(
                                    a["resource"]["value"],
                                ),
                                "version": ContentIdentity(a["version"]["value"]),
                                "snapshot": RepositorySnapshotId(a["snapshot"]["value"])
                                if a["snapshot"]
                                else None,
                            },
                        )
                        for a in n["support"]
                    ),
                    "contradicts": tuple(n["contradicts"]),
                    "supersedes": tuple(n["supersedes"]),
                },
            )
            for n in state["notes"]
        )
        following = WorkingNotes(self.scope, self.book.sources)
        following.restore(scope, notes)
        self.book = following
