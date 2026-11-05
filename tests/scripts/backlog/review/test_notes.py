# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, ANN401, PLC0414 -- deterministic boundary fixtures
"""Independent working Context; simulated responses are not live-model evidence."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import Any

import pytest

from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.document import RepositoryTextDocumentId
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval.source.representation import RepositorySourceUnit
from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from scripts.backlog.native.review.notes import CONTRACT, PREFIX, ReviewNotes
from tests.context.working.test_notes import binding
from tests.scripts.backlog.test_native import (
    PUBLIC,
    conclusion,
    native_candidate,
    review_response,
    reviewer_policy,
)
from tests.scripts.backlog.test_native import (
    repository as repository,
)
from tests.scripts.backlog.test_review_acquisition import MemoryCapture


def setup() -> tuple[dict[str, Any], RepositorySnapshot, MemoryCapture]:
    resource = binding("base").resource
    helper = replace(
        binding("helper source").resource,
        address=type(resource.address)("helper.py"),
    )
    snapshot = RepositorySnapshot(
        RepositorySnapshotId("a" * 64),
        RepositoryId.new(),
        (resource, helper),
    )
    packet = {
        "sha256": "b" * 64,
        "subject": {
            "item": "task",
            "inputs": {"fixture.py": "old", "helper.py": "helper"},
            "references": {
                "baseline": "baseline-receipt",
                "candidate": "candidate-receipt",
            },
            "evidence": {
                "baseline": {"path": "fixture.py", "text": "base"},
                "candidate": {"path": "fixture.py", "text": "candidate"},
            },
        },
        "policy": {
            "actor": "separate reviewer",
            "read_paths": ["fixture.py", "helper.py"],
        },
    }
    return packet, snapshot, MemoryCapture()


def note(**changes: Any) -> dict[str, Any]:
    return {
        "kind": "hypothesis",
        "text": "Candidate may violate a contract",
        "expected_contract": "Verify source before deciding",
        "support": [{"reference": "candidate", "start": 0, "end": 1, "quote": "c"}],
        "contradicts": [],
        "supersedes": [],
        **changes,
    }


def payload(*notes: dict[str, Any]) -> str:
    return PREFIX + json.dumps({"working_notes": list(notes)})


def test_independent_evidence_and_read_gap_context() -> None:
    packet, snapshot, capture = setup()
    memory = ReviewNotes(packet, snapshot, capture)
    assert memory.book.sources["candidate"].snapshot is None
    assert memory.book.sources["baseline"].snapshot == snapshot.id
    assert (
        memory.book.sources["candidate"].resource
        != memory.book.sources["baseline"].resource
    )
    view = json.loads(memory.message().content)["working_context"]
    helper = next(s for s in view["sources"] if s["reference"] == "source:helper.py")
    assert helper["unread_gaps"] == [[0, len("helper source")]]
    assert not memory.accept("Ordinary assistant prose", "model")
    assert memory.accept(payload(note()), "model-response:digest")
    assert memory.book.status(memory.book.notes[0]) == "provisional"
    assert capture.values[-1]["origin"] == "model-response:digest"


@pytest.mark.parametrize(
    "fault",
    [
        "verification",
        "private",
        "unread",
        "quote",
        "type",
        "empty",
        "many",
        "missing",
        "duplicate",
    ],
)
def test_model_cannot_mint_truth_or_cite_unread_private_data(fault: str) -> None:
    packet, snapshot, capture = setup()
    memory = ReviewNotes(packet, snapshot, capture)
    row = note()
    if fault == "verification":
        row["verification"] = "model says verified"
    elif fault == "private":
        row["support"][0]["reference"] = "private-acceptance-implementation"
    elif fault == "unread":
        row["support"] = [
            {"reference": "source:helper.py", "start": 0, "end": 1, "quote": "h"},
        ]
    elif fault == "quote":
        row["support"][0]["quote"] = "invented"
    elif fault == "type":
        row["supersedes"] = "not a list"
    elif fault == "missing":
        del row["text"]
    text = payload(note(), row)
    if fault == "empty":
        text = payload()
    elif fault == "many":
        text = payload(*(note() for _ in range(9)))
    elif fault == "duplicate":
        text = PREFIX + '{"working_notes":[],"working_notes":[]}'
    with pytest.raises(
        ValueError,
        match=r"(?i)invalid|match|reference|interval|duplicate",
    ):
        memory.accept(text, "model")
    assert not memory.book.notes  # Entire batch refused before checkpoint mutation.
    assert not capture.values


def test_completed_reads_and_checkpoint_reconstruction() -> None:
    packet, snapshot, capture = setup()
    memory = ReviewNotes(packet, snapshot, capture)
    assert memory.accept(payload(note()), "response")
    resource = snapshot.resources[1]
    unit = RepositorySourceUnit(
        RepositoryTextDocumentId("c" * 64),
        snapshot.repository_id,
        resource,
        snapshot.id,
        "file",
        0,
        len(resource.content),
    )
    option = SourceRangeDisclosureOption("review", unit, 0, 6, 100)
    memory.observed("read:1", option)
    assert memory.book.status(memory.book.notes[-1]) == "host-verified"
    state = json.loads(json.dumps(capture.values[-1]["state"]))
    # Reconstruct original source bindings from the completed read, then notes;
    # raw historical model messages can be absent from the next Context.
    recovered = ReviewNotes(packet, snapshot, MemoryCapture())
    recovered.observed("read:1", option)
    recovered.restore(state)
    assert recovered.message() == memory.message()
    wrong = json.loads(json.dumps(state))
    wrong["scope"]["role"] = "coding-worker"
    with pytest.raises(ValueError, match="incompatible"):
        recovered.restore(wrong)
    with pytest.raises(ValueError, match="Unsupported"):
        recovered.restore({"schema": "unknown"})
    other = json.loads(json.dumps(packet))
    other["subject"]["evidence"]["baseline"]["text"] = "drift"
    with pytest.raises(ValueError, match="baseline"):
        ReviewNotes(other, snapshot, MemoryCapture())


def test_subject_baseline_outside_read_scope_cannot_gain_live_tool_pointer() -> None:
    packet, snapshot, capture = setup()
    packet["policy"]["read_paths"] = ["helper.py"]
    memory = ReviewNotes(packet, snapshot, capture)
    source = memory.book.sources["baseline"]
    assert source.reopen(source.anchor(0, 1, "b"))["read_source"] is None


def test_native_reviewer_keeps_notes_across_reads_and_reserved_final_call(
    repository: Any,
) -> None:
    cycle, item = repository

    class Reviewer:
        source = InteractionSource("neutral-review-a")
        calls = 0

        async def send(self, request: ModelRequest) -> ModelResponse:
            self.calls += 1
            assert not any(
                m.content.startswith(PREFIX) for m in request.prompt.messages
            )
            state = json.loads(request.prompt.messages[-1].content)["working_context"]
            assert state["scope"]["role"].startswith("independent-reviewer:")
            if self.calls == 1:
                assert not state["notes"]
                subject = json.loads(request.prompt.messages[1].content)["subject"]
                quote = subject["evidence"]["candidate"]["text"][:1]
                row = note(
                    support=[
                        {
                            "reference": "candidate",
                            "start": 0,
                            "end": 1,
                            "quote": quote,
                        },
                    ],
                )
                return ModelResponse(
                    payload(row),
                    self.source,
                    termination=ModelTermination.TOOL_CALL,
                    tool_calls=(
                        ModelToolCall(
                            "read_source",
                            json.dumps({"path": PUBLIC, "start": 0, "end": 10}),
                            "read-once",
                        ),
                    ),
                )
            if self.calls == 2:
                assert state["notes"][0]["status"] == "provisional"
                assert any(n["verification"] for n in state["notes"])
                return ModelResponse(
                    payload(
                        note(
                            kind="question",
                            text="Prior claim is unresolved",
                            support=[],
                            supersedes=[1],
                        ),
                    ),
                    self.source,
                )
            assert state["notes"][0]["status"] == "superseded"
            assert [t.name for t in request.tools] == ["submit_review_proposal"]
            return review_response(request, self.source, conclusion())

    async def run() -> None:
        await native_candidate(cycle, item)
        packet = await cycle.native.reviewer.prepare(
            item,
            reviewer=reviewer_policy(),
            working_notes=True,
        )
        assert packet["working_notes"] == CONTRACT
        await cycle.native.reviewer.authorize(
            item,
            reference="fixture://independent-notes",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        model = Reviewer()
        result = await cycle.native.reviewer.execute(
            item,
            interaction=model,
            profile="review-script-v1",
            authorize=lambda _: True,
        )
        assert result["status"] == "proposed", result
        assert result["model_calls"] == 3
        assert result["reads"] == 1
        assert not result["host_approved"]
        folder = cycle.native.reviewer.folder(item)
        records = [
            json.loads((folder / x["file"]).read_bytes())
            for x in result["observations"]
        ]
        states = [x["state"] for x in records if x["kind"] == "review-working-state"]
        assert len(states) == 4
        assert states[-1]["notes"][0]["verification"] is None
        assert any(n["supersedes"] == [1] for n in states[-1]["notes"])
        assert not any("private" in json.dumps(x).lower() for x in states)

    asyncio.run(run())


def test_worst_case_note_projection_stays_bounded() -> None:
    packet, snapshot, capture = setup()
    memory = ReviewNotes(packet, snapshot, capture)
    for _ in range(32):
        memory.book.record("question", "?" * 1024, "")
    message = memory.message()
    assert len(message.content.encode()) <= 8192
    assert json.loads(message.content)["working_context"]["omitted_notes"]
