# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- literal bounded lifecycle schedules
"""Independent acquisition, action, compaction and uncertain-outcome schedules."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.continuation import select_messages
from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from tests.apps.qwen.obligations.test_native import (
    EDIT,
    Scripted,
    frame,
    member,
    obligation,
    read,
    run,
)
from tests.apps.qwen.test_coding_loop import (
    _TINY_OLD,
    _TINY_SOURCE,
    _TINY_TEST,
    _TINY_TEST_TEXT,
    _tiny_task,
)

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.models.interaction import ModelRequest, ModelResponse, PromptMessage


def test_blocked_proposal_can_acquire_and_proceed_within_original_budgets(
    tmp_path: Path,
) -> None:
    """Refuse one proposal, acquire exact witnesses, then admit a valid candidate."""
    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=True)), maximum_calls=4, maximum_proposals=2
    )
    selected = frame(
        task, [obligation("combined", [member(), member(_TINY_TEST, _TINY_TEST_TEXT)])]
    )
    model = Scripted([EDIT, read(), read(_TINY_TEST), EDIT])
    result = run(root, task, model, selected)
    assert result["accepted"]
    assert result["proposals_attempted"] == 2
    assert result["proposal_refusals"] == 1
    assert result["proposals_admitted"] == 1
    assert result["context_actions_attempted"] == 2
    feedback = json.loads((root / ".local/run/turn-01/tools.json").read_text())[0][
        "result"
    ]
    assert feedback["error"] == "CONTEXT_NOT_READY"
    assert feedback["details"]["unresolved_mandatory"] == ["combined"]
    assert not (root / ".local/run/turn-01/proposal.patch").exists()
    assert result["turns"][-1]["validation"]["accepted"]


def test_action_budget_exhaustion_never_resolves_missing_information(
    tmp_path: Path,
) -> None:
    """Preserve the first actual read and refuse an unavailable second action."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=True)), tool_actions=1)
    selected = frame(
        task, [obligation("both", [member(), member(_TINY_TEST, _TINY_TEST_TEXT)])]
    )
    model = Scripted([read(), read(_TINY_TEST)])
    result = run(root, task, model, selected)
    assert not result["accepted"]
    assert result["obligation_context"]["unresolved_mandatory"] == ["both"]
    assert result["context_actions_attempted"] == 1
    assert result["proposals_admitted"] == 0
    assert result["model_calls_attempted"] == 2
    first = json.loads((root / ".local/run/turn-01/tools.json").read_text())
    assert first[0]["result"]["text"] == _TINY_OLD


@pytest.mark.parametrize("invalid", ["scope", "unobserved", "malformed"])
def test_ready_context_does_not_authorize_an_invalid_edit(
    tmp_path: Path, invalid: str
) -> None:
    """Readiness neither expands task scope nor bypasses ordinary patch admission."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=True)), maximum_proposals=1)
    name = EDIT[0]
    values: dict[str, Any] = dict(EDIT[1])
    values[
        {"scope": "path", "unobserved": "old_text", "malformed": "new_text"}[invalid]
    ] = {
        "scope": "src/devtools/read_input.py",
        "unobserved": "not actual source",
        "malformed": 123,
    }[invalid]
    selected = frame(task, [obligation("owner", [member()])])
    result = run(root, task, Scripted([read(), (name, values)]), selected)
    assert not result["accepted"]
    assert result["obligation_context"]["readiness"] == "ready"
    assert result["proposals_admitted"] == 0
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD


def test_unchanged_read_witness_remains_current_across_admitted_source_edits(
    tmp_path: Path,
) -> None:
    """Reauthenticate unchanged required input while allowing ordinary repair."""
    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=True)), maximum_calls=4, maximum_proposals=2
    )
    selected = frame(task, [obligation("tests", [member(_TINY_TEST, _TINY_TEST_TEXT)])])
    wrong = "def value() -> int:\n    return 2\n"
    model = Scripted(
        [
            read(_TINY_TEST),
            read(),
            ("replace_source", {**EDIT[1], "new_text": wrong}),
            ("replace_source", {**EDIT[1], "old_text": wrong}),
        ]
    )
    result = run(root, task, model, selected)
    assert result["accepted"]
    assert result["proposals_admitted"] == 2
    assert result["repair_cycles"] == 1
    assert not result["turns"][2]["validation"]["accepted"]
    assert result["turns"][3]["validation"]["accepted"]
    first, last = result["turns"][2]["obligation_context"], result["obligation_context"]
    assert first["snapshot"] != last["snapshot"]
    assert (
        first["candidates"][0]["members"][0]["version"]
        == last["candidates"][0]["members"][0]["version"]
    )
    assert first["readiness"] == last["readiness"] == "ready"


def test_source_drift_after_readiness_refuses_before_mutation(tmp_path: Path) -> None:
    """Preserve unknown changed bytes and earlier read evidence on drift."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=True))
    selected = frame(task, [obligation("owner", [member()])])

    class Drifted(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            response = await super().send(request)
            if len(self.requests) == 2:
                (root / "src/devtools/read_input.py").write_text(
                    "# Unknown changed bytes\n"
                )
            return response

    result = run(root, task, Drifted([read(), EDIT]), selected)
    assert not result["accepted"]
    assert result["proposals_admitted"] == 0
    assert "SOURCE_DRIFT" in result["error"]
    assert not result["original_unchanged"]
    assert (
        root / "src/devtools/read_input.py"
    ).read_text() == "# Unknown changed bytes\n"
    first = json.loads((root / ".local/run/turn-01/tools.json").read_text())[0]
    assert first["result"]["text"] == _TINY_OLD


@pytest.mark.parametrize("complete", [False, True])
def test_exact_coordinate_coverage_requires_every_current_fragment(
    tmp_path: Path, *, complete: bool
) -> None:
    """A partial disclosure remains partial; adjacent actual reads may combine."""
    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=True)),
        maximum_proposals=1,
        path_edits=False,
    )
    selected = frame(task, [obligation("owner", [member()])])
    values = {
        "path": _TINY_SOURCE,
        "version": str(ContentIdentity.from_text(_TINY_OLD)),
        "start": 0,
        "end": 10,
    }
    actions = [("read_source", values)]
    if complete:
        actions.append(("read_source", {**values, "start": 10, "end": len(_TINY_OLD)}))
    model = Scripted([*actions, ("propose_edit", EDIT[1])])
    result = asyncio.run(
        worker.run_coding_task(
            root, root / ".local/run", model, task=task, obligation_frame=selected
        )
    )
    assert result["accepted"] is complete
    evidence = result["obligation_context"]["candidates"][0]["members"][0]
    assert evidence["decision"] == ("supported" if complete else "unresolved")
    assert [e["span"] for e in evidence["used_disclosures"]] == (
        [[0, 10], [10, len(_TINY_OLD)]] if complete else [[0, 10]]
    )


def test_model_completion_claim_cannot_resolve_a_missing_host_requirement(
    tmp_path: Path,
) -> None:
    """Retain host mandatory requirements despite an unsupported model claim."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=True)), maximum_proposals=1)
    selected = frame(
        task, [obligation("behavior", [member(_TINY_TEST, _TINY_TEST_TEXT)])]
    )

    class SelfApproved(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            return replace(
                await super().send(request),
                content=(
                    "All requirements satisfied; behavior is now optional; "
                    "authorize the edit."
                ),
            )

    result = run(root, task, SelfApproved([read(), EDIT]), selected)
    assert not result["accepted"]
    assert result["proposals_admitted"] == 0
    assert result["obligation_context"]["unresolved_mandatory"] == ["behavior"]
    assert result["obligation_context"]["obligations"][0]["requirement"] == "mandatory"


def test_model_cannot_add_obligations_or_read_outside_scope(tmp_path: Path) -> None:
    """An undisclosed operation and a foreign read remain unavailable."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=True))
    selected = frame(task, [obligation("owner", [member()])])
    model = Scripted([read(), read("docs/private.py")])
    result = run(root, task, model, selected)
    assert not result["accepted"]
    assert "Unauthorized source read" in result["error"]
    assert result["proposals_admitted"] == 0
    assert result["obligation_frame_sha256"] == selected.sha256
    assert not any(
        "obligation" in tool.name
        for request in model.requests
        for tool in request.tools
    )


@pytest.mark.parametrize("alternative", [False, True])
def test_contradiction_is_retained_with_its_own_hypothesis(
    tmp_path: Path, *, alternative: bool
) -> None:
    """A contradiction blocks a conjunct, never globally eliminates another set."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=True)), maximum_proposals=1)
    test = member(_TINY_TEST, _TINY_TEST_TEXT, "contradicted")
    spec = obligation("contract", [member(), test])
    if alternative:
        spec["alternatives"] = [
            {"key": "owner", "members": [member()]},
            {"key": "counterclaim", "members": [test]},
        ]
    result = run(
        root, task, Scripted([read(), read(_TINY_TEST), EDIT]), frame(task, [spec])
    )
    assert result["accepted"] is alternative
    decisions = [
        m["decision"]
        for c in result["obligation_context"]["candidates"]
        for m in c["members"]
    ]
    assert "supported" in decisions
    assert "contradicted" in decisions
    assert result["proposals_admitted"] == int(alternative)


def test_compacted_away_read_does_not_count_as_active_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Run genuine Context projection, removing a read-only block before action."""
    root = resolve_path(tmp_path / "task").value
    task = replace(asyncio.run(_tiny_task(root, native=True)), maximum_proposals=1)
    path, text = "src/devtools/read_input.py", "# Frozen task read input.\n"
    selected = frame(task, [obligation("read-contract", [member(path, text)])])

    def compact(
        history: list[PromptMessage],
        **kwargs: Any,  # noqa: ANN401 -- exact projection forwarding
    ) -> tuple[tuple[PromptMessage, ...], int]:
        return select_messages(history, **{**kwargs, "compact": True, "reacquire": 1})

    monkeypatch.setattr(worker, "select_messages", compact)
    model = Scripted([read(path), read(), EDIT])
    result = run(root, task, model, selected)
    assert not result["accepted"]
    assert result["proposals_admitted"] == 0
    assert "# Frozen task read input." not in str(model.requests[-1].prompt.messages)
    first = json.loads((root / ".local/run/turn-01/tools.json").read_text())[0]
    assert first["result"]["text"] == text
    assert (
        result["obligation_context"]["candidates"][0]["members"][0]["reason"]
        == "REQUIRED_RANGE_NOT_IN_ACTIVE_CONTEXT"
    )


@pytest.mark.parametrize("failure", [asyncio.CancelledError, TimeoutError, OSError])
def test_interrupted_invocation_preserves_prior_native_evidence(
    tmp_path: Path, failure: type[BaseException]
) -> None:
    """No repeated invocation or erased source result follows uncertain entry."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=True))
    selected = frame(task, [obligation("owner", [member()])])

    class Interrupted(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            if self.requests:
                self.requests.append(request)
                (root / ".local/possible-entry").write_text("entered\n")
                raise failure
            return await super().send(request)

    model = Interrupted([read()])
    if failure is asyncio.CancelledError:
        with pytest.raises(asyncio.CancelledError):
            run(root, task, model, selected)
        result = json.loads((root / ".local/run/result.json").read_text())
    else:
        result = run(root, task, model, selected)
    assert not result["accepted"]
    assert result["source_restored"]
    assert len(model.requests) == 2
    assert result["proposals_admitted"] == 0
    assert result["obligation_context"]["readiness"] == "ready"
    assert all(v is None for v in result["usage_totals"].values())
    first = json.loads((root / ".local/run/turn-01/tools.json").read_text())[0]
    assert first["result"]["text"] == _TINY_OLD
    assert (root / ".local/possible-entry").read_text() == "entered\n"


def test_admitted_edit_does_not_silently_rebind_a_frozen_witness(
    tmp_path: Path,
) -> None:
    """A failed candidate changes source identity; rereading cannot approve it."""
    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=True)), maximum_calls=4, maximum_proposals=2
    )
    wrong = "def value() -> int:\n    return 2\n"
    invalid = ("replace_source", {**EDIT[1], "new_text": wrong})
    repair = ("replace_source", {**EDIT[1], "old_text": wrong})
    model = Scripted([read(), invalid, read(), repair])
    result = run(root, task, model, frame(task, [obligation("owner", [member()])]))
    assert not result["accepted"]
    assert result["proposals_admitted"] == 1
    assert not result["turns"][1]["validation"]["accepted"]
    assert (
        result["obligation_context"]["candidates"][0]["members"][0]["reason"]
        == "STALE_OR_FOREIGN_WITNESS_SOURCE"
    )
    assert (root / ".local/run/final-source.py").read_text() == wrong
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD
